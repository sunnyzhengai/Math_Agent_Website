"""
Student World Model: Internal model of student understanding.

Implements Yann LeCun's World Models philosophy:
- Build internal representation of student's conceptual state
- Predict future struggles before they happen
- Update model based on observations
- Enable proactive interventions

The world model maintains:
- Concept dependency graph
- Mastery levels for each concept
- Error patterns and misconceptions
- Learning velocity and trajectory
"""

from typing import Dict, List, Set, Any, NamedTuple, Optional
from collections import defaultdict
import time


class ConceptNode(NamedTuple):
    """A node in the concept graph representing understanding state."""
    concept_id: str
    mastery_level: float  # 0-1, current estimated mastery
    confidence: float  # 0-1, how confident we are in the estimate
    last_updated: float  # timestamp
    total_attempts: int
    correct_attempts: int
    common_errors: List[str]
    prerequisites: List[str]


class StrugglePrediction(NamedTuple):
    """Prediction of where student will struggle."""
    target_skill: str
    predicted_struggle_concepts: List[str]
    confidence: float  # 0-1
    reason: str
    intervention_suggestions: List[str]


class InterventionRecommendation(NamedTuple):
    """Recommended intervention to prevent struggle."""
    intervention_type: str  # "review_prerequisite", "scaffold_problem", "provide_hint"
    target_concept: str
    reason: str
    action: str
    priority: str  # "high", "medium", "low"


