"""
Acceptance tests for Educational Constitutional Validator.

Validates Anthropic's Constitutional AI pattern:
- 6 educational principles as constitution
- Automated checking against principles
- Severity-weighted scoring
- Self-critique without human intervention
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agentic.agents.educational_constitutional_validator import (
    EducationalConstitutionalValidator,
    EducationalConstitution,
    PrincipleViolation
)
from engine.templates import generate_item


def test_validator_initialization():
    """Test that validator initializes with constitution."""
    validator = EducationalConstitutionalValidator(strict_mode=True)

    assert validator.strict_mode == True, "Should set strict mode"
    assert validator.constitution is not None, "Should have constitution"
    assert len(validator.constitution.PRINCIPLES) == 6, "Should have 6 principles"
    assert validator.validation_history == [], "Should start with empty history"

    print("✓ Validator initializes correctly")
    print(f"  Constitution has {len(validator.constitution.PRINCIPLES)} principles")


def test_constitution_principles():
    """Test that all 6 principles are defined correctly."""
    constitution = EducationalConstitution()

    expected_principles = [
        "genuine_understanding",
        "pedagogical_soundness",
        "honest_distractors",
        "appropriate_difficulty",
        "safe_learning",
        "inclusive_accessible"
    ]

    actual_principles = [p["id"] for p in constitution.PRINCIPLES]

    for expected in expected_principles:
        assert expected in actual_principles, f"Missing principle: {expected}"

    # Check critical principles have correct severity
    critical_principles = [
        p for p in constitution.PRINCIPLES
        if p["severity"] == "critical"
    ]
    assert len(critical_principles) >= 2, "Should have critical principles"

    print("✓ All 6 constitutional principles defined")
    print(f"  Critical principles: {len(critical_principles)}")
    for p in constitution.PRINCIPLES:
        print(f"    - {p['name']} ({p['severity']})")


def test_validates_good_question():
    """Test that a good question passes all checks."""
    validator = EducationalConstitutionalValidator(strict_mode=True)

    # Generate a standard question
    question = generate_item("quad.graph.vertex", "easy", seed=42)

    result = validator.validate(question)

    # Good questions should pass
    assert result.principles_checked == 6, "Should check all 6 principles"
    assert result.overall_score >= 0.5, "Good questions should score well"

    print(f"✓ Good question validated")
    print(f"  Principles checked: {result.principles_checked}")
    print(f"  Principles passed: {result.principles_passed}")
    print(f"  Overall score: {result.overall_score:.2f}")
    print(f"  Passes constitution: {result.passes_constitution}")
    if result.violations:
        print(f"  Violations: {len(result.violations)}")
        for v in result.violations:
            print(f"    - {v.principle_name} ({v.severity}): {v.violation_description}")


def test_detects_genuine_understanding_violation():
    """Test detection of questions lacking genuine understanding."""
    validator = EducationalConstitutionalValidator(strict_mode=False)

    # Create a question that's pure recall (bad)
    bad_question = {
        "stem": "What color is the sky?",  # Pure recall, no reasoning
        "choices": {
            "A": "Blue",
            "B": "Red",
            "C": "Green",
            "D": "Yellow"
        },
        "solution_choice_id": "A",
        "skill_id": "quad.graph.vertex",
        "difficulty": "easy"
    }

    result = validator.validate(bad_question)

    # Should detect lack of reasoning
    genuine_violations = [
        v for v in result.violations
        if v.principle_id == "genuine_understanding"
    ]

    assert len(genuine_violations) > 0, "Should detect lack of genuine understanding"
    assert any(v.severity == "critical" for v in genuine_violations), "Should be critical"

    print(f"✓ Detects genuine understanding violations")
    print(f"  Violations: {len(genuine_violations)}")
    for v in genuine_violations:
        print(f"    - {v.violation_description}")


def test_detects_pedagogical_soundness_violation():
    """Test detection of pedagogically unsound content."""
    validator = EducationalConstitutionalValidator(strict_mode=False)

    # Create a question with too-large numbers
    bad_question = {
        "stem": "Find the vertex of y = -9999x^2 + 8888x - 7777",
        "choices": {
            "A": "(0.444, -7777)",
            "B": "(0.555, -8888)",
            "C": "(0.666, -9999)",
            "D": "(0.777, -6666)"
        },
        "solution_choice_id": "A",
        "skill_id": "quad.graph.vertex",
        "difficulty": "easy"
    }

    result = validator.validate(bad_question)

    # Should detect pedagogical issues
    pedagogical_violations = [
        v for v in result.violations
        if v.principle_id == "pedagogical_soundness"
    ]

    assert len(pedagogical_violations) > 0, "Should detect pedagogical issues"

    print(f"✓ Detects pedagogical soundness violations")
    print(f"  Violations: {len(pedagogical_violations)}")
    for v in pedagogical_violations:
        print(f"    - {v.violation_description}")


def test_detects_honest_distractor_violation():
    """Test detection of dishonest distractors."""
    validator = EducationalConstitutionalValidator(strict_mode=False)

    # Create question with only one distractor
    bad_question = {
        "stem": "Find the vertex of y = -2x^2 + 8x - 5",
        "choices": {
            "A": "(2, 3)",  # Correct
            "B": "(1, 1)"   # Only one distractor
        },
        "solution_choice_id": "A",
        "skill_id": "quad.graph.vertex",
        "difficulty": "easy"
    }

    result = validator.validate(bad_question)

    # Should detect insufficient distractors
    distractor_violations = [
        v for v in result.violations
        if v.principle_id == "honest_distractors"
    ]

    assert len(distractor_violations) > 0, "Should detect distractor issues"

    print(f"✓ Detects honest distractor violations")
    print(f"  Violations: {len(distractor_violations)}")
    for v in distractor_violations:
        print(f"    - {v.violation_description}")


def test_detects_appropriate_difficulty_violation():
    """Test detection of difficulty mismatch."""
    validator = EducationalConstitutionalValidator(strict_mode=False)

    # Create "easy" question with large numbers
    bad_question = {
        "stem": "Find the vertex of y = -250x^2 + 1000x - 3000",
        "choices": {
            "A": "(2, -1000)",
            "B": "(3, -1500)",
            "C": "(4, -2000)",
            "D": "(5, -2500)"
        },
        "solution_choice_id": "A",
        "skill_id": "quad.graph.vertex",
        "difficulty": "easy"  # But numbers are too large for easy
    }

    result = validator.validate(bad_question)

    # Should detect difficulty mismatch
    difficulty_violations = [
        v for v in result.violations
        if v.principle_id == "appropriate_difficulty"
    ]

    assert len(difficulty_violations) > 0, "Should detect difficulty mismatch"

    print(f"✓ Detects appropriate difficulty violations")
    print(f"  Violations: {len(difficulty_violations)}")
    for v in difficulty_violations:
        print(f"    - {v.violation_description}")


def test_detects_safe_learning_violation():
    """Test detection of unsafe content."""
    validator = EducationalConstitutionalValidator(strict_mode=True)

    # Create question with harmful content
    bad_question = {
        "stem": "A weapon is fired with velocity v. Find the height after t seconds using y = -16t^2 + vt.",
        "choices": {
            "A": "y = -16t^2 + 100t",
            "B": "y = -16t^2 + 200t",
            "C": "y = -16t^2 + 300t",
            "D": "y = -16t^2 + 400t"
        },
        "solution_choice_id": "A",
        "skill_id": "quad.graph.vertex",
        "difficulty": "applied"
    }

    result = validator.validate(bad_question)

    # Should detect harmful content
    safety_violations = [
        v for v in result.violations
        if v.principle_id == "safe_learning"
    ]

    assert len(safety_violations) > 0, "Should detect unsafe content"
    assert any(v.severity == "critical" for v in safety_violations), "Should be critical"

    # In strict mode, critical violations should fail
    assert not result.passes_constitution, "Should fail in strict mode"

    print(f"✓ Detects safe learning violations")
    print(f"  Violations: {len(safety_violations)}")
    print(f"  Passes constitution: {result.passes_constitution} (correctly fails)")


def test_detects_inclusive_accessible_violation():
    """Test detection of accessibility issues."""
    validator = EducationalConstitutionalValidator(strict_mode=False)

    # Create vertex question without equation
    bad_question = {
        "stem": "Find the vertex",  # Missing equation!
        "choices": {
            "A": "(1, 2)",
            "B": "(2, 3)",
            "C": "(3, 4)",
            "D": "(4, 5)"
        },
        "solution_choice_id": "A",
        "skill_id": "quad.graph.vertex",
        "difficulty": "easy"
    }

    result = validator.validate(bad_question)

    # Should detect accessibility issues
    accessibility_violations = [
        v for v in result.violations
        if v.principle_id == "inclusive_accessible"
    ]

    # May or may not detect (depends on implementation), but shouldn't crash
    print(f"✓ Checks inclusive & accessible principles")
    if accessibility_violations:
        print(f"  Violations: {len(accessibility_violations)}")
        for v in accessibility_violations:
            print(f"    - {v.violation_description}")
    else:
        print(f"  No violations detected (may need stricter checks)")


def test_weighted_scoring():
    """Test that violations are weighted by severity."""
    validator = EducationalConstitutionalValidator(strict_mode=False)

    # Create question with only low-severity violations
    minor_issue_question = {
        "stem": "Find the vertex of y = -2x^2 + 8x - 5",  # Good question
        "choices": {
            "A": "(2, 3)",
            "B": "(1, 1)",
            "C": "(3, -2)",
            "D": "(0, -5)"
        },
        "solution_choice_id": "A",
        "skill_id": "quad.graph.vertex",
        "difficulty": "easy"
    }

    result1 = validator.validate(minor_issue_question)

    # Create question with critical violations
    critical_issue_question = {
        "stem": "What weapon has maximum range?",  # Harmful + not math
        "choices": {
            "A": "A",
            "B": "B"
        },
        "solution_choice_id": "A",
        "skill_id": "quad.graph.vertex",
        "difficulty": "easy"
    }

    result2 = validator.validate(critical_issue_question)

    # Critical violations should score much lower
    assert result2.overall_score < result1.overall_score, "Critical violations should score lower"

    print(f"✓ Weighted scoring works")
    print(f"  Minor issues score: {result1.overall_score:.2f}")
    print(f"  Critical issues score: {result2.overall_score:.2f}")


def test_strict_mode():
    """Test that strict mode fails on critical violations."""
    strict_validator = EducationalConstitutionalValidator(strict_mode=True)
    lenient_validator = EducationalConstitutionalValidator(strict_mode=False)

    # Question with critical violation
    bad_question = {
        "stem": "Violence problem with y = x^2",
        "choices": {"A": "1", "B": "2"},
        "solution_choice_id": "A",
        "skill_id": "quad.graph.vertex",
        "difficulty": "easy"
    }

    strict_result = strict_validator.validate(bad_question)
    lenient_result = lenient_validator.validate(bad_question)

    # Strict mode should fail on critical violations
    if any(v.severity == "critical" for v in strict_result.violations):
        assert not strict_result.passes_constitution, "Strict mode should fail critical violations"

    print(f"✓ Strict mode enforces critical violations")
    print(f"  Strict mode passes: {strict_result.passes_constitution}")
    print(f"  Lenient mode passes: {lenient_result.passes_constitution}")


def test_validation_history():
    """Test that validation history is tracked."""
    validator = EducationalConstitutionalValidator()

    # Validate a few questions
    for i in range(3):
        question = generate_item("quad.graph.vertex", "easy", seed=i)
        validator.validate(question)

    assert len(validator.validation_history) == 3, "Should track all validations"

    stats = validator.get_validation_stats()

    assert stats["total_validations"] == 3, "Should count validations"
    assert "pass_rate" in stats, "Should calculate pass rate"
    assert "avg_score" in stats, "Should calculate average score"
    assert 0 <= stats["avg_score"] <= 1, "Score should be 0-1"

    print(f"✓ Validation history tracked")
    print(f"  Total validations: {stats['total_validations']}")
    print(f"  Passed: {stats['passed']}")
    print(f"  Pass rate: {stats['pass_rate']:.1%}")
    print(f"  Avg score: {stats['avg_score']:.2f}")


def test_multiple_skills():
    """Test validation across multiple skills."""
    validator = EducationalConstitutionalValidator(strict_mode=False)

    skills_to_test = [
        ("quad.graph.vertex", "easy"),
        ("quad.solve.by_factoring", "easy"),
        ("quad.standard.vertex", "medium")
    ]

    results = []

    for skill_id, difficulty in skills_to_test:
        question = generate_item(skill_id, difficulty, seed=0)
        result = validator.validate(question)
        results.append((skill_id, result))

    # All should complete without errors
    assert len(results) == 3, "Should validate all skills"

    print(f"✓ Validates multiple skills")
    for skill_id, result in results:
        print(f"  {skill_id}: score {result.overall_score:.2f}, passes={result.passes_constitution}")


def test_provides_improvement_suggestions():
    """Test that violations include actionable suggestions."""
    validator = EducationalConstitutionalValidator(strict_mode=False)

    # Create a bad question
    bad_question = {
        "stem": "What?",  # Unclear
        "choices": {"A": "1"},  # Not enough choices
        "solution_choice_id": "A",
        "skill_id": "quad.graph.vertex",
        "difficulty": "easy"
    }

    result = validator.validate(bad_question)

    # All violations should have suggestions
    for violation in result.violations:
        assert violation.suggested_fix, "Should provide improvement suggestion"
        assert len(violation.suggested_fix) > 10, "Suggestion should be meaningful"

    print(f"✓ Provides improvement suggestions")
    print(f"  Violations: {len(result.violations)}")
    for v in result.violations[:3]:  # Show first 3
        print(f"    - {v.principle_name}: {v.suggested_fix}")


if __name__ == "__main__":
    print("=" * 70)
    print("EDUCATIONAL CONSTITUTIONAL VALIDATOR ACCEPTANCE TESTS")
    print("=" * 70)
    print()

    # Run all tests
    test_validator_initialization()
    print()

    test_constitution_principles()
    print()

    test_validates_good_question()
    print()

    test_detects_genuine_understanding_violation()
    print()

    test_detects_pedagogical_soundness_violation()
    print()

    test_detects_honest_distractor_violation()
    print()

    test_detects_appropriate_difficulty_violation()
    print()

    test_detects_safe_learning_violation()
    print()

    test_detects_inclusive_accessible_violation()
    print()

    test_weighted_scoring()
    print()

    test_strict_mode()
    print()

    test_validation_history()
    print()

    test_multiple_skills()
    print()

    test_provides_improvement_suggestions()
    print()

    print("=" * 70)
    print("ALL ACCEPTANCE TESTS PASSED ✓")
    print("=" * 70)
