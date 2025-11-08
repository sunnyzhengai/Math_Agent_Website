"""
Solution Generators - Generate step-by-step explanations for each skill.

Each skill has a generator function that:
1. Extracts values from the question stem
2. Shows step-by-step work
3. Explains common mistakes
4. Returns formatted explanation text
"""

import re
from fractions import Fraction
from typing import Dict, Any, Optional


def generate_solution(item: Dict[str, Any], selected_choice_id: str, correct_choice_id: str) -> str:
    """
    Generate a detailed step-by-step solution for a question.

    Args:
        item: The question item with stem, choices, skill_id
        selected_choice_id: The choice the student selected
        correct_choice_id: The correct choice

    Returns:
        Formatted explanation string with step-by-step solution
    """
    skill_id = item.get("skill_id", "")

    # Route to skill-specific generator
    if skill_id == "quad.standard.vertex":
        return _explain_standard_vertex(item, selected_choice_id, correct_choice_id)
    elif skill_id == "quad.graph.vertex":
        return _explain_vertex_form(item, selected_choice_id, correct_choice_id)
    elif skill_id == "quad.roots.factored":
        return _explain_factored_roots(item, selected_choice_id, correct_choice_id)
    elif skill_id == "quad.solve.by_factoring":
        return _explain_solve_factoring(item, selected_choice_id, correct_choice_id)
    elif skill_id == "quad.solve.by_formula":
        return _explain_quadratic_formula(item, selected_choice_id, correct_choice_id)
    elif skill_id == "quad.discriminant.analysis":
        return _explain_discriminant(item, selected_choice_id, correct_choice_id)
    elif skill_id == "quad.intercepts":
        return _explain_intercepts(item, selected_choice_id, correct_choice_id)
    elif skill_id == "quad.complete.square":
        return _explain_complete_square(item, selected_choice_id, correct_choice_id)
    elif skill_id == "quad.axis.symmetry":
        return _explain_axis_symmetry(item, selected_choice_id, correct_choice_id)
    else:
        # Generic fallback
        return _generic_explanation(item, selected_choice_id, correct_choice_id)


def _explain_standard_vertex(item: Dict[str, Any], selected_id: str, correct_id: str) -> str:
    """Generate explanation for finding vertex from standard form."""
    stem = item["stem"]

    # Parse coefficients from stem (e.g., "Find the vertex of y = x^2 + 10x + 21")
    # Handle various formats: ax^2 + bx + c, -x^2 + bx + c, etc.
    match = re.search(r'y\s*=\s*([+-]?\s*\d*\.?\d*)\s*x\^?2?\s*([+-]\s*\d+\.?\d*)\s*x\s*([+-]\s*\d+\.?\d*)', stem)

    if not match:
        return _generic_explanation(item, selected_id, correct_id)

    a_str = match.group(1).replace(' ', '') or '1'
    if a_str == '+' or a_str == '': a_str = '1'
    if a_str == '-': a_str = '-1'

    b_str = match.group(2).replace(' ', '')
    c_str = match.group(3).replace(' ', '')

    try:
        a = Fraction(a_str)
        b = Fraction(b_str)
        c = Fraction(c_str)
    except:
        return _generic_explanation(item, selected_id, correct_id)

    # Calculate vertex
    h = Fraction(-b, 2 * a)
    k = a * h * h + b * h + c

    # Format numbers nicely
    def fmt(val):
        val = Fraction(val)
        if val.denominator == 1:
            return str(val.numerator)
        else:
            # Also show decimal approximation for fractions
            decimal = float(val)
            return f"{val.numerator}/{val.denominator} (or {decimal:.2f})"

    correct_answer = next((c['text'] for c in item['choices'] if c['id'] == correct_id), "unknown")
    student_answer = next((c['text'] for c in item['choices'] if c['id'] == selected_id), "unknown")

    explanation = f"""**Step-by-step solution:**

**Given equation:** y = {a if a != 1 else ''}x² {'+' if b >= 0 else ''} {b}x {'+' if c >= 0 else ''} {c}

**Step 1:** Identify coefficients
   • a = {a}
   • b = {b}
   • c = {c}

**Step 2:** Find h-coordinate using h = -b/(2a)
   h = -{b}/(2 × {a})
   h = -{b}/{2*a}
   h = {fmt(h)}

**Step 3:** Find k-coordinate by substituting h into the equation
   k = {a}({h})² + {b}({h}) + {c}
   k = {a}({h*h}) + {b*h} + {c}
   k = {fmt(a*h*h)} + {fmt(b*h)} + {fmt(c)}
   k = {fmt(k)}

**Vertex: ({fmt(h)}, {fmt(k)})**

✓ **Correct answer:** {correct_answer}
✗ **You selected:** {student_answer}
"""

    # Add common mistake analysis
    if selected_id != correct_id:
        explanation += f"\n**Common mistake:** "

        # Try to identify the specific error
        try:
            # Parse student answer
            student_match = re.search(r'\(([^,]+),\s*([^)]+)\)', student_answer)
            if student_match:
                student_h = student_match.group(1).strip()
                student_k = student_match.group(2).strip()
                correct_h = str(h) if h.denominator == 1 else f"{h.numerator}/{h.denominator}"
                correct_k = str(k) if k.denominator == 1 else f"{k.numerator}/{k.denominator}"

                # Check for sign error in h
                if student_h == correct_h.replace('-', '') or student_h == '-' + correct_h:
                    explanation += f"Sign error on h. Remember h = -b/(2a), not +b/(2a)."
                # Check if they used c for k
                elif student_k == str(c):
                    explanation += f"You used c as the k-coordinate. The k-coordinate must be calculated by substituting h back into the original equation."
                # Check if they swapped h and k
                elif student_h == correct_k or student_k == correct_h:
                    explanation += f"The vertex coordinates are in the wrong order. The vertex is (h, k), not (k, h)."
                else:
                    explanation += f"Review the vertex formula: h = -b/(2a), then k = f(h)."
        except:
            explanation += "Review the vertex formula: h = -b/(2a), then k = f(h)."

    return explanation


