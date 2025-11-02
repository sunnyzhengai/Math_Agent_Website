"""
Golden snapshot tests for seed=42, easy difficulty.

Validates that generate_item() produces byte-for-byte deterministic output
across all five quadratic skills.
"""

import json
from pathlib import Path

import pytest

from engine.templates import generate_item


# Golden file paths
GOLDEN_DIR = Path(__file__).parent.parent / "goldens"

GOLDEN_CASES = [
    ("quad.graph.vertex", "golden_item_quad_graph_vertex_easy_42.json"),
    ("quad.standard.vertex", "golden_item_quad_standard_vertex_easy_42.json"),
    ("quad.roots.factored", "golden_item_quad_roots_factored_easy_42.json"),
    ("quad.solve.by_factoring", "golden_item_quad_solve_by_factoring_easy_42.json"),
    ("quad.solve.by_formula", "golden_item_quad_solve_by_formula_easy_42.json"),
]


@pytest.mark.parametrize("skill_id,golden_file", GOLDEN_CASES)
def test_golden_item_easy_seed_42(skill_id, golden_file):
    """
    Verify that generate_item(skill, "easy", seed=42) matches golden snapshot.
    
    This is a regression test: any change to the item generation logic,
    choice shuffling, or template will fail this test, alerting us to:
    - Intentional changes (update golden after review)
    - Accidental regressions (fix the code)
    
    The test does byte-for-byte comparison to catch:
    - Choice order changes
    - Solution ID shifts
    - Stem/rationale wording changes
    - Tags additions/removals
    """
    # Load golden
    golden_path = GOLDEN_DIR / golden_file
    assert golden_path.exists(), f"Golden file missing: {golden_path}"
    
    with open(golden_path) as f:
        golden = json.load(f)
    
    # Generate item deterministically
    generated = generate_item(skill_id, "easy", seed=42)
    
    # Compare field by field for clear error messages
    assert generated["item_id"] == golden["item_id"], \
        f"item_id mismatch: {generated['item_id']} != {golden['item_id']}"
    
    assert generated["skill_id"] == golden["skill_id"], \
        f"skill_id mismatch: {generated['skill_id']} != {golden['skill_id']}"
    
    assert generated["difficulty"] == golden["difficulty"], \
        f"difficulty mismatch: {generated['difficulty']} != {golden['difficulty']}"
    
    assert generated["stem"] == golden["stem"], \
        f"stem mismatch: {generated['stem']} != {golden['stem']}"
    
    assert len(generated["choices"]) == len(golden["choices"]), \
        f"choice count mismatch: {len(generated['choices'])} != {len(golden['choices'])}"
    
    # Check choice order and IDs
    for i, (gen_choice, gold_choice) in enumerate(zip(generated["choices"], golden["choices"])):
        assert gen_choice["id"] == gold_choice["id"], \
            f"choice {i} id mismatch: {gen_choice['id']} != {gold_choice['id']}"
        assert gen_choice["text"] == gold_choice["text"], \
            f"choice {i} text mismatch: {gen_choice['text']} != {gold_choice['text']}"
    
    assert generated["solution_choice_id"] == golden["solution_choice_id"], \
        f"solution_choice_id mismatch: {generated['solution_choice_id']} != {golden['solution_choice_id']}"
    
    assert generated["solution_text"] == golden["solution_text"], \
        f"solution_text mismatch: {generated['solution_text']} != {golden['solution_text']}"
    
    assert set(generated.get("tags", [])) == set(golden.get("tags", [])), \
        f"tags mismatch: {generated.get('tags', [])} != {golden.get('tags', [])}"
    
    # If all fields match, do a full deep equality check
    assert generated == golden, \
        f"Full item mismatch.\nGenerated:\n{json.dumps(generated, indent=2)}\n\nGolden:\n{json.dumps(golden, indent=2)}"


def test_all_golden_files_exist():
    """Sanity check: verify all golden files are present."""
    for skill_id, golden_file in GOLDEN_CASES:
        golden_path = GOLDEN_DIR / golden_file
        assert golden_path.exists(), f"Missing golden: {golden_path}"


def test_golden_files_are_valid_json():
    """Sanity check: verify all golden files are parseable JSON."""
    for skill_id, golden_file in GOLDEN_CASES:
        golden_path = GOLDEN_DIR / golden_file
        with open(golden_path) as f:
            data = json.load(f)
        assert isinstance(data, dict), f"Golden {golden_file} is not a dict"
        assert "item_id" in data, f"Golden {golden_file} missing item_id"
        assert "choices" in data, f"Golden {golden_file} missing choices"
