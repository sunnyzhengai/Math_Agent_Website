"""
Parameter generation system for infinite question variations.

This module enables generating unlimited unique questions from a single template
by parameterizing values and generating different instances.

Architecture:
- ParameterSpec: Defines what parameters a template needs
- ParameterGenerator: Generates valid parameter sets
- DistractorGenerator: Creates plausible wrong answers
"""

import random
from typing import Dict, List, Any, Optional, Callable, Set, Tuple
from dataclasses import dataclass


@dataclass
class ParameterConstraint:
    """Constraint on a single parameter."""
    param_name: str
    param_type: str  # 'int', 'float', 'choice'
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    choices: Optional[List[Any]] = None
    exclude: Optional[Set[Any]] = None


@dataclass
class ParameterSpec:
    """
    Specification for a parameterized template.

    Defines:
    - What parameters are needed
    - Constraints on each parameter
    - How to compute the solution
    - How to generate distractors
    """
    template_id: str
    difficulty: str
    stem_template: str  # Template string with {param} placeholders
    constraints: List[ParameterConstraint]
    solver: Callable[[Dict[str, Any]], Any]  # params -> solution
    distractor_generator: Callable[[Dict[str, Any], Any, str], List[Any]]  # params, solution, difficulty -> distractors


class ParameterGenerator:
    """Generates valid parameter sets for templates."""

    def __init__(self, seed: Optional[int] = None):
        self.rng = random.Random(seed)

    def generate(self, spec: ParameterSpec) -> Dict[str, Any]:
        """
        Generate a valid parameter set satisfying all constraints.

        Args:
            spec: Parameter specification

        Returns:
            Dict mapping parameter names to values
        """
        params = {}

        for constraint in spec.constraints:
            value = self._generate_value(constraint)
            params[constraint.param_name] = value

        return params

    def _generate_value(self, constraint: ParameterConstraint) -> Any:
        """Generate a single parameter value."""
        if constraint.param_type == 'int':
            value = self.rng.randint(
                int(constraint.min_value or 0),
                int(constraint.max_value or 100)
            )
            # Handle exclusions
            if constraint.exclude and value in constraint.exclude:
                # Retry once
                value = self.rng.randint(
                    int(constraint.min_value or 0),
                    int(constraint.max_value or 100)
                )
            return value

        elif constraint.param_type == 'float':
            value = self.rng.uniform(
                constraint.min_value or 0.0,
                constraint.max_value or 1.0
            )
            return round(value, 2)

        elif constraint.param_type == 'choice':
            if not constraint.choices:
                raise ValueError(f"Choice constraint needs choices: {constraint.param_name}")
            return self.rng.choice(constraint.choices)

        else:
            raise ValueError(f"Unknown parameter type: {constraint.param_type}")


class DistractorGenerator:
    """Generates plausible wrong answers (distractors)."""

    @staticmethod
    def sign_error(correct_value: Any) -> Any:
        """Common error: flip sign."""
        if isinstance(correct_value, (int, float)):
            return -correct_value
        elif isinstance(correct_value, str) and correct_value.startswith('-'):
            return correct_value[1:]
        elif isinstance(correct_value, str):
            return '-' + correct_value
        return correct_value

    @staticmethod
    def swap_values(correct_value: str, separator: str = " and ") -> str:
        """Common error: swap order of values."""
        if separator in correct_value:
            parts = correct_value.split(separator)
            return separator.join(reversed(parts))
        return correct_value

    @staticmethod
    def off_by_one(correct_value: Any, direction: int = 1) -> Any:
        """Common error: off by one."""
        if isinstance(correct_value, int):
            return correct_value + direction
        return correct_value

    @staticmethod
    def formula_error(params: Dict[str, Any], operation: str = 'add') -> Any:
        """Common error: wrong formula application."""
        # This is template-specific, just a placeholder
        return None


# ====================================================================================
# Parameterized Template Specifications
# ====================================================================================

def solve_by_factoring_easy_solver(params: Dict[str, Any]) -> str:
    """
    Solve x^2 + bx + c = 0 where roots are r1, r2.

    Given roots r1, r2:
    - (x - r1)(x - r2) = 0
    - x^2 - (r1+r2)x + r1*r2 = 0
    - So b = -(r1+r2), c = r1*r2

    Solution format: "x = r1 and x = r2"
    """
    r1 = params['r1']
    r2 = params['r2']

    # Format solution (smaller root first)
    roots = sorted([r1, r2])
    return f"x = {roots[0]} and x = {roots[1]}"


def solve_by_factoring_easy_distractors(params: Dict[str, Any], solution: str, difficulty: str) -> List[str]:
    """
    Generate difficulty-aware distractors for solve by factoring.

    Easy: Sign errors (too obvious, make more subtle)
    Medium: Add off-by-one errors and computation mistakes
    Hard: Add factoring errors and more sophisticated mistakes
    """
    r1 = params['r1']
    r2 = params['r2']

    distractors = []

    if difficulty == "easy":
        # Sign errors - but make them more plausible
        distractors.append(f"x = {-r1} and x = {-r2}")
        distractors.append(f"x = {-r1} and x = {r2}")
        distractors.append(f"x = {r1} and x = {-r2}")

    elif difficulty == "medium":
        # Mix sign errors with arithmetic errors
        distractors.append(f"x = {-r1} and x = {-r2}")  # All signs wrong
        distractors.append(f"x = {r1 + 1} and x = {r2}")  # Off-by-one
        distractors.append(f"x = {r1} and x = {r2 + 1}")  # Off-by-one other root

    elif difficulty == "hard":
        # More sophisticated errors
        distractors.append(f"x = {-r1} and x = {-r2}")  # Sign error
        # Swap with sum/product (confusing with coefficients)
        b = -(r1 + r2)
        c = r1 * r2
        distractors.append(f"x = {b} and x = {c}")  # Confused with coefficients
        distractors.append(f"x = {r1 + 2} and x = {r2 - 2}")  # Arithmetic error

    else:  # applied - static templates handle this
        distractors.append(f"x = {-r1} and x = {-r2}")
        distractors.append(f"x = {-r1} and x = {r2}")
        distractors.append(f"x = {r1} and x = {-r2}")

    return distractors


