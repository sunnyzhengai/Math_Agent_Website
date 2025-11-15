#!/usr/bin/env python3
"""
Simplifying Radicals - Question Generator

Generates 4 templates for simplifying radicals.
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
        variation = f"{random.randint(2, 10)}√{random.randint(2, 10)}"
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


def find_largest_perfect_square_factor(n):
    """Find the largest perfect square factor of n"""
    factors = []
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % (i * i) == 0:
            factors.append(i * i)
    return max(factors) if factors else 1


# Template 1: Simplify √n (n has perfect square factor)
def template_1():
    """Simplify √n where n has a perfect square factor"""
    # Choose numbers with perfect square factors
    # Examples: 50 = 25×2, 72 = 36×2, 48 = 16×3, etc.
    numbers_with_factors = [
        (50, 5, 2),   # √50 = 5√2
        (72, 6, 2),   # √72 = 6√2
        (48, 4, 3),   # √48 = 4√3
        (45, 3, 5),   # √45 = 3√5
        (32, 4, 2),   # √32 = 4√2
        (75, 5, 3),   # √75 = 5√3
        (98, 7, 2),   # √98 = 7√2
        (27, 3, 3),   # √27 = 3√3
        (18, 3, 2),   # √18 = 3√2
        (20, 2, 5),   # √20 = 2√5
        (28, 2, 7),   # √28 = 2√7
        (80, 4, 5),   # √80 = 4√5
    ]

    n, coefficient, radical = random.choice(numbers_with_factors)

    question = f"√{n}"
    correct_answer = f"{coefficient}√{radical}"

    # Wrong answers - common mistakes
    wrong_answers = [
        f"√{n}",  # Didn't simplify
        f"{coefficient + 1}√{radical}",  # Coefficient off by one
        f"{coefficient}√{radical + 1}",  # Radical off by one
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 2: Simplify ³√(n·x^m) (cube root with variables)
def template_2():
    """Simplify cube root with variables"""
    # Cube root values: 8=2³, 27=3³, 54=27×2, 128=64×2
    cube_options = [
        (8, 2, 1),     # ³√(8x^3) = 2x
        (27, 3, 1),    # ³√(27x^3) = 3x
        (8, 2, 2),     # ³√(8x^6) = 2x²
        (27, 3, 2),    # ³√(27x^6) = 3x²
    ]

    n, coef, x_power = random.choice(cube_options)
    m = x_power * 3  # Ensure m is divisible by 3

    question = f"³√({n}x^{m})"

    if x_power == 1:
        correct_answer = f"{coef}x"
    else:
        correct_answer = f"{coef}x^{x_power}"

    # Wrong answers - common mistakes
    wrong_answers = [
        f"{coef + 1}x^{x_power}" if x_power > 1 else f"{coef + 1}x",  # Coefficient off
        f"{coef}x^{m}",  # Didn't simplify power
        f"³√({n}x^{m})",  # Didn't simplify at all
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 3: Multiply and simplify √a × √b
def template_3():
    """Multiply and simplify radicals"""
    # Choose values where a×b has a nice simplification
    products = [
        (2, 8, 4),     # √2 × √8 = √16 = 4
        (3, 3, 3),     # √3 × √3 = 3
        (5, 5, 5),     # √5 × √5 = 5
        (2, 2, 2),     # √2 × √2 = 2
        (4, 9, 6),     # √4 × √9 = 2 × 3 = 6
        (2, 18, 6),    # √2 × √18 = √36 = 6
        (3, 12, 6),    # √3 × √12 = √36 = 6
    ]

    a, b, result = random.choice(products)

    question = f"√{a} × √{b}"
    correct_answer = str(result)

    # Wrong answers - common mistakes
    wrong_answers = [
        f"√{a + b}",  # Added under radical
        str(result + 1),  # Off by one
        f"√{a * b}",  # Left unsimplified
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 4: Divide and simplify √a / √b
def template_4():
    """Divide and simplify radicals"""
    # Choose values where a/b simplifies nicely
    divisions = [
        (8, 2, 2),     # √8 / √2 = √4 = 2
        (12, 3, 2),    # √12 / √3 = √4 = 2
        (18, 2, 3),    # √18 / √2 = √9 = 3
        (50, 2, 5),    # √50 / √2 = √25 = 5
        (32, 2, 4),    # √32 / √2 = √16 = 4
        (45, 5, 3),    # √45 / √5 = √9 = 3
        (72, 2, 6),    # √72 / √2 = √36 = 6
    ]

    a, b, result = random.choice(divisions)

    question = f"√{a} / √{b}"
    correct_answer = str(result)

    # Wrong answers - common mistakes
    wrong_answers = [
        f"√{a // b}" if a // b != result else str(result + 1),  # Divided values first
        str(result + 1),  # Off by one
        f"√{a - b}" if a > b else str(result + 2),  # Subtracted under radical
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices
