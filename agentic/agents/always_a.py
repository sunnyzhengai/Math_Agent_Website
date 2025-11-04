"""
AlwaysA agent: always picks choice A.

This is a sanity check baseline. On average, this should achieve ~25% accuracy
(since answers are shuffled randomly). If accuracy is significantly different,
it indicates a problem with the question generation or choice shuffling.
"""

from typing import Dict, Any
from .base import Agent


class AlwaysAAgent(Agent):
    """Agent that always picks choice A."""

    name = "always_a"

    def choose(self, item: Dict[str, Any]) -> str:
        """
        Always return 'A'.

        Args:
            item: Question item dict (unused).

        Returns:
            'A' (first choice).
        """
        return "A"
