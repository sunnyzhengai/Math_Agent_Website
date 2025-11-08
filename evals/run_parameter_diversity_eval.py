#!/usr/bin/env python3
"""
Parameter Diversity Evaluation

Tests that generated questions have diverse parameters.
This eval is critical for Phase 2 parameterized generation.

For current static templates, this measures stem diversity.
For future parameterized templates, it will measure parameter space coverage.
"""

import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Set, Any
from collections import defaultdict

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.templates import generate_item, SKILL_TEMPLATES


def load_config() -> Dict[str, Any]:
    """Load evaluation configuration."""
    config_path = Path(__file__).parent / "parameter_diversity_eval.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def extract_stem_signature(stem: str) -> str:
    """
    Extract a signature from the question stem.
    For static templates, the stem itself is the signature.
    For parameterized templates, this would extract parameter values.
    """
    # For now, use the stem as-is
    # In Phase 2, we'll parse out parameter values
    return stem


def test_parameter_diversity(
    skill_id: str,
    difficulty: str,
    n_samples: int,
    min_unique_ratio: float,
    min_coverage: float
) -> Dict[str, Any]:
    """
    Test parameter diversity for a skill/difficulty combination.

    Args:
        skill_id: Skill to test
        difficulty: Difficulty level
        n_samples: Number of questions to generate
        min_unique_ratio: Minimum ratio of unique parameter sets
        min_coverage: Minimum coverage of available templates

    Returns:
        Dict with test results
    """
    stems = []
    signatures = []

    # Generate questions
    for seed in range(n_samples):
        try:
            item = generate_item(skill_id, difficulty, seed=seed)
            stem = item.get("stem", "")
            stems.append(stem)
            signatures.append(extract_stem_signature(stem))
        except Exception as e:
            print(f"    ⚠️  Generation failed for seed {seed}: {e}")
            continue

    if not stems:
        return {
            "passed": False,
            "error": "No questions generated",
            "unique_count": 0,
            "total_count": 0,
            "unique_ratio": 0.0,
            "template_coverage": 0.0
        }

    # Calculate metrics
    unique_signatures = set(signatures)
    unique_count = len(unique_signatures)
    total_count = len(stems)
    unique_ratio = unique_count / total_count if total_count > 0 else 0.0

    # Calculate template coverage
    available_templates = len(SKILL_TEMPLATES.get(skill_id, {}).get(difficulty, []))
    template_coverage = unique_count / available_templates if available_templates > 0 else 0.0

    # Check pass/fail
    passed = (unique_ratio >= min_unique_ratio and template_coverage >= min_coverage)

    # Identify issues
    issues = []
    if unique_ratio < min_unique_ratio:
        issues.append(f"Low uniqueness: {unique_ratio:.1%} < {min_unique_ratio:.1%}")
    if template_coverage < min_coverage:
        issues.append(f"Low coverage: {template_coverage:.1%} < {min_coverage:.1%}")

    return {
        "passed": passed,
        "unique_count": unique_count,
        "total_count": total_count,
        "unique_ratio": unique_ratio,
        "available_templates": available_templates,
        "template_coverage": template_coverage,
        "issues": issues
    }


def main():
    """Run parameter diversity evaluation."""
    config = load_config()

    print("=" * 60)
    print("PARAMETER DIVERSITY EVALUATION")
    print("=" * 60)
    print()
    print(f"📊 Testing {len(config['skills'])} skills across {len(config['difficulties'])} difficulty levels")
    print(f"   Samples per test: {config['test_config']['n_samples']}")
    print(f"   Min unique ratio: {config['thresholds']['min_unique_ratio']:.1%}")
    print(f"   Min coverage: {config['thresholds']['min_coverage']:.1%}")
    print()

    results = []
    passed_count = 0
    failed_count = 0

    for skill_id in config['skills']:
        print(f"📚 Testing skill: {skill_id}")

        for difficulty in config['difficulties']:
            result = test_parameter_diversity(
                skill_id=skill_id,
                difficulty=difficulty,
                n_samples=config['test_config']['n_samples'],
                min_unique_ratio=config['thresholds']['min_unique_ratio'],
                min_coverage=config['thresholds']['min_coverage']
            )

            result['skill_id'] = skill_id
            result['difficulty'] = difficulty
            results.append(result)

            # Print result
            status = "✅ PASS" if result['passed'] else "❌ FAIL"
            print(f"  Difficulty: {difficulty}")
            print(f"    {status}")
            print(f"    - Unique: {result['unique_count']}/{result['total_count']} ({result['unique_ratio']:.1%})")
            print(f"    - Templates: {result['available_templates']} available")
            print(f"    - Coverage: {result['template_coverage']:.1%}")

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

    overall_status = "✅ PASS" if failed_count == 0 else "❌ FAIL"
    print(f"Overall status: {overall_status}")
    print()

    # Write detailed results
    output_path = Path(__file__).parent / "parameter_diversity_report.jsonl"
    with open(output_path, "w") as f:
        for result in results:
            f.write(json.dumps(result) + "\n")

    print(f"📝 Detailed results written to: {output_path}")
    print()

    # Exit with appropriate code
    sys.exit(0 if failed_count == 0 else 1)


if __name__ == "__main__":
    main()
