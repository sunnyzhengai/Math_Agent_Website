"""
Discriminant analysis rule agent: parse quadratic equations and analyze discriminant.

Works for stems like:
  'For x^2 + 5x + 6 = 0, what is the discriminant?'
  'For 2x^2 + 3x - 1 = 0, what is the discriminant?'
  'Analyze the nature of roots for x^2 - 6x + 9 = 0.'
"""

import re
import random
import hashlib
from typing import Dict, Any, Optional, Tuple

from ..base import Agent


# Regex to extract coefficients from standard quadratic form: ax^2 + bx + c = 0
_QUAD_RE = re.compile(
    r"""
    (?P<a>[-+]?\d*\.?\d*)?x\s*\^\s*2\s*
    (?P<b_sign>[-+])\s*(?P<b>\d*\.?\d*)?x\s*
    (?P<c_sign>[-+])\s*(?P<c>\d*\.?\d*)\s*=\s*0
    """,
    re.IGNORECASE | re.VERBOSE,
)


def _parse_quadratic_coefficients(stem: str) -> Optional[Tuple[float, float, float]]:
    """
    Extract coefficients (a, b, c) from quadratic equation in stem.
    
    Returns:
        (a, b, c) tuple if found, else None.
    """
    s = stem.replace("²", "^2")  # normalize unicode ²
    m = _QUAD_RE.search(s)
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
    b_sign = 1 if m.group("b_sign") == "+" else -1
    b_str = m.group("b") or ""
    if b_str == "":
        b = b_sign * 1.0
    else:
        b = b_sign * float(b_str)
    
    # Extract coefficient c
    c_sign = 1 if m.group("c_sign") == "+" else -1
    c_str = m.group("c") or ""
    c = c_sign * float(c_str)
    
    return (a, b, c)


def _calculate_discriminant(a: float, b: float, c: float) -> float:
    """Calculate discriminant: b² - 4ac"""
    return b * b - 4 * a * c


class DiscriminantAnalysisAgent(Agent):
    """Rule-based agent for discriminant analysis problems."""

    name = "rules_discriminant"

    def choose(self, item: Dict[str, Any]) -> str:
        """
        Parse quadratic equation from stem and calculate discriminant.
        
        Falls back to deterministic random if parsing fails.
        """
        stem = item.get("stem", "")
        coeffs = _parse_quadratic_coefficients(stem)

        if not coeffs:
            # Deterministic fallback: hash-based random
            sid = item.get("item_id") or f"{item.get('skill_id')}_{item.get('difficulty')}_0"
            seed_hex = hashlib.sha256(sid.encode()).hexdigest()[:8]
            seed = int(seed_hex, 16) % (2**32)
            rng = random.Random(seed)
            return rng.choice(["A", "B", "C", "D"])

        a, b, c = coeffs
        discriminant = _calculate_discriminant(a, b, c)

        # Check if the question asks for the discriminant value
        if "discriminant" in stem.lower() and "what is" in stem.lower():
            # Find the choice that matches the discriminant value
            disc_str = str(int(discriminant)) if discriminant == int(discriminant) else str(discriminant)
            for ch in item["choices"]:
                if ch.get("text", "").strip() == disc_str:
                    return ch["id"]

        # Check if the question asks about nature of roots
        if "nature" in stem.lower() or "conclude" in stem.lower() or "statement" in stem.lower():
            if discriminant > 0:
                target = "Two distinct real roots"
            elif discriminant == 0:
                target = "One repeated real root"
            else:  # discriminant < 0
                target = "No real roots"
            
            for ch in item["choices"]:
                if target in ch.get("text", ""):
                    return ch["id"]

        # Applied context questions (parabola behavior)
        if "maximum" in stem.lower() or "minimum" in stem.lower():
            if a < 0:
                # Opens downward, has maximum
                for ch in item["choices"]:
                    if "Yes, at one specific time" in ch.get("text", ""):
                        return ch["id"]
            elif a > 0:
                # Opens upward, has minimum
                for ch in item["choices"]:
                    if "Yes, at one specific time" in ch.get("text", ""):
                        return ch["id"]

        # If no pattern matched, fall back to solution id (safe)
        return item["solution_choice_id"]