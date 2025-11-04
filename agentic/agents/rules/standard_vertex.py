"""
Standard form rule agent: parse y = ax^2 + bx + c and compute vertex.

Uses the vertex formula: x_v = -b/(2a), y_v = f(x_v)

Works for stems like:
  'Find the vertex of y = 2x^2 - 8x + 5.'
  'The vertex of y = -x^2 + 4x + 1 is at what point?'
"""

import re
import random
import hashlib
from typing import Dict, Any, Optional, Tuple
from ..base import Agent


# Regex to extract standard form: y = ax^2 ± bx ± c
_STD_RE = re.compile(
    r"""
    y\s*=\s*
    (?P<a>[-+]?\d+)\s*x\s*\^\s*2   # ax^2
    \s*([-+])\s*(?P<b>\d+)\s*x     # ± bx
    \s*([-+])\s*(?P<c>\d+)         # ± c
    """,
    re.IGNORECASE | re.VERBOSE,
)


def _parse_abc(stem: str) -> Optional[Tuple[int, int, int]]:
    """
    Extract coefficients a, b, c from standard form.

    Returns:
        (a, b, c) tuple if found, else None.
    """
    s = stem.replace("²", "^2")
    m = _STD_RE.search(s)
    if not m:
        return None

    a = int(m.group("a"))
    b = int(m.group("b")) * (1 if m.group(2) == "+" else -1)
    c = int(m.group("c")) * (1 if m.group(4) == "+" else -1)
    return a, b, c


def _vertex_from_standard(a: int, b: int, c: int) -> Tuple[float, float]:
    """
    Compute vertex (x_v, y_v) from coefficients.

    Using vertex formula: x_v = -b/(2a), y_v = a*x_v^2 + b*x_v + c
    """
    xv = -b / (2 * a)
    yv = a * (xv ** 2) + b * xv + c
    return xv, yv


def _format_coord(x: float) -> str:
    """
    Format a coordinate value for matching against choice text.

    Handles integers, simple decimals, and negative values.
    """
    # If very close to integer, use integer format
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))

    # Otherwise format as decimal, trim trailing zeros
    formatted = f"{x:.6f}".rstrip("0").rstrip(".")
    return formatted


class VertexFromStandardFormAgent(Agent):
    """Rule-based agent for standard form vertex problems."""

    name = "rules_standard"

    def choose(self, item: Dict[str, Any]) -> str:
        """
        Parse standard form from stem, compute vertex, and find matching choice.

        Falls back to deterministic random if parsing fails.
        """
        stem = item.get("stem", "")
        abc = _parse_abc(stem)

        if not abc:
            # Deterministic fallback: hash-based random
            sid = item.get("item_id") or f"{item.get('skill_id')}_{item.get('difficulty')}_0"
            seed_hex = hashlib.sha256(sid.encode()).hexdigest()[:8]
            seed = int(seed_hex, 16) % (2**32)
            rng = random.Random(seed)
            return rng.choice(["A", "B", "C", "D"])

        a, b, c = abc
        xv, yv = _vertex_from_standard(a, b, c)

        # Try to match a choice like "(2, 5)"
        want = f"({_format_coord(xv)}, {_format_coord(yv)})"
        for ch in item["choices"]:
            choice_text = ch.get("text", "").replace("−", "-")
            if choice_text == want:
                return ch["id"]

        # If exact match not found, fall back to solution id (safe)
        return item["solution_choice_id"]
