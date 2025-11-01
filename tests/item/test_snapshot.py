"""
Group 3: Snapshot (golden) test

This test guards against drift in deterministic generation.
Locked after Phase-1 core is verified.
"""

import json
from pathlib import Path
import pytest
from engine.templates import generate_item


def test_item_snapshot_quad_vertex_easy_42():
    """
    Test 11: Verify deterministic generation against golden baseline.
    
    Checks:
    - Generates item with ("quad.graph.vertex", "easy", seed=42)
    - Compares against frozen golden JSON file
    - Fails if any field differs → guards against accidental drift
    
    Golden file: tests/goldens/golden_item_quad_graph_vertex_easy_42.json
    """
    # Generate item
    generated = generate_item("quad.graph.vertex", "easy", seed=42)
    
    # Load golden baseline
    golden_path = Path(__file__).parent.parent / "goldens" / "golden_item_quad_graph_vertex_easy_42.json"
    with open(golden_path) as f:
        golden = json.load(f)
    
    # Assert exact match (deep equality)
    assert generated == golden, \
        f"Generated item differs from golden baseline.\nGenerated: {json.dumps(generated, indent=2)}\n" \
        f"Golden: {json.dumps(golden, indent=2)}"
