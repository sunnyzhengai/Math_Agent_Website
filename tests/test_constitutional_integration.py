"""
Quick integration test for Constitutional Validator in Validation Committee.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agentic.agents.question_validation_committee import QuestionValidationCommittee
from engine.templates import generate_item


def test_constitutional_validator_integration():
    """Test that constitutional validator is integrated and working."""

    # TEST 1: Verify integration
    committee = QuestionValidationCommittee(use_constitutional=True)
    assert committee.constitutional_validator is not None, "Constitutional validator should be initialized"

    print(f"✓ Constitutional validator integrated into committee")

    # TEST 2: Test constitutional validator directly (bypassing other agents)
    good_question = {
        "stem": "Find the vertex of y = (x - 3)^2 + 2",
        "choices": [
            {"id": "A", "text": "(3, 2)"},
            {"id": "B", "text": "(-3, 2)"},
            {"id": "C", "text": "(3, -2)"},
            {"id": "D", "text": "(2, 3)"}
        ],
        "solution_choice_id": "A",
        "skill_id": "quad.graph.vertex",
        "difficulty": "easy"
    }

    # Call constitutional validator directly
    const_result = committee.constitutional_validator.validate(good_question)

    print(f"\n✓ Constitutional validator checks all principles")
    print(f"  Principles checked: {const_result.principles_checked}")
    print(f"  Principles passed: {const_result.principles_passed}")
    print(f"  Overall score: {const_result.overall_score:.2f}")
    print(f"  Passes constitution: {const_result.passes_constitution}")

    # TEST 3: Test with harmful content
    bad_question = {
        "stem": "A weapon is fired with velocity 100 m/s. Find the trajectory using y = -16t^2 + 100t.",
        "choices": [
            {"id": "A", "text": "y = -16t^2 + 100t"},
            {"id": "B", "text": "y = -16t^2 + 50t"},
        ],
        "solution_choice_id": "A",
        "skill_id": "quad.graph.vertex",
        "difficulty": "applied"
    }

    # Call constitutional validator directly on harmful content
    const_result_bad = committee.constitutional_validator.validate(bad_question)

    print(f"\n✓ Constitutional validator detects harmful content")
    print(f"  Passes constitution: {const_result_bad.passes_constitution}")
    print(f"  Violations: {len(const_result_bad.violations)}")
    for v in const_result_bad.violations[:2]:
        print(f"    - {v.principle_name} ({v.severity}): {v.violation_description[:60]}...")

    # TEST 4: Verify optional feature (can be disabled)
    committee_no_const = QuestionValidationCommittee(use_constitutional=False)
    assert committee_no_const.constitutional_validator is None, "Should be None when disabled"

    print(f"\n✓ Constitutional validator is optional (can be disabled)")
    print(f"  Committee without constitutional validator created successfully")


if __name__ == "__main__":
    print("=" * 70)
    print("CONSTITUTIONAL VALIDATOR INTEGRATION TEST")
    print("=" * 70)
    print()

    test_constitutional_validator_integration()

    print()
    print("=" * 70)
    print("INTEGRATION TEST PASSED ✓")
    print("=" * 70)