# Example parameterized template
SOLVE_BY_FACTORING_EASY = ParameterSpec(
    template_id="quad.solve.by_factoring",
    difficulty="easy",
    stem_template="Solve by factoring: x^2 {sign_b}{b}x {sign_c}{c} = 0.",
    constraints=[
        ParameterConstraint(param_name='r1', param_type='int', min_value=-15, max_value=15, exclude={0}),
        ParameterConstraint(param_name='r2', param_type='int', min_value=-15, max_value=15, exclude={0}),
    ],
    solver=solve_by_factoring_easy_solver,
    distractor_generator=solve_by_factoring_easy_distractors
)

SOLVE_BY_FACTORING_MEDIUM = ParameterSpec(
    template_id="quad.solve.by_factoring",
    difficulty="medium",
    stem_template="Solve by factoring: x^2 {sign_b}{b}x {sign_c}{c} = 0.",
    constraints=[
        ParameterConstraint(param_name='r1', param_type='int', min_value=-30, max_value=30, exclude={0}),
        ParameterConstraint(param_name='r2', param_type='int', min_value=-30, max_value=30, exclude={0}),
    ],
    solver=solve_by_factoring_easy_solver,  # Same solver
    distractor_generator=solve_by_factoring_easy_distractors  # Same distractors
)

SOLVE_BY_FACTORING_HARD = ParameterSpec(
    template_id="quad.solve.by_factoring",
    difficulty="hard",
    stem_template="Solve by factoring: x^2 {sign_b}{b}x {sign_c}{c} = 0.",
    constraints=[
        ParameterConstraint(param_name='r1', param_type='int', min_value=-45, max_value=45, exclude={0}),
        ParameterConstraint(param_name='r2', param_type='int', min_value=-45, max_value=45, exclude={0}),
    ],
    solver=solve_by_factoring_easy_solver,  # Same solver
    distractor_generator=solve_by_factoring_easy_distractors  # Same distractors
)


# ====================================================================================
# quad.roots.factored - Find roots from factored form
# ====================================================================================

def roots_factored_easy_solver(params: Dict[str, Any]) -> str:
    """Extract roots from (x - r1)(x - r2) = 0."""
    r1 = params['r1']
    r2 = params['r2']
    roots = sorted([r1, r2])
    return f"x = {roots[0]} and x = {roots[1]}"


def roots_factored_easy_distractors(params: Dict[str, Any], solution: str, difficulty: str) -> List[str]:
    """Generate difficulty-aware distractors for roots from factored form."""
    r1 = params['r1']
    r2 = params['r2']

    distractors = []

    if difficulty == "easy":
        distractors.append(f"x = {-r1} and x = {-r2}")
        distractors.append(f"x = {-r1} and x = {r2}")
        distractors.append(f"x = {r1} and x = {-r2}")

    elif difficulty == "medium":
        distractors.append(f"x = {-r1} and x = {-r2}")  # Sign error
        distractors.append(f"x = {r1 + 1} and x = {r2}")  # Off-by-one
        distractors.append(f"x = {r1} and x = {r2 - 1}")  # Off-by-one

    elif difficulty == "hard":
        distractors.append(f"x = {-r1} and x = {-r2}")  # Sign error
        b = -(r1 + r2)
        c = r1 * r2
        distractors.append(f"x = {b} and x = {c}")  # Confused coefficients
        distractors.append(f"x = {r1 * 2} and x = {r2}")  # Multiplication error

    else:  # applied
        distractors.append(f"x = {-r1} and x = {-r2}")
        distractors.append(f"x = {-r1} and x = {r2}")
        distractors.append(f"x = {r1} and x = {-r2}")

    return distractors


ROOTS_FACTORED_EASY = ParameterSpec(
    template_id="quad.roots.factored",
    difficulty="easy",
    stem_template="Find the roots of y = (x {sign_r1}{r1})(x {sign_r2}{r2}).",
    constraints=[
        ParameterConstraint(param_name='r1', param_type='int', min_value=-15, max_value=15, exclude={0}),
        ParameterConstraint(param_name='r2', param_type='int', min_value=-15, max_value=15, exclude={0}),
    ],
    solver=roots_factored_easy_solver,
    distractor_generator=roots_factored_easy_distractors
)


# ====================================================================================
# quad.solve.by_formula - Solve using quadratic formula
# ====================================================================================

def solve_by_formula_easy_solver(params: Dict[str, Any]) -> str:
    """Solve using quadratic formula (same roots as factoring)."""
    r1 = params['r1']
    r2 = params['r2']
    roots = sorted([r1, r2])
    return f"x = {roots[0]} and x = {roots[1]}"


