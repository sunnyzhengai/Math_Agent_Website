"""
Learning Path Planner: Multi-step planning for skill mastery.

Implements Andrew Ng's Planning pattern:
- Analyzes prerequisite dependencies
- Identifies skill gaps
- Sequences skills using topological sort
- Estimates time to mastery
- Creates checkpoints and milestones
- Plans spaced repetition reviews
"""

from typing import Dict, List, Set, Any, NamedTuple, Optional
from collections import deque, defaultdict


class LearningPhase(NamedTuple):
    """A single phase in the learning plan."""
    skill_id: str
    estimated_hours: float
    start_offset_hours: float
    success_criteria: Dict[str, Any]
    checkpoint: Dict[str, Any]
    review_schedule: List[int]  # Days after completion
    fallback_strategies: List[Dict[str, str]]


class LearningPlan(NamedTuple):
    """Complete learning plan to mastery."""
    target_skill: str
    phases: List[LearningPhase]
    total_estimated_hours: float
    review_sessions: List[Dict[str, Any]]
    prerequisite_chain: List[str]


class StudentProfile:
    """Simplified student profile for planning."""

    def __init__(
        self,
        student_id: str,
        mastered_skills: List[str] = None,
        learning_rate_avg: float = 0.15,
        current_progress: Dict[str, float] = None
    ):
        """
        Initialize student profile.

        Args:
            student_id: Unique student identifier
            mastered_skills: List of skill IDs student has mastered
            learning_rate_avg: Estimated questions per hour to achieve mastery
            current_progress: Dict of skill_id -> progress (0-1)
        """
        self.student_id = student_id
        self.mastered_skills = mastered_skills or []
        self.learning_rate_avg = learning_rate_avg
        self.current_progress = current_progress or {}

    def get_mastery_levels(self) -> Dict[str, float]:
        """Get mastery level for all skills (0-1)."""
        mastery = {}
        for skill in self.mastered_skills:
            mastery[skill] = 1.0
        for skill, progress in self.current_progress.items():
            if skill not in mastery:
                mastery[skill] = progress
        return mastery


