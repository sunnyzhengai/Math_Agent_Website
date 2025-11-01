"""
Shared fixtures and constants for item tests.
"""

import pytest


# Skill ID known to exist (will be implemented in generate_item)
VALID_SKILL_ID = "quad.graph.vertex"

# Valid seed for deterministic tests
VALID_SEED = 42

# Alternative valid seed for variance testing
ALTERNATE_SEED = 43

# Valid difficulties
VALID_DIFFICULTIES = ["easy", "medium", "hard", "applied"]


@pytest.fixture
def valid_item_dict():
    """
    A manually constructed valid item that passes the contract.
    Used as a positive control in validator tests.
    """
    return {
        "item_id": "quad.graph.vertex:easy:42",
        "skill_id": "quad.graph.vertex",
        "difficulty": "easy",
        "stem": "For y = (x - 3)^2 + 2, what is the vertex?",
        "choices": [
            {"id": "A", "text": "(3, 2)"},
            {"id": "B", "text": "(-3, 2)"},
            {"id": "C", "text": "(3, -2)"},
            {"id": "D", "text": "(2, 3)"},
        ],
        "solution_choice_id": "A",
        "solution_text": "(3, 2)",
        "tags": ["vertex_form"],
    }
