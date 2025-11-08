"""
Acceptance tests for Oracle Agent reflection implementation.

Validates Andrew Ng's Reflection pattern:
- Self-assessment of confidence
- Multiple solving attempts for low confidence
- Disagreement resolution through reasoning comparison
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agentic.agents.oracle import OracleAgent
from engine.templates import generate_item


def test_reflection_enabled_by_default():
    """Test that reflection is enabled by default."""
    agent = OracleAgent()
    assert agent.use_reflection is True, "Reflection should be enabled by default"
    assert agent.reflection_threshold == 0.9, "Default confidence threshold should be 0.9"


def test_reflection_can_be_disabled():
    """Test that reflection can be disabled for backwards compatibility."""
    agent = OracleAgent(use_reflection=False)
    assert agent.use_reflection is False, "Reflection should be disabled when requested"


def test_reflection_stats_tracking():
    """Test that reflection statistics are tracked correctly."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Skipping test: ANTHROPIC_API_KEY not set")
        return

    agent = OracleAgent(use_reflection=True)

    # Generate a simple question
    item = generate_item(
        skill_id="solve_by_factoring",
        difficulty="easy",
        template_id="standard_factoring_easy"
    )

    # Solve the question
    answer = agent.choose(item)

    # Check that stats were tracked
    stats = agent.get_reflection_stats()
    assert stats["total_solves"] == 1, "Should track total solves"
    assert "reflection_triggered" in stats, "Should track reflection triggers"
    assert "disagreements_resolved" in stats, "Should track disagreement resolutions"
    assert "confidence_below_threshold" in stats, "Should track low confidence cases"

    print(f"✓ Reflection stats tracking works")
    print(f"  Stats: {stats}")


def test_oracle_accuracy_maintained():
    """Test that Oracle maintains 100% accuracy with reflection enabled."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Skipping test: ANTHROPIC_API_KEY not set")
        return

    agent = OracleAgent(use_reflection=True)

    # Test across different skills and difficulties
    test_cases = [
        ("solve_by_factoring", "easy"),
        ("solve_by_factoring", "medium"),
        ("find_vertex_from_standard", "easy"),
        ("find_vertex_from_vertex_form", "easy"),
        ("quadratic_formula", "medium"),
    ]

    correct = 0
    total = 0

    for skill_id, difficulty in test_cases:
        # Generate question
        item = generate_item(skill_id=skill_id, difficulty=difficulty)

        # Solve with reflection
        answer = agent.choose(item)

        # Check correctness
        correct_answer = item["solution_choice_id"]

        total += 1
        if answer == correct_answer:
            correct += 1
            print(f"✓ {skill_id} ({difficulty}): {answer} = {correct_answer}")
        else:
            print(f"✗ {skill_id} ({difficulty}): {answer} ≠ {correct_answer}")

    accuracy = (correct / total) * 100
    print(f"\nAccuracy: {accuracy:.1f}% ({correct}/{total})")

    assert accuracy == 100.0, f"Oracle accuracy must be 100%, got {accuracy:.1f}%"


def test_reflection_disabled_still_works():
    """Test that disabling reflection doesn't break existing functionality."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Skipping test: ANTHROPIC_API_KEY not set")
        return

    agent = OracleAgent(use_reflection=False)

    # Generate a simple question
    item = generate_item(
        skill_id="solve_by_factoring",
        difficulty="easy",
    )

    # Solve without reflection
    answer = agent.choose(item)
    correct_answer = item["solution_choice_id"]

    assert answer == correct_answer, "Oracle should still work with reflection disabled"
    print(f"✓ Non-reflection mode works: {answer} = {correct_answer}")


def test_stats_getter_returns_copy():
    """Test that get_reflection_stats returns a copy, not the original."""
    agent = OracleAgent()

    stats1 = agent.get_reflection_stats()
    stats1["total_solves"] = 999

    stats2 = agent.get_reflection_stats()

    assert stats2["total_solves"] == 0, "Should return copy, not original"
    print("✓ Stats getter returns copy (immutable)")


if __name__ == "__main__":
    print("=" * 70)
    print("ORACLE REFLECTION ACCEPTANCE TESTS")
    print("=" * 70)
    print()

    # Run all tests
    test_reflection_enabled_by_default()
    print()

    test_reflection_can_be_disabled()
    print()

    test_stats_getter_returns_copy()
    print()

    test_reflection_stats_tracking()
    print()

    test_reflection_disabled_still_works()
    print()

    test_oracle_accuracy_maintained()
    print()

    print("=" * 70)
    print("ALL ACCEPTANCE TESTS PASSED ✓")
    print("=" * 70)
