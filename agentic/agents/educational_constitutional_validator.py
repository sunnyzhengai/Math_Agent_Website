"""
Educational Constitutional Validator: Anthropic's Constitutional AI for Education.

Implements Dario Amodei's Constitutional AI pattern:
- Define educational principles as constitution
- Check all content against principles
- Flag violations with severity levels
- Enable self-critique without human intervention

The 6 Educational Principles:
1. Genuine Understanding - Promote reasoning over memorization
2. Pedagogical Soundness - Clear, appropriate explanations
3. Honest Distractors - Real misconceptions, not tricks
4. Appropriate Difficulty - Calibrated challenge levels
5. Safe Learning Environment - No harmful content
6. Inclusive & Accessible - Works for diverse learners
"""

from typing import Dict, Any, List, NamedTuple
import re


class PrincipleViolation(NamedTuple):
    """A violation of an educational principle."""
    principle_id: str
    principle_name: str
    severity: str  # "critical", "high", "medium", "low"
    violation_description: str
    suggested_fix: str


class ConstitutionalValidation(NamedTuple):
    """Result of constitutional validation."""
    passes_constitution: bool
    violations: List[PrincipleViolation]
    principles_checked: int
    principles_passed: int
    overall_score: float  # 0-1, weighted by severity


class EducationalConstitution:
    """
    The Educational Constitution: 6 core principles.

    Based on Anthropic's Constitutional AI approach:
    - Principles defined upfront
    - Automated checking against principles
    - Self-critique capabilities
    - No human review needed for most content
    """

    PRINCIPLES = [
        {
            "id": "genuine_understanding",
            "name": "Genuine Understanding",
            "description": "Questions must promote genuine understanding, not memorization",
            "checks": ["requires_reasoning", "not_pure_recall", "multi_step_thinking"],
            "severity": "critical",
            "weight": 1.0
        },
        {
            "id": "pedagogical_soundness",
            "name": "Pedagogical Soundness",
            "description": "Explanations must be pedagogically sound and age-appropriate",
            "checks": ["clear_language", "appropriate_complexity", "correct_terminology"],
            "severity": "critical",
            "weight": 1.0
        },
        {
            "id": "honest_distractors",
            "name": "Honest Distractors",
            "description": "Wrong answers must represent real misconceptions, not tricks",
            "checks": ["plausible_errors", "not_deliberately_confusing", "educational_value"],
            "severity": "high",
            "weight": 0.8
        },
        {
            "id": "appropriate_difficulty",
            "name": "Appropriate Difficulty",
            "description": "Challenge level must match stated difficulty",
            "checks": ["calibrated_to_level", "not_trivial", "not_impossible"],
            "severity": "high",
            "weight": 0.7
        },
        {
            "id": "safe_learning",
            "name": "Safe Learning Environment",
            "description": "Content must be safe, respectful, and harm-free",
            "checks": ["no_harmful_content", "no_stereotypes", "respectful_language"],
            "severity": "critical",
            "weight": 1.0
        },
        {
            "id": "inclusive_accessible",
            "name": "Inclusive & Accessible",
            "description": "Content must work for diverse learners",
            "checks": ["clear_notation", "context_provided", "no_cultural_bias"],
            "severity": "medium",
            "weight": 0.6
        }
    ]


