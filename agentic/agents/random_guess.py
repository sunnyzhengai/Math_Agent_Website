"""
Random guess agent: picks a random choice deterministically per item.

Uses SHA256 hashing of item_id to derive a deterministic seed, ensuring
reproducibility across runs and processes (unlike Python's hash()).
"""

import random
import hashlib
from typing import Dict, Any
from .base import Agent


class RandomGuessAgent(Agent):
    """Agent that picks a random choice, deterministically per item."""

    name = "random"

    def choose(self, item: Dict[str, Any]) -> str:
        """
        Pick a random choice, deterministically per item.

        Uses SHA256 hash of item_id for reproducible pseudo-randomness
        across processes and runs.

        Args:
            item: Question item dict with 'item_id' field.

        Returns:
            One of 'A', 'B', 'C', 'D' chosen randomly (but deterministically).
        """
        # Derive deterministic seed from item_id
        # Use item_id if present; fallback to skill:difficulty:0 if not
        sid = item.get("item_id")
        if not sid:
            sid = f"{item.get('skill_id')}_{item.get('difficulty')}_0"

        # Hash to deterministic seed (SHA256 is cross-process stable)
        seed_hex = hashlib.sha256(sid.encode()).hexdigest()[:8]
        seed = int(seed_hex, 16) % (2**32)

        # Create local RNG with deterministic seed
        rng = random.Random(seed)
        return rng.choice(["A", "B", "C", "D"])
