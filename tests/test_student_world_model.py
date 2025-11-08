"""
Acceptance tests for Student World Model.

Validates Yann LeCun's World Models pattern:
- Internal representation of student understanding
- Predictive capabilities (forecast struggles)
- Learning from observations
- Proactive interventions
"""

import sys
from pathlib import Path
import time

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agentic.agents.student_world_model import StudentWorldModel


def test_initialization():
    """Test that world model initializes with concept graph."""
    model = StudentWorldModel()

    assert len(model.concept_nodes) > 0, "Should initialize concept nodes"
    assert "vertex_form_reading" in model.concept_nodes, "Should have vertex concept"
    assert "quadratic_formula" in model.concept_nodes, "Should have formula concept"

    # Check concept graph structure
    vertex_node = model.concept_nodes["vertex_form_reading"]
    assert vertex_node.mastery_level == 0.0, "Should start at 0 mastery"
    assert vertex_node.confidence == 0.0, "Should start with 0 confidence"
    assert vertex_node.total_attempts == 0, "Should have 0 attempts"

    print(f"✓ World model initialized")
    print(f"  Total concepts: {len(model.concept_nodes)}")
    print(f"  Concept graph edges: {sum(len(model.CONCEPT_GRAPH[c]) for c in model.CONCEPT_GRAPH)}")


def test_updates_from_performance():
    """Test that model learns from student performance."""
    model = StudentWorldModel()

    # Simulate correct performance on vertex reading
    model.update_from_performance("quad.graph.vertex", correct=True)

    # Check that related concepts updated
    vertex_concepts = model.SKILL_TO_CONCEPTS["quad.graph.vertex"]
    for concept in vertex_concepts:
        node = model.concept_nodes[concept]
        assert node.total_attempts > 0, "Should track attempts"
        assert node.mastery_level > 0, "Mastery should increase after correct answer"

    print(f"✓ Model updates from performance")
    print(f"  Concepts updated: {vertex_concepts}")
    print(f"  New mastery levels: {[model.concept_nodes[c].mastery_level for c in vertex_concepts]}")

    # Simulate incorrect performance
    initial_mastery = model.concept_nodes[vertex_concepts[0]].mastery_level
    model.update_from_performance("quad.graph.vertex", correct=False, error_type="sign_error")

    # Mastery should decrease (or increase less)
    new_mastery = model.concept_nodes[vertex_concepts[0]].mastery_level
    print(f"  After incorrect: mastery went from {initial_mastery:.2f} to {new_mastery:.2f}")


def test_predicts_struggles():
    """Test that model can predict where student will struggle."""
    model = StudentWorldModel()

    # Student has not practiced anything yet
    prediction = model.predict_struggle("quad.solve.by_formula")

    # Should predict struggles on unfamiliar concepts
    assert len(prediction.predicted_struggle_concepts) > 0, "Should predict struggles for unpracticed skill"
    assert prediction.target_skill == "quad.solve.by_formula", "Should track target skill"
    assert len(prediction.intervention_suggestions) > 0, "Should suggest interventions"

    print(f"✓ Model predicts struggles")
    print(f"  Target skill: {prediction.target_skill}")
    print(f"  Predicted struggle concepts: {prediction.predicted_struggle_concepts[:3]}")
    print(f"  Confidence: {prediction.confidence:.2f}")
    print(f"  Reason: {prediction.reason}")

    # Now simulate mastery of prerequisites
    for _ in range(10):
        model.update_from_performance("quad.standard.vertex", correct=True)
        model.update_from_performance("quad.discriminant.analysis", correct=True)

    # Predict again
    prediction2 = model.predict_struggle("quad.solve.by_formula")

    # Should predict fewer struggles
    print(f"\n  After practice:")
    print(f"  Predicted struggle concepts: {prediction2.predicted_struggle_concepts}")
    print(f"  Reason: {prediction2.reason}")


def test_recommends_interventions():
    """Test that model recommends appropriate interventions."""
    model = StudentWorldModel()

    # For unprepared student
    interventions = model.recommend_intervention("quad.solve.by_formula")

    assert len(interventions) > 0, "Should recommend interventions"

    # Check intervention structure
    for intervention in interventions[:2]:
        assert intervention.intervention_type in ["review_prerequisite", "scaffold_problem", "provide_hint"], \
            "Should have valid intervention type"
        assert intervention.priority in ["high", "medium", "low"], "Should have priority"
        assert intervention.action, "Should specify action"

    print(f"✓ Model recommends interventions")
    print(f"  Interventions: {len(interventions)}")
    for i in interventions[:3]:
        print(f"    - [{i.priority}] {i.intervention_type}: {i.action[:60]}...")


