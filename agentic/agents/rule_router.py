"""
Rule router: dispatches to skill-specific rule implementations.

Enables adding domain-specific agents without modifying the base registry.
Falls back to deterministic random for unsupported skills.
"""

from typing import Dict, Any
from .base import Agent
from .rules.vertex_from_vertexform import VertexFromVertexFormAgent
from .rules.standard_vertex import VertexFromStandardFormAgent
from .random_guess import RandomGuessAgent


# Instantiate rule agents (stateless, safe to share)
_VTXFORM = VertexFromVertexFormAgent()
_STD = VertexFromStandardFormAgent()
_RAND = RandomGuessAgent()


class RuleRouterAgent(Agent):
    """
    Routes to skill-specific rule implementations.

    Supported skills:
    - quad.graph.vertex → vertex form parsing
    - quad.standard.vertex → standard form parsing + vertex calculation
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

        # Extend here for more skills:
        # if skill_id == "quad.roots.factored":
        #     return _ROOTS.choose(item)

        # Default: deterministic random
        return _RAND.choose(item)
