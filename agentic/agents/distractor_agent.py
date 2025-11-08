"""
Distractor Agent: Evaluates quality of wrong answer choices.

Checks if wrong answers represent plausible common misconceptions
rather than obviously incorrect or random values.
"""

import re
from typing import Dict, Any, List, NamedTuple
from .base import Agent


class DistractorQuality(NamedTuple):
    """Result of distractor evaluation."""
    plausible_count: int
    total_distractors: int
    issues: List[str]
    quality_score: float
    improvement_suggestions: List[str]


class DistractorAgent(Agent):
    """Evaluates quality of wrong answer choices."""

    name = "distractor_validator"

    def evaluate(self, question: Dict[str, Any]) -> DistractorQuality:
        """
        Checks if wrong answers represent common misconceptions.

        Args:
            question: Full question item with choices

        Returns:
            DistractorQuality with plausibility assessment
        """
        choices = question.get("choices", [])
        solution_id = question.get("solution_choice_id", "A")

        # Get correct answer for comparison
        correct_answer = None
        for choice in choices:
            if choice.get("id") == solution_id:
                correct_answer = choice.get("text", "")
                break

        plausible_count = 0
        issues = []
        suggestions = []

        distractors = [c for c in choices if c.get("id") != solution_id]

        for choice in distractors:
            choice_id = choice.get("id", "")
            choice_text = choice.get("text", "")

            # Check 1: Must look like a valid math answer
            if not self._looks_like_math_answer(choice_text):
                issues.append(f"Choice {choice_id}: '{choice_text}' doesn't look like valid math")
                suggestions.append(f"Replace {choice_id} with plausible mathematical value")
                continue

            # Check 2: Should not be identical to correct answer
            if correct_answer and choice_text == correct_answer:
                issues.append(f"Choice {choice_id}: Identical to correct answer")
                suggestions.append(f"Make {choice_id} distinct from correct answer")
                continue

            # Check 3: Should be in same format as correct answer
            if correct_answer and not self._matches_format(choice_text, correct_answer):
                issues.append(f"Choice {choice_id}: Format mismatch with correct answer")
                suggestions.append(f"Format {choice_id} consistently with correct answer")

            # Check 4: Could be a realistic mistake
            if self._could_be_common_error(choice_text, correct_answer, question):
                plausible_count += 1
            else:
                # Not obviously a common error, but might still be valid
                # Don't penalize too harshly
                plausible_count += 0.5

        # Calculate quality score
        if len(distractors) == 0:
            quality_score = 0.0
        else:
            quality_score = plausible_count / len(distractors)

        return DistractorQuality(
            plausible_count=int(plausible_count),
            total_distractors=len(distractors),
            issues=issues,
            quality_score=quality_score,
            improvement_suggestions=suggestions if suggestions else ["Distractors appear reasonable"]
        )

    def _looks_like_math_answer(self, text: str) -> bool:
        """Check if text looks like a valid mathematical answer."""
        if not text or not text.strip():
            return False

        # Should contain numbers, variables, or mathematical symbols
        has_numbers = bool(re.search(r'\d', text))
        has_variables = bool(re.search(r'[xy]', text))
        has_math_symbols = bool(re.search(r'[+\-=\(\),/]', text))

        return has_numbers or has_variables or has_math_symbols

    def _matches_format(self, distractor: str, correct: str) -> bool:
        """Check if distractor matches format of correct answer."""
        # Both should be similar types

        # Check for coordinate pairs: (x, y)
        distractor_has_coords = bool(re.search(r'\([^)]+,\s*[^)]+\)', distractor))
        correct_has_coords = bool(re.search(r'\([^)]+,\s*[^)]+\)', correct))

        if distractor_has_coords != correct_has_coords:
            return False

        # Check for equation format: x = ... or y = ...
        distractor_has_eq = bool(re.search(r'[xy]\s*=', distractor))
        correct_has_eq = bool(re.search(r'[xy]\s*=', correct))

        if distractor_has_eq != correct_has_eq:
            return False

        # Otherwise consider format compatible
        return True

    def _could_be_common_error(
        self,
        distractor: str,
        correct: str,
        question: Dict[str, Any]
    ) -> bool:
        """
        Check if distractor represents a plausible common misconception.

        Args:
            distractor: Wrong answer text
            correct: Correct answer text
            question: Full question for context

        Returns:
            True if represents a realistic mistake
        """
        if not correct or not distractor:
            return False

        skill_id = question.get("skill_id", "")

        # Extract numbers from both answers
        distractor_nums = re.findall(r'-?\d+\.?\d*', distractor)
        correct_nums = re.findall(r'-?\d+\.?\d*', correct)

        if not distractor_nums or not correct_nums:
            return True  # Can't analyze, assume it's reasonable

        try:
            # Common error 1: Sign errors (forgot negative, or added negative)
            if len(distractor_nums) >= len(correct_nums):
                for i in range(len(correct_nums)):
                    dist_val = float(distractor_nums[i])
                    corr_val = float(correct_nums[i])

                    # Sign flip
                    if abs(dist_val + corr_val) < 0.01:
                        return True  # Sign error is common

            # Common error 2: Off-by-factor errors (forgot to divide/multiply by 2)
            if len(correct_nums) > 0 and len(distractor_nums) > 0:
                dist_val = float(distractor_nums[0])
                corr_val = float(correct_nums[0])

                # Check for 2x, 0.5x errors
                if abs(dist_val - 2 * corr_val) < 0.01 or abs(dist_val - 0.5 * corr_val) < 0.01:
                    return True

            # Common error 3: For vertex problems, swapped h and k
            if "vertex" in skill_id and len(correct_nums) >= 2 and len(distractor_nums) >= 2:
                if (abs(float(distractor_nums[0]) - float(correct_nums[1])) < 0.01 and
                    abs(float(distractor_nums[1]) - float(correct_nums[0])) < 0.01):
                    return True  # Swapped coordinates

            # Common error 4: Reasonably close to correct answer
            if len(correct_nums) > 0 and len(distractor_nums) > 0:
                dist_val = abs(float(distractor_nums[0]))
                corr_val = abs(float(correct_nums[0]))

                # Within 50% of correct value is plausible
                if corr_val > 0:
                    ratio = dist_val / corr_val
                    if 0.5 <= ratio <= 2.0:
                        return True

        except (ValueError, ZeroDivisionError):
            # If we can't parse numbers, assume it's reasonable
            return True

        # If distractor and correct are very similar in structure, likely plausible
        if len(distractor) > 0 and len(correct) > 0:
            similarity = len(set(distractor) & set(correct)) / len(set(distractor) | set(correct))
            if similarity > 0.5:
                return True

        return False

    def choose(self, item: Dict[str, Any]) -> str:
        """
        Not used for distractor agent - use evaluate() instead.

        Included for base Agent interface compatibility.
        """
        # Distractor agent doesn't make choices, it evaluates
        return item.get("solution_choice_id", "A")