def solve_by_formula_easy_distractors(params: Dict[str, Any], solution: str, difficulty: str) -> List[str]:
    """Generate difficulty-aware distractors for quadratic formula."""
    r1 = params['r1']
    r2 = params['r2']

    distractors = []

    if difficulty == "easy":
        distractors.append(f"x = {-r1} and x = {-r2}")
        distractors.append(f"x = {-r1} and x = {r2}")
        distractors.append(f"x = {r1} and x = {-r2}")

    elif difficulty == "medium":
        distractors.append(f"x = {-r1} and x = {-r2}")  # Sign error
        distractors.append(f"x = {r1 + 1} and x = {r2 - 1}")  # Arithmetic error
        distractors.append(f"x = {r1} and x = {r2 + 2}")  # Off-by-two

    elif difficulty == "hard":
        distractors.append(f"x = {-r1} and x = {-r2}")  # Sign error
        # Square root errors (discriminant mistakes)
        distractors.append(f"x = {r1 + 3} and x = {r2 - 3}")
        distractors.append(f"x = {abs(r1)} and x = {abs(r2)}")  # Absolute value error

    else:  # applied
        distractors.append(f"x = {-r1} and x = {-r2}")
        distractors.append(f"x = {-r1} and x = {r2}")
        distractors.append(f"x = {r1} and x = {-r2}")

    return distractors


SOLVE_BY_FORMULA_EASY = ParameterSpec(
    template_id="quad.solve.by_formula",
    difficulty="easy",
    stem_template="Solve using the quadratic formula: x^2 {sign_b}{b}x {sign_c}{c} = 0.",
    constraints=[
        ParameterConstraint(param_name='r1', param_type='int', min_value=-15, max_value=15, exclude={0}),
        ParameterConstraint(param_name='r2', param_type='int', min_value=-15, max_value=15, exclude={0}),
    ],
    solver=solve_by_formula_easy_solver,
    distractor_generator=solve_by_formula_easy_distractors
)


# ====================================================================================
# quad.intercepts - Find x-intercepts (same as finding roots)
# ====================================================================================

def intercepts_easy_solver(params: Dict[str, Any]) -> str:
    """Find x-intercepts (where y=0, i.e., the roots)."""
    r1 = params['r1']
    r2 = params['r2']
    roots = sorted([r1, r2])
    return f"x = {roots[0]} and x = {roots[1]}"


def intercepts_easy_distractors(params: Dict[str, Any], solution: str, difficulty: str) -> List[str]:
    """Generate difficulty-aware distractors for intercepts."""
    r1 = params['r1']
    r2 = params['r2']

    distractors = []

    if difficulty == "easy":
        distractors.append(f"x = {-r1} and x = {-r2}")
        distractors.append(f"x = {-r1} and x = {r2}")
        distractors.append(f"x = {r1} and x = {-r2}")

    elif difficulty == "medium":
        distractors.append(f"x = {-r1} and x = {-r2}")
        distractors.append(f"x = {r1 + 1} and x = {r2}")
        distractors.append(f"x = {r1} and x = {r2 + 1}")

    elif difficulty == "hard":
        distractors.append(f"x = {-r1} and x = {-r2}")
        b = -(r1 + r2)
        c = r1 * r2
        distractors.append(f"x = {b} and x = {c}")
        distractors.append(f"x = {r1 + 3} and x = {r2 - 3}")

    else:  # applied
        distractors.append(f"x = {-r1} and x = {-r2}")
        distractors.append(f"x = {-r1} and x = {r2}")
        distractors.append(f"x = {r1} and x = {-r2}")

    return distractors


INTERCEPTS_EASY = ParameterSpec(
    template_id="quad.intercepts",
    difficulty="easy",
    stem_template="Find the x-intercepts of y = (x {sign_r1}{r1})(x {sign_r2}{r2}).",
    constraints=[
        ParameterConstraint(param_name='r1', param_type='int', min_value=-15, max_value=15, exclude={0}),
        ParameterConstraint(param_name='r2', param_type='int', min_value=-15, max_value=15, exclude={0}),
    ],
    solver=intercepts_easy_solver,
    distractor_generator=intercepts_easy_distractors
)


# ====================================================================================
# quad.graph.vertex - Find vertex from vertex form y = (x - h)^2 + k
# ====================================================================================

def graph_vertex_easy_solver(params: Dict[str, Any]) -> str:
    """Find vertex from vertex form."""
    h = params['h']
    k = params['k']
    return f"({h}, {k})"


def graph_vertex_easy_distractors(params: Dict[str, Any], solution: str, difficulty: str) -> List[str]:
    """Generate difficulty-aware distractors for vertex from graph."""
    h = params['h']
    k = params['k']

    distractors = []

    if difficulty == "easy":
        distractors.append(f"({-h}, {k})")
        distractors.append(f"({h}, {-k})")
        distractors.append(f"({-h}, {-k})")

    elif difficulty == "medium":
        distractors.append(f"({-h}, {k})")  # Sign error on h
        distractors.append(f"({h}, {-k})")  # Sign error on k
        distractors.append(f"({h + 1}, {k})")  # Off-by-one on h

    elif difficulty == "hard":
        distractors.append(f"({-h}, {-k})")  # Both signs wrong
        distractors.append(f"({h + 2}, {k - 2})")  # Arithmetic errors
        distractors.append(f"({k}, {h})")  # Swapped coordinates

    else:  # applied
        distractors.append(f"({-h}, {k})")
        distractors.append(f"({h}, {-k})")
        distractors.append(f"({-h}, {-k})")

    return distractors


