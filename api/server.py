"""
FastAPI server for Math Agent engine.

Exposes /items/generate and /grade endpoints.
See api/CONTRACTS.md for request/response schemas.
"""

import os
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, Literal
from collections import OrderedDict
import asyncio
import time

from engine.templates import generate_item, SKILL_TEMPLATES
from engine.grader import grade_response
from engine.validators import validate_item


# ============================================================================
# Cycle Manager (inline to avoid import issues in tests)
# ============================================================================

PoolKey = tuple  # (session_id, skill_id, difficulty)


class LRUSeenBags:
    """
    Simple LRU cache for seen stems to avoid unbounded growth.
    Keyed by (session_id, skill_id, difficulty) -> set of stems.
    """

    def __init__(self, max_entries: int = 1000):
        self.max_entries = max_entries
        self._bags: dict = {}
        self._lru: OrderedDict = OrderedDict()
        self._lock = asyncio.Lock()

    async def mark_seen(self, key: PoolKey, stem: str) -> None:
        """Mark a stem as seen in this pool."""
        async with self._lock:
            bag = self._bags.setdefault(key, set())
            bag.add(stem)
            self._touch(key)

    async def has_seen(self, key: PoolKey, stem: str) -> bool:
        """Check if a stem has been seen in this pool."""
        async with self._lock:
            self._touch(key)
            return stem in self._bags.get(key, set())

    async def size(self, key: PoolKey) -> int:
        """Get the number of unique stems seen in this pool."""
        async with self._lock:
            self._touch(key)
            return len(self._bags.get(key, set()))

    async def clear(self, key: PoolKey) -> None:
        """Clear all seen stems for this pool (start a new cycle)."""
        async with self._lock:
            self._bags[key] = set()
            self._touch(key)

    def _touch(self, key: PoolKey) -> None:
        """Update LRU timestamp for this key."""
        now = time.time()
        if key in self._lru:
            self._lru.move_to_end(key)
        self._lru[key] = now


# Singleton for the app lifetime
cycle_bags = LRUSeenBags(max_entries=2000)


app = FastAPI(title="Math Agent API", version="0.1.0")


# ============================================================================
# Request/Response Models (Pydantic)
# ============================================================================

class GenerateItemRequest(BaseModel):
    """Request schema for POST /items/generate"""
    skill_id: str
    difficulty: Optional[str] = None
    seed: Optional[int] = None
    mode: Literal["random", "cycle"] = "random"
    session_id: Optional[str] = None


class ChoiceSchema(BaseModel):
    """Choice object in item"""
    id: str
    text: str


class GenerateItemResponse(BaseModel):
    """Response schema for POST /items/generate"""
    item_id: str
    skill_id: str
    difficulty: str
    stem: str
    choices: List[ChoiceSchema]
    solution_choice_id: str
    solution_text: str
    tags: List[str]


class GradeRequest(BaseModel):
    """Request schema for POST /grade"""
    item: dict
    choice_id: str


class GradeResponse(BaseModel):
    """Response schema for POST /grade"""
    correct: bool
    solution_choice_id: str
    explanation: str


class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str
    message: str


# ============================================================================
# Endpoints
# ============================================================================

