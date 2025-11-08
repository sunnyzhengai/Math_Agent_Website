#!/usr/bin/env python3
"""Test the enhanced solution explanation system."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from engine.templates import generate_item
from engine.grader import grade_response


def test_correct_answer():
    """Test explanation for correct answer."""
    print("=" * 70)
    print("TEST 1: Correct Answer")
    print("=" * 70)

    item = generate_item("quad.standard.vertex", "easy", seed=0)
    print(f"\nQuestion: {item['stem']}")
    print(f"\nChoices:")
    for choice in item['choices']:
        print(f"  {choice['id']}. {choice['text']}")

    # Grade correct answer
    result = grade_response(item, item['solution_choice_id'])
    print(f"\n✓ Selected correct answer: {item['solution_choice_id']}")
    print(f"\nExplanation:")
    print(result['explanation'])
    print("\n" + "=" * 70)
    return result['correct']


def test_wrong_answer():
    """Test detailed explanation for wrong answer."""
    print("\n" + "=" * 70)
    print("TEST 2: Wrong Answer (Should get detailed step-by-step solution)")
    print("=" * 70)

    item = generate_item("quad.standard.vertex", "easy", seed=0)
    print(f"\nQuestion: {item['stem']}")
    print(f"\nChoices:")
    for choice in item['choices']:
        marker = "✓" if choice['id'] == item['solution_choice_id'] else ""
        print(f"  {choice['id']}. {choice['text']} {marker}")

    # Select a wrong answer (any choice that's not the solution)
    wrong_choice = next(c['id'] for c in item['choices'] if c['id'] != item['solution_choice_id'])

    # Grade wrong answer
    result = grade_response(item, wrong_choice)
    print(f"\n✗ Selected wrong answer: {wrong_choice}")
    print(f"\nDetailed Explanation:")
    print(result['explanation'])
    print("\n" + "=" * 70)
    return not result['correct']  # Should be False (incorrect)


def test_vertex_form():
    """Test explanation for vertex form question."""
    print("\n" + "=" * 70)
    print("TEST 3: Vertex Form Question")
    print("=" * 70)

    item = generate_item("quad.graph.vertex", "easy", seed=0)
    print(f"\nQuestion: {item['stem']}")
    print(f"\nChoices:")
    for choice in item['choices']:
        print(f"  {choice['id']}. {choice['text']}")

    # Select a wrong answer
    wrong_choice = next(c['id'] for c in item['choices'] if c['id'] != item['solution_choice_id'])

    # Grade wrong answer
    result = grade_response(item, wrong_choice)
    print(f"\n✗ Selected wrong answer: {wrong_choice}")
    print(f"\nDetailed Explanation:")
    print(result['explanation'])
    print("\n" + "=" * 70)
    return not result['correct']


def main():
    """Run all tests."""
    print("\n" + "🧪 TESTING ENHANCED SOLUTION EXPLANATIONS" + "\n")

    tests = [
        ("Correct answer feedback", test_correct_answer),
        ("Wrong answer detailed solution", test_wrong_answer),
        ("Vertex form explanation", test_vertex_form),
    ]

    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n❌ TEST FAILED: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")

    all_passed = all(passed for _, passed in results)
    print("\n" + ("✅ All tests passed!" if all_passed else "❌ Some tests failed"))
    print("=" * 70 + "\n")

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
