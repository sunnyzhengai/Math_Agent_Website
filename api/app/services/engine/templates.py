"""
Item generation: Wraps the MVP templates with consistent skill IDs.
"""

import sys
from pathlib import Path

# Add MVP to path
mvp_path = Path(__file__).parent.parent.parent.parent.parent / "quadratics_mvp"
if str(mvp_path) not in sys.path:
    sys.path.insert(0, str(mvp_path))

try:
    from engine.templates import generate_item as _generate_item_mvp
except ImportError:
    _generate_item_mvp = None


def generate_item(skill_id: str, difficulty: str = "medium", seed: int = None) -> dict:
    """
    Generate a question for the given skill and difficulty.
    Maps new skill IDs to MVP templates.
    """
    if not _generate_item_mvp:
        # Fallback if MVP templates not available
        return {
            "id": f"{skill_id}_mock",
            "skill_id": skill_id,
            "difficulty": difficulty,
            "stem": "Mock question",
            "choices": [
                {"id": "a", "text": "Option A", "tags_on_select": ["correct"]},
                {"id": "b", "text": "Option B", "tags_on_select": ["wrong"]},
            ],
            "solution": "a",
            "rationale": "Mock rationale"
        }
    
    # Use MVP generator - it uses legacy skill names which match our new naming
    item = _generate_item_mvp(skill_id, difficulty, seed=seed)
    
    # Ensure item has the skill_id we requested (not what generator thinks)
    item["skill_id"] = skill_id
    
    return item
