#!/usr/bin/env python3
"""
Understanding Radicals - Question Generator

Generates 4 templates for basic radical understanding.
Following patterns from Phase 1 with lessons from SPEC_ERRORS_TO_AVOID.md applied.
"""

import random
import math


def generate_choices_simple(correct_answer, wrong_answers):
    """
    Generate 4 multiple choice options (1 correct + 3 wrong).
    Shuffle them and return (correct_letter, [A, B, C, D])

    Avoiding Error #4: Ensure all choices are unique
    """
    # Filter out duplicates
    unique_wrong = []
    seen = {correct_answer}
    for ans in wrong_answers:
        if ans not in seen:
            unique_wrong.append(ans)
            seen.add(ans)

    # Ensure we have 3 unique wrong answers
    while len(unique_wrong) < 3:
        variation = str(random.randint(10, 200))
        if variation not in seen:
            unique_wrong.append(variation)
            seen.add(variation)

    wrong_answers = unique_wrong[:3]

    # Combine and shuffle
    all_choices = [correct_answer] + wrong_answers
    random.shuffle(all_choices)

    # Find correct letter
    correct_index = all_choices.index(correct_answer)
    correct_letter = chr(65 + correct_index)

    return correct_letter, all_choices


# Template 1: What is √n? (n is perfect square)
def template_1():
    """Evaluate √n where n is a perfect square"""
    perfect_squares = [4, 9, 16, 25, 36, 49, 64, 81, 100]
    n = random.choice(perfect_squares)

    result = int(math.sqrt(n))

    question = f"What is √{n}?"
    correct_answer = str(result)

    # Wrong answers - common mistakes
    wrong_answers = [
        str(result + 1),  # Off by one
        str(result - 1) if result > 1 else str(result + 2),  # Off by one (other direction)
        str(n // 2) if n // 2 != result else str(result + 3),  # Divide by 2 instead
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 2: Solve x² = n (n is perfect square)
def template_2():
    """Solve x² = n where n is a perfect square"""
    perfect_squares = [4, 9, 16, 25, 36, 49, 64, 81, 100]
    n = random.choice(perfect_squares)

    root = int(math.sqrt(n))

    question = f"Solve: x² = {n}"
    correct_answer = f"x = ±{root}"

    # Wrong answers - common mistakes
    wrong_answers = [
        f"x = {root}",  # Forgot negative solution
        f"x = -{root}",  # Forgot positive solution
        f"x = ±{root + 1}",  # Off by one
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 3: Rewrite ⁿ√(x^m) as a power (convert to rational exponent)
def template_3():
    """Convert radical to rational exponent"""
    # Root index (2 or 3)
    n = random.choice([2, 3])
    # Power (1-6)
    m = random.randint(1, 6)

    # Display format
    if n == 2:
        question = f"Rewrite √(x^{m}) using a rational exponent"
    else:
        question = f"Rewrite ³√(x^{m}) using a rational exponent"

    correct_answer = f"x^({m}/{n})"

    # Wrong answers - common mistakes
    wrong_answers = [
        f"x^({n}/{m})",  # Flipped numerator/denominator
        f"x^{m * n}",  # Multiplied instead
        f"x^({m + n})",  # Added instead
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 4: √n is between what two integers? (n is non-perfect square)
def template_4():
    """Find consecutive integers that √n falls between"""
    # Choose a non-perfect square
    perfect_squares = {4, 9, 16, 25, 36, 49, 64, 81, 100}
    n = random.randint(2, 50)

    # Ensure n is not a perfect square
    while n in perfect_squares or int(math.sqrt(n)) ** 2 == n:
        n = random.randint(2, 50)

    # Find the two consecutive integers
    lower = int(math.sqrt(n))
    upper = lower + 1

    question = f"√{n} is between which two consecutive integers?"
    correct_answer = f"between {lower} and {upper}"

    # Wrong answers - common mistakes
    wrong_answers = [
        f"between {lower - 1} and {lower}",  # Off by one (lower)
        f"between {upper} and {upper + 1}",  # Off by one (upper)
        f"between {lower + 1} and {upper + 1}",  # Both off by one
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices
