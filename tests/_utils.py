# tests/_utils.py

import re
import unicodedata

def norm_stem(s: str) -> str:
    """Normalize stem for comparison (NFKC, strip, lowercase)."""
    return unicodedata.normalize("NFKC", (s or "")).strip().lower()

# Crude ax^2 + bx + c parser (space-tolerant, signs okay). Assumes x is the variable.
_QUAD_RE = re.compile(
    r"""^\s*y\s*=\s*
        (?P<a>[+-]?\d+)\s*\*\s*x\^2
        \s*([+−-])\s*(?P<b>\d+)\s*\*\s*x
        \s*([+−-])\s*(?P<c>\d+)\s*\.?\s*$""",
    re.VERBOSE | re.IGNORECASE
)

def parse_standard_form(stem: str):
    """Parse standard form y = ax^2 + bx + c from a stem string.
    
    Returns tuple (a, b, c) or None if parse fails.
    Handles implicit a=1, various spacing, and Unicode minus signs.
    """
    import re
    
    # Normalize the stem
    s = norm_stem(stem).replace("−", "-")
    
    # Extract just the equation part (y = ...)
    # Look for "y = " and take everything after
    eq_match = re.search(r'y\s*=\s*(.+?)\.?\s*$', s)
    if not eq_match:
        return None
    
    eq = eq_match.group(1).strip()
    
    # Normalize forms:
    # "x^2 - 4x + 1" -> "1*x^2 - 4*x + 1"
    # "2x^2 - 8x + 3" -> "2*x^2 - 8*x + 3"
    
    # First: insert implicit 1 for standalone x^2
    eq = re.sub(r'^x\^2', '1*x^2', eq)  # Start of string
    eq = re.sub(r'(\s)x\^2', r'\g<1>1*x^2', eq)  # After space
    eq = re.sub(r'([-+])x\^2', r'\g<1>1*x^2', eq)  # After sign
    
    # Second: add * before x (not x^)
    eq = re.sub(r'(\d)x(?!\^)', r'\g<1>*x', eq)
    
    # Now the equation should be like: "1*x^2 - 4*x + 1" or "2*x^2 - 8*x + 3"
    # Match: [+-]? coeff*x^2 [+-] coeff*x [+-] constant
    m = re.match(r'([+-]?\d+)\*x\^2\s*([+-])\s*(\d+)\*x\s*([+-])\s*(\d+)', eq)
    
    if not m:
        return None
    
    a = int(m.group(1))
    b_sign = -1 if m.group(2) == "-" else 1
    b = b_sign * int(m.group(3))
    c_sign = -1 if m.group(4) == "-" else 1
    c = c_sign * int(m.group(5))
    
    return a, b, c
