"""
Guardrail tests for skill registry to prevent accidental duplication and regressions.

These tests ensure:
1. SKILL_TEMPLATES is non-empty and well-formed
2. No duplicate stems within any (skill, difficulty) pool
3. All items have exactly 4 choices with valid solution indices
"""

import pytest

from engine.templates import SKILL_TEMPLATES


def test_no_duplicate_skill_ids():
    """SKILL_TEMPLATES must be non-empty (keys are unique by dict definition)."""
    assert SKILL_TEMPLATES, "SKILL_TEMPLATES must not be empty"


def test_no_duplicate_stems_within_pool():
    """Within each (skill, difficulty), stems must be unique (no repeats)."""
    for skill, diffs in SKILL_TEMPLATES.items():
        assert isinstance(diffs, dict), f"{skill} diffs must be a dict"
        
        for diff, items in diffs.items():
            stems = [i["stem"] for i in items]
            
            # Check for duplicates
            if len(stems) != len(set(stems)):
                duplicates = [s for s in set(stems) if stems.count(s) > 1]
                pytest.fail(
                    f"Duplicate stems in {skill}:{diff}:\n"
                    f"  Duplicates: {duplicates}"
                )


def test_choices_are_4_and_solution_index_valid():
    """All items must have exactly 4 choices with valid solution indices (0-3)."""
    for skill, diffs in SKILL_TEMPLATES.items():
        for diff, items in diffs.items():
            for idx, item in enumerate(items):
                # Check 4 choices
                assert len(item["choices"]) == 4, (
                    f"{skill}:{diff}[{idx}] must have exactly 4 choices, "
                    f"got {len(item['choices'])}"
                )
                
                # Check solution index is in range
                assert 0 <= item["solution"] < 4, (
                    f"{skill}:{diff}[{idx}] solution index {item['solution']} "
                    f"out of range [0, 3]"
                )


def test_all_items_have_required_fields():
    """All items must have stem, choices, solution, and rationale."""
    required_fields = {"stem", "choices", "solution", "rationale"}
    
    for skill, diffs in SKILL_TEMPLATES.items():
        for diff, items in diffs.items():
            for idx, item in enumerate(items):
                missing = required_fields - set(item.keys())
                assert not missing, (
                    f"{skill}:{diff}[{idx}] missing fields: {missing}"
                )
