#!/usr/bin/env python3
"""Quick test of explanation quality eval with just 2 samples."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from evals.run_explanation_quality_eval import ExplanationQualityEvaluator, test_explanation_quality

def main():
    print("\n" + "=" * 80)
    print("QUICK TEST: Explanation Quality Eval (2 samples)")
    print("=" * 80)

    try:
        evaluator = ExplanationQualityEvaluator()
        print("✅ Claude API client initialized successfully\n")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        sys.exit(1)

    # Test just 2 samples from one skill
    print("Testing quad.solve.by_factoring (easy) with 2 samples...\n")

    result = test_explanation_quality(
        skill_id="quad.solve.by_factoring",
        difficulty="easy",
        n_samples=2,
        evaluator=evaluator
    )

    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)

    print(f"\nAverage Scores:")
    for criterion, score in result['average_scores'].items():
        print(f"  {criterion.replace('_', ' ').title()}: {score:.2f}/10")

    print(f"\nPass Rate: {result['pass_rate'] * 100:.0f}%")

    # Show individual results
    print("\n" + "-" * 80)
    print("Individual Evaluations:")
    print("-" * 80)
    for r in result['results']:
        print(f"\nSeed {r['seed']}: {r['stem']}")
        print(f"  Average: {r['scores']['average']:.2f}/10")
        print(f"  Strengths: {r['strengths'][:100]}...")
        print(f"  Weaknesses: {r['weaknesses'][:100]}...")

    print("\n" + "=" * 80)
    print("✅ Test completed successfully!")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
