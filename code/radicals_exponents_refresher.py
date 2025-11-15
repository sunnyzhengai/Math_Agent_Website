#!/usr/bin/env python3
"""
Exponents Refresher - Question Generator

Generates 5 templates for basic exponent rules.
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
        variation = f"{random.randint(10, 200)}"
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


# Template 1: a^m × a^n (product rule)
def template_1():
    """Evaluate a^m × a^n using product rule"""
    a = random.randint(2, 5)
    m = random.randint(2, 6)
    n = random.randint(2, 6)

    # Correct: a^(m+n)
    result = a ** (m + n)

    question = f"{a}^{m} × {a}^{n}"
    correct_answer = str(result)

    # Wrong answers - common mistakes
    wrong_answers = [
        str(a ** (m * n)),  # Multiplied exponents instead of adding
        str(a ** m + a ** n),  # Added the results
        str((a ** m) * (a ** n) // 2) if (a ** m) * (a ** n) > 2 else str(result + 10),  # Off by factor
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 2: a^m / a^n (quotient rule)
def template_2():
    """Evaluate a^m / a^n using quotient rule"""
    a = random.randint(2, 5)
    # Ensure m > n so result is positive exponent
    n = random.randint(2, 4)
    m = random.randint(n + 1, 6)

    # Correct: a^(m-n)
    result = a ** (m - n)

    question = f"{a}^{m} / {a}^{n}"
    correct_answer = str(result)

    # Wrong answers
    wrong_answers = [
        str(a ** (m + n)),  # Added instead of subtracting
        str((a ** m) // (a ** n)) if a ** n != 0 else "1",  # Division error
        str(result + random.randint(1, 10)),  # Off by small amount
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 3: a^(-n) (negative exponent)
def template_3():
    """Simplify a^(-n) using negative exponent rule"""
    a = random.randint(2, 5)
    n = random.randint(2, 4)

    question = f"{a}^{{-{n}}}"
    correct_answer = f"\\frac{{1}}{{{a}^{n}}}"

    # Wrong answers
    wrong_answers = [
        f"-{a}^{n}",  # Made base negative
        f"{a}^{n}",  # Ignored negative
        f"-1/{a}^{n}",  # Made fraction negative
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 4: (a^m)^n (power rule)
def template_4():
    """Evaluate (a^m)^n using power rule"""
    a = random.randint(2, 4)
    m = random.randint(2, 3)
    n = random.randint(2, 3)

    # Correct: a^(m*n)
    result = a ** (m * n)

    question = f"({a}^{m})^{n}"
    correct_answer = str(result)

    # Wrong answers
    wrong_answers = [
        str(a ** (m + n)),  # Added exponents instead of multiplying
        str(result // (a ** m)) if result > a ** m else str(result * 2),  # Divided instead of multiplied
        str(result + random.randint(10, 100)),  # Off by amount
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 5: Is n a perfect square?
def template_5():
    """Recognize perfect squares"""
    import math

    # 50/50 chance of perfect vs non-perfect
    if random.choice([True, False]):
        # Perfect square
        perfect_squares = [4, 9, 16, 25, 36, 49, 64, 81, 100]
        n = random.choice(perfect_squares)
        correct_answer = "Yes"
    else:
        # Non-perfect square
        non_perfect = [6, 8, 10, 12, 15, 18, 20, 24]
        n = random.choice(non_perfect)
        correct_answer = "No"

    question = f"Is {n} a perfect square?"

    # Only 2 possible answers, so we need filler choices
    if correct_answer == "Yes":
        wrong_answers = ["No", f"Yes, {n} = {int(math.sqrt(n)) + 1}²", f"No, √{n} is not an integer"]
    else:
        wrong_answers = ["Yes", f"Yes, {n} = {random.randint(2, 8)}²", f"No, but close to {(int(math.sqrt(n)))**2}"]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices
