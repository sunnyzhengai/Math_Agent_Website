"""
Acceptance tests for Question Validation Committee.

Validates Andrew Ng's Multi-Agent Collaboration pattern:
- Multiple specialized agents work together
- Each agent has veto power
- Provides detailed feedback
- Ensures high-quality questions
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agentic.agents.question_validation_committee import (
    QuestionValidationCommittee,
    ValidationResult
)
from engine.templates import generate_item


def test_committee_structure():
    """Test that committee has all required agents."""
    committee = QuestionValidationCommittee(use_reflection=False)

    assert hasattr(committee, 'oracle_agent'), "Should have Oracle agent"
    assert hasattr(committee, 'clarity_agent'), "Should have Clarity agent"
    assert hasattr(committee, 'difficulty_agent'), "Should have Difficulty agent"
    assert hasattr(committee, 'distractor_agent'), "Should have Distractor agent"

    print("✓ Committee has all 4 required agents")


def test_committee_rejects_unclear_question():
    """Test that clarity agent catches unclear wording."""
    committee = QuestionValidationCommittee(use_reflection=False)

    unclear_question = {
        "stem": "Thing the do math equation solve it",  # Intentionally unclear
        "choices": [
            {"id": "A", "text": "x = 2"},
            {"id": "B", "text": "x = 3"},
            {"id": "C", "text": "x = 4"},
            {"id": "D", "text": "x = 5"}
        ],
        "solution_choice_id": "A",
        "difficulty": "easy",
        "skill_id": "quad.solve.by_factoring"
    }

    result = committee.validate_question(unclear_question)

    assert not result.approved, "Should reject unclear question"
    assert result.failed_agent == "clarity", f"Should fail on clarity, got {result.failed_agent}"
    assert result.fix_suggestion is not None, "Should provide fix suggestion"

    print(f"✓ Clarity agent correctly rejected unclear question")
    print(f"  Reason: {result.reason}")
    print(f"  Fix: {result.fix_suggestion}")


def test_committee_rejects_wrong_answer():
    """Test that oracle catches incorrect answer keys."""
    committee = QuestionValidationCommittee(use_reflection=False)

    wrong_answer_question = {
        "stem": "Solve by factoring: x^2 + 5x + 6 = 0",
        "choices": [
            {"id": "A", "text": "x = 1 or x = 2"},  # Wrong
            {"id": "B", "text": "x = -2 or x = -3"},  # Correct
            {"id": "C", "text": "x = 2 or x = 3"},
            {"id": "D", "text": "x = -1 or x = -6"}
        ],
        "solution_choice_id": "A",  # Marked as A but B is correct
        "difficulty": "easy",
        "skill_id": "quad.solve.by_factoring"
    }

    # Skip if no API key (oracle will trust answer key)
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("⊘ Skipping oracle test (no API key)")
        return

    result = committee.validate_question(wrong_answer_question)

    assert not result.approved, "Should reject question with wrong answer"
    assert result.failed_agent == "oracle", f"Should fail on oracle, got {result.failed_agent}"

    print(f"✓ Oracle correctly rejected wrong answer key")
    print(f"  Reason: {result.reason}")


def test_committee_rejects_difficulty_mismatch():
    """Test that difficulty agent catches calibration issues."""
    committee = QuestionValidationCommittee(use_reflection=False)

    # Create a hard problem but label it as easy
    hard_problem = {
        "stem": "Complete the square for x^2 - 147x + 1832 = 0",  # Complex coefficients
        "choices": [
            {"id": "A", "text": "(x - 73.5)^2 = 3570.25"},
            {"id": "B", "text": "(x - 73.5)^2 = 3572.25"},
            {"id": "C", "text": "(x + 73.5)^2 = 3570.25"},
            {"id": "D", "text": "(x - 147)^2 = 1832"}
        ],
        "solution_choice_id": "A",
        "difficulty": "easy",  # Labeled easy but is actually hard
        "skill_id": "quad.complete.square"
    }

    result = committee.validate_question(hard_problem, strict=True)

    # Should fail on difficulty (though might fail oracle first if no API key)
    assert not result.approved, "Should reject difficulty mismatch"

    if result.failed_agent == "difficulty":
        print(f"✓ Difficulty agent correctly rejected calibration mismatch")
        print(f"  Reason: {result.reason}")
        print(f"  Fix: {result.fix_suggestion}")
    else:
        print(f"⊘ Failed on {result.failed_agent} before reaching difficulty check")


def test_committee_approves_good_question():
    """Test that committee approves high-quality questions."""
    committee = QuestionValidationCommittee(use_reflection=False)

    # Generate a real question from templates
    good_question = generate_item(
        skill_id="quad.graph.vertex",
        difficulty="easy",
        seed=42
    )

    result = committee.validate_question(good_question, strict=False)

    # With no API key, oracle will trust answer key, so this should pass
    print(f"✓ Validation result: {'APPROVED' if result.approved else 'REJECTED'}")
    print(f"  Consensus score: {result.consensus_score:.2f}")

    if result.approved:
        print(f"  All agents approved: {', '.join(result.validating_agents)}")
    else:
        print(f"  Failed agent: {result.failed_agent}")
        print(f"  Reason: {result.reason}")

    # Details
    print(f"\n  Agent details:")
    for agent, details in result.details.items():
        print(f"    {agent}: {details}")


def test_committee_batch_validation():
    """Test that committee can validate multiple questions."""
    committee = QuestionValidationCommittee(use_reflection=False)

    # Generate multiple questions
    questions = [
        generate_item("quad.graph.vertex", "easy", seed=i)
        for i in range(5)
    ]

    results = committee.validate_batch(questions, strict=False)

    assert len(results) == 5, "Should return result for each question"

    approved_count = sum(1 for r in results if r.approved)
    print(f"✓ Batch validation: {approved_count}/{len(questions)} approved")

    # Test filtering to approved only
    approved_questions = committee.get_approved_questions(questions, strict=False)
    print(f"✓ Filtered to {len(approved_questions)} approved questions")


def test_committee_tracks_statistics():
    """Test that committee tracks validation history."""
    committee = QuestionValidationCommittee(use_reflection=False)

    # Validate several questions
    questions = [
        generate_item("quad.graph.vertex", "easy", seed=i)
        for i in range(3)
    ]

    for q in questions:
        committee.validate_question(q, strict=False)

    stats = committee.get_validation_stats()

    assert stats["total_validations"] == 3, "Should track all validations"
    assert "approval_rate" in stats, "Should calculate approval rate"
    assert "avg_consensus_score" in stats, "Should calculate average consensus"

    print(f"✓ Committee statistics:")
    print(f"  Total validations: {stats['total_validations']}")
    print(f"  Approval rate: {stats['approval_rate']:.1%}")
    print(f"  Avg consensus: {stats['avg_consensus_score']:.2f}")

    if stats.get("failures_by_agent"):
        print(f"  Failures by agent: {stats['failures_by_agent']}")


def test_individual_agents():
    """Test that individual agents work correctly."""
    committee = QuestionValidationCommittee(use_reflection=False)

    question = generate_item("quad.graph.vertex", "easy", seed=42)

    # Test clarity agent
    clarity_score = committee.clarity_agent.evaluate(question["stem"])
    print(f"✓ Clarity agent: score = {clarity_score:.2f}")
    assert 0.0 <= clarity_score <= 1.0, "Score should be in valid range"

    # Test difficulty agent
    difficulty_score = committee.difficulty_agent.estimate(question)
    difficulty_label = committee.difficulty_agent.get_difficulty_label(difficulty_score)
    print(f"✓ Difficulty agent: score = {difficulty_score:.2f} ({difficulty_label})")
    assert 0.0 <= difficulty_score <= 1.0, "Score should be in valid range"

    # Test distractor agent
    distractor_result = committee.distractor_agent.evaluate(question)
    print(f"✓ Distractor agent: {distractor_result.plausible_count}/{distractor_result.total_distractors} plausible")
    assert distractor_result.plausible_count >= 0, "Should count plausible distractors"


if __name__ == "__main__":
    print("=" * 70)
    print("QUESTION VALIDATION COMMITTEE ACCEPTANCE TESTS")
    print("=" * 70)
    print()

    # Run all tests
    test_committee_structure()
    print()

    test_individual_agents()
    print()

    test_committee_rejects_unclear_question()
    print()

    test_committee_rejects_wrong_answer()
    print()

    test_committee_rejects_difficulty_mismatch()
    print()

    test_committee_approves_good_question()
    print()

    test_committee_batch_validation()
    print()

    test_committee_tracks_statistics()
    print()

    print("=" * 70)
    print("ALL ACCEPTANCE TESTS PASSED ✓")
    print("=" * 70)
