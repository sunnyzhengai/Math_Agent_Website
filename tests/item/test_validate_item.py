"""
Group 2: Validator correctness tests for engine.validators.validate_item()

Tests verify that the validator correctly detects each contract violation.
"""

import pytest
from engine.validators import validate_item


def test_validator_accepts_valid_item(valid_item_dict):
    """
    Verify that validate_item accepts a structurally valid item.
    
    Checks:
    - Manually constructed valid item returns (True, "")
    """
    is_valid, error_msg = validate_item(valid_item_dict)
    assert (is_valid, error_msg) == (True, "")


def test_validator_detects_missing_fields(valid_item_dict):
    """
    Verify that missing required fields are detected.
    
    Checks:
    - Missing stem → "missing_field"
    - Missing solution_choice_id → "missing_field"
    """
    # Missing stem
    item_no_stem = {k: v for k, v in valid_item_dict.items() if k != "stem"}
    is_valid, error_msg = validate_item(item_no_stem)
    assert (is_valid, error_msg) == (False, "missing_field")
    
    # Missing solution_choice_id
    item_no_solution = {k: v for k, v in valid_item_dict.items() if k != "solution_choice_id"}
    is_valid, error_msg = validate_item(item_no_solution)
    assert (is_valid, error_msg) == (False, "missing_field")


def test_validator_bad_choice_ids(valid_item_dict):
    """
    Verify that invalid choice IDs or wrong order are detected.
    
    Checks:
    - Choice IDs not in ["A","B","C","D"] → "bad_choice_ids"
    - Choice IDs in wrong order (e.g., ["A","C","B","D"]) → "bad_choice_ids"
    """
    # Wrong IDs (e.g., numeric instead of letters)
    item_bad_ids = valid_item_dict.copy()
    item_bad_ids["choices"] = [
        {"id": "1", "text": "(3, 2)"},
        {"id": "2", "text": "(-3, 2)"},
        {"id": "3", "text": "(3, -2)"},
        {"id": "4", "text": "(2, 3)"},
    ]
    
    is_valid, error_msg = validate_item(item_bad_ids)
    assert (is_valid, error_msg) == (False, "bad_choice_ids")
    
    # Wrong order (A,C,B,D instead of A,B,C,D)
    item_wrong_order = valid_item_dict.copy()
    item_wrong_order["choices"] = [
        {"id": "A", "text": "(3, 2)"},
        {"id": "C", "text": "(3, -2)"},
        {"id": "B", "text": "(-3, 2)"},
        {"id": "D", "text": "(2, 3)"},
    ]
    
    is_valid, error_msg = validate_item(item_wrong_order)
    assert (is_valid, error_msg) == (False, "bad_choice_ids")


def test_validator_duplicate_choice_text(valid_item_dict):
    """
    Verify that duplicate choice texts (after normalization) are detected.
    
    Checks:
    - Texts differing only by whitespace → "duplicate_choice_text"
    - Texts differing only by case → "duplicate_choice_text"
    - Normalization: NFKC, strip(), lowercase()
    """
    # Duplicate after trim/lowercase normalization
    item_dup_whitespace = valid_item_dict.copy()
    item_dup_whitespace["choices"] = [
        {"id": "A", "text": "(3, 2)"},
        {"id": "B", "text": " (3, 2) "},  # Same after trim/lowercase
        {"id": "C", "text": "(3, -2)"},
        {"id": "D", "text": "(2, 3)"},
    ]
    
    is_valid, error_msg = validate_item(item_dup_whitespace)
    assert (is_valid, error_msg) == (False, "duplicate_choice_text")
    
    # Duplicate after case normalization
    item_dup_case = valid_item_dict.copy()
    item_dup_case["choices"] = [
        {"id": "A", "text": "Answer One"},
        {"id": "B", "text": "ANSWER ONE"},  # Same after lowercase
        {"id": "C", "text": "(3, -2)"},
        {"id": "D", "text": "(2, 3)"},
    ]
    
    is_valid, error_msg = validate_item(item_dup_case)
    assert (is_valid, error_msg) == (False, "duplicate_choice_text")
    
    # Duplicate after NFKC Unicode normalization (composed vs decomposed)
    item_dup_unicode = valid_item_dict.copy()
    item_dup_unicode["choices"] = [
        {"id": "A", "text": "café"},           # Composed: é (single char U+00E9)
        {"id": "B", "text": "cafe\u0301"},     # Decomposed: e + combining accent (U+0301)
        {"id": "C", "text": "(3, -2)"},
        {"id": "D", "text": "(2, 3)"},
    ]
    
    is_valid, error_msg = validate_item(item_dup_unicode)
    assert (is_valid, error_msg) == (False, "duplicate_choice_text")


def test_validator_invalid_solution_choice_id(valid_item_dict):
    """
    Verify that invalid solution_choice_id is detected.
    
    Checks:
    - solution_choice_id not in ["A","B","C","D"] → "invalid_solution_id"
    """
    item_invalid_id = valid_item_dict.copy()
    item_invalid_id["solution_choice_id"] = "E"
    
    is_valid, error_msg = validate_item(item_invalid_id)
    assert (is_valid, error_msg) == (False, "invalid_solution_id")


def test_validator_solution_text_mismatch(valid_item_dict):
    """
    Verify that solution_text mismatches are detected.
    
    Checks:
    - solution_text not matching choice text → "solution_text_mismatch"
    """
    item_text_mismatch = valid_item_dict.copy()
    item_text_mismatch["solution_text"] = "WRONG ANSWER"
    
    is_valid, error_msg = validate_item(item_text_mismatch)
    assert (is_valid, error_msg) == (False, "solution_text_mismatch")


def test_validator_invalid_stem(valid_item_dict):
    """
    Verify that invalid stem (empty or whitespace-only) is detected.
    
    Checks:
    - Empty stem → "invalid_stem"
    - Whitespace-only stem → "invalid_stem"
    """
    # Empty stem
    item_empty_stem = valid_item_dict.copy()
    item_empty_stem["stem"] = ""
    
    is_valid, error_msg = validate_item(item_empty_stem)
    assert (is_valid, error_msg) == (False, "invalid_stem")
    
    # Whitespace-only stem
    item_ws_stem = valid_item_dict.copy()
    item_ws_stem["stem"] = "   "
    
    is_valid, error_msg = validate_item(item_ws_stem)
    assert (is_valid, error_msg) == (False, "invalid_stem")