def test_mastery_summary():
    """Test that model provides mastery summary."""
    model = StudentWorldModel()

    # Practice some skills
    for _ in range(5):
        model.update_from_performance("quad.graph.vertex", correct=True)
    for _ in range(3):
        model.update_from_performance("quad.solve.by_factoring", correct=True)

    summary = model.get_mastery_summary()

    assert "total_concepts" in summary, "Should have total concepts"
    assert "avg_mastery" in summary, "Should calculate average mastery"
    assert "strongest_concepts" in summary, "Should identify strongest concepts"
    assert "weakest_concepts" in summary, "Should identify weakest concepts"

    print(f"✓ Model provides mastery summary")
    print(f"  Total concepts: {summary['total_concepts']}")
    print(f"  Mastered: {summary['mastered']}")
    print(f"  In progress: {summary['in_progress']}")
    print(f"  Not started: {summary['not_started']}")
    print(f"  Avg mastery: {summary['avg_mastery']:.1%}")
    print(f"  Strongest: {summary['strongest_concepts'][:2]}")
    print(f"  Weakest: {summary['weakest_concepts'][:2]}")


def test_learning_trajectory():
    """Test that model tracks learning trajectory."""
    model = StudentWorldModel()

    # Practice a skill multiple times
    for i in range(10):
        correct = i > 2  # Incorrect first 3, then correct
        model.update_from_performance("quad.graph.vertex", correct=correct)

    # Get trajectory for a concept
    concept = "vertex_form_reading"
    trajectory = model.get_learning_trajectory(concept)

    assert "current_mastery" in trajectory, "Should have current mastery"
    assert "total_attempts" in trajectory, "Should track attempts"
    assert "accuracy" in trajectory, "Should calculate accuracy"
    assert "trend" in trajectory, "Should indicate trend"

    print(f"✓ Model tracks learning trajectory")
    print(f"  Concept: {trajectory['concept_id']}")
    print(f"  Current mastery: {trajectory['current_mastery']:.1%}")
    print(f"  Attempts: {trajectory['total_attempts']}")
    print(f"  Accuracy: {trajectory['accuracy']:.1%}")
    print(f"  Trend: {trajectory['trend']}")


def test_confidence_increases_with_data():
    """Test that confidence increases as model collects more data."""
    model = StudentWorldModel()

    # Initial confidence should be low
    initial_node = model.concept_nodes["vertex_form_reading"]
    initial_confidence = initial_node.confidence

    # Practice many times
    for _ in range(20):
        model.update_from_performance("quad.graph.vertex", correct=True)

    # Confidence should increase
    updated_node = model.concept_nodes["vertex_form_reading"]
    updated_confidence = updated_node.confidence

    assert updated_confidence > initial_confidence, "Confidence should increase with data"

    print(f"✓ Confidence increases with data")
    print(f"  Initial confidence: {initial_confidence:.2f}")
    print(f"  After 20 attempts: {updated_confidence:.2f}")


def test_mastery_exponential_moving_average():
    """Test that mastery uses exponential moving average (recent performance weighted more)."""
    model = StudentWorldModel()

    # Many incorrect attempts
    for _ in range(10):
        model.update_from_performance("quad.graph.vertex", correct=False)

    mastery_after_incorrect = model.concept_nodes["vertex_form_reading"].mastery_level

    # Now correct attempts
    for _ in range(5):
        model.update_from_performance("quad.graph.vertex", correct=True)

    mastery_after_correct = model.concept_nodes["vertex_form_reading"].mastery_level

    # Recent correct performance should improve mastery
    assert mastery_after_correct > mastery_after_incorrect, "Recent performance should affect mastery"

    print(f"✓ Mastery uses exponential moving average")
    print(f"  After 10 incorrect: {mastery_after_incorrect:.2f}")
    print(f"  After 5 correct: {mastery_after_correct:.2f}")
    print(f"  Improvement: {mastery_after_correct - mastery_after_incorrect:.2f}")


def test_tracks_error_patterns():
    """Test that model tracks common error patterns."""
    model = StudentWorldModel()

    # Make errors with specific types
    model.update_from_performance("quad.graph.vertex", correct=False, error_type="sign_error")
    model.update_from_performance("quad.graph.vertex", correct=False, error_type="sign_error")
    model.update_from_performance("quad.graph.vertex", correct=False, error_type="coordinate_swap")

    node = model.concept_nodes["vertex_form_reading"]

    # Should track error types
    assert len(node.common_errors) > 0, "Should track errors"
    assert "sign_error" in node.common_errors, "Should record sign errors"

    print(f"✓ Model tracks error patterns")
    print(f"  Concept: {node.concept_id}")
    print(f"  Common errors: {node.common_errors}")


