"""
Rule router: dispatches to skill-specific rule implementations.

Enables adding domain-specific agents without modifying the base registry.
Falls back to deterministic random for unsupported skills.
"""

from typing import Dict, Any
from .base import Agent
from .rules.vertex_from_vertexform import VertexFromVertexFormAgent
from .rules.standard_vertex import VertexFromStandardFormAgent
from .rules.solve_factoring_agent import SolveFactoringAgent
from .rules.factored_roots_agent import FactoredRootsAgent
from .rules.solve_formula_agent import SolveFormulaAgent
from .rules.discriminant_agent import DiscriminantAnalysisAgent
from .rules.intercepts_agent import InterceptsAgent
from .rules.complete_square_agent import CompleteSquareAgent
from .rules.axis_symmetry_agent import AxisSymmetryAgent
from .random_guess import RandomGuessAgent


# Instantiate rule agents (stateless, safe to share)
_VTXFORM = VertexFromVertexFormAgent()
_STD = VertexFromStandardFormAgent()
_SOLVE_FACTORING = SolveFactoringAgent()
_FACTORED_ROOTS = FactoredRootsAgent()
_FORMULA = SolveFormulaAgent()
_DISCRIMINANT = DiscriminantAnalysisAgent()
_INTERCEPTS = InterceptsAgent()
_COMPLETE_SQUARE = CompleteSquareAgent()
_AXIS_SYMMETRY = AxisSymmetryAgent()
_RAND = RandomGuessAgent()


class RuleRouterAgent(Agent):
    """
    Routes to skill-specific rule implementations.

    Supported skills:
    - quad.graph.vertex → vertex form parsing
    - quad.standard.vertex → standard form parsing + vertex calculation
    - quad.solve.by_factoring → integer factoring solver
    - quad.roots.factored → factored form root extraction
    - quad.solve.by_formula → quadratic formula solver
    - quad.discriminant.analysis → discriminant calculation and root analysis
    - quad.intercepts → x and y intercept finding
    - quad.complete.square → completing the square transformations
    - quad.axis.symmetry → axis of symmetry calculation
    - (others) → deterministic random fallback
    """

    name = "rules"

    def choose(self, item: Dict[str, Any]) -> str:
        """
        Route to appropriate rule agent based on skill_id.

        Falls back to deterministic random if no rule matches.
        """
        skill_id = item.get("skill_id", "")

        if skill_id == "quad.graph.vertex":
            return _VTXFORM.choose(item)

        if skill_id == "quad.standard.vertex":
            return _STD.choose(item)

        if skill_id == "quad.solve.by_factoring":
            return _SOLVE_FACTORING.choose(item)

        if skill_id == "quad.roots.factored":
            return _FACTORED_ROOTS.choose(item)

        if skill_id == "quad.solve.by_formula":
            return _FORMULA.choose(item)

        if skill_id == "quad.discriminant.analysis":
            return _DISCRIMINANT.choose(item)

        if skill_id == "quad.intercepts":
            return _INTERCEPTS.choose(item)

        if skill_id == "quad.complete.square":
            return _COMPLETE_SQUARE.choose(item)

        if skill_id == "quad.axis.symmetry":
            return _AXIS_SYMMETRY.choose(item)

        # Extend here for more skills

        # Default: deterministic random
        return _RAND.choose(item)
