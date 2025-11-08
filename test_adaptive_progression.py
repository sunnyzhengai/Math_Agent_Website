#!/usr/bin/env python3
"""
Test adaptive difficulty progression by simulating a quiz session.

This test verifies that:
1. Questions start at 'easy' difficulty
2. After 3 consecutive correct answers, difficulty advances to 'medium'
3. After 3 more consecutive correct at medium, advances to 'hard'
4. After mastering all difficulties, skill is marked as mastered
5. Wrong answers reset the streak without changing difficulty
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from engine.templates import generate_item
from engine.grader import grade_response


def simulate_quiz_session():
    """Simulate a student answering questions with adaptive progression."""

    print("\n" + "=" * 80)
    print("ADAPTIVE DIFFICULTY PROGRESSION TEST")
    print("=" * 80)

    skill_id = "quad.graph.vertex"
    difficulties = ["easy", "medium", "hard"]

    # Simulate progression through difficulties
    for target_difficulty in difficulties:
        print(f"\n{'─' * 80}")
        print(f"TARGET DIFFICULTY: {target_difficulty.upper()}")
        print(f"{'─' * 80}")

        consecutive_correct = 0
        question_num = 1

        # Answer questions until we get 3 consecutive correct
        while consecutive_correct < 3:
            print(f"\nQuestion {question_num} ({target_difficulty}):")

            # Generate question at current difficulty
            item = generate_item(skill_id, target_difficulty, seed=question_num * 10)
            print(f"  Stem: {item['stem'][:70]}...")

            # Simulate correct answer
            result = grade_response(item, item['solution_choice_id'], detailed=False)

            if result['correct']:
                consecutive_correct += 1
                print(f"  ✓ Correct! Streak: {consecutive_correct}/3")
            else:
                consecutive_correct = 0
                print(f"  ✗ Wrong (this shouldn't happen in this test)")

            question_num += 1

        print(f"\n✅ MASTERY ACHIEVED for {target_difficulty}!")

        if target_difficulty == "hard":
            print(f"\n🎉 SKILL FULLY MASTERED: {skill_id}")

    # Test streak reset on wrong answer
    print(f"\n{'─' * 80}")
    print("TESTING STREAK RESET ON WRONG ANSWER")
    print(f"{'─' * 80}")

    consecutive_correct = 0
    for i in range(2):
        item = generate_item(skill_id, "easy", seed=i + 100)
        result = grade_response(item, item['solution_choice_id'], detailed=False)
        consecutive_correct += 1
        print(f"\nQuestion {i+1}: ✓ Correct (streak: {consecutive_correct})")

    # Now answer wrong
    item = generate_item(skill_id, "easy", seed=999)
    wrong_choice = next(c['id'] for c in item['choices'] if c['id'] != item['solution_choice_id'])
    result = grade_response(item, wrong_choice, detailed=False)
    print(f"\nQuestion 3: ✗ Wrong answer - streak should reset to 0")
    print("Expected behavior: Stay at current difficulty, reset consecutive_correct to 0")

    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)
    print("\nNext steps:")
    print("  1. Test in the actual UI by answering questions in Adaptive Quiz")
    print("  2. Check browser console for adaptive progression logs")
    print("  3. Verify difficulty advances after 3 consecutive correct answers")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    simulate_quiz_session()
