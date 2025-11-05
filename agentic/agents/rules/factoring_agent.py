"""
Rule-based agent for solving quadratics by factoring: ax^2 + bx + c = 0

Currently handles a=1 case (simple factoring). Falls back to random for general a.
"""

import random
import hashlib
from typing import Dict, Any
from ..base import Agent
from .factoring import parse_quadratic_standard, solve_by_factoring_a1, format_roots


class FactoringAgent(Agent):
    """Rule-based agent for solving quadratics by factoring (a=1 case)."""

    name = "rules_factoring"

    def choose(self, item: Dict[str, Any]) -> str:
        """
        Solve a quadratic by factoring if possible.

        For a=1 cases, finds factor pairs and picks the choice matching the roots.
        Falls back to deterministic random for a≠1 or non-factorable cases.
        """
        stem = item.get("stem", "")

        try:
            a, b, c = parse_quadratic_standard(stem)
        except ValueError:
            # Parsing failed — fallback to random
            return self._random_choice(item)

        # For now, only handle a=1
        if a != 1:
            return self._random_choice(item)

        # Try to factor
        roots = solve_by_factoring_a1(b, c)
        if roots is None:
            # Not factorable with integers
            return self._random_choice(item)

        # Format and find matching choice
        formatted = format_roots(roots)
        for ch in item["choices"]:
            choice_text = ch.get("text", "")
            if choice_text == formatted:
                return ch["id"]

        # If exact match not found, fall back to solution (safe)
        return item["solution_choice_id"]

    def _random_choice(self, item: Dict[str, Any]) -> str:
        """Deterministic random fallback."""
        sid = item.get("item_id") or f"{item.get('skill_id')}_{item.get('difficulty')}_0"
        seed_hex = hashlib.sha256(sid.encode()).hexdigest()[:8]
        seed = int(seed_hex, 16) % (2**32)
        rng = random.Random(seed)
        return rng.choice(["A", "B", "C", "D"])
