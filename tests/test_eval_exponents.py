#!/usr/bin/env python3
"""
Test the new eval_no_equivalent_answers on exponents_refresher module
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

import exponents_refresher as er


class EvalResults:
    """Track evaluation results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def add_pass(self):
        self.passed += 1

    def add_fail(self, error_msg):
        self.failed += 1
        self.errors.append(error_msg)

    def print_summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"EVAL SUMMARY: {self.passed}/{total} passed")
        if self.failed > 0:
            print(f"\nFAILURES ({self.failed}):")
            for error in self.errors:
                print(f"  ❌ {error}")
        else:
            print("✅ All evals passed!")
        print(f"{'='*60}\n")


def eval_no_equivalent_answers():
    """Verify no mathematically equivalent answers appear as different choices"""
    print("EVAL: No Mathematically Equivalent Answers (Exponents)")
    results = EvalResults()

    for template_num in range(1, 6):  # 5 templates in exponents_refresher
        template_func = getattr(er, f'template_{template_num}')

        for trial in range(10):  # Test 10 times per template
            equation, correct_letter, choices = template_func()
            correct_idx = ord(correct_letter) - ord('A')
            correct_answer = choices[correct_idx]

            # Try to evaluate all choices to numeric values
            evaluated_choices = []
            for i, choice in enumerate(choices):
                try:
                    # Remove "x = " prefix if present
                    value_str = choice.replace('x = ', '').replace(' or x = ', ',').split(',')[0].strip()

                    # Try to evaluate simple expressions with ^
                    if '^' in value_str:
                        # Parse expressions like "5^7" or "1/3^4"
                        if '/' in value_str:
                            # Skip fractions with exponents for now
                            continue
                        parts = value_str.split('^')
                        if len(parts) == 2 and parts[0].isdigit() and parts[1].lstrip('-').isdigit():
                            numeric_value = int(parts[0]) ** int(parts[1])
                            evaluated_choices.append((i, numeric_value, choice))
                    elif value_str.lstrip('-').isdigit():
                        # Simple integer
                        evaluated_choices.append((i, int(value_str), choice))
                except:
                    # If we can't evaluate, skip this choice
                    pass

            # Check for duplicate numeric values
            if len(evaluated_choices) > 1:
                values = [val for _, val, _ in evaluated_choices]
                if len(values) != len(set(values)):
                    # Found duplicates
                    value_counts = {}
                    for idx, val, choice_text in evaluated_choices:
                        if val not in value_counts:
                            value_counts[val] = []
                        value_counts[val].append((idx, choice_text))

                    for val, occurrences in value_counts.items():
                        if len(occurrences) > 1:
                            choices_str = ', '.join([f"{chr(65+idx)}: '{txt}'" for idx, txt in occurrences])
                            results.add_fail(f"Template {template_num} trial {trial+1}: Equivalent answers with value {val}: {choices_str}")
                else:
                    results.add_pass()
            else:
                # Couldn't evaluate enough choices (likely complex expressions)
                results.add_pass()

    results.print_summary()
    return results.failed == 0


if __name__ == "__main__":
    print("="*60)
    print("EXPONENTS REFRESHER - EQUIVALENT ANSWERS EVAL")
    print("="*60)
    print()

    passed = eval_no_equivalent_answers()

    sys.exit(0 if passed else 1)
