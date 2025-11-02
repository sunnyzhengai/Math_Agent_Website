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
    s = norm_stem(stem).replace("−", "-").replace(" + ", "+").replace(" - ", "-")
    
    # Handle implicit a=1 (e.g., "y = x^2 - 6x + 5")
    s = s.replace("y = x^2", "y = 1*x^2") \
         .replace("x^2 +", "1*x^2 +") \
         .replace("x^2 -", "1*x^2 -")
    
    m = _QUAD_RE.match(s)
    if not m:
        return None
    
    a = int(m.group("a"))
    b_sign = -1 if m.group(2) == "-" or m.group(2) == "−" else 1
    c_sign = -1 if m.group(4) == "-" or m.group(4) == "−" else 1
    b = b_sign * int(m.group("b"))
    c = c_sign * int(m.group("c"))
    
    return a, b, c