@app.post("/items/generate", response_model=GenerateItemResponse)
async def generate_item_endpoint(request: GenerateItemRequest):
    """
    Generate a new math question item.
    
    Supports two modes:
    - "random" (default): standard random generation
    - "cycle": deterministic no-repeat within (session_id, skill_id, difficulty)
    
    See api/CONTRACTS.md for full specification.
    
    Args:
        request: GenerateItemRequest with skill_id, difficulty (optional), seed (optional), mode, session_id
    
    Returns:
        GenerateItemResponse matching the item schema
    
    Raises:
        HTTPException 400: invalid_skill, invalid_difficulty, invalid_seed, missing_session_id
    """
    # Validate cycle mode parameters
    if request.mode == "cycle" and not request.session_id:
        raise HTTPException(
            status_code=400,
            detail={"error": "missing_session_id", "message": "session_id is required when mode='cycle'"}
        )
    
    # Fast path: random mode (unchanged)
    if request.mode != "cycle":
        try:
            item = generate_item(
                skill_id=request.skill_id,
                difficulty=request.difficulty,
                seed=request.seed,
            )
            return GenerateItemResponse(**item)
        except ValueError as e:
            error_msg = str(e)
            
            # Map engine errors to API errors
            if error_msg == "unknown_skill":
                raise HTTPException(
                    status_code=400,
                    detail={"error": "invalid_skill", "message": f"Unknown skill_id: {request.skill_id}"}
                )
            elif error_msg == "invalid_difficulty":
                raise HTTPException(
                    status_code=400,
                    detail={"error": "invalid_difficulty", "message": f"Invalid difficulty: {request.difficulty}"}
                )
            elif error_msg == "invalid_seed":
                raise HTTPException(
                    status_code=400,
                    detail={"error": "invalid_seed", "message": f"Seed must be an integer, got {type(request.seed).__name__}"}
                )
            else:
                raise HTTPException(status_code=500, detail={"error": "internal_error", "message": str(e)})
    
    # Cycle mode: guarantee no repeats until pool exhausted
    difficulty = request.difficulty or "easy"
    
    # Validate skill and difficulty exist
    
    skill_templates = SKILL_TEMPLATES.get(request.skill_id)
    if not skill_templates:
        raise HTTPException(
            status_code=400,
            detail={"error": "invalid_skill", "message": f"Unknown skill_id: {request.skill_id}"}
        )
    
    if difficulty not in skill_templates:
        raise HTTPException(
            status_code=400,
            detail={"error": "invalid_difficulty", "message": f"Invalid difficulty: {difficulty}"}
        )
    
    pool = skill_templates[difficulty]
    if not pool:
        raise HTTPException(
            status_code=400,
            detail={"error": "invalid_difficulty", "message": f"No templates for {difficulty}"}
        )
    
    # Cycle mode logic
    pool_key = (request.session_id, request.skill_id, difficulty)  # type: ignore
    pool_size = len(pool)
    
    # If bag is full, clear it (start a new cycle)
    current_seen_size = await cycle_bags.size(pool_key)
    if current_seen_size >= pool_size:
        await cycle_bags.clear(pool_key)
    
    # Try to find an unseen template
    max_attempts = min(8, pool_size * 2)
    last_item = None
    
    for attempt in range(max_attempts):
        item = generate_item(
            skill_id=request.skill_id,
            difficulty=difficulty,
            seed=None,  # randomness within cycle mode
        )
        stem = item.get("stem", "")
        
        if not await cycle_bags.has_seen(pool_key, stem):
            # Found an unseen stem
            await cycle_bags.mark_seen(pool_key, stem)
            return GenerateItemResponse(**item)
        
        last_item = item
    
    # Fallback: couldn't find unseen after max attempts (tiny pool or bad luck)
    # Clear bag and return one fresh
    await cycle_bags.clear(pool_key)
    item = generate_item(
        skill_id=request.skill_id,
        difficulty=difficulty,
        seed=None,
    )
    stem = item.get("stem", "")
    await cycle_bags.mark_seen(pool_key, stem)
    return GenerateItemResponse(**item)


@app.post("/grade", response_model=GradeResponse)
async def grade_endpoint(request: GradeRequest):
    """
    Grade a student's response to a question.
    
    See api/CONTRACTS.md for full specification.
    
    Args:
        request: GradeRequest with item dict and choice_id
    
    Returns:
        GradeResponse with correct flag, solution_choice_id, and explanation
    
    Raises:
        HTTPException 400: invalid_item, invalid_choice_id, missing_field
    """
    # Validate that required fields are present
    if "item" not in request.__dict__ or request.item is None:
        raise HTTPException(
            status_code=400,
            detail={"error": "missing_field", "message": "Missing required field: item"}
        )
    if "choice_id" not in request.__dict__ or request.choice_id is None:
        raise HTTPException(
            status_code=400,
            detail={"error": "missing_field", "message": "Missing required field: choice_id"}
        )
    
    try:
        result = grade_response(item=request.item, choice_id=request.choice_id)
        return GradeResponse(**result)
    except ValueError as e:
        error_msg = str(e)
        
        # Map engine errors to API errors
        if error_msg == "invalid_choice_id":
            raise HTTPException(
                status_code=400,
                detail={"error": "invalid_choice_id", "message": f"choice_id must be A-D, got: {request.choice_id}"}
            )
        elif error_msg.startswith("invalid_item"):
            # Extract error code if propagated: "invalid_item:<code>"
            error_code = error_msg.split(":")[1] if ":" in error_msg else "unknown"
            raise HTTPException(
                status_code=400,
                detail={"error": "invalid_item", "message": f"Item validation failed: {error_code}"}
            )
        else:
            # Unexpected error
            raise HTTPException(status_code=500, detail={"error": "internal_error", "message": str(e)})


# ============================================================================
# Health check (for sanity testing)
# ============================================================================

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


# ============================================================================
# Static Files (Web UI)
# ============================================================================

# Resolve web directory relative to project root
WEB_DIR = str(Path(__file__).parent.parent / "web")

# Mount static files at root with SPA support (html=True serves index.html for any route)
app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="web")
