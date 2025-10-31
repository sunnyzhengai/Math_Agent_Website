from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

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

# Mock item generation (in production, use real engine)
MOCK_ITEM = Item(
    item_id="item_test_001",
    skill_id="quad.identify",
    difficulty="easy",
    stem="Is the following expression a quadratic? x² + 3x + 2",
    choices=[
        Choice(id="c1", text="Yes", tags_on_select=["correct"]),
        Choice(id="c2", text="No", tags_on_select=["wrong"]),
    ],
    explanation="A quadratic has highest degree 2.",
    confidence_target=0.75
)

@router.post("/next-item", response_model=NextItemResponse)
async def next_item(req: NextItemRequest):
    """
    Generate next item for student.
    
    In production, this calls:
    - planner.generate_adaptive_item(user_id, domain, seed)
    
    Returns item with reasoning.
    """
    if not req.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "missing_parameter", "message": "user_id is required"}
        )
    
    # Mock response (in production, call real engine)
    return NextItemResponse(
        item=MOCK_ITEM,
        reason="Skill quad.identify is due for review; you had 60% mastery last week",
        difficulty="easy",
        learner_mastery_before=0.6
    )

@router.post("/grade", response_model=GradeResponse)
async def grade(req: GradeRequest):
    """
    Grade student response and update mastery.
    
    In production, this:
    1. Calls engine.grade() to validate answer
    2. Updates Neo4j: HAS_PROGRESS, Attempt node, misconception tags
    3. Returns updated mastery
    """
    if not req.user_id or not req.item_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "missing_parameter", "message": "user_id and item_id required"}
        )
    
    # Mock grading (in production, call real engine)
    is_correct = req.selected_choice_id == "c1"  # Mock: c1 is correct
    
    return GradeResponse(
        correct=is_correct,
        tags=["correct"] if is_correct else ["wrong"],
        p_mastery_after=0.65 if is_correct else 0.55,
        attempts_on_skill=5,
        next_due_at=datetime.utcnow() if is_correct else None,
        suggested_resource_url=None if is_correct else "https://khan.academy.com/..."
    )