GRAPH_VERTEX_EASY = ParameterSpec(
    template_id="quad.graph.vertex",
    difficulty="easy",
    stem_template="What is the vertex of y = (x {sign_h}{h})^2 {sign_k}{k}?",
    constraints=[
        ParameterConstraint(param_name='h', param_type='int', min_value=-10, max_value=10, exclude={0}),
        ParameterConstraint(param_name='k', param_type='int', min_value=-10, max_value=10, exclude={0}),
    ],
    solver=graph_vertex_easy_solver,
    distractor_generator=graph_vertex_easy_distractors
)


# ====================================================================================
# quad.axis.symmetry - Find axis of symmetry
# ====================================================================================

def axis_symmetry_easy_solver(params: Dict[str, Any]) -> str:
    """Find axis of symmetry x = h."""
    h = params['h']
    return f"x = {h}"


def axis_symmetry_easy_distractors(params: Dict[str, Any], solution: str, difficulty: str) -> List[str]:
    """Generate difficulty-aware distractors for axis of symmetry."""
    h = params['h']
    k = params['k']

    distractors = []

    if difficulty == "easy":
        distractors.append(f"x = {-h}")
        distractors.append(f"x = {h + 1}")
        distractors.append(f"x = {h - 1}")

    elif difficulty == "medium":
        distractors.append(f"x = {-h}")  # Sign error
        distractors.append(f"x = {k}")  # Confused with k
        distractors.append(f"x = {h + 2}")  # Off-by-two

    elif difficulty == "hard":
        distractors.append(f"x = {-h}")  # Sign error
        distractors.append(f"x = {k}")  # Confused with k
        distractors.append(f"x = {h * 2}")  # Multiplication error

    else:  # applied
        distractors.append(f"x = {-h}")
        distractors.append(f"x = {h + 1}")
        distractors.append(f"x = {h - 1}")

    return distractors


AXIS_SYMMETRY_EASY = ParameterSpec(
    template_id="quad.axis.symmetry",
    difficulty="easy",
    stem_template="Find the axis of symmetry for y = (x {sign_h}{h})^2 {sign_k}{k}.",
    constraints=[
        ParameterConstraint(param_name='h', param_type='int', min_value=-10, max_value=10, exclude={0}),
        ParameterConstraint(param_name='k', param_type='int', min_value=-10, max_value=10, exclude={0}),
    ],
    solver=axis_symmetry_easy_solver,
    distractor_generator=axis_symmetry_easy_distractors
)


# ====================================================================================
# quad.standard.vertex - Find vertex from standard form y = ax^2 + bx + c
# ====================================================================================

def standard_vertex_easy_solver(params: Dict[str, Any]) -> str:
    """
    Find vertex from standard form.

    Vertex: h = -b/(2a), k = c - b^2/(4a)
    """
    a = params['a']
    b = params['b']
    c = params['c']

    h = -b // (2 * a)  # Use integer division for clean answers
    k = c - (b * b) // (4 * a)

    return f"({h}, {k})"


def standard_vertex_easy_distractors(params: Dict[str, Any], solution: str, difficulty: str) -> List[str]:
    """Generate difficulty-aware distractors for vertex from standard form."""
    a = params['a']
    b = params['b']
    c = params['c']

    h = -b // (2 * a)
    k = c - (b * b) // (4 * a)

    distractors = []

    if difficulty == "easy":
        distractors.append(f"({h}, {h})")  # Used h for both
        distractors.append(f"({-h}, {k})")  # Sign error on h
        distractors.append(f"({h}, {c})")  # Used c as k

    elif difficulty == "medium":
        distractors.append(f"({h}, {h})")  # Used h for both
        distractors.append(f"({-h}, {k})")  # Sign error on h
        distractors.append(f"({h + 1}, {k})")  # Off-by-one on h

    elif difficulty == "hard":
        distractors.append(f"({-h}, {k})")  # Sign error on h
        distractors.append(f"({h}, {c})")  # Used c as k
        distractors.append(f"({h}, {k + a})")  # Added a to k

    else:  # applied
        distractors.append(f"({h}, {h})")
        distractors.append(f"({-h}, {k})")
        distractors.append(f"({h}, {c})")

    return distractors


STANDARD_VERTEX_EASY = ParameterSpec(
    template_id="quad.standard.vertex",
    difficulty="easy",
    stem_template="Find the vertex of y = {a}x^2 {sign_b}{b}x {sign_c}{c}.",
    constraints=[
        ParameterConstraint(param_name='a', param_type='choice', choices=[1, -1]),  # Keep simple for easy
        ParameterConstraint(param_name='b', param_type='int', min_value=-10, max_value=10, exclude={0}),
        ParameterConstraint(param_name='c', param_type='int', min_value=-10, max_value=10),
    ],
    solver=standard_vertex_easy_solver,
    distractor_generator=standard_vertex_easy_distractors
)


# ====================================================================================
# quad.discriminant.analysis - Calculate discriminant b^2 - 4ac
# ====================================================================================

def discriminant_easy_solver(params: Dict[str, Any]) -> str:
    """Calculate discriminant b^2 - 4ac."""
    a = params['a']
    b = params['b']
    c = params['c']

    discriminant = b * b - 4 * a * c
    return str(discriminant)