class LearningPathPlanner:
    """
    Plans multi-session learning sequences to achieve mastery.

    Implements Andrew Ng's Planning pattern with:
    - Prerequisite analysis
    - Gap identification
    - Dependency-based sequencing
    - Time estimation
    - Checkpoint creation
    - Spaced repetition
    """

    # Prerequisite graph for quadratic equations
    PREREQUISITE_GRAPH = {
        # Basic reading skills (no prerequisites)
        "quad.graph.vertex": [],
        "quad.roots.factored": [],

        # Conversion skills (require reading)
        "quad.standard.vertex": ["quad.graph.vertex"],

        # Solving skills (require reading and understanding)
        "quad.solve.by_factoring": ["quad.roots.factored"],
        "quad.solve.by_formula": ["quad.discriminant.analysis"],

        # Analysis skills (require understanding forms)
        "quad.discriminant.analysis": ["quad.standard.vertex"],
        "quad.intercepts": ["quad.solve.by_factoring"],

        # Advanced skills (require solving methods)
        "quad.complete.square": ["quad.standard.vertex", "quad.solve.by_factoring"],
        "quad.axis.symmetry": ["quad.graph.vertex", "quad.standard.vertex"]
    }

    # Estimated questions needed to master each skill
    MASTERY_ESTIMATES = {
        "quad.graph.vertex": 15,  # Easy - reading from vertex form
        "quad.roots.factored": 15,  # Easy - reading from factored form
        "quad.standard.vertex": 25,  # Medium - conversion required
        "quad.solve.by_factoring": 30,  # Medium - multi-step solving
        "quad.solve.by_formula": 35,  # Hard - complex formula application
        "quad.discriminant.analysis": 20,  # Medium - analysis skill
        "quad.intercepts": 25,  # Medium - multiple concepts
        "quad.complete.square": 40,  # Hard - advanced technique
        "quad.axis.symmetry": 20,  # Medium - conceptual understanding
    }

    def __init__(self, mastery_threshold: float = 0.7):
        """
        Initialize learning path planner.

        Args:
            mastery_threshold: Minimum progress to consider skill mastered (0-1)
        """
        self.mastery_threshold = mastery_threshold

    def plan_to_mastery(
        self,
        student_profile: StudentProfile,
        target_skill: str
    ) -> LearningPlan:
        """
        Create detailed learning plan with steps, time estimates, checkpoints.

        Implements Andrew Ng's Planning pattern with:
        1. Prerequisite analysis
        2. Gap identification
        3. Dependency sequencing
        4. Time estimation
        5. Checkpoint creation
        6. Review scheduling

        Args:
            student_profile: Current student state
            target_skill: Skill to achieve mastery in

        Returns:
            LearningPlan with phases and checkpoints
        """
        # STEP 1: Analyze prerequisites
        prereq_chain = self._get_prerequisite_chain(target_skill)

        # STEP 2: Identify gaps
        current_mastery = student_profile.get_mastery_levels()
        missing_skills = [
            skill for skill in prereq_chain
            if current_mastery.get(skill, 0) < self.mastery_threshold
        ]

        # Add target skill if not mastered
        if current_mastery.get(target_skill, 0) < self.mastery_threshold:
            if target_skill not in missing_skills:
                missing_skills.append(target_skill)

        # STEP 3: Sequence skills (topological sort)
        if missing_skills:
            learning_sequence = self._topological_sort(missing_skills)
        else:
            learning_sequence = [target_skill]

        # STEP 4: Create phased plan
        phases = []
        cumulative_hours = 0.0

        for skill in learning_sequence:
            # Estimate time to mastery
            estimated_hours = self._estimate_time_to_mastery(
                skill,
                student_profile,
                current_mastery.get(skill, 0)
            )

            # Create phase
            phase = LearningPhase(
                skill_id=skill,
                estimated_hours=estimated_hours,
                start_offset_hours=cumulative_hours,
                success_criteria={
                    "mastery_probability": 0.8,
                    "minimum_attempts": 10,
                    "consecutive_correct": 3
                },
                checkpoint=self._create_checkpoint(skill),
                review_schedule=self._plan_spaced_reviews(skill),
                fallback_strategies=self._create_fallback_strategies(skill)
            )

            phases.append(phase)
            cumulative_hours += estimated_hours

        # STEP 5: Plan review sessions for already mastered skills
        review_sessions = []
        already_mastered = [
            skill for skill in student_profile.mastered_skills
            if skill not in learning_sequence
        ]

        for skill in already_mastered:
            review_sessions.extend(
                self._schedule_review_sessions(skill, spacing="fibonacci")
            )

        return LearningPlan(
            target_skill=target_skill,
            phases=phases,
            total_estimated_hours=cumulative_hours,
            review_sessions=review_sessions,
            prerequisite_chain=prereq_chain
        )

    def _get_prerequisite_chain(self, skill_id: str) -> List[str]:
        """
        Get all prerequisites for a skill (recursive).

        Args:
            skill_id: Target skill

        Returns:
            List of all prerequisite skills in order
        """
        visited = set()
        chain = []

        def dfs(skill: str):
            if skill in visited:
                return
            visited.add(skill)

            # Visit prerequisites first
            for prereq in self.PREREQUISITE_GRAPH.get(skill, []):
                dfs(prereq)

            chain.append(skill)

        dfs(skill_id)

        # Remove target skill from chain (will be added separately)
        if skill_id in chain:
            chain.remove(skill_id)

        return chain

    def _topological_sort(self, skills: List[str]) -> List[str]:
        """
        Order skills by dependency using topological sort.

        Args:
            skills: List of skills to order

        Returns:
            List of skills in dependency order
        """
        # Build subgraph for only the skills we care about
        in_degree = defaultdict(int)
        adj_list = defaultdict(list)

        skills_set = set(skills)

        for skill in skills:
            in_degree[skill] = 0

        for skill in skills:
            for prereq in self.PREREQUISITE_GRAPH.get(skill, []):
                if prereq in skills_set:
                    adj_list[prereq].append(skill)
                    in_degree[skill] += 1

        # Kahn's algorithm
        queue = deque([skill for skill in skills if in_degree[skill] == 0])
        result = []

        while queue:
            skill = queue.popleft()
            result.append(skill)

            for dependent in adj_list[skill]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        return result

    def _estimate_time_to_mastery(
        self,
        skill_id: str,
        student_profile: StudentProfile,
        current_progress: float
    ) -> float:
        """
        Estimate hours needed to master skill.

        Args:
            skill_id: Skill to estimate
            student_profile: Student's learning rate
            current_progress: Current progress (0-1)

        Returns:
            Estimated hours to mastery
        """
        # Get base questions needed
        questions_needed = self.MASTERY_ESTIMATES.get(skill_id, 20)

        # Adjust for current progress
        remaining_questions = questions_needed * (1 - current_progress)

        # Convert to hours using student's learning rate
        hours = remaining_questions / student_profile.learning_rate_avg

        return max(1.0, hours)  # At least 1 hour

    def _create_checkpoint(self, skill_id: str) -> Dict[str, Any]:
        """
        Create checkpoint assessment for skill.

        Args:
            skill_id: Skill to create checkpoint for

        Returns:
            Dict with checkpoint specification
        """
        return {
            "type": "mastery_check",
            "skill_id": skill_id,
            "questions": 5,
            "passing_score": 0.8,
            "description": f"Demonstrate mastery of {skill_id}"
        }

    def _plan_spaced_reviews(self, skill_id: str) -> List[int]:
        """
        Plan spaced repetition review schedule.

        Uses Fibonacci spacing: 1, 2, 3, 5, 8 days after completion

        Args:
            skill_id: Skill to schedule reviews for

        Returns:
            List of days after completion for reviews
        """
        return [1, 2, 3, 5, 8, 13]  # Fibonacci sequence in days

    def _create_fallback_strategies(self, skill_id: str) -> List[Dict[str, str]]:
        """
        Create fallback strategies for when student struggles.

        Args:
            skill_id: Skill to create fallbacks for

        Returns:
            List of fallback strategy dicts
        """
        return [
            {
                "condition": "no_progress_after_20_attempts",
                "action": "switch_to_easier_difficulty",
                "description": "Drop to easier difficulty level"
            },
            {
                "condition": "mastery_declining",
                "action": "provide_worked_examples",
                "description": "Show detailed step-by-step examples"
            },
            {
                "condition": "repeated_same_error",
                "action": "targeted_misconception_lesson",
                "description": "Address specific misconception"
            }
        ]

    def _schedule_review_sessions(
        self,
        skill_id: str,
        spacing: str = "fibonacci"
    ) -> List[Dict[str, Any]]:
        """
        Schedule review sessions for retention.

        Args:
            skill_id: Skill to review
            spacing: Spacing algorithm ("fibonacci", "exponential")

        Returns:
            List of review session specifications
        """
        if spacing == "fibonacci":
            days = [1, 2, 3, 5, 8, 13, 21]
        else:
            days = [1, 2, 4, 8, 16, 32]

        sessions = []
        for day in days:
            sessions.append({
                "skill_id": skill_id,
                "days_from_now": day,
                "questions": 3,
                "purpose": "retention_check"
            })

        return sessions
