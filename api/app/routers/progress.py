from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter()

# Schemas
class ErrorTag(BaseModel):
    tag: str
    count: int

class SkillProgress(BaseModel):
    skill_id: str
    name: str
    p_mastery: float
    attempts: int
    correct_count: int
    streak: int
    last_attempt: Optional[datetime] = None
    due_at: Optional[datetime] = None
    top_errors: List[ErrorTag] = []

class Misconception(BaseModel):
    tag: str
    count: int
    skill_ids: List[str]

class WeeklyStats(BaseModel):
    attempts_this_week: int
    correct_this_week: int
    accuracy_this_week: float
    skills_with_progress: int

class ProgressResponse(BaseModel):
    user_id: str
    domain: str
    skills: List[SkillProgress]
    top_misconceptions: List[Misconception]
    weekly_stats: WeeklyStats
    due_today: List[SkillProgress]

# Mock progress data
MOCK_PROGRESS = ProgressResponse(
    user_id="user_julia_001",
    domain="Quadratics",
    skills=[
        SkillProgress(
            skill_id="quad.identify",
            name="Identify Quadratic",
            p_mastery=0.85,
            attempts=12,
            correct_count=10,
            streak=2,
            last_attempt=datetime.utcnow(),
            top_errors=[ErrorTag(tag="wrong_degree", count=2)]
        ),
        SkillProgress(
            skill_id="quad.vertex.form",
            name="Convert to Vertex Form",
            p_mastery=0.6,
            attempts=8,
            correct_count=5,
            streak=0,
            last_attempt=datetime.utcnow(),
            top_errors=[ErrorTag(tag="sign_error", count=2), ErrorTag(tag="missing_h", count=1)]
        ),
        SkillProgress(
            skill_id="quad.factor.a1",
            name="Factor Quadratics (a=1)",
            p_mastery=0.7,
            attempts=10,
            correct_count=7,
            streak=1,
            top_errors=[]
        ),
    ],
    top_misconceptions=[
        Misconception(tag="sign_error", count=4, skill_ids=["quad.vertex.form", "quad.factor.a1"]),
        Misconception(tag="wrong_degree", count=2, skill_ids=["quad.identify"]),
    ],
    weekly_stats=WeeklyStats(
        attempts_this_week=10,
        correct_this_week=7,
        accuracy_this_week=0.7,
        skills_with_progress=3
    ),
    due_today=[
        SkillProgress(
            skill_id="quad.vertex.form",
            name="Convert to Vertex Form",
            p_mastery=0.6,
            attempts=8,
            correct_count=5,
            streak=0
        )
    ]
)

@router.get("", response_model=ProgressResponse)
async def get_progress(user_id: str, domain: str = "Quadratics"):
    """
    Get learner progress dashboard data.
    
    In production, this queries Neo4j:
    - HAS_PROGRESS relationships for mastery, attempts, streak
    - Attempt nodes for recent history
    - HAS_ERROR relationships for misconception counts
    
    Args:
        user_id: User ID
        domain: Skill domain (default: Quadratics)
    
    Returns:
        ProgressResponse with skill mastery, misconceptions, and weekly stats
    """
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "missing_parameter", "message": "user_id is required"}
        )
    
    # Mock response (in production, query Neo4j)
    return MOCK_PROGRESS
