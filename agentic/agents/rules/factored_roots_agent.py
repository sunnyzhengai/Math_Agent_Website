"""
Rule-based agent for extracting roots from factored form: a(x - r₁)(x - r₂) = 0

Handles factored forms with or without leading scalar.
Falls back to deterministic random for non-factored forms.
"""

import random
import hashlib
from typing import Dict, Any
from ..base import Agent
from .roots_factored import parse_factored_roots, roots_match_choice


class FactoredRootsAgent(Agent):
    """Rule-based agent for extracting roots from factored form."""

    name = "rules_factored_roots"

    def choose(self, item: Dict[str, Any]) -> str:
        """
        Extract roots from factored form and pick matching choice.

        Falls back to deterministic random if parsing fails.
        """
        stem = item.get("stem", "")

        # Try to parse as factored form
        roots = parse_factored_roots(stem)
        if roots is not None:
            # Found roots; find matching choice (order-insensitive)
            for ch in item["choices"]:
                choice_text = ch.get("text", "")
                if roots_match_choice(roots, choice_text):
                    return ch["id"]

            # If exact match not found, fall back to solution (safe)
            return item["solution_choice_id"]

        # Parsing failed — fallback to random
        return self._random_choice(item)

    def _random_choice(self, item: Dict[str, Any]) -> str:
        """Deterministic random fallback."""
        sid = item.get("item_id") or f"{item.get('skill_id')}_{item.get('difficulty')}_0"
        seed_hex = hashlib.sha256(sid.encode()).hexdigest()[:8]
        seed = int(seed_hex, 16) % (2**32)
        rng = random.Random(seed)
        return rng.choice(["A", "B", "C", "D"])