def _explain_vertex_form(item: Dict[str, Any], selected_id: str, correct_id: str) -> str:
    """Generate explanation for finding vertex from vertex form."""
    stem = item["stem"]

    # Parse vertex form: y = a(x - h)^2 + k
    match = re.search(r'y\s*=\s*([+-]?\s*\d*\.?\d*)\s*\(x\s*([+-])\s*(\d+\.?\d*)\)\^?2?\s*([+-])\s*(\d+\.?\d*)', stem)

    if not match:
        return _generic_explanation(item, selected_id, correct_id)

    a_str = match.group(1).replace(' ', '') or '1'
    if a_str == '+' or a_str == '': a_str = '1'
    if a_str == '-': a_str = '-1'

    h_sign = match.group(2)
    h_val = match.group(3)
    k_sign = match.group(4)
    k_val = match.group(5)

    # In vertex form y = a(x - h)^2 + k, if we see (x + 3), then h = -3
    h = f"-{h_val}" if h_sign == '+' else h_val
    k = f"-{k_val}" if k_sign == '-' else k_val

    correct_answer = next((c['text'] for c in item['choices'] if c['id'] == correct_id), "unknown")
    student_answer = next((c['text'] for c in item['choices'] if c['id'] == selected_id), "unknown")

    explanation = f"""**Step-by-step solution:**

**Given equation in vertex form:** {stem.split('y = ')[1] if 'y = ' in stem else stem}

**Key concept:** Vertex form is y = a(x - h)² + k, where the vertex is (h, k)

**Step 1:** Identify the pattern
   The equation is in the form y = a(x - h)² + k

**Step 2:** Extract h and k
   • h = {h} (note the sign change: x {h_sign} {h_val} means h = {h})
   • k = {k} (the constant at the end)

**Vertex: ({h}, {k})**

✓ **Correct answer:** {correct_answer}
✗ **You selected:** {student_answer}
"""

    if selected_id != correct_id:
        explanation += f"\n**Common mistake:** Watch the signs! In vertex form y = a(x - h)² + k:\n"
        explanation += f"   • (x - 3) means h = 3\n"
        explanation += f"   • (x + 3) means h = -3\n"
        explanation += f"   The vertex is directly (h, k) from the form."

    return explanation


