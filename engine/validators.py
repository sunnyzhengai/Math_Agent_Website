"""
Validation engine for math question items.

See engine/CONTRACTS.md for the full specification.
"""

import unicodedata
from typing import Tuple


def validate_item(item: dict) -> Tuple[bool, str]:
    """
    Validate a generated item's structure per contract.

    Args:
        item: Item dict to validate (must not be mutated)

    Returns:
        A tuple (is_valid, error_code):
        - (True, "") if valid
        - (False, error_code) if invalid, where error_code is one of:
            - "missing_field": required field absent
            - "bad_choice_ids": choices do not have IDs ["A","B","C","D"]
            - "duplicate_choice_text": choice texts not unique after normalization
            - "invalid_solution_id": solution_choice_id not in ["A","B","C","D"]
            - "solution_text_mismatch": solution_text doesn't match choice text
            - "invalid_stem": stem is empty or not a string
    """
    # NOTE: Do not mutate `item`; validator must remain pure.
    
    # Check required fields
    required_fields = {"item_id", "skill_id", "difficulty", "stem", "choices", "solution_choice_id"}
    if not required_fields.issubset(item.keys()):
        return (False, "missing_field")
    
    # Check stem (non-empty string)
    stem = item.get("stem")
    if not isinstance(stem, str) or not stem.strip():
        return (False, "invalid_stem")
    
    # Check choices: exactly 4 items with IDs A,B,C,D in order
    choices = item.get("choices")
    if not isinstance(choices, list) or len(choices) != 4:
        return (False, "bad_choice_ids")
    
    # Defend against non-dict choices
    if not all(isinstance(c, dict) for c in choices):
        return (False, "bad_choice_ids")
    
    # Check that each choice has required keys
    if any("id" not in c or "text" not in c for c in choices):
        return (False, "missing_field")
    
    # Check choice IDs are A,B,C,D in order
    expected_ids = ["A", "B", "C", "D"]
    actual_ids = [c["id"] for c in choices]
    if actual_ids != expected_ids:
        return (False, "bad_choice_ids")
    
    # Check choice texts: non-empty and unique after normalization
    def normalize(text: str) -> str:
        """Normalize text: NFKC, strip, lowercase."""
        return unicodedata.normalize("NFKC", text).strip().lower()
    
    texts = [c["text"] for c in choices]
    if not all(isinstance(t, str) and t.strip() for t in texts):
        return (False, "bad_choice_ids")
    
    normalized_texts = [normalize(t) for t in texts]
    if len(normalized_texts) != len(set(normalized_texts)):
        return (False, "duplicate_choice_text")
    
    # Check solution_choice_id is valid
    solution_id = item.get("solution_choice_id")
    if solution_id not in expected_ids:
        return (False, "invalid_solution_id")
    
    # Check solution_text consistency (if present)
    if "solution_text" in item and item["solution_text"] is not None:
        solution_idx = expected_ids.index(solution_id)
        solution_choice_text = choices[solution_idx]["text"]
        if item["solution_text"] != solution_choice_text:
            return (False, "solution_text_mismatch")
    
    return (True, "")
