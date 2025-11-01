"""
Phase 2a: Grader tests for engine.grader.grade_response()

Tests verify that grading logic correctly evaluates student responses.
Pure function: no randomness, no time, deterministic.
"""

import pytest
from engine.grader import grade_response
from engine.templates import generate_item


class TestGradeResponseHappyPath:
    """Happy-path grading tests"""

    def test_grade_response_correct_answer(self, valid_item_dict):
        """
        Test 1: Correct answer
        
        Generate item, grade with correct choice.
        Assert correct=True, solution shown, explanation starts with "Correct!".
        """
        result = grade_response(valid_item_dict, "A")

        assert isinstance(result, dict), "Result must be dict"
        assert "correct" in result, "Missing 'correct' key"
        assert "solution_choice_id" in result, "Missing 'solution_choice_id' key"
        assert "explanation" in result, "Missing 'explanation' key"

        assert result["correct"] is True, "Should be correct"
        assert result["solution_choice_id"] == "A", "Should match solution"
        assert isinstance(result["explanation"], str), "Explanation must be string"
        assert result["explanation"].startswith("Correct!"), "Correct answer explanation should start with 'Correct!'"

    def test_grade_response_incorrect_answer(self, valid_item_dict):
        """
        Test 2: Incorrect answer
        
        Pick wrong choice, grade it.
        Assert correct=False, solution still shown, explanation mentions both texts.
        """
        result = grade_response(valid_item_dict, "B")

        assert result["correct"] is False, "Should be incorrect"
        assert result["solution_choice_id"] == "A", "Should still show correct answer"
        assert isinstance(result["explanation"], str), "Explanation must be string"
        assert result["explanation"], "Explanation must be non-empty"
        
        # Verify explanation mentions both the correct and wrong answers
        assert "The correct answer is" in result["explanation"], "Should mention correct answer"
        assert "not" in result["explanation"], "Should mention it's wrong"


class TestGradeResponseInvalidChoiceId:
    """Choice ID validation tests"""

    def test_grade_response_rejects_invalid_choice_id_out_of_range(self, valid_item_dict):
        """
        Test 3a: Invalid choice IDs (out of range)
        
        Try choice_id="E", "F", etc.
        Assert ValueError("invalid_choice_id").
        """
        with pytest.raises(ValueError, match="invalid_choice_id"):
            grade_response(valid_item_dict, "E")

        with pytest.raises(ValueError, match="invalid_choice_id"):
            grade_response(valid_item_dict, "F")

    def test_grade_response_rejects_lowercase_choice_id(self, valid_item_dict):
        """
        Test 3b: Invalid choice IDs (lowercase, non-string, etc)
        
        Try choice_id="a", "", "AA", None, 5.
        Assert ValueError("invalid_choice_id") for each.
        """
        with pytest.raises(ValueError, match="invalid_choice_id"):
            grade_response(valid_item_dict, "a")

        with pytest.raises(ValueError, match="invalid_choice_id"):
            grade_response(valid_item_dict, "")

        with pytest.raises(ValueError, match="invalid_choice_id"):
            grade_response(valid_item_dict, "AA")

        with pytest.raises(ValueError, match="invalid_choice_id"):
            grade_response(valid_item_dict, None)

        with pytest.raises(ValueError, match="invalid_choice_id"):
            grade_response(valid_item_dict, 5)


class TestGradeResponseInvalidItem:
    """Item validation tests"""

    def test_grade_response_rejects_malformed_item(self, valid_item_dict):
        """
        Test 4: Invalid items
        
        Start from valid item, break it (delete choices[0]["text"], set solution_choice_id="E").
        Assert ValueError("invalid_item:<code>").
        """
        # Break: delete choice text
        bad_item_1 = valid_item_dict.copy()
        bad_item_1["choices"] = bad_item_1["choices"].copy()
        bad_item_1["choices"][0] = bad_item_1["choices"][0].copy()
        del bad_item_1["choices"][0]["text"]

        with pytest.raises(ValueError, match="invalid_item"):
            grade_response(bad_item_1, "A")

        # Break: invalid solution_choice_id
        bad_item_2 = valid_item_dict.copy()
        bad_item_2["solution_choice_id"] = "E"

        with pytest.raises(ValueError, match="invalid_item"):
            grade_response(bad_item_2, "A")

        # Break: missing solution_choice_id entirely
        bad_item_3 = valid_item_dict.copy()
        del bad_item_3["solution_choice_id"]

        with pytest.raises(ValueError, match="invalid_item"):
            grade_response(bad_item_3, "A")


class TestGradeResponseDeterminismAndPurity:
    """Determinism and side-effect tests"""

    def test_grade_response_determinism_with_same_item(self, valid_item_dict):
        """
        Test 5: Determinism and purity
        
        Call grade_response twice with same inputs.
        Assert identical outputs and input dict unchanged.
        """
        import copy
        original_item = copy.deepcopy(valid_item_dict)

        result1 = grade_response(valid_item_dict, "A")
        result2 = grade_response(valid_item_dict, "A")
        result3 = grade_response(valid_item_dict, "A")

        assert result1 == result2 == result3, "Results must be identical on repeat calls"
        assert valid_item_dict == original_item, "Input item must not be mutated"


class TestGradeResponseConsistency:
    """Validator consistency tests"""

    def test_grade_response_with_generated_item(self):
        """
        Test 6: Consistency with validator
        
        Generate item, validate it (should be True).
        Grade with correct choice → should succeed (not raise).
        """
        from engine.validators import validate_item
        
        item = generate_item("quad.graph.vertex", "easy", seed=42)

        # Verify validator accepts it
        is_valid, err = validate_item(item)
        assert is_valid, f"Generated item should pass validation, but got error: {err}"

        # Grade correct choice → should not raise
        correct_result = grade_response(item, item["solution_choice_id"])
        assert correct_result["correct"] is True, "Should be correct"

        # Grade incorrect choice → should not raise
        other_choice = next(c for c in item["choices"] if c["id"] != item["solution_choice_id"])
        incorrect_result = grade_response(item, other_choice["id"])
        assert incorrect_result["correct"] is False, "Should be incorrect"
        assert incorrect_result["solution_choice_id"] == item["solution_choice_id"], "Should still show solution"


# Legacy tests (kept for backward compatibility)

def test_grade_response_correct_answer_legacy(valid_item_dict):
    """Legacy: correct answer returns correct=True with solution details."""
    result = grade_response(valid_item_dict, "A")

    assert isinstance(result, dict), "Result must be dict"
    assert "correct" in result, "Missing 'correct' key"
    assert "solution_choice_id" in result, "Missing 'solution_choice_id' key"
    assert "explanation" in result, "Missing 'explanation' key"

    assert result["correct"] is True, "Should be correct"
    assert result["solution_choice_id"] == "A", "Should match solution"
    assert isinstance(result["explanation"], str), "Explanation must be string"
    assert result["explanation"], "Explanation must be non-empty"


def test_grade_response_incorrect_answer_legacy(valid_item_dict):
    """Legacy: incorrect answer returns correct=False but still shows solution."""
    result = grade_response(valid_item_dict, "B")

    assert result["correct"] is False, "Should be incorrect"
    assert result["solution_choice_id"] == "A", "Should still show correct answer"
    assert isinstance(result["explanation"], str), "Explanation must be string"
    assert result["explanation"], "Explanation must be non-empty"


def test_grade_response_explanation_is_meaningful(valid_item_dict):
    """Legacy: explanation provides some pedagogical value."""
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
