"""
FastAPI server for Math Agent engine.

Exposes /items/generate and /grade endpoints.
See api/CONTRACTS.md for request/response schemas.
"""

import os
import sys
import json
import time
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, Literal, Dict, Any
from collections import OrderedDict
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from engine.templates import generate_item, SKILL_TEMPLATES
from engine.grader import grade_response
from engine.validators import validate_item

# Import cycle_manager - use absolute import with fallback
try:
    from api.cycle_manager import cycle_bags
except ImportError:
    import importlib.util
    spec = importlib.util.spec_from_file_location("cycle_manager", os.path.join(os.path.dirname(__file__), "cycle_manager.py"))
    if spec and spec.loader:
        cycle_manager_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cycle_manager_module)
        cycle_bags = cycle_manager_module.cycle_bags
    else:
        raise ImportError("Could not load cycle_manager")

# Import telemetry - use absolute import with fallback
try:
    from api.telemetry import log_event
except ImportError:
    import importlib.util
    spec = importlib.util.spec_from_file_location("telemetry", os.path.join(os.path.dirname(__file__), "telemetry.py"))
    if spec and spec.loader:
        telemetry_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(telemetry_module)
        log_event = telemetry_module.log_event
    else:
        raise ImportError("Could not load telemetry")


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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add security headers middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    # Core security headers (conservative defaults)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    
    # CSP – strict (no inline scripts/styles, safe for our static-only UI)
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self'; "
        "img-src 'self' data:; "
        "connect-src 'self'; "
        "font-src 'self'; "
        "object-src 'none'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self'"
    )
    return response


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
            t0 = time.time()
            item = generate_item(
                skill_id=request.skill_id,
                difficulty=request.difficulty,
                seed=request.seed,
            )
            latency_ms = float((time.time() - t0) * 1000.0)
            
            # Log telemetry (async, don't await in sync path; fire-and-forget)
            try:
                asyncio.create_task(log_event(
                    "generate",
                    session_id=request.session_id,
                    mode="random",
                    skill_id=item["skill_id"],
                    difficulty=item["difficulty"],
                    item_id=item["item_id"],
                    stem=item["stem"],
                    choice_ids=[c["id"] for c in item["choices"]],
                    latency_ms=latency_ms,
                ))
            except Exception:
                pass  # fail-open: don't crash if telemetry fails
            
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
    t0 = time.time()
    pool_key = (request.session_id, request.skill_id, difficulty)  # type: ignore
    pool_size = len(pool)
    
    # If bag is full, clear it (start a new cycle) and emit cycle_reset
    current_seen_size = await cycle_bags.size(pool_key)
    if current_seen_size >= pool_size:
        await cycle_bags.clear(pool_key)
        # Emit cycle_reset event
        try:
            await log_event(
                "cycle_reset",
                session_id=request.session_id,
                skill_id=request.skill_id,
                difficulty=difficulty,
            )
        except Exception:
            pass  # fail-open
    
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
            latency_ms = float((time.time() - t0) * 1000.0)
            
            # Log telemetry
            try:
                await log_event(
                    "generate",
                    session_id=request.session_id,
                    mode="cycle",
                    skill_id=item["skill_id"],
                    difficulty=item["difficulty"],
                    item_id=item["item_id"],
                    stem=item["stem"],
                    choice_ids=[c["id"] for c in item["choices"]],
                    latency_ms=latency_ms,
                )
            except Exception:
                pass  # fail-open
            
            return GenerateItemResponse(**item)
        
        last_item = item
    
    # Fallback: couldn't find unseen after max attempts (tiny pool or bad luck)
    # Clear bag and emit cycle_reset
    await cycle_bags.clear(pool_key)
    try:
        await log_event(
            "cycle_reset",
            session_id=request.session_id,
            skill_id=request.skill_id,
            difficulty=difficulty,
        )
    except Exception:
        pass  # fail-open
    
    item = generate_item(
        skill_id=request.skill_id,
        difficulty=difficulty,
        seed=None,
    )
    stem = item.get("stem", "")
    await cycle_bags.mark_seen(pool_key, stem)
    latency_ms = float((time.time() - t0) * 1000.0)
    
    # Log telemetry (fallback case)
    try:
        await log_event(
            "generate",
            session_id=request.session_id,
            mode="cycle",
            skill_id=item["skill_id"],
            difficulty=item["difficulty"],
            item_id=item["item_id"],
            stem=item["stem"],
            choice_ids=[c["id"] for c in item["choices"]],
            latency_ms=latency_ms,
        )
    except Exception:
        pass  # fail-open
    
    return GenerateItemResponse(**item)


# ============================================================================
# Telemetry Helper
# ============================================================================

def log_telemetry(event: str, **kwargs) -> None:
    """
    Log event to telemetry JSONL file (non-blocking, fail-open).
    
    Args:
        event: Event type (e.g., "cycle_generate", "graded")
        **kwargs: Additional fields to log
    """
    try:
        log_dir = Path(__file__).parent.parent / "var"
        log_dir.mkdir(exist_ok=True)
        
        log_entry = {
            "t": time.time(),
            "event": event,
            **kwargs
        }
        
        with open(log_dir / "events.jsonl", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception:
        # Fail open: don't crash the API if telemetry fails
        pass


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
        t0 = time.time()
        result = grade_response(item=request.item, choice_id=request.choice_id)
        latency_ms = float((time.time() - t0) * 1000.0)
        
        # Log telemetry (async, fire-and-forget)
        try:
            asyncio.create_task(log_event(
                "grade",
                session_id=None,  # simplest for now; link via item_id
                skill_id=request.item.get("skill_id"),
                difficulty=request.item.get("difficulty"),
                item_id=request.item.get("item_id"),
                choice_id=request.choice_id,
                correct=result["correct"],
                solution_choice_id=result["solution_choice_id"],
                latency_ms=latency_ms,
            ))
        except Exception:
            pass  # fail-open: don't crash if telemetry fails
        
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


@app.get("/healthz")
async def healthz():
    """Kubernetes-compatible health check endpoint."""
    return {"status": "ok"}


@app.get("/skills/manifest")
async def skills_manifest() -> Dict[str, Dict[str, int]]:
    """
    Get pool sizes for all skills and difficulties.
    
    Useful for UI to dynamically set POOL_SIZE_HINT without hardcoding.
    
    Returns:
        {
            "quad.graph.vertex": {"easy": 2, "medium": 1, "hard": 1, "applied": 1},
            ...
        }
    """
    return {
        skill_id: {difficulty: len(templates) for difficulty, templates in skill_templates.items()}
        for skill_id, skill_templates in SKILL_TEMPLATES.items()
    }


# ============================================================================
# Static Files (Web UI)
# ============================================================================

# Resolve web directory relative to project root
WEB_DIR = str(Path(__file__).parent.parent / "web")

# Mount static files at root with SPA support (html=True serves index.html for any route)
app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="web")