def _explain_factored_roots(item: Dict[str, Any], selected_id: str, correct_id: str) -> str:
    """Generate explanation for finding roots from factored form."""
    stem = item["stem"]

    # Parse factored form: y = a(x - r1)(x - r2) or similar variations
    # Examples: y = (x + 3)(x - 5), y = 2(x - 1)(x + 4), etc.
    match = re.search(r'\(x\s*([+-])\s*(\d+\.?\d*)\)\s*\(x\s*([+-])\s*(\d+\.?\d*)\)', stem)

    correct_answer = next((c['text'] for c in item['choices'] if c['id'] == correct_id), "unknown")
    student_answer = next((c['text'] for c in item['choices'] if c['id'] == selected_id), "unknown")

    if match:
        sign1 = match.group(1)
        val1 = match.group(2)
        sign2 = match.group(3)
        val2 = match.group(4)

        # Convert to roots: (x - r) means root is +r, (x + r) means root is -r
        r1 = f"-{val1}" if sign1 == '+' else val1
        r2 = f"-{val2}" if sign2 == '+' else val2

        explanation = f"""**Step-by-step solution:**

**Key concept:** When y = 0, each factor must equal zero.

**Given factored form:** Contains (x {sign1} {val1})(x {sign2} {val2})

**Step 1: Set each factor equal to zero**

   First factor: (x {sign1} {val1}) = 0
   Second factor: (x {sign2} {val2}) = 0

**Step 2: Solve for x in each equation**

   From (x {sign1} {val1}) = 0:
      x = {r1}

   From (x {sign2} {val2}) = 0:
      x = {r2}

**The roots are: x = {r1} and x = {r2}**

✓ **Correct answer:** {correct_answer}
✗ **You selected:** {student_answer}

**Common mistake:** Watch the signs carefully!
   • (x - 3) = 0 means x = +3 (not -3)
   • (x + 3) = 0 means x = -3 (not +3)
"""
    else:
        # Generic fallback
        explanation = f"""**Step-by-step solution:**

**Key concept:** If y = a(x - r₁)(x - r₂), the roots are r₁ and r₂

**Step 1:** Set each factor equal to zero
   (x - r₁) = 0  →  x = r₁
   (x - r₂) = 0  →  x = r₂

**Step 2:** Solve for x in each factor
   The roots are the x-values from the factored form.

✓ **Correct answer:** {correct_answer}
✗ **You selected:** {student_answer}

**Common mistake:** Remember to change the sign. If the factor is (x - 3), the root is x = 3, not x = -3.
"""

    return explanation


def _explain_solve_factoring(item: Dict[str, Any], selected_id: str, correct_id: str) -> str:
    """Generate explanation for solving by factoring."""
    stem = item["stem"]

    # Parse equation: x^2 + bx + c = 0 or ax^2 + bx + c = 0
    match = re.search(r'([+-]?\s*\d*\.?\d*)\s*x\^?2?\s*([+-]\s*\d+\.?\d*)\s*x\s*([+-]\s*\d+\.?\d*)\s*=\s*0', stem)

    if not match:
        # Fallback to generic
        correct_answer = next((c['text'] for c in item['choices'] if c['id'] == correct_id), "unknown")
        student_answer = next((c['text'] for c in item['choices'] if c['id'] == selected_id), "unknown")
        return f"""**Correct answer:** {correct_answer}
**You selected:** {student_answer}

**Tip:** Factor the equation, set each factor = 0, and solve for x."""

    a_str = match.group(1).replace(' ', '') or '1'
    if a_str == '+' or a_str == '': a_str = '1'
    if a_str == '-': a_str = '-1'

    b_str = match.group(2).replace(' ', '')
    c_str = match.group(3).replace(' ', '')

    try:
        a = int(float(a_str))
        b = int(float(b_str))
        c = int(float(c_str))
    except:
        # Fallback
        correct_answer = next((c['text'] for c in item['choices'] if c['id'] == correct_id), "unknown")
        student_answer = next((c['text'] for c in item['choices'] if c['id'] == selected_id), "unknown")
        return f"""**Correct answer:** {correct_answer}
**You selected:** {student_answer}"""

    correct_answer = next((c['text'] for c in item['choices'] if c['id'] == correct_id), "unknown")
    student_answer = next((c['text'] for c in item['choices'] if c['id'] == selected_id), "unknown")

    # Extract the actual roots from the correct answer
    # Format is usually "x = r1 and x = r2"
    roots_match = re.findall(r'x\s*=\s*([+-]?\d+)', correct_answer)

    if len(roots_match) == 2:
        r1 = int(roots_match[0])
        r2 = int(roots_match[1])

        explanation = f"""**Step-by-step solution:**

**Given equation:** {a if a != 1 else ''}x² {'+' if b >= 0 else ''} {b}x {'+' if c >= 0 else ''} {c} = 0

**Step 1: Factor the quadratic**

We need to find two numbers that:
   • Multiply to {a * c} (a × c)
   • Add to {b} (the coefficient of x)

These numbers are {-r1 * a} and {-r2 * a}

Factored form: (x {'+' if -r1 < 0 else '-'} {abs(r1)})(x {'+' if -r2 < 0 else '-'} {abs(r2)}) = 0

**Step 2: Set each factor equal to zero**

   x {'+' if -r1 < 0 else '-'} {abs(r1)} = 0  →  x = {r1}
   x {'+' if -r2 < 0 else '-'} {abs(r2)} = 0  →  x = {r2}

**Step 3: The solutions are x = {r1} and x = {r2}**

**Verification:** Substitute back to check:
   • If x = {r1}: ({r1})² {'+' if b >= 0 else ''}{b}({r1}) {'+' if c >= 0 else ''}{c} = {r1**2 + b*r1 + c} ✓
   • If x = {r2}: ({r2})² {'+' if b >= 0 else ''}{b}({r2}) {'+' if c >= 0 else ''}{c} = {r2**2 + b*r2 + c} ✓

✓ **Correct answer:** {correct_answer}
✗ **You selected:** {student_answer}

**Common mistake:** Don't forget to change the sign when moving from factored form to roots!
   • (x - 3) = 0 means x = +3 (not -3)
   • (x + 5) = 0 means x = -5 (not +5)
"""
    else:
        # Generic version if we can't parse roots
        explanation = f"""**Step-by-step solution:**

**Given equation:** {a if a != 1 else ''}x² {'+' if b >= 0 else ''} {b}x {'+' if c >= 0 else ''} {c} = 0

**Step 1:** Factor the quadratic (find two numbers that multiply to {c} and add to {b})

**Step 2:** Set each factor equal to zero

**Step 3:** Solve for x

✓ **Correct answer:** {correct_answer}
✗ **You selected:** {student_answer}

**Tip:** Check your factoring by FOILing back to verify you get the original equation.
"""

    return explanation


