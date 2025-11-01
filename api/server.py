"""
FastAPI server for Math Agent engine.

Exposes /items/generate and /grade endpoints.
See api/CONTRACTS.md for request/response schemas.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from engine.templates import generate_item
from engine.grader import grade_response
from engine.validators import validate_item


app = FastAPI(title="Math Agent API", version="0.1.0")


# ============================================================================
# Request/Response Models (Pydantic)
# ============================================================================

class GenerateItemRequest(BaseModel):
    """Request schema for POST /items/generate"""
    skill_id: str
    difficulty: Optional[str] = None
    seed: Optional[int] = None


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
    
    See api/CONTRACTS.md for full specification.
    
    Args:
        request: GenerateItemRequest with skill_id, difficulty (optional), seed (optional)
    
    Returns:
        GenerateItemResponse matching the item schema
    
    Raises:
        HTTPException 400: invalid_skill, invalid_difficulty, invalid_seed
    """
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
            # Unexpected error
            raise HTTPException(status_code=500, detail={"error": "internal_error", "message": str(e)})


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
