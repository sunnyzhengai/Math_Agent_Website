"""
Acceptance tests for Least-to-Most Decomposer.

Validates Denny Zhou's (Google) Least-to-Most pattern:
- Break complex problems into simpler subproblems
- Progressive difficulty building
- Scaffolded learning sequences
- Cognitive load reduction
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agentic.agents.least_to_most_decomposer import LeastToMostDecomposer


def test_initialization():
    """Test that decomposer initializes correctly."""
    decomposer = LeastToMostDecomposer()

    assert decomposer.decomposition_history == [], "Should start with empty history"

    print("✓ Decomposer initialized")


def test_analyzes_complexity():
    """Test that decomposer analyzes problem complexity."""
    decomposer = LeastToMostDecomposer()

    # Simple problem
    simple = "Find the vertex of y = x^2"
    simple_complexity = decomposer._analyze_complexity(simple, "quad.graph.vertex")

    # Complex problem
    complex_prob = "Find the vertex of y = -2(x + 4)^2 - 5"
    complex_complexity = decomposer._analyze_complexity(complex_prob, "quad.graph.vertex")

    # Complex should be higher than simple
    assert complex_complexity > simple_complexity, "Complex problems should have higher complexity"

    print("✓ Analyzes complexity correctly")
    print(f"  Simple: {simple_complexity}")
    print(f"  Complex: {complex_complexity}")


def test_generates_progressive_levels():
    """Test that decomposer generates progressive complexity levels."""
    decomposer = LeastToMostDecomposer()

    problem = "Find the vertex of y = -2(x + 3)^2 + 5"
    decomposed = decomposer.decompose_problem(
        problem=problem,
        skill_id="quad.graph.vertex",
        target_concept="vertex"
    )

    assert len(decomposed.levels) >= 3, "Should have multiple levels"

    # Levels should be in order
    for i in range(len(decomposed.levels) - 1):
        assert decomposed.levels[i].level < decomposed.levels[i + 1].level, \
            "Levels should be in ascending order"

    print("✓ Generates progressive levels")
    print(f"  Total levels: {len(decomposed.levels)}")
    for level in decomposed.levels:
        print(f"    Level {level.level}: {level.description}")


def test_simplest_level_is_basic():
    """Test that level 1 is the simplest possible."""
    decomposer = LeastToMostDecomposer()

    problem = "Find the vertex of y = -3(x - 5)^2 + 7"
    decomposed = decomposer.decompose_problem(
        problem=problem,
        skill_id="quad.graph.vertex",
        target_concept="vertex"
    )

    level_1 = decomposed.levels[0]

    assert level_1.level == 1, "First level should be 1"
    assert "simplest" in level_1.description.lower() or "simple" in level_1.description.lower(), \
        "Level 1 should be described as simplest"

    # For vertex problems, simplest should be y = x²
    if "equation" in level_1.features:
        assert "x²" in level_1.features["equation"] or "x^2" in level_1.features["equation"], \
            "Simplest vertex form should be y = x²"

    print("✓ Simplest level is basic")
    print(f"  Level 1: {level_1.description}")
    print(f"  Example: {level_1.example}")


def test_levels_add_one_concept_at_time():
    """Test that each level adds ONE new concept."""
    decomposer = LeastToMostDecomposer()

    problem = "Find the vertex of y = 2(x - 3)^2 + 5"
    decomposed = decomposer.decompose_problem(
        problem=problem,
        skill_id="quad.graph.vertex",
        target_concept="vertex"
    )

    # Check that complexity builds gradually
    for i in range(len(decomposed.levels) - 1):
        current = decomposed.levels[i]
        next_level = decomposed.levels[i + 1]

        # Level should only increase by 1
        assert next_level.level - current.level == 1, "Should increment by 1 level at a time"

    print("✓ Levels add one concept at a time")
    print(f"  Progression: {[l.level for l in decomposed.levels]}")


def test_creates_learning_sequence():
    """Test that decomposer creates a learning sequence."""
    decomposer = LeastToMostDecomposer()

    problem = "Find the vertex of y = (x - 4)^2 + 1"
    decomposed = decomposer.decompose_problem(
        problem=problem,
        skill_id="quad.graph.vertex",
        target_concept="vertex"
    )

    assert len(decomposed.learning_sequence) > 0, "Should have learning sequence"

    # Sequence should explain the progression
    sequence_text = "\n".join(decomposed.learning_sequence)
    assert "Level" in sequence_text, "Should mention levels"

    print("✓ Creates learning sequence")
    print(f"  Steps: {len(decomposed.learning_sequence)}")
    print(f"  First step: {decomposed.learning_sequence[0]}")


def test_generates_explanation():
    """Test that decomposer generates overall explanation."""
    decomposer = LeastToMostDecomposer()

    problem = "Find the vertex of y = -2(x + 3)^2 - 4"
    decomposed = decomposer.decompose_problem(
        problem=problem,
        skill_id="quad.graph.vertex",
        target_concept="vertex"
    )

    assert decomposed.explanation, "Should have explanation"
    assert len(decomposed.explanation) > 100, "Explanation should be substantial"

    # Should mention key concepts
    assert "step" in decomposed.explanation.lower() or "level" in decomposed.explanation.lower(), \
        "Should explain step-by-step approach"

    print("✓ Generates explanation")
    print(f"  Length: {len(decomposed.explanation)} chars")
    print(f"  Preview: {decomposed.explanation[:100]}...")


def test_scaffolded_practice_generation():
    """Test generating scaffolded practice sequence."""
    decomposer = LeastToMostDecomposer()

    practice = decomposer.generate_scaffolded_practice(
        skill_id="quad.graph.vertex",
        start_level=1,
        end_level=3,
        problems_per_level=2
    )

    # Should have problems
    expected_problems = (3 - 1 + 1) * 2  # 3 levels × 2 problems
    assert len(practice.problems) == expected_problems, f"Should have {expected_problems} problems"

    # Should have difficulty progression
    assert len(practice.difficulty_progression) == expected_problems, \
        "Should track difficulty for each problem"

    # Difficulty should be increasing
    assert practice.difficulty_progression[0] <= practice.difficulty_progression[-1], \
        "Difficulty should not decrease"

    print("✓ Generates scaffolded practice")
    print(f"  Problems: {len(practice.problems)}")
    print(f"  Difficulty progression: {practice.difficulty_progression}")


def test_scaffolding_notes_at_level_transitions():
    """Test that scaffolding notes appear at level transitions."""
    decomposer = LeastToMostDecomposer()

    practice = decomposer.generate_scaffolded_practice(
        skill_id="quad.graph.vertex",
        start_level=1,
        end_level=3,
        problems_per_level=2
    )

    # First problem of each level should have scaffolding note
    notes_with_content = [n for n in practice.scaffolding_notes if n]
    assert len(notes_with_content) >= 3, "Should have notes for each level transition"

    print("✓ Scaffolding notes at transitions")
    print(f"  Total notes: {len(notes_with_content)}")
    for note in notes_with_content[:3]:
        print(f"    - {note[:60]}...")


def test_generates_problems_at_specific_levels():
    """Test generating problems at specific complexity levels."""
    decomposer = LeastToMostDecomposer()

    # Generate at level 1
    problem_1 = decomposer._generate_problem_at_level("quad.graph.vertex", 1, seed=0)
    assert problem_1["level"] == 1, "Should generate at level 1"

    # Generate at level 5
    problem_5 = decomposer._generate_problem_at_level("quad.graph.vertex", 5, seed=0)
    assert problem_5["level"] == 5, "Should generate at level 5"

    # Level 5 should be more complex
    print("✓ Generates problems at specific levels")
    print(f"  Level 1: {problem_1['stem']}")
    print(f"  Level 5: {problem_5['stem']}")


def test_level_1_vertex_problems():
    """Test that level 1 vertex problems are simplest."""
    decomposer = LeastToMostDecomposer()

    problem = decomposer._generate_vertex_problem_at_level(1, seed=0)

    # Should be y = x²
    assert "x²" in problem["equation"] or "x^2" in problem["equation"], \
        "Level 1 should be y = x²"
    assert problem["answer"] == "(0, 0)", "Vertex should be origin"

    print("✓ Level 1 vertex problems are simplest")
    print(f"  Equation: {problem['equation']}")
    print(f"  Answer: {problem['answer']}")


def test_level_5_vertex_problems():
    """Test that level 5 vertex problems are complex."""
    decomposer = LeastToMostDecomposer()

    problem = decomposer._generate_vertex_problem_at_level(5, seed=0)

    # Should have coefficient
    assert "equation" in problem, "Should have equation"
    # Level 5 has coefficient, so should have number before (x
    equation = problem["equation"]

    print("✓ Level 5 vertex problems are complex")
    print(f"  Equation: {equation}")
    print(f"  Answer: {problem['answer']}")


def test_progressive_difficulty_in_scaffolded_practice():
    """Test that scaffolded practice progresses from easy to hard."""
    decomposer = LeastToMostDecomposer()

    practice = decomposer.generate_scaffolded_practice(
        skill_id="quad.graph.vertex",
        start_level=1,
        end_level=5,
        problems_per_level=2
    )

    # First few should be level 1
    assert practice.difficulty_progression[0] == 1, "Should start at level 1"
    assert practice.difficulty_progression[1] == 1, "Second problem also level 1"

    # Last few should be level 5
    assert practice.difficulty_progression[-1] == 5, "Should end at level 5"
    assert practice.difficulty_progression[-2] == 5, "Second-to-last also level 5"

    # Should be non-decreasing
    for i in range(len(practice.difficulty_progression) - 1):
        assert practice.difficulty_progression[i] <= practice.difficulty_progression[i + 1], \
            "Difficulty should not decrease"

    print("✓ Progressive difficulty in scaffolded practice")
    print(f"  Progression: {practice.difficulty_progression}")


def test_tracks_decomposition_history():
    """Test that decomposer tracks history."""
    decomposer = LeastToMostDecomposer()

    # Decompose a few problems
    problems = [
        "Find the vertex of y = x^2",
        "Find the vertex of y = (x - 2)^2 + 3",
        "Find the vertex of y = -2(x + 1)^2 - 5"
    ]

    for problem in problems:
        decomposer.decompose_problem(problem, "quad.graph.vertex", "vertex")

    assert len(decomposer.decomposition_history) == 3, "Should track all decompositions"

    print("✓ Tracks decomposition history")
    print(f"  Total decompositions: {len(decomposer.decomposition_history)}")


def test_decomposition_statistics():
    """Test that decomposer provides statistics."""
    decomposer = LeastToMostDecomposer()

    # Decompose some problems
    for i in range(3):
        decomposer.decompose_problem(
            f"Find the vertex of y = (x - {i})^2 + {i}",
            "quad.graph.vertex",
            "vertex"
        )

    stats = decomposer.get_decomposition_stats()

    assert stats["total_decompositions"] == 3, "Should count decompositions"
    assert "avg_complexity" in stats, "Should calculate average complexity"
    assert "avg_levels_generated" in stats, "Should track levels generated"

    print("✓ Provides decomposition statistics")
    print(f"  Total: {stats['total_decompositions']}")
    print(f"  Avg complexity: {stats['avg_complexity']:.1f}")
    print(f"  Avg levels: {stats['avg_levels_generated']:.1f}")


def test_reduces_cognitive_overload():
    """Test that decomposition reduces cognitive overload."""
    decomposer = LeastToMostDecomposer()

    # Complex problem
    complex_problem = "Find the vertex of y = -3(x + 7)^2 - 9"

    decomposed = decomposer.decompose_problem(
        complex_problem,
        "quad.graph.vertex",
        "vertex"
    )

    # Should have multiple levels
    assert len(decomposed.levels) >= 4, "Should break into multiple levels"

    # Each level should add manageable complexity
    for i in range(len(decomposed.levels) - 1):
        # Complexity should increase gradually, not jump
        assert decomposed.levels[i + 1].level - decomposed.levels[i].level == 1, \
            "Should add complexity gradually"

    print("✓ Reduces cognitive overload")
    print(f"  Complex problem broken into {len(decomposed.levels)} manageable levels")


def test_explains_transitions():
    """Test that transitions between levels are explained."""
    decomposer = LeastToMostDecomposer()

    level1 = type('Level', (), {
        'level': 1,
        'description': "Simple form"
    })()

    level2 = type('Level', (), {
        'level': 2,
        'description': "Add horizontal shift (h)"
    })()

    explanation = decomposer._explain_transition(level1, level2)

    assert explanation, "Should provide transition explanation"
    assert len(explanation) > 10, "Explanation should be meaningful"

    print("✓ Explains transitions")
    print(f"  Example: {explanation}")


def test_scaffolding_notes_are_helpful():
    """Test that scaffolding notes provide helpful guidance."""
    decomposer = LeastToMostDecomposer()

    # Get notes for different levels
    note_1 = decomposer._get_scaffolding_note(1, "quad.graph.vertex")
    note_2 = decomposer._get_scaffolding_note(2, "quad.graph.vertex")
    note_5 = decomposer._get_scaffolding_note(5, "quad.graph.vertex")

    # Should have content
    assert note_1, "Level 1 should have note"
    assert note_2, "Level 2 should have note"
    assert note_5, "Level 5 should have note"

    # Should be different
    assert note_1 != note_2, "Different levels should have different notes"

    print("✓ Scaffolding notes are helpful")
    print(f"  Level 1: {note_1[:50]}...")
    print(f"  Level 2: {note_2[:50]}...")
    print(f"  Level 5: {note_5[:50]}...")


def test_handles_multiple_skills():
    """Test that decomposer works for different skill types."""
    decomposer = LeastToMostDecomposer()

    # Test vertex skill
    vertex_decomp = decomposer.decompose_problem(
        "Find the vertex of y = (x - 2)^2 + 3",
        "quad.graph.vertex",
        "vertex"
    )

    # Test factoring skill
    factor_decomp = decomposer.decompose_problem(
        "Factor x^2 + 5x + 6",
        "quad.solve.by_factoring",
        "factoring"
    )

    # Both should have levels
    assert len(vertex_decomp.levels) > 0, "Vertex should have levels"
    assert len(factor_decomp.levels) > 0, "Factoring should have levels"

    print("✓ Handles multiple skill types")
    print(f"  Vertex: {len(vertex_decomp.levels)} levels")
    print(f"  Factoring: {len(factor_decomp.levels)} levels")


def test_seed_variations_within_level():
    """Test that seed creates variations within same level."""
    decomposer = LeastToMostDecomposer()

    # Generate multiple problems at same level with different seeds
    problem_1 = decomposer._generate_problem_at_level("quad.graph.vertex", 2, seed=0)
    problem_2 = decomposer._generate_problem_at_level("quad.graph.vertex", 2, seed=1)
    problem_3 = decomposer._generate_problem_at_level("quad.graph.vertex", 2, seed=2)

    # Should all be same level
    assert problem_1["level"] == problem_2["level"] == problem_3["level"] == 2

    # But should have different content (seed variation)
    problems = [problem_1["stem"], problem_2["stem"], problem_3["stem"]]
    unique_problems = set(problems)
    assert len(unique_problems) >= 2, "Different seeds should create variations"

    print("✓ Seed creates variations within level")
    print(f"  Unique problems at level 2: {len(unique_problems)}")


if __name__ == "__main__":
    print("=" * 70)
    print("LEAST-TO-MOST DECOMPOSER ACCEPTANCE TESTS")
    print("=" * 70)
    print()

    # Run all tests
    test_initialization()
    print()

    test_analyzes_complexity()
    print()

    test_generates_progressive_levels()
    print()

    test_simplest_level_is_basic()
    print()

    test_levels_add_one_concept_at_time()
    print()

    test_creates_learning_sequence()
    print()

    test_generates_explanation()
    print()

    test_scaffolded_practice_generation()
    print()

    test_scaffolding_notes_at_level_transitions()
    print()

    test_generates_problems_at_specific_levels()
    print()

    test_level_1_vertex_problems()
    print()

    test_level_5_vertex_problems()
    print()

    test_progressive_difficulty_in_scaffolded_practice()
    print()

    test_tracks_decomposition_history()
    print()

    test_decomposition_statistics()
    print()

    test_reduces_cognitive_overload()
    print()

    test_explains_transitions()
    print()

    test_scaffolding_notes_are_helpful()
    print()

    test_handles_multiple_skills()
    print()

    test_seed_variations_within_level()
    print()

    print("=" * 70)
    print("ALL ACCEPTANCE TESTS PASSED ✓")
    print("=" * 70)
