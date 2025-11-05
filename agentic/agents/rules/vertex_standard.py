"""
Rule-based agent for standard-form vertex problems: y = ax^2 + bx + c → (h, k)

Functions:
  parse_standard_quadratic(stem: str) -> tuple[float, float, float]
    Parses y = ax^2 + bx + c and returns (a, b, c)
  
  vertex_from_standard(stem: str) -> tuple[float, float]
    Computes vertex (h, k) using h = -b/(2a), k = f(h)

Implementation follows the regex spec:
  1. Normalization: NFKC, lowercase, collapse whitespace
  2. Fast rejection: parentheses, non-x variables, powers ≠ 2, no x^2
  3. Three passes: extract a, b, c independently (order-independent)
  4. Post-condition: a != 0
"""

import re
import unicodedata
from typing import Tuple


def parse_standard_quadratic(stem: str) -> Tuple[float, float, float]:
    """
    Parse standard form quadratic y = ax^2 + bx + c.
    
    Args:
        stem: Question stem (may contain extra text before/after equation)
    
    Returns:
        (a, b, c) as floats
    
    Raises:
        ValueError: If stem doesn't contain a valid standard-form quadratic
    """
    # 0) Normalization
    text = unicodedata.normalize("NFKC", stem).lower()
    # Explicit conversion of Unicode minus variants to ASCII hyphen
    text = text.replace("\u2212", "-").replace("\u2013", "-").replace("\u2014", "-")
    text = re.sub(r"\s+", " ", text).strip()
    
    # 1) Extract RHS after "y ="
    m = re.search(r"y\s*=\s*(.+)$", text)
    if not m:
        raise ValueError("no_equation")
    rhs = m.group(1)
    
    # 2) Fast rejection rules
    if re.search(r"[()]", rhs):
        raise ValueError("parentheses_detected")
    
    if re.search(r"[a-wyz]", rhs):
        raise ValueError("non_x_variable")
    
    if re.search(r"x\s*\^\s*(?!2)\d+", rhs):
        raise ValueError("power_not_2")
    
    if re.search(r"/", rhs):
        raise ValueError("division_detected")
    
    if not re.search(r"x\s*\^\s*2", rhs):
        raise ValueError("not_quadratic")
    
    # 3) Three-pass extraction with working string
    work = rhs
    
    # 3a) Quadratic terms (collect a)
    a = 0.0
    quad_pattern = r"(?P<sign>[+\-]?)\s*(?:(?P<coef>\d+(?:\.\d+)?)\s*)?x\s*\^\s*2"
    for match in re.finditer(quad_pattern, work):
        sgn = -1 if match.group("sign") == "-" else 1
        coef = float(match.group("coef")) if match.group("coef") else 1.0
        a += sgn * coef
        
        # Remove matched substring from working copy
        work = work[:match.start()] + " " * (match.end() - match.start()) + work[match.end():]
    
    # 3b) Linear terms (collect b)
    b = 0.0
    linear_pattern = r"(?P<sign>[+\-]?)\s*(?:(?P<coef>\d+(?:\.\d+)?)\s*)?x(?!\s*\^)"
    for match in re.finditer(linear_pattern, work):
        sgn = -1 if match.group("sign") == "-" else 1
        coef = float(match.group("coef")) if match.group("coef") else 1.0
        b += sgn * coef
        
        # Remove matched substring
        work = work[:match.start()] + " " * (match.end() - match.start()) + work[match.end():]
    
    # 3c) Constant terms (collect c)
    c = 0.0
    const_pattern = r"(?P<sign>[+\-]?)\s*(?P<num>\d+(?:\.\d+)?)\b"
    for match in re.finditer(const_pattern, work):
        sgn = -1 if match.group("sign") == "-" else 1
        num = float(match.group("num"))
        c += sgn * num
    
    # 4) Post-conditions
    if abs(a) < 1e-12:
        raise ValueError("a_is_zero")
    
    return (float(a), float(b), float(c))


def vertex_from_standard(stem: str) -> Tuple[float, float]:
    """
    Compute vertex (h, k) from standard form y = ax^2 + bx + c.
    
    Args:
        stem: Question stem containing a standard-form quadratic
    
    Returns:
        (h, k) where h = -b/(2a), k = f(h)
    
    Raises:
        ValueError: If stem doesn't contain a valid standard-form quadratic
    """
    a, b, c = parse_standard_quadratic(stem)
    
    h = -b / (2 * a)
    k = a * (h ** 2) + b * h + c
    
    return (h, k)
