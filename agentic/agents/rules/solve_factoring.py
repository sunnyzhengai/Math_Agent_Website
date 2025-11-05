"""
Rule-based trinomial factoring solver: ax^2 + bx + c = 0

Handles:
  - Simple case (a=1): find roots via factor pairs
  - General case (a≠1): AC method to find integer factorization
  - Returns real roots if cleanly factorable, None otherwise
  - Falls back to formula rule for non-integer roots

Implements:
  - factor_trinomial(a,b,c) → (r1, r2) or None
  - roots_match_choice(roots, text) → bool (order-insensitive)
"""

from typing import Optional, Tuple


def factor_trinomial(a: float, b: float, c: float) -> Optional[Tuple[float, float]]:
    """
    Factor ax^2 + bx + c = 0 over integers.

    For a=1: find r1, r2 such that r1 + r2 = b and r1 * r2 = c.
    For a≠1: AC method — find m, n such that m*n = a*c and m+n = b,
             then factor by grouping to extract roots.

    Args:
        a, b, c: Coefficients (must be integers or very close)

    Returns:
        Tuple (r1, r2) with r1 ≤ r2 if cleanly factorable over integers,
        None otherwise (formula rule will handle via discriminant).
    """
    # Ensure we're working with integers
    # (coefficients may be floats that represent integers)
    eps = 1e-9
    
    try:
        a_int = round(a)
        b_int = round(b)
        c_int = round(c)
        
        # Validate they're close to their rounded values
        if (abs(a - a_int) > eps or abs(b - b_int) > eps or abs(c - c_int) > eps):
            return None
        
        a, b, c = float(a_int), float(b_int), float(c_int)
    except (ValueError, OverflowError):
        return None

    if abs(a) < eps:
        return None

    # Case 1: a = 1, simple factoring
    if abs(a - 1.0) < eps:
        return _factor_simple(b_int, c_int)

    # Case 2: a ≠ 1, AC method
    return _factor_ac_method(a_int, b_int, c_int)


def _factor_simple(b: int, c: int) -> Optional[Tuple[float, float]]:
    """
    Factor x^2 + bx + c by finding r1, r2 where:
      r1 + r2 = b
      r1 * r2 = c

    Returns sorted (r1, r2) or None.
    """
    if c == 0:
        # x^2 + bx = x(x + b), roots: 0, -b
        return (min(0.0, float(-b)), max(0.0, float(-b)))

    # Enumerate factor pairs of c
    for p in range(-abs(c), abs(c) + 1):
        if p == 0:
            continue
        if c % p != 0:
            continue
        q = c // p
        if p + q == b:
            # Found pair: (x + p)(x + q), roots: -p, -q
            r1, r2 = float(-p), float(-q)
            return (min(r1, r2), max(r1, r2))

    return None


def _factor_ac_method(a: int, b: int, c: int) -> Optional[Tuple[float, float]]:
    """
    Factor ax^2 + bx + c via AC method:
      1. Find m, n where m*n = a*c and m+n = b
      2. Rewrite: ax^2 + mx + nx + c
      3. Factor by grouping: a*x*(x + m/a) + c*(...)
      4. Extract roots

    For now, we'll compute roots via formula if AC succeeds,
    to avoid messy algebra. If m,n don't exist, return None.

    Returns sorted (r1, r2) or None if not cleanly factorable.
    """
    ac = a * c

    if ac == 0:
        return None

    # Find m, n: m*n = ac, m+n = b
    limit = abs(ac)
    m_n_pair = None

    for m in range(-limit, limit + 1):
        if m == 0:
            continue
        if ac % m != 0:
            continue
        n = ac // m
        if m + n == b:
            m_n_pair = (m, n)
            break

    if m_n_pair is None:
        # No integer AC pair exists
        return None

    m, n = m_n_pair

    # Now rewrite: ax^2 + mx + nx + c = 0
    # Factor by grouping: a*x*(x + m/a) + something...
    # Actually, easier: use quadratic formula with these m, n values
    # or solve: (x + m/a)(x + n/c) or similar
    #
    # For simplicity: compute roots via formula
    # discriminant = b^2 - 4ac
    disc = b * b - 4 * a * c

    if disc < 0:
        return None

    sqrt_d = disc ** 0.5
    r1 = (-b - sqrt_d) / (2 * a)
    r2 = (-b + sqrt_d) / (2 * a)

    # Check if roots are (close to) integers
    if abs(r1 - round(r1)) < 1e-9 and abs(r2 - round(r2)) < 1e-9:
        r1 = float(round(r1))
        r2 = float(round(r2))
        return (min(r1, r2), max(r1, r2))

    # Check for simple rationals like -0.5
    # Allow roots if they're "nice" (integer or simple fraction like ±0.5, ±1/3, etc.)
    # For now, accept if close enough to integer or half-integer
    eps = 1e-9
    r1_frac = r1 * 2.0
    r2_frac = r2 * 2.0

    if (abs(r1 - round(r1)) < eps or abs(r1_frac - round(r1_frac)) < eps) and \
       (abs(r2 - round(r2)) < eps or abs(r2_frac - round(r2_frac)) < eps):
        # Accept: round to nearest 0.5
        r1 = round(r1 * 2.0) / 2.0
        r2 = round(r2 * 2.0) / 2.0
        return (min(r1, r2), max(r1, r2))

    return None


def roots_match_choice(roots: Optional[Tuple[float, float]], choice_text: str) -> bool:
    """
    Check if roots match choice text, order-insensitive.

    Reused from solve_formula.py: order-insensitive,
    handles "(a,b)" and "{a,b}" formats.

    Args:
        roots: Tuple (r1, r2) or None
        choice_text: Text like "(2, 3)" or "{-0.5, 3}"

    Returns:
        True if match, False otherwise
    """
    if roots is None:
        return False

    import re
    import unicodedata

    # Normalize
    text = unicodedata.normalize("NFKC", choice_text).lower()
    text = text.replace("\u2212", "-").replace("\u2013", "-").replace("\u2014", "-")
    text = re.sub(r"\s+", " ", text).strip()

    # Normalize brackets
    text = text.replace("{", "(").replace("}", ")")

    # Extract numbers
    m = re.match(r"^\(\s*([+\-]?[0-9]+(?:\.[0-9]+)?)\s*,\s*([+\-]?[0-9]+(?:\.[0-9]+)?)\s*\)$", text)
    if not m:
        return False

    a = float(m.group(1))
    b = float(m.group(2))

    r1, r2 = roots

    # Unordered comparison
    eps = 1e-6
    return (
        (abs(a - r1) < eps and abs(b - r2) < eps) or
        (abs(a - r2) < eps and abs(b - r1) < eps)
    )
