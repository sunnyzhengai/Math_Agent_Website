"""
Clarity Agent: Evaluates question clarity and readability.

Uses heuristics to assess whether a question is clearly worded
and easy for students to understand.
"""

import re
from typing import Dict, Any, List
from .base import Agent


class ClarityAgent(Agent):
    """Evaluates question clarity and readability."""

    name = "clarity"

    def evaluate(self, question_stem: str) -> float:
        """
        Returns clarity score 0-1 where 1.0 is perfectly clear.

        Args:
            question_stem: The question text to evaluate

        Returns:
            Float score between 0.0 (unclear) and 1.0 (clear)
        """
        score = 1.0

        # Check 1: Reasonable length (not too short/long)
        if len(question_stem) < 10:
            score -= 0.3  # Too short, likely missing context
        if len(question_stem) > 300:
            score -= 0.2  # Too verbose

        # Check 2: Has clear question structure
        has_question_marker = (
            "?" in question_stem or
            "Find" in question_stem or
            "What" in question_stem or
            "Which" in question_stem or
            "Solve" in question_stem or
            "Determine" in question_stem
        )
        if not has_question_marker:
            score -= 0.3  # Unclear what's being asked

        # Check 3: No ambiguous language
        ambiguous_words = [
            "thing", "stuff", "maybe", "sort of",
            "kind of", "approximately", "around"
        ]
        for word in ambiguous_words:
            if word.lower() in question_stem.lower():
                score -= 0.3
                break  # Only penalize once

        # Check 4: No garbled text or nonsense
        # Check for consecutive non-word characters
        if re.search(r'[^a-zA-Z0-9\s\+\-\=\(\)\.\,\?\!]{3,}', question_stem):
            score -= 0.4  # Likely garbled

        # Check 5: Has proper sentence structure
        # Should start with capital letter and end with punctuation
        if question_stem and not question_stem[0].isupper():
            score -= 0.1
        if question_stem and question_stem[-1] not in '.?!':
            score -= 0.1

        # Check 6: Not empty or whitespace only
        if not question_stem or question_stem.strip() == "":
            return 0.0

        return max(0.0, min(1.0, score))

    def suggest_improvements(self, question: Dict[str, Any]) -> List[str]:
        """
        Provide specific suggestions for improving clarity.

        Args:
            question: Full question item dict

        Returns:
            List of improvement suggestions
        """
        suggestions = []
        stem = question.get("stem", "")

        # Analyze specific issues
        if len(stem) < 10:
            suggestions.append("Add more context to the question")

        if len(stem) > 300:
            suggestions.append("Simplify wording to make question more concise")

        if "?" not in stem and "Find" not in stem and "Solve" not in stem:
            suggestions.append("Make it clearer what the student should find or solve")

        # Check for ambiguous words
        ambiguous_words = ["thing", "stuff", "maybe", "sort of", "kind of"]
        found_ambiguous = [w for w in ambiguous_words if w.lower() in stem.lower()]
        if found_ambiguous:
            suggestions.append(f"Remove ambiguous words: {', '.join(found_ambiguous)}")

        if not stem or not stem[0].isupper():
            suggestions.append("Start question with capital letter")

        if stem and stem[-1] not in '.?!':
            suggestions.append("End question with proper punctuation")

        if not suggestions:
            suggestions.append("Question appears clear")

        return suggestions

    def choose(self, item: Dict[str, Any]) -> str:
        """
        Not used for clarity agent - use evaluate() instead.

        Included for base Agent interface compatibility.
        """
        # Clarity agent doesn't make choices, it evaluates
        return item.get("solution_choice_id", "A")