def _explain_quadratic_formula(item: Dict[str, Any], selected_id: str, correct_id: str) -> str:
    """Generate explanation for quadratic formula."""
    stem = item["stem"]

    # Parse equation: ax^2 + bx + c = 0
    match = re.search(r'([+-]?\s*\d*\.?\d*)\s*x\^?2?\s*([+-]\s*\d+\.?\d*)\s*x\s*([+-]\s*\d+\.?\d*)\s*=\s*0', stem)

    correct_answer = next((c['text'] for c in item['choices'] if c['id'] == correct_id), "unknown")
    student_answer = next((c['text'] for c in item['choices'] if c['id'] == selected_id), "unknown")

    if not match:
        # Generic fallback
        return f"""**Step-by-step solution:**

**Quadratic Formula:** x = (-b ± √(b² - 4ac)) / (2a)

**Step 1:** Identify a, b, and c from the equation ax² + bx + c = 0

**Step 2:** Calculate the discriminant: b² - 4ac

**Step 3:** Substitute into the quadratic formula

**Step 4:** Simplify to get the two solutions

✓ **Correct answer:** {correct_answer}
✗ **You selected:** {student_answer}

**Tip:** Be careful with signs, especially when b is negative!
"""

    a_str = match.group(1).replace(' ', '') or '1'
    if a_str == '+' or a_str == '': a_str = '1'
    if a_str == '-': a_str = '-1'

    b_str = match.group(2).replace(' ', '')
    c_str = match.group(3).replace(' ', '')

    try:
        a = Fraction(a_str)
        b = Fraction(b_str)
        c = Fraction(c_str)
    except:
        # Use generic fallback
        return f"""**Correct answer:** {correct_answer}
**You selected:** {student_answer}

**Tip:** Use the quadratic formula: x = (-b ± √(b² - 4ac)) / (2a)"""

    # Calculate discriminant
    discriminant = b*b - 4*a*c

    # Helper to format numbers
    def fmt(val):
        val = Fraction(val)
        if val.denominator == 1:
            return str(val.numerator)
        return f"{val.numerator}/{val.denominator}"

    explanation = f"""**Step-by-step solution:**

**Quadratic Formula:** x = (-b ± √(b² - 4ac)) / (2a)

**Given equation:** {a if a != 1 else ''}x² {'+' if b >= 0 else ''} {b}x {'+' if c >= 0 else ''} {c} = 0

**Step 1: Identify coefficients**
   • a = {a}
   • b = {b}
   • c = {c}

**Step 2: Calculate the discriminant (b² - 4ac)**
   Discriminant = ({b})² - 4({a})({c})
   Discriminant = {b*b} - {4*a*c}
   Discriminant = {discriminant}

**Step 3: Substitute into the quadratic formula**
   x = (-({b}) ± √{discriminant}) / (2({a}))
   x = ({-b} ± √{discriminant}) / {2*a}

**Step 4: Simplify to get two solutions**
   x = ({-b} + √{discriminant}) / {2*a}  or  x = ({-b} - √{discriminant}) / {2*a}

✓ **Correct answer:** {correct_answer}
✗ **You selected:** {student_answer}

**Tip:** Be careful with signs! When b is negative, -b becomes positive.
   • The discriminant tells us: if positive = 2 real roots, if zero = 1 repeated root, if negative = complex roots
"""

    return explanation


