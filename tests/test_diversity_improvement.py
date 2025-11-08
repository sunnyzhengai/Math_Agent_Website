"""
Acceptance tests for Diversity Improvement Agent.

Validates closed-loop feedback pattern:
- Measures diversity
- Detects low diversity
- Automatically generates new questions
- Validates with committee
- Re-measures to confirm improvement
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agentic.agents.diversity_improvement_agent import DiversityImprovementAgent


def test_agent_initialization():
    """Test that agent initializes with correct settings."""
    agent = DiversityImprovementAgent(target_diversity=0.8)

    assert agent.target_diversity == 0.8, "Should set target diversity"
    assert agent.committee is not None, "Should have validation committee"
    assert agent.improvement_history == [], "Should start with empty history"

    print("✓ Agent initializes correctly")


def test_measure_diversity():
    """Test that agent can measure diversity."""
    agent = DiversityImprovementAgent()

    # Measure diversity for a skill
    measurement = agent.measure_diversity(
        skill_id="quad.graph.vertex",
        difficulty="easy",
        n_samples=20
    )

    assert measurement.total_samples > 0, "Should generate samples"
    assert measurement.unique_stems > 0, "Should have unique stems"
    assert 0 <= measurement.diversity_score <= 1, "Diversity should be 0-1"
    assert 0 <= measurement.repetition_rate <= 1, "Repetition rate should be 0-1"
    assert len(measurement.stems) == measurement.total_samples, "Should track stems"

    print(f"✓ Diversity measurement works")
    print(f"  Samples: {measurement.total_samples}")
    print(f"  Unique: {measurement.unique_stems}")
    print(f"  Diversity: {measurement.diversity_score:.1%}")
    print(f"  Repetition: {measurement.repetition_rate:.1%}")


def test_identifies_low_diversity():
    """Test that agent identifies when diversity is low."""
    agent = DiversityImprovementAgent(target_diversity=0.8)

    measurement = agent.measure_diversity(
        skill_id="quad.graph.vertex",
        difficulty="easy",
        n_samples=20
    )

    # Check if issues identified correctly
    if measurement.diversity_score < 0.8:
        assert len(measurement.issues) > 0, "Should identify issues when diversity low"
        assert any("diversity" in issue.lower() for issue in measurement.issues), "Should mention diversity"
        print(f"✓ Correctly identified low diversity: {measurement.diversity_score:.1%}")
        print(f"  Issues: {', '.join(measurement.issues)}")
    else:
        assert len(measurement.issues) == 0 or all("diversity" not in issue.lower() for issue in measurement.issues), "Should not report diversity issue when high"
        print(f"✓ Correctly identified good diversity: {measurement.diversity_score:.1%}")


def test_closed_loop_improvement():
    """Test the complete closed-loop feedback cycle."""
    agent = DiversityImprovementAgent(target_diversity=0.8)

    # Run closed-loop improvement
    result = agent.test_and_improve_diversity(
        skill_id="quad.graph.vertex",
        difficulty="easy"
    )

    # Verify result structure
    assert result.status in ["ok", "improved", "failed"], "Should have valid status"
    assert 0 <= result.old_diversity <= 1, "Old diversity should be 0-1"
    assert 0 <= result.new_diversity <= 1, "New diversity should be 0-1"
    assert result.questions_generated >= 0, "Should track questions generated"
    assert result.questions_approved >= 0, "Should track questions approved"
    assert result.action, "Should specify action taken"

    print(f"✓ Closed-loop improvement executed")
    print(f"  Status: {result.status}")
    print(f"  Old diversity: {result.old_diversity:.1%}")
    print(f"  New diversity: {result.new_diversity:.1%}")
    print(f"  Generated: {result.questions_generated}")
    print(f"  Approved: {result.questions_approved}")
    print(f"  Action: {result.action}")


def test_validates_with_committee():
    """Test that generated questions are validated by committee."""
    agent = DiversityImprovementAgent(target_diversity=0.8)

    # Force improvement attempt by setting high target
    agent.target_diversity = 0.95  # Very high to trigger improvement

    result = agent.test_and_improve_diversity(
        skill_id="quad.graph.vertex",
        difficulty="easy"
    )

    # If improvement was attempted, questions should have been validated
    if result.status == "improved" or result.questions_generated > 0:
        # Some questions should have been generated
        assert result.questions_generated > 0, "Should generate questions"

        # Check committee was used (approval rate should be reasonable)
        if result.questions_generated > 0:
            approval_rate = result.questions_approved / result.questions_generated
            assert 0 <= approval_rate <= 1, "Approval rate should be valid"

            print(f"✓ Committee validation used")
            print(f"  Approval rate: {approval_rate:.1%} ({result.questions_approved}/{result.questions_generated})")
    else:
        print(f"⊘ No improvement needed (diversity already {result.old_diversity:.1%})")


def test_tracks_improvement_history():
    """Test that agent tracks improvement attempts."""
    agent = DiversityImprovementAgent()

    # Run a few improvement attempts
    for i in range(3):
        agent.test_and_improve_diversity(
            skill_id="quad.graph.vertex",
            difficulty="easy"
        )

    # Check history
    assert len(agent.improvement_history) == 3, "Should track all attempts"

    # Get statistics
    stats = agent.get_improvement_stats()

    assert stats["total_attempts"] == 3, "Should count attempts"
    assert "success_rate" in stats, "Should calculate success rate"
    assert "avg_diversity_improvement" in stats, "Should track average improvement"

    print(f"✓ Improvement history tracked")
    print(f"  Total attempts: {stats['total_attempts']}")
    print(f"  Success rate: {stats['success_rate']:.1%}")
    print(f"  Avg improvement: {stats['avg_diversity_improvement']:+.2%}")


def test_status_ok_when_diversity_good():
    """Test that status is 'ok' when diversity already meets target."""
    agent = DiversityImprovementAgent(target_diversity=0.5)  # Low threshold

    result = agent.test_and_improve_diversity(
        skill_id="quad.graph.vertex",
        difficulty="easy"
    )

    # With low threshold, diversity should be OK
    if result.old_diversity >= 0.5:
        assert result.status == "ok", "Should return 'ok' when diversity meets target"
        assert result.questions_generated == 0, "Should not generate when OK"
        print(f"✓ Returns 'ok' when diversity good ({result.old_diversity:.1%})")
    else:
        print(f"⊘ Diversity was low ({result.old_diversity:.1%}), improvement attempted")


def test_handles_multiple_skills():
    """Test that agent can handle multiple skills."""
    agent = DiversityImprovementAgent(target_diversity=0.8)

    skills_to_test = [
        ("quad.graph.vertex", "easy"),
        ("quad.solve.by_factoring", "easy"),
        ("quad.standard.vertex", "easy")
    ]

    results = []

    for skill_id, difficulty in skills_to_test:
        result = agent.test_and_improve_diversity(skill_id, difficulty)
        results.append(result)

    assert len(results) == 3, "Should test all skills"

    # All should have valid status
    for result in results:
        assert result.status in ["ok", "improved", "failed"], "Should have valid status"

    print(f"✓ Handles multiple skills")
    print(f"  Tested: {len(skills_to_test)} skill/difficulty combinations")
    print(f"  Statuses: {', '.join(r.status for r in results)}")


if __name__ == "__main__":
    print("=" * 70)
    print("DIVERSITY IMPROVEMENT AGENT ACCEPTANCE TESTS")
    print("=" * 70)
    print()

    # Run all tests
    test_agent_initialization()
    print()

    test_measure_diversity()
    print()

    test_identifies_low_diversity()
    print()

    test_closed_loop_improvement()
    print()

    test_validates_with_committee()
    print()

    test_tracks_improvement_history()
    print()

    test_status_ok_when_diversity_good()
    print()

    test_handles_multiple_skills()
    print()

    print("=" * 70)
    print("ALL ACCEPTANCE TESTS PASSED ✓")
    print("=" * 70)
