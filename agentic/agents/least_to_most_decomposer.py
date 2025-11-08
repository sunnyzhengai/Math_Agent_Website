"""
Least-to-Most Decomposer: Break complex problems into simpler subproblems.

Implements Denny Zhou's (Google) Least-to-Most prompting:
- Start with the simplest version of a problem
- Solve that first
- Gradually add complexity
- Build understanding incrementally

This reduces cognitive overload and enables mastery at each level before
progressing to the next.

For quadratic equations, complexity dimensions:
- Coefficient (a = 1 vs a ≠ 1)
- Horizontal shift (h = 0 vs h ≠ 0)
- Vertical shift (k = 0 vs k ≠ 0)
- Sign (positive vs negative)
- Magnitude (small numbers vs large)
"""

from typing import Dict, List, Any, NamedTuple, Optional
import re


class ComplexityLevel(NamedTuple):
    """A complexity level with specific features."""
    level: int  # 1 (simplest) to 5 (most complex)
    description: str
    features: Dict[str, Any]
    example: str


class DecomposedProblem(NamedTuple):
    """A problem broken down into progressive levels."""
    original_problem: str
    original_complexity: int
    levels: List[ComplexityLevel]
    learning_sequence: List[str]
    explanation: str


class ScaffoldedPractice(NamedTuple):
    """Scaffolded practice sequence."""
    problems: List[Dict[str, Any]]
    difficulty_progression: List[int]
    scaffolding_notes: List[str]


