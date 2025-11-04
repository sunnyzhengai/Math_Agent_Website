"""
Abstract base class for agent strategies.

All agents must implement choose(item) -> str where choice is in ['A','B','C','D'].
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class Agent(ABC):
    """Abstract base for agent strategies."""

    name: str = "base"

    @abstractmethod
    def choose(self, item: Dict[str, Any]) -> str:
        """
        Choose a response for a question item.

        Args:
            item: Question item dict with keys: stem, choices (list of dicts), solution_choice_id, etc.

        Returns:
            One of 'A', 'B', 'C', 'D' (choice ID).

        Raises:
            ValueError: If choice is invalid or unavailable.
        """
        raise NotImplementedError