def discriminant_easy_distractors(params: Dict[str, Any], solution: str, difficulty: str) -> List[str]:
    """Generate difficulty-aware distractors for discriminant."""
    a = params['a']
    b = params['b']
    c = params['c']

    discriminant = b * b - 4 * a * c

    distractors = []

    if difficulty == "easy":
        distractors.append(str(b * b - a * c))  # Forgot the 4
        distractors.append(str(b * b))  # Just b^2
        distractors.append(str(b * b + 4 * a * c))  # Sign error

    elif difficulty == "medium":
        distractors.append(str(b * b - a * c))  # Forgot the 4
        distractors.append(str(b * b + 4 * a * c))  # Sign error
        distractors.append(str(b - 4 * a * c))  # Forgot to square b

    elif difficulty == "hard":
        distractors.append(str(b * b + 4 * a * c))  # Sign error
        distractors.append(str(b - 4 * a * c))  # Forgot to square b
        distractors.append(str(2 * b - 4 * a * c))  # 2b instead of b^2

    else:  # applied
        distractors.append(str(b * b - a * c))
        distractors.append(str(b * b))
        distractors.append(str(b * b + 4 * a * c))

    return distractors


DISCRIMINANT_EASY = ParameterSpec(
    template_id="quad.discriminant.analysis",
    difficulty="easy",
    stem_template="For {a_fmt}x^2 {sign_b}{b}x {sign_c}{c} = 0, what is the discriminant?",
    constraints=[
        ParameterConstraint(param_name='a', param_type='choice', choices=[1, -1]),
        ParameterConstraint(param_name='b', param_type='int', min_value=-10, max_value=10, exclude={0}),
        ParameterConstraint(param_name='c', param_type='int', min_value=-10, max_value=10, exclude={0}),
    ],
    solver=discriminant_easy_solver,
    distractor_generator=discriminant_easy_distractors
)


# ====================================================================================
# quad.complete.square - Complete the square: x^2 + bx → (x + b/2)^2 - (b/2)^2
# ====================================================================================

def complete_square_easy_solver(params: Dict[str, Any]) -> str:
    """
    Complete the square for x^2 + bx.

    Result: (x + b/2)^2 - (b/2)^2
    """
    b = params['b']

    # Use only even b values for clean integer division
    half_b = b // 2
    square_term = half_b * half_b

    # Format: (x + half_b)^2 - square_term
    sign_half_b = '+ ' if half_b >= 0 else '- '
    abs_half_b = abs(half_b)

    return f"(x {sign_half_b}{abs_half_b})^2 - {square_term}"


def complete_square_easy_distractors(params: Dict[str, Any], solution: str, difficulty: str) -> List[str]:
    """Generate difficulty-aware distractors for completing the square."""
    b = params['b']
    half_b = b // 2
    square_term = half_b * half_b

    sign_half_b = '+ ' if half_b >= 0 else '- '
    abs_half_b = abs(half_b)
    sign_b = '+ ' if b >= 0 else '- '
    abs_b = abs(b)

    distractors = []

    if difficulty == "easy":
        distractors.append(f"(x {sign_half_b}{abs_half_b})^2")  # Forgot to subtract
        distractors.append(f"(x {sign_b}{abs_b})^2 - {b * b}")  # Used b instead of b/2
        distractors.append(f"(x {sign_half_b}{abs_half_b})^2 + {square_term}")  # Sign error

    elif difficulty == "medium":
        distractors.append(f"(x {sign_half_b}{abs_half_b})^2")  # Forgot to subtract
        distractors.append(f"(x {sign_b}{abs_b})^2 - {b * b}")  # Used b instead of b/2
        distractors.append(f"(x {sign_half_b}{abs_half_b})^2 - {square_term * 2}")  # Doubled the constant

    elif difficulty == "hard":
        distractors.append(f"(x {sign_b}{abs_b})^2 - {b * b}")  # Used b instead of b/2
        distractors.append(f"(x {sign_half_b}{abs_half_b})^2 + {square_term}")  # Sign error
        distractors.append(f"(x {sign_half_b}{abs_half_b})^2 - {half_b}")  # Used half_b instead of square

    else:  # applied
        distractors.append(f"(x {sign_half_b}{abs_half_b})^2")
        distractors.append(f"(x {sign_b}{abs_b})^2 - {b * b}")
        distractors.append(f"(x {sign_half_b}{abs_half_b})^2 + {square_term}")

    return distractors


COMPLETE_SQUARE_EASY = ParameterSpec(
    template_id="quad.complete.square",
    difficulty="easy",
    stem_template="Complete the square for x^2 {sign_b}{b}x.",
    constraints=[
        # Use even b values only for clean division
        ParameterConstraint(param_name='b', param_type='choice',
                          choices=[-10, -8, -6, -4, -2, 2, 4, 6, 8, 10]),
    ],
    solver=complete_square_easy_solver,
    distractor_generator=complete_square_easy_distractors
)


# Medium and Hard difficulty specs

ROOTS_FACTORED_MEDIUM = ParameterSpec(
    template_id="quad.roots.factored",
    difficulty="medium",
    stem_template="Find the roots of y = (x {sign_r1}{r1})(x {sign_r2}{r2}).",
    constraints=[
        ParameterConstraint(param_name='r1', param_type='int', min_value=-30, max_value=30, exclude={0}),
        ParameterConstraint(param_name='r2', param_type='int', min_value=-30, max_value=30, exclude={0}),
    ],
    solver=roots_factored_easy_solver,
    distractor_generator=roots_factored_easy_distractors
)

ROOTS_FACTORED_HARD = ParameterSpec(
    template_id="quad.roots.factored",
    difficulty="hard",
    stem_template="Find the roots of y = (x {sign_r1}{r1})(x {sign_r2}{r2}).",
    constraints=[
        ParameterConstraint(param_name='r1', param_type='int', min_value=-45, max_value=45, exclude={0}),
        ParameterConstraint(param_name='r2', param_type='int', min_value=-45, max_value=45, exclude={0}),
    ],
    solver=roots_factored_easy_solver,
    distractor_generator=roots_factored_easy_distractors
)

