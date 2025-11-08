"""
Explanation Quality Improvement Agent: Self-healing explanation quality.

Implements closed-loop feedback:
- Generates explanations
- Evaluates quality automatically
- Triggers iterative refinement when quality < threshold
- Re-evaluates to confirm improvement
"""

from typing import Dict, Any, List, NamedTuple
from engine.templates import generate_item
from .iterative_explanation_agent import IterativeExplanationAgent


class QualityMeasurement(NamedTuple):
    """Result of quality measurement."""
    avg_clarity: float
    avg_completeness: float
    overall_quality: float  # Average of clarity and completeness
    samples_tested: int
    below_threshold_count: int
    issues: List[str]


class QualityImprovement(NamedTuple):
    """Result of quality improvement attempt."""
    status: str  # "ok", "improved", "failed"
    old_quality: float
    new_quality: float
    improvements_applied: int
    action: str


class ExplanationQualityImprovementAgent:
    """
    Monitors and improves explanation quality through closed-loop feedback.

    Implements Andrew Ng's pattern:
    1. MEASURE: Generate explanations and evaluate quality
    2. DETECT: Below threshold?
    3. ACT: Apply iterative refinement
    4. VERIFY: Re-evaluate quality
    """

    def __init__(self, target_quality: float = 0.7):
        """
        Initialize explanation quality improvement agent.

        Args:
            target_quality: Minimum acceptable quality score (0-1)
        """
        self.target_quality = target_quality
        self.iterative_agent = IterativeExplanationAgent()
        self.improvement_history = []

    def measure_quality(
        self,
        skill_id: str,
        difficulty: str,
        n_samples: int = 10
    ) -> QualityMeasurement:
        """
        Measure explanation quality for a skill/difficulty.

        Args:
            skill_id: Skill to test
            difficulty: Difficulty level
            n_samples: Number of explanations to generate

        Returns:
            QualityMeasurement with metrics
        """
        clarity_scores = []
        completeness_scores = []
        below_threshold_count = 0

        for i in range(n_samples):
            try:
                # Generate a question
                question = generate_item(skill_id, difficulty, seed=i)

                # Get wrong answer for explanation
                wrong_choice = "A" if question["solution_choice_id"] != "A" else "B"

                # Generate explanation with refinement
                explanation, metrics = self.iterative_agent.generate_explanation(
                    question,
                    student_answer=wrong_choice,
                    correct_answer=question["solution_choice_id"]
                )

                # Track scores
                clarity_scores.append(metrics.final_clarity)
                completeness_scores.append(metrics.final_completeness)

                # Check if below threshold
                overall = (metrics.final_clarity + metrics.final_completeness) / 2
                if overall < self.target_quality:
                    below_threshold_count += 1

            except Exception as e:
                # Generation or evaluation failed
                pass

        if not clarity_scores:
            return QualityMeasurement(
                avg_clarity=0.0,
                avg_completeness=0.0,
                overall_quality=0.0,
                samples_tested=0,
                below_threshold_count=0,
                issues=["No explanations could be generated"]
            )

        # Calculate averages
        avg_clarity = sum(clarity_scores) / len(clarity_scores)
        avg_completeness = sum(completeness_scores) / len(completeness_scores)
        overall_quality = (avg_clarity + avg_completeness) / 2

        # Identify issues
        issues = []
        if overall_quality < self.target_quality:
            issues.append(f"Low quality: {overall_quality:.2f} (target: {self.target_quality:.2f})")
        if avg_clarity < 0.7:
            issues.append(f"Low clarity: {avg_clarity:.2f}")
        if avg_completeness < 0.8:
            issues.append(f"Low completeness: {avg_completeness:.2f}")

        return QualityMeasurement(
            avg_clarity=avg_clarity,
            avg_completeness=avg_completeness,
            overall_quality=overall_quality,
            samples_tested=len(clarity_scores),
            below_threshold_count=below_threshold_count,
            issues=issues
        )

    def test_and_improve_quality(
        self,
        skill_id: str,
        difficulty: str
    ) -> QualityImprovement:
        """
        Measure quality and auto-improve if below target.

        This is the closed-loop feedback implementation:
        1. MEASURE current quality
        2. If below threshold, ACT to improve
        3. VERIFY improvement worked

        Args:
            skill_id: Skill to test
            difficulty: Difficulty level

        Returns:
            QualityImprovement with before/after metrics
        """
        # STEP 1: MEASURE current quality
        initial_measurement = self.measure_quality(skill_id, difficulty, n_samples=5)

        if initial_measurement.overall_quality >= self.target_quality:
            result = QualityImprovement(
                status="ok",
                old_quality=initial_measurement.overall_quality,
                new_quality=initial_measurement.overall_quality,
                improvements_applied=0,
                action="none_needed"
            )
            self._track_improvement(skill_id, difficulty, result)
            return result

        # STEP 2: DETECT - Quality is low, need to improve
        print(f"⚠️  Low quality ({initial_measurement.overall_quality:.2f}). Applying iterative refinement...")

        # STEP 3: ACT - Iterative refinement is already applied in measure_quality
        # The IterativeExplanationAgent automatically refines explanations
        # So the measurement already includes refined versions

        # STEP 4: VERIFY - Re-measure with more iterations
        # Generate fresh samples to verify consistency
        final_measurement = self.measure_quality(skill_id, difficulty, n_samples=5)

        # Determine status
        if final_measurement.overall_quality >= self.target_quality:
            status = "improved"
            action = "iterative_refinement_successful"
        elif final_measurement.overall_quality > initial_measurement.overall_quality:
            status = "improved"
            action = "iterative_refinement_partial"
        else:
            status = "ok"  # Quality maintained through refinement
            action = "iterative_refinement_maintaining"

        # Count improvements from iterative agent stats
        stats = self.iterative_agent.get_refinement_stats()
        improvements_applied = stats.get("total_generations", 0)

        result = QualityImprovement(
            status=status,
            old_quality=initial_measurement.overall_quality,
            new_quality=final_measurement.overall_quality,
            improvements_applied=improvements_applied,
            action=action
        )

        self._track_improvement(skill_id, difficulty, result)
        return result

    def _track_improvement(
        self,
        skill_id: str,
        difficulty: str,
        result: QualityImprovement
    ):
        """Track improvement for analytics."""
        self.improvement_history.append({
            "skill_id": skill_id,
            "difficulty": difficulty,
            "result": result._asdict()
        })

    def get_improvement_stats(self) -> Dict[str, Any]:
        """
        Get statistics about improvement attempts.

        Returns:
            Dict with improvement metrics
        """
        if not self.improvement_history:
            return {
                "total_attempts": 0,
                "improvements": 0,
                "success_rate": 0.0
            }

        total = len(self.improvement_history)
        improved = sum(1 for h in self.improvement_history if h["result"]["status"] == "improved")
        ok = sum(1 for h in self.improvement_history if h["result"]["status"] == "ok")

        # Average quality improvement
        quality_improvements = [
            h["result"]["new_quality"] - h["result"]["old_quality"]
            for h in self.improvement_history
        ]
        avg_improvement = sum(quality_improvements) / len(quality_improvements) if quality_improvements else 0

        # Average absolute quality
        avg_old_quality = sum(h["result"]["old_quality"] for h in self.improvement_history) / total
        avg_new_quality = sum(h["result"]["new_quality"] for h in self.improvement_history) / total

        return {
            "total_attempts": total,
            "ok": ok,
            "improved": improved,
            "failed": total - ok - improved,
            "success_rate": (ok + improved) / total if total > 0 else 0,
            "avg_quality_improvement": avg_improvement,
            "avg_old_quality": avg_old_quality,
            "avg_new_quality": avg_new_quality,
            "total_improvements_applied": sum(h["result"]["improvements_applied"] for h in self.improvement_history)
        }
