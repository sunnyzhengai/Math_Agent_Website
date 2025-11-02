"""
Pydantic models for Math Agent API.

Extends existing request/response schemas with mastery and planner support.
"""

from typing import Dict, Optional, Literal

from pydantic import BaseModel, Field, conint, confloat


# ============================================================================
# Mastery & Planner Models (NEW)
# ============================================================================

class SkillProgress(BaseModel):
    """Mastery progress snapshot for a single skill."""

    p: confloat(ge=0.0, le=1.0) = Field(
        ..., description="Mastery probability [0, 1]"
    )
    attempts: int = Field(..., description="Total attempts")
    streak: int = Field(..., description="Consecutive correct answers")
    last_ts: float = Field(..., description="Last update timestamp (unix seconds)")


class ProgressGetRequest(BaseModel):
    """Request to retrieve mastery state for a session."""

    session_id: str = Field(
        ..., description="Session ID to retrieve mastery from"
    )


class ProgressGetResponse(BaseModel):
    """Response: all mastery state for a session."""

    session_id: str
    skills: Dict[str, SkillProgress]


Difficulty = Literal["easy", "medium", "hard", "applied"]


class PlannerNextRequest(BaseModel):
    """Request to get next recommended difficulty."""

    session_id: Optional[str] = Field(
        None, description="Optional session ID; if provided, read p from session"
    )
    skill_id: str = Field(..., description="Skill to plan for")
    p_override: Optional[confloat(ge=0.0, le=1.0)] = Field(
        None,
        description="Optional p override. Priority: p_override > session state > default(0.5)",
    )


class PlannerNextResponse(BaseModel):
    """Response: recommended difficulty and reason."""

    difficulty: Difficulty = Field(
        ..., description="Recommended difficulty level"
    )
    reason: str = Field(
        ..., description="Short explanation for the recommendation"
    )
    p_used: confloat(ge=0.0, le=1.0) = Field(
        ..., description="Mastery p value used for this recommendation"
    )


# ============================================================================
# Extended Grade Models (NEW optional fields)
# ============================================================================


class GradeRequestExtended(BaseModel):
    """Extended grade request (backward compatible)."""

    item: dict = Field(..., description="Question item dict")
    choice_id: str = Field(..., description="User's choice ID (A-D)")
    session_id: Optional[str] = Field(
        None, description="Optional session ID for mastery tracking"
    )
    confidence: Optional[conint(ge=1, le=5)] = Field(
        None,
        description="Optional confidence 1-5 to scale mastery update; None → neutral (1.0×)",
    )
