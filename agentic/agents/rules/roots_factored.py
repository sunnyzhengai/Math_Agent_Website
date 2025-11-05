"""
Rule-based extractor for roots from factored form: a(x - r₁)(x - r₂) = 0

Handles:
  - Leading scalar (ignored for roots)
  - Spaces and Unicode dashes
  - Forms with zero root: (x)(x - 3) = 0
  - Order-insensitive choice matching
"""

import re
import unicodedata
from typing import Optional, Tuple


def _normalize(s: str) -> str:
    """Normalize: NFKC, lowercase, collapse spaces, handle dashes."""
    s = unicodedata.normalize("NFKC", s).lower()
    s = s.replace("\u2212", "-").replace("\u2013", "-").replace("\u2014", "-")
    s = s.replace("\u2012", "-").replace("\u2010", "-")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def parse_factored_roots(stem: str) -> Optional[Tuple[float, float]]:
    """
    Extract roots from factored form a(x - r₁)(x - r₂) = 0.

    Examples:
      "(x - 3)(x + 2) = 0" → (3.0, -2.0)
      "2(x + 4)(x - 1) = 0" → (-4.0, 1.0)
      "(x)(x - 3) = 0" → (0.0, 3.0)
      "-(x + 5)(x - 1) = 0" → (-5.0, 1.0)

    Returns:
        Tuple of two floats (roots), or None if parsing fails.
    """
    s = _normalize(stem)

    # Extract LHS (before "= 0")
    m = re.search(r"^(.*?)=\s*0\b", s)
    if not m:
        # Try without "= 0" constraint
        expr = s
    else:
        expr = m.group(1).strip()

    # Remove leading scalar a (if present)
    # Handles: "2*(x-...)" or "2(x-...)" or "-(...)"
    expr = re.sub(r"^[+\-]?\d+(?:\.\d+)?\s*\*\s*", "", expr)  # "2 * (..."
    expr = re.sub(r"^[+\-]?\d+(?:\.\d+)?\s*(?=\()", "", expr)  # "2(...)"
    expr = re.sub(r"^\s*-\s*(?=\()", "", expr)  # Leading minus before (

    # Pattern 1: Two non-trivial factors (x ± c)(x ± d)
    pat1 = r"\(\s*x\s*([+\-])\s*([0-9]+(?:\.[0-9]+)?)\s*\)\s*\(\s*x\s*([+\-])\s*([0-9]+(?:\.[0-9]+)?)\s*\)"
    m1 = re.search(pat1, expr)

    if m1:
        s1, v1, s2, v2 = m1.groups()
        v1 = float(v1)
        v2 = float(v2)

        # (x + c) → root is -c; (x - c) → root is c
        r1 = -v1 if s1 == "+" else v1
        r2 = -v2 if s2 == "+" else v2

        return (r1, r2)

    # Pattern 2: One factor is (x) → root 0
    pat2 = r"\(\s*x\s*\)\s*\(\s*x\s*([+\-])\s*([0-9]+(?:\.[0-9]+)?)\s*\)"
    m2 = re.search(pat2, expr)

    if m2:
        s2, v2 = m2.groups()
        v2 = float(v2)
        r2 = -v2 if s2 == "+" else v2
        return (0.0, r2)

    # Pattern 3: Reversed order (x ± c)(x) → other root first
    pat3 = r"\(\s*x\s*([+\-])\s*([0-9]+(?:\.[0-9]+)?)\s*\)\s*\(\s*x\s*\)"
    m3 = re.search(pat3, expr)

    if m3:
        s1, v1 = m3.groups()
        v1 = float(v1)
        r1 = -v1 if s1 == "+" else v1
        return (r1, 0.0)

    return None


def roots_match_choice(roots: Tuple[float, float], choice_text: str) -> bool:
    """
    Check if roots match choice text, order-insensitive.

    Handles formats: "(a, b)", "{a, b}", "[a, b]", etc.
    Compares with small tolerance for floating point.

    Args:
        roots: Tuple of (r1, r2) as floats
        choice_text: Text like "(3, -2)" or "{-2, 3}"

    Returns:
        True if roots match (order-insensitive), False otherwise
    """
    text = _normalize(choice_text)

    # Normalize brackets: {a, b} → (a, b)
    text = text.replace("{", "(").replace("}", ")")

    # Extract numbers: "(a, b)" → [a, b]
    m = re.match(r"^\(\s*([+\-]?[0-9]+(?:\.[0-9]+)?)\s*,\s*([+\-]?[0-9]+(?:\.[0-9]+)?)\s*\)$", text)
    if not m:
        return False

    a = float(m.group(1))
    b = float(m.group(2))

    r1, r2 = roots

    # Unordered comparison with small tolerance
    eps = 1e-9
    return (
        (abs(a - r1) < eps and abs(b - r2) < eps) or
        (abs(a - r2) < eps and abs(b - r1) < eps)
    )