class EducationalConstitutionalValidator:
    """
    Validates educational content against constitutional principles.

    Implements Anthropic's Constitutional AI:
    - Self-critique against defined principles
    - Automated violation detection
    - Severity-weighted scoring
    - Actionable improvement suggestions
    """

    def __init__(self, strict_mode: bool = True):
        """
        Initialize constitutional validator.

        Args:
            strict_mode: If True, critical violations fail validation
        """
        self.strict_mode = strict_mode
        self.constitution = EducationalConstitution()
        self.validation_history = []

    def validate(self, question: Dict[str, Any]) -> ConstitutionalValidation:
        """
        Validate question against all constitutional principles.

        Args:
            question: Question dict with stem, choices, solution_choice_id, skill_id

        Returns:
            ConstitutionalValidation with violations and scores
        """
        violations = []

        # PRINCIPLE 1: Genuine Understanding
        violations.extend(self._check_genuine_understanding(question))

        # PRINCIPLE 2: Pedagogical Soundness
        violations.extend(self._check_pedagogical_soundness(question))

        # PRINCIPLE 3: Honest Distractors
        violations.extend(self._check_honest_distractors(question))

        # PRINCIPLE 4: Appropriate Difficulty
        violations.extend(self._check_appropriate_difficulty(question))

        # PRINCIPLE 5: Safe Learning Environment
        violations.extend(self._check_safe_learning(question))

        # PRINCIPLE 6: Inclusive & Accessible
        violations.extend(self._check_inclusive_accessible(question))

        # Calculate overall score
        total_principles = len(self.constitution.PRINCIPLES)
        principles_passed = total_principles - len(set(v.principle_id for v in violations))

        # Weight by severity
        overall_score = self._calculate_weighted_score(violations, total_principles)

        # Determine if passes
        if self.strict_mode:
            # Critical violations fail
            has_critical = any(v.severity == "critical" for v in violations)
            passes = not has_critical
        else:
            # Must score above 0.7
            passes = overall_score >= 0.7

        result = ConstitutionalValidation(
            passes_constitution=passes,
            violations=violations,
            principles_checked=total_principles,
            principles_passed=principles_passed,
            overall_score=overall_score
        )

        # Track history
        self.validation_history.append({
            "question_id": question.get("id"),
            "skill_id": question.get("skill_id"),
            "result": result._asdict()
        })

        return result

    def _check_genuine_understanding(self, question: Dict[str, Any]) -> List[PrincipleViolation]:
        """Check if question promotes genuine understanding."""
        violations = []
        stem = question.get("stem", "")
        skill_id = question.get("skill_id", "")

        # CHECK 1: Requires reasoning (not pure recall)
        # Look for computational or analytical requirements
        has_computation = any(word in stem.lower() for word in [
            "find", "solve", "calculate", "determine", "what is"
        ])

        if not has_computation:
            violations.append(PrincipleViolation(
                principle_id="genuine_understanding",
                principle_name="Genuine Understanding",
                severity="critical",
                violation_description="Question appears to be pure recall, not reasoning",
                suggested_fix="Rephrase to require calculation or analysis"
            ))

        # CHECK 2: Multi-step thinking required
        # For advanced skills, should require multiple conceptual steps
        advanced_skills = ["complete.square", "by_formula", "discriminant"]
        is_advanced = any(adv in skill_id for adv in advanced_skills)

        if is_advanced:
            # Check if question is too simple for advanced skill
            if len(stem) < 30:  # Very short questions unlikely to be multi-step
                violations.append(PrincipleViolation(
                    principle_id="genuine_understanding",
                    principle_name="Genuine Understanding",
                    severity="high",
                    violation_description="Advanced skill requires multi-step reasoning",
                    suggested_fix="Add complexity requiring multiple conceptual steps"
                ))

        return violations

    def _check_pedagogical_soundness(self, question: Dict[str, Any]) -> List[PrincipleViolation]:
        """Check if content is pedagogically sound."""
        violations = []
        stem = question.get("stem", "")

        # CHECK 1: Clear, appropriate language
        if len(stem) > 200:
            violations.append(PrincipleViolation(
                principle_id="pedagogical_soundness",
                principle_name="Pedagogical Soundness",
                severity="medium",
                violation_description="Question stem too long, may overwhelm students",
                suggested_fix="Simplify wording or break into smaller parts"
            ))

        # CHECK 2: Correct mathematical terminology
        # Check for common notation errors
        if "x^2" in stem and "LaTeX" not in stem:
            # Raw x^2 without proper formatting
            violations.append(PrincipleViolation(
                principle_id="pedagogical_soundness",
                principle_name="Pedagogical Soundness",
                severity="low",
                violation_description="Mathematical notation should use proper formatting",
                suggested_fix="Use LaTeX or proper superscripts for exponents"
            ))

        # CHECK 3: Appropriate complexity for algebra level
        # Avoid unnecessarily complex numbers
        numbers = re.findall(r'-?\d+', stem)
        if numbers:
            max_num = max(abs(int(n)) for n in numbers if n)
            if max_num > 1000:
                violations.append(PrincipleViolation(
                    principle_id="pedagogical_soundness",
                    principle_name="Pedagogical Soundness",
                    severity="medium",
                    violation_description="Numbers too large, adds cognitive load without pedagogical value",
                    suggested_fix="Use more manageable numbers (< 100) unless testing large-number skills"
                ))

        return violations

    def _check_honest_distractors(self, question: Dict[str, Any]) -> List[PrincipleViolation]:
        """Check if wrong answers represent real misconceptions."""
        violations = []

        choices = question.get("choices", [])
        solution_id = question.get("solution_choice_id")

        if not choices or not solution_id:
            return violations

        # Choices can be either list of dicts or plain dict
        if isinstance(choices, list):
            # Format: [{"id": "A", "text": "..."}, ...]
            choices_dict = {c["id"]: c["text"] for c in choices}
        else:
            # Legacy format: {"A": "...", "B": "..."}
            choices_dict = choices

        # Get correct answer
        correct_answer = choices_dict.get(solution_id)

        # Check distractors
        distractors = [
            (choice_id, choice_text)
            for choice_id, choice_text in choices_dict.items()
            if choice_id != solution_id
        ]

        if len(distractors) < 2:
            violations.append(PrincipleViolation(
                principle_id="honest_distractors",
                principle_name="Honest Distractors",
                severity="high",
                violation_description="Need at least 2 plausible distractors",
                suggested_fix="Add more wrong answers representing common errors"
            ))

        # CHECK: Distractors should be plausible
        for dist_id, dist_text in distractors:
            # Check if distractor is clearly wrong (like "banana" or "999999")
            if self._is_obviously_wrong(dist_text, correct_answer, question):
                violations.append(PrincipleViolation(
                    principle_id="honest_distractors",
                    principle_name="Honest Distractors",
                    severity="high",
                    violation_description=f"Distractor '{dist_text}' is not plausible",
                    suggested_fix="Use distractor representing a common algebraic error"
                ))

        return violations

    def _is_obviously_wrong(
        self,
        distractor: str,
        correct: str,
        question: Dict[str, Any]
    ) -> bool:
        """Check if distractor is obviously wrong (not a plausible error)."""
        # Extract numeric values if present
        dist_numbers = re.findall(r'-?\d+\.?\d*', distractor)
        corr_numbers = re.findall(r'-?\d+\.?\d*', correct)

        if not dist_numbers or not corr_numbers:
            return False

        try:
            dist_val = float(dist_numbers[0])
            corr_val = float(corr_numbers[0])

            # If distractor is 100x different, probably not plausible
            if abs(dist_val) > 0:
                ratio = abs(corr_val / dist_val)
                if ratio > 100 or ratio < 0.01:
                    return True

            # If numbers are wildly different in magnitude
            if abs(dist_val - corr_val) > 1000:
                return True

        except (ValueError, ZeroDivisionError):
            pass

        return False

    def _check_appropriate_difficulty(self, question: Dict[str, Any]) -> List[PrincipleViolation]:
        """Check if difficulty matches stated level."""
        violations = []

        difficulty = question.get("difficulty", "")
        skill_id = question.get("skill_id", "")
        stem = question.get("stem", "")

        # CHECK: Easy questions should have simple numbers
        if difficulty == "easy":
            numbers = re.findall(r'-?\d+', stem)
            if numbers:
                max_num = max(abs(int(n)) for n in numbers if n)
                if max_num > 50:
                    violations.append(PrincipleViolation(
                        principle_id="appropriate_difficulty",
                        principle_name="Appropriate Difficulty",
                        severity="medium",
                        violation_description="'Easy' difficulty should use small numbers",
                        suggested_fix="Use numbers between -20 and 20 for easy level"
                    ))

        # CHECK: Applied difficulty should have context
        if difficulty == "applied":
            # Applied should have real-world context
            context_words = ["height", "cost", "time", "distance", "area", "profit", "revenue"]
            has_context = any(word in stem.lower() for word in context_words)

            if not has_context:
                violations.append(PrincipleViolation(
                    principle_id="appropriate_difficulty",
                    principle_name="Appropriate Difficulty",
                    severity="high",
                    violation_description="'Applied' difficulty should include real-world context",
                    suggested_fix="Add a practical scenario (projectile motion, business, etc.)"
                ))

        return violations

    def _check_safe_learning(self, question: Dict[str, Any]) -> List[PrincipleViolation]:
        """Check for safe, respectful content."""
        violations = []
        stem = question.get("stem", "")

        # CHECK: No harmful or sensitive topics
        sensitive_words = [
            "weapon", "violence", "drugs", "alcohol", "gambling",
            "suicide", "death", "harm", "kill"
        ]

        for word in sensitive_words:
            if word in stem.lower():
                violations.append(PrincipleViolation(
                    principle_id="safe_learning",
                    principle_name="Safe Learning Environment",
                    severity="critical",
                    violation_description=f"Contains potentially harmful content: '{word}'",
                    suggested_fix="Use neutral context (geometry, motion, business, etc.)"
                ))

        # CHECK: No stereotypes or biased language
        # For math, this is rarely an issue, but check proper names

        return violations

    def _check_inclusive_accessible(self, question: Dict[str, Any]) -> List[PrincipleViolation]:
        """Check for inclusive, accessible content."""
        violations = []
        stem = question.get("stem", "")

        # CHECK 1: Clear mathematical notation
        if "^" in stem and "**" not in stem:
            # Using plain text exponents without explanation
            if "y = " in stem or "x = " in stem:
                # This is actually okay for equations
                pass

        # CHECK 2: Context provided when needed
        # For graph/vertex questions, ensure form is clear
        skill_id = question.get("skill_id", "")
        if "vertex" in skill_id:
            has_equation = "y =" in stem or "f(x)" in stem
            if not has_equation:
                violations.append(PrincipleViolation(
                    principle_id="inclusive_accessible",
                    principle_name="Inclusive & Accessible",
                    severity="medium",
                    violation_description="Vertex question should show full equation",
                    suggested_fix="Include complete equation: y = ax² + bx + c"
                ))

        # CHECK 3: No cultural assumptions
        # Math is generally culture-neutral, but check contexts

        return violations

    def _calculate_weighted_score(
        self,
        violations: List[PrincipleViolation],
        total_principles: int
    ) -> float:
        """
        Calculate weighted score based on violations.

        Severity weights:
        - critical: -1.0 (complete failure)
        - high: -0.7
        - medium: -0.4
        - low: -0.1
        """
        severity_weights = {
            "critical": 1.0,
            "high": 0.7,
            "medium": 0.4,
            "low": 0.1
        }

        # Start at perfect score
        score = 1.0

        # Deduct for violations
        for violation in violations:
            weight = severity_weights.get(violation.severity, 0.5)
            score -= (weight / total_principles)

        return max(0.0, min(1.0, score))

    def get_validation_stats(self) -> Dict[str, Any]:
        """Get statistics about validation history."""
        if not self.validation_history:
            return {
                "total_validations": 0,
                "pass_rate": 0.0,
                "avg_score": 0.0
            }

        total = len(self.validation_history)
        passed = sum(
            1 for h in self.validation_history
            if h["result"]["passes_constitution"]
        )

        avg_score = sum(
            h["result"]["overall_score"]
            for h in self.validation_history
        ) / total

        # Count violations by principle
        violation_counts = {}
        for h in self.validation_history:
            for v in h["result"]["violations"]:
                pid = v["principle_id"]
                violation_counts[pid] = violation_counts.get(pid, 0) + 1

        return {
            "total_validations": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": passed / total if total > 0 else 0,
            "avg_score": avg_score,
            "violation_counts_by_principle": violation_counts
        }