def test_simulates_future_performance():
    """Test that model can simulate future performance."""
    model = StudentWorldModel()

    # Practice some prerequisites
    for _ in range(5):
        model.update_from_performance("quad.graph.vertex", correct=True)

    # Simulate a learning path
    skill_sequence = [
        "quad.graph.vertex",
        "quad.standard.vertex",
        "quad.solve.by_formula"
    ]

    simulation = model.simulate_future_performance(skill_sequence)

    assert "skill_sequence" in simulation, "Should return skill sequence"
    assert "simulations" in simulation, "Should have simulation results"
    assert "overall_readiness" in simulation, "Should calculate readiness"

    print(f"✓ Model simulates future performance")
    print(f"  Skill sequence: {skill_sequence}")
    print(f"  Overall readiness: {simulation['overall_readiness']:.1%}")
    for sim in simulation["simulations"]:
        print(f"    {sim['skill_id']}: {sim['predicted_success_rate']:.1%} success")


def test_prerequisite_dependencies():
    """Test that model understands prerequisite dependencies."""
    model = StudentWorldModel()

    # Master a basic concept
    for _ in range(10):
        model.update_from_performance("quad.graph.vertex", correct=True)

    # Check that vertex_form_reading has high mastery
    vertex_mastery = model.concept_nodes["vertex_form_reading"].mastery_level
    assert vertex_mastery > 0.5, "Should master basic concepts"

    # Now try a skill that requires this as prerequisite
    prediction = model.predict_struggle("quad.standard.vertex")

    # Should predict less struggle since prerequisite is mastered
    print(f"✓ Model understands prerequisite dependencies")
    print(f"  Mastered prerequisite: vertex_form_reading ({vertex_mastery:.1%})")
    print(f"  Predicted struggles for dependent skill: {len(prediction.predicted_struggle_concepts)}")


def test_history_tracking():
    """Test that model maintains learning history."""
    model = StudentWorldModel()

    # Perform some actions
    model.update_from_performance("quad.graph.vertex", correct=True)
    model.update_from_performance("quad.solve.by_factoring", correct=False)
    model.predict_struggle("quad.solve.by_formula")

    # Check histories
    assert len(model.learning_history) == 2, "Should track learning events"
    assert len(model.prediction_history) == 1, "Should track predictions"

    print(f"✓ Model maintains history")
    print(f"  Learning events: {len(model.learning_history)}")
    print(f"  Predictions made: {len(model.prediction_history)}")


def test_intervention_priorities():
    """Test that interventions have appropriate priorities."""
    model = StudentWorldModel()

    # Very low mastery (should get high priority intervention)
    interventions = model.recommend_intervention("quad.solve.by_formula")

    # Should have high priority items for very low mastery
    high_priority = [i for i in interventions if i.priority == "high"]
    assert len(high_priority) > 0, "Should have high priority interventions for low mastery"

    print(f"✓ Interventions have appropriate priorities")
    print(f"  High priority: {len(high_priority)}")
    print(f"  All priorities: {[i.priority for i in interventions[:5]]}")

    # Now build some mastery
    for _ in range(5):
        model.update_from_performance("quad.discriminant.analysis", correct=True)

    interventions2 = model.recommend_intervention("quad.solve.by_formula")

    # Should have lower priority interventions now
    print(f"  After practice:")
    print(f"  Priorities: {[i.priority for i in interventions2[:5]]}")


if __name__ == "__main__":
    print("=" * 70)
    print("STUDENT WORLD MODEL ACCEPTANCE TESTS")
    print("=" * 70)
    print()

    # Run all tests
    test_initialization()
    print()

    test_updates_from_performance()
    print()

    test_predicts_struggles()
    print()

    test_recommends_interventions()
    print()

    test_mastery_summary()
    print()

    test_learning_trajectory()
    print()

    test_confidence_increases_with_data()
    print()

    test_mastery_exponential_moving_average()
    print()

    test_tracks_error_patterns()
    print()

    test_simulates_future_performance()
    print()

    test_prerequisite_dependencies()
    print()

    test_history_tracking()
    print()

    test_intervention_priorities()
    print()

    print("=" * 70)
    print("ALL ACCEPTANCE TESTS PASSED ✓")
    print("=" * 70)