class LeastToMostDecomposer:
    """
    Decomposes complex problems into simpler subproblems.

    Implements Denny Zhou's Least-to-Most pattern:
    1. Identify problem complexity
    2. Generate simpler versions
    3. Create learning sequence (simple → complex)
    4. Provide scaffolded practice
    """

    # Complexity dimensions for vertex form problems
    VERTEX_FORM_COMPLEXITY = {
        "coefficient": {
            "simple": {"value": 1, "description": "a = 1"},
            "complex": {"value": "≠1", "description": "a ≠ 1"}
        },
        "horizontal_shift": {
            "simple": {"value": 0, "description": "No horizontal shift (h = 0)"},
            "complex": {"value": "≠0", "description": "Horizontal shift (h ≠ 0)"}
        },
        "vertical_shift": {
            "simple": {"value": 0, "description": "No vertical shift (k = 0)"},
            "complex": {"value": "≠0", "description": "Vertical shift (k ≠ 0)"}
        },
        "sign": {
            "simple": {"value": "positive", "description": "Positive values"},
            "complex": {"value": "mixed", "description": "Mixed positive/negative"}
        }
    }

    def __init__(self):
        """Initialize decomposer."""
        self.decomposition_history = []

    def decompose_problem(
        self,
        problem: str,
        skill_id: str,
        target_concept: str
    ) -> DecomposedProblem:
        """
        Decompose a problem into progressive complexity levels.

        Args:
            problem: Original problem statement
            skill_id: Skill being practiced
            target_concept: Main concept (e.g., "vertex", "factoring")

        Returns:
            DecomposedProblem with levels from simplest to most complex
        """
        # Analyze original complexity
        original_complexity = self._analyze_complexity(problem, skill_id)

        # Generate progressive levels
        levels = self._generate_progressive_levels(problem, skill_id, target_concept)

        # Create learning sequence
        learning_sequence = self._create_learning_sequence(levels)

        # Generate explanation
        explanation = self._generate_explanation(levels, target_concept)

        decomposed = DecomposedProblem(
            original_problem=problem,
            original_complexity=original_complexity,
            levels=levels,
            learning_sequence=learning_sequence,
            explanation=explanation
        )

        # Track
        self.decomposition_history.append({
            "problem": problem,
            "complexity": original_complexity,
            "levels_generated": len(levels)
        })

        return decomposed

    def generate_scaffolded_practice(
        self,
        skill_id: str,
        start_level: int = 1,
        end_level: int = 5,
        problems_per_level: int = 3
    ) -> ScaffoldedPractice:
        """
        Generate scaffolded practice sequence from simple to complex.

        Args:
            skill_id: Skill to practice
            start_level: Starting complexity level (1-5)
            end_level: Ending complexity level (1-5)
            problems_per_level: Number of problems at each level

        Returns:
            ScaffoldedPractice with progressive problems
        """
        problems = []
        difficulty_progression = []
        scaffolding_notes = []

        # Generate problems for each level
        for level in range(start_level, end_level + 1):
            for i in range(problems_per_level):
                problem = self._generate_problem_at_level(skill_id, level, seed=i)
                problems.append(problem)
                difficulty_progression.append(level)

                # Add scaffolding notes
                if i == 0:  # First problem at new level
                    note = self._get_scaffolding_note(level, skill_id)
                    scaffolding_notes.append(note)
                else:
                    scaffolding_notes.append("")

        return ScaffoldedPractice(
            problems=problems,
            difficulty_progression=difficulty_progression,
            scaffolding_notes=scaffolding_notes
        )

    def _analyze_complexity(self, problem: str, skill_id: str) -> int:
        """
        Analyze problem complexity (1-5).

        Complexity factors:
        - Coefficient (a ≠ 1: +1)
        - Horizontal shift (h ≠ 0: +1)
        - Vertical shift (k ≠ 0: +1)
        - Negative values (+1)
        - Large numbers (>10: +1)
        """
        complexity = 1  # Base complexity

        # Extract equation from problem
        equation_match = re.search(r'y = [^.?]*', problem)
        if not equation_match:
            return 3  # Default to medium

        equation = equation_match.group(0)

        # Check for coefficient
        if re.search(r'[-+]?\d*\.\d+|\d+(?!/\d)', equation):
            # Has explicit coefficient
            if not equation.startswith("y = (x") and not equation.startswith("y = x"):
                complexity += 1

        # Check for horizontal shift
        if re.search(r'\(x\s*[-+]\s*\d+\)', equation):
            complexity += 1

        # Check for vertical shift
        if re.search(r'\)\s*\^2\s*[-+]\s*\d+', equation):
            complexity += 1

        # Check for negative values
        if '-' in equation:
            complexity += 1

        # Check for large numbers
        numbers = re.findall(r'\d+', equation)
        if any(int(n) > 10 for n in numbers):
            complexity += 1

        return min(5, complexity)  # Cap at 5

    def _generate_progressive_levels(
        self,
        problem: str,
        skill_id: str,
        target_concept: str
    ) -> List[ComplexityLevel]:
        """Generate progressive complexity levels."""
        levels = []

        if "vertex" in skill_id:
            # Level 1: Simplest possible (y = x²)
            levels.append(ComplexityLevel(
                level=1,
                description="Simplest form: No shifts, a = 1",
                features={
                    "coefficient": 1,
                    "h": 0,
                    "k": 0,
                    "equation": "y = x²"
                },
                example="Find the vertex of y = x²"
            ))

            # Level 2: Horizontal shift only
            levels.append(ComplexityLevel(
                level=2,
                description="Add horizontal shift (h)",
                features={
                    "coefficient": 1,
                    "h": 3,
                    "k": 0,
                    "equation": "y = (x - 3)²"
                },
                example="Find the vertex of y = (x - 3)²"
            ))

            # Level 3: Both shifts
            levels.append(ComplexityLevel(
                level=3,
                description="Add vertical shift (k)",
                features={
                    "coefficient": 1,
                    "h": 3,
                    "k": 2,
                    "equation": "y = (x - 3)² + 2"
                },
                example="Find the vertex of y = (x - 3)² + 2"
            ))

            # Level 4: Add negative values
            levels.append(ComplexityLevel(
                level=4,
                description="Include negative values",
                features={
                    "coefficient": 1,
                    "h": -4,
                    "k": -5,
                    "equation": "y = (x + 4)² - 5"
                },
                example="Find the vertex of y = (x + 4)² - 5"
            ))

            # Level 5: Add coefficient
            levels.append(ComplexityLevel(
                level=5,
                description="Add coefficient (a ≠ 1)",
                features={
                    "coefficient": -2,
                    "h": -4,
                    "k": 3,
                    "equation": "y = -2(x + 4)² + 3"
                },
                example="Find the vertex of y = -2(x + 4)² + 3"
            ))

        elif "factor" in skill_id:
            # Progressive complexity for factoring
            levels.append(ComplexityLevel(
                level=1,
                description="Simple: (x + a)(x + b) where a, b > 0",
                features={"a": 2, "b": 3},
                example="Factor: x² + 5x + 6"
            ))

            levels.append(ComplexityLevel(
                level=2,
                description="One negative: (x + a)(x - b)",
                features={"a": 2, "b": -3},
                example="Factor: x² - x - 6"
            ))

            levels.append(ComplexityLevel(
                level=3,
                description="Both negative: (x - a)(x - b)",
                features={"a": -2, "b": -3},
                example="Factor: x² - 5x + 6"
            ))

        return levels

    def _create_learning_sequence(self, levels: List[ComplexityLevel]) -> List[str]:
        """Create step-by-step learning sequence."""
        sequence = []

        sequence.append(f"📚 We'll learn this in {len(levels)} progressive steps:")
        sequence.append("")

        for i, level in enumerate(levels, 1):
            sequence.append(f"**Level {level.level}: {level.description}**")
            sequence.append(f"   Example: {level.example}")

            # Add transition explanation
            if i < len(levels):
                next_level = levels[i]
                transition = self._explain_transition(level, next_level)
                sequence.append(f"   → {transition}")

            sequence.append("")

        return sequence

    def _explain_transition(
        self,
        current: ComplexityLevel,
        next_level: ComplexityLevel
    ) -> str:
        """Explain what changes between levels."""
        # Identify what's being added
        if "horizontal shift" in next_level.description.lower():
            return "Next, we'll add a horizontal shift to see how (x - h) affects the vertex"

        if "vertical shift" in next_level.description.lower():
            return "Next, we'll add a vertical shift (+k) to move the parabola up or down"

        if "negative" in next_level.description.lower():
            return "Next, we'll introduce negative values (watch those signs!)"

        if "coefficient" in next_level.description.lower():
            return "Finally, we'll add a coefficient (a) which affects the parabola's shape"

        return "Next, we'll increase the complexity"

    def _generate_explanation(
        self,
        levels: List[ComplexityLevel],
        target_concept: str
    ) -> str:
        """Generate overall explanation of the decomposition."""
        parts = []

        parts.append(f"🎯 Learning {target_concept} step-by-step:\n")

        parts.append(
            "Instead of jumping straight to complex problems, we'll build your "
            "understanding gradually. Each level adds ONE new concept, so you "
            "master it before moving on."
        )

        parts.append(f"\n**Why this works:**")
        parts.append("✓ Reduces cognitive overload")
        parts.append("✓ Builds confidence at each level")
        parts.append("✓ Shows how complexity builds logically")
        parts.append("✓ Prevents confusion from too many concepts at once")

        parts.append(f"\n**Your learning path:**")
        for level in levels:
            parts.append(f"{level.level}. {level.description}")

        parts.append(
            "\n💡 Master each level before moving on. "
            "This way, complex problems feel manageable!"
        )

        return "\n".join(parts)

    def _generate_problem_at_level(
        self,
        skill_id: str,
        level: int,
        seed: int
    ) -> Dict[str, Any]:
        """Generate a problem at specific complexity level."""
        if "vertex" in skill_id:
            return self._generate_vertex_problem_at_level(level, seed)
        else:
            return self._generate_generic_problem(skill_id, level, seed)

    def _generate_vertex_problem_at_level(
        self,
        level: int,
        seed: int
    ) -> Dict[str, Any]:
        """Generate vertex problem at specific level."""
        # Use seed to vary problems within level
        h_values = [0, 2, 3, 4, 5]
        k_values = [0, 1, 2, 3, 4]
        a_values = [1, 2, -1, -2, 0.5]

        h_idx = seed % len(h_values)
        k_idx = (seed + 1) % len(k_values)
        a_idx = (seed + 2) % len(a_values)

        if level == 1:
            # y = x²
            equation = "y = x²"
            answer = "(0, 0)"

        elif level == 2:
            # y = (x - h)²
            h = h_values[h_idx] if h_values[h_idx] != 0 else 2
            equation = f"y = (x - {h})²"
            answer = f"({h}, 0)"

        elif level == 3:
            # y = (x - h)² + k
            h = h_values[h_idx] if h_values[h_idx] != 0 else 2
            k = k_values[k_idx] if k_values[k_idx] != 0 else 1
            equation = f"y = (x - {h})² + {k}"
            answer = f"({h}, {k})"

        elif level == 4:
            # y = (x + h)² - k (negatives)
            h = -(h_values[h_idx] if h_values[h_idx] != 0 else 3)
            k = -(k_values[k_idx] if k_values[k_idx] != 0 else 2)
            equation = f"y = (x - ({h}))² + ({k})"
            answer = f"({h}, {k})"

        else:  # level 5
            # y = a(x - h)² + k
            a = a_values[a_idx] if a_values[a_idx] != 1 else 2
            h = h_values[h_idx] if h_values[h_idx] != 0 else 3
            k = k_values[k_idx] if k_values[k_idx] != 0 else 2
            equation = f"y = {a}(x - {h})² + {k}"
            answer = f"({h}, {k})"

        return {
            "stem": f"Find the vertex of {equation}",
            "equation": equation,
            "answer": answer,
            "level": level,
            "skill_id": "quad.graph.vertex"
        }

    def _generate_generic_problem(
        self,
        skill_id: str,
        level: int,
        seed: int
    ) -> Dict[str, Any]:
        """Generate generic problem at level."""
        return {
            "stem": f"Problem for {skill_id} at level {level} (seed: {seed})",
            "level": level,
            "skill_id": skill_id
        }

    def _get_scaffolding_note(self, level: int, skill_id: str) -> str:
        """Get scaffolding note for transitioning to new level."""
        if "vertex" in skill_id:
            notes = {
                1: "🎯 Starting simple: Just y = x². The vertex is at the origin (0, 0).",
                2: "📈 Level up! Now we add horizontal shifts. Remember: (x - h) means move RIGHT by h.",
                3: "📊 Adding vertical shifts! The +k at the end moves the vertex UP by k.",
                4: "⚠️ Watch the signs! (x + 4) means h = -4 (opposite sign). -5 means k = -5.",
                5: "🎓 Final level! The coefficient 'a' changes the width, but NOT the vertex location."
            }
            return notes.get(level, "")

        return f"Level {level}: Building complexity..."

    def get_decomposition_stats(self) -> Dict[str, Any]:
        """Get statistics about decompositions performed."""
        if not self.decomposition_history:
            return {
                "total_decompositions": 0,
                "avg_complexity": 0,
                "avg_levels_generated": 0
            }

        total = len(self.decomposition_history)
        avg_complexity = sum(d["complexity"] for d in self.decomposition_history) / total
        avg_levels = sum(d["levels_generated"] for d in self.decomposition_history) / total

        return {
            "total_decompositions": total,
            "avg_complexity": avg_complexity,
            "avg_levels_generated": avg_levels
        }
