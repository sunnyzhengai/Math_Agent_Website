"""
Grader for evaluating student responses against items.

See engine/CONTRACTS.md for the grading contract.

NOTE: Do not mutate `item`; grader must remain pure.
"""

from engine.validators import validate_item


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
        ValueError("invalid_item:<error_code>"): If item fails validation
    """
    # Validate choice_id type and value (strict)
    if not isinstance(choice_id, str) or len(choice_id) != 1 or choice_id not in ["A", "B", "C", "D"]:
        raise ValueError("invalid_choice_id")

    # Validate item structure, propagate error code for debuggability
    is_valid, error_msg = validate_item(item)
    if not is_valid:
        raise ValueError(f"invalid_item:{error_msg}")

    # Determine if answer is correct
    correct = (choice_id == item["solution_choice_id"])

    # Get choice texts for explanation
    student_choice = next(c for c in item["choices"] if c["id"] == choice_id)
    correct_choice = next(c for c in item["choices"] if c["id"] == item["solution_choice_id"])

    # Build pedagogical explanation
    if correct:
        explanation = f"Correct! The answer is {correct_choice['text']}."
    else:
        explanation = f"Not quite. The correct answer is {correct_choice['text']}, not {student_choice['text']}."

    return {
        "correct": correct,
        "solution_choice_id": item["solution_choice_id"],
        "explanation": explanation,
    }
