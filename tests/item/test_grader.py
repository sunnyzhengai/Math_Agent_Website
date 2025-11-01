"""
Phase 2a: Grader tests for engine.grader.grade_response()

Tests verify that grading logic correctly evaluates student responses.
Pure function: no randomness, no time, deterministic.
"""

import pytest
from engine.grader import grade_response


def test_grade_response_correct_answer():
    """
    Test that a correct choice returns correct=True with solution details.
    
    Checks:
    - Returns dict with keys: correct, solution_choice_id, explanation
    - correct == True
    - solution_choice_id matches item's solution
    - explanation is non-empty string
    """
    pass


def test_grade_response_incorrect_answer():
    """
    Test that an incorrect choice returns correct=False but still shows solution.
    
    Checks:
    - correct == False
    - solution_choice_id still echoed (student learns right answer)
    - explanation provided
    """
    pass


def test_grade_response_rejects_invalid_choice_id_out_of_range():
    """
    Test that out-of-range choice IDs are rejected.
    
    Checks:
    - choice_id="E" raises ValueError("invalid_choice_id")
    - choice_id="F" raises ValueError("invalid_choice_id")
    """
    pass


def test_grade_response_rejects_lowercase_choice_id():
    """
    Test that lowercase choice IDs are rejected (case-sensitive).
    
    Checks:
    - choice_id="a" raises ValueError("invalid_choice_id")
    - choice_id="b" raises ValueError("invalid_choice_id")
    """
    pass


def test_grade_response_rejects_malformed_item():
    """
    Test that items that fail validation are rejected.
    
    Checks:
    - Missing solution_choice_id raises ValueError("invalid_item")
    - Malformed choices (not 4 items) raises ValueError("invalid_item")
    """
    pass


def test_grade_response_determinism_with_same_item():
    """
    Test that grading is deterministic (no RNG, no time).
    
    Checks:
    - Same (item, choice_id) always returns identical result
    - No time-based logic, no randomness
    """
    pass


def test_grade_response_with_generated_item():
    """
    Test grading with an actual generated item from Phase-1.
    
    Checks:
    - Generates item via generate_item()
    - Grades correct choice → correct=True
    - Grades wrong choice → correct=False, but solution_choice_id shown
    """
    pass


def test_grade_response_explanation_is_meaningful():
    """
    Test that explanation provides some pedagogical value.
    
    Checks:
    - explanation is not empty
    - explanation is a string
    - (Optional) explanation differs for correct vs incorrect
    """
    pass
