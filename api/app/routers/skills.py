from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from ..services.engine_service import EngineService

router = APIRouter()

# Schemas
class Skill(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    difficulty: Optional[str] = None
    prerequisites: List[str] = []

class SkillsResponse(BaseModel):
    domain: str
    skills: List[Skill]

@router.get("", response_model=SkillsResponse)
async def list_skills(domain: str = "Quadratics"):
    """
    List all skills in a domain.
    
    Calls EngineService.list_skills() which queries Neo4j skill nodes.
    
    Args:
        domain: Skill domain (e.g., Quadratics, Linear, Systems)
    
    Returns:
        SkillsResponse with list of skills
    
    Raises:
        HTTPException 400: Unsupported domain
    """
    # Get skills from engine service
    skills_data = EngineService.list_skills(domain)
    
    if not skills_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "unsupported_domain",
                "message": f"Domain '{domain}' not found"
            }
        )
    
    # Convert to Skill models
    skills = [
        Skill(
            id=s["id"],
            name=s["name"],
            description=s.get("description"),
            prerequisites=s.get("prerequisites", [])
        )
        for s in skills_data
    ]
    
    return SkillsResponse(domain=domain, skills=skills)