def _explain_discriminant(item: Dict[str, Any], selected_id: str, correct_id: str) -> str:
    """Generate explanation for discriminant analysis."""
    correct_answer = next((c['text'] for c in item['choices'] if c['id'] == correct_id), "unknown")
    student_answer = next((c['text'] for c in item['choices'] if c['id'] == selected_id), "unknown")

    explanation = f"""**Step-by-step solution:**

**Discriminant:** Δ = b² - 4ac

**Step 1:** Identify a, b, and c

**Step 2:** Calculate b² - 4ac

**Step 3:** Interpret the result:
   • If Δ > 0: Two real roots
   • If Δ = 0: One real root (repeated)
   • If Δ < 0: No real roots (two complex roots)

✓ **Correct answer:** {correct_answer}
✗ **You selected:** {student_answer}
"""

    return explanation


def _explain_intercepts(item: Dict[str, Any], selected_id: str, correct_id: str) -> str:
    """Generate explanation for finding intercepts."""
    correct_answer = next((c['text'] for c in item['choices'] if c['id'] == correct_id), "unknown")
    student_answer = next((c['text'] for c in item['choices'] if c['id'] == selected_id), "unknown")

    explanation = f"""**Step-by-step solution:**

**For x-intercepts:** Set y = 0 and solve for x
**For y-intercept:** Set x = 0 and solve for y

✓ **Correct answer:** {correct_answer}
✗ **You selected:** {student_answer}
"""

    return explanation


def _explain_complete_square(item: Dict[str, Any], selected_id: str, correct_id: str) -> str:
    """Generate explanation for completing the square."""
    correct_answer = next((c['text'] for c in item['choices'] if c['id'] == correct_id), "unknown")
    student_answer = next((c['text'] for c in item['choices'] if c['id'] == selected_id), "unknown")

    explanation = f"""**Step-by-step solution:**

**Completing the square:** Transform ax² + bx + c into a(x - h)² + k

**Step 1:** Group x² and x terms
**Step 2:** Factor out 'a' if a ≠ 1
**Step 3:** Add and subtract (b/2a)²
**Step 4:** Rewrite as perfect square

✓ **Correct answer:** {correct_answer}
✗ **You selected:** {student_answer}
"""

    return explanation


def _explain_axis_symmetry(item: Dict[str, Any], selected_id: str, correct_id: str) -> str:
    """Generate explanation for axis of symmetry."""
    correct_answer = next((c['text'] for c in item['choices'] if c['id'] == correct_id), "unknown")
    student_answer = next((c['text'] for c in item['choices'] if c['id'] == selected_id), "unknown")

    explanation = f"""**Step-by-step solution:**

**Axis of symmetry:** x = -b/(2a)

**Step 1:** Identify a and b from ax² + bx + c

**Step 2:** Calculate x = -b/(2a)

**Note:** This is the same as the h-coordinate of the vertex!

✓ **Correct answer:** {correct_answer}
✗ **You selected:** {student_answer}
"""

    return explanation


def _generic_explanation(item: Dict[str, Any], selected_id: str, correct_id: str) -> str:
    """Generic fallback explanation."""
    correct_answer = next((c['text'] for c in item['choices'] if c['id'] == correct_id), "unknown")
    student_answer = next((c['text'] for c in item['choices'] if c['id'] == selected_id), "unknown")

    return f"""**Correct answer:** {correct_answer}

**You selected:** {student_answer}

Review the question and try to identify where your approach differed from the correct method.
"""
