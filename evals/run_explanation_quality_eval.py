#!/usr/bin/env python3
"""
Explanation Quality Evaluation

Uses Claude API to evaluate the pedagogical quality of solution explanations.
Assesses completeness, accuracy, clarity, pedagogical value, and specificity.

This eval ensures our explanations provide genuine educational value,
not just generic templates.
"""

import os
import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.templates import generate_item
from engine.grader import grade_response

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("Warning: anthropic package not installed. Install with: pip install anthropic")


def load_config() -> Dict[str, Any]:
    """Load evaluation configuration."""
    config_path = Path(__file__).parent / "explanation_quality_eval.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


class ExplanationQualityEvaluator:
    """Evaluates explanation quality using Claude API."""

    def __init__(self):
        """Initialize the evaluator with Claude client."""
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not set. This eval requires Claude API access.\n"
                "Set the API key: export ANTHROPIC_API_KEY=your_key_here"
            )

        if not ANTHROPIC_AVAILABLE:
            raise ImportError("anthropic package not installed")

        self.client = Anthropic(api_key=api_key)

    def evaluate_explanation(
        self,
        question_stem: str,
        correct_answer: str,
        student_answer: str,
        explanation: str,
        skill_id: str
    ) -> Dict[str, Any]:
        """
        Use Claude API to evaluate an explanation's quality.

        Args:
            question_stem: The question text
            correct_answer: The correct answer
            student_answer: What the student selected (wrong)
            explanation: The explanation to evaluate
            skill_id: The skill being tested

        Returns:
            Dict with scores for each criterion and overall assessment
        """
        prompt = f"""You are an expert math educator evaluating the quality of a solution explanation.

**Question:** {question_stem}

**Correct Answer:** {correct_answer}
**Student Selected:** {student_answer} (incorrect)

**Explanation Provided:**
{explanation}

**Skill Being Tested:** {skill_id}

---

Please evaluate this explanation on the following criteria, giving a score from 1-10 for each:

1. **Completeness** (1-10): Does it show actual step-by-step work?
   - 1-3: Just says "do X" without showing how
   - 4-6: Shows some steps but missing key work
   - 7-8: Shows most steps with actual computation
   - 9-10: Complete step-by-step with all work shown

2. **Accuracy** (1-10): Are all mathematical steps correct?
   - 1-3: Contains mathematical errors
   - 4-6: Minor errors or confusing notation
   - 7-8: Mathematically correct with minor presentation issues
   - 9-10: Perfectly accurate mathematics

3. **Clarity** (1-10): Is the explanation easy to understand?
   - 1-3: Confusing, hard to follow
   - 4-6: Understandable but could be clearer
   - 7-8: Clear and well-organized
   - 9-10: Exceptionally clear and intuitive

4. **Pedagogical Value** (1-10): Does it explain WHY and identify common mistakes?
   - 1-3: No explanation of reasoning or mistakes
   - 4-6: Mentions mistakes but doesn't explain why
   - 7-8: Explains reasoning and common errors
   - 9-10: Deep insight into why mistakes happen

5. **Specificity** (1-10): Does it use actual values or generic templates?
   - 1-3: Generic templates like "factor the equation"
   - 4-6: Mix of specific and generic
   - 7-8: Uses actual values throughout
   - 9-10: Every step shows actual computation

Respond ONLY with a JSON object in this format:
{{
  "completeness": <score>,
  "accuracy": <score>,
  "clarity": <score>,
  "pedagogical_value": <score>,
  "specificity": <score>,
  "reasoning": "<brief explanation of scores>",
  "strengths": "<what the explanation does well>",
  "weaknesses": "<what could be improved>"
}}

Respond with ONLY the JSON, no other text."""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                temperature=0.0,
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse JSON response
            response_text = response.content[0].text.strip()

            # Try to extract JSON if there's extra text
            if response_text.startswith('{') and response_text.endswith('}'):
                result = json.loads(response_text)
            else:
                # Try to find JSON in the response
                import re
                json_match = re.search(r'\{[^}]+\}', response_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group(0))
                else:
                    raise ValueError(f"Could not parse JSON from response: {response_text}")

            # Calculate average score
            scores = [
                result.get('completeness', 0),
                result.get('accuracy', 0),
                result.get('clarity', 0),
                result.get('pedagogical_value', 0),
                result.get('specificity', 0)
            ]
            result['average_score'] = sum(scores) / len(scores)

            return result

        except Exception as e:
            print(f"Warning: Failed to evaluate explanation: {e}")
            return {
                "completeness": 0,
                "accuracy": 0,
                "clarity": 0,
                "pedagogical_value": 0,
                "specificity": 0,
                "average_score": 0,
                "reasoning": f"Evaluation failed: {str(e)}",
                "strengths": "N/A",
                "weaknesses": "N/A",
                "error": str(e)
            }


