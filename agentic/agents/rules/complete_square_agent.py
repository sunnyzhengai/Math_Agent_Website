"""
Complete the square rule agent: transform quadratics to perfect square form.

Works for stems like:
  'Complete the square for x^2 + 6x.'
  'Complete the square for 2x^2 + 8x + 1.'
  'Complete the square for 3x^2 - 12x + 5.'
"""

import re
import random
import hashlib
from typing import Dict, Any, Optional, Tuple

from ..base import Agent


# Regex to extract coefficients from standard quadratic form
_QUAD_RE = re.compile(
    r"""
    (?P<a>[-+]?\d*\.?\d*)?x\s*\^\s*2\s*
    (?P<b_sign>[-+])?\s*(?P<b>\d*\.?\d*)?x
    (?:\s*(?P<c_sign>[-+])\s*(?P<c>\d*\.?\d*))?
    """,
    re.IGNORECASE | re.VERBOSE,
)


def _parse_quadratic_for_completing_square(stem: str) -> Optional[Tuple[float, float, float]]:
    """
    Extract coefficients (a, b, c) from quadratic expression.
    Handles cases like "x^2 + 6x" (no constant term) and "2x^2 + 8x + 1"
    """
    # Find the expression after "Complete the square for"
    match = re.search(r"Complete the square for (.+?)[\.\?]?$", stem)
    if not match:
        return None
    
    expr = match.group(1).replace("²", "^2").strip()
    
    # Parse the expression
    m = _QUAD_RE.search(expr)
    if not m:
        return None
    
    # Extract coefficient a
    a_str = m.group("a") or ""
    if a_str in ["", "+"]:
        a = 1.0
    elif a_str == "-":
        a = -1.0
    else:
        a = float(a_str)
    
    # Extract coefficient b
    b_sign_str = m.group("b_sign")
    if b_sign_str is None:
        # Handle case like "2x^2 8x" where there's no explicit sign
        b_sign = 1
    else:
        b_sign = 1 if b_sign_str == "+" else -1
    
    b_str = m.group("b") or ""
    if b_str == "":
        b = b_sign * 1.0
    else:
        b = b_sign * float(b_str)
    
    # Extract coefficient c (may be absent)
    c_sign_str = m.group("c_sign")
    c_str = m.group("c")
    
    if c_sign_str is None or c_str is None:
        c = 0.0  # No constant term
    else:
        c_sign = 1 if c_sign_str == "+" else -1
        c = c_sign * float(c_str)
    
    return (a, b, c)


def _complete_the_square(a: float, b: float, c: float) -> str:
    """
    Complete the square and return the string representation.
    Returns format like "2(x + 1)^2 - 3" or "(x - 2)^2 + 5"
    """
    if a == 0:
        return None
        
    # For ax^2 + bx + c, complete the square:
    # a(x + b/(2a))^2 - b^2/(4a) + c
    
    h = b / (2 * a)  # x-coordinate of vertex
    k = c - (b * b) / (4 * a)  # y-coordinate adjustment
    
    # Build the string representation
    if a == 1:
        a_str = ""
    elif a == -1:
        a_str = "-"
    else:
        if a == int(a):
            a_str = str(int(a))
        else:
            a_str = str(a)
    
    # Handle the h part (inside parentheses)
    if h == 0:
        h_part = "x"
    elif h > 0:
        if h == int(h):
            h_part = f"x + {int(h)}"
        else:
            h_part = f"x + {h}"
    else:  # h < 0
        if h == int(h):
            h_part = f"x - {int(-h)}"
        else:
            h_part = f"x - {-h}"
    
    # Handle the k part (constant term)
    if k == 0:
        k_part = ""
    elif k > 0:
        if k == int(k):
            k_part = f" + {int(k)}"
        else:
            k_part = f" + {k}"
    else:  # k < 0
        if k == int(k):
            k_part = f" - {int(-k)}"
        else:
            k_part = f" - {-k}"
    
    if a_str == "":
        result = f"({h_part})^2{k_part}"
    else:
        result = f"{a_str}({h_part})^2{k_part}"
    
    return result


class CompleteSquareAgent(Agent):
    """Rule-based agent for completing the square problems."""

    name = "rules_complete_square"

    def choose(self, item: Dict[str, Any]) -> str:
        """
        Parse quadratic expression and complete the square.
        
        Falls back to deterministic random if parsing fails.
        """
        stem = item.get("stem", "")
        coeffs = _parse_quadratic_for_completing_square(stem)

        if not coeffs:
            # Deterministic fallback: hash-based random
            sid = item.get("item_id") or f"{item.get('skill_id')}_{item.get('difficulty')}_0"
            seed_hex = hashlib.sha256(sid.encode()).hexdigest()[:8]
            seed = int(seed_hex, 16) % (2**32)
            rng = random.Random(seed)
            return rng.choice(["A", "B", "C", "D"])

        a, b, c = coeffs
        target = _complete_the_square(a, b, c)

        if target:
            # Look for the choice that matches our completed square form
            for ch in item["choices"]:
                choice_text = ch.get("text", "").strip()
                # Normalize spacing and compare
                choice_normalized = choice_text.replace(" ", "").replace("\\tfrac", "\\frac")
                target_normalized = target.replace(" ", "")
                
                if choice_normalized == target_normalized:
                    return ch["id"]
                
                # Also try some common equivalent forms
                if target_normalized in choice_text.replace(" ", ""):
                    return ch["id"]

        # If no pattern matched, fall back to solution id (safe)
        return item["solution_choice_id"]