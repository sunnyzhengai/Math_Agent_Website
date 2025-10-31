from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from ..services.engine_service import EngineService

router = APIRouter()

# Schemas
class Choice(BaseModel):
    id: str
    text: str
    tags_on_select: List[str] = []

class Item(BaseModel):
    item_id: str
    skill_id: str
    difficulty: str
    stem: str
    choices: List[Choice]
    hints: List[str] = []
    explanation: Optional[str] = None
    confidence_target: Optional[float] = 0.7

class NextItemRequest(BaseModel):
    user_id: str
    domain: str = "Quadratics"
    seed: Optional[int] = None

class NextItemResponse(BaseModel):
    item: Item
    reason: str
    difficulty: str
    learner_mastery_before: float

class GradeRequest(BaseModel):
    user_id: str
    item_id: str
    selected_choice_id: str
    time_ms: int
    confidence: Optional[float] = 0.5

class GradeResponse(BaseModel):
    correct: bool
    tags: List[str]
    p_mastery_after: float
    attempts_on_skill: int
    next_due_at: Optional[datetime] = None
    suggested_resource_url: Optional[str] = None

@router.post("/next-item", response_model=NextItemResponse)
async def next_item(req: NextItemRequest):
    """
    Generate next item for student.
    
    Calls EngineService.generate_next_item() which:
    1. Queries Neo4j (or files) for learner mastery & misconceptions
    2. Uses planner logic to select skill (remediation, entropy, spaced review)
    3. Generates adaptive item with difficulty
    
    Returns:
        NextItemResponse with item, reasoning, and learner mastery
    
    Raises:
        HTTPException 400: Missing user_id
        HTTPException 500: Engine error
    """
    if not req.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "missing_parameter", "message": "user_id is required"}
        )
    
    try:
        # Call engine service to generate item
        item_data = EngineService.generate_next_item(
            user_id=req.user_id,
            domain=req.domain,
            seed=req.seed
        )
        
        # Convert to response model
        choices = [
            Choice(
                id=c["id"],
                text=c["text"],
                tags_on_select=c.get("tags_on_select", [])
            )
            for c in item_data.get("choices", [])
        ]
        
        item = Item(
            item_id=item_data.get("item_id"),
            skill_id=item_data.get("skill_id"),
            difficulty=item_data.get("difficulty", "medium"),
            stem=item_data.get("stem"),
            choices=choices,
            explanation=item_data.get("explanation"),
            confidence_target=0.7
        )
        
        return NextItemResponse(
            item=item,
            reason=item_data.get("reason", "Continue practicing"),
            difficulty=item_data.get("difficulty", "medium"),
            learner_mastery_before=item_data.get("learner_mastery_before", 0.5)
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "generation_failed", "message": str(e)}
        )

@router.post("/grade", response_model=GradeResponse)
async def grade(req: GradeRequest):
    """
    Grade student response and update mastery.
    
    Calls EngineService.grade_response() which:
    1. Validates answer against correct choice
    2. Detects misconception tags (sign_error, wrong_degree, etc.)
    3. Updates mastery: p_mastery_after = f(p_mastery, correct, confidence)
    4. Logs Attempt node to Neo4j (immutable)
    5. Updates HAS_PROGRESS edge + misconception counters
    
    Returns:
        GradeResponse with correctness, tags, updated mastery, and suggested resource
    
    Raises:
        HTTPException 400: Missing parameters
        HTTPException 404: Item not found
        HTTPException 500: Grading error
    """
    if not req.user_id or not req.item_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "missing_parameter", "message": "user_id and item_id required"}
        )
    
    try:
        # Call engine service to grade
        result = EngineService.grade_response(
            user_id=req.user_id,
            item_id=req.item_id,
            selected_choice_id=req.selected_choice_id,
            time_ms=req.time_ms,
            confidence=req.confidence or 0.5
        )
        
        return GradeResponse(
            correct=result.get("correct", False),
            tags=result.get("tags", []),
            p_mastery_after=result.get("p_mastery_after", 0.5),
            attempts_on_skill=result.get("attempts_on_skill", 0),
            next_due_at=result.get("next_due_at"),
            suggested_resource_url=result.get("suggested_resource_url")
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "grading_failed", "message": str(e)}
        )
