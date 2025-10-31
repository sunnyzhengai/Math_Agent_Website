from typing import List, Optional

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel

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

# Mock skills data (in production, query from Neo4j)
MOCK_SKILLS = {
    "Quadratics": [
        Skill(
            id="quad.identify",
            name="Identify Quadratic",
            description="Determine if an expression is quadratic",
            prerequisites=[]
        ),
        Skill(
            id="quad.vertex.form",
            name="Convert to Vertex Form",
            description="Write quadratic in vertex form a(x-h)² + k",
            prerequisites=["quad.identify"]
        ),
        Skill(
            id="quad.factor.a1",
            name="Factor Quadratics (a=1)",
            description="Factor quadratic trinomials with leading coefficient 1",
            prerequisites=["quad.identify"]
        ),
        Skill(
            id="quad.discriminant",
            name="Use Discriminant",
            description="Determine number of real solutions using discriminant",
            prerequisites=["quad.identify"]
        ),
    ]
}

@router.get("", response_model=SkillsResponse)
async def list_skills(domain: str = "Quadratics"):
    """
    List all skills in a domain.
    
    Args:
        domain: Skill domain (e.g., Quadratics, Linear, Systems)
    
    Returns:
        SkillsResponse with list of skills
    """
    if domain not in MOCK_SKILLS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "unsupported_domain",
                "message": f"Domain '{domain}' not found"
            }
        )
    
    skills = MOCK_SKILLS[domain]
    return SkillsResponse(domain=domain, skills=skills)
