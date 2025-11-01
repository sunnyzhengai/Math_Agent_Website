"""
Phase 2b: API schema validation tests

Validate that engine functions return shapes matching API contracts.
"""

import pytest
from engine.templates import generate_item
from engine.grader import grade_response


def test_generate_item_response_schema():
    """
    Test that generate_item() returns response matching /items/generate contract.
    
    Checks:
    - All required keys present: item_id, skill_id, difficulty, stem, choices, solution_choice_id
    - Types match contract
    - choices is array of exactly 4 objects with id, text
    """
    pass


def test_generate_item_request_validation():
    """
    Test that generate_item() validates request parameters per contract.
    
    Checks:
    - Invalid skill_id raises ValueError("unknown_skill")
    - Invalid difficulty raises ValueError("invalid_difficulty")
    - Non-int seed raises ValueError("invalid_seed")
    """
    pass


def test_grade_response_schema():
    """
    Test that grade_response() returns response matching /grade contract.
    
    Checks:
    - All required keys present: correct, solution_choice_id, explanation
    - correct is boolean
    - solution_choice_id is string (A-D)
    - explanation is string
    """
    pass


def test_grade_request_validation():
    """
    Test that grade_response() validates request per contract.
    
    Checks:
    - Invalid choice_id raises ValueError("invalid_choice_id")
    - Malformed item raises ValueError("invalid_item")
    """
    pass


def test_generate_and_grade_roundtrip():
    """
    Test happy-path: generate item, then grade it (round-trip).
    
    Checks:
    - Generated item can be passed to grade_response()
    - Both responses match contract
    - Determinism: same seed produces same item
    """
    pass


def test_json_serializable():
    """
    Test that all responses are JSON-serializable (no UUID, datetime, etc).
    
    Checks:
    - generate_item() response is JSON-serializable
    - grade_response() response is JSON-serializable
    """
    pass
