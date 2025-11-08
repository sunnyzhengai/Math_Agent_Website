#!/usr/bin/env python3
"""
Adaptive Difficulty Progression Evaluation

Tests the adaptive learning algorithm that advances students through
difficulty levels based on performance.

Validates:
- Advancement after mastery threshold (3 consecutive correct)
- Streak reset on wrong answers
- Mastery detection after completing all difficulties
- Edge cases and boundary conditions
"""

import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


@dataclass
class ProgressTracker:
    """Tracks student progress through difficulty levels."""
    difficulty_index: int = 0
    consecutive_correct: int = 0
    total_attempts: int = 0
    mastered: bool = False


class AdaptiveProgressionSimulator:
    """Simulates the adaptive progression algorithm."""

    def __init__(self, mastery_threshold: int = 3, difficulties: List[str] = None):
        """
        Initialize the simulator.

        Args:
            mastery_threshold: Number of consecutive correct to advance
            difficulties: List of difficulty levels in order
        """
        self.mastery_threshold = mastery_threshold
        self.difficulties = difficulties or ["easy", "medium", "hard"]
        self.tracker = ProgressTracker()

    def get_current_difficulty(self) -> str:
        """Get the current difficulty level."""
        if self.tracker.mastered:
            return "mastered"
        return self.difficulties[self.tracker.difficulty_index]

    def submit_answer(self, correct: bool) -> Dict[str, Any]:
        """
        Simulate submitting an answer and updating progress.

        Args:
            correct: Whether the answer was correct

        Returns:
            Dict with state after this answer
        """
        self.tracker.total_attempts += 1
        previous_difficulty_index = self.tracker.difficulty_index
        previous_streak = self.tracker.consecutive_correct

        if correct:
            self.tracker.consecutive_correct += 1

            # Check if mastery threshold reached
            if self.tracker.consecutive_correct >= self.mastery_threshold:
                current_difficulty = self.difficulties[self.tracker.difficulty_index]

                # Advance to next difficulty
                if self.tracker.difficulty_index < len(self.difficulties) - 1:
                    self.tracker.difficulty_index += 1
                    self.tracker.consecutive_correct = 0  # Reset for new difficulty
                    next_difficulty = self.difficulties[self.tracker.difficulty_index]
                    advanced = True
                else:
                    # Completed all difficulties - mark as mastered
                    self.tracker.mastered = True
                    advanced = False
                    next_difficulty = "mastered"
            else:
                advanced = False
                next_difficulty = self.difficulties[self.tracker.difficulty_index]
        else:
            # Wrong answer - reset streak but stay at current difficulty
            self.tracker.consecutive_correct = 0
            advanced = False
            next_difficulty = self.difficulties[self.tracker.difficulty_index]

        return {
            "correct": correct,
            "previous_difficulty": self.difficulties[previous_difficulty_index],
            "current_difficulty": next_difficulty,
            "previous_streak": previous_streak,
            "current_streak": self.tracker.consecutive_correct,
            "difficulty_advanced": advanced,
            "mastered": self.tracker.mastered,
            "total_attempts": self.tracker.total_attempts
        }

    def get_state(self) -> Dict[str, Any]:
        """Get current state of the tracker."""
        return {
            "difficulty_index": self.tracker.difficulty_index,
            "current_difficulty": self.get_current_difficulty(),
            "consecutive_correct": self.tracker.consecutive_correct,
            "total_attempts": self.tracker.total_attempts,
            "mastered": self.tracker.mastered
        }


def load_config() -> Dict[str, Any]:
    """Load evaluation configuration."""
    config_path = Path(__file__).parent / "adaptive_progression_eval.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def run_scenario(
    scenario: Dict[str, Any],
    mastery_threshold: int,
    difficulties: List[str]
) -> Dict[str, Any]:
    """
    Run a test scenario through the adaptive progression simulator.

    Args:
        scenario: Scenario configuration
        mastery_threshold: Consecutive correct threshold
        difficulties: List of difficulty levels

    Returns:
        Dict with test results
    """
    name = scenario["name"]
    pattern = scenario["pattern"]  # List of 1s (correct) and 0s (wrong)
    expected_sequence = scenario["expected_difficulty_sequence"]
    expected_final = scenario["expected_final_difficulty"]
    expected_mastered = scenario["expected_mastered"]

    # Run simulation
    simulator = AdaptiveProgressionSimulator(mastery_threshold, difficulties)
    actual_sequence = []
    events = []

    for i, correct in enumerate(pattern):
        # Record difficulty before this answer
        current_diff = simulator.get_current_difficulty()
        actual_sequence.append(current_diff)

        # Submit answer
        result = simulator.submit_answer(bool(correct))
        events.append({
            "attempt": i + 1,
            "correct": bool(correct),
            "before_difficulty": current_diff,
            "after_difficulty": result["current_difficulty"],
            "streak_before": result["previous_streak"],
            "streak_after": result["current_streak"],
            "advanced": result["difficulty_advanced"]
        })

    # Get final state
    final_state = simulator.get_state()

    # Validate results
    sequence_match = actual_sequence == expected_sequence
    final_difficulty_match = final_state["current_difficulty"] == expected_final
    mastery_match = final_state["mastered"] == expected_mastered

    all_correct = sequence_match and final_difficulty_match and mastery_match

    # Count specific behaviors
    advancements = sum(1 for e in events if e["advanced"])
    streak_resets = sum(
        1 for i, e in enumerate(events)
        if not e["correct"] and i > 0 and events[i-1]["streak_after"] > 0
    )

    return {
        "scenario": name,
        "description": scenario["description"],
        "passed": all_correct,
        "sequence_match": sequence_match,
        "final_difficulty_match": final_difficulty_match,
        "mastery_match": mastery_match,
        "expected_sequence": expected_sequence,
        "actual_sequence": actual_sequence,
        "expected_final_difficulty": expected_final,
        "actual_final_difficulty": final_state["current_difficulty"],
        "expected_mastered": expected_mastered,
        "actual_mastered": final_state["mastered"],
        "advancements": advancements,
        "streak_resets": streak_resets,
        "events": events
    }


