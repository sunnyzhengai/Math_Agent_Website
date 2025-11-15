#!/usr/bin/env python3
"""
Formatting and Logic Evaluation Tests

Tests to catch common issues:
1. Missing spaces in LaTeX rendering
2. Multiple correct answers
3. Improper LaTeX syntax
4. Answer choice quality
"""

import sys
import pytest
from pathlib import Path

# Add code directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "code"))

# Import all skill modules
import radicals_exponents_refresher
import radicals_understanding_radicals
import radicals_simplifying_radicals
import radicals_operations_with_radicals
import quadratics_completing_the_square
import quadratics_solving_with_square_roots
import quadratics_vertex_form
import quadratics_quadratic_formula
import quadratics_graphing_and_application


# ============================================================================
# Test Configuration
# ============================================================================

ALL_MODULES = [
    radicals_exponents_refresher,
    radicals_understanding_radicals,
    radicals_simplifying_radicals,
    radicals_operations_with_radicals,
    quadratics_completing_the_square,
    quadratics_solving_with_square_roots,
    quadratics_vertex_form,
    quadratics_quadratic_formula,
    quadratics_graphing_and_application,
]


def get_all_templates():
    """Get all template functions from all modules."""
    templates = []
    for module in ALL_MODULES:
        module_name = module.__name__
        # Find all template functions
        for attr_name in dir(module):
            if attr_name.startswith('template_'):
                func = getattr(module, attr_name)
                templates.append((module_name, attr_name, func))
    return templates


# ============================================================================
# Test 1: No Missing Spaces (LaTeX \text{} usage)
# ============================================================================

def test_no_missing_spaces_in_questions():
    """Ensure questions with text use \\text{} for proper spacing"""
    issues = []

    for module_name, template_name, template_func in get_all_templates():
        # Generate a few samples to check
        for _ in range(3):
            try:
                equation, correct_letter, choices = template_func()

                # Check if equation has words without \text{}
                # Look for common patterns like "Is12" or "aperfect"
                equation_no_latex = equation.replace('\\text{', '').replace('}', '')

                # Check for concatenated words (letters followed immediately by digits or vice versa)
                import re
                # Pattern: lowercase letter followed by uppercase (e.g., "aperfect")
                if re.search(r'[a-z][A-Z]', equation_no_latex):
                    issues.append(f"{module_name}.{template_name}: Possible missing space in question: {equation}")

                # Pattern: word characters smashed together without spaces
                # Look for "Is12" pattern - letter followed immediately by digit
                if re.search(r'[a-zA-Z]\d', equation) and '\\text{' not in equation:
                    issues.append(f"{module_name}.{template_name}: Text without \\text{{}} may lose spaces: {equation}")

            except Exception as e:
                issues.append(f"{module_name}.{template_name}: Error generating question: {e}")

    if issues:
        pytest.fail("Found spacing issues:\n" + "\n".join(issues))


def test_no_missing_spaces_in_answers():
    """Ensure answer choices with text use \\text{} for proper spacing"""
    issues = []

    for module_name, template_name, template_func in get_all_templates():
        # Generate a few samples
        for _ in range(3):
            try:
                equation, correct_letter, choices = template_func()

                for i, choice in enumerate(choices):
                    # Check for common text patterns without \text{}
                    # e.g., "Yes,36=7" should be "Yes, 36 = 7"
                    if any(word in str(choice).lower() for word in ['yes', 'no', 'because', 'is', 'not']):
                        if '\\text{' not in str(choice):
                            issues.append(f"{module_name}.{template_name}: Answer choice {i+1} has text without \\text{{}}: {choice}")

            except Exception as e:
                issues.append(f"{module_name}.{template_name}: Error generating answers: {e}")

    if issues:
        pytest.fail("Found answer spacing issues:\n" + "\n".join(issues))


# ============================================================================
# Test 2: No Multiple Correct Answers
# ============================================================================

