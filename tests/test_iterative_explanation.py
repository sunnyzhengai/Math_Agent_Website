"""
Acceptance tests for Iterative Explanation Agent.

Validates Andrew Ng's Iterative Refinement pattern:
- Multiple refinement passes
- Clarity scoring and improvement
- Completeness checking
- Quality thresholds met
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agentic.agents.iterative_explanation_agent import IterativeExplanationAgent
from engine.templates import generate_item


def test_agent_initialization():
    """Test that agent initializes with correct thresholds."""
    agent = IterativeExplanationAgent()

    assert agent.target_clarity == 0.7, "Default clarity threshold should be 0.7"
    assert agent.target_completeness == 0.8, "Default completeness threshold should be 0.8"
    assert agent.max_iterations == 3, "Default max iterations should be 3"

    print("✓ Agent initializes with correct thresholds")


def test_explanation_generation():
    """Test that agent generates explanations with refinement."""
    agent = IterativeExplanationAgent()

    # Generate a question
    question = generate_item(
        skill_id="quad.graph.vertex",
        difficulty="easy",
        seed=42
    )

    # Get wrong answer for explanation
    wrong_choice = "A" if question["solution_choice_id"] != "A" else "B"

    # Generate explanation with refinement
    explanation, metrics = agent.generate_explanation(
        question,
        student_answer=wrong_choice,
        correct_answer=question["solution_choice_id"]
    )

    # Verify explanation was generated
    assert explanation, "Should generate explanation"
    assert len(explanation) > 50, "Explanation should be substantial"

    # Verify metrics tracked
    assert metrics.iterations >= 1, "Should track iterations"
    assert 0 <= metrics.initial_clarity <= 1, "Clarity score should be 0-1"
    assert 0 <= metrics.final_clarity <= 1, "Clarity score should be 0-1"
    assert isinstance(metrics.improvements_made, list), "Should track improvements"

    print(f"✓ Generated explanation with refinement")
    print(f"  Initial clarity: {metrics.initial_clarity:.2f}")
    print(f"  Final clarity: {metrics.final_clarity:.2f}")
    print(f"  Iterations: {metrics.iterations}")
    print(f"  Improvements: {', '.join(metrics.improvements_made)}")


def test_clarity_scoring():
    """Test that clarity scoring works correctly."""
    agent = IterativeExplanationAgent()

    # Test clear explanation (has structure, steps, numbers)
    clear_text = """**Step 1: Identify the formula**

The vertex form is y = a(x - h)² + k where (h, k) is the vertex.

**Step 2: Read the values**

From y = 2(x - 3)² + 5, we can see:
  • h = 3
  • k = 5

**Step 3: State the answer**

Therefore, the vertex is (3, 5)."""

    clarity_clear = agent._score_clarity(clear_text)
    assert clarity_clear >= 0.7, f"Clear text should score high, got {clarity_clear:.2f}"

    # Test unclear explanation (dense, no structure)
    unclear_text = "The answer is (3, 5) because that's what the formula says."

    clarity_unclear = agent._score_clarity(unclear_text)
    assert clarity_unclear < 0.7, f"Unclear text should score low, got {clarity_unclear:.2f}"

    print(f"✓ Clarity scoring works")
    print(f"  Clear text: {clarity_clear:.2f}")
    print(f"  Unclear text: {clarity_unclear:.2f}")


def test_completeness_checking():
    """Test that completeness checking identifies missing elements."""
    agent = IterativeExplanationAgent()

    # Test incomplete explanation (missing verification)
    incomplete = "The vertex is at (3, 5). That's the answer."

    result = agent._check_completeness(incomplete, "quad.graph.vertex")

    assert not result.is_complete or result.score < 0.8, "Should identify as incomplete"
    assert result.missing_elements, "Should identify missing elements"

    print(f"✓ Completeness checking works")
    print(f"  Score: {result.score:.2f}")
    print(f"  Missing: {', '.join(result.missing_elements)}")


def test_refinement_improves_quality():
    """Test that refinement actually improves explanation quality."""
    agent = IterativeExplanationAgent()

    # Generate multiple explanations
    questions = [
        generate_item("quad.graph.vertex", "easy", seed=i)
        for i in range(5)
    ]

    improved_count = 0

    for question in questions:
        wrong_choice = "A" if question["solution_choice_id"] != "A" else "B"

        explanation, metrics = agent.generate_explanation(
            question,
            student_answer=wrong_choice,
            correct_answer=question["solution_choice_id"]
        )

        # Check if quality improved or was already high
        if metrics.final_clarity >= metrics.initial_clarity:
            improved_count += 1

    improvement_rate = improved_count / len(questions)

    assert improvement_rate >= 0.8, f"Should improve/maintain quality in 80%+ cases, got {improvement_rate:.1%}"

    print(f"✓ Refinement improves quality")
    print(f"  Improved/maintained: {improvement_rate:.1%}")


def test_tracks_refinement_statistics():
    """Test that agent tracks refinement statistics."""
    agent = IterativeExplanationAgent()

    # Generate several explanations
    for i in range(3):
        question = generate_item("quad.graph.vertex", "easy", seed=i)
        wrong_choice = "A" if question["solution_choice_id"] != "A" else "B"

        agent.generate_explanation(
            question,
            student_answer=wrong_choice,
            correct_answer=question["solution_choice_id"]
        )

    stats = agent.get_refinement_stats()

    assert stats["total_generations"] == 3, "Should track all generations"
    assert stats["avg_iterations"] >= 1, "Should track iterations"
    assert "avg_clarity_improvement" in stats, "Should track clarity improvement"
    assert "improvement_types" in stats, "Should track improvement types"

    print(f"✓ Tracks refinement statistics")
    print(f"  Total generations: {stats['total_generations']}")
    print(f"  Avg iterations: {stats['avg_iterations']:.1f}")
    print(f"  Avg clarity improvement: {stats['avg_clarity_improvement']:+.2f}")
    print(f"  Improvement types: {stats['improvement_types']}")


def test_works_across_all_skills():
    """Test that refinement works for all skills."""
    agent = IterativeExplanationAgent()

    skills = [
        "quad.graph.vertex",
        "quad.standard.vertex",
        "quad.roots.factored",
        "quad.solve.by_factoring",
        "quad.solve.by_formula",
    ]

    for skill_id in skills:
        question = generate_item(skill_id, "easy", seed=42)
        wrong_choice = "A" if question["solution_choice_id"] != "A" else "B"

        explanation, metrics = agent.generate_explanation(
            question,
            student_answer=wrong_choice,
            correct_answer=question["solution_choice_id"]
        )

        assert explanation, f"Should generate explanation for {skill_id}"
        assert metrics.final_clarity >= 0, f"Should have clarity score for {skill_id}"

        print(f"✓ {skill_id}: clarity={metrics.final_clarity:.2f}, iterations={metrics.iterations}")


if __name__ == "__main__":
    print("=" * 70)
    print("ITERATIVE EXPLANATION AGENT ACCEPTANCE TESTS")
    print("=" * 70)
    print()

    # Run all tests
    test_agent_initialization()
    print()

    test_clarity_scoring()
    print()

    test_completeness_checking()
    print()

    test_explanation_generation()
    print()

    test_refinement_improves_quality()
    print()

    test_tracks_refinement_statistics()
    print()

    test_works_across_all_skills()
    print()

    print("=" * 70)
    print("ALL ACCEPTANCE TESTS PASSED ✓")
    print("=" * 70)