SOLVE_BY_FORMULA_MEDIUM = ParameterSpec(
    template_id="quad.solve.by_formula",
    difficulty="medium",
    stem_template="Solve using the quadratic formula: x^2 {sign_b}{b}x {sign_c}{c} = 0.",
    constraints=[
        ParameterConstraint(param_name='r1', param_type='int', min_value=-30, max_value=30, exclude={0}),
        ParameterConstraint(param_name='r2', param_type='int', min_value=-30, max_value=30, exclude={0}),
    ],
    solver=solve_by_formula_easy_solver,
    distractor_generator=solve_by_formula_easy_distractors
)

SOLVE_BY_FORMULA_HARD = ParameterSpec(
    template_id="quad.solve.by_formula",
    difficulty="hard",
    stem_template="Solve using the quadratic formula: x^2 {sign_b}{b}x {sign_c}{c} = 0.",
    constraints=[
        ParameterConstraint(param_name='r1', param_type='int', min_value=-45, max_value=45, exclude={0}),
        ParameterConstraint(param_name='r2', param_type='int', min_value=-45, max_value=45, exclude={0}),
    ],
    solver=solve_by_formula_easy_solver,
    distractor_generator=solve_by_formula_easy_distractors
)

INTERCEPTS_MEDIUM = ParameterSpec(
    template_id="quad.intercepts",
    difficulty="medium",
    stem_template="Find the x-intercepts of y = (x {sign_r1}{r1})(x {sign_r2}{r2}).",
    constraints=[
        ParameterConstraint(param_name='r1', param_type='int', min_value=-30, max_value=30, exclude={0}),
        ParameterConstraint(param_name='r2', param_type='int', min_value=-30, max_value=30, exclude={0}),
    ],
    solver=intercepts_easy_solver,
    distractor_generator=intercepts_easy_distractors
)

INTERCEPTS_HARD = ParameterSpec(
    template_id="quad.intercepts",
    difficulty="hard",
    stem_template="Find the x-intercepts of y = (x {sign_r1}{r1})(x {sign_r2}{r2}).",
    constraints=[
        ParameterConstraint(param_name='r1', param_type='int', min_value=-45, max_value=45, exclude={0}),
        ParameterConstraint(param_name='r2', param_type='int', min_value=-45, max_value=45, exclude={0}),
    ],
    solver=intercepts_easy_solver,
    distractor_generator=intercepts_easy_distractors
)

GRAPH_VERTEX_MEDIUM = ParameterSpec(
    template_id="quad.graph.vertex",
    difficulty="medium",
    stem_template="What is the vertex of y = (x {sign_h}{h})^2 {sign_k}{k}?",
    constraints=[
        ParameterConstraint(param_name='h', param_type='int', min_value=-20, max_value=20, exclude={0}),
        ParameterConstraint(param_name='k', param_type='int', min_value=-20, max_value=20, exclude={0}),
    ],
    solver=graph_vertex_easy_solver,
    distractor_generator=graph_vertex_easy_distractors
)

GRAPH_VERTEX_HARD = ParameterSpec(
    template_id="quad.graph.vertex",
    difficulty="hard",
    stem_template="What is the vertex of y = (x {sign_h}{h})^2 {sign_k}{k}?",
    constraints=[
        ParameterConstraint(param_name='h', param_type='int', min_value=-30, max_value=30, exclude={0}),
        ParameterConstraint(param_name='k', param_type='int', min_value=-30, max_value=30, exclude={0}),
    ],
    solver=graph_vertex_easy_solver,
    distractor_generator=graph_vertex_easy_distractors
)

AXIS_SYMMETRY_MEDIUM = ParameterSpec(
    template_id="quad.axis.symmetry",
    difficulty="medium",
    stem_template="Find the axis of symmetry for y = (x {sign_h}{h})^2 {sign_k}{k}.",
    constraints=[
        ParameterConstraint(param_name='h', param_type='int', min_value=-20, max_value=20, exclude={0}),
        ParameterConstraint(param_name='k', param_type='int', min_value=-20, max_value=20, exclude={0}),
    ],
    solver=axis_symmetry_easy_solver,
    distractor_generator=axis_symmetry_easy_distractors
)

AXIS_SYMMETRY_HARD = ParameterSpec(
    template_id="quad.axis.symmetry",
    difficulty="hard",
    stem_template="Find the axis of symmetry for y = (x {sign_h}{h})^2 {sign_k}{k}.",
    constraints=[
        ParameterConstraint(param_name='h', param_type='int', min_value=-30, max_value=30, exclude={0}),
        ParameterConstraint(param_name='k', param_type='int', min_value=-30, max_value=30, exclude={0}),
    ],
    solver=axis_symmetry_easy_solver,
    distractor_generator=axis_symmetry_easy_distractors
)

STANDARD_VERTEX_MEDIUM = ParameterSpec(
    template_id="quad.standard.vertex",
    difficulty="medium",
    stem_template="Find the vertex of y = {a}x^2 {sign_b}{b}x {sign_c}{c}.",
    constraints=[
        ParameterConstraint(param_name='a', param_type='choice', choices=[1, -1, 2, -2]),
        ParameterConstraint(param_name='b', param_type='int', min_value=-20, max_value=20, exclude={0}),
        ParameterConstraint(param_name='c', param_type='int', min_value=-20, max_value=20),
    ],
    solver=standard_vertex_easy_solver,
    distractor_generator=standard_vertex_easy_distractors
)