def test_unique_correct_answer():
    """Ensure only one answer is correct (no duplicates or logically equivalent answers)"""
    issues = []

    for module_name, template_name, template_func in get_all_templates():
        for trial in range(5):
            try:
                equation, correct_letter, choices = template_func()

                # Get the correct answer
                correct_index = ord(correct_letter) - ord('A')
                correct_answer = choices[correct_index]

                # Check for exact duplicates
                if choices.count(correct_answer) > 1:
                    issues.append(
                        f"{module_name}.{template_name}: Duplicate correct answer '{correct_answer}' appears {choices.count(correct_answer)} times"
                    )

                # Check for similar answers (e.g., "No" and "No, but...")
                # Both could be considered correct
                for i, choice in enumerate(choices):
                    if i == correct_index:
                        continue

                    # Check if wrong answer starts with same word as correct answer
                    # e.g., both start with "No"
                    correct_first_word = str(correct_answer).split()[0] if ' ' in str(correct_answer) else str(correct_answer)
                    choice_first_word = str(choice).split()[0] if ' ' in str(choice) else str(choice)

                    # Remove LaTeX formatting for comparison
                    correct_clean = correct_first_word.replace('\\text{', '').replace('}', '').strip(',')
                    choice_clean = choice_first_word.replace('\\text{', '').replace('}', '').strip(',')

                    if correct_clean.lower() == choice_clean.lower():
                        # Both answers start with same Yes/No - could be ambiguous
                        issues.append(
                            f"{module_name}.{template_name}: Possibly ambiguous - Correct: '{correct_answer}', Also has: '{choice}'"
                        )
                        break

            except Exception as e:
                issues.append(f"{module_name}.{template_name}: Error in trial {trial}: {e}")

    if issues:
        pytest.fail("Found multiple correct answer issues:\n" + "\n".join(issues))


# ============================================================================
# Test 3: Proper LaTeX Syntax
# ============================================================================

def test_latex_syntax():
    """Ensure LaTeX syntax is correct (braces balanced, proper commands)"""
    issues = []

    for module_name, template_name, template_func in get_all_templates():
        for _ in range(3):
            try:
                equation, correct_letter, choices = template_func()

                # Check equation LaTeX syntax
                if equation.count('{') != equation.count('}'):
                    issues.append(f"{module_name}.{template_name}: Unbalanced braces in question: {equation}")

                # Check for proper exponent formatting
                # Should be a^{n} not a^n for multi-char exponents
                import re
                # Pattern: ^( followed by anything that's not a single digit
                if re.search(r'\^\(-', equation):
                    # Negative exponent should use braces: ^{-n} not ^(-n)
                    if not re.search(r'\^\{-\d+\}', equation):
                        issues.append(f"{module_name}.{template_name}: Negative exponent should use {{}} not (): {equation}")

                # Check all choices
                for i, choice in enumerate(choices):
                    if str(choice).count('{') != str(choice).count('}'):
                        issues.append(f"{module_name}.{template_name}: Unbalanced braces in choice {i+1}: {choice}")

            except Exception as e:
                issues.append(f"{module_name}.{template_name}: Error checking syntax: {e}")

    if issues:
        pytest.fail("Found LaTeX syntax issues:\n" + "\n".join(issues))


# ============================================================================
# Test 4: Answer Quality
# ============================================================================

def test_answer_quality():
    """Ensure answer choices are distinct and reasonable"""
    issues = []

    for module_name, template_name, template_func in get_all_templates():
        for _ in range(3):
            try:
                equation, correct_letter, choices = template_func()

                # Check for exact duplicates among all choices
                unique_choices = set(choices)
                if len(unique_choices) < len(choices):
                    duplicates = [c for c in choices if choices.count(c) > 1]
                    issues.append(f"{module_name}.{template_name}: Duplicate answer choices: {duplicates}")

                # Check that we have 4 choices
                if len(choices) != 4:
                    issues.append(f"{module_name}.{template_name}: Expected 4 choices, got {len(choices)}")

                # Verify correct_letter is valid (A, B, C, or D)
                if correct_letter not in ['A', 'B', 'C', 'D']:
                    issues.append(f"{module_name}.{template_name}: Invalid correct_letter: {correct_letter}")

            except Exception as e:
                issues.append(f"{module_name}.{template_name}: Error checking quality: {e}")

    if issues:
        pytest.fail("Found answer quality issues:\n" + "\n".join(issues))


# ============================================================================
# Test 5: No Repeated Questions Within Template
# ============================================================================

def test_no_immediate_duplicates():
    """Ensure the same question isn't generated twice in a row (check randomness)"""
    issues = []

    for module_name, template_name, template_func in get_all_templates():
        try:
            # Generate 20 questions and check for duplicates
            questions = []
            for _ in range(20):
                equation, _, _ = template_func()
                questions.append(equation)

            # Check for any duplicates
            unique_questions = set(questions)
            if len(unique_questions) < len(questions) * 0.8:  # Allow some overlap, but not too much
                duplicate_count = len(questions) - len(unique_questions)
                issues.append(
                    f"{module_name}.{template_name}: Low variety - {duplicate_count} duplicates in 20 generations"
                )

        except Exception as e:
            issues.append(f"{module_name}.{template_name}: Error checking duplicates: {e}")

    if issues:
        pytest.fail("Found duplicate generation issues:\n" + "\n".join(issues))


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
