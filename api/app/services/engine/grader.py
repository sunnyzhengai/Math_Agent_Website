"""
Grading: Validate answers and detect misconceptions.
"""

import sys
from pathlib import Path

# Add MVP to path
mvp_path = Path(__file__).parent.parent.parent.parent.parent / "quadratics_mvp"
if str(mvp_path) not in sys.path:
    sys.path.insert(0, str(mvp_path))

try:
    from engine.grader import grade as _grade_mvp
except ImportError:
    _grade_mvp = None


def grade_item(item: dict, selected_choice_id: str) -> tuple:
    """
    Grade the user's answer to a question.
    
    Returns:
        (is_correct, tags, chosen_text, score)
    """
    if not _grade_mvp:
        # Simple fallback grading
        correct = selected_choice_id == "a"
        tags = ["correct"] if correct else ["wrong"]
        chosen_text = next(
            (c.get("text", "") for c in item.get("choices", []) if c.get("id") == selected_choice_id),
            "Unknown choice"
        )
        return correct, tags, chosen_text, 1.0 if correct else 0.0
    
    # Use MVP grader
    return _grade_mvp(item, selected_choice_id)
