"""
Rule router: dispatches to skill-specific rule implementations.

Enables adding domain-specific agents without modifying the base registry.
Falls back to deterministic random for unsupported skills.
"""

from typing import Dict, Any
from .base import Agent
from .rules.vertex_from_vertexform import VertexFromVertexFormAgent
from .rules.standard_vertex import VertexFromStandardFormAgent
from .rules.factoring_agent import FactoringAgent
from .rules.factored_roots_agent import FactoredRootsAgent
from .random_guess import RandomGuessAgent


# Instantiate rule agents (stateless, safe to share)
_VTXFORM = VertexFromVertexFormAgent()
_STD = VertexFromStandardFormAgent()
_FACTORING = FactoringAgent()
_FACTORED_ROOTS = FactoredRootsAgent()
_RAND = RandomGuessAgent()


class RuleRouterAgent(Agent):
    """
    Routes to skill-specific rule implementations.

    Supported skills:
    - quad.graph.vertex → vertex form parsing
    - quad.standard.vertex → standard form parsing + vertex calculation
    - quad.solve.by_factoring → integer factoring solver
    - quad.roots.factored → factored form root extraction
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
            return _FACTORING.choose(item)

        if skill_id == "quad.roots.factored":
            return _FACTORED_ROOTS.choose(item)

        # Extend here for more skills (e.g., quadratic formula)

        # Default: deterministic random
        return _RAND.choose(item)
