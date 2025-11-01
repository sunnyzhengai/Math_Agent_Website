"""
Phase 2b: API schema validation tests

Validate that engine functions return shapes matching API contracts (server-agnostic).
"""

import json
import pytest

from engine.templates import generate_item
from engine.grader import grade_response


# ============================================================================
# Constants
# ============================================================================

VALID_SKILL = "quad.graph.vertex"
VALID_SEED = 42


# ============================================================================
# Helper Functions
# ============================================================================

def _assert_item_schema(item: dict):
    """Assert that item dict matches /items/generate response schema."""
    # Required top-level keys
    for k in ["item_id", "skill_id", "difficulty", "stem", "choices", "solution_choice_id"]:
        assert k in item, f"Missing key: {k} in item: {item}"

    # Types
    assert isinstance(item["item_id"], str), "item_id must be string"
    assert isinstance(item["skill_id"], str), "skill_id must be string"
    assert isinstance(item["difficulty"], str), "difficulty must be string"
    assert isinstance(item["stem"], str), "stem must be string"
    assert isinstance(item["choices"], list), "choices must be list"
    assert isinstance(item["solution_choice_id"], str), "solution_choice_id must be string"

    # choices: exactly 4 objects with id/text
    assert len(item["choices"]) == 4, f"choices must have 4 entries, got {len(item['choices'])}"
    ids = [c.get("id") for c in item["choices"]]
    assert ids == ["A", "B", "C", "D"], f"choice IDs must be A..D in order, got {ids}"
    
    for i, c in enumerate(item["choices"]):
        assert isinstance(c, dict), f"choice {i} must be an object"
        assert "text" in c and isinstance(c["text"], str) and c["text"].strip(), \
            f"choice {i} must have non-empty 'text'"

    # solution_choice_id must be one of A..D
    assert item["solution_choice_id"] in {"A", "B", "C", "D"}, \
        f"solution_choice_id must be A-D, got {item['solution_choice_id']}"


def _assert_grade_schema(res: dict):
    """Assert that grade response dict matches /grade response schema."""
    for k in ["correct", "solution_choice_id", "explanation"]:
        assert k in res, f"Missing key '{k}' in grade response: {res}"
    
    assert isinstance(res["correct"], bool), "correct must be boolean"
    assert res["solution_choice_id"] in {"A", "B", "C", "D"}, \
        f"solution_choice_id must be A-D, got {res['solution_choice_id']}"
    assert isinstance(res["explanation"], str) and res["explanation"].strip(), \
        "explanation must be non-empty string"


# ============================================================================
# Tests: generate_item() schema
# ============================================================================

def test_generate_item_response_schema():
    """
    generate_item() returns /items/generate response shape.
    """
    item = generate_item(VALID_SKILL, "easy", seed=VALID_SEED)
    _assert_item_schema(item)


def test_generate_item_request_validation():
    """
    generate_item() validates inputs:
    - unknown skill -> ValueError("unknown_skill")
    - invalid difficulty -> ValueError("invalid_difficulty")
    - non-int seed -> ValueError("invalid_seed")
    """
    with pytest.raises(ValueError, match="unknown_skill"):
        generate_item("unknown.skill", "easy", seed=VALID_SEED)

    for bad in ["EASY", "Easy", "extreme"]:
        with pytest.raises(ValueError, match="invalid_difficulty"):
            generate_item(VALID_SKILL, bad, seed=VALID_SEED)

    # Note: True is accepted as seed (bool is subclass of int in Python)
    # Only truly incompatible types raise ValueError
    with pytest.raises(ValueError, match="invalid_seed"):
        generate_item(VALID_SKILL, "easy", seed="42")
    
    with pytest.raises(ValueError, match="invalid_seed"):
        generate_item(VALID_SKILL, "easy", seed=3.14)


# ============================================================================
# Tests: grade_response() schema
# ============================================================================

def test_grade_response_schema():
    """
    grade_response() returns /grade response shape.
    """
    item = generate_item(VALID_SKILL, "easy", seed=VALID_SEED)
    res = grade_response(item, item["solution_choice_id"])
    _assert_grade_schema(res)


def test_grade_request_validation():
    """
    grade_response() validates:
    - invalid choice_id -> ValueError("invalid_choice_id")
    - malformed item -> ValueError("invalid_item")
    """
    item = generate_item(VALID_SKILL, "easy", seed=VALID_SEED)

    for bad in ["E", "a", "", "AA", None, 5]:
        with pytest.raises(ValueError, match="invalid_choice_id"):
            grade_response(item, bad)

    broken = dict(item)
    broken.pop("solution_choice_id", None)
    with pytest.raises(ValueError, match="invalid_item"):
        grade_response(broken, "A")


# ============================================================================
# Tests: Round-trip & Determinism
# ============================================================================

def test_generate_and_grade_roundtrip():
    """
    Happy path: generate then grade.
    Also checks determinism for seeded generation.
    """
    item1 = generate_item(VALID_SKILL, "easy", seed=VALID_SEED)
    item2 = generate_item(VALID_SKILL, "easy", seed=VALID_SEED)
    assert item1 == item2, "Seeded generation must be deterministic"

    res = grade_response(item1, item1["solution_choice_id"])
    _assert_grade_schema(res)
    assert res["correct"] is True


def test_json_serializable():
    """
    Responses are JSON-serializable (no datetimes/UUID objects, etc).
    """
    item = generate_item(VALID_SKILL, "easy", seed=VALID_SEED)
    grade = grade_response(item, item["solution_choice_id"])

    json.dumps(item)   # should not raise
    json.dumps(grade)  # should not raise
