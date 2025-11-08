#!/usr/bin/env python3
"""
Question Uniqueness Evaluation

Checks that students don't see consecutive duplicate questions.
This eval specifically tests the anti-repetition mechanism.

Metrics:
- Consecutive duplicates (must be 0)
- Near duplicates within sliding window
- Minimum distance between repeated questions
"""

import sys
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.templates import generate_item, SKILL_TEMPLATES


def run_uniqueness_eval(output_path: str = "evals/uniqueness_report.jsonl"):
    """Run question uniqueness evaluation across all skills."""

    results = []
    timestamp = datetime.utcnow().isoformat() + "Z"

    print("=" * 60)
    print("QUESTION UNIQUENESS EVALUATION")
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

            # Generate sequence of 50 questions to test repetition patterns
            n_questions = 50
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

            # Metric 1: Consecutive duplicates
            consecutive_dupes = 0
            consecutive_positions = []
            for i in range(1, len(stems)):
                if stems[i] == stems[i-1]:
                    consecutive_dupes += 1
                    consecutive_positions.append(i)

            # Metric 2: Near duplicates (within window of 5)
            window_size = 5
            near_dupes = 0
            near_dupe_positions = []
            for i in range(len(stems)):
                window_start = max(0, i - window_size + 1)
                window_stems = stems[window_start:i]
                if stems[i] in window_stems:
                    near_dupes += 1
                    near_dupe_positions.append(i)

            # Metric 3: Minimum distance between repeats
            stem_positions = defaultdict(list)
            for i, stem in enumerate(stems):
                stem_positions[stem].append(i)

            min_distance = float('inf')
            distances = []
            for stem, positions in stem_positions.items():
                if len(positions) > 1:
                    for j in range(1, len(positions)):
                        distance = positions[j] - positions[j-1]
                        distances.append(distance)
                        min_distance = min(min_distance, distance)

            if min_distance == float('inf'):
                min_distance = None  # No repeats at all

            # Determine pass/fail
            passed = True
            issues = []

            # Thresholds from yaml
            max_consecutive = 0
            max_near_in_5 = 1
            min_distance_threshold = 3

            if consecutive_dupes > max_consecutive:
                passed = False
                issues.append(f"Found {consecutive_dupes} consecutive duplicates at positions {consecutive_positions[:5]}")

            if near_dupes > len(stems) * 0.2:  # More than 20% are near-duplicates
                passed = False
                issues.append(f"Too many near-duplicates: {near_dupes}/{len(stems)} ({near_dupes/len(stems)*100:.1f}%)")

            if min_distance is not None and min_distance < min_distance_threshold:
                passed = False
                issues.append(f"Questions repeated too quickly (min distance: {min_distance}, need: {min_distance_threshold})")

            # Report results
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"    {status}")
            print(f"    - Consecutive duplicates: {consecutive_dupes}")
            print(f"    - Near duplicates (within 5): {near_dupes}")
            if min_distance is not None:
                print(f"    - Min distance between repeats: {min_distance}")
            else:
                print(f"    - Min distance: N/A (no repeats)")

            if distances:
                avg_distance = sum(distances) / len(distances)
                print(f"    - Avg distance between repeats: {avg_distance:.1f}")

            if issues:
                for issue in issues:
                    print(f"    {issue}")

            if not passed:
                all_passed = False
                failed_skills.append(f"{skill_id}:{difficulty}")

            # Save detailed results
            results.append({
                "timestamp": timestamp,
                "eval_type": "uniqueness",
                "skill_id": skill_id,
                "difficulty": difficulty,
                "metrics": {
                    "consecutive_duplicates": consecutive_dupes,
                    "near_duplicates": near_dupes,
                    "min_distance": min_distance,
                    "avg_distance": sum(distances) / len(distances) if distances else None,
                    "total_questions": len(stems),
                    "unique_questions": len(set(stems)),
                    "uniqueness_rate": len(set(stems)) / len(stems) if stems else 0
                },
                "passed": passed,
                "issues": issues,
                "consecutive_positions": consecutive_positions[:10],  # First 10 only
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
        for skill in failed_skills[:10]:  # Show first 10
            print(f"  - {skill}")
        if len(failed_skills) > 10:
            print(f"  ... and {len(failed_skills) - 10} more")

        print("\n💡 Recommendation: Implement anti-repetition tracking")
        print("   - Track last N questions per session")
        print("   - Filter out recently seen questions")
        print("   - Ensure minimum distance between repeats")

    print(f"\n📝 Detailed results written to: {output_path}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(run_uniqueness_eval())
