"""
Rule-based factoring agent for solving quadratics by factoring: ax^2 + bx + c = 0

Supports:
  - Simple a=1 case: find (p,q) where p*q=c and p+q=b, roots are -p, -q
  - General a: AC-method (find (m,n) where m*n=ac and m+n=b)

Conservative approach: only fires when clean integer factors exist.
Falls back to random on parse failure or when no integer factors exist.
"""

import re
import unicodedata
from typing import Optional, Tuple


def _normalize(s: str) -> str:
    """Normalize text: NFKC, lowercase, collapse whitespace."""
    s = unicodedata.normalize("NFKC", s).lower()
    s = s.replace("\u2212", "-").replace("\u2013", "-").replace("\u2014", "-")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def parse_quadratic_standard(stem: str) -> Optional[Tuple[int, int, int]]:
    """
    Extract a, b, c from stem like "Solve: x^2 + 5x + 6 = 0"

    Returns:
        (a, b, c) as ints, or None if not in standard form

    Raises:
        ValueError if parsing fails
    """
    s = _normalize(stem)

    # Find the part before "= 0"
    m = re.search(r"([^=]+)=\s*0", s)
    if not m:
        raise ValueError("no_equation_format")

    expr = m.group(1).strip()

    # Extract quadratic term (a x^2)
    am = re.search(r"([+\-]?\d*)\s*x\s*\^\s*2", expr)
    if not am:
        raise ValueError("not_quadratic")

    a_txt = am.group(1)
    if a_txt in ("", "+"):
        a = 1
    elif a_txt == "-":
        a = -1
    else:
        a = int(a_txt)

    if a == 0:
        raise ValueError("a_is_zero")

    # Extract linear term (b x), with lookahead to avoid x^2
    bm = re.search(r"([+\-]?\d*)\s*x(?!\s*\^)", expr)
    b = 0
    if bm:
        b_txt = bm.group(1)
        if b_txt in ("", "+"):
            b = 1
        elif b_txt == "-":
            b = -1
        else:
            b = int(b_txt)

    # Extract constant term using three-pass approach (like vertex_standard.py):
    # 1. Remove a x^2 term
    # 2. Remove b x term
    # 3. Extract remaining numbers
    work = expr
    
    # Remove quadratic terms
    work = re.sub(r"[+\-]?\d*\s*x\s*\^\s*2", "", work)
    
    # Remove linear terms
    work = re.sub(r"[+\-]?\d*\s*x(?!\s*\^)", "", work)
    
    # Find all signed numbers in what remains
    c = 0
    for match in re.finditer(r"([+\-])\s*(\d+)", work):
        sign = -1 if match.group(1) == "-" else 1
        num = int(match.group(2))
        c += sign * num

    return (a, b, c)


def factor_a1(b: int, c: int) -> Optional[Tuple[int, int]]:
    """
    Find (p, q) such that p*q = c and p+q = b.

    Returns:
        (p, q) tuple if found, else None
    """
    if c == 0:
        # Special case: x^2 + bx = 0 => x(x+b) = 0 => roots 0, -b
        return (0, b)

    # Enumerate factor pairs of c
    for p in range(-abs(c), abs(c) + 1):
        if p == 0:
            continue
        if c % p != 0:
            continue
        q = c // p
        if p + q == b:
            return (p, q)

    return None


def factor_general_ac(a: int, b: int, c: int) -> Optional[Tuple[int, int]]:
    """
    AC method: find (m, n) where m*n = a*c and m+n = b.

    Returns:
        (m, n) tuple if found, else None (caller can rewrite and factor)
    """
    ac = a * c

    if ac == 0:
        # Degenerate case; let caller handle
        return None

    # Enumerate factor pairs of ac
    limit = abs(ac)
    for m in range(-limit, limit + 1):
        if m == 0:
            continue
        if ac % m != 0:
            continue
        n = ac // m
        if m + n == b:
            return (m, n)

    return None


def solve_by_factoring_a1(b: int, c: int) -> Optional[Tuple[int, int]]:
    """
    Solve x^2 + bx + c = 0 by factoring (a=1 case).

    Returns:
        Sorted tuple of roots (as ints) if factorable, else None
    """
    pair = factor_a1(b, c)
    if not pair:
        return None

    p, q = pair
    # (x + p)(x + q) = 0 => x = -p or x = -q
    root1, root2 = -p, -q
    return tuple(sorted([root1, root2]))


def format_roots(roots: Tuple[int, int]) -> str:
    """
    Format roots as "x = r1 and x = r2" (sorted).

    Example: (2, 3) -> "x = 2 and x = 3"
    """
    r1, r2 = sorted(roots)
    return f"x = {r1} and x = {r2}"
