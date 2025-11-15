#!/usr/bin/env python3
"""
Vertex Form - Question Generator

Generates 8 templates for completing the square and vertex form.
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
        variation = str(random.randint(1, 20))
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


# Template 1: Complete the square for x² + bx (b even, b > 0)
def template_1():
    """Complete the square for x² + bx"""
    b = random.choice([2, 4, 6, 8, 10])  # Even values
    half_b = b // 2
    c = half_b ** 2

    question = f"Complete the square: x² + {b}x + ___ = (x + ___)²"
    correct_answer = f"{c}, {half_b}"

    # Wrong answers
    wrong_answers = [
        f"{b}, {b}",  # Used b instead of (b/2)²
        f"{c + 1}, {half_b}",  # Off by one on c
        f"{c}, {b}",  # Wrong value for h
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 2: Complete the square for x² - bx (b even, b > 0)
def template_2():
    """Complete the square for x² - bx"""
    b = random.choice([2, 4, 6, 8, 10])
    half_b = b // 2
    c = half_b ** 2

    question = f"Complete the square: x² - {b}x + ___ = (x - ___)²"
    correct_answer = f"{c}, {half_b}"

    # Wrong answers
    wrong_answers = [
        f"{b}, {b}",
        f"{c + 1}, {half_b}",
        f"{c}, {-half_b}",  # Wrong sign - used -h instead of h
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 3: What value completes the square: x² + bx
def template_3():
    """Find the value that completes the square"""
    b = random.choice([2, 4, 6, 8, 10])
    half_b = b // 2
    c = half_b ** 2

    question = f"What value completes the square for x² + {b}x?"
    correct_answer = str(c)

    # Wrong answers
    wrong_answers = [
        str(b),  # Used b instead of (b/2)²
        str(half_b),  # Used b/2 instead of (b/2)²
        str(c + 1),  # Off by one
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 4: What value completes the square: x² - bx
def template_4():
    """Find the value that completes the square"""
    b = random.choice([2, 4, 6, 8, 10])
    half_b = b // 2
    c = half_b ** 2

    question = f"What value completes the square for x² - {b}x?"
    correct_answer = str(c)

    # Wrong answers
    wrong_answers = [
        str(b),
        str(half_b),
        str(c - 1) if c > 1 else str(c + 2),
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 5: y = x² + bx + c → y = (x + h)² + k
def template_5():
    """Convert to vertex form with positive b and c"""
    b = random.choice([2, 4, 6, 8, 10])
    c = random.randint(1, 8)

    half_b = b // 2
    h = half_b  # For x² + bx, h = b/2
    k = c - (half_b ** 2)  # k = c - (b/2)²

    question = f"Rewrite in vertex form: y = x² + {b}x + {c}"
    correct_answer = f"y = (x + {h})² + {k}"

    # Wrong answers
    wrong_answers = [
        f"y = (x + {h})² + {c}",  # Didn't subtract (b/2)²
        f"y = (x - {h})² + {k}",  # Wrong sign on h
        f"y = (x + {b})² + {k}",  # Used b instead of b/2
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 6: y = x² - bx + c → y = (x - h)² + k
def template_6():
    """Convert to vertex form with negative b"""
    b = random.choice([2, 4, 6, 8, 10])
    c = random.randint(1, 8)

    half_b = b // 2
    h = half_b
    k = c - (half_b ** 2)

    question = f"Rewrite in vertex form: y = x² - {b}x + {c}"
    correct_answer = f"y = (x - {h})² + {k}"

    # Wrong answers
    wrong_answers = [
        f"y = (x - {h})² + {c}",
        f"y = (x + {h})² + {k}",  # Wrong sign
        f"y = (x - {b})² + {k}",
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 7: y = x² + bx - c → y = (x + h)² + k
def template_7():
    """Convert to vertex form with positive b, negative c"""
    b = random.choice([2, 4, 6, 8, 10])
    c = random.randint(1, 8)

    half_b = b // 2
    h = half_b
    k = -c - (half_b ** 2)  # k = -c - (b/2)²

    question = f"Rewrite in vertex form: y = x² + {b}x - {c}"
    correct_answer = f"y = (x + {h})² + {k}"

    # Wrong answers
    wrong_answers = [
        f"y = (x + {h})² - {c}",
        f"y = (x - {h})² + {k}",
        f"y = (x + {h})² + {-c}",  # Forgot to subtract (b/2)²
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices


# Template 8: y = x² - bx - c → y = (x - h)² + k
def template_8():
    """Convert to vertex form with negative b and c"""
    b = random.choice([2, 4, 6, 8, 10])
    c = random.randint(1, 8)

    half_b = b // 2
    h = half_b
    k = -c - (half_b ** 2)

    question = f"Rewrite in vertex form: y = x² - {b}x - {c}"
    correct_answer = f"y = (x - {h})² + {k}"

    # Wrong answers
    wrong_answers = [
        f"y = (x - {h})² - {c}",
        f"y = (x + {h})² + {k}",
        f"y = (x - {b})² + {k}",
    ]

    correct_letter, choices = generate_choices_simple(correct_answer, wrong_answers)
    return question, correct_letter, choices
