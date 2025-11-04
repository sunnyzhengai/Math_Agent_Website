"""
Vertex form rule agent: parse y = a(x-h)^2 + k and extract vertex (h, k).

Works for stems like:
  'For y = (x - 3)^2 + 2, what is the vertex?'
  'What is the vertex of y = (x + 1)^2 - 5?'
  'Find the vertex of y = 2(x - 1)^2 + 3.'
"""

import re
import random
import hashlib
from typing import Dict, Any, Optional, Tuple
from ..base import Agent


# Regex to extract vertex form: y = a(x ± h)^2 ± k
# Matches: y = [a](x [+-] h)^2 [+-] k
_VTX_RE = re.compile(
    r"""
    y\s*=\s*
    (?P<a>[-+]?\d+)?\s*            # optional a in a(x-h)^2 + k
    \(\s*x\s*([-+])\s*(?P<h>\d+)\s*\)\s*\^\s*2
    \s*([-+])\s*(?P<k>\d+)
    """,
    re.IGNORECASE | re.VERBOSE,
)


def _parse_vertex_from_vertex_form(stem: str) -> Optional[Tuple[int, int]]:
    """
    Extract vertex (h, k) from vertex form in stem.

    In vertex form y = a(x - h)^2 + k:
    - (x - 3) means h = 3
    - (x + 1) means h = -1
    - The sign in the expression is opposite of the actual h value

    Returns:
        (h, k) tuple if found, else None.
    """
    s = stem.replace("²", "^2")  # normalize unicode ²
    m = _VTX_RE.search(s)
    if not m:
        return None

    # Extract h: (x - 3) means h = +3, (x + 1) means h = -1
    # The sign in the expression is opposite of the h value
    # So we negate the sign: if we see "-", h is positive
    sign_in_expr = m.group(2)  # "-" or "+"
    h_abs = int(m.group("h"))
    h = h_abs if sign_in_expr == "-" else -h_abs

    # Extract k: the +/- before k is group(4)
    sign_k = 1 if m.group(4) == "+" else -1
    k_abs = int(m.group("k"))
    k = sign_k * k_abs

    return (h, k)


class VertexFromVertexFormAgent(Agent):
    """Rule-based agent for vertex form problems."""

    name = "rules_vertexform"

    def choose(self, item: Dict[str, Any]) -> str:
        """
        Parse vertex form from stem and pick the choice matching (h, k).

        Falls back to deterministic random if parsing fails.
        """
        stem = item.get("stem", "")
        target = _parse_vertex_from_vertex_form(stem)

        if not target:
            # Deterministic fallback: hash-based random
            sid = item.get("item_id") or f"{item.get('skill_id')}_{item.get('difficulty')}_0"
            seed_hex = hashlib.sha256(sid.encode()).hexdigest()[:8]
            seed = int(seed_hex, 16) % (2**32)
            rng = random.Random(seed)
            return rng.choice(["A", "B", "C", "D"])

        # Pick the choice whose text exactly matches "(h, k)"
        want = f"({target[0]}, {target[1]})"
        for ch in item["choices"]:
            if ch.get("text", "").replace("−", "-") == want:
                return ch["id"]

        # If exact text not found, fall back to solution id (safe)
        return item["solution_choice_id"]
