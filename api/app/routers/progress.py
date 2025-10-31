from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from ..services.engine_service import EngineService

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

@router.get("", response_model=ProgressResponse)
async def get_progress(user_id: str, domain: str = "Quadratics"):
    """
    Get learner progress dashboard data.
    
    Calls EngineService.get_progress() which queries Neo4j:
    - HAS_PROGRESS relationships (mastery, attempts, streak, last_attempt)
    - Recent Attempt nodes (for weekly stats and accuracy)
    - HAS_ERROR relationships (misconception counts)
    
    Args:
        user_id: User ID (required)
        domain: Skill domain (default: Quadratics)
    
    Returns:
        ProgressResponse with skill mastery, misconceptions, and weekly stats
    
    Raises:
        HTTPException 400: Missing user_id
        HTTPException 404: User not found
        HTTPException 500: Query error
    """
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "missing_parameter", "message": "user_id is required"}
        )
    
    try:
        # Get progress from engine service
        progress_data = EngineService.get_progress(user_id, domain)
        
        # Convert skills to SkillProgress models
        skills = [
            SkillProgress(
                skill_id=s["skill_id"],
                name=s["name"],
                p_mastery=s.get("p_mastery", 0.5),
                attempts=s.get("attempts", 0),
                correct_count=s.get("correct_count", 0),
                streak=s.get("streak", 0),
                last_attempt=s.get("last_attempt"),
                due_at=s.get("due_at"),
                top_errors=[ErrorTag(tag=e["tag"], count=e["count"]) for e in s.get("top_errors", [])]
            )
            for s in progress_data.get("skills", [])
        ]
        
        # Convert misconceptions
        misconceptions = [
            Misconception(
                tag=m["tag"],
                count=m["count"],
                skill_ids=m["skill_ids"]
            )
            for m in progress_data.get("top_misconceptions", [])
        ]
        
        # Weekly stats
        stats_data = progress_data.get("weekly_stats", {})
        weekly_stats = WeeklyStats(
            attempts_this_week=stats_data.get("attempts_this_week", 0),
            correct_this_week=stats_data.get("correct_this_week", 0),
            accuracy_this_week=stats_data.get("accuracy_this_week", 0.0),
            skills_with_progress=stats_data.get("skills_with_progress", 0)
        )
        
        # Due today
        due_today = [
            SkillProgress(
                skill_id=s["skill_id"],
                name=s["name"],
                p_mastery=s.get("p_mastery", 0.5),
                attempts=s.get("attempts", 0),
                correct_count=s.get("correct_count", 0),
                streak=s.get("streak", 0),
                last_attempt=s.get("last_attempt"),
                due_at=s.get("due_at")
            )
            for s in progress_data.get("due_today", [])
        ]
        
        return ProgressResponse(
            user_id=user_id,
            domain=domain,
            skills=skills,
            top_misconceptions=misconceptions,
            weekly_stats=weekly_stats,
            due_today=due_today
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "progress_query_failed", "message": str(e)}
        )
