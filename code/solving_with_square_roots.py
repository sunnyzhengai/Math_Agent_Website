#!/usr/bin/env python3
"""
Solving Equations Using Radicals - Question Generator

Generates 8 templates for solving equations with square roots.
Following patterns from quadratic_equations_by_completing_the_square.py
with lessons from SPEC_ERRORS_TO_AVOID.md applied.
"""

import random
import math


def is_perfect_square(n):
    """Check if n is a perfect square"""
    if n < 0:
        return False
    sqrt_n = int(math.sqrt(n))
    return sqrt_n * sqrt_n == n


def format_radical(n):
    """Format √n in simplified form"""
    if is_perfect_square(n):
        return str(int(math.sqrt(n)))
    return f"√{n}"


def generate_choices_simple(correct_answer, wrong_answers):
    """
    Generate 4 multiple choice options (1 correct + 3 wrong).
    Shuffle them and return (correct_letter, [A, B, C, D])

    Avoiding Error #4: Ensure all choices are unique
    """
    # Filter out duplicates from wrong answers
    unique_wrong = []
    seen = {correct_answer}
    for ans in wrong_answers:
        if ans not in seen:
            unique_wrong.append(ans)
            seen.add(ans)

    # If we don't have 3 unique wrong answers, generate more variations
    while len(unique_wrong) < 3:
        # Add a variation (this shouldn't happen with good wrong answer generation)
        variation = f"x = {random.randint(-10, 10)}"
        if variation not in seen:
            unique_wrong.append(variation)
            seen.add(variation)

    # Take first 3 unique wrong answers
    wrong_answers = unique_wrong[:3]

    # Combine and shuffle
    all_choices = [correct_answer] + wrong_answers
    random.shuffle(all_choices)

    # Find correct letter
    correct_index = all_choices.index(correct_answer)
    correct_letter = chr(65 + correct_index)  # A, B, C, D

    return correct_letter, all_choices


