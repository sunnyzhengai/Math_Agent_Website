#!/usr/bin/env python3
"""
Test the upgraded Oracle Agent that uses Claude API.

This test verifies that the Oracle can solve problems independently
rather than just trusting the answer key.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from engine.templates import generate_item
from agentic.agents.oracle import OracleAgent


def test_oracle_with_correct_answer():
    """Test Oracle with a correctly generated question."""
    print("Test 1: Oracle with correctly generated question")
    print("-" * 60)

    # Generate a vertex question (should be correct after our fix)
    item = generate_item("quad.standard.vertex", "easy", seed=0)

    print(f"Question: {item['stem']}")
    print(f"\nChoices:")
    for choice in item['choices']:
        marker = "✓" if choice['id'] == item['solution_choice_id'] else " "
        print(f"  {choice['id']}. {choice['text']} {marker}")

    print(f"\nSystem's answer: {item['solution_choice_id']}")

    # Test Oracle
    try:
        oracle = OracleAgent()
        oracle_answer = oracle.choose(item)
        print(f"Oracle's answer: {oracle_answer}")

        if oracle_answer == item['solution_choice_id']:
            print("✅ Oracle agrees with system answer")
            return True
        else:
            print("❌ Oracle disagrees with system answer!")
            print("   This could mean the system's answer is wrong.")
            return False
    except ValueError as e:
        print(f"⚠️  API key not configured: {e}")
        print("   Set ANTHROPIC_API_KEY environment variable to test Oracle.")
        return None


def test_oracle_with_wrong_answer():
    """Test Oracle with an intentionally wrong answer key."""
    print("\n\nTest 2: Oracle with intentionally wrong answer key")
    print("-" * 60)

    # Generate a question
    item = generate_item("quad.standard.vertex", "easy", seed=1)

    print(f"Question: {item['stem']}")
    print(f"\nChoices:")
    for choice in item['choices']:
        marker = "✓" if choice['id'] == item['solution_choice_id'] else " "
        print(f"  {choice['id']}. {choice['text']} {marker}")

    # Deliberately corrupt the answer key
    original_answer = item['solution_choice_id']
    wrong_choices = [c['id'] for c in item['choices'] if c['id'] != original_answer]
    item['solution_choice_id'] = wrong_choices[0]

    print(f"\nSystem's answer (deliberately wrong): {item['solution_choice_id']}")
    print(f"Correct answer: {original_answer}")

    # Test Oracle
    try:
        oracle = OracleAgent()
        oracle_answer = oracle.choose(item)
        print(f"Oracle's answer: {oracle_answer}")

        if oracle_answer == original_answer:
            print("✅ Oracle found the correct answer (ignoring wrong system answer)")
            return True
        elif oracle_answer == item['solution_choice_id']:
            print("❌ Oracle trusted the wrong system answer")
            return False
        else:
            print("❌ Oracle gave a different wrong answer")
            return False
    except ValueError as e:
        print(f"⚠️  API key not configured: {e}")
        print("   Set ANTHROPIC_API_KEY environment variable to test Oracle.")
        return None


def main():
    """Run all Oracle tests."""
    print("=" * 60)
    print("ORACLE AGENT UPGRADE TEST")
    print("=" * 60)
    print()

    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("⚠️  WARNING: ANTHROPIC_API_KEY not set")
        print("   The Oracle Agent needs this to call Claude API.")
        print("   Tests will use fallback mode (trust answer key).")
        print()

    results = []

    # Run tests
    result1 = test_oracle_with_correct_answer()
    results.append(("Correct answer test", result1))

    result2 = test_oracle_with_wrong_answer()
    results.append(("Wrong answer detection", result2))

    # Summary
    print("\n\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for name, result in results:
        if result is True:
            print(f"✅ {name}: PASS")
        elif result is False:
            print(f"❌ {name}: FAIL")
        else:
            print(f"⚠️  {name}: SKIPPED (no API key)")
    print()

    # Exit code
    if any(r is False for _, r in results):
        sys.exit(1)
    elif all(r is None for _, r in results):
        print("⚠️  All tests skipped. Set ANTHROPIC_API_KEY to run full tests.")
        sys.exit(2)
    else:
        print("✅ All tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
