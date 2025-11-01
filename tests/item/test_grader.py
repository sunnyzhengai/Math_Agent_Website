"""
Phase 2a: Grader tests for engine.grader.grade_response()

Tests verify that grading logic correctly evaluates student responses.
Pure function: no randomness, no time, deterministic.
"""

import pytest
from engine.grader import grade_response
from engine.templates import generate_item


def test_grade_response_correct_answer(valid_item_dict):
    """
    Test that a correct choice returns correct=True with solution details.
    
    Checks:
    - Returns dict with keys: correct, solution_choice_id, explanation
    - correct == True
    - solution_choice_id matches item's solution
    - explanation is non-empty string
    """
    result = grade_response(valid_item_dict, "A")
    
    assert isinstance(result, dict), "Result must be dict"
    assert "correct" in result, "Missing 'correct' key"
    assert "solution_choice_id" in result, "Missing 'solution_choice_id' key"
    assert "explanation" in result, "Missing 'explanation' key"
    
    assert result["correct"] is True, "Should be correct"
    assert result["solution_choice_id"] == "A", "Should match solution"
    assert isinstance(result["explanation"], str), "Explanation must be string"
    assert result["explanation"], "Explanation must be non-empty"


def test_grade_response_incorrect_answer(valid_item_dict):
    """
    Test that an incorrect choice returns correct=False but still shows solution.
    
    Checks:
    - correct == False
    - solution_choice_id still echoed (student learns right answer)
    - explanation provided
    """
    result = grade_response(valid_item_dict, "B")
    
    assert result["correct"] is False, "Should be incorrect"
    assert result["solution_choice_id"] == "A", "Should still show correct answer"
    assert isinstance(result["explanation"], str), "Explanation must be string"
    assert result["explanation"], "Explanation must be non-empty"


def test_grade_response_rejects_invalid_choice_id_out_of_range(valid_item_dict):
    """
    Test that out-of-range choice IDs are rejected.
    
    Checks:
    - choice_id="E" raises ValueError("invalid_choice_id")
    - choice_id="F" raises ValueError("invalid_choice_id")
    """
    with pytest.raises(ValueError, match="invalid_choice_id"):
        grade_response(valid_item_dict, "E")
    
    with pytest.raises(ValueError, match="invalid_choice_id"):
        grade_response(valid_item_dict, "F")


def test_grade_response_rejects_lowercase_choice_id(valid_item_dict):
    """
    Test that lowercase choice IDs are rejected (case-sensitive).
    
    Checks:
    - choice_id="a" raises ValueError("invalid_choice_id")
    - choice_id="b" raises ValueError("invalid_choice_id")
    """
    with pytest.raises(ValueError, match="invalid_choice_id"):
        grade_response(valid_item_dict, "a")
    
    with pytest.raises(ValueError, match="invalid_choice_id"):
        grade_response(valid_item_dict, "b")


def test_grade_response_rejects_malformed_item():
    """
    Test that items that fail validation are rejected.
    
    Checks:
    - Missing solution_choice_id raises ValueError("invalid_item")
    - Malformed choices (not 4 items) raises ValueError("invalid_item")
    """
    # Missing solution_choice_id
    bad_item_1 = {
        "item_id": "test:easy:42",
        "skill_id": "test",
        "difficulty": "easy",
        "stem": "Test question",
        "choices": [
            {"id": "A", "text": "Option A"},
            {"id": "B", "text": "Option B"},
            {"id": "C", "text": "Option C"},
            {"id": "D", "text": "Option D"},
        ],
    }
    
    with pytest.raises(ValueError, match="invalid_item"):
        grade_response(bad_item_1, "A")
    
    # Wrong number of choices
    bad_item_2 = {
        "item_id": "test:easy:42",
        "skill_id": "test",
        "difficulty": "easy",
        "stem": "Test question",
        "choices": [
            {"id": "A", "text": "Option A"},
            {"id": "B", "text": "Option B"},
        ],
        "solution_choice_id": "A",
    }
    
    with pytest.raises(ValueError, match="invalid_item"):
        grade_response(bad_item_2, "A")


def test_grade_response_determinism_with_same_item(valid_item_dict):
    """
    Test that grading is deterministic (no RNG, no time).
    
    Checks:
    - Same (item, choice_id) always returns identical result
    - No time-based logic, no randomness
    """
    result1 = grade_response(valid_item_dict, "A")
    result2 = grade_response(valid_item_dict, "A")
    result3 = grade_response(valid_item_dict, "A")
    
    assert result1 == result2 == result3, "Results must be identical on repeat calls"


def test_grade_response_with_generated_item():
    """
    Test grading with an actual generated item from Phase-1.
    
    Checks:
    - Generates item via generate_item()
    - Grades correct choice → correct=True
    - Grades wrong choice → correct=False, but solution_choice_id shown
    """
    item = generate_item("quad.graph.vertex", "easy", seed=42)
    
    # Grade correct choice
    correct_result = grade_response(item, item["solution_choice_id"])
    assert correct_result["correct"] is True, "Should be correct"
    
    # Grade incorrect choice (pick a different one)
    other_choice = next(c for c in item["choices"] if c["id"] != item["solution_choice_id"])
    incorrect_result = grade_response(item, other_choice["id"])
    assert incorrect_result["correct"] is False, "Should be incorrect"
    assert incorrect_result["solution_choice_id"] == item["solution_choice_id"], "Should still show solution"


def test_grade_response_explanation_is_meaningful(valid_item_dict):
    """
    Test that explanation provides some pedagogical value.
    
    Checks:
    - explanation is not empty
    - explanation is a string
    - (Optional) explanation differs for correct vs incorrect
    """
    correct_result = grade_response(valid_item_dict, "A")
    incorrect_result = grade_response(valid_item_dict, "B")
    
    # Both have explanations
    assert correct_result["explanation"], "Correct explanation must exist"
    assert incorrect_result["explanation"], "Incorrect explanation must exist"
    
    # Both are strings
    assert isinstance(correct_result["explanation"], str), "Must be string"
    assert isinstance(incorrect_result["explanation"], str), "Must be string"
    
    # Explanations differ
    assert correct_result["explanation"] != incorrect_result["explanation"], \
        "Correct and incorrect explanations should differ"