def main():
    """Run the adaptive progression evaluation."""
    print("\n" + "=" * 80)
    print("ADAPTIVE DIFFICULTY PROGRESSION EVALUATION")
    print("=" * 80)

    # Load config
    config = load_config()
    print(f"\nConfiguration: {config['name']}")
    print(f"Description: {config['description'].strip()[:200]}...")

    mastery_threshold = config["test_config"]["mastery_threshold"]
    difficulties = config["test_config"]["difficulties"]

    print(f"\nMastery Threshold: {mastery_threshold} consecutive correct")
    print(f"Difficulty Levels: {' → '.join(difficulties)}")

    # Run test scenarios
    scenarios = config["test_scenarios"]
    print(f"\nRunning {len(scenarios)} test scenarios...\n")

    results = []
    for scenario in scenarios:
        print(f"Testing: {scenario['name']}", end=" ... ", flush=True)
        result = run_scenario(scenario, mastery_threshold, difficulties)
        results.append(result)

        if result["passed"]:
            print("✅ PASS")
        else:
            print("❌ FAIL")
            if not result["sequence_match"]:
                print(f"  ❌ Difficulty sequence mismatch")
                print(f"     Expected: {result['expected_sequence']}")
                print(f"     Actual:   {result['actual_sequence']}")
            if not result["final_difficulty_match"]:
                print(f"  ❌ Final difficulty mismatch: expected {result['expected_final_difficulty']}, got {result['actual_final_difficulty']}")
            if not result["mastery_match"]:
                print(f"  ❌ Mastery detection mismatch: expected {result['expected_mastered']}, got {result['actual_mastered']}")

    # Calculate summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    pass_rate = passed / total if total > 0 else 0

    print(f"\nScenarios Passed: {passed}/{total} ({pass_rate * 100:.1f}%)")

    # Check against thresholds
    thresholds = config["thresholds"]
    threshold_checks = []

    # All scenarios should pass
    all_pass = pass_rate == 1.0
    threshold_checks.append(("All scenarios pass", all_pass, True))

    print("\nThreshold Checks:")
    all_thresholds_met = True
    for name, value, required in threshold_checks:
        status = "✅" if value == required else "❌"
        print(f"  {status} {name}: {value} (required: {required})")
        if value != required:
            all_thresholds_met = False

    # Save detailed report
    report_path = Path(__file__).parent / "adaptive_progression_report.jsonl"
    with open(report_path, 'w') as f:
        for result in results:
            f.write(json.dumps(result) + '\n')

    print(f"\n📄 Detailed report saved to: {report_path}")

    # Show detailed event trace for failed scenarios
    failed = [r for r in results if not r["passed"]]
    if failed:
        print("\n" + "=" * 80)
        print("FAILED SCENARIO DETAILS")
        print("=" * 80)
        for result in failed:
            print(f"\n{result['scenario']}: {result['description']}")
            print("\nEvent Trace:")
            print(f"  {'#':<3} {'Correct':<8} {'Streak':<7} {'Difficulty':<15} {'Advanced':<8}")
            print("  " + "-" * 50)
            for event in result['events']:
                print(
                    f"  {event['attempt']:<3} "
                    f"{'✓' if event['correct'] else '✗':<8} "
                    f"{event['streak_after']:<7} "
                    f"{event['before_difficulty']:<15} "
                    f"{'→ ' + event['after_difficulty'] if event['advanced'] else '':<8}"
                )

    # Final status
    print("\n" + "=" * 80)
    if all_thresholds_met and not failed:
        print("✅ ADAPTIVE PROGRESSION EVAL PASSED")
        print("\nThe adaptive learning algorithm works correctly!")
    else:
        print("❌ ADAPTIVE PROGRESSION EVAL FAILED")
        print("\nThe adaptive learning algorithm has issues that need to be fixed.")
    print("=" * 80 + "\n")

    sys.exit(0 if (all_thresholds_met and not failed) else 1)


if __name__ == "__main__":
    main()
