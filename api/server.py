"""
FastAPI server for Math Agent engine.

Exposes /items/generate and /grade endpoints.
See api/CONTRACTS.md for request/response schemas.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List


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
# Endpoints (stubs — to be implemented)
# ============================================================================

@app.post("/items/generate", response_model=GenerateItemResponse)
async def generate_item(request: GenerateItemRequest):
    """
    Generate a new math question item.
    
    See api/CONTRACTS.md for full specification.
    """
    raise NotImplementedError("Endpoint not yet implemented")


@app.post("/grade", response_model=GradeResponse)
async def grade_response(request: GradeRequest):
    """
    Grade a student's response to a question.
    
    See api/CONTRACTS.md for full specification.
    """
    raise NotImplementedError("Endpoint not yet implemented")


# ============================================================================
# Health check (for sanity testing)
# ============================================================================

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}
