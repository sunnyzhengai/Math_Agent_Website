#!/usr/bin/env python3
"""
Difficulty Calibration Evaluation

Tests whether difficulty labels match actual performance.
Uses the Rules agent as a proxy for "average student" performance.

Expected accuracy by difficulty:
- Easy: 70-80% (building confidence)
- Medium: 50-60% (challenge but achievable)  
- Hard: 30-40% (stretch goals)
- Applied: 40-50% (real-world context)

Metrics:
- Empirical accuracy per difficulty
- Calibration error (|actual - target|)
- Difficulty ordering (hard < medium < easy)
"""

import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.templates import generate_item, SKILL_TEMPLATES
from engine.grader import grade_response
from agents.registry import get_agent


def run_calibration_eval(output_path: str = "evals/calibration_report.jsonl"):
    """Run difficulty calibration evaluation using Rules agent."""

    results = []
    timestamp = datetime.utcnow().isoformat() + "Z"

    print("=" * 60)
    print("DIFFICULTY CALIBRATION EVALUATION")
    print("=" * 60)
    print("\nUsing Rules agent (83% overall) as proxy for average student\n")

    # Get Rules agent
    try:
        agent = get_agent("rules")
    except:
        print("❌ Rules agent not available. Install agent framework first.")
        return 1

    all_passed = True
    total_skills = 0

    # Target accuracies
    targets = {
        "easy": 0.75,
        "medium": 0.55,
        "hard": 0.35,
        "applied": 0.45
    }
    tolerance = 0.15

    for skill_id in SKILL_TEMPLATES.keys():
        total_skills += 1
        print(f"\n📊 Testing skill: {skill_id}")

        for difficulty in ["easy", "medium", "hard", "applied"]:
            if difficulty not in SKILL_TEMPLATES[skill_id]:
                continue

            # Generate and test questions
            n_questions = 20
            correct_count = 0
            total_count = 0

            for i in range(n_questions):
                try:
                    item = generate_item(skill_id, difficulty)
                    choice = agent.choose(item)
                    result = grade_response(item, choice)
                    
                    if result["correct"]:
                        correct_count += 1
                    total_count += 1
                except Exception as e:
                    continue

            if total_count == 0:
                continue

            # Calculate metrics
            accuracy = correct_count / total_count
            target = targets.get(difficulty, 0.5)
            calibration_error = abs(accuracy - target)
            
            # Pass/fail
            passed = calibration_error <= tolerance
            status = "✅ PASS" if passed else "❌ FAIL"

            # Interpretation
            if accuracy > target + tolerance:
                interpretation = "TOO EASY"
            elif accuracy < target - tolerance:
                interpretation = "TOO HARD"
            else:
                interpretation = "WELL CALIBRATED"

            print(f"  {difficulty.capitalize()}: {status}")
            print(f"    - Accuracy: {accuracy:.1%} (target: {target:.0%} ± {tolerance:.0%})")
            print(f"    - Calibration error: {calibration_error:.1%}")
            print(f"    - {interpretation}")

            if not passed:
                all_passed = False

            # Save results
            results.append({
                "timestamp": timestamp,
                "eval_type": "calibration",
                "skill_id": skill_id,
                "difficulty": difficulty,
                "metrics": {
                    "accuracy": accuracy,
                    "target": target,
                    "calibration_error": calibration_error,
                    "questions_tested": total_count,
                    "correct_count": correct_count,
                },
                "passed": passed,
                "interpretation": interpretation,
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
    
    if not all_passed:
        print("\n💡 Recommendations:")
        print("   - TOO EASY: Move to higher difficulty tier or add complexity")
        print("   - TOO HARD: Simplify or move to lower difficulty tier")
        print("   - Ensure difficulty progression: easy > medium > hard")

    print(f"\n📝 Detailed results written to: {output_path}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(run_calibration_eval())
