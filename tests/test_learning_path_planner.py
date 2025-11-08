"""
Acceptance tests for Learning Path Planner.

Validates Andrew Ng's Planning pattern:
- Prerequisite analysis
- Gap identification
- Dependency-based sequencing
- Time estimation
- Checkpoint creation
- Spaced repetition scheduling
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agentic.agents.learning_path_planner import (
    LearningPathPlanner,
    StudentProfile
)


def test_planner_initialization():
    """Test that planner initializes with correct settings."""
    planner = LearningPathPlanner(mastery_threshold=0.7)

    assert planner.mastery_threshold == 0.7, "Should set mastery threshold"
    assert planner.PREREQUISITE_GRAPH, "Should have prerequisite graph"
    assert planner.MASTERY_ESTIMATES, "Should have mastery estimates"

    print("✓ Planner initializes correctly")


def test_student_profile():
    """Test student profile creation."""
    student = StudentProfile(
        student_id="test_123",
        mastered_skills=["quad.graph.vertex", "quad.roots.factored"],
        learning_rate_avg=0.15
    )

    mastery = student.get_mastery_levels()

    assert mastery["quad.graph.vertex"] == 1.0, "Mastered skills should be 1.0"
    assert mastery["quad.roots.factored"] == 1.0, "Mastered skills should be 1.0"

    print("✓ Student profile works correctly")


def test_prerequisite_chain():
    """Test that prerequisite chains are identified correctly."""
    planner = LearningPathPlanner()

    # Test simple skill with no prerequisites
    chain = planner._get_prerequisite_chain("quad.graph.vertex")
    assert chain == [], "Basic skill should have no prerequisites"

    # Test skill with prerequisites
    chain = planner._get_prerequisite_chain("quad.solve.by_formula")
    assert "quad.discriminant.analysis" in chain, "Should include direct prerequisite"
    assert "quad.standard.vertex" in chain, "Should include transitive prerequisite"
    assert "quad.graph.vertex" in chain, "Should include root prerequisite"

    print(f"✓ Prerequisite chain identified correctly")
    print(f"  Chain for quad.solve.by_formula: {chain}")


def test_topological_sort():
    """Test that skills are ordered by dependencies."""
    planner = LearningPathPlanner()

    skills = [
        "quad.solve.by_formula",
        "quad.discriminant.analysis",
        "quad.standard.vertex",
        "quad.graph.vertex"
    ]

    sorted_skills = planner._topological_sort(skills)

    # Verify order respects dependencies
    vertex_idx = sorted_skills.index("quad.graph.vertex")
    standard_idx = sorted_skills.index("quad.standard.vertex")
    discriminant_idx = sorted_skills.index("quad.discriminant.analysis")
    formula_idx = sorted_skills.index("quad.solve.by_formula")

    assert vertex_idx < standard_idx, "quad.graph.vertex must come before quad.standard.vertex"
    assert standard_idx < discriminant_idx, "quad.standard.vertex must come before quad.discriminant.analysis"
    assert discriminant_idx < formula_idx, "quad.discriminant.analysis must come before quad.solve.by_formula"

    print(f"✓ Topological sort respects dependencies")
    print(f"  Ordered sequence: {sorted_skills}")


def test_plan_to_mastery_beginner():
    """Test planning for a beginner student."""
    planner = LearningPathPlanner()

    # Beginner student with only one skill
    student = StudentProfile(
        student_id="beginner",
        mastered_skills=["quad.graph.vertex"],
        learning_rate_avg=0.15
    )

    # Plan to master quadratic formula (complex skill)
    plan = planner.plan_to_mastery(student, "quad.solve.by_formula")

    # Should identify multiple prerequisites
    assert len(plan.phases) >= 2, "Should have multiple phases for complex skill"

    # Target skill should be last
    assert plan.phases[-1].skill_id == "quad.solve.by_formula", "Target should be last phase"

    # All phases should have time estimates
    for phase in plan.phases:
        assert phase.estimated_hours > 0, "Each phase should have time estimate"

    # Should have checkpoints
    for phase in plan.phases:
        assert phase.checkpoint is not None, "Each phase should have checkpoint"
        assert phase.checkpoint["type"] == "mastery_check", "Checkpoint should be mastery check"

    # Should have review schedules
    for phase in plan.phases:
        assert len(phase.review_schedule) > 0, "Should have review schedule"

    # Should have fallback strategies
    for phase in plan.phases:
        assert len(phase.fallback_strategies) > 0, "Should have fallback strategies"

    print(f"✓ Beginner plan created successfully")
    print(f"  Phases: {len(plan.phases)}")
    print(f"  Total estimated hours: {plan.total_estimated_hours:.1f}")
    print(f"  Prerequisite chain: {plan.prerequisite_chain}")
    for i, phase in enumerate(plan.phases):
        print(f"  Phase {i+1}: {phase.skill_id} ({phase.estimated_hours:.1f}h)")


def test_plan_to_mastery_advanced():
    """Test planning for an advanced student."""
    planner = LearningPathPlanner()

    # Advanced student with most skills mastered
    student = StudentProfile(
        student_id="advanced",
        mastered_skills=[
            "quad.graph.vertex",
            "quad.roots.factored",
            "quad.standard.vertex",
            "quad.discriminant.analysis"
        ],
        learning_rate_avg=0.20  # Faster learner
    )

    # Plan to master formula (should be shorter)
    plan = planner.plan_to_mastery(student, "quad.solve.by_formula")

    # Should have fewer phases (prerequisites already mastered)
    assert len(plan.phases) == 1, "Should only need target skill phase"
    assert plan.phases[0].skill_id == "quad.solve.by_formula", "Should be target skill"

    # Should have review sessions for mastered skills
    assert len(plan.review_sessions) > 0, "Should schedule reviews for mastered skills"

    print(f"✓ Advanced plan created successfully")
    print(f"  Phases: {len(plan.phases)}")
    print(f"  Total estimated hours: {plan.total_estimated_hours:.1f}")
    print(f"  Review sessions: {len(plan.review_sessions)}")


def test_time_estimation():
    """Test that time estimation considers student learning rate."""
    planner = LearningPathPlanner()

    # Fast learner
    fast_student = StudentProfile(
        student_id="fast",
        learning_rate_avg=0.30,  # 30 questions per hour
        current_progress={}
    )

    # Slow learner
    slow_student = StudentProfile(
        student_id="slow",
        learning_rate_avg=0.10,  # 10 questions per hour
        current_progress={}
    )

    skill = "quad.solve.by_factoring"

    fast_time = planner._estimate_time_to_mastery(skill, fast_student, 0.0)
    slow_time = planner._estimate_time_to_mastery(skill, slow_student, 0.0)

    # Slow learner should need more time
    assert slow_time > fast_time, "Slow learner should need more time"

    # With progress, time should be less
    partial_time = planner._estimate_time_to_mastery(skill, fast_student, 0.5)
    assert partial_time < fast_time, "Partial progress should reduce time"

    print(f"✓ Time estimation considers learning rate")
    print(f"  Fast learner: {fast_time:.1f}h")
    print(f"  Slow learner: {slow_time:.1f}h")
    print(f"  With 50% progress: {partial_time:.1f}h")


def test_spaced_repetition():
    """Test that spaced repetition is planned."""
    planner = LearningPathPlanner()

    review_schedule = planner._plan_spaced_reviews("quad.graph.vertex")

    # Should have multiple review points
    assert len(review_schedule) > 0, "Should have review schedule"

    # Should use increasing intervals (Fibonacci)
    assert review_schedule[0] < review_schedule[-1], "Intervals should increase"

    print(f"✓ Spaced repetition planned")
    print(f"  Review days: {review_schedule}")


def test_fallback_strategies():
    """Test that fallback strategies are created."""
    planner = LearningPathPlanner()

    strategies = planner._create_fallback_strategies("quad.solve.by_formula")

    # Should have multiple strategies
    assert len(strategies) > 0, "Should have fallback strategies"

    # Each strategy should have condition and action
    for strategy in strategies:
        assert "condition" in strategy, "Strategy should have condition"
        assert "action" in strategy, "Strategy should have action"
        assert "description" in strategy, "Strategy should have description"

    print(f"✓ Fallback strategies created")
    print(f"  Strategies: {len(strategies)}")
    for strategy in strategies:
        print(f"    - {strategy['condition']}: {strategy['action']}")


def test_checkpoint_creation():
    """Test that checkpoints are meaningful."""
    planner = LearningPathPlanner()

    checkpoint = planner._create_checkpoint("quad.solve.by_factoring")

    assert checkpoint["type"] == "mastery_check", "Should be mastery check"
    assert checkpoint["questions"] > 0, "Should have questions"
    assert checkpoint["passing_score"] > 0, "Should have passing score"
    assert "skill_id" in checkpoint, "Should reference skill"

    print(f"✓ Checkpoint created correctly")
    print(f"  Type: {checkpoint['type']}")
    print(f"  Questions: {checkpoint['questions']}")
    print(f"  Passing score: {checkpoint['passing_score']:.0%}")


if __name__ == "__main__":
    print("=" * 70)
    print("LEARNING PATH PLANNER ACCEPTANCE TESTS")
    print("=" * 70)
    print()

    # Run all tests
    test_planner_initialization()
    print()

    test_student_profile()
    print()

    test_prerequisite_chain()
    print()

    test_topological_sort()
    print()

    test_plan_to_mastery_beginner()
    print()

    test_plan_to_mastery_advanced()
    print()

    test_time_estimation()
    print()

    test_spaced_repetition()
    print()

    test_fallback_strategies()
    print()

    test_checkpoint_creation()
    print()

    print("=" * 70)
    print("ALL ACCEPTANCE TESTS PASSED ✓")
    print("=" * 70)
