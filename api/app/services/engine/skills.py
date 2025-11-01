"""
Skill definitions for Quadratics learning path.
"""

SKILLS = [
    {
        "id": "quad.identify",
        "name": "Identify Quadratic Expressions",
        "prereqs": [],
        "progression": ["easy", "easy", "medium", "medium", "hard", "hard", "hard"]
    },
    {
        "id": "quad.vertex.form",
        "name": "Vertex Form",
        "prereqs": ["quad.identify"],
        "progression": ["easy", "easy", "medium", "medium", "hard", "hard", "hard"]
    },
    {
        "id": "quad.factor.a1",
        "name": "Factor (a=1)",
        "prereqs": ["quad.identify", "quad.vertex.form"],
        "progression": ["easy", "easy", "medium", "medium", "hard", "hard"]
    },
    {
        "id": "quad.discriminant",
        "name": "Discriminant",
        "prereqs": ["quad.identify", "quad.vertex.form"],
        "progression": ["easy", "easy", "medium", "medium", "hard", "hard"]
    },
    {
        "id": "quad.formula",
        "name": "Quadratic Formula",
        "prereqs": ["quad.identify"],
        "progression": ["easy", "easy", "medium", "medium", "hard"]
    },
]

SKILL_BY_ID = {s["id"]: s for s in SKILLS}


def get_skill(skill_id: str) -> dict:
    """Get skill definition by ID."""
    return SKILL_BY_ID.get(skill_id)
