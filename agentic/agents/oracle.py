"""
Oracle agent: always picks the correct answer.

This is the upper bound for all agents and serves as a regression guard
for the item generation and grading pipeline.
"""

from typing import Dict, Any
from .base import Agent


class OracleAgent(Agent):
    """Oracle agent that always picks the correct answer."""

    name = "oracle"

    def choose(self, item: Dict[str, Any]) -> str:
        """
        Return the correct choice ID.

        Args:
            item: Question item dict.

        Returns:
            The solution_choice_id (the correct answer).
        """
        return item["solution_choice_id"]
