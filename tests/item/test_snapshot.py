"""
Group 3: Snapshot (golden) test

This test guards against drift once all other tests pass.
Will be implemented after tests 1-10 are green.
"""

import pytest


def test_item_snapshot_quad_vertex_easy_42():
    """
    Test 11: Guard against drift once everything passes.
    
    Checks:
    - Calls generate_item("quad.graph.vertex", "easy", seed=42)
    - Compares filtered dict (id, skill_id, difficulty, stem, choices[id,text], solution_choice_id)
      to the golden JSON file
    - Fails if any field differs → forces conscious update
    
    Note: This test will be implemented after tests 1-10 are all green.
    """
    pytest.skip("Golden snapshot test — implement after core tests pass")
