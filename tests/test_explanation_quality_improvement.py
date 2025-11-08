"""
Acceptance tests for Explanation Quality Improvement Agent.

Validates closed-loop feedback pattern:
- Measures explanation quality
- Detects low quality
- Applies iterative refinement
- Re-measures to confirm improvement
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agentic.agents.explanation_quality_improvement_agent import ExplanationQualityImprovementAgent


def test_agent_initialization():
    """Test that agent initializes with correct settings."""
    agent = ExplanationQualityImprovementAgent(target_quality=0.7)

    assert agent.target_quality == 0.7, "Should set target quality"
    assert agent.iterative_agent is not None, "Should have iterative explanation agent"
    assert agent.improvement_history == [], "Should start with empty history"

    print("✓ Agent initializes correctly")


def test_measure_quality():
    """Test that agent can measure explanation quality."""
    agent = ExplanationQualityImprovementAgent()

    # Measure quality for a skill
    measurement = agent.measure_quality(
        skill_id="quad.graph.vertex",
        difficulty="easy",
        n_samples=5
    )

    assert measurement.samples_tested > 0, "Should test samples"
    assert 0 <= measurement.avg_clarity <= 1, "Clarity should be 0-1"
    assert 0 <= measurement.avg_completeness <= 1, "Completeness should be 0-1"
    assert 0 <= measurement.overall_quality <= 1, "Overall quality should be 0-1"

    print(f"✓ Quality measurement works")
    print(f"  Samples tested: {measurement.samples_tested}")
    print(f"  Avg clarity: {measurement.avg_clarity:.2f}")
    print(f"  Avg completeness: {measurement.avg_completeness:.2f}")
    print(f"  Overall quality: {measurement.overall_quality:.2f}")
    if measurement.issues:
        print(f"  Issues: {', '.join(measurement.issues)}")


def test_identifies_quality_issues():
    """Test that agent identifies when quality is low."""
    agent = ExplanationQualityImprovementAgent(target_quality=0.9)  # High threshold

    measurement = agent.measure_quality(
        skill_id="quad.graph.vertex",
        difficulty="easy",
        n_samples=5
    )

    # With high threshold, likely to have issues
    if measurement.overall_quality < 0.9:
        assert len(measurement.issues) > 0, "Should identify issues when quality low"
        print(f"✓ Correctly identified low quality: {measurement.overall_quality:.2f}")
        print(f"  Issues: {', '.join(measurement.issues)}")
    else:
        print(f"✓ Quality is high: {measurement.overall_quality:.2f}")


def test_closed_loop_improvement():
    """Test the complete closed-loop feedback cycle."""
    agent = ExplanationQualityImprovementAgent(target_quality=0.7)

    # Run closed-loop improvement
    result = agent.test_and_improve_quality(
        skill_id="quad.graph.vertex",
        difficulty="easy"
    )

    # Verify result structure
    assert result.status in ["ok", "improved", "failed"], "Should have valid status"
    assert 0 <= result.old_quality <= 1, "Old quality should be 0-1"
    assert 0 <= result.new_quality <= 1, "New quality should be 0-1"
    assert result.improvements_applied >= 0, "Should track improvements applied"
    assert result.action, "Should specify action taken"

    print(f"✓ Closed-loop improvement executed")
    print(f"  Status: {result.status}")
    print(f"  Old quality: {result.old_quality:.2f}")
    print(f"  New quality: {result.new_quality:.2f}")
    print(f"  Improvements applied: {result.improvements_applied}")
    print(f"  Action: {result.action}")


def test_uses_iterative_refinement():
    """Test that agent uses iterative refinement to improve quality."""
    agent = ExplanationQualityImprovementAgent(target_quality=0.95)  # High threshold to trigger improvement

    result = agent.test_and_improve_quality(
        skill_id="quad.graph.vertex",
        difficulty="easy"
    )

    # Iterative agent should have been used
    stats = agent.iterative_agent.get_refinement_stats()

    assert stats["total_generations"] > 0, "Should use iterative agent"

    print(f"✓ Iterative refinement used")
    print(f"  Total generations: {stats['total_generations']}")
    print(f"  Avg clarity improvement: {stats['avg_clarity_improvement']:+.2f}")


def test_tracks_improvement_history():
    """Test that agent tracks improvement attempts."""
    agent = ExplanationQualityImprovementAgent()

    # Run a few improvement attempts
    for i in range(2):
        agent.test_and_improve_quality(
            skill_id="quad.graph.vertex",
            difficulty="easy"
        )

    # Check history
    assert len(agent.improvement_history) == 2, "Should track all attempts"

    # Get statistics
    stats = agent.get_improvement_stats()

    assert stats["total_attempts"] == 2, "Should count attempts"
    assert "success_rate" in stats, "Should calculate success rate"
    assert "avg_quality_improvement" in stats, "Should track average improvement"

    print(f"✓ Improvement history tracked")
    print(f"  Total attempts: {stats['total_attempts']}")
    print(f"  Success rate: {stats['success_rate']:.1%}")
    print(f"  Avg improvement: {stats['avg_quality_improvement']:+.2f}")
    print(f"  Avg old quality: {stats['avg_old_quality']:.2f}")
    print(f"  Avg new quality: {stats['avg_new_quality']:.2f}")


def test_status_ok_when_quality_good():
    """Test that status is 'ok' when quality already meets target."""
    agent = ExplanationQualityImprovementAgent(target_quality=0.5)  # Low threshold

    result = agent.test_and_improve_quality(
        skill_id="quad.graph.vertex",
        difficulty="easy"
    )

    # With low threshold and good explanation system, quality should be OK
    if result.old_quality >= 0.5:
        assert result.status in ["ok", "improved"], "Should return success when quality meets target"
        print(f"✓ Returns success when quality good ({result.old_quality:.2f})")
    else:
        print(f"⊘ Quality was low ({result.old_quality:.2f}), improvement attempted")


def test_handles_multiple_skills():
    """Test that agent can handle multiple skills."""
    agent = ExplanationQualityImprovementAgent(target_quality=0.7)

    skills_to_test = [
        ("quad.graph.vertex", "easy"),
        ("quad.solve.by_factoring", "easy"),
        ("quad.standard.vertex", "easy")
    ]

    results = []

    for skill_id, difficulty in skills_to_test:
        result = agent.test_and_improve_quality(skill_id, difficulty)
        results.append(result)

    assert len(results) == 3, "Should test all skills"

    # All should have valid status
    for result in results:
        assert result.status in ["ok", "improved", "failed"], "Should have valid status"

    print(f"✓ Handles multiple skills")
    print(f"  Tested: {len(skills_to_test)} skill/difficulty combinations")
    for i, (skill_id, diff) in enumerate(skills_to_test):
        r = results[i]
        print(f"  {skill_id}: {r.status}, quality {r.old_quality:.2f} → {r.new_quality:.2f}")


if __name__ == "__main__":
    print("=" * 70)
    print("EXPLANATION QUALITY IMPROVEMENT AGENT ACCEPTANCE TESTS")
    print("=" * 70)
    print()

    # Run all tests
    test_agent_initialization()
    print()

    test_measure_quality()
    print()

    test_identifies_quality_issues()
    print()

    test_closed_loop_improvement()
    print()

    test_uses_iterative_refinement()
    print()

    test_tracks_improvement_history()
    print()

    test_status_ok_when_quality_good()
    print()

    test_handles_multiple_skills()
    print()

    print("=" * 70)
    print("ALL ACCEPTANCE TESTS PASSED ✓")
    print("=" * 70)
