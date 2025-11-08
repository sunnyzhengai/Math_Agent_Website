#!/usr/bin/env python3
"""
Distractor Quality Evaluation

Tests that wrong answer choices (distractors) are high quality.
Ensures questions are educational and appropriately challenging.

Verifies:
- Distractors are unique
- Rules agent achieves reasonable accuracy (60-85%)
- Questions aren't too easy or too hard
"""

import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.templates import generate_item, SKILL_TEMPLATES
from agentic.agents.rule_router import RuleRouterAgent


def load_config() -> Dict[str, Any]:
    """Load evaluation configuration."""
    config_path = Path(__file__).parent / "distractor_quality_eval.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def analyze_distractors(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze the quality of distractor choices.

    Args:
        item: Generated question item

    Returns:
        Dict with distractor analysis
    """
    choices = item.get("choices", [])
    solution_text = item.get("solution_text", "")

    # Get all choice texts
    choice_texts = [c.get("text", "") for c in choices]

    # Identify distractors (non-solution choices)
    distractors = [text for text in choice_texts if text != solution_text]

    # Check uniqueness
    unique_distractors = set(distractors)
    num_unique = len(unique_distractors)

    # Check if all choices are unique
    all_unique = len(set(choice_texts)) == len(choice_texts)

    return {
        "num_distractors": len(distractors),
        "num_unique_distractors": num_unique,
        "all_choices_unique": all_unique,
        "distractor_texts": distractors
    }


def test_distractor_quality(
    skill_id: str,
    difficulty: str,
    n_samples: int,
    min_rules_accuracy: float,
    max_rules_accuracy: float
) -> Dict[str, Any]:
    """
    Test distractor quality for a skill/difficulty combination.

    Args:
        skill_id: Skill to test
        difficulty: Difficulty level
        n_samples: Number of questions to test
        min_rules_accuracy: Minimum acceptable rules agent accuracy
        max_rules_accuracy: Maximum acceptable rules agent accuracy

    Returns:
        Dict with test results
    """
    rules_agent = RuleRouterAgent()
    results = []

    for seed in range(n_samples):
        try:
            # Generate item
            item = generate_item(skill_id, difficulty, seed=seed)

            # Analyze distractors
            distractor_analysis = analyze_distractors(item)

            # Test with rules agent
            rules_answer = rules_agent.choose(item)
            rules_correct = (rules_answer == item['solution_choice_id'])

            result = {
                "seed": seed,
                "item_id": item.get("item_id"),
                "rules_correct": rules_correct,
                "rules_answer": rules_answer,
                "expected_answer": item['solution_choice_id'],
                **distractor_analysis
            }

            results.append(result)

        except Exception as e:
            error_result = {
                "seed": seed,
                "error": str(e),
                "rules_correct": False
            }
            results.append(error_result)

    # Calculate metrics
    total = len(results)
    rules_correct_count = sum(1 for r in results if r.get("rules_correct", False))
    rules_accuracy = rules_correct_count / total if total > 0 else 0.0

    # Check distractor uniqueness
    all_unique_count = sum(1 for r in results if r.get("all_choices_unique", False))
    uniqueness_rate = all_unique_count / total if total > 0 else 0.0

    # Check pass/fail
    accuracy_ok = (min_rules_accuracy <= rules_accuracy <= max_rules_accuracy)
    uniqueness_ok = (uniqueness_rate >= 0.95)  # 95%+ should have unique choices

    passed = accuracy_ok and uniqueness_ok

    issues = []
    if not accuracy_ok:
        if rules_accuracy < min_rules_accuracy:
            issues.append(f"Too hard: Rules accuracy {rules_accuracy:.1%} < {min_rules_accuracy:.1%}")
        else:
            issues.append(f"Too easy: Rules accuracy {rules_accuracy:.1%} > {max_rules_accuracy:.1%}")

    if not uniqueness_ok:
        issues.append(f"Poor uniqueness: {uniqueness_rate:.1%} have unique choices (need 95%+)")

    return {
        "passed": passed,
        "total_tested": total,
        "rules_correct": rules_correct_count,
        "rules_accuracy": rules_accuracy,
        "accuracy_in_range": accuracy_ok,
        "all_unique_count": all_unique_count,
        "uniqueness_rate": uniqueness_rate,
        "issues": issues
    }


def main():
    """Run distractor quality evaluation."""
    config = load_config()

    print("=" * 60)
    print("DISTRACTOR QUALITY EVALUATION")
    print("=" * 60)
    print()
    print(f"📊 Testing {len(config['skills'])} skills across {len(config['difficulties'])} difficulty levels")
    print(f"   Samples per test: {config['test_config']['n_samples']}")
    print(f"   Target rules accuracy: {config['thresholds']['min_rules_accuracy']:.1%} - {config['thresholds']['max_rules_accuracy']:.1%}")
    print()

    results = []
    passed_count = 0
    failed_count = 0

    for skill_id in config['skills']:
        print(f"📚 Testing skill: {skill_id}")

        for difficulty in config['difficulties']:
            result = test_distractor_quality(
                skill_id=skill_id,
                difficulty=difficulty,
                n_samples=config['test_config']['n_samples'],
                min_rules_accuracy=config['thresholds']['min_rules_accuracy'],
                max_rules_accuracy=config['thresholds']['max_rules_accuracy']
            )

            result['skill_id'] = skill_id
            result['difficulty'] = difficulty
            results.append(result)

            # Print result
            status = "✅ PASS" if result['passed'] else "❌ FAIL"
            print(f"  Difficulty: {difficulty}")
            print(f"    {status}")
            print(f"    - Rules accuracy: {result['rules_accuracy']:.1%} ({result['rules_correct']}/{result['total_tested']})")
            print(f"    - Uniqueness rate: {result['uniqueness_rate']:.1%}")

            if result['issues']:
                for issue in result['issues']:
                    print(f"    - ⚠️  {issue}")

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

    # Calculate overall rules accuracy
    avg_rules_accuracy = sum(r['rules_accuracy'] for r in results) / len(results)
    print(f"Average rules accuracy: {avg_rules_accuracy:.1%}")
    print()

    overall_status = "✅ PASS" if failed_count == 0 else "❌ FAIL"
    print(f"Overall status: {overall_status}")
    print()

    # Write detailed results
    output_path = Path(__file__).parent / "distractor_quality_report.jsonl"
    with open(output_path, "w") as f:
        for result in results:
            f.write(json.dumps(result) + "\n")

    print(f"📝 Detailed results written to: {output_path}")
    print()

    # Exit with appropriate code
    sys.exit(0 if failed_count == 0 else 1)


if __name__ == "__main__":
    main()
