"""
Grader for evaluating student responses against items.

See engine/CONTRACTS.md for the grading contract.
"""

from typing import Tuple


def grade_response(item: dict, choice_id: str) -> dict:
    """
    Grade a student's response to a question item.

    Args:
        item: Question item (must pass validate_item)
        choice_id: Student's selected choice ID ("A", "B", "C", or "D")

    Returns:
        A dict with keys:
        - correct (bool): True if choice_id matches solution
        - solution_choice_id (str): The correct choice ID
        - explanation (str): Pedagogical feedback

    Raises:
        ValueError("invalid_choice_id"): If choice_id not in ["A","B","C","D"]
        ValueError("invalid_item"): If item fails validation
    """
    raise NotImplementedError("grade_response not yet implemented")
