#!/usr/bin/env python3
"""
Template Coverage Evaluation

Verifies that all available question templates get used over time.
A good distribution means students see variety, not the same subset repeatedly.

Metrics:
- Coverage at N questions (what % of templates seen?)
- Questions needed for full coverage
- Template usage distribution (are some templates never used?)
"""

import sys
import json
from pathlib import Path
from collections import Counter
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.templates import generate_item, SKILL_TEMPLATES


def run_coverage_eval(output_path: str = "evals/coverage_report.jsonl"):
    """Run template coverage evaluation across all skills."""

    results = []
    timestamp = datetime.utcnow().isoformat() + "Z"

    print("=" * 60)
    print("TEMPLATE COVERAGE EVALUATION")
    print("=" * 60)

    all_passed = True
    total_skills = 0
    failed_skills = []

    for skill_id in SKILL_TEMPLATES.keys():
        total_skills += 1
        print(f"\n📊 Testing skill: {skill_id}")

        for difficulty in ["easy", "medium", "hard", "applied"]:
            if difficulty not in SKILL_TEMPLATES[skill_id]:
                continue

            print(f"  Difficulty: {difficulty}")

            pool_size = len(SKILL_TEMPLATES[skill_id][difficulty])
            
            # Generate questions and track which templates are used
            n_questions = min(100, pool_size * 10)  # Generate enough to test coverage
            stem_counts = Counter()
            seen_order = []

            for i in range(n_questions):
                try:
                    item = generate_item(skill_id, difficulty)
                    stem = item["stem"]
                    stem_counts[stem] += 1
                    if stem not in seen_order:
                        seen_order.append(stem)
                except Exception as e:
                    print(f"    ❌ Generation failed: {e}")
                    continue

            # Metrics
            unique_seen = len(stem_counts)
            coverage_rate = unique_seen / pool_size if pool_size > 0 else 0
            
            # Questions needed to see all templates
            questions_to_full_coverage = len(seen_order) if unique_seen == pool_size else None
            
            # Coverage at checkpoints
            coverage_at_50 = len([s for s in seen_order[:50]]) / pool_size if pool_size > 0 and len(seen_order) >= 50 else None
            coverage_at_100 = len([s for s in seen_order[:100]]) / pool_size if pool_size > 0 and len(seen_order) >= 100 else None

            # Unused templates
            all_stems = {q["stem"] for q in SKILL_TEMPLATES[skill_id][difficulty]}
            unused_stems = all_stems - set(stem_counts.keys())

            # Distribution analysis
            if stem_counts:
                most_common = stem_counts.most_common(1)[0]
                least_common = stem_counts.most_common()[-1]
                usage_ratio = most_common[1] / least_common[1] if least_common[1] > 0 else float('inf')
            else:
                usage_ratio = None

            # Pass/fail determination
            passed = True
            issues = []

            if pool_size > 5:  # Only enforce for pools with enough templates
                if coverage_at_50 and coverage_at_50 < 0.8:
                    passed = False
                    issues.append(f"Low coverage at 50 questions: {coverage_at_50:.1%} (need 80%)")
                
                if coverage_at_100 and coverage_at_100 < 0.95:
                    passed = False
                    issues.append(f"Low coverage at 100 questions: {coverage_at_100:.1%} (need 95%)")

            if unused_stems:
                issues.append(f"⚠️  {len(unused_stems)} templates never appeared in {n_questions} questions")

            if usage_ratio and usage_ratio > 5:
                issues.append(f"⚠️  Uneven distribution: most used {usage_ratio:.1f}x more than least used")

            # Report
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"    {status}")
            print(f"    - Pool size: {pool_size} templates")
            print(f"    - Coverage: {unique_seen}/{pool_size} ({coverage_rate:.0%})")
            if coverage_at_50:
                print(f"    - Coverage at 50 questions: {coverage_at_50:.0%}")
            if questions_to_full_coverage:
                print(f"    - Questions to full coverage: {questions_to_full_coverage}")
            if unused_stems:
                print(f"    - Unused templates: {len(unused_stems)}")
            if usage_ratio:
                print(f"    - Usage ratio (max/min): {usage_ratio:.1f}x")

            if issues:
                for issue in issues:
                    print(f"    {issue}")

            if not passed:
                all_passed = False
                failed_skills.append(f"{skill_id}:{difficulty}")

            # Save results
            results.append({
                "timestamp": timestamp,
                "eval_type": "coverage",
                "skill_id": skill_id,
                "difficulty": difficulty,
                "metrics": {
                    "pool_size": pool_size,
                    "unique_seen": unique_seen,
                    "coverage_rate": coverage_rate,
                    "coverage_at_50": coverage_at_50,
                    "coverage_at_100": coverage_at_100,
                    "questions_to_full_coverage": questions_to_full_coverage,
                    "unused_count": len(unused_stems),
                    "usage_ratio": usage_ratio,
                },
                "passed": passed,
                "issues": issues,
            })

    # Write results
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "a") as f:
        for result in results:
            f.write(json.dumps(result) + "\n")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total skills tested: {total_skills}")
    print(f"Overall status: {'✅ PASS' if all_passed else '❌ FAIL'}")

    if failed_skills:
        print(f"\n❌ Failed skills ({len(failed_skills)}):")
        for skill in failed_skills[:10]:
            print(f"  - {skill}")

    print(f"\n📝 Detailed results written to: {output_path}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(run_coverage_eval())
