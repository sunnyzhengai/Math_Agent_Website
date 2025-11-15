"""
Quadratic Equations by Completing the Square - Template Generator

This module provides 24 different equation templates for generating
quadratic equation practice problems that can be solved by completing the square.

Each template function generates random coefficients and returns:
- equation_string: The equation to display to the student
- correct_answer: Tuple of (x1, x2) solutions
- choices: List of 4 multiple choice options [A, B, C, D]
"""

import random
import math
from fractions import Fraction


def format_coefficient(coef, var='x'):
    """
    Format a coefficient for display.

    Examples:
        format_coefficient(1, 'x') -> 'x'
        format_coefficient(5, 'x') -> '5x'
        format_coefficient(1, 'x²') -> 'x²'
    """
    if coef == 1:
        return var
    return f"{coef}{var}"


def solve_by_completing_square(a, b, c):
    """
    Solves ax² + bx + c = 0 using the completing the square method.

    Args:
        a, b, c: Coefficients of the quadratic equation

    Returns:
        dict: {
            'solutions': (x1, x2) as floats for sorting/comparison,
            'exact_form': tuple of exact representations,
            'discriminant': the discriminant value,
            'a': coefficient a,
            'b': coefficient b
        }
    """
    # Calculate discriminant to ensure real solutions
    discriminant = b**2 - 4*a*c

    if discriminant < 0:
        return None  # No real solutions

    # Using quadratic formula (equivalent to completing the square)
    x1 = (-b + math.sqrt(discriminant)) / (2*a)
    x2 = (-b - math.sqrt(discriminant)) / (2*a)

    # Return detailed info for exact formatting
    return {
        'solutions': tuple(sorted([x1, x2])),
        'discriminant': discriminant,
        'a': a,
        'b': b
    }


def generate_wrong_answers(solution_info):
    """
    Generates 3 plausible wrong answers based on common mistakes
    when completing the square.

    Common mistakes:
    1. Sign error when finding (x + p)²  -> flip sign of b
    2. Forgetting ± when taking square root -> only positive root
    3. Arithmetic errors -> wrong discriminant

    Args:
        solution_info: Dict from solve_by_completing_square

    Returns:
        list: 3 wrong answer formatted tuples
    """
    a = solution_info['a']
    b = solution_info['b']
    disc = solution_info['discriminant']
    x1, x2 = solution_info['solutions']

    wrong_answers = []

    # Mistake 1: Sign error on b (flip the sign when completing square)
    wrong_b = -b  # This is like solving ax² - bx + c instead of ax² + bx + c
    wrong_disc_1 = wrong_b**2 - 4*a*(b**2 - 4*a*0)/(4*a)  # Simplified: just use b²
    # Actually, let's just flip the solutions' signs
    x1_str, x2_str, x1_f, x2_f = format_solution_pair(a, -b, disc)
    wrong_answers.append((x1_str, x2_str, x1_f, x2_f))

    # Mistake 2: Mixed sign error (flip only the negative solution)
    if x1 != x2:
        # Flip the sign of one solution
        x1_str_wrong, x2_str_wrong, x1_f_wrong, x2_f_wrong = format_solution_pair(a, b, disc)
        # Manually create flipped version
        x1_str_flipped = x2_str_wrong.replace('-', 'TEMP').replace('+', '-').replace('TEMP', '+') if '-' in x2_str_wrong or '+' in x2_str_wrong else f"-{x2_str_wrong}" if not x2_str_wrong.startswith('-') else x2_str_wrong[1:]
        wrong_answers.append((x1_str_wrong, x1_str_flipped, x1, -x2))
    else:
        # For repeated roots, create small arithmetic error
        offset = abs(x1) * 0.5 if x1 != 0 else 1
        x1_off_str, x2_off_str, x1_off_f, x2_off_f = format_solution_pair(a, b - int(offset*2*a), disc)
        wrong_answers.append((x1_off_str, x2_off_str, x1_off_f, x2_off_f))

    # Mistake 3: Forget ± (only take positive root)
    positive_root = max(abs(x1), abs(x2))
    # Format as if both solutions are the same positive value
    if is_perfect_square(disc):
        pos_str = format_exact_solution(-abs(b) + int(math.sqrt(disc)), disc, 2*abs(a))
    else:
        # Just use the positive solution string
        _, x2_str_pos, _, x2_f_pos = format_solution_pair(a, b, disc)
        pos_str = x2_str_pos.lstrip('-') if x2_str_pos.startswith('-') else x2_str_pos
        positive_root = abs(x2)

    wrong_answers.append((pos_str, pos_str, positive_root, positive_root))

    return wrong_answers


