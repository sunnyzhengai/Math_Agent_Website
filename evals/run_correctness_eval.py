#!/usr/bin/env python3
"""
Mathematical Correctness Evaluation

Tests that generated questions are mathematically correct.
This is a CRITICAL eval - must pass 100% for production use.

Verifies:
- Solutions are correct (using oracle agent)
- No duplicate answer choices
- No solution collisions (solution matches a distractor)
"""

import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.templates import generate_item, SKILL_TEMPLATES
from agentic.agents.oracle import OracleAgent


def load_config() -> Dict[str, Any]:
    """Load evaluation configuration."""
    config_path = Path(__file__).parent / "correctness_eval.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def check_choice_validity(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check if answer choices are valid (no duplicates, no collisions).

    Args:
        item: Generated question item

    Returns:
        Dict with validation results
    """
    choices = item.get("choices", [])
    choice_texts = [c.get("text", "") for c in choices]
    solution_text = item.get("solution_text", "")
    solution_id = item.get("solution_choice_id", "")

    issues = []

    # Check for duplicate choices
    unique_choices = set(choice_texts)
    if len(unique_choices) < len(choice_texts):
        duplicates = [text for text in choice_texts if choice_texts.count(text) > 1]
        issues.append(f"Duplicate choices found: {set(duplicates)}")

    # Check that solution matches one of the choices
    if solution_text not in choice_texts:
        issues.append(f"Solution '{solution_text}' not found in choices")

    # Check that solution_id is valid
    valid_ids = [c.get("id") for c in choices]
    if solution_id not in valid_ids:
        issues.append(f"Solution ID '{solution_id}' not in valid IDs: {valid_ids}")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "num_choices": len(choices),
        "num_unique": len(unique_choices)
    }


def test_correctness(
    skill_id: str,
    difficulty: str,
    n_samples: int
) -> Dict[str, Any]:
    """
    Test mathematical correctness for a skill/difficulty combination.

    Args:
        skill_id: Skill to test
        difficulty: Difficulty level
        n_samples: Number of questions to test

    Returns:
        Dict with test results
    """
    oracle = OracleAgent()
    results = []
    errors = []

    for seed in range(n_samples):
        try:
            # Generate item
            item = generate_item(skill_id, difficulty, seed=seed)

            # Check choice validity
            validity = check_choice_validity(item)

            # Test with oracle
            oracle_answer = oracle.choose(item)
            correct = (oracle_answer == item['solution_choice_id'])

            result = {
                "seed": seed,
                "item_id": item.get("item_id"),
                "stem": item.get("stem", "")[:100],  # Truncate for readability
                "oracle_correct": correct,
                "oracle_answer": oracle_answer,
                "expected_answer": item['solution_choice_id'],
                "choice_valid": validity["valid"],
                "choice_issues": validity.get("issues", [])
            }

            results.append(result)

            # Track failures
            if not correct or not validity["valid"]:
                errors.append(result)

        except Exception as e:
            error_result = {
                "seed": seed,
                "error": str(e),
                "oracle_correct": False,
                "choice_valid": False
            }
            results.append(error_result)
            errors.append(error_result)

    # Calculate metrics
    total = len(results)
    oracle_correct_count = sum(1 for r in results if r.get("oracle_correct", False))
    choice_valid_count = sum(1 for r in results if r.get("choice_valid", False))

    oracle_accuracy = oracle_correct_count / total if total > 0 else 0.0
    choice_validity_rate = choice_valid_count / total if total > 0 else 0.0

    # Check pass/fail (must be 100% on both)
    passed = (oracle_accuracy == 1.0 and choice_validity_rate == 1.0)

    return {
        "passed": passed,
        "total_tested": total,
        "oracle_correct": oracle_correct_count,
        "oracle_accuracy": oracle_accuracy,
        "choice_valid": choice_valid_count,
        "choice_validity_rate": choice_validity_rate,
        "errors": errors
    }


def main():
    """Run correctness evaluation."""
    config = load_config()

    print("=" * 60)
    print("MATHEMATICAL CORRECTNESS EVALUATION")
    print("=" * 60)
    print()
    print("⚠️  CRITICAL: This eval must achieve 100% accuracy")
    print(f"📊 Testing {len(config['skills'])} skills across {len(config['difficulties'])} difficulty levels")
    print(f"   Samples per test: {config['test_config']['n_samples']}")
    print()

    results = []
    passed_count = 0
    failed_count = 0
    all_errors = []

    for skill_id in config['skills']:
        print(f"📚 Testing skill: {skill_id}")

        for difficulty in config['difficulties']:
            result = test_correctness(
                skill_id=skill_id,
                difficulty=difficulty,
                n_samples=config['test_config']['n_samples']
            )

            result['skill_id'] = skill_id
            result['difficulty'] = difficulty
            results.append(result)

            # Print result
            status = "✅ PASS" if result['passed'] else "❌ FAIL"
            print(f"  Difficulty: {difficulty}")
            print(f"    {status}")
            print(f"    - Oracle accuracy: {result['oracle_accuracy']:.1%} ({result['oracle_correct']}/{result['total_tested']})")
            print(f"    - Choice validity: {result['choice_validity_rate']:.1%} ({result['choice_valid']}/{result['total_tested']})")

            if result['errors']:
                print(f"    - ⚠️  {len(result['errors'])} errors found")
                all_errors.extend(result['errors'])

            if result['passed']:
                passed_count += 1
            else:
                failed_count += 1

        print()

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    total_tests = len(results)
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_count} ({passed_count/total_tests*100:.1f}%)")
    print(f"Failed: {failed_count} ({failed_count/total_tests*100:.1f}%)")
    print()

    if all_errors:
        print(f"⚠️  ERRORS FOUND: {len(all_errors)} total")
        print()
        print("First 5 errors:")
        for i, error in enumerate(all_errors[:5], 1):
            print(f"\n{i}. Seed: {error.get('seed')}")
            print(f"   Stem: {error.get('stem', 'N/A')}")
            if 'oracle_correct' in error and not error['oracle_correct']:
                print(f"   Oracle: {error.get('oracle_answer')} (expected: {error.get('expected_answer')})")
            if 'choice_issues' in error and error['choice_issues']:
                print(f"   Choice issues: {error['choice_issues']}")
            if 'error' in error:
                print(f"   Error: {error['error']}")
        print()

    overall_status = "✅ PASS" if failed_count == 0 else "❌ FAIL"
    print(f"Overall status: {overall_status}")
    print()

    # Write detailed results
    output_path = Path(__file__).parent / "correctness_report.jsonl"
    with open(output_path, "w") as f:
        for result in results:
            f.write(json.dumps(result) + "\n")

    print(f"📝 Detailed results written to: {output_path}")
    print()

    # Exit with appropriate code
    sys.exit(0 if failed_count == 0 else 1)


if __name__ == "__main__":
    main()
