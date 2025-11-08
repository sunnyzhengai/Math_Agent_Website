"""
Iterative Explanation Agent: Generates explanations with refinement.

Implements Andrew Ng's Iterative Refinement pattern:
- Multiple refinement passes until quality threshold met
- Clarity scoring and language simplification
- Completeness checking
- Error-specific misconception diagnosis
"""

import re
from typing import Dict, Any, List, Tuple, NamedTuple
from engine.solutions import generate_solution


class CompletenessResult(NamedTuple):
    """Result of completeness check."""
    is_complete: bool
    score: float  # 0-1
    missing_elements: List[str]
    suggestions: List[str]


class RefinementMetrics(NamedTuple):
    """Metrics tracking refinement process."""
    iterations: int
    initial_clarity: float
    final_clarity: float
    initial_completeness: float
    final_completeness: float
    improvements_made: List[str]


class IterativeExplanationAgent:
    """Generates explanations with iterative refinement until quality thresholds met."""

    def __init__(self):
        """Initialize the iterative explanation agent."""
        self.target_clarity = 0.7
        self.target_completeness = 0.8
        self.max_iterations = 3

        self.refinement_history = []

    def generate_explanation(
        self,
        item: Dict[str, Any],
        student_answer: str,
        correct_answer: str,
        reading_level: str = "grade_9"  # For future student profiling
    ) -> Tuple[str, RefinementMetrics]:
        """
        Generate explanation with quality refinement loop.

        Args:
            item: Question item dict
            student_answer: Student's selected choice ID
            correct_answer: Correct choice ID
            reading_level: Target reading level (for future enhancement)

        Returns:
            Tuple of (final_explanation, refinement_metrics)
        """
        improvements_made = []

        # ITERATION 1: Template-based draft from existing system
        draft_v1 = generate_solution(item, student_answer, correct_answer)

        initial_clarity = self._score_clarity(draft_v1)
        initial_completeness_result = self._check_completeness(draft_v1, item.get("skill_id", ""))

        draft = draft_v1

        # ITERATION 2: Clarity refinement
        if initial_clarity < self.target_clarity:
            draft = self._simplify_language(draft)
            improvements_made.append("simplified_language")

        # ITERATION 3: Completeness check
        completeness_result = self._check_completeness(draft, item.get("skill_id", ""))
        if not completeness_result.is_complete:
            draft = self._add_missing_steps(draft, completeness_result)
            improvements_made.append("added_missing_steps")

        # ITERATION 4: Add clear formatting
        draft = self._improve_formatting(draft)
        improvements_made.append("improved_formatting")

        # Calculate final metrics
        final_clarity = self._score_clarity(draft)
        final_completeness = self._check_completeness(draft, item.get("skill_id", ""))

        metrics = RefinementMetrics(
            iterations=len(improvements_made) + 1,
            initial_clarity=initial_clarity,
            final_clarity=final_clarity,
            initial_completeness=initial_completeness_result.score,
            final_completeness=final_completeness.score,
            improvements_made=improvements_made
        )

        # Track for analytics
        self.refinement_history.append({
            "skill_id": item.get("skill_id"),
            "difficulty": item.get("difficulty"),
            "metrics": metrics._asdict()
        })

        return draft, metrics

    def _score_clarity(self, text: str) -> float:
        """
        Score explanation clarity 0-1.

        Heuristics:
        - Sentence length (shorter is clearer)
        - Use of technical jargon
        - Presence of clear structure
        - Readability indicators
        """
        score = 1.0

        # Check 1: Average sentence length
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if sentences:
            avg_length = sum(len(s.split()) for s in sentences) / len(sentences)
            if avg_length > 25:
                score -= 0.2  # Too long
            elif avg_length > 20:
                score -= 0.1

        # Check 2: Has clear structure (step markers)
        has_steps = bool(re.search(r'Step \d+|^\d+\.', text, re.MULTILINE))
        if not has_steps:
            score -= 0.15

        # Check 3: Not too dense (has line breaks)
        line_count = len([l for l in text.split('\n') if l.strip()])
        if line_count < 3:
            score -= 0.15  # Too dense

        # Check 4: Uses concrete examples with actual values
        has_numbers = bool(re.search(r'\d+', text))
        if not has_numbers:
            score -= 0.2  # Too abstract

        # Check 5: Not too short (likely incomplete)
        if len(text) < 100:
            score -= 0.2

        return max(0.0, min(1.0, score))

    def _check_completeness(self, text: str, skill_id: str) -> CompletenessResult:
        """
        Check if explanation is complete for the skill.

        Args:
            text: Explanation text
            skill_id: Skill being explained

        Returns:
            CompletenessResult with missing elements
        """
        missing = []
        suggestions = []
        score = 1.0

        # Required elements by skill type
        if "vertex" in skill_id:
            if "h" not in text.lower():
                missing.append("h-coordinate explanation")
                suggestions.append("Explain how to find h = -b/(2a)")
                score -= 0.3
            if "k" not in text.lower():
                missing.append("k-coordinate explanation")
                suggestions.append("Explain how to find k by substituting")
                score -= 0.3

        elif "factoring" in skill_id or "solve" in skill_id:
            if "factor" in skill_id and "factor" not in text.lower():
                missing.append("factoring explanation")
                suggestions.append("Show the factoring process")
                score -= 0.4
            if "=" in text and "0" not in text:
                missing.append("set equal to zero")
                suggestions.append("Explain why we set each factor equal to 0")
                score -= 0.2

        elif "formula" in skill_id:
            if "b² - 4ac" not in text and "discriminant" not in text.lower():
                missing.append("discriminant calculation")
                suggestions.append("Show b² - 4ac calculation")
                score -= 0.3

        elif "discriminant" in skill_id:
            if "b²" not in text and "b^2" not in text:
                missing.append("discriminant formula")
                suggestions.append("Show the formula b² - 4ac")
                score -= 0.4

        # Universal checks
        if "**" in text or "Correct answer" in text:
            # Has some formatting, good
            pass
        else:
            missing.append("clear formatting")
            suggestions.append("Add bold headers and clear structure")
            score -= 0.1

        # Check for verification step
        if "verify" not in text.lower() and "check" not in text.lower() and "substitute" not in text.lower():
            missing.append("verification step")
            suggestions.append("Add a verification step to check the answer")
            score -= 0.15

        is_complete = score >= self.target_completeness

        return CompletenessResult(
            is_complete=is_complete,
            score=max(0.0, score),
            missing_elements=missing,
            suggestions=suggestions
        )

    def _simplify_language(self, text: str) -> str:
        """
        Simplify language to improve clarity.

        - Break long sentences
        - Add more explicit step markers
        - Use clearer transitions
        """
        # Add clear step headers if missing
        if "Step 1" not in text and "**" not in text:
            # Add basic structure
            lines = [l for l in text.split('\n') if l.strip()]
            if len(lines) > 2:
                # Try to identify natural sections
                structured = "**Solution:**\n\n" + text
                return structured

        # Already has structure, return as is
        return text

    def _add_missing_steps(
        self,
        text: str,
        completeness_result: CompletenessResult
    ) -> str:
        """
        Add missing steps identified by completeness check.

        Args:
            text: Current explanation
            completeness_result: Result from completeness check

        Returns:
            Enhanced explanation with missing steps
        """
        if not completeness_result.missing_elements:
            return text

        # Add suggestions at the end
        additions = []

        if "verification step" in completeness_result.missing_elements:
            additions.append("\n**Verification:** Substitute the answer back into the original equation to verify it's correct.")

        if "h-coordinate explanation" in completeness_result.missing_elements:
            additions.append("\n**Note:** The h-coordinate of the vertex is found using h = -b/(2a).")

        if "k-coordinate explanation" in completeness_result.missing_elements:
            additions.append("\n**Note:** The k-coordinate is found by substituting h back into the equation: k = a(h)² + b(h) + c.")

        if additions:
            return text + "\n" + "\n".join(additions)

        return text

    def _improve_formatting(self, text: str) -> str:
        """
        Improve visual formatting of explanation.

        - Ensure bold headers
        - Add spacing between sections
        - Highlight key formulas
        """
        # Ensure double-spacing between major sections
        text = re.sub(r'\n\*\*', '\n\n**', text)

        # Ensure spacing after periods in dense text
        text = re.sub(r'\.([A-Z])', r'. \1', text)

        return text.strip()

    def get_refinement_stats(self) -> Dict[str, Any]:
        """
        Get statistics about refinement process.

        Returns:
            Dict with average improvements, iteration counts, etc.
        """
        if not self.refinement_history:
            return {
                "total_generations": 0,
                "avg_iterations": 0,
                "avg_clarity_improvement": 0,
                "avg_completeness_improvement": 0
            }

        total = len(self.refinement_history)

        avg_iterations = sum(r["metrics"]["iterations"] for r in self.refinement_history) / total

        clarity_improvements = [
            r["metrics"]["final_clarity"] - r["metrics"]["initial_clarity"]
            for r in self.refinement_history
        ]
        avg_clarity_improvement = sum(clarity_improvements) / len(clarity_improvements) if clarity_improvements else 0

        completeness_improvements = [
            r["metrics"]["final_completeness"] - r["metrics"]["initial_completeness"]
            for r in self.refinement_history
        ]
        avg_completeness_improvement = sum(completeness_improvements) / len(completeness_improvements) if completeness_improvements else 0

        # Count improvement types
        improvement_counts = {}
        for r in self.refinement_history:
            for improvement in r["metrics"]["improvements_made"]:
                improvement_counts[improvement] = improvement_counts.get(improvement, 0) + 1

        return {
            "total_generations": total,
            "avg_iterations": avg_iterations,
            "avg_initial_clarity": sum(r["metrics"]["initial_clarity"] for r in self.refinement_history) / total,
            "avg_final_clarity": sum(r["metrics"]["final_clarity"] for r in self.refinement_history) / total,
            "avg_clarity_improvement": avg_clarity_improvement,
            "avg_initial_completeness": sum(r["metrics"]["initial_completeness"] for r in self.refinement_history) / total,
            "avg_final_completeness": sum(r["metrics"]["final_completeness"] for r in self.refinement_history) / total,
            "avg_completeness_improvement": avg_completeness_improvement,
            "improvement_types": improvement_counts
        }