def is_perfect_square(n):
    """Check if n is a perfect square."""
    if n < 0:
        return False
    sqrt_n = int(math.sqrt(n))
    return sqrt_n * sqrt_n == n


def is_simple_discriminant(discriminant):
    """
    Check if discriminant produces simple answers.

    Returns True if:
    - Discriminant is a perfect square (rational solutions), OR
    - Discriminant is ≤ 20 (simple radical solutions)
    """
    return is_perfect_square(discriminant) or discriminant <= 20


def gcd(a, b):
    """Calculate greatest common divisor."""
    while b:
        a, b = b, a % b
    return abs(a)


def format_exact_solution(numerator, discriminant, denominator):
    """
    Format a single solution in exact form.

    Args:
        numerator: The constant part (-b)
        discriminant: The discriminant value
        denominator: 2a

    Returns:
        str: Formatted solution (integer, fraction, or radical form)
    """
    # Case 1: Perfect square discriminant (rational solution)
    if is_perfect_square(discriminant):
        sqrt_disc = int(math.sqrt(discriminant))

        # Simplified numerator for this solution
        actual_num = numerator + sqrt_disc

        # Check if it simplifies to an integer
        if actual_num % denominator == 0:
            return str(actual_num // denominator)

        # Otherwise show as fraction
        g = gcd(actual_num, denominator)
        num = actual_num // g
        den = denominator // g

        if den == 1:
            return str(num)
        return f"{num}/{den}"

    # Case 2: Non-perfect square (irrational - use radical form)
    else:
        # Simplify the radical
        sqrt_disc = discriminant
        outside = 1

        # Factor out perfect squares from under the radical
        i = 2
        while i * i <= sqrt_disc:
            while sqrt_disc % (i * i) == 0:
                outside *= i
                sqrt_disc //= (i * i)
            i += 1

        # Simplify the fraction part
        g = gcd(gcd(abs(numerator), outside), denominator)
        num = numerator // g
        radical_coef = outside // g
        den = denominator // g

        # Build the string
        parts = []

        # Add constant term
        if num != 0:
            if den == 1:
                parts.append(str(num))
            else:
                parts.append(f"{num}/{den}")

        # Add radical term
        radical_str = f"√{sqrt_disc}" if sqrt_disc != 1 else ""
        if radical_coef == 1 and sqrt_disc == 1:
            radical_part = "1"
        elif radical_coef == 1:
            radical_part = radical_str
        elif sqrt_disc == 1:
            radical_part = str(radical_coef)
        else:
            radical_part = f"{radical_coef}{radical_str}"

        if den != 1:
            radical_part = f"{radical_part}/{den}"

        # Combine
        if len(parts) == 0:
            return radical_part
        elif num > 0:
            return f"{parts[0]} + {radical_part}"
        else:
            return f"{parts[0]} + {radical_part}"


def format_solution_pair(a, b, discriminant):
    """
    Format both solutions using exact form.

    Returns:
        tuple: (x1_str, x2_str, x1_float, x2_float)
    """
    # Calculate float values for sorting
    x1_float = (-b + math.sqrt(discriminant)) / (2*a)
    x2_float = (-b - math.sqrt(discriminant)) / (2*a)

    # Ensure x1 <= x2
    if x1_float > x2_float:
        x1_float, x2_float = x2_float, x1_float
        use_flipped = True
    else:
        use_flipped = False

    # Format exact forms
    if is_perfect_square(discriminant):
        # Rational solutions
        sqrt_disc = int(math.sqrt(discriminant))

        # Two solutions: (-b - sqrt_disc)/(2a) and (-b + sqrt_disc)/(2a)
        num1 = -b - sqrt_disc
        num2 = -b + sqrt_disc
        denom = 2 * a

        # Simplify each fraction
        g1 = gcd(num1, denom)
        g2 = gcd(num2, denom)

        num1_simp = num1 // g1
        denom1_simp = denom // g1

        num2_simp = num2 // g2
        denom2_simp = denom // g2

        # Format as integer or fraction
        if denom1_simp == 1:
            sol1_str = str(num1_simp)
        else:
            sol1_str = f"{num1_simp}/{denom1_simp}"

        if denom2_simp == 1:
            sol2_str = str(num2_simp)
        else:
            sol2_str = f"{num2_simp}/{denom2_simp}"

        # Sort by float value
        if use_flipped:
            x1_str, x2_str = sol1_str, sol2_str
        else:
            x1_str, x2_str = sol2_str, sol1_str

    else:
        # Irrational solutions - use radical form
        sqrt_disc_simplified = discriminant
        outside = 1

        # Simplify radical
        i = 2
        while i * i <= sqrt_disc_simplified:
            while sqrt_disc_simplified % (i * i) == 0:
                outside *= i
                sqrt_disc_simplified //= (i * i)
            i += 1

        # Simplify fractions
        g = gcd(gcd(abs(b), outside), abs(2*a))
        if g == 0:
            g = 1

        num_const = -b // g
        radical_coef = outside // g
        denom = (2*a) // g

        # Build string representations
        if radical_coef == 1:
            radical_str = f"√{sqrt_disc_simplified}"
        else:
            radical_str = f"{radical_coef}√{sqrt_disc_simplified}"

        if denom == 1:
            if num_const == 0:
                x1_str = f"-{radical_str}"
                x2_str = f"{radical_str}"
            else:
                x1_str = f"{num_const} - {radical_str}"
                x2_str = f"{num_const} + {radical_str}"
        else:
            if num_const == 0:
                x1_str = f"-{radical_str}/{denom}"
                x2_str = f"{radical_str}/{denom}"
            else:
                x1_str = f"({num_const} - {radical_str})/{denom}"
                x2_str = f"({num_const} + {radical_str})/{denom}"

    return (x1_str, x2_str, x1_float, x2_float)


def format_choice(solution_info):
    """
    Formats a solution pair as a string for multiple choice display.

    Args:
        solution_info: Either dict from solve_by_completing_square or
                      tuple (x1_str, x2_str, x1_float, x2_float)

    Returns:
        str: Formatted like "x = -5 or x = 2" or "x = (3 + √5)/2 or x = (3 - √5)/2"
    """
    if isinstance(solution_info, dict):
        # Extract from solver output
        a = solution_info['a']
        b = solution_info['b']
        disc = solution_info['discriminant']
        x1_str, x2_str, _, _ = format_solution_pair(a, b, disc)
    elif isinstance(solution_info, tuple) and len(solution_info) == 4:
        # Pre-formatted tuple
        x1_str, x2_str, _, _ = solution_info
    else:
        # Legacy: just float values
        x1, x2 = solution_info
        x1_str = str(int(x1)) if x1 == int(x1) else f"{x1:.2f}"
        x2_str = str(int(x2)) if x2 == int(x2) else f"{x2:.2f}"

    return f"x = {x1_str} or x = {x2_str}"


def generate_choices(correct_solution_info, wrong_answers):
    """
    Generates 4 multiple choice options with correct answer randomly positioned.

    Args:
        correct_solution_info: Dict from solve_by_completing_square
        wrong_answers: List of 3 wrong answer tuples (x1_str, x2_str, x1_float, x2_float)

    Returns:
        tuple: (correct_letter, [choice_A, choice_B, choice_C, choice_D])
    """
    # Format correct answer
    correct_formatted = format_solution_pair(
        correct_solution_info['a'],
        correct_solution_info['b'],
        correct_solution_info['discriminant']
    )

    all_choices = [correct_formatted] + wrong_answers
    random.shuffle(all_choices)

    # Find which position the correct answer is in
    correct_index = all_choices.index(correct_formatted)
    correct_letter = ['A', 'B', 'C', 'D'][correct_index]

    # Format all choices
    formatted_choices = [format_choice(choice) for choice in all_choices]

    return correct_letter, formatted_choices


# Template 1: x² + bx + c = 0 (b > 0, c > 0)
def template_1():
    """x² + bx + c = 0"""
    b = random.randint(1, 8)
    c = random.randint(1, 8)

    # Ensure real solutions and simple discriminants
    disc = b**2 - 4*c
    while disc < 0 or not is_simple_discriminant(disc):
        b = random.randint(1, 8)
        c = random.randint(1, 8)
        disc = b**2 - 4*c

    equation = f"x² + {format_coefficient(b, 'x')} + {c} = 0"
    solution_info = solve_by_completing_square(1, b, c)
    wrong_answers = generate_wrong_answers(solution_info)
    correct_letter, choices = generate_choices(solution_info, wrong_answers)

    return equation, correct_letter, choices


# Template 2: x² - bx + c = 0 (b > 0, c > 0)
def template_2():
    """x² - bx + c = 0"""
    b = random.randint(1, 8)
    c = random.randint(1, 8)

    # Ensure real solutions
    disc = b**2 - 4*c
    while disc < 0 or not is_simple_discriminant(disc):
        b = random.randint(1, 8)
        c = random.randint(1, 8)

        disc = b**2 - 4*c
    equation = f"x² - {format_coefficient(b, 'x')} + {c} = 0"
    solution_info = solve_by_completing_square(1, -b, c)
    wrong_answers = generate_wrong_answers(solution_info)
    correct_letter, choices = generate_choices(solution_info, wrong_answers)

    return equation, correct_letter, choices


# Template 3: x² + bx - c = 0 (b > 0, c > 0)
def template_3():
    """x² + bx - c = 0"""
    b = random.randint(1, 8)
    c = random.randint(1, 8)

    # b² + 4c is always positive, but ensure simple discriminant
    disc = b**2 + 4*c
    while not is_simple_discriminant(disc):
        b = random.randint(1, 8)
        c = random.randint(1, 8)
        disc = b**2 + 4*c

    equation = f"x² + {format_coefficient(b, 'x')} - {c} = 0"
    solution_info = solve_by_completing_square(1, b, -c)
    wrong_answers = generate_wrong_answers(solution_info)
    correct_letter, choices = generate_choices(solution_info, wrong_answers)

    return equation, correct_letter, choices


# Template 4: x² - bx - c = 0 (b > 0, c > 0)
def template_4():
    """x² - bx - c = 0"""
    b = random.randint(1, 8)
    c = random.randint(1, 8)

    # b² + 4c is always positive, but ensure simple discriminant
    disc = b**2 + 4*c
    while not is_simple_discriminant(disc):
        b = random.randint(1, 8)
        c = random.randint(1, 8)
        disc = b**2 + 4*c

    equation = f"x² - {format_coefficient(b, 'x')} - {c} = 0"
    solution_info = solve_by_completing_square(1, -b, -c)
    wrong_answers = generate_wrong_answers(solution_info)
    correct_letter, choices = generate_choices(solution_info, wrong_answers)

    return equation, correct_letter, choices


# Templates 5-8: x² ± c = d ± bx variations
def template_5():
    """x² + c = d + bx (b > 0, c > 0, d > 0)"""
    b = random.randint(1, 8)
    c = random.randint(1, 8)
    d = random.randint(1, 8)

    # Rearrange to standard form: x² - bx + (c - d) = 0
    new_c = c - d

    # Ensure real solutions: b² - 4(c - d) >= 0
    disc = b**2 - 4*new_c
    while disc < 0 or not is_simple_discriminant(disc):
        b = random.randint(1, 8)
        c = random.randint(1, 8)
        d = random.randint(1, 8)
        new_c = c - d

        disc = b**2 - 4*new_c
    equation = f"x² + {c} = {d} + {format_coefficient(b, 'x')}"
    solution_info = solve_by_completing_square(1, -b, new_c)
    wrong_answers = generate_wrong_answers(solution_info)
    correct_letter, choices = generate_choices(solution_info, wrong_answers)

    return equation, correct_letter, choices


def template_6():
    """x² + c = d - bx (b > 0, c > 0, d > 0)"""
    b = random.randint(1, 8)
    c = random.randint(1, 8)
    d = random.randint(1, 8)

    # Rearrange to standard form: x² + bx + (c - d) = 0
    new_c = c - d

    # Ensure real solutions: b² - 4(c - d) >= 0
    disc = b**2 - 4*new_c
    while disc < 0 or not is_simple_discriminant(disc):
        b = random.randint(1, 8)
        c = random.randint(1, 8)
        d = random.randint(1, 8)
        new_c = c - d

        disc = b**2 - 4*new_c
    equation = f"x² + {c} = {d} - {format_coefficient(b, 'x')}"
    solution_info = solve_by_completing_square(1, b, new_c)
    wrong_answers = generate_wrong_answers(solution_info)
    correct_letter, choices = generate_choices(solution_info, wrong_answers)

    return equation, correct_letter, choices


def template_7():
    """x² - c = d - bx (b > 0, c > 0, d > 0)"""
    b = random.randint(1, 8)
    c = random.randint(1, 8)
    d = random.randint(1, 8)

    # Rearrange to standard form: x² + bx + (-c - d) = 0
    new_c = -c - d

    # b² - 4(-c - d) = b² + 4(c + d) always positive, but ensure simple discriminant
    disc = b**2 + 4*(c + d)
    while not is_simple_discriminant(disc):
        b = random.randint(1, 8)
        c = random.randint(1, 8)
        d = random.randint(1, 8)
        new_c = -c - d
        disc = b**2 + 4*(c + d)

    equation = f"x² - {c} = {d} - {format_coefficient(b, 'x')}"
    solution_info = solve_by_completing_square(1, b, new_c)
    wrong_answers = generate_wrong_answers(solution_info)
    correct_letter, choices = generate_choices(solution_info, wrong_answers)

    return equation, correct_letter, choices


def template_8():
    """x² - c = d + bx (b > 0, c > 0, d > 0)"""
    b = random.randint(1, 8)
    c = random.randint(1, 8)
    d = random.randint(1, 8)

    # Rearrange to standard form: x² - bx + (-c - d) = 0
    new_c = -c - d

    # b² - 4(-c - d) = b² + 4(c + d) always positive, so always real solutions

    equation = f"x² - {c} = {d} + {format_coefficient(b, 'x')}"
    solution_info = solve_by_completing_square(1, -b, new_c)
    wrong_answers = generate_wrong_answers(solution_info)
    correct_letter, choices = generate_choices(solution_info, wrong_answers)

    return equation, correct_letter, choices


# Templates 9-16: ax² ± bx ± c = x² ± d variations
def template_9():
    """ax² + bx + c = x² + d (b > 0, c > 0, d > 0)"""
    a = random.randint(2, 5)
    b = random.randint(1, 6)
    c = random.randint(1, 6)
    d = random.randint(1, 6)

    # Rearrange to standard form: (a-1)x² + bx + (c - d) = 0
    new_a = a - 1
    new_c = c - d

    # Ensure real solutions: b² - 4(a-1)(c-d) >= 0
    disc = b**2 - 4*new_a*new_c
    while disc < 0 or not is_simple_discriminant(disc):
        a = random.randint(2, 5)
        b = random.randint(1, 6)
        c = random.randint(1, 6)
        d = random.randint(1, 6)
        new_a = a - 1
        new_c = c - d

        disc = b**2 - 4*new_a*new_c
    equation = f"{format_coefficient(a, 'x²')} + {format_coefficient(b, 'x')} + {c} = x² + {d}"
    solution_info = solve_by_completing_square(new_a, b, new_c)
    wrong_answers = generate_wrong_answers(solution_info)
    correct_letter, choices = generate_choices(solution_info, wrong_answers)

    return equation, correct_letter, choices


def template_10():
    """ax² - bx + c = x² + d (b > 0, c > 0, d > 0)"""
    a = random.randint(2, 5)
    b = random.randint(1, 6)
    c = random.randint(1, 6)
    d = random.randint(1, 6)

    # Rearrange to standard form: (a-1)x² - bx + (c - d) = 0
    new_a = a - 1
    new_c = c - d

    # Ensure real solutions: b² - 4(a-1)(c-d) >= 0
    disc = b**2 - 4*new_a*new_c
    while disc < 0 or not is_simple_discriminant(disc):
        a = random.randint(2, 5)
        b = random.randint(1, 6)
        c = random.randint(1, 6)
        d = random.randint(1, 6)
        new_a = a - 1
        new_c = c - d

        disc = b**2 - 4*new_a*new_c
    equation = f"{format_coefficient(a, 'x²')} - {format_coefficient(b, 'x')} + {c} = x² + {d}"
    solution_info = solve_by_completing_square(new_a, -b, new_c)
    wrong_answers = generate_wrong_answers(solution_info)
    correct_letter, choices = generate_choices(solution_info, wrong_answers)

    return equation, correct_letter, choices


def template_11():
    """ax² + bx - c = x² + d (b > 0, c > 0, d > 0)"""
    a = random.randint(2, 5)
    b = random.randint(1, 6)
    c = random.randint(1, 6)
    d = random.randint(1, 6)

    # Rearrange to standard form: (a-1)x² + bx + (-c - d) = 0
    new_a = a - 1
    new_c = -c - d

    # b² - 4(a-1)(-c-d) = b² + 4(a-1)(c+d) always positive

    equation = f"{format_coefficient(a, 'x²')} + {format_coefficient(b, 'x')} - {c} = x² + {d}"
    solution_info = solve_by_completing_square(new_a, b, new_c)
    wrong_answers = generate_wrong_answers(solution_info)
    correct_letter, choices = generate_choices(solution_info, wrong_answers)

    return equation, correct_letter, choices


def template_12():
    """ax² + bx + c = x² - d (b > 0, c > 0, d > 0)"""
    a = random.randint(2, 5)
    b = random.randint(1, 6)
    c = random.randint(1, 6)
    d = random.randint(1, 6)

    # Rearrange to standard form: (a-1)x² + bx + (c + d) = 0
    new_a = a - 1
    new_c = c + d

    # Ensure real solutions: b² - 4(a-1)(c+d) >= 0
    disc = b**2 - 4*new_a*new_c
    while disc < 0 or not is_simple_discriminant(disc):
        a = random.randint(2, 5)
        b = random.randint(1, 6)
        c = random.randint(1, 6)
        d = random.randint(1, 6)
        new_a = a - 1
        new_c = c + d

        disc = b**2 - 4*new_a*new_c
    equation = f"{format_coefficient(a, 'x²')} + {format_coefficient(b, 'x')} + {c} = x² - {d}"
    solution_info = solve_by_completing_square(new_a, b, new_c)
    wrong_answers = generate_wrong_answers(solution_info)
    correct_letter, choices = generate_choices(solution_info, wrong_answers)

    return equation, correct_letter, choices


def template_13():
    """ax² - bx - c = x² + d (b > 0, c > 0, d > 0)"""
    a = random.randint(2, 5)
    b = random.randint(1, 6)
    c = random.randint(1, 6)
    d = random.randint(1, 6)

    # Rearrange to standard form: (a-1)x² - bx + (-c - d) = 0
    new_a = a - 1
    new_c = -c - d

    # b² - 4(a-1)(-c-d) = b² + 4(a-1)(c+d) always positive

    equation = f"{format_coefficient(a, 'x²')} - {format_coefficient(b, 'x')} - {c} = x² + {d}"
    solution_info = solve_by_completing_square(new_a, -b, new_c)
    wrong_answers = generate_wrong_answers(solution_info)
    correct_letter, choices = generate_choices(solution_info, wrong_answers)

    return equation, correct_letter, choices


def template_14():
    """ax² + bx - c = x² - d (b > 0, c > 0, d > 0)"""
    a = random.randint(2, 5)
    b = random.randint(1, 6)
    c = random.randint(1, 6)
    d = random.randint(1, 6)

    # Rearrange to standard form: (a-1)x² + bx + (-c + d) = 0
    new_a = a - 1
    new_c = -c + d

    # Ensure real solutions
    disc = b**2 - 4*new_a*new_c
    while disc < 0 or not is_simple_discriminant(disc):
        a = random.randint(2, 5)
        b = random.randint(1, 6)
        c = random.randint(1, 6)
        d = random.randint(1, 6)
        new_a = a - 1
        new_c = -c + d

        disc = b**2 - 4*new_a*new_c
    equation = f"{format_coefficient(a, 'x²')} + {format_coefficient(b, 'x')} - {c} = x² - {d}"
    solution_info = solve_by_completing_square(new_a, b, new_c)
    wrong_answers = generate_wrong_answers(solution_info)
    correct_letter, choices = generate_choices(solution_info, wrong_answers)

    return equation, correct_letter, choices


def template_15():
    """ax² - bx - c = x² + d (b > 0, c > 0, d > 0)"""
    # Note: This is duplicate of template_13 per SPEC
    a = random.randint(2, 5)
    b = random.randint(1, 6)
    c = random.randint(1, 6)
    d = random.randint(1, 6)

    # Rearrange to standard form: (a-1)x² - bx + (-c - d) = 0
    new_a = a - 1
    new_c = -c - d

    # b² - 4(a-1)(-c-d) = b² + 4(a-1)(c+d) always positive

    equation = f"{format_coefficient(a, 'x²')} - {format_coefficient(b, 'x')} - {c} = x² + {d}"
    solution_info = solve_by_completing_square(new_a, -b, new_c)
    wrong_answers = generate_wrong_answers(solution_info)
    correct_letter, choices = generate_choices(solution_info, wrong_answers)

    return equation, correct_letter, choices


def template_16():
    """ax² - bx - c = x² - d (b > 0, c > 0, d > 0)"""
    a = random.randint(2, 5)
    b = random.randint(1, 6)
    c = random.randint(1, 6)
    d = random.randint(1, 6)

    # Rearrange to standard form: (a-1)x² - bx + (-c + d) = 0
    new_a = a - 1
    new_c = -c + d

    # Ensure real solutions
    disc = b**2 - 4*new_a*new_c
    while disc < 0 or not is_simple_discriminant(disc):
        a = random.randint(2, 5)
        b = random.randint(1, 6)
        c = random.randint(1, 6)
        d = random.randint(1, 6)
        new_a = a - 1
        new_c = -c + d

        disc = b**2 - 4*new_a*new_c
    equation = f"{format_coefficient(a, 'x²')} - {format_coefficient(b, 'x')} - {c} = x² - {d}"
    solution_info = solve_by_completing_square(new_a, -b, new_c)
    wrong_answers = generate_wrong_answers(solution_info)
    correct_letter, choices = generate_choices(solution_info, wrong_answers)

    return equation, correct_letter, choices


# Templates 17-24: ax² ± bx ± c = d ± bx variations
def template_17():
    """ax² + bx + c = d + bx (b > 0, c > 0, d > 0)"""
    a = random.randint(2, 5)
    b = random.randint(1, 6)
    c = random.randint(1, 6)
    d = random.randint(1, 6)

    # Rearrange to standard form: ax² + (c - d) = 0
    # Note: bx cancels out on both sides
    new_c = c - d

    # For ax² + new_c = 0, we need new_c to be negative or zero for real solutions
    # x² = -new_c/a, so -new_c/a >= 0, meaning new_c <= 0
    while new_c > 0:
        c = random.randint(1, 6)
        d = random.randint(1, 6)
        new_c = c - d

    equation = f"{format_coefficient(a, 'x²')} + {format_coefficient(b, 'x')} + {c} = {d} + {format_coefficient(b, 'x')}"
    solution_info = solve_by_completing_square(a, 0, new_c)
    wrong_answers = generate_wrong_answers(solution_info)
    correct_letter, choices = generate_choices(solution_info, wrong_answers)

    return equation, correct_letter, choices


def template_18():
    """ax² - bx + c = d + bx (b > 0, c > 0, d > 0)"""
    a = random.randint(2, 5)
    b = random.randint(1, 6)
    c = random.randint(1, 6)
    d = random.randint(1, 6)

    # Rearrange to standard form: ax² - 2bx + (c - d) = 0
    new_b = -2 * b
    new_c = c - d

    # Ensure real solutions: 4b² - 4a(c-d) >= 0
    disc = 4 * b**2 - 4 * a * new_c
    while disc < 0 or not is_simple_discriminant(disc):
        a = random.randint(2, 5)
        b = random.randint(1, 6)
        c = random.randint(1, 6)
        d = random.randint(1, 6)
        new_c = c - d

        disc = 4 * b**2 - 4 * a * new_c
    equation = f"{format_coefficient(a, 'x²')} - {format_coefficient(b, 'x')} + {c} = {d} + {format_coefficient(b, 'x')}"
    solution_info = solve_by_completing_square(a, new_b, new_c)
    wrong_answers = generate_wrong_answers(solution_info)
    correct_letter, choices = generate_choices(solution_info, wrong_answers)

    return equation, correct_letter, choices


def template_19():
    """ax² + bx - c = d + bx (b > 0, c > 0, d > 0)"""
    a = random.randint(2, 5)
    b = random.randint(1, 6)
    c = random.randint(1, 6)
    d = random.randint(1, 6)

    # Rearrange to standard form: ax² + (-c - d) = 0
    # Note: bx cancels out
    new_c = -c - d

    # ax² + new_c = 0, always has real solutions since new_c is negative

    equation = f"{format_coefficient(a, 'x²')} + {format_coefficient(b, 'x')} - {c} = {d} + {format_coefficient(b, 'x')}"
    solution_info = solve_by_completing_square(a, 0, new_c)
    wrong_answers = generate_wrong_answers(solution_info)
    correct_letter, choices = generate_choices(solution_info, wrong_answers)

    return equation, correct_letter, choices


def template_20():
    """ax² + bx + c = d - bx (b > 0, c > 0, d > 0)"""
    a = random.randint(2, 5)
    b = random.randint(1, 6)
    c = random.randint(1, 6)
    d = random.randint(1, 6)

    # Rearrange to standard form: ax² + 2bx + (c - d) = 0
    new_b = 2 * b
    new_c = c - d

    # Ensure real solutions: 4b² - 4a(c-d) >= 0
    disc = 4 * b**2 - 4 * a * new_c
    while disc < 0 or not is_simple_discriminant(disc):
        a = random.randint(2, 5)
        b = random.randint(1, 6)
        c = random.randint(1, 6)
        d = random.randint(1, 6)
        new_b = 2 * b  # Recalculate derived variable
        new_c = c - d

        disc = 4 * b**2 - 4 * a * new_c
    equation = f"{format_coefficient(a, 'x²')} + {format_coefficient(b, 'x')} + {c} = {d} - {format_coefficient(b, 'x')}"
    solution_info = solve_by_completing_square(a, new_b, new_c)
    wrong_answers = generate_wrong_answers(solution_info)
    correct_letter, choices = generate_choices(solution_info, wrong_answers)

    return equation, correct_letter, choices


def template_21():
    """ax² - bx - c = d + bx (b > 0, c > 0, d > 0)"""
    a = random.randint(2, 5)
    b = random.randint(1, 6)
    c = random.randint(1, 6)
    d = random.randint(1, 6)

    # Rearrange to standard form: ax² - 2bx + (-c - d) = 0
    new_b = -2 * b
    new_c = -c - d

    # 4b² - 4a(-c-d) = 4b² + 4a(c+d) always positive

    equation = f"{format_coefficient(a, 'x²')} - {format_coefficient(b, 'x')} - {c} = {d} + {format_coefficient(b, 'x')}"
    solution_info = solve_by_completing_square(a, new_b, new_c)
    wrong_answers = generate_wrong_answers(solution_info)
    correct_letter, choices = generate_choices(solution_info, wrong_answers)

    return equation, correct_letter, choices


def template_22():
    """ax² + bx - c = d - bx (b > 0, c > 0, d > 0)"""
    a = random.randint(2, 5)
    b = random.randint(1, 6)
    c = random.randint(1, 6)
    d = random.randint(1, 6)

    # Rearrange to standard form: ax² + 2bx + (-c - d) = 0
    new_b = 2 * b
    new_c = -c - d

    # 4b² - 4a(-c-d) = 4b² + 4a(c+d) always positive

    equation = f"{format_coefficient(a, 'x²')} + {format_coefficient(b, 'x')} - {c} = {d} - {format_coefficient(b, 'x')}"
    solution_info = solve_by_completing_square(a, new_b, new_c)
    wrong_answers = generate_wrong_answers(solution_info)
    correct_letter, choices = generate_choices(solution_info, wrong_answers)

    return equation, correct_letter, choices


def template_23():
    """ax² - bx + c = d - bx (b > 0, c > 0, d > 0)"""
    a = random.randint(2, 5)
    b = random.randint(1, 6)
    c = random.randint(1, 6)
    d = random.randint(1, 6)

    # Rearrange to standard form: ax² + (c - d) = 0
    # Note: -bx cancels out
    new_c = c - d

    # Need c - d <= 0 for real solutions
    while new_c > 0:
        c = random.randint(1, 6)
        d = random.randint(1, 6)
        new_c = c - d

    equation = f"{format_coefficient(a, 'x²')} - {format_coefficient(b, 'x')} + {c} = {d} - {format_coefficient(b, 'x')}"
    solution_info = solve_by_completing_square(a, 0, new_c)
    wrong_answers = generate_wrong_answers(solution_info)
    correct_letter, choices = generate_choices(solution_info, wrong_answers)

    return equation, correct_letter, choices


def template_24():
    """ax² - bx - c = d - bx (b > 0, c > 0, d > 0)"""
    a = random.randint(2, 5)
    b = random.randint(1, 6)
    c = random.randint(1, 6)
    d = random.randint(1, 6)

    # Rearrange to standard form: ax² + (-c - d) = 0
    # Note: -bx cancels out
    new_c = -c - d

    # Always has real solutions since new_c is negative

    equation = f"{format_coefficient(a, 'x²')} - {format_coefficient(b, 'x')} - {c} = {d} - {format_coefficient(b, 'x')}"
    solution_info = solve_by_completing_square(a, 0, new_c)
    wrong_answers = generate_wrong_answers(solution_info)
    correct_letter, choices = generate_choices(solution_info, wrong_answers)

    return equation, correct_letter, choices
