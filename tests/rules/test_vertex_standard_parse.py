r"""
Unit tests for parsing standard-form quadratics: y = ax^2 + bx + c

CONTRACT:
  parse_standard_quadratic(stem: str) -> tuple[float, float, float]
  Returns (a, b, c) for a quadratic y = ax^2 + bx + c

Parsing rules:
  - Normalization: NFKC, lowercase, collapse whitespace
  - Fast rejection: parentheses, non-x variables, powers ≠ 2, no x^2 term
  - Three passes: extract quadratic a, linear b, constant c (order-independent)
  - Post-condition: a != 0 (must be quadratic)
  - Missing b or c terms are treated as 0.0

REGEX SPEC:
  Normalization:
    import unicodedata, re
    text = unicodedata.normalize("NFKC", stem).lower()
    text = text.replace(chr(0x2212), "-")  # Unicode minus to ASCII hyphen
    text = re.sub(r"\s+", " ", text).strip()

  Fast rejection (fail if any of these):
    - Parentheses: r"[()]"
    - Non-x variables: r"[a-wyz]"
    - Powers other than 2: r"x\s*\^\s*(?!2)\d+"
    - Division: r"/"
    - No x^2 term: not r"x\s*\^\s*2"

  Three-pass extraction:
    1. Quadratic (a): r"(?P<sign>[+\-]?)\s*(?:(?P<coef>\d+(?:\.\d+)?)\s*)?x\s*\^\s*2"
    2. Linear (b):   r"(?P<sign>[+\-]?)\s*(?:(?P<coef>\d+(?:\.\d+)?)\s*)?x(?!\s*\^)"
    3. Constant (c): r"(?P<sign>[+\-]?)\s*(?P<num>\d+(?:\.\d+)?)\b"
       (after removing matched a and b substrings from working copy)
"""

import pytest
from agentic.agents.rules.vertex_standard import parse_standard_quadratic


CASES = [
    # Basic cases
    ("Find the vertex of y = x^2 - 4x + 7.", (1.0, -4.0, 7.0)),
    ("Find vertex: y = -x^2 + 4x + 1", (-1.0, 4.0, 1.0)),
    ("y = 2x^2 + 3x - 5", (2.0, 3.0, -5.0)),
    
    # Decimal coefficients
    ("y = 0.5x^2 - 1.25x + 0.75", (0.5, -1.25, 0.75)),
    
    # Missing terms (b or c optional)
    ("y = x^2 + 7", (1.0, 0.0, 7.0)),       # missing bx
    ("y = x^2 - 4x", (1.0, -4.0, 0.0)),     # missing c
    ("y = x^2", (1.0, 0.0, 0.0)),           # only quadratic
    
    # Whitespace variations
    ("y = -x^2  +   4x   - 9", (-1.0, 4.0, -9.0)),
    
    # Unicode minus (U+2212)
    ("y = −x^2 + 2x − 3", (-1.0, 2.0, -3.0)),
    
    # Reordered terms
    ("y = 3x - 5 + 2x^2", (2.0, 3.0, -5.0)),
    ("y = 7 + 3x - x^2", (-1.0, 3.0, 7.0)),
    ("y = -4x + 1 - x^2", (-1.0, -4.0, 1.0)),
    
    # Implicit coefficients
    ("y = x^2 + x + 1", (1.0, 1.0, 1.0)),
    ("y = -x^2 + x", (-1.0, 1.0, 0.0)),
]


@pytest.mark.parametrize("stem, expected", CASES)
def test_parse_standard_quadratic_ok(stem, expected):
    """Verify parse_standard_quadratic extracts (a, b, c) correctly."""
    a, b, c = parse_standard_quadratic(stem)
    
    assert pytest.approx(a, rel=1e-9, abs=1e-12) == expected[0]
    assert pytest.approx(b, rel=1e-9, abs=1e-12) == expected[1]
    assert pytest.approx(c, rel=1e-9, abs=1e-12) == expected[2]


BAD_INPUTS = [
    ("Find the vertex of y = (x-2)^2 + 5", "parentheses (vertex form, not standard)"),
    ("y = 5x + 7", "linear, not quadratic (no x^2)"),
    ("vertex of y = x^3 - 3x + 1", "cubic (x^3)"),
    ("y = ax^2 + bx + c", "non-numeric coefficients"),
    ("y = x^2 + (3/2)x + 1", "fraction (division)"),
    ("y = ", "empty"),
    ("What is the answer?", "no equation"),
]


@pytest.mark.parametrize("bad, reason", BAD_INPUTS)
def test_parse_standard_quadratic_bad_inputs(bad, reason):
    """Verify parse_standard_quadratic rejects invalid forms."""
    with pytest.raises(ValueError):
        parse_standard_quadratic(bad)
