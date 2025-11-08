#!/usr/bin/env python3
"""
Question Diversity Evaluation

Measures how diverse and unique generated questions are to ensure students
don't see the same questions repeatedly. This eval catches the issue where
only 2 question templates exist for a skill, causing repetitive learning experience.

Metrics:
- Unique question stems in N generations
- Repetition rate (consecutive duplicates)
- Template utilization (what % of available templates get used)
- Parameter variation (for parameterized questions)
"""

import sys
import json
from pathlib import Path
from collections import Counter
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.templates import generate_item, SKILL_TEMPLATES


def run_diversity_eval(output_path: str = "evals/diversity_report.jsonl"):
    """Run question diversity evaluation across all skills."""

    results = []
    timestamp = datetime.utcnow().isoformat() + "Z"

    print("=" * 60)
    print("QUESTION DIVERSITY EVALUATION")
    print("=" * 60)

    all_passed = True
    total_skills = 0
    failed_skills = []

    for skill_id in SKILL_TEMPLATES.keys():
        total_skills += 1
        print(f"\n📊 Testing skill: {skill_id}")

        # Test each difficulty level
        for difficulty in ["easy", "medium", "hard", "applied"]:
            if difficulty not in SKILL_TEMPLATES[skill_id]:
                continue

            print(f"  Difficulty: {difficulty}")

            # Generate 20 questions
            n_questions = 20
            questions = []
            stems = []

            for i in range(n_questions):
                try:
                    item = generate_item(skill_id, difficulty)
                    questions.append(item)
                    stems.append(item["stem"])
                except Exception as e:
                    print(f"    ❌ Generation failed: {e}")
                    continue

            # Calculate metrics
            unique_stems = len(set(stems))
            template_count = len(SKILL_TEMPLATES[skill_id][difficulty])

            # Count consecutive duplicates
            consecutive_dupes = 0
            for i in range(1, len(stems)):
                if stems[i] == stems[i-1]:
                    consecutive_dupes += 1

            # Calculate repetition rate
            stem_counts = Counter(stems)
            most_common_count = stem_counts.most_common(1)[0][1] if stem_counts else 0
            repetition_rate = most_common_count / n_questions if n_questions > 0 else 0

            # Template utilization - how many unique templates were used
            template_utilization = unique_stems / template_count if template_count > 0 else 0

            # Determine pass/fail
            passed = True
            issues = []

            # Thresholds from yaml
            min_unique_stems = 10
            max_repetition_rate = 0.3
            min_template_utilization = 0.5

            if unique_stems < min_unique_stems:
                passed = False
                issues.append(f"Only {unique_stems}/{n_questions} unique stems (need {min_unique_stems})")

            if repetition_rate > max_repetition_rate:
                passed = False
                issues.append(f"Repetition rate {repetition_rate:.1%} exceeds {max_repetition_rate:.0%}")

            if template_utilization < min_template_utilization and template_count > 2:
                passed = False
                issues.append(f"Template utilization {template_utilization:.1%} below {min_template_utilization:.0%}")

            # Low template count warning
            if template_count < 5:
                issues.append(f"⚠️  Only {template_count} templates available (recommend 10+)")
                if template_count < 3:
                    passed = False

            # Report results
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"    {status}")
            print(f"    - Unique stems: {unique_stems}/{n_questions} ({unique_stems/n_questions*100:.0f}%)")
            print(f"    - Available templates: {template_count}")
            print(f"    - Template utilization: {template_utilization:.0%}")
            print(f"    - Repetition rate: {repetition_rate:.1%}")
            print(f"    - Consecutive duplicates: {consecutive_dupes}")

            if issues:
                for issue in issues:
                    print(f"    {issue}")

            if not passed:
                all_passed = False
                failed_skills.append(f"{skill_id}:{difficulty}")

            # Save detailed results
            results.append({
                "timestamp": timestamp,
                "eval_type": "diversity",
                "skill_id": skill_id,
                "difficulty": difficulty,
                "metrics": {
                    "unique_stems": unique_stems,
                    "total_generated": n_questions,
                    "template_count": template_count,
                    "template_utilization": template_utilization,
                    "repetition_rate": repetition_rate,
                    "consecutive_duplicates": consecutive_dupes,
                    "diversity_score": unique_stems / n_questions
                },
                "passed": passed,
                "issues": issues
            })

    # Write results
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "a") as f:
        for result in results:
            f.write(json.dumps(result) + "\n")

    # Final summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total skills tested: {total_skills}")
    print(f"Overall status: {'✅ PASS' if all_passed else '❌ FAIL'}")

    if failed_skills:
        print(f"\n❌ Failed skills ({len(failed_skills)}):")
        for skill in failed_skills:
            print(f"  - {skill}")
        print("\n💡 Recommendation: Add more question templates to improve diversity")
        print("   Each skill should have 10+ templates per difficulty level")

    print(f"\n📝 Detailed results written to: {output_path}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(run_diversity_eval())
