"""
Rule-based quadratic formula solver: ax^2 + bx + c = 0

Extracts coefficients and computes roots using:
  discriminant = b² - 4ac
  roots = (-b ± √discriminant) / 2a

Handles:
  - Spaces and Unicode dashes
  - Signed/decimal coefficients
  - Implicit coefficients (x² → 1x², -x → -1x)
  - Order-insensitive choice matching
"""

import re
import math
import unicodedata
from typing import Optional, Tuple


def _normalize(s: str) -> str:
    """Normalize: NFKC, lowercase, collapse spaces, handle dashes."""
    s = unicodedata.normalize("NFKC", s).lower()
    s = s.replace("\u2212", "-").replace("\u2013", "-").replace("\u2014", "-")
    s = s.replace("\u2012", "-").replace("\u2010", "-")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def parse_quadratic_coeffs(stem: str) -> Optional[Tuple[float, float, float]]:
    """
    Parse a, b, c from quadratic equation stem.

    Examples:
      "Solve: x^2 - 5x + 6 = 0" → (1.0, -5.0, 6.0)
      "2x^2 + 4x - 30 = 0" → (2.0, 4.0, -30.0)

    Returns:
        (a, b, c) as floats, or None if not quadratic or a=0
    """
    s = _normalize(stem)

    # Extract LHS before "= 0"
    m = re.search(r"^(.*?)=\s*0\b", s)
    if not m:
        # Try without "= 0" constraint
        expr = s
    else:
        expr = m.group(1).strip()

    # Make implicit coefficients explicit: x^2→1x^2, x→1x
    expr = re.sub(r"(?<![0-9.])\s*x\s*\^", "1x^", expr)  # x^ → 1x^
    expr = re.sub(r"(?<![0-9.])\s*x(?!\s*\^|[0-9])", "1x", expr)  # x (not followed by ^ or digit) → 1x

    # Extract a x^2 coefficients
    a_terms = re.findall(r"([+\-]?\s*\d+(?:\.\d+)?)\s*x\s*\^\s*2", expr)
    a = sum(float(t.replace(" ", "")) for t in a_terms) if a_terms else 0.0

    if abs(a) < 1e-12:
        return None

    # Extract b x coefficients (but not x^2)
    b_terms = re.findall(r"([+\-]?\s*\d+(?:\.\d+)?)\s*x(?!\s*\^)", expr)
    b = sum(float(t.replace(" ", "")) for t in b_terms) if b_terms else 0.0

    # Extract constant terms (those not attached to x)
    # Remove all x-containing terms, then extract remaining numbers
    expr_no_x = re.sub(r"[+\-]?\s*\d+(?:\.\d+)?\s*x\s*(?:\^\s*\d+)?", "", expr)
    c_terms = re.findall(r"([+\-]?\s*\d+(?:\.\d+)?)", expr_no_x)
    c = sum(float(t.replace(" ", "")) for t in c_terms) if c_terms else 0.0

    return (a, b, c)


def quadratic_roots(a: float, b: float, c: float) -> Optional[Tuple[float, float]]:
    """
    Compute roots using quadratic formula.

    discriminant = b² - 4ac
    roots = (-b ± √discriminant) / 2a

    Args:
        a, b, c: Coefficients (a must be non-zero)

    Returns:
        Tuple (r1, r2) with r1 ≤ r2, or None if discriminant < 0 (complex roots)
    """
    if abs(a) < 1e-12:
        return None

    disc = b * b - 4 * a * c

    # Complex roots
    if disc < -1e-12:
        return None

    # Clamp to 0 for numerical stability
    if disc < 0:
        disc = 0.0

    sqrt_d = math.sqrt(disc)
    r1 = (-b - sqrt_d) / (2 * a)
    r2 = (-b + sqrt_d) / (2 * a)

    # Return sorted (r1 ≤ r2)
    return (min(r1, r2), max(r1, r2))


def roots_match_choice(roots: Tuple[float, float], choice_text: str) -> bool:
    """
    Check if roots match choice text, order-insensitive.

    Handles formats: "(a, b)", "{a, b}", etc.
    Compares with tolerance for floating point.

    Args:
        roots: Tuple (r1, r2) as floats
        choice_text: Text like "(2, 3)" or "{3, 2}"

    Returns:
        True if roots match (order-insensitive), False otherwise
    """
    if roots is None:
        return False

    text = _normalize(choice_text)

    # Normalize brackets
    text = text.replace("{", "(").replace("}", ")")

    # Extract numbers: "(a, b)" → [a, b]
    m = re.match(r"^\(\s*([+\-]?[0-9]+(?:\.[0-9]+)?)\s*,\s*([+\-]?[0-9]+(?:\.[0-9]+)?)\s*\)$", text)
    if not m:
        return False

    a = float(m.group(1))
    b = float(m.group(2))

    r1, r2 = roots

    # Unordered comparison with tolerance
    eps = 1e-6
    return (
        (abs(a - r1) < eps and abs(b - r2) < eps) or
        (abs(a - r2) < eps and abs(b - r1) < eps)
    )
