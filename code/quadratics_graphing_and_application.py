#!/usr/bin/env python3
"""
Graphing and Application - Question Generator

Generates 10 templates for graphing and application problems.
Following patterns from Phase 1 with lessons from SPEC_ERRORS_TO_AVOID.md applied.
"""

import random
import math


def generate_choices_simple(correct_answer, wrong_answers):
    """
    Generate 4 multiple choice options (1 correct + 3 wrong).
    Shuffle them and return (correct_letter, [A, B, C, D])
    """
    unique_wrong = []
    seen = {correct_answer}
    for ans in wrong_answers:
        if ans not in seen:
            unique_wrong.append(ans)
            seen.add(ans)

    while len(unique_wrong) < 3:
        variation = str(random.randint(1, 20))
        if variation not in seen:
            unique_wrong.append(variation)
            seen.add(variation)

    wrong_answers = unique_wrong[:3]
    all_choices = [correct_answer] + wrong_answers
    random.shuffle(all_choices)

    correct_index = all_choices.index(correct_answer)
    correct_letter = chr(65 + correct_index)

    return correct_letter, all_choices


# Template 1: Find x-intercepts of y = x² - n (n perfect square)
def template_1():
    """Find x-intercepts with perfect square"""
    perfect_squares = [4, 9, 16, 25, 36, 49, 64, 81, 100]
    n = random.choice(perfect_squares)
    root = int(math.sqrt(n))

    question = f"Find the x-intercepts of y = x² - {n}"
    correct_answer = f"x = ±{root}"

    wrong_answers = [
        f"x = {root}",
        f"x = -{root}",
        f"x = ±{root + 1}",
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 2: Find x-intercepts of y = x² - n (n ≤ 20, non-perfect)
def template_2():
    """Find x-intercepts with non-perfect square"""
    perfect_squares = {4, 9, 16}
    n = random.randint(2, 20)
    while n in perfect_squares:
        n = random.randint(2, 20)

    question = f"Find the x-intercepts of y = x² - {n}"
    correct_answer = f"x = ±√{n}"

    wrong_answers = [
        f"x = √{n}",
        f"x = -√{n}",
        f"x = ±{n}",
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 3: Find x-intercepts of y = x² + bx + c (discriminant perfect square)
def template_3():
    """Find x-intercepts using quadratic with perfect discriminant"""
    # Use factored form (x - p)(x - q) to ensure integer roots
    p = random.randint(1, 5)
    q = random.randint(-5, -1)

    b = -(p + q)
    c = p * q

    question = f"Find the x-intercepts of y = x² + {b}x + {c}"

    if p > abs(q):
        correct_answer = f"x = {p} or x = {q}"
    else:
        correct_answer = f"x = {q} or x = {p}"

    wrong_answers = [
        f"x = {p} or x = {-q}",
        f"x = {-p} or x = {q}",
        f"x = {-p} or x = {-q}",
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 4: Find x-intercepts of y = ax² + bx + c
def template_4():
    """Find x-intercepts with a ≠ 1"""
    a = random.randint(2, 5)
    # Use values that give nice roots
    p = random.randint(1, 4)
    q = random.randint(-4, -1)

    # For a(x - p)(x - q) = ax² - a(p+q)x + apq
    b = -a * (p + q)
    c = a * p * q

    question = f"Find the x-intercepts of y = {a}x² + {b}x + {c}"

    if p > abs(q):
        correct_answer = f"x = {p} or x = {q}"
    else:
        correct_answer = f"x = {q} or x = {p}"

    wrong_answers = [
        f"x = {p * a} or x = {q * a}",
        f"x = {p} or x = {-q}",
        f"x = {-p} or x = {q}",
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 5: √n is between what two integers?
def template_5():
    """Estimate square root"""
    perfect_squares = {4, 9, 16, 25, 36, 49}
    n = random.randint(2, 50)
    while n in perfect_squares or int(math.sqrt(n)) ** 2 == n:
        n = random.randint(2, 50)

    lower = int(math.sqrt(n))
    upper = lower + 1

    question = f"√{n} is between which two consecutive integers?"
    correct_answer = f"between {lower} and {upper}"

    wrong_answers = [
        f"between {lower - 1} and {lower}",
        f"between {upper} and {upper + 1}",
        f"between {lower} and {lower + 2}",
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 6: Approximate √n to 1 decimal place
def template_6():
    """Approximate square root to 1 decimal"""
    n = random.randint(2, 20)
    while int(math.sqrt(n)) ** 2 == n:
        n = random.randint(2, 20)

    actual = math.sqrt(n)
    approx = round(actual, 1)

    question = f"Approximate √{n} to 1 decimal place"
    correct_answer = str(approx)

    wrong_answers = [
        str(round(approx + 0.1, 1)),
        str(round(approx - 0.1, 1)) if approx > 0.1 else str(round(approx + 0.2, 1)),
        str(int(actual)),
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 7: If b² - 4ac > 0, how many x-intercepts?
def template_7():
    """Discriminant > 0 interpretation for graphing"""
    question = "If b² - 4ac > 0, how many x-intercepts does the parabola have?"
    correct_answer = "2 x-intercepts"

    wrong_answers = [
        "1 x-intercept",
        "0 x-intercepts",
        "infinitely many x-intercepts",
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 8: If b² - 4ac = 0, how many x-intercepts?
def template_8():
    """Discriminant = 0 interpretation for graphing"""
    question = "If b² - 4ac = 0, how many x-intercepts does the parabola have?"
    correct_answer = "1 x-intercept"

    wrong_answers = [
        "2 x-intercepts",
        "0 x-intercepts",
        "infinitely many x-intercepts",
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 9: If b² - 4ac < 0, how many x-intercepts?
def template_9():
    """Discriminant < 0 interpretation for graphing"""
    question = "If b² - 4ac < 0, how many x-intercepts does the parabola have?"
    correct_answer = "0 x-intercepts"

    wrong_answers = [
        "2 x-intercepts",
        "1 x-intercept",
        "infinitely many x-intercepts",
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 10: For discriminant = 49, how many x-intercepts?
def template_10():
    """Given specific discriminant value"""
    disc = random.choice([0, 25, 36, 49, -4, -9])

    question = f"For y = ax² + bx + c, if the discriminant = {disc}, how many x-intercepts does the graph have?"

    if disc > 0:
        correct_answer = "2 x-intercepts"
    elif disc == 0:
        correct_answer = "1 x-intercept"
    else:
        correct_answer = "0 x-intercepts"

    wrong_answers = [
        "2 x-intercepts" if correct_answer != "2 x-intercepts" else "1 x-intercept",
        "1 x-intercept" if correct_answer != "1 x-intercept" else "0 x-intercepts",
        "0 x-intercepts" if correct_answer != "0 x-intercepts" else "2 x-intercepts",
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices
