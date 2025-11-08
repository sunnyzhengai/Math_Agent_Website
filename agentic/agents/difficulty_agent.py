"""
Difficulty Agent: Estimates question difficulty based on complexity.

Analyzes mathematical complexity, required operations, and coefficient
sizes to estimate whether a question matches its labeled difficulty level.
"""

import re
from typing import Dict, Any
from .base import Agent


class DifficultyAgent(Agent):
    """Estimates question difficulty based on complexity."""

    name = "difficulty_estimator"

    # Difficulty level mappings
    DIFFICULTY_MAP = {
        "easy": 0.25,
        "medium": 0.5,
        "hard": 0.75,
        "applied": 0.85
    }

    def estimate(self, question: Dict[str, Any]) -> float:
        """
        Returns estimated difficulty 0-1 (easy=0.25, medium=0.5, hard=0.75, applied=0.85).

        Args:
            question: Question item dict with stem, skill_id, etc.

        Returns:
            Float difficulty estimate between 0.0 and 1.0
        """
        stem = question.get("stem", "")
        skill_id = question.get("skill_id", "")

        # Base difficulty by skill type
        difficulty_score = 0.3  # Default: easy-medium

        # Factor 1: Skill complexity
        if "factored" in skill_id or "vertex_form" in skill_id:
            difficulty_score += 0.0  # Reading from standard form is easier
        elif "by_factoring" in skill_id:
            difficulty_score += 0.2  # Factoring requires more steps
        elif "by_formula" in skill_id:
            difficulty_score += 0.25  # Quadratic formula is complex
        elif "complete.square" in skill_id:
            difficulty_score += 0.3  # Completing square is advanced
        elif "discriminant" in skill_id:
            difficulty_score += 0.15  # Analysis skill
        elif "standard.vertex" in skill_id:
            difficulty_score += 0.1  # Conversion required

        # Factor 2: Number of variables in problem
        # More variables = more complex
        variables = set(re.findall(r'[a-z]', stem.lower()))
        # Remove common words that aren't variables
        variables.discard('a')  # Could be article "a"
        variables.discard('o')  # From "of", "to", etc.
        difficulty_score += len(variables) * 0.05

        # Factor 3: Coefficient complexity
        # Large numbers make arithmetic harder
        numbers = re.findall(r'-?\d+', stem)
        if numbers:
            max_num = max(abs(int(n)) for n in numbers)
            if max_num > 100:
                difficulty_score += 0.2  # Very large coefficients
            elif max_num > 20:
                difficulty_score += 0.1  # Moderately large
            elif max_num > 10:
                difficulty_score += 0.05  # Slightly large

        # Factor 4: Negative coefficients (more error-prone)
        negative_count = len(re.findall(r'-\d+', stem))
        difficulty_score += negative_count * 0.03

        # Factor 5: Fractions present
        if '/' in stem or 'frac' in stem:
            difficulty_score += 0.15  # Fractions increase difficulty

        # Factor 6: Multiple steps required (compound operations)
        operation_keywords = [
            'solve', 'find', 'determine', 'calculate', 'identify'
        ]
        keyword_count = sum(1 for kw in operation_keywords if kw.lower() in stem.lower())
        if keyword_count > 1:
            difficulty_score += 0.1  # Multi-step problem

        # Factor 7: Applied/word problems (context makes it harder)
        context_words = [
            'ball', 'height', 'object', 'projectile', 'area',
            'garden', 'fence', 'profit', 'cost', 'revenue'
        ]
        has_context = any(word in stem.lower() for word in context_words)
        if has_context:
            difficulty_score += 0.15  # Applied context

        # Clamp to valid range
        return max(0.0, min(1.0, difficulty_score))

    def get_difficulty_label(self, score: float) -> str:
        """
        Convert numeric difficulty to label.

        Args:
            score: Difficulty score 0-1

        Returns:
            "easy", "medium", "hard", or "applied"
        """
        if score < 0.375:
            return "easy"
        elif score < 0.625:
            return "medium"
        elif score < 0.8:
            return "hard"
        else:
            return "applied"

    def matches_target(self, question: Dict[str, Any], tolerance: float = 0.2) -> bool:
        """
        Check if estimated difficulty matches target difficulty.

        Args:
            question: Question item with target difficulty
            tolerance: Acceptable difference (default 0.2 on 0-1 scale)

        Returns:
            True if within tolerance, False otherwise
        """
        estimated = self.estimate(question)
        target_label = question.get("difficulty", "easy")
        target_score = self.DIFFICULTY_MAP.get(target_label, 0.5)

        return abs(estimated - target_score) <= tolerance

    def choose(self, item: Dict[str, Any]) -> str:
        """
        Not used for difficulty agent - use estimate() instead.

        Included for base Agent interface compatibility.
        """
        # Difficulty agent doesn't make choices, it estimates
        return item.get("solution_choice_id", "A")
