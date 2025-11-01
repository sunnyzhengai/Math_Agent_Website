"""
Group 1: Generator correctness tests for engine.templates.generate_item()

Tests verify that generated items follow the contract exactly.
"""

import pytest
from engine.templates import generate_item
from engine.validators import validate_item


# Constants from conftest (replicated for local use in assertions)
VALID_SKILL_ID = "quad.graph.vertex"
VALID_SEED = 42
ALTERNATE_SEED = 43


def test_generate_item_returns_expected_keys():
    """
    Verify that generate_item returns all required top-level fields.
    
    Checks:
    - Type is dict
    - Keys include: item_id, skill_id, difficulty, stem, choices, solution_choice_id
    - No required field is None or missing
    - All required keys have non-None values
    """
    item = generate_item(VALID_SKILL_ID, difficulty="easy", seed=VALID_SEED)
    
    assert isinstance(item, dict), "Item must be a dict"
    
    required_keys = {"item_id", "skill_id", "difficulty", "stem", "choices", "solution_choice_id"}
    assert required_keys.issubset(item.keys()), f"Missing required keys. Got: {item.keys()}"
    
    # Check no required field is None
    for key in required_keys:
        assert item[key] is not None, f"Required key '{key}' is None"
    
    # Verify skill_id matches input
    assert item["skill_id"] == VALID_SKILL_ID, "skill_id must match input"


def test_generate_item_structure_and_ids():
    """
    Verify that the structural contract holds for choices and solution.
    
    Checks:
    - choices is a list of exactly 4
    - Each element has id ∈ ["A","B","C","D"] in display order
    - Each text is a non-empty string
    - solution_choice_id ∈ ["A","B","C","D"]
    - If solution_text exists, equals the text of the correct choice
    """
    item = generate_item(VALID_SKILL_ID, difficulty="easy", seed=VALID_SEED)
    
    # Check choices structure
    assert isinstance(item["choices"], list), "choices must be a list"
    assert len(item["choices"]) == 4, f"choices must have exactly 4 items, got {len(item['choices'])}"
    
    # Check choice IDs are A,B,C,D in order
    expected_ids = ["A", "B", "C", "D"]
    actual_ids = [choice["id"] for choice in item["choices"]]
    assert actual_ids == expected_ids, f"Choice IDs must be {expected_ids} in order, got {actual_ids}"
    
    # Check each choice has non-empty text
    for i, choice in enumerate(item["choices"]):
        assert "text" in choice, f"Choice {i} missing 'text'"
        assert isinstance(choice["text"], str), f"Choice {i} text must be string"
        assert choice["text"].strip(), f"Choice {i} text must be non-empty"
    
    # Check solution_choice_id is valid
    assert item["solution_choice_id"] in expected_ids, f"solution_choice_id must be in {expected_ids}"
    
    # If solution_text exists, must match the corresponding choice
    if "solution_text" in item and item["solution_text"] is not None:
        solution_choice = next(
            c for c in item["choices"] if c["id"] == item["solution_choice_id"]
        )
        assert item["solution_text"] == solution_choice["text"], \
            "solution_text must match the text of the solution choice"


def test_generate_item_determinism():
    """
    Verify that seeding produces deterministic output.
    
    Checks:
    - Two calls with identical (skill_id, difficulty, seed) → identical dict
    - Two calls with different seeds → different items
    - seed=None → item_id differs on successive calls (random generation)
    """
    # Test determinism: same seed → identical items
    item1 = generate_item(VALID_SKILL_ID, "easy", seed=VALID_SEED)
    item2 = generate_item(VALID_SKILL_ID, "easy", seed=VALID_SEED)
    
    assert item1 == item2, "Same (skill, difficulty, seed) must produce identical items"
    assert item1["item_id"] == item2["item_id"], "item_id must be deterministic with same seed"
    
    # Test variance: different seeds → different items
    item3 = generate_item(VALID_SKILL_ID, "easy", seed=ALTERNATE_SEED)
    assert item1 != item3, "Different seeds should produce different items"
    
    # Test seed=None: different item_ids on successive calls
    item_none1 = generate_item(VALID_SKILL_ID, "easy", seed=None)
    item_none2 = generate_item(VALID_SKILL_ID, "easy", seed=None)
    
    assert item_none1["item_id"] != item_none2["item_id"], \
        "seed=None should produce different item_ids on successive calls"


def test_generate_item_difficulty_validation():
    """
    Verify that invalid difficulty values raise ValueError("invalid_difficulty").
    
    Checks:
    - Valid difficulties are exactly {"easy", "medium", "hard", "applied"}
    - Uppercase or mixed-case raises error
    - Unknown values raise error
    - Difficulty is case-sensitive (lowercase only)
    """
    # Invalid: uppercase difficulty
    with pytest.raises(ValueError, match="invalid_difficulty"):
        generate_item(VALID_SKILL_ID, "EASY", seed=VALID_SEED)
    
    # Invalid: unknown difficulty
    with pytest.raises(ValueError, match="invalid_difficulty"):
        generate_item(VALID_SKILL_ID, "extreme", seed=VALID_SEED)
    
    # Invalid: mixed case
    with pytest.raises(ValueError, match="invalid_difficulty"):
        generate_item(VALID_SKILL_ID, "Easy", seed=VALID_SEED)


def test_generate_item_unknown_skill_raises():
    """
    Verify that unknown skill_id raises ValueError("unknown_skill").
    
    Checks:
    - Unrecognized skill_id immediately raises error (fail-fast)
    """
    with pytest.raises(ValueError, match="unknown_skill"):
        generate_item("unknown.skill.id", "easy", seed=VALID_SEED)


def test_generate_item_seed_validation():
    """
    Verify that non-integer seed values raise ValueError("invalid_seed").
    
    Checks:
    - seed can be None (optional) or an integer only
    - String seeds raise error
    - Float seeds raise error
    """
    # Invalid: string seed
    with pytest.raises(ValueError, match="invalid_seed"):
        generate_item(VALID_SKILL_ID, "easy", seed="42")
    
    # Invalid: float seed
    with pytest.raises(ValueError, match="invalid_seed"):
        generate_item(VALID_SKILL_ID, "easy", seed=3.14)


def test_generate_item_difficulty_default():
    """
    Verify that difficulty defaults to "easy" when None.
    
    Checks:
    - difficulty=None resolves to "easy" in the returned item
    """
    item = generate_item(VALID_SKILL_ID, difficulty=None, seed=VALID_SEED)
    assert item["difficulty"] == "easy", "difficulty=None should resolve to 'easy'"


def test_generate_item_passes_validator():
    """
    Verify that generated items always pass validate_item.
    
    Checks:
    - A generated item with valid inputs passes validate_item() → (True, "")
    - Generator output is always valid per the contract
    """
    item = generate_item(VALID_SKILL_ID, "easy", seed=VALID_SEED)
    is_valid, error_msg = validate_item(item)
    
    assert (is_valid, error_msg) == (True, ""), \
        f"Generated item should be valid, got ({is_valid}, {error_msg})"
