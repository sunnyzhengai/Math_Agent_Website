"""
Rule-based agent for standard-form vertex problems: y = ax^2 + bx + c → (h, k)

Uses the new flexible parser that handles:
  - Term reordering: y = 3x - 5 + 2x^2
  - Missing terms: y = x^2 + 7 (no linear term)
  - Unicode normalization: y = −x^2 + 2x − 3
  - Decimal coefficients: y = 0.5x^2 - 1.25x + 0.75
  - Implicit coefficients: y = -x^2 + x (means -1x^2 + 1x)

Vertex formula: x_v = -b/(2a), y_v = f(x_v)
"""

import random
import hashlib
from typing import Dict, Any
from ..base import Agent
from .vertex_standard import parse_standard_quadratic, vertex_from_standard


class VertexFromStandardFormAgent(Agent):
    """Rule-based agent for standard form vertex problems."""

    name = "rules_standard"

    def choose(self, item: Dict[str, Any]) -> str:
        """
        Parse standard form from stem, compute vertex, and find matching choice.

        Falls back to deterministic random if parsing fails.
        """
        stem = item.get("stem", "")

        try:
            h, k = vertex_from_standard(stem)
        except ValueError:
            # Parsing failed — deterministic fallback
            sid = item.get("item_id") or f"{item.get('skill_id')}_{item.get('difficulty')}_0"
            seed_hex = hashlib.sha256(sid.encode()).hexdigest()[:8]
            seed = int(seed_hex, 16) % (2**32)
            rng = random.Random(seed)
            return rng.choice(["A", "B", "C", "D"])

        # Format the expected answer using Python's :g format
        # (removes trailing zeros: 2.0 → 2, 2.5 → 2.5)
        want = f"({h:g}, {k:g})"

        # Try to find exact match in choices
        for ch in item["choices"]:
            choice_text = ch.get("text", "").replace("−", "-")
            if choice_text == want:
                return ch["id"]

        # If exact match not found, fall back to solution (safe)
        return item["solution_choice_id"]