STANDARD_VERTEX_HARD = ParameterSpec(
    template_id="quad.standard.vertex",
    difficulty="hard",
    stem_template="Find the vertex of y = {a}x^2 {sign_b}{b}x {sign_c}{c}.",
    constraints=[
        ParameterConstraint(param_name='a', param_type='choice', choices=[1, -1, 2, -2, 3, -3]),
        ParameterConstraint(param_name='b', param_type='int', min_value=-30, max_value=30, exclude={0}),
        ParameterConstraint(param_name='c', param_type='int', min_value=-30, max_value=30),
    ],
    solver=standard_vertex_easy_solver,
    distractor_generator=standard_vertex_easy_distractors
)

DISCRIMINANT_MEDIUM = ParameterSpec(
    template_id="quad.discriminant.analysis",
    difficulty="medium",
    stem_template="For {a_fmt}x^2 {sign_b}{b}x {sign_c}{c} = 0, what is the discriminant?",
    constraints=[
        ParameterConstraint(param_name='a', param_type='choice', choices=[1, -1, 2, -2]),
        ParameterConstraint(param_name='b', param_type='int', min_value=-20, max_value=20, exclude={0}),
        ParameterConstraint(param_name='c', param_type='int', min_value=-20, max_value=20, exclude={0}),
    ],
    solver=discriminant_easy_solver,
    distractor_generator=discriminant_easy_distractors
)

DISCRIMINANT_HARD = ParameterSpec(
    template_id="quad.discriminant.analysis",
    difficulty="hard",
    stem_template="For {a_fmt}x^2 {sign_b}{b}x {sign_c}{c} = 0, what is the discriminant?",
    constraints=[
        ParameterConstraint(param_name='a', param_type='choice', choices=[1, -1, 2, -2, 3, -3]),
        ParameterConstraint(param_name='b', param_type='int', min_value=-30, max_value=30, exclude={0}),
        ParameterConstraint(param_name='c', param_type='int', min_value=-30, max_value=30, exclude={0}),
    ],
    solver=discriminant_easy_solver,
    distractor_generator=discriminant_easy_distractors
)

COMPLETE_SQUARE_MEDIUM = ParameterSpec(
    template_id="quad.complete.square",
    difficulty="medium",
    stem_template="Complete the square for x^2 {sign_b}{b}x.",
    constraints=[
        ParameterConstraint(param_name='b', param_type='choice', choices=list(range(-20, 22, 2))),
    ],
    solver=complete_square_easy_solver,
    distractor_generator=complete_square_easy_distractors
)

COMPLETE_SQUARE_HARD = ParameterSpec(
    template_id="quad.complete.square",
    difficulty="hard",
    stem_template="Complete the square for x^2 {sign_b}{b}x.",
    constraints=[
        ParameterConstraint(param_name='b', param_type='choice', choices=list(range(-30, 32, 2))),
    ],
    solver=complete_square_easy_solver,
    distractor_generator=complete_square_easy_distractors
)


# Registry of parameterized templates
PARAMETERIZED_TEMPLATES: Dict[str, Dict[str, ParameterSpec]] = {
    "quad.solve.by_factoring": {
        "easy": SOLVE_BY_FACTORING_EASY,
        "medium": SOLVE_BY_FACTORING_MEDIUM,
        "hard": SOLVE_BY_FACTORING_HARD
    },
    "quad.roots.factored": {
        "easy": ROOTS_FACTORED_EASY,
        "medium": ROOTS_FACTORED_MEDIUM,
        "hard": ROOTS_FACTORED_HARD
    },
    "quad.solve.by_formula": {
        "easy": SOLVE_BY_FORMULA_EASY,
        "medium": SOLVE_BY_FORMULA_MEDIUM,
        "hard": SOLVE_BY_FORMULA_HARD
    },
    "quad.intercepts": {
        "easy": INTERCEPTS_EASY,
        "medium": INTERCEPTS_MEDIUM,
        "hard": INTERCEPTS_HARD
    },
    "quad.graph.vertex": {
        "easy": GRAPH_VERTEX_EASY,
        "medium": GRAPH_VERTEX_MEDIUM,
        "hard": GRAPH_VERTEX_HARD
    },
    "quad.axis.symmetry": {
        "easy": AXIS_SYMMETRY_EASY,
        "medium": AXIS_SYMMETRY_MEDIUM,
        "hard": AXIS_SYMMETRY_HARD
    },
    "quad.standard.vertex": {
        "easy": STANDARD_VERTEX_EASY,
        "medium": STANDARD_VERTEX_MEDIUM,
        "hard": STANDARD_VERTEX_HARD
    },
    "quad.discriminant.analysis": {
        "easy": DISCRIMINANT_EASY,
        "medium": DISCRIMINANT_MEDIUM,
        "hard": DISCRIMINANT_HARD
    },
    "quad.complete.square": {
        "easy": COMPLETE_SQUARE_EASY,
        "medium": COMPLETE_SQUARE_MEDIUM,
        "hard": COMPLETE_SQUARE_HARD
    }
}