def test_explanation_quality(
    skill_id: str,
    difficulty: str,
    n_samples: int,
    evaluator: ExplanationQualityEvaluator
) -> Dict[str, Any]:
    """
    Test explanation quality for a skill/difficulty combination.

    Args:
        skill_id: Skill to test
        difficulty: Difficulty level
        n_samples: Number of questions to test
        evaluator: ExplanationQualityEvaluator instance

    Returns:
        Dict with test results and scores
    """
    results = []
    errors = []

    for seed in range(n_samples):
        try:
            # Generate item
            item = generate_item(skill_id, difficulty, seed=seed)

            # Get a wrong answer (first choice that's not the solution)
            wrong_choice = next(
                c['id'] for c in item['choices']
                if c['id'] != item['solution_choice_id']
            )

            # Grade to get explanation
            grade_result = grade_response(item, wrong_choice, detailed=True)

            # Evaluate explanation quality
            evaluation = evaluator.evaluate_explanation(
                question_stem=item['stem'],
                correct_answer=grade_result['solution_choice_id'],
                student_answer=wrong_choice,
                explanation=grade_result['explanation'],
                skill_id=skill_id
            )

            results.append({
                "seed": seed,
                "item_id": item.get('item_id', f'seed_{seed}'),
                "stem": item['stem'][:100] + "..." if len(item['stem']) > 100 else item['stem'],
                "scores": {
                    "completeness": evaluation['completeness'],
                    "accuracy": evaluation['accuracy'],
                    "clarity": evaluation['clarity'],
                    "pedagogical_value": evaluation['pedagogical_value'],
                    "specificity": evaluation['specificity'],
                    "average": evaluation['average_score']
                },
                "reasoning": evaluation.get('reasoning', ''),
                "strengths": evaluation.get('strengths', ''),
                "weaknesses": evaluation.get('weaknesses', ''),
                "passed": evaluation['average_score'] >= 7.0
            })

        except Exception as e:
            errors.append({
                "seed": seed,
                "error": str(e),
                "skill_id": skill_id,
                "difficulty": difficulty
            })

    # Calculate aggregate scores
    if results:
        avg_scores = {
            "completeness": sum(r['scores']['completeness'] for r in results) / len(results),
            "accuracy": sum(r['scores']['accuracy'] for r in results) / len(results),
            "clarity": sum(r['scores']['clarity'] for r in results) / len(results),
            "pedagogical_value": sum(r['scores']['pedagogical_value'] for r in results) / len(results),
            "specificity": sum(r['scores']['specificity'] for r in results) / len(results),
            "average": sum(r['scores']['average'] for r in results) / len(results)
        }
    else:
        avg_scores = {k: 0.0 for k in ['completeness', 'accuracy', 'clarity', 'pedagogical_value', 'specificity', 'average']}

    pass_rate = sum(1 for r in results if r['passed']) / len(results) if results else 0.0

    return {
        "skill_id": skill_id,
        "difficulty": difficulty,
        "n_tested": len(results),
        "n_errors": len(errors),
        "average_scores": avg_scores,
        "pass_rate": pass_rate,
        "results": results,
        "errors": errors
    }


def main():
    """Run the explanation quality evaluation."""
    print("\n" + "=" * 80)
    print("EXPLANATION QUALITY EVALUATION")
    print("=" * 80)

    # Load config
    config = load_config()
    print(f"\nConfiguration: {config['name']}")
    print(f"Description: {config['description'].strip()}")

    # Initialize evaluator
    try:
        evaluator = ExplanationQualityEvaluator()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)

    # Run tests
    all_results = []
    skills = config.get('skills', [])
    difficulties = config.get('difficulties', [])
    n_samples = config['test_config']['n_samples']

    print(f"\nTesting {len(skills)} skills × {len(difficulties)} difficulties × {n_samples} samples")
    print(f"Total: {len(skills) * len(difficulties) * n_samples} explanations to evaluate\n")

    for skill in skills:
        for difficulty in difficulties:
            print(f"Testing {skill} ({difficulty})...", end=" ", flush=True)

            result = test_explanation_quality(skill, difficulty, n_samples, evaluator)
            all_results.append(result)

            avg = result['average_scores']['average']
            status = "✅" if avg >= config['thresholds']['min_avg_score'] else "❌"
            print(f"{status} Avg: {avg:.2f}/10")

    # Generate summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    overall_avg = sum(r['average_scores']['average'] for r in all_results) / len(all_results)
    overall_completeness = sum(r['average_scores']['completeness'] for r in all_results) / len(all_results)
    overall_accuracy = sum(r['average_scores']['accuracy'] for r in all_results) / len(all_results)
    overall_clarity = sum(r['average_scores']['clarity'] for r in all_results) / len(all_results)
    overall_pedagogical = sum(r['average_scores']['pedagogical_value'] for r in all_results) / len(all_results)
    overall_specificity = sum(r['average_scores']['specificity'] for r in all_results) / len(all_results)

    print(f"\nOverall Average Score: {overall_avg:.2f}/10")
    print(f"  Completeness:       {overall_completeness:.2f}/10")
    print(f"  Accuracy:           {overall_accuracy:.2f}/10")
    print(f"  Clarity:            {overall_clarity:.2f}/10")
    print(f"  Pedagogical Value:  {overall_pedagogical:.2f}/10")
    print(f"  Specificity:        {overall_specificity:.2f}/10")

    # Check thresholds
    thresholds = config['thresholds']
    print("\nThreshold Checks:")
    checks = [
        ("Average Score", overall_avg, thresholds['min_avg_score']),
        ("Completeness", overall_completeness, thresholds['min_completeness']),
        ("Accuracy", overall_accuracy, thresholds['min_accuracy']),
        ("Clarity", overall_clarity, thresholds['min_clarity']),
        ("Specificity", overall_specificity, thresholds['min_specificity'])
    ]

    all_passed = True
    for name, value, threshold in checks:
        status = "✅" if value >= threshold else "❌"
        print(f"  {status} {name}: {value:.2f} (min: {threshold})")
        if value < threshold:
            all_passed = False

    # Save detailed report
    report_path = Path(__file__).parent / "explanation_quality_report.jsonl"
    with open(report_path, 'w') as f:
        for result in all_results:
            f.write(json.dumps(result) + '\n')

    print(f"\n📄 Detailed report saved to: {report_path}")

    # Final status
    print("\n" + "=" * 80)
    if all_passed:
        print("✅ EXPLANATION QUALITY EVAL PASSED")
    else:
        print("❌ EXPLANATION QUALITY EVAL FAILED")
        print("\nSome explanations need improvement. Review the report for details.")
    print("=" * 80 + "\n")

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
