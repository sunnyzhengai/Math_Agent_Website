"""
ReAct Explanation Generator: Transparent reasoning through Thought-Action-Observation.

Implements Shunyu Yao's ReAct pattern:
- Thought: Internal reasoning about the problem/error
- Action: Concrete action to take (analyze, check, diagnose)
- Observation: Result of the action
- Repeat until solution/explanation is complete

This makes AI reasoning transparent and educational:
- Students see HOW the system thinks
- Builds trust through observable reasoning
- Teaches diagnostic thinking
- More engaging than direct answers
"""

from typing import Dict, List, Any, NamedTuple, Optional
import re


class ReActStep(NamedTuple):
    """A single step in the ReAct reasoning cycle."""
    thought: str  # Internal reasoning
    action: str  # Action to take
    observation: str  # Result of action


class ReActExplanation(NamedTuple):
    """Complete explanation with reasoning trace."""
    explanation_text: str  # Final formatted explanation
    reasoning_steps: List[ReActStep]  # Transparent reasoning process
    key_insight: str  # Main teaching point
    error_type: str  # Classification of student's error
    correction_strategy: str  # How to fix it


class ReActExplanationGenerator:
    """
    Generates explanations using ReAct pattern for transparent reasoning.

    Instead of directly providing answers, shows the thinking process:
    "Let me think about this... [Thought]"
    "I'll check... [Action]"
    "I observe that... [Observation]"

    This teaches students HOW to reason about math problems.
    """

    # Common error types we can diagnose
    ERROR_PATTERNS = {
        "sign_error": {
            "indicators": ["negative", "positive", "minus", "plus"],
            "typical_cause": "Confusion with negative signs in vertex form"
        },
        "coordinate_swap": {
            "indicators": ["swap", "reversed", "backwards"],
            "typical_cause": "Mixing up x and y coordinates"
        },
        "formula_misapplication": {
            "indicators": ["formula", "equation", "substitution"],
            "typical_cause": "Incorrect formula application"
        },
        "conceptual_confusion": {
            "indicators": ["concept", "meaning", "why"],
            "typical_cause": "Fundamental misunderstanding of concept"
        }
    }

    def __init__(self):
        """Initialize ReAct explanation generator."""
        self.explanation_count = 0
        self.reasoning_trace_history = []

    def generate_explanation_with_react(
        self,
        question: Dict[str, Any],
        student_answer: str,
        correct_answer: str,
        context: Optional[Dict[str, Any]] = None
    ) -> ReActExplanation:
        """
        Generate explanation using ReAct reasoning pattern.

        Args:
            question: Question dict with stem, choices, etc.
            student_answer: Student's chosen answer (choice ID)
            correct_answer: Correct answer (choice ID)
            context: Optional context (past errors, memory, etc.)

        Returns:
            ReActExplanation with transparent reasoning
        """
        skill_id = question.get("skill_id", "")
        stem = question.get("stem", "")
        choices = question.get("choices", [])

        # Convert choices to dict for easy lookup
        if isinstance(choices, list):
            choices_dict = {c["id"]: c["text"] for c in choices}
        else:
            choices_dict = choices

        student_choice_text = choices_dict.get(student_answer, "")
        correct_choice_text = choices_dict.get(correct_answer, "")

        # Run ReAct reasoning cycles
        reasoning_steps = []

        # CYCLE 1: Understand the situation
        reasoning_steps.append(self._cycle_1_understand(
            stem, student_answer, correct_answer,
            student_choice_text, correct_choice_text
        ))

        # CYCLE 2: Diagnose the error
        reasoning_steps.append(self._cycle_2_diagnose(
            skill_id, student_choice_text, correct_choice_text, context
        ))

        # CYCLE 3: Explain the correct approach
        reasoning_steps.append(self._cycle_3_explain_correct(
            skill_id, stem, correct_choice_text
        ))

        # CYCLE 4: Provide correction strategy
        reasoning_steps.append(self._cycle_4_correction_strategy(
            skill_id, reasoning_steps[1].observation
        ))

        # Determine error type from diagnosis
        error_type = self._extract_error_type(reasoning_steps[1].observation)

        # Extract key insight from correct approach
        key_insight = self._extract_key_insight(skill_id, reasoning_steps[2].observation)

        # Extract correction strategy
        correction_strategy = reasoning_steps[3].observation

        # Format final explanation
        explanation_text = self._format_explanation(
            reasoning_steps,
            key_insight,
            error_type
        )

        # Track in history
        self.reasoning_trace_history.append({
            "question": stem,
            "steps": [s._asdict() for s in reasoning_steps],
            "error_type": error_type
        })
        self.explanation_count += 1

        return ReActExplanation(
            explanation_text=explanation_text,
            reasoning_steps=reasoning_steps,
            key_insight=key_insight,
            error_type=error_type,
            correction_strategy=correction_strategy
        )

    def _cycle_1_understand(
        self,
        stem: str,
        student_answer: str,
        correct_answer: str,
        student_text: str,
        correct_text: str
    ) -> ReActStep:
        """Cycle 1: Understand what happened."""
        thought = (
            f"The student chose answer {student_answer}, but the correct answer is {correct_answer}. "
            f"Let me understand what went wrong."
        )

        action = f"Compare student's answer '{student_text}' with correct answer '{correct_text}'"

        observation = (
            f"The student selected '{student_text}' instead of '{correct_text}'. "
            f"I need to figure out why they made this choice."
        )

        return ReActStep(thought=thought, action=action, observation=observation)

    def _cycle_2_diagnose(
        self,
        skill_id: str,
        student_text: str,
        correct_text: str,
        context: Optional[Dict[str, Any]]
    ) -> ReActStep:
        """Cycle 2: Diagnose the specific error."""
        thought = "Let me analyze the student's answer to identify the specific error pattern."

        action = f"Examine the difference between '{student_text}' and '{correct_text}' in context of {skill_id}"

        # Analyze the error
        error_diagnosis = self._diagnose_error(skill_id, student_text, correct_text, context)

        observation = error_diagnosis

        return ReActStep(thought=thought, action=action, observation=observation)

    def _cycle_3_explain_correct(
        self,
        skill_id: str,
        stem: str,
        correct_text: str
    ) -> ReActStep:
        """Cycle 3: Explain the correct approach."""
        thought = "Now I need to explain the correct way to solve this problem."

        action = f"Walk through the correct solution process for {skill_id}"

        # Generate correct approach explanation
        correct_explanation = self._explain_correct_approach(skill_id, stem, correct_text)

        observation = correct_explanation

        return ReActStep(thought=thought, action=action, observation=observation)

    def _cycle_4_correction_strategy(
        self,
        skill_id: str,
        error_diagnosis: str
    ) -> ReActStep:
        """Cycle 4: Provide strategy to avoid future errors."""
        thought = "Finally, I should give the student a strategy to avoid this error in the future."

        action = "Provide specific tips based on the error pattern"

        strategy = self._generate_correction_strategy(skill_id, error_diagnosis)

        observation = strategy

        return ReActStep(thought=thought, action=action, observation=observation)

    def _diagnose_error(
        self,
        skill_id: str,
        student_text: str,
        correct_text: str,
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Diagnose specific error pattern."""
        # Extract numbers from both answers
        student_nums = re.findall(r'-?\d+\.?\d*', student_text)
        correct_nums = re.findall(r'-?\d+\.?\d*', correct_text)

        # Vertex form skills
        if "vertex" in skill_id:
            if len(student_nums) >= 2 and len(correct_nums) >= 2:
                # Check for sign error
                if (abs(float(student_nums[0])) == abs(float(correct_nums[0])) and
                    float(student_nums[0]) == -float(correct_nums[0])):
                    return (
                        "This appears to be a SIGN ERROR. The student got the magnitude correct "
                        "but used the wrong sign. In vertex form y = (x - h)² + k, the h value "
                        "has the OPPOSITE sign from what appears in the equation. If you see (x - 3), "
                        "then h = +3, not -3."
                    )

                # Check for coordinate swap
                if (abs(float(student_nums[0])) == abs(float(correct_nums[1])) and
                    abs(float(student_nums[1])) == abs(float(correct_nums[0]))):
                    return (
                        "This appears to be a COORDINATE SWAP. The student switched the x and y "
                        "coordinates of the vertex. Remember: vertex is (h, k) where h is the "
                        "x-coordinate and k is the y-coordinate."
                    )

        # Factoring skills
        if "factor" in skill_id:
            return (
                "The student appears to have made an error in factoring. "
                "Let me help identify where the factorization went wrong."
            )

        # Generic diagnosis
        return (
            "The student made a calculation or conceptual error. "
            "Let me explain the correct approach."
        )

    def _explain_correct_approach(
        self,
        skill_id: str,
        stem: str,
        correct_text: str
    ) -> str:
        """Explain the correct solution approach."""
        if "vertex" in skill_id and "graph" in skill_id:
            # Extract equation from stem
            equation_match = re.search(r'y = .*?\^2[^\?]*', stem)
            equation = equation_match.group(0) if equation_match else "the equation"

            return (
                f"To find the vertex from {equation}, I need to identify the vertex form "
                f"y = a(x - h)² + k. The vertex is at point (h, k). "
                f"Looking at the equation, I can read off h and k directly, "
                f"remembering that the sign of h is OPPOSITE to what appears with x. "
                f"This gives us the vertex: {correct_text}."
            )

        if "standard" in skill_id and "vertex" in skill_id:
            return (
                f"To convert from standard form to vertex form, I need to complete the square. "
                f"This involves grouping x terms, factoring, and rewriting in vertex form. "
                f"The correct vertex is: {correct_text}."
            )

        # Generic explanation
        return (
            f"Following the standard approach for {skill_id}, "
            f"the correct answer is: {correct_text}."
        )

    def _generate_correction_strategy(
        self,
        skill_id: str,
        error_diagnosis: str
    ) -> str:
        """Generate specific strategy to avoid this error."""
        if "SIGN ERROR" in error_diagnosis:
            return (
                "To avoid sign errors in the future:\n"
                "1. When you see (x - h), remember h is POSITIVE\n"
                "2. When you see (x + h), remember h is NEGATIVE\n"
                "3. The sign is always OPPOSITE to what you see\n"
                "4. Double-check: plug the vertex back into the equation to verify"
            )

        if "COORDINATE SWAP" in error_diagnosis:
            return (
                "To avoid coordinate confusion:\n"
                "1. Always write vertex as (x-coordinate, y-coordinate)\n"
                "2. In vertex form (x - h)² + k, remember: h is x, k is y\n"
                "3. Label your answer: (h=x, k=y) = (?, ?)\n"
                "4. Check: does the first number make sense for horizontal position?"
            )

        # Generic strategy
        return (
            "General tips:\n"
            "1. Read the question carefully\n"
            "2. Write out each step\n"
            "3. Check your answer by substituting back\n"
            "4. Look for common error patterns you make"
        )

    def _extract_error_type(self, diagnosis: str) -> str:
        """Extract error type from diagnosis."""
        if "SIGN ERROR" in diagnosis:
            return "sign_error"
        if "COORDINATE SWAP" in diagnosis:
            return "coordinate_swap"
        if "factoring" in diagnosis.lower():
            return "factoring_error"
        return "conceptual_error"

    def _extract_key_insight(self, skill_id: str, explanation: str) -> str:
        """Extract the key teaching point."""
        if "vertex" in skill_id:
            return "In vertex form y = (x - h)² + k, the vertex is (h, k), but watch the signs!"

        if "factor" in skill_id:
            return "Factoring requires finding numbers that multiply to give ac and add to give b"

        return "Understanding the core concept is key to solving these problems"

    def _format_explanation(
        self,
        steps: List[ReActStep],
        key_insight: str,
        error_type: str
    ) -> str:
        """Format the complete explanation with reasoning trace."""
        parts = []

        parts.append("🤔 Let me think through this with you step by step:\n")

        # Show reasoning cycles
        for i, step in enumerate(steps, 1):
            parts.append(f"\n**Step {i}: {['Understanding', 'Diagnosing', 'Explaining', 'Strategy'][i-1]}**")
            parts.append(f"💭 *Thought:* {step.thought}")
            parts.append(f"🎯 *Action:* {step.action}")
            parts.append(f"👁️ *Observation:* {step.observation}\n")

        # Add key insight
        parts.append(f"\n✨ **Key Insight:** {key_insight}\n")

        # Add summary
        parts.append("\n📝 **Summary:**")
        parts.append(f"You made a {error_type.replace('_', ' ')}. {steps[1].observation.split('.')[0]}.")
        parts.append(f"The correct approach is: {steps[2].observation.split('.')[0]}.")

        return "\n".join(parts)

    def get_reasoning_stats(self) -> Dict[str, Any]:
        """Get statistics about reasoning traces generated."""
        if not self.reasoning_trace_history:
            return {
                "total_explanations": 0,
                "avg_steps_per_explanation": 0
            }

        error_types = {}
        for trace in self.reasoning_trace_history:
            error_type = trace["error_type"]
            error_types[error_type] = error_types.get(error_type, 0) + 1

        avg_steps = sum(len(t["steps"]) for t in self.reasoning_trace_history) / len(self.reasoning_trace_history)

        return {
            "total_explanations": len(self.reasoning_trace_history),
            "avg_steps_per_explanation": avg_steps,
            "error_types_diagnosed": error_types,
            "most_common_error": max(error_types.items(), key=lambda x: x[1])[0] if error_types else None
        }
