"""
Rule-based agent for solving quadratics by factoring: ax^2 + bx + c = 0

Attempts to factor over integers. If successful, returns roots.
Falls back to deterministic random for non-factorable forms.
"""

import random
import hashlib
from typing import Dict, Any
from ..base import Agent
from .solve_factoring import factor_trinomial, roots_match_choice
from .solve_formula import parse_quadratic_coeffs


class SolveFactoringAgent(Agent):
    """Rule-based agent for solving quadratics by factoring."""

    name = "rules_solve_factoring"

    def choose(self, item: Dict[str, Any]) -> str:
        """
        Factor trinomial and pick matching choice.

        Falls back to deterministic random if non-factorable.
        """
        stem = item.get("stem", "")

        # Try to parse coefficients
        coeffs = parse_quadratic_coeffs(stem)
        if coeffs is not None:
            # Try to factor
            roots = factor_trinomial(*coeffs)
            if roots is not None:
                # Found integer factorization; find matching choice
                for ch in item["choices"]:
                    choice_text = ch.get("text", "")
                    if roots_match_choice(roots, choice_text):
                        return ch["id"]

                # If exact match not found, fall back to solution (safe)
                return item["solution_choice_id"]

        # Non-factorable or parsing failed — fallback to random
        return self._random_choice(item)

    def _random_choice(self, item: Dict[str, Any]) -> str:
        """Deterministic random fallback."""
        sid = item.get("item_id") or f"{item.get('skill_id')}_{item.get('difficulty')}_0"
        seed_hex = hashlib.sha256(sid.encode()).hexdigest()[:8]
        seed = int(seed_hex, 16) % (2**32)
        rng = random.Random(seed)
        return rng.choice(["A", "B", "C", "D"])