class StudentWorldModel:
    """
    Internal model of student's understanding.

    Implements Yann LeCun's World Models:
    - Predicts student's next actions/struggles
    - Learns from observations
    - Enables planning and intervention
    """

    # Concept dependency graph for quadratic equations
    CONCEPT_GRAPH = {
        # Basic concepts (no prerequisites)
        "parabola_shape": [],
        "coordinate_system": [],
        "function_notation": [],

        # Vertex form concepts
        "vertex_definition": ["parabola_shape", "coordinate_system"],
        "vertex_form_reading": ["vertex_definition", "function_notation"],
        "vertex_form_parameters": ["vertex_form_reading"],

        # Standard form concepts
        "standard_form_structure": ["function_notation"],
        "coefficient_effects": ["standard_form_structure", "parabola_shape"],

        # Conversion between forms
        "vertex_to_standard": ["vertex_form_parameters", "standard_form_structure"],
        "standard_to_vertex": ["standard_form_structure", "vertex_definition"],
        "completing_square": ["standard_to_vertex", "coefficient_effects"],

        # Solving concepts
        "factoring_basics": ["standard_form_structure"],
        "solve_by_factoring": ["factoring_basics"],
        "quadratic_formula": ["standard_form_structure", "coefficient_effects"],
        "discriminant": ["quadratic_formula"],

        # Analysis concepts
        "axis_of_symmetry": ["vertex_definition", "coefficient_effects"],
        "intercepts": ["solve_by_factoring", "coordinate_system"],
        "domain_range": ["parabola_shape", "vertex_definition"],
    }

    # Map skills to concepts
    SKILL_TO_CONCEPTS = {
        "quad.graph.vertex": ["vertex_form_reading", "vertex_definition"],
        "quad.roots.factored": ["factoring_basics", "solve_by_factoring"],
        "quad.standard.vertex": ["standard_to_vertex", "vertex_form_parameters"],
        "quad.solve.by_factoring": ["solve_by_factoring", "factoring_basics"],
        "quad.solve.by_formula": ["quadratic_formula", "discriminant"],
        "quad.discriminant.analysis": ["discriminant", "coefficient_effects"],
        "quad.complete.square": ["completing_square", "standard_to_vertex"],
        "quad.axis.symmetry": ["axis_of_symmetry", "vertex_definition"],
        "quad.intercepts": ["intercepts", "solve_by_factoring"],
    }

    def __init__(self):
        """Initialize the world model."""
        self.concept_nodes: Dict[str, ConceptNode] = {}
        self.learning_history: List[Dict[str, Any]] = []
        self.prediction_history: List[Dict[str, Any]] = []

        # Initialize all concept nodes
        for concept_id in self.CONCEPT_GRAPH.keys():
            self.concept_nodes[concept_id] = ConceptNode(
                concept_id=concept_id,
                mastery_level=0.0,
                confidence=0.0,
                last_updated=time.time(),
                total_attempts=0,
                correct_attempts=0,
                common_errors=[],
                prerequisites=self.CONCEPT_GRAPH[concept_id]
            )

    def update_from_performance(
        self,
        skill_id: str,
        correct: bool,
        time_taken: Optional[float] = None,
        error_type: Optional[str] = None
    ):
        """
        Update world model based on student performance.

        This is the "learning" part of the world model - updating internal
        representation based on observations.

        Args:
            skill_id: Skill student attempted
            correct: Whether they got it correct
            time_taken: Optional time taken (faster = higher mastery)
            error_type: Optional error classification
        """
        # Get concepts for this skill
        concepts = self.SKILL_TO_CONCEPTS.get(skill_id, [])

        for concept_id in concepts:
            if concept_id not in self.concept_nodes:
                continue

            node = self.concept_nodes[concept_id]

            # Update attempts
            new_total = node.total_attempts + 1
            new_correct = node.correct_attempts + (1 if correct else 0)

            # Calculate new mastery level using exponential moving average
            # This gives more weight to recent performance
            alpha = 0.3  # Learning rate
            observation = 1.0 if correct else 0.0
            new_mastery = alpha * observation + (1 - alpha) * node.mastery_level

            # Adjust mastery based on time taken (if provided)
            if correct and time_taken is not None:
                # Fast correct answers indicate higher mastery
                if time_taken < 30:
                    new_mastery = min(1.0, new_mastery + 0.05)
                elif time_taken > 120:
                    new_mastery = max(0.0, new_mastery - 0.05)

            # Update confidence (more attempts = more confident)
            new_confidence = min(1.0, new_total / 20.0)

            # Track error patterns
            new_errors = list(node.common_errors)
            if not correct and error_type:
                new_errors.append(error_type)
                # Keep only last 5 errors
                new_errors = new_errors[-5:]

            # Create updated node
            self.concept_nodes[concept_id] = ConceptNode(
                concept_id=concept_id,
                mastery_level=new_mastery,
                confidence=new_confidence,
                last_updated=time.time(),
                total_attempts=new_total,
                correct_attempts=new_correct,
                common_errors=new_errors,
                prerequisites=node.prerequisites
            )

        # Track in history
        self.learning_history.append({
            "timestamp": time.time(),
            "skill_id": skill_id,
            "correct": correct,
            "concepts_updated": concepts,
            "error_type": error_type
        })

    def predict_struggle(self, target_skill: str) -> StrugglePrediction:
        """
        Predict where student will struggle on target skill.

        This is the "predictive" part of the world model - using internal
        representation to forecast future states.

        Args:
            target_skill: Skill student is about to attempt

        Returns:
            StrugglePrediction with concepts likely to cause difficulty
        """
        # Get concepts required for this skill
        required_concepts = self.SKILL_TO_CONCEPTS.get(target_skill, [])

        struggle_concepts = []
        lowest_mastery = 1.0
        weakest_concept = None

        # Check mastery of required concepts
        for concept_id in required_concepts:
            if concept_id not in self.concept_nodes:
                continue

            node = self.concept_nodes[concept_id]

            # Low mastery indicates potential struggle
            if node.mastery_level < 0.6:
                struggle_concepts.append(concept_id)

                if node.mastery_level < lowest_mastery:
                    lowest_mastery = node.mastery_level
                    weakest_concept = concept_id

            # Also check prerequisites recursively
            for prereq in node.prerequisites:
                if prereq in self.concept_nodes:
                    prereq_node = self.concept_nodes[prereq]
                    if prereq_node.mastery_level < 0.5:
                        struggle_concepts.append(prereq)

        # Deduplicate
        struggle_concepts = list(set(struggle_concepts))

        # Generate interventions
        interventions = []
        if weakest_concept:
            interventions.append(f"Review {weakest_concept} (mastery: {lowest_mastery:.1%})")

            # Check if prerequisites of weakest concept are also weak
            weak_node = self.concept_nodes[weakest_concept]
            for prereq in weak_node.prerequisites:
                if prereq in self.concept_nodes:
                    prereq_node = self.concept_nodes[prereq]
                    if prereq_node.mastery_level < 0.6:
                        interventions.append(f"First strengthen {prereq} (prerequisite)")

        if not struggle_concepts:
            interventions.append("Student appears ready for this skill")

        # Calculate confidence in prediction
        # Higher confidence if we have more data
        avg_confidence = sum(
            self.concept_nodes[c].confidence
            for c in required_concepts
            if c in self.concept_nodes
        ) / max(len(required_concepts), 1)

        prediction = StrugglePrediction(
            target_skill=target_skill,
            predicted_struggle_concepts=struggle_concepts,
            confidence=avg_confidence,
            reason=f"Low mastery in {len(struggle_concepts)} required concepts" if struggle_concepts else "All prerequisites mastered",
            intervention_suggestions=interventions
        )

        # Track prediction
        self.prediction_history.append({
            "timestamp": time.time(),
            "target_skill": target_skill,
            "prediction": prediction._asdict()
        })

        return prediction

    def recommend_intervention(self, skill_id: str) -> List[InterventionRecommendation]:
        """
        Recommend proactive interventions before student attempts skill.

        Args:
            skill_id: Skill student is about to attempt

        Returns:
            List of intervention recommendations
        """
        prediction = self.predict_struggle(skill_id)
        recommendations = []

        if not prediction.predicted_struggle_concepts:
            # No intervention needed
            return recommendations

        # Create interventions for struggling concepts
        for concept_id in prediction.predicted_struggle_concepts:
            if concept_id not in self.concept_nodes:
                continue

            node = self.concept_nodes[concept_id]

            # Determine intervention type based on mastery level
            if node.mastery_level < 0.3:
                # Very low mastery - need to review prerequisites
                recommendations.append(InterventionRecommendation(
                    intervention_type="review_prerequisite",
                    target_concept=concept_id,
                    reason=f"Mastery too low ({node.mastery_level:.1%})",
                    action=f"Practice prerequisite concepts: {', '.join(node.prerequisites[:2])}",
                    priority="high"
                ))
            elif node.mastery_level < 0.6:
                # Moderate mastery - scaffold the problem
                recommendations.append(InterventionRecommendation(
                    intervention_type="scaffold_problem",
                    target_concept=concept_id,
                    reason=f"Moderate mastery ({node.mastery_level:.1%})",
                    action=f"Start with easier problems for {concept_id}, then progress",
                    priority="medium"
                ))
            else:
                # Just need a hint
                recommendations.append(InterventionRecommendation(
                    intervention_type="provide_hint",
                    target_concept=concept_id,
                    reason=f"Near mastery ({node.mastery_level:.1%}) but not solid",
                    action=f"Provide hints related to {concept_id}",
                    priority="low"
                ))

        return recommendations

    def get_mastery_summary(self) -> Dict[str, Any]:
        """Get summary of student's overall mastery."""
        if not self.concept_nodes:
            return {
                "total_concepts": 0,
                "mastered": 0,
                "in_progress": 0,
                "not_started": 0
            }

        mastered = sum(1 for n in self.concept_nodes.values() if n.mastery_level >= 0.8)
        in_progress = sum(1 for n in self.concept_nodes.values() if 0.3 <= n.mastery_level < 0.8)
        not_started = sum(1 for n in self.concept_nodes.values() if n.mastery_level < 0.3)

        avg_mastery = sum(n.mastery_level for n in self.concept_nodes.values()) / len(self.concept_nodes)

        # Find strongest and weakest concepts
        sorted_concepts = sorted(
            self.concept_nodes.values(),
            key=lambda n: n.mastery_level,
            reverse=True
        )

        return {
            "total_concepts": len(self.concept_nodes),
            "mastered": mastered,
            "in_progress": in_progress,
            "not_started": not_started,
            "avg_mastery": avg_mastery,
            "strongest_concepts": [n.concept_id for n in sorted_concepts[:3]],
            "weakest_concepts": [n.concept_id for n in sorted_concepts[-3:]],
            "total_attempts": sum(n.total_attempts for n in self.concept_nodes.values()),
            "overall_accuracy": (
                sum(n.correct_attempts for n in self.concept_nodes.values()) /
                max(sum(n.total_attempts for n in self.concept_nodes.values()), 1)
            )
        }

    def get_learning_trajectory(self, concept_id: str) -> Dict[str, Any]:
        """
        Get learning trajectory for a specific concept.

        Args:
            concept_id: Concept to analyze

        Returns:
            Dict with trajectory information
        """
        if concept_id not in self.concept_nodes:
            return {"error": "Concept not found"}

        node = self.concept_nodes[concept_id]

        # Get historical performance from learning history
        concept_history = [
            event for event in self.learning_history
            if concept_id in event.get("concepts_updated", [])
        ]

        return {
            "concept_id": concept_id,
            "current_mastery": node.mastery_level,
            "confidence": node.confidence,
            "total_attempts": node.total_attempts,
            "accuracy": node.correct_attempts / max(node.total_attempts, 1),
            "recent_errors": node.common_errors[-3:],
            "learning_events": len(concept_history),
            "trend": "improving" if node.mastery_level > 0.5 else "needs_work"
        }

    def simulate_future_performance(
        self,
        skill_sequence: List[str],
        num_attempts_per_skill: int = 5
    ) -> Dict[str, Any]:
        """
        Simulate future performance on a sequence of skills.

        This demonstrates the "planning" capability of world models -
        using the internal model to simulate future scenarios.

        Args:
            skill_sequence: Sequence of skills to simulate
            num_attempts_per_skill: Simulated attempts per skill

        Returns:
            Dict with simulation results
        """
        simulation_results = []

        for skill_id in skill_sequence:
            prediction = self.predict_struggle(skill_id)

            # Estimate success probability based on prerequisite mastery
            required_concepts = self.SKILL_TO_CONCEPTS.get(skill_id, [])
            avg_mastery = sum(
                self.concept_nodes[c].mastery_level
                for c in required_concepts
                if c in self.concept_nodes
            ) / max(len(required_concepts), 1)

            # Success probability is roughly equal to average prerequisite mastery
            success_prob = avg_mastery

            simulation_results.append({
                "skill_id": skill_id,
                "predicted_success_rate": success_prob,
                "struggle_concepts": prediction.predicted_struggle_concepts,
                "recommended_prep": prediction.intervention_suggestions[:2]
            })

        return {
            "skill_sequence": skill_sequence,
            "simulations": simulation_results,
            "overall_readiness": sum(s["predicted_success_rate"] for s in simulation_results) / len(simulation_results)
        }
