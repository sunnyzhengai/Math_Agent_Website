"""
Acceptance tests for ReAct Explanation Generator.

Validates Shunyu Yao's ReAct pattern:
- Thought-Action-Observation cycles
- Transparent reasoning visible to students
- Step-by-step diagnostic process
- Error classification and correction strategies
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agentic.agents.react_explanation_generator import ReActExplanationGenerator
from engine.templates import generate_item


def test_initialization():
    """Test that ReAct generator initializes correctly."""
    generator = ReActExplanationGenerator()

    assert generator.explanation_count == 0, "Should start with 0 explanations"
    assert generator.reasoning_trace_history == [], "Should start with empty history"

    print("✓ ReAct generator initialized")


def test_generates_with_reasoning_steps():
    """Test that explanations include reasoning steps."""
    generator = ReActExplanationGenerator()

    # Create a simple question
    question = {
        "stem": "Find the vertex of y = (x - 3)^2 + 2",
        "choices": [
            {"id": "A", "text": "(3, 2)"},
            {"id": "B", "text": "(-3, 2)"},
            {"id": "C", "text": "(3, -2)"},
            {"id": "D", "text": "(2, 3)"}
        ],
        "solution_choice_id": "A",
        "skill_id": "quad.graph.vertex"
    }

    # Student chose wrong answer
    explanation = generator.generate_explanation_with_react(
        question=question,
        student_answer="B",  # Wrong (sign error)
        correct_answer="A"
    )

    # Should have reasoning steps
    assert len(explanation.reasoning_steps) > 0, "Should have reasoning steps"
    assert len(explanation.reasoning_steps) >= 4, "Should have at least 4 cycles"

    # Each step should have thought, action, observation
    for step in explanation.reasoning_steps:
        assert step.thought, "Should have thought"
        assert step.action, "Should have action"
        assert step.observation, "Should have observation"

    print("✓ Generates with reasoning steps")
    print(f"  Steps: {len(explanation.reasoning_steps)}")
    print(f"  First thought: {explanation.reasoning_steps[0].thought[:60]}...")


def test_thought_action_observation_structure():
    """Test that each step follows Thought-Action-Observation pattern."""
    generator = ReActExplanationGenerator()

    question = {
        "stem": "Find the vertex of y = (x + 4)^2 + 3",
        "choices": [
            {"id": "A", "text": "(-4, 3)"},
            {"id": "B", "text": "(4, 3)"},
            {"id": "C", "text": "(-4, -3)"},
            {"id": "D", "text": "(3, -4)"}
        ],
        "solution_choice_id": "A",
        "skill_id": "quad.graph.vertex"
    }

    explanation = generator.generate_explanation_with_react(
        question=question,
        student_answer="B",
        correct_answer="A"
    )

    step1 = explanation.reasoning_steps[0]

    # Thought should indicate reasoning
    assert ("chose" in step1.thought.lower() or "selected" in step1.thought.lower()), \
        "Thought should mention student's choice"

    # Action should describe what to do
    assert ("compare" in step1.action.lower() or "analyze" in step1.action.lower()), \
        "Action should describe comparison/analysis"

    # Observation should state result
    assert ("selected" in step1.observation.lower() or "instead" in step1.observation.lower()), \
        "Observation should state what was observed"

    print("✓ Follows Thought-Action-Observation structure")
    print(f"  Thought: {step1.thought[:50]}...")
    print(f"  Action: {step1.action[:50]}...")
    print(f"  Observation: {step1.observation[:50]}...")


def test_diagnoses_sign_error():
    """Test that system diagnoses sign errors correctly."""
    generator = ReActExplanationGenerator()

    question = {
        "stem": "Find the vertex of y = (x - 5)^2 + 1",
        "choices": [
            {"id": "A", "text": "(5, 1)"},
            {"id": "B", "text": "(-5, 1)"},  # Sign error
            {"id": "C", "text": "(5, -1)"},
            {"id": "D", "text": "(1, 5)"}
        ],
        "solution_choice_id": "A",
        "skill_id": "quad.graph.vertex"
    }

    explanation = generator.generate_explanation_with_react(
        question=question,
        student_answer="B",  # Sign error
        correct_answer="A"
    )

    assert explanation.error_type == "sign_error", "Should diagnose as sign error"

    # Diagnosis step should mention sign
    diagnosis_step = explanation.reasoning_steps[1]
    assert "SIGN ERROR" in diagnosis_step.observation or "sign" in diagnosis_step.observation.lower(), \
        "Should mention sign error in diagnosis"

    print("✓ Diagnoses sign errors")
    print(f"  Error type: {explanation.error_type}")
    print(f"  Diagnosis: {diagnosis_step.observation[:80]}...")


def test_diagnoses_coordinate_swap():
    """Test that system diagnoses coordinate swaps."""
    generator = ReActExplanationGenerator()

    question = {
        "stem": "Find the vertex of y = (x - 3)^2 + 5",
        "choices": [
            {"id": "A", "text": "(3, 5)"},
            {"id": "B", "text": "(5, 3)"},  # Swapped
            {"id": "C", "text": "(-3, 5)"},
            {"id": "D", "text": "(3, -5)"}
        ],
        "solution_choice_id": "A",
        "skill_id": "quad.graph.vertex"
    }

    explanation = generator.generate_explanation_with_react(
        question=question,
        student_answer="B",  # Coordinate swap
        correct_answer="A"
    )

    assert explanation.error_type == "coordinate_swap", "Should diagnose as coordinate swap"

    diagnosis_step = explanation.reasoning_steps[1]
    assert "COORDINATE SWAP" in diagnosis_step.observation or "swap" in diagnosis_step.observation.lower(), \
        "Should mention coordinate swap"

    print("✓ Diagnoses coordinate swaps")
    print(f"  Error type: {explanation.error_type}")
    print(f"  Diagnosis: {diagnosis_step.observation[:80]}...")


def test_provides_correction_strategy():
    """Test that system provides actionable correction strategies."""
    generator = ReActExplanationGenerator()

    question = {
        "stem": "Find the vertex of y = (x + 2)^2 + 8",
        "choices": [
            {"id": "A", "text": "(-2, 8)"},
            {"id": "B", "text": "(2, 8)"},
            {"id": "C", "text": "(-2, -8)"},
            {"id": "D", "text": "(8, -2)"}
        ],
        "solution_choice_id": "A",
        "skill_id": "quad.graph.vertex"
    }

    explanation = generator.generate_explanation_with_react(
        question=question,
        student_answer="B",
        correct_answer="A"
    )

    assert explanation.correction_strategy, "Should provide correction strategy"

    # Should have specific tips
    assert len(explanation.correction_strategy) > 50, "Strategy should be detailed"

    # For sign errors, should mention how to avoid them
    if explanation.error_type == "sign_error":
        assert ("OPPOSITE" in explanation.correction_strategy or
                "opposite" in explanation.correction_strategy), \
            "Sign error strategy should mention opposite signs"

    print("✓ Provides correction strategies")
    print(f"  Strategy length: {len(explanation.correction_strategy)} chars")
    print(f"  Strategy preview: {explanation.correction_strategy[:100]}...")


def test_explains_correct_approach():
    """Test that system explains the correct solution approach."""
    generator = ReActExplanationGenerator()

    question = {
        "stem": "Find the vertex of y = (x - 7)^2 + 4",
        "choices": [
            {"id": "A", "text": "(7, 4)"},
            {"id": "B", "text": "(-7, 4)"},
            {"id": "C", "text": "(7, -4)"},
            {"id": "D", "text": "(4, 7)"}
        ],
        "solution_choice_id": "A",
        "skill_id": "quad.graph.vertex"
    }

    explanation = generator.generate_explanation_with_react(
        question=question,
        student_answer="B",
        correct_answer="A"
    )

    # Step 3 should explain correct approach
    correct_approach_step = explanation.reasoning_steps[2]

    assert "vertex form" in correct_approach_step.observation.lower(), \
        "Should mention vertex form"
    assert "(7, 4)" in correct_approach_step.observation, \
        "Should state the correct answer"

    print("✓ Explains correct approach")
    print(f"  Explanation: {correct_approach_step.observation[:80]}...")


def test_formats_explanation_text():
    """Test that final explanation is well-formatted."""
    generator = ReActExplanationGenerator()

    question = {
        "stem": "Find the vertex of y = (x - 1)^2 - 3",
        "choices": [
            {"id": "A", "text": "(1, -3)"},
            {"id": "B", "text": "(-1, -3)"},
            {"id": "C", "text": "(1, 3)"},
            {"id": "D", "text": "(-3, 1)"}
        ],
        "solution_choice_id": "A",
        "skill_id": "quad.graph.vertex"
    }

    explanation = generator.generate_explanation_with_react(
        question=question,
        student_answer="B",
        correct_answer="A"
    )

    # Should have formatted text
    assert explanation.explanation_text, "Should have explanation text"
    assert len(explanation.explanation_text) > 100, "Should be substantial"

    # Should include section markers
    assert "Step" in explanation.explanation_text, "Should have step markers"
    assert ("Thought" in explanation.explanation_text or "💭" in explanation.explanation_text), \
        "Should mark thoughts"

    print("✓ Formats explanation text")
    print(f"  Length: {len(explanation.explanation_text)} chars")
    print(f"  Preview: {explanation.explanation_text[:100]}...")


def test_includes_key_insight():
    """Test that explanation includes key teaching point."""
    generator = ReActExplanationGenerator()

    question = {
        "stem": "Find the vertex of y = (x + 6)^2 - 2",
        "choices": [
            {"id": "A", "text": "(-6, -2)"},
            {"id": "B", "text": "(6, -2)"},
            {"id": "C", "text": "(-6, 2)"},
            {"id": "D", "text": "(-2, -6)"}
        ],
        "solution_choice_id": "A",
        "skill_id": "quad.graph.vertex"
    }

    explanation = generator.generate_explanation_with_react(
        question=question,
        student_answer="B",
        correct_answer="A"
    )

    assert explanation.key_insight, "Should have key insight"
    assert len(explanation.key_insight) > 20, "Key insight should be meaningful"

    # For vertex skills, should mention vertex form
    if "vertex" in question["skill_id"]:
        assert "vertex" in explanation.key_insight.lower(), "Should mention vertex"

    print("✓ Includes key insight")
    print(f"  Insight: {explanation.key_insight}")


def test_tracks_reasoning_history():
    """Test that system tracks reasoning traces."""
    generator = ReActExplanationGenerator()

    # Generate a few explanations
    question = {
        "stem": "Find the vertex of y = (x - 2)^2 + 5",
        "choices": [
            {"id": "A", "text": "(2, 5)"},
            {"id": "B", "text": "(-2, 5)"}
        ],
        "solution_choice_id": "A",
        "skill_id": "quad.graph.vertex"
    }

    for i in range(3):
        generator.generate_explanation_with_react(
            question=question,
            student_answer="B",
            correct_answer="A"
        )

    assert len(generator.reasoning_trace_history) == 3, "Should track all traces"
    assert generator.explanation_count == 3, "Should count explanations"

    print("✓ Tracks reasoning history")
    print(f"  Total traces: {len(generator.reasoning_trace_history)}")
    print(f"  Explanation count: {generator.explanation_count}")


def test_reasoning_statistics():
    """Test that system provides reasoning statistics."""
    generator = ReActExplanationGenerator()

    question1 = {
        "stem": "Find the vertex of y = (x - 3)^2 + 2",
        "choices": [
            {"id": "A", "text": "(3, 2)"},
            {"id": "B", "text": "(-3, 2)"}
        ],
        "solution_choice_id": "A",
        "skill_id": "quad.graph.vertex"
    }

    question2 = {
        "stem": "Find the vertex of y = (x + 1)^2 - 5",
        "choices": [
            {"id": "A", "text": "(-1, -5)"},
            {"id": "B", "text": "(-5, -1)"}
        ],
        "solution_choice_id": "A",
        "skill_id": "quad.graph.vertex"
    }

    # Generate explanations with different error types
    generator.generate_explanation_with_react(question1, "B", "A")  # Sign error
    generator.generate_explanation_with_react(question2, "B", "A")  # Coordinate swap

    stats = generator.get_reasoning_stats()

    assert stats["total_explanations"] == 2, "Should count explanations"
    assert "error_types_diagnosed" in stats, "Should track error types"
    assert "avg_steps_per_explanation" in stats, "Should calculate average steps"

    print("✓ Provides reasoning statistics")
    print(f"  Total explanations: {stats['total_explanations']}")
    print(f"  Avg steps: {stats['avg_steps_per_explanation']:.1f}")
    print(f"  Error types: {stats['error_types_diagnosed']}")


def test_transparent_reasoning_visible():
    """Test that reasoning is transparent and visible."""
    generator = ReActExplanationGenerator()

    question = {
        "stem": "Find the vertex of y = (x - 4)^2 + 1",
        "choices": [
            {"id": "A", "text": "(4, 1)"},
            {"id": "B", "text": "(-4, 1)"}
        ],
        "solution_choice_id": "A",
        "skill_id": "quad.graph.vertex"
    }

    explanation = generator.generate_explanation_with_react(
        question=question,
        student_answer="B",
        correct_answer="A"
    )

    # Check that reasoning is visible in explanation text
    for step in explanation.reasoning_steps:
        # At least one of thought/action/observation should be in text
        assert (step.thought in explanation.explanation_text or
                step.action in explanation.explanation_text or
                step.observation in explanation.explanation_text), \
            "Reasoning steps should be visible in explanation"

    print("✓ Reasoning is transparent and visible")
    print(f"  All {len(explanation.reasoning_steps)} steps are in explanation text")


def test_handles_multiple_skills():
    """Test that ReAct works for different skill types."""
    generator = ReActExplanationGenerator()

    # Test vertex skill
    vertex_question = {
        "stem": "Find the vertex of y = (x - 2)^2 + 3",
        "choices": [
            {"id": "A", "text": "(2, 3)"},
            {"id": "B", "text": "(-2, 3)"}
        ],
        "solution_choice_id": "A",
        "skill_id": "quad.graph.vertex"
    }

    vertex_explanation = generator.generate_explanation_with_react(
        vertex_question, "B", "A"
    )

    # Test standard to vertex skill
    standard_question = {
        "stem": "Convert y = x^2 + 4x + 5 to vertex form",
        "choices": [
            {"id": "A", "text": "y = (x + 2)^2 + 1"},
            {"id": "B", "text": "y = (x - 2)^2 + 1"}
        ],
        "solution_choice_id": "A",
        "skill_id": "quad.standard.vertex"
    }

    standard_explanation = generator.generate_explanation_with_react(
        standard_question, "B", "A"
    )

    # Both should have reasoning steps
    assert len(vertex_explanation.reasoning_steps) >= 4, "Vertex should have steps"
    assert len(standard_explanation.reasoning_steps) >= 4, "Standard should have steps"

    print("✓ Handles multiple skill types")
    print(f"  Vertex skill: {len(vertex_explanation.reasoning_steps)} steps")
    print(f"  Standard skill: {len(standard_explanation.reasoning_steps)} steps")


def test_four_reasoning_cycles():
    """Test that all 4 ReAct cycles are present."""
    generator = ReActExplanationGenerator()

    question = {
        "stem": "Find the vertex of y = (x + 5)^2 + 6",
        "choices": [
            {"id": "A", "text": "(-5, 6)"},
            {"id": "B", "text": "(5, 6)"}
        ],
        "solution_choice_id": "A",
        "skill_id": "quad.graph.vertex"
    }

    explanation = generator.generate_explanation_with_react(
        question=question,
        student_answer="B",
        correct_answer="A"
    )

    assert len(explanation.reasoning_steps) == 4, "Should have exactly 4 cycles"

    # Cycle 1: Understand
    assert "chose" in explanation.reasoning_steps[0].thought.lower()

    # Cycle 2: Diagnose
    assert "diagnose" in explanation.reasoning_steps[1].thought.lower() or \
           "analyze" in explanation.reasoning_steps[1].thought.lower()

    # Cycle 3: Explain correct
    assert "explain" in explanation.reasoning_steps[2].thought.lower() or \
           "correct" in explanation.reasoning_steps[2].thought.lower()

    # Cycle 4: Strategy
    assert "strategy" in explanation.reasoning_steps[3].thought.lower() or \
           "avoid" in explanation.reasoning_steps[3].thought.lower()

    print("✓ All 4 ReAct cycles present")
    print("  1. Understanding")
    print("  2. Diagnosing")
    print("  3. Explaining")
    print("  4. Strategy")


if __name__ == "__main__":
    print("=" * 70)
    print("REACT EXPLANATION GENERATOR ACCEPTANCE TESTS")
    print("=" * 70)
    print()

    # Run all tests
    test_initialization()
    print()

    test_generates_with_reasoning_steps()
    print()

    test_thought_action_observation_structure()
    print()

    test_diagnoses_sign_error()
    print()

    test_diagnoses_coordinate_swap()
    print()

    test_provides_correction_strategy()
    print()

    test_explains_correct_approach()
    print()

    test_formats_explanation_text()
    print()

    test_includes_key_insight()
    print()

    test_tracks_reasoning_history()
    print()

    test_reasoning_statistics()
    print()

    test_transparent_reasoning_visible()
    print()

    test_handles_multiple_skills()
    print()

    test_four_reasoning_cycles()
    print()

    print("=" * 70)
    print("ALL ACCEPTANCE TESTS PASSED ✓")
    print("=" * 70)