def generate_parameterized_item(
    skill_id: str,
    difficulty: str,
    seed: Optional[int] = None
) -> Dict[str, Any]:
    """
    Generate a question item using parameterized generation.

    Args:
        skill_id: Skill identifier
        difficulty: Difficulty level
        seed: Random seed for reproducibility

    Returns:
        Dict with generated item (same schema as static templates)
    """
    # Check if parameterized template exists
    if skill_id not in PARAMETERIZED_TEMPLATES:
        raise ValueError(f"No parameterized template for skill: {skill_id}")

    if difficulty not in PARAMETERIZED_TEMPLATES[skill_id]:
        raise ValueError(f"No parameterized template for {skill_id}:{difficulty}")

    spec = PARAMETERIZED_TEMPLATES[skill_id][difficulty]

    # Generate parameters
    generator = ParameterGenerator(seed=seed)
    params = generator.generate(spec)

    # Build stem from template
    stem = spec.stem_template

    # For roots-based templates (r1, r2), compute coefficients and format stem
    if 'r1' in params and 'r2' in params:
        r1 = params['r1']
        r2 = params['r2']

        # For factored form templates: (x - r1)(x - r2)
        # Need to format as (x + r1) when r1 is negative (so subtraction becomes addition)
        sign_r1 = '- ' if r1 >= 0 else '+ '
        abs_r1 = abs(r1)
        sign_r2 = '- ' if r2 >= 0 else '+ '
        abs_r2 = abs(r2)

        # For standard form templates: x^2 + bx + c
        # where b = -(r1+r2), c = r1*r2
        b = -(r1 + r2)
        c = r1 * r2
        sign_b = '+ ' if b >= 0 else '- '
        abs_b = abs(b)
        sign_c = '+ ' if c >= 0 else '- '
        abs_c = abs(c)

        # Replace placeholders in template
        stem = stem.replace('{sign_r1}', sign_r1)
        stem = stem.replace('{r1}', str(abs_r1))
        stem = stem.replace('{sign_r2}', sign_r2)
        stem = stem.replace('{r2}', str(abs_r2))
        stem = stem.replace('{sign_b}', sign_b)
        stem = stem.replace('{b}', str(abs_b))
        stem = stem.replace('{sign_c}', sign_c)
        stem = stem.replace('{c}', str(abs_c))

    # For vertex-based templates (h, k), format vertex form
    if 'h' in params and 'k' in params:
        h = params['h']
        k = params['k']

        # Vertex form: (x - h)^2 + k
        sign_h = '- ' if h >= 0 else '+ '
        abs_h = abs(h)
        sign_k = '+ ' if k >= 0 else '- '
        abs_k = abs(k)

        stem = stem.replace('{sign_h}', sign_h)
        stem = stem.replace('{h}', str(abs_h))
        stem = stem.replace('{sign_k}', sign_k)
        stem = stem.replace('{k}', str(abs_k))

    # For standard form with a, b, c parameters
    if 'a' in params and 'b' in params and 'c' in params:
        a = params['a']
        b = params['b']
        c = params['c']

        # Format as ax^2 + bx + c
        a_str = '' if a == 1 else ('-' if a == -1 else str(a))
        a_fmt = '' if a == 1 else ('-' if a == -1 else f'{a}')  # Alternative formatting
        sign_b = '+ ' if b >= 0 else '- '
        abs_b = abs(b)
        sign_c = '+ ' if c >= 0 else '- '
        abs_c = abs(c)

        stem = stem.replace('{a}', a_str)
        stem = stem.replace('{a_fmt}', a_fmt)
        stem = stem.replace('{sign_b}', sign_b)
        stem = stem.replace('{b}', str(abs_b))
        stem = stem.replace('{sign_c}', sign_c)
        stem = stem.replace('{c}', str(abs_c))

    # For templates with only b parameter (e.g., complete the square)
    elif 'b' in params and 'a' not in params:
        b = params['b']
        sign_b = '+ ' if b >= 0 else '- '
        abs_b = abs(b)

        stem = stem.replace('{sign_b}', sign_b)
        stem = stem.replace('{b}', str(abs_b))

    # Compute solution
    solution = spec.solver(params)

    # Generate distractors (pass difficulty for difficulty-aware distractor generation)
    distractors = spec.distractor_generator(params, solution, difficulty)

    # Create choices list
    choices = [solution] + distractors

    # Shuffle choices deterministically
    rng = random.Random(seed)
    choice_indices = list(range(len(choices)))
    rng.shuffle(choice_indices)

    shuffled_choices = [choices[i] for i in choice_indices]
    solution_idx = choice_indices.index(0)

    # Generate item_id
    if seed is not None:
        item_id = f"{skill_id}:{difficulty}:param:{seed}"
    else:
        import uuid
        item_id = str(uuid.uuid4())

    # Format as standard item
    return {
        "item_id": item_id,
        "skill_id": skill_id,
        "difficulty": difficulty,
        "stem": stem,
        "choices": [
            {"id": chr(ord("A") + i), "text": text}
            for i, text in enumerate(shuffled_choices)
        ],
        "solution_choice_id": chr(ord("A") + solution_idx),
        "solution_text": solution,
        "tags": ["parameterized", "factoring"],
        "parameters": params  # Include for debugging/analysis
    }


# Test function
if __name__ == "__main__":
    # Generate a few examples
    print("Parameterized Question Generation Examples:")
    print("=" * 60)

    for seed in [42, 123, 999]:
        item = generate_parameterized_item(
            "quad.solve.by_factoring",
            "easy",
            seed=seed
        )
        print(f"\nSeed {seed}:")
        print(f"  Stem: {item['stem']}")
        print(f"  Solution: {item['solution_text']}")
        print(f"  Choices: {[c['text'] for c in item['choices']]}")
        print(f"  Parameters: {item['parameters']}")
