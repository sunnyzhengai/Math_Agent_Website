"""
Question Validation Committee: Multi-agent system for collaborative validation.

Implements Andrew Ng's Multi-Agent Collaboration pattern where multiple
specialized agents work together to validate question quality.

Each agent has veto power - all must approve for question to pass.
"""

from typing import Dict, Any, List, NamedTuple, Optional
from .oracle import OracleAgent
from .clarity_agent import ClarityAgent
from .difficulty_agent import DifficultyAgent
from .distractor_agent import DistractorAgent


class ValidationResult(NamedTuple):
    """Result of committee validation."""
    approved: bool
    consensus_score: float
    failed_agent: Optional[str]
    reason: Optional[str]
    fix_suggestion: Optional[str]
    validating_agents: List[str]
    details: Dict[str, Any]


class QuestionValidationCommittee:
    """
    Multi-agent system for collaborative question validation.

    Implements Andrew Ng's Multi-Agent Collaboration pattern:
    - Multiple specialized agents each validate different aspects
    - All agents must approve (veto power)
    - Provides detailed feedback for improvements
    - Ensures high-quality questions reach students
    """

    def __init__(self, use_reflection: bool = True):
        """
        Initialize the validation committee.

        Args:
            use_reflection: Whether to enable reflection in Oracle Agent
        """
        self.oracle_agent = OracleAgent(use_reflection=use_reflection)
        self.clarity_agent = ClarityAgent()
        self.difficulty_agent = DifficultyAgent()
        self.distractor_agent = DistractorAgent()

        self.validation_history = []

    def validate_question(
        self,
        question: Dict[str, Any],
        strict: bool = True
    ) -> ValidationResult:
        """
        All agents validate the question. Each has veto power.

        Args:
            question: Question item dict with stem, choices, solution, etc.
            strict: If True, requires all agents to pass. If False, requires majority.

        Returns:
            ValidationResult with approval status and detailed feedback
        """
        # Track which agents approve
        agent_results = {}
        details = {}

        # AGENT 1: Oracle - Correctness validation
        oracle_answer = self.oracle_agent.choose(question)
        correct_answer = question.get("solution_choice_id", "")
        oracle_correct = (oracle_answer == correct_answer)

        agent_results["oracle"] = oracle_correct
        details["oracle"] = {
            "answer": oracle_answer,
            "expected": correct_answer,
            "correct": oracle_correct
        }

        if not oracle_correct:
            result = ValidationResult(
                approved=False,
                consensus_score=0.0,
                failed_agent="oracle",
                reason=f"Oracle solved incorrectly: got {oracle_answer}, expected {correct_answer}",
                fix_suggestion="Review answer key and solution generation logic",
                validating_agents=["oracle"],
                details=details
            )
            self._track_validation(question, result)
            return result

        # AGENT 2: Clarity - Readability check
        stem = question.get("stem", "")
        clarity_score = self.clarity_agent.evaluate(stem)
        clarity_threshold = 0.7 if strict else 0.5

        agent_results["clarity"] = clarity_score >= clarity_threshold
        details["clarity"] = {
            "score": clarity_score,
            "threshold": clarity_threshold,
            "passed": clarity_score >= clarity_threshold
        }

        if clarity_score < clarity_threshold:
            improvements = self.clarity_agent.suggest_improvements(question)
            result = ValidationResult(
                approved=False,
                consensus_score=clarity_score,
                failed_agent="clarity",
                reason=f"Unclear wording (score: {clarity_score:.2f}, needs {clarity_threshold:.2f})",
                fix_suggestion="; ".join(improvements),
                validating_agents=["oracle", "clarity"],
                details=details
            )
            self._track_validation(question, result)
            return result

        # AGENT 3: Difficulty - Calibration check
        estimated_difficulty = self.difficulty_agent.estimate(question)
        target_label = question.get("difficulty", "easy")
        target_score = self.difficulty_agent.DIFFICULTY_MAP.get(target_label, 0.5)

        difficulty_tolerance = 0.25 if strict else 0.35
        difficulty_match = abs(estimated_difficulty - target_score) <= difficulty_tolerance

        agent_results["difficulty"] = difficulty_match
        details["difficulty"] = {
            "estimated": estimated_difficulty,
            "estimated_label": self.difficulty_agent.get_difficulty_label(estimated_difficulty),
            "target": target_score,
            "target_label": target_label,
            "difference": abs(estimated_difficulty - target_score),
            "tolerance": difficulty_tolerance,
            "passed": difficulty_match
        }

        if not difficulty_match:
            estimated_label = self.difficulty_agent.get_difficulty_label(estimated_difficulty)
            result = ValidationResult(
                approved=False,
                consensus_score=1.0 - abs(estimated_difficulty - target_score),
                failed_agent="difficulty",
                reason=f"Difficulty mismatch: estimated '{estimated_label}' ({estimated_difficulty:.2f}), labeled '{target_label}' ({target_score:.2f})",
                fix_suggestion=f"Either adjust problem complexity or relabel as '{estimated_label}'",
                validating_agents=["oracle", "clarity", "difficulty"],
                details=details
            )
            self._track_validation(question, result)
            return result

        # AGENT 4: Distractors - Wrong answer quality
        distractor_quality = self.distractor_agent.evaluate(question)
        distractor_threshold = 2 if strict else 1  # Min plausible distractors

        agent_results["distractors"] = distractor_quality.plausible_count >= distractor_threshold
        details["distractors"] = {
            "plausible_count": distractor_quality.plausible_count,
            "total_distractors": distractor_quality.total_distractors,
            "quality_score": distractor_quality.quality_score,
            "threshold": distractor_threshold,
            "issues": distractor_quality.issues,
            "passed": distractor_quality.plausible_count >= distractor_threshold
        }

        if distractor_quality.plausible_count < distractor_threshold:
            result = ValidationResult(
                approved=False,
                consensus_score=distractor_quality.quality_score,
                failed_agent="distractors",
                reason=f"Insufficient plausible wrong answers ({distractor_quality.plausible_count}/{distractor_quality.total_distractors} plausible, need {distractor_threshold})",
                fix_suggestion="; ".join(distractor_quality.improvement_suggestions),
                validating_agents=["oracle", "clarity", "difficulty", "distractors"],
                details=details
            )
            self._track_validation(question, result)
            return result

        # ALL AGENTS APPROVED - Calculate consensus score
        consensus_score = (
            1.0 +  # Oracle (binary: pass/fail)
            clarity_score +
            (1.0 - abs(estimated_difficulty - target_score)) +  # Difficulty accuracy
            distractor_quality.quality_score
        ) / 4.0

        result = ValidationResult(
            approved=True,
            consensus_score=consensus_score,
            failed_agent=None,
            reason="All validation agents approved",
            fix_suggestion="Question meets quality standards",
            validating_agents=["oracle", "clarity", "difficulty", "distractors"],
            details=details
        )

        self._track_validation(question, result)
        return result

    def _track_validation(self, question: Dict[str, Any], result: ValidationResult):
        """Track validation for analytics."""
        self.validation_history.append({
            "question_id": question.get("id"),
            "skill_id": question.get("skill_id"),
            "difficulty": question.get("difficulty"),
            "result": result._asdict()
        })

    def get_validation_stats(self) -> Dict[str, Any]:
        """
        Get statistics about validation history.

        Returns:
            Dict with approval rates, common failure reasons, etc.
        """
        if not self.validation_history:
            return {
                "total_validations": 0,
                "approval_rate": 0.0,
                "avg_consensus_score": 0.0
            }

        total = len(self.validation_history)
        approved = sum(1 for v in self.validation_history if v["result"]["approved"])

        consensus_scores = [v["result"]["consensus_score"] for v in self.validation_history]
        avg_consensus = sum(consensus_scores) / len(consensus_scores) if consensus_scores else 0.0

        # Count failures by agent
        failed_agents = {}
        for v in self.validation_history:
            if not v["result"]["approved"]:
                agent = v["result"]["failed_agent"]
                failed_agents[agent] = failed_agents.get(agent, 0) + 1

        return {
            "total_validations": total,
            "approved": approved,
            "rejected": total - approved,
            "approval_rate": approved / total if total > 0 else 0.0,
            "avg_consensus_score": avg_consensus,
            "failures_by_agent": failed_agents
        }

    def validate_batch(
        self,
        questions: List[Dict[str, Any]],
        strict: bool = True
    ) -> List[ValidationResult]:
        """
        Validate multiple questions.

        Args:
            questions: List of question items
            strict: Whether to use strict validation

        Returns:
            List of ValidationResults
        """
        return [self.validate_question(q, strict=strict) for q in questions]

    def get_approved_questions(
        self,
        questions: List[Dict[str, Any]],
        strict: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Filter questions to only those approved by committee.

        Args:
            questions: List of question items
            strict: Whether to use strict validation

        Returns:
            List of approved questions
        """
        approved = []
        for question in questions:
            result = self.validate_question(question, strict=strict)
            if result.approved:
                approved.append(question)

        return approved
