#!/usr/bin/env python3
"""
Operations with Radicals - Question Generator

Generates 4 templates for operations with radicals.
Following patterns from Phase 1 with lessons from SPEC_ERRORS_TO_AVOID.md applied.
"""

import random


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


# Template 1: Add like radicals: a√n + b√n
def template_1():
    """Add like radicals"""
    a = random.randint(1, 8)
    b = random.randint(1, 8)
    n = random.choice([2, 3, 5, 7])  # Common radicals

    result = a + b

    question = f"{a}√{n} + {b}√{n}"
    correct_answer = f"{result}√{n}"

    # Wrong answers - common mistakes
    wrong_answers = [
        f"{a + b}√{2 * n}",  # Added under radical too
        f"{result + 1}√{n}",  # Coefficient off by one
        f"{a}√{n} + {b}√{n}",  # Didn't combine
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 2: Multiply binomials with radicals: (a + √n)(a - √n) [difference of squares]
def template_2():
    """Multiply using difference of squares pattern"""
    a = random.randint(2, 5)
    n = random.randint(2, 10)

    # (a + √n)(a - √n) = a² - n
    result = a * a - n

    question = f"({a} + √{n})({a} - √{n})"
    correct_answer = str(result)

    # Wrong answers - common mistakes
    wrong_answers = [
        str(a * a + n),  # Added instead of subtracted
        f"{a * a} - √{n}",  # Forgot to square the radical
        str(result + 1) if result > 0 else str(result - 1),  # Off by one
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 3: Rationalize denominator: a/√n
def template_3():
    """Rationalize denominator with single radical"""
    a = random.randint(2, 8)
    n = random.choice([2, 3, 5, 6, 7])  # Common radicals

    question = f"{a}/√{n}"
    correct_answer = f"{a}√{n}/{n}"

    # Wrong answers - common mistakes
    wrong_answers = [
        f"{a}/√{n}",  # Didn't rationalize
        f"√{n}/{a}",  # Flipped
        f"{a}√{n}",  # Forgot denominator
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 4: Rationalize denominator: a/(b + √n) [conjugate method]
def template_4():
    """Rationalize denominator with binomial using conjugate"""
    a = random.randint(2, 8)
    b = random.randint(2, 5)
    n = random.randint(2, 10)

    # Result: a(b - √n)/(b² - n)
    denominator = b * b - n

    # Ensure denominator is positive and not zero
    while denominator <= 0:
        b = random.randint(2, 5)
        n = random.randint(2, 10)
        denominator = b * b - n

    question = f"{a}/({b} + √{n})"

    # Simplified form
    if denominator == 1:
        correct_answer = f"{a * b} - {a}√{n}"
    else:
        correct_answer = f"({a * b} - {a}√{n})/{denominator}"

    # Wrong answers - common mistakes
    wrong_answers = [
        f"{a}/({b} + √{n})",  # Didn't rationalize
        f"({a * b} + {a}√{n})/{denominator}",  # Wrong sign on radical
        f"{a}({b} - √{n})",  # Forgot to square denominator
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices
