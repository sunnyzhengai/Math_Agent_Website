"""
Unit tests for vertex computation: y = ax^2 + bx + c → (h, k)

CONTRACT:
  vertex_from_standard(stem: str) -> tuple[float, float]

Implementation:
  1. Call parse_standard_quadratic(stem) to get (a, b, c)
  2. Compute h = -b / (2a)
  3. Compute k = a*h^2 + b*h + c
  4. Return (h, k) as unrounded floats
  5. Raises ValueError for invalid stems

Formula background:
  For y = ax^2 + bx + c, the vertex (h, k) is found by:
  - h = -b/(2a)  [x-coordinate of axis of symmetry]
  - k = f(h)     [y-value at the vertex]
"""

import math
import pytest
from agentic.agents.rules.vertex_standard import vertex_from_standard


CASES_VERTEX = [
    # From your UI example: y = -x^2 + 4x + 1 → vertex at (2, 5)
    ("Find the vertex of y = -x^2 + 4x + 1.", (2.0, 5.0)),
    
    # Standard cases
    ("Find vertex: y = x^2 - 4x + 7", (2.0, 3.0)),
    
    # Decimal coefficients
    # y = 0.5x^2 - 1.25x + 0.75
    # h = 1.25 / 1.0 = 1.25
    # k = 0.5*(1.25)^2 - 1.25*1.25 + 0.75 = 0.78125 - 1.5625 + 0.75 = -0.03125
    ("y = 0.5x^2 - 1.25x + 0.75", (1.25, -0.03125)),
    
    # Vertex at origin
    ("y = x^2 + 7", (0.0, 7.0)),  # b=0 → h=0, k=7
    
    # Unicode minus
    ("y = −x^2 + 2x − 3", (1.0, -2.0)),  # h = -2/-2 = 1, k = -1+2-3 = -2
    
    # Reordered terms
    # y = 7 + 3x - x^2  →  a=-1, b=3, c=7
    # h = -3 / (2*-1) = -3 / -2 = 1.5
    # k = -1*(1.5)^2 + 3*1.5 + 7 = -2.25 + 4.5 + 7 = 9.25
    ("y = 7 + 3x - x^2", (1.5, 9.25)),
]


@pytest.mark.parametrize("stem, expected", CASES_VERTEX)
def test_vertex_from_standard_ok(stem, expected):
    """Verify vertex_from_standard computes (h, k) correctly."""
    h, k = vertex_from_standard(stem)
    
    eh, ek = expected
    
    # Check that outputs are finite
    assert math.isfinite(h), f"h must be finite, got {h}"
    assert math.isfinite(k), f"k must be finite, got {k}"
    
    # Check accuracy
    assert pytest.approx(h, rel=1e-9, abs=1e-12) == eh
    assert pytest.approx(k, rel=1e-9, abs=1e-12) == ek


BAD_INPUTS_VERTEX = [
    "Find the vertex of y = (x-2)^2 + 5",  # vertex form, not standard
    "y = 5x + 7",                          # linear, not quadratic
    "y = x^3 - 3x + 1",                    # cubic
    "What is the vertex?",                 # no equation
]


@pytest.mark.parametrize("bad", BAD_INPUTS_VERTEX)
def test_vertex_from_standard_bad_inputs(bad):
    """Verify vertex_from_standard rejects invalid forms."""
    with pytest.raises(ValueError):
        vertex_from_standard(bad)
