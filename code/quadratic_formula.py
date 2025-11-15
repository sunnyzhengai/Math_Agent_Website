#!/usr/bin/env python3
"""
Quadratic Formula - Question Generator

Generates 12 templates for quadratic formula and discriminant.
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
        variation = str(random.randint(1, 50))
        if variation not in seen:
            unique_wrong.append(variation)
            seen.add(variation)

    wrong_answers = unique_wrong[:3]
    all_choices = [correct_answer] + wrong_answers
    random.shuffle(all_choices)

    correct_index = all_choices.index(correct_answer)
    correct_letter = chr(65 + correct_index)

    return correct_letter, all_choices


def find_quadratic_with_perfect_discriminant(sign_b, sign_c):
    """Find coefficients where discriminant is a perfect square"""
    for attempt in range(100):
        a = random.randint(1, 5)
        b = random.randint(2, 8)
        c = random.randint(1, 8)

        discriminant = b * b - 4 * a * c

        if discriminant > 0 and int(math.sqrt(discriminant)) ** 2 == discriminant:
            return a, b, c, discriminant

    # Fallback to known good values
    return 1, 5, 6, 1  # x² + 5x + 6, discriminant = 25 - 24 = 1


# Template 1: Solve ax² + bx + c = 0 (perfect square discriminant)
def template_1():
    """Solve using quadratic formula with perfect square discriminant"""
    a, b, c, disc = find_quadratic_with_perfect_discriminant(1, 1)

    sqrt_disc = int(math.sqrt(disc))
    x1 = (-b + sqrt_disc) / (2 * a)
    x2 = (-b - sqrt_disc) / (2 * a)

    # Format solutions
    if x1 == int(x1) and x2 == int(x2):
        if x1 == x2:
            correct_answer = f"x = {int(x1)}"
        else:
            correct_answer = f"x = {int(x1)} or x = {int(x2)}"
    else:
        correct_answer = f"x = ({-b} ± √{disc})/{2*a}"

    question = f"Solve using the quadratic formula: {a}x² + {b}x + {c} = 0"

    wrong_answers = [
        f"x = ({-b} ± √{b})/{2*a}",  # Wrong discriminant
        f"x = ({b} ± √{disc})/{2*a}",  # Forgot negative on b
        f"x = ({-b} ± √{disc})/{a}",  # Forgot 2 in denominator
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 2: Solve ax² - bx + c = 0
def template_2():
    """Solve with negative b coefficient"""
    a, b, c, disc = find_quadratic_with_perfect_discriminant(-1, 1)

    sqrt_disc = int(math.sqrt(disc))

    question = f"Solve using the quadratic formula: {a}x² - {b}x + {c} = 0"
    correct_answer = f"x = ({b} ± √{disc})/{2*a}"

    wrong_answers = [
        f"x = ({-b} ± √{disc})/{2*a}",
        f"x = ({b} ± √{b})/{2*a}",
        f"x = ({b} ± √{disc})/{a}",
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 3: Solve ax² + bx - c = 0
def template_3():
    """Solve with negative c coefficient"""
    a = random.randint(1, 3)
    b = random.randint(2, 6)
    c = random.randint(1, 6)

    discriminant = b * b + 4 * a * c  # Note: +4ac since c is subtracted

    question = f"Solve using the quadratic formula: {a}x² + {b}x - {c} = 0"
    correct_answer = f"x = ({-b} ± √{discriminant})/{2*a}"

    wrong_answers = [
        f"x = ({-b} ± √{b*b - 4*a*c})/{2*a}",  # Wrong discriminant sign
        f"x = ({b} ± √{discriminant})/{2*a}",
        f"x = ({-b} ± √{discriminant})/{a}",
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 4: Solve with non-perfect discriminant ≤ 20
def template_4():
    """Solve with discriminant ≤ 20, non-perfect square"""
    a = random.randint(1, 3)
    b = random.randint(3, 7)
    c = random.randint(1, 5)

    discriminant = b * b - 4 * a * c

    # Ensure it's non-perfect and positive and ≤ 20
    while discriminant <= 0 or discriminant > 20 or int(math.sqrt(discriminant)) ** 2 == discriminant:
        c = random.randint(1, 5)
        discriminant = b * b - 4 * a * c

    question = f"Solve using the quadratic formula: {a}x² + {b}x + {c} = 0"
    correct_answer = f"x = ({-b} ± √{discriminant})/{2*a}"

    wrong_answers = [
        f"x = ({-b} ± √{b})/{2*a}",
        f"x = ({b} ± √{discriminant})/{2*a}",
        f"x = ({-b} ± √{discriminant})/{a}",
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 5: What is the discriminant of ax² + bx + c = 0?
def template_5():
    """Compute discriminant"""
    a = random.randint(1, 5)
    b = random.randint(2, 8)
    c = random.randint(1, 8)

    discriminant = b * b - 4 * a * c

    question = f"What is the discriminant of {a}x² + {b}x + {c} = 0?"
    correct_answer = str(discriminant)

    wrong_answers = [
        str(b * b + 4 * a * c),  # Added instead of subtracted
        str(b * b - 2 * a * c),  # Forgot the 4
        str(discriminant + 1) if discriminant >= 0 else str(discriminant - 1),
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 6: What is the discriminant of ax² - bx - c = 0?
def template_6():
    """Compute discriminant with negative coefficients"""
    a = random.randint(1, 5)
    b = random.randint(2, 8)
    c = random.randint(1, 8)

    discriminant = b * b + 4 * a * c  # Note: + because both b and c are negated

    question = f"What is the discriminant of {a}x² - {b}x - {c} = 0?"
    correct_answer = str(discriminant)

    wrong_answers = [
        str(b * b - 4 * a * c),
        str(b * b + 2 * a * c),
        str(discriminant - 1),
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 7: Given discriminant = 25, how many real solutions?
def template_7():
    """Interpret positive discriminant"""
    disc = random.choice([4, 9, 16, 25, 36])

    question = f"If the discriminant = {disc}, how many real solutions does the equation have?"
    correct_answer = "2 real solutions"

    wrong_answers = [
        "1 real solution",
        "0 real solutions",
        "2 complex solutions",
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 8: Given discriminant = 0, how many real solutions?
def template_8():
    """Interpret zero discriminant"""
    question = "If the discriminant = 0, how many real solutions does the equation have?"
    correct_answer = "1 real solution"

    wrong_answers = [
        "2 real solutions",
        "0 real solutions",
        "2 complex solutions",
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 9: Given discriminant = -5, how many real solutions?
def template_9():
    """Interpret negative discriminant"""
    disc = random.choice([-1, -4, -5, -9, -10])

    question = f"If the discriminant = {disc}, how many real solutions does the equation have?"
    correct_answer = "0 real solutions"

    wrong_answers = [
        "2 real solutions",
        "1 real solution",
        "infinitely many solutions",
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 10: What discriminant means 2 real solutions?
def template_10():
    """Discriminant condition for 2 real solutions"""
    question = "For ax² + bx + c = 0 to have 2 real solutions, the discriminant must be:"
    correct_answer = "b² - 4ac > 0"

    wrong_answers = [
        "b² - 4ac = 0",
        "b² - 4ac < 0",
        "b² - 4ac ≥ 0",
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 11: Simplify with discriminant = 48
def template_11():
    """Simplify radical in quadratic formula solution"""
    b = random.randint(2, 6)
    a = random.randint(1, 3)
    discriminant = 48  # 48 = 16 × 3, so √48 = 4√3

    question = f"Simplify: x = ({-b} ± √48)/{2*a}"
    correct_answer = f"x = ({-b} ± 4√3)/{2*a}"

    wrong_answers = [
        f"x = ({-b} ± 6√2)/{2*a}",  # Wrong simplification
        f"x = ({-b} ± √48)/{2*a}",  # Didn't simplify
        f"x = ({-b} ± 2√12)/{2*a}",  # Partial simplification
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 12: Simplify with discriminant = 50
def template_12():
    """Simplify radical in quadratic formula solution"""
    b = random.randint(2, 6)
    a = random.randint(1, 3)
    discriminant = 50  # 50 = 25 × 2, so √50 = 5√2

    question = f"Simplify: x = ({-b} ± √50)/{2*a}"
    correct_answer = f"x = ({-b} ± 5√2)/{2*a}"

    wrong_answers = [
        f"x = ({-b} ± 7√1)/{2*a}",
        f"x = ({-b} ± √50)/{2*a}",
        f"x = ({-b} ± 2√25)/{2*a}",
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices
