#!/usr/bin/env python3
"""
Parameter Variation Evaluation

For parameterized templates, measures how diverse the generated parameters are.
This ensures we're not just generating the same numbers over and over.

Currently a placeholder - will be fully implemented in Phase 2.

Metrics:
- Unique parameter combinations
- Parameter range utilization
- Distribution evenness
"""

import sys
import json
import re
from pathlib import Path
from collections import Counter
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.templates import generate_item, SKILL_TEMPLATES


def extract_numbers_from_stem(stem: str) -> tuple:
    """Extract all numbers from a question stem as a tuple (for hashing)."""
    numbers = re.findall(r'-?\d+\.?\d*', stem)
    return tuple(numbers)


def run_variation_eval(output_path: str = "evals/variation_report.jsonl"):
    """Run parameter variation evaluation."""

    results = []
    timestamp = datetime.utcnow().isoformat() + "Z"

    print("=" * 60)
    print("PARAMETER VARIATION EVALUATION")
    print("=" * 60)
    print("\n⚠️  NOTE: This eval is a placeholder for Phase 2 (Parameterized Generation)")
    print("Current templates are static, so we're measuring number patterns in stems.\n")

    all_passed = True
    total_skills = 0

    for skill_id in SKILL_TEMPLATES.keys():
        total_skills += 1
        print(f"\n📊 Testing skill: {skill_id}")

        for difficulty in ["easy", "medium", "hard", "applied"]:
            if difficulty not in SKILL_TEMPLATES[skill_id]:
                continue

            print(f"  Difficulty: {difficulty}")

            # Generate questions and extract number patterns
            n_questions = 20
            number_patterns = []

            for i in range(n_questions):
                try:
                    item = generate_item(skill_id, difficulty)
                    pattern = extract_numbers_from_stem(item["stem"])
                    number_patterns.append(pattern)
                except Exception as e:
                    continue

            # Metrics
            unique_patterns = len(set(number_patterns))
            total_patterns = len(number_patterns)
            reuse_rate = 1 - (unique_patterns / total_patterns) if total_patterns > 0 else 0

            # For current static templates, we expect low variation
            # In Phase 2, we'll expect high variation

            print(f"    📈 Analysis:")
            print(f"    - Unique number patterns: {unique_patterns}/{total_patterns}")
            print(f"    - Pattern reuse rate: {reuse_rate:.1%}")
            print(f"    - Status: ⏳ PHASE 2 (Not yet parameterized)")

            # Save results
            results.append({
                "timestamp": timestamp,
                "eval_type": "variation",
                "skill_id": skill_id,
                "difficulty": difficulty,
                "metrics": {
                    "unique_patterns": unique_patterns,
                    "total_generated": total_patterns,
                    "reuse_rate": reuse_rate,
                    "is_parameterized": False,  # Will be True in Phase 2
                },
                "passed": None,  # Not applicable until parameterization
                "note": "Baseline measurement before parameterization"
            })

    # Write results
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "a") as f:
        for result in results:
            f.write(json.dumps(result) + "\n")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total skills tested: {total_skills}")
    print(f"\n💡 This eval will become active in Phase 2 when we implement:")
    print("   - Parameterized question templates")
    print("   - Variable coefficients and values")
    print("   - Target: 15+ unique parameter sets in 20 generations")
    print(f"\n📝 Baseline results written to: {output_path}")

    return 0  # Always pass for now


if __name__ == "__main__":
    sys.exit(run_variation_eval())
