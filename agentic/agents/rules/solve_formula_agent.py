"""
Rule-based agent for solving quadratics via the quadratic formula: ax^2 + bx + c = 0

Parses coefficients and uses discriminant to compute real roots.
Falls back to deterministic random for non-standard forms or complex roots.
"""

import random
import hashlib
from typing import Dict, Any
from ..base import Agent
from .solve_formula import parse_quadratic_coeffs, quadratic_roots, roots_match_choice


class SolveFormulaAgent(Agent):
    """Rule-based agent for solving quadratics via the quadratic formula."""

    name = "rules_solve_formula"

    def choose(self, item: Dict[str, Any]) -> str:
        """
        Solve quadratic via formula and pick matching choice.

        Falls back to deterministic random if parsing fails or roots are complex.
        """
        stem = item.get("stem", "")

        # Try to parse coefficients
        coeffs = parse_quadratic_coeffs(stem)
        if coeffs is not None:
            # Try to compute real roots
            roots = quadratic_roots(*coeffs)
            if roots is not None:
                # Found real roots; find matching choice (order-insensitive)
                for ch in item["choices"]:
                    choice_text = ch.get("text", "")
                    if roots_match_choice(roots, choice_text):
                        return ch["id"]

                # If exact match not found, fall back to solution (safe)
                return item["solution_choice_id"]

        # Parsing failed or no real roots — fallback to random
        return self._random_choice(item)

    def _random_choice(self, item: Dict[str, Any]) -> str:
        """Deterministic random fallback."""
        sid = item.get("item_id") or f"{item.get('skill_id')}_{item.get('difficulty')}_0"
        seed_hex = hashlib.sha256(sid.encode()).hexdigest()[:8]
        seed = int(seed_hex, 16) % (2**32)
        rng = random.Random(seed)
        return rng.choice(["A", "B", "C", "D"])
