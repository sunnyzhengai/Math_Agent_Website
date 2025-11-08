#!/usr/bin/env python3
"""
Analyze telemetry data to extract insights for improving question generation.

Usage:
    python tools/analyze_telemetry.py --days 7
    python tools/analyze_telemetry.py --report difficulty_calibration
    python tools/analyze_telemetry.py --report distractor_effectiveness
"""

import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Any


def load_telemetry_events(days: int = 1) -> List[Dict[str, Any]]:
    """Load telemetry events from the last N days."""
    events = []
    logs_dir = Path(__file__).parent.parent / "logs"

    end_date = datetime.now()
    for i in range(days):
        date_str = (end_date - timedelta(days=i)).strftime("%Y-%m-%d")
        telemetry_file = logs_dir / f"telemetry_{date_str}.jsonl"

        if not telemetry_file.exists():
            continue

        with open(telemetry_file, 'r') as f:
            for line in f:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    return events


def analyze_difficulty_calibration(events: List[Dict[str, Any]]):
    """
    Analyze actual student accuracy by difficulty level.

    Target ranges:
    - Easy: 75-90%
    - Medium: 60-75%
    - Hard: 45-60%
    """
    print("\n" + "="*80)
    print("DIFFICULTY CALIBRATION REPORT")
    print("="*80)

    by_skill_difficulty = defaultdict(lambda: defaultdict(lambda: {"total": 0, "correct": 0}))

    for event in events:
        if event.get("event_type") != "question_answered":
            continue

        skill_id = event.get("skill_id")
        difficulty = event.get("difficulty")

        if not skill_id or not difficulty:
            continue

        by_skill_difficulty[skill_id][difficulty]["total"] += 1
        if event.get("is_correct"):
            by_skill_difficulty[skill_id][difficulty]["correct"] += 1

    # Print results
    print(f"\nTarget Accuracy Ranges:")
    print(f"  Easy:   75-90%")
    print(f"  Medium: 60-75%")
    print(f"  Hard:   45-60%")
    print()

    for skill_id in sorted(by_skill_difficulty.keys()):
        print(f"\n📚 {skill_id}")

        for difficulty in ["easy", "medium", "hard", "applied"]:
            if difficulty not in by_skill_difficulty[skill_id]:
                continue

            data = by_skill_difficulty[skill_id][difficulty]
            total = data["total"]
            correct = data["correct"]

            if total == 0:
                continue

            accuracy = correct / total
            status = ""

            if difficulty == "easy":
                if accuracy < 0.75:
                    status = " ⚠️  TOO HARD"
                elif accuracy > 0.90:
                    status = " ⚠️  TOO EASY"
                else:
                    status = " ✅"
            elif difficulty == "medium":
                if accuracy < 0.60:
                    status = " ⚠️  TOO HARD"
                elif accuracy > 0.75:
                    status = " ⚠️  TOO EASY"
                else:
                    status = " ✅"
            elif difficulty == "hard":
                if accuracy < 0.45:
                    status = " ⚠️  TOO HARD"
                elif accuracy > 0.60:
                    status = " ⚠️  TOO EASY"
                else:
                    status = " ✅"

            print(f"  {difficulty:8s}: {accuracy:5.1%} ({correct}/{total}){status}")


def analyze_distractor_effectiveness(events: List[Dict[str, Any]]):
    """
    Analyze which distractors are being chosen.

    Effective distractors should:
    - Be chosen by some students (not ignored)
    - Not be chosen too often (not too similar to correct answer)
    """
    print("\n" + "="*80)
    print("DISTRACTOR EFFECTIVENESS REPORT")
    print("="*80)

    by_skill = defaultdict(lambda: defaultdict(int))
    total_wrong_by_skill = defaultdict(int)

    for event in events:
        if event.get("event_type") != "question_answered":
            continue

        if event.get("is_correct"):
            continue  # Only look at incorrect answers

        skill_id = event.get("skill_id")
        distractor_type = event.get("distractor_type_chosen")

        if not skill_id:
            continue

        total_wrong_by_skill[skill_id] += 1

        if distractor_type:
            by_skill[skill_id][distractor_type] += 1

    # Print results
    print("\nMost common wrong answers by skill:")
    print("(Shows which error patterns students are making)")
    print()

    for skill_id in sorted(by_skill.keys()):
        print(f"\n📚 {skill_id}")
        total_wrong = total_wrong_by_skill[skill_id]

        # Sort distractors by frequency
        distractors = sorted(
            by_skill[skill_id].items(),
            key=lambda x: x[1],
            reverse=True
        )

        for distractor_type, count in distractors:
            pct = count / total_wrong if total_wrong > 0 else 0
            print(f"  {distractor_type:30s}: {count:3d} ({pct:5.1%})")


def analyze_parameter_difficulty(events: List[Dict[str, Any]]):
    """
    Analyze how parameter values correlate with difficulty.

    For example: Do larger numbers make questions harder?
    """
    print("\n" + "="*80)
    print("PARAMETER DIFFICULTY CORRELATION")
    print("="*80)

    by_skill_param = defaultdict(lambda: defaultdict(lambda: {"total": 0, "correct": 0}))

    for event in events:
        if event.get("event_type") != "question_answered":
            continue

        skill_id = event.get("skill_id")
        params = event.get("parameters")

        if not skill_id or not params:
            continue

        # For root-based questions, use max absolute value of roots
        if "r1" in params and "r2" in params:
            max_abs = max(abs(params["r1"]), abs(params["r2"]))

            # Bucket by magnitude
            if max_abs <= 15:
                bucket = "small (≤15)"
            elif max_abs <= 30:
                bucket = "medium (16-30)"
            else:
                bucket = "large (>30)"

            by_skill_param[skill_id][bucket]["total"] += 1
            if event.get("is_correct"):
                by_skill_param[skill_id][bucket]["correct"] += 1

    # Print results
    print("\nAccuracy by parameter magnitude:")
    print("(Do larger numbers make questions harder?)")
    print()

    for skill_id in sorted(by_skill_param.keys()):
        print(f"\n📚 {skill_id}")

        for bucket in ["small (≤15)", "medium (16-30)", "large (>30)"]:
            if bucket not in by_skill_param[skill_id]:
                continue

            data = by_skill_param[skill_id][bucket]
            total = data["total"]
            correct = data["correct"]

            if total == 0:
                continue

            accuracy = correct / total
            print(f"  {bucket:18s}: {accuracy:5.1%} ({correct}/{total})")


def main():
    parser = argparse.ArgumentParser(description="Analyze telemetry data")
    parser.add_argument("--days", type=int, default=7, help="Number of days to analyze")
    parser.add_argument(
        "--report",
        choices=["all", "difficulty_calibration", "distractor_effectiveness", "parameter_difficulty"],
        default="all",
        help="Which report to generate"
    )

    args = parser.parse_args()

    # Load events
    events = load_telemetry_events(days=args.days)

    if not events:
        print(f"No telemetry data found for the last {args.days} days.")
        print(f"Make sure students are using the system and events are being logged to logs/telemetry_*.jsonl")
        return

    print(f"\nLoaded {len(events)} events from the last {args.days} days")

    # Generate reports
    if args.report in ["all", "difficulty_calibration"]:
        analyze_difficulty_calibration(events)

    if args.report in ["all", "distractor_effectiveness"]:
        analyze_distractor_effectiveness(events)

    if args.report in ["all", "parameter_difficulty"]:
        analyze_parameter_difficulty(events)

    print("\n" + "="*80)
    print()


if __name__ == "__main__":
    main()