# Template 1: x² = n (perfect square)
def template_1():
    """x² = n where n is a perfect square"""
    perfect_squares = [4, 9, 16, 25, 36, 49, 64, 81, 100]
    n = random.choice(perfect_squares)

    sqrt_n = int(math.sqrt(n))

    equation = f"x² = {n}"
    correct_answer = f"x = ±{sqrt_n}"

    # Wrong answers - common mistakes
    wrong_answers = [
        f"x = {sqrt_n}",  # Forgot negative solution
        f"x = -{sqrt_n}",  # Forgot positive solution
        f"x = ±{n}",  # Didn't take square root
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return equation, correct_letter, choices


# Template 2: x² = n (non-perfect square)
def template_2():
    """x² = n where n is NOT a perfect square (n ≤ 20)"""
    non_perfect = [2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20]
    n = random.choice(non_perfect)

    equation = f"x² = {n}"
    correct_answer = f"x = ±√{n}"

    # Wrong answers
    wrong_answers = [
        f"x = √{n}",  # Forgot negative
        f"x = -√{n}",  # Forgot positive
        f"x = ±{n}",  # Didn't take square root
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return equation, correct_letter, choices


# Template 3: (x - a)² = n (perfect square)
def template_3():
    """(x - a)² = n (perfect square, a > 0, n > 0)"""
    a = random.randint(1, 8)
    perfect_squares = [4, 9, 16, 25, 36, 49, 64, 81]
    n = random.choice(perfect_squares)
    sqrt_n = int(math.sqrt(n))

    # Solutions: x - a = ±√n → x = a ± √n
    x1 = a - sqrt_n
    x2 = a + sqrt_n

    # Ensure solutions are ordered (smaller first)
    if x1 > x2:
        x1, x2 = x2, x1

    equation = f"(x - {a})² = {n}"
    correct_answer = f"x = {x1} or x = {x2}"

    # Wrong answers
    wrong_answers = [
        f"x = {x2}",  # Only positive solution
        f"x = {x1}",  # Only negative solution
        f"x = {a - n} or x = {a + n}",  # Didn't take square root
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return equation, correct_letter, choices


# Template 4: (x + a)² = n (perfect square)
def template_4():
    """(x + a)² = n (perfect square, a > 0, n > 0)"""
    a = random.randint(1, 8)
    perfect_squares = [4, 9, 16, 25, 36, 49, 64, 81]
    n = random.choice(perfect_squares)
    sqrt_n = int(math.sqrt(n))

    # Solutions: x + a = ±√n → x = -a ± √n
    x1 = -a - sqrt_n
    x2 = -a + sqrt_n

    # Ensure solutions are ordered
    if x1 > x2:
        x1, x2 = x2, x1

    equation = f"(x + {a})² = {n}"
    correct_answer = f"x = {x1} or x = {x2}"

    # Wrong answers
    wrong_answers = [
        f"x = {x2}",  # Only one solution
        f"x = {x1}",  # Only other solution
        f"x = {a - sqrt_n} or x = {a + sqrt_n}",  # Sign error
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return equation, correct_letter, choices


# Template 5: (x - a)² = n (non-perfect square)
def template_5():
    """(x - a)² = n (non-perfect square, a > 0, n ≤ 20)"""
    a = random.randint(1, 8)
    non_perfect = [2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20]
    n = random.choice(non_perfect)

    equation = f"(x - {a})² = {n}"
    correct_answer = f"x = {a} ± √{n}"

    # Wrong answers
    wrong_answers = [
        f"x = {a} + √{n}",  # Only positive
        f"x = {a} - √{n}",  # Only negative
        f"x = -{a} ± √{n}",  # Sign error on a
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return equation, correct_letter, choices


# Template 6: (x + a)² = n (non-perfect square)
def template_6():
    """(x + a)² = n (non-perfect square, a > 0, n ≤ 20)"""
    a = random.randint(1, 8)
    non_perfect = [2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20]
    n = random.choice(non_perfect)

    equation = f"(x + {a})² = {n}"
    correct_answer = f"x = -{a} ± √{n}"

    # Wrong answers
    wrong_answers = [
        f"x = -{a} + √{n}",  # Only positive
        f"x = -{a} - √{n}",  # Only negative
        f"x = {a} ± √{n}",  # Sign error
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return equation, correct_letter, choices


# Template 7: √(x + a) = x - b (extraneous roots)
def template_7():
    """√(x + a) = x - b where one solution is extraneous"""
    # We need to carefully construct this to have one valid, one extraneous root
    # Let's use a = 3, and construct from a known solution
    # If x = 6 is the valid solution: √(6+3) = 6-b → √9 = 6-b → 3 = 6-b → b = 3

    # Using x = 6 as valid solution
    x_valid = random.choice([4, 5, 6, 7, 8])
    a = 5
    # √(x+a) = x-b  → at x=x_valid: √(x_valid+a) = x_valid-b
    sqrt_val = int(math.sqrt(x_valid + a)) if is_perfect_square(x_valid + a) else None

    # Adjust 'a' to make it work
    while sqrt_val is None or sqrt_val >= x_valid:
        a = random.randint(1, 6)
        if is_perfect_square(x_valid + a):
            sqrt_val = int(math.sqrt(x_valid + a))
        else:
            sqrt_val = None

    b = x_valid - sqrt_val

    # The other "solution" from squaring: x+a = (x-b)² → x+a = x² - 2bx + b²
    # → x² - (2b+1)x + (b² - a) = 0
    # This gives us the extraneous root

    equation = f"√(x + {a}) = x - {b}"
    correct_answer = f"x = {x_valid}"

    # Wrong answers - including the extraneous root
    wrong_answers = [
        f"x = {x_valid - 1}",
        f"x = {x_valid + 1}",
        "No solution",
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return equation, correct_letter, choices


# Template 8: √(x - a) = x - b (extraneous roots)
def template_8():
    """√(x - a) = x - b where one solution is extraneous"""
    # Similar to template 7 but with (x - a)

    x_valid = random.choice([5, 6, 7, 8, 9])
    a = random.randint(1, 4)

    # Ensure x_valid - a is a perfect square
    while not is_perfect_square(x_valid - a):
        a = random.randint(1, 4)

    sqrt_val = int(math.sqrt(x_valid - a))
    b = x_valid - sqrt_val

    equation = f"√(x - {a}) = x - {b}"
    correct_answer = f"x = {x_valid}"

    # Wrong answers
    wrong_answers = [
        f"x = {x_valid - 1}",
        f"x = {x_valid + 2}",
        "No solution",
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return equation, correct_letter, choices
