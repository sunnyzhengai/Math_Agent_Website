"""
Agent registry: centralized lookup and instantiation.

Registry stores agent classes (not instances) and instantiates on demand,
enabling flexibility for stateful agents and better testing.
"""

from typing import Dict, Type, List
from .base import Agent
from .oracle import OracleAgent
from .always_a import AlwaysAAgent
from .random_guess import RandomGuessAgent
from .rule_router import RuleRouterAgent


# Registry maps agent names to classes (not instances)
_REGISTRY: Dict[str, Type[Agent]] = {
    "oracle": OracleAgent,
    "always_a": AlwaysAAgent,
    "random": RandomGuessAgent,
    "rules": RuleRouterAgent,
}


def get_agent(name: str) -> Agent:
    """
    Get an agent instance by name.

    Args:
        name: Agent name (must be in registry).

    Returns:
        Agent instance.

    Raises:
        ValueError: If agent name is not in registry.
    """
    if name not in _REGISTRY:
        raise ValueError(f"unknown_agent:{name}")
    return _REGISTRY[name]()


def list_agents() -> List[str]:
    """
    List all registered agent names.

    Returns:
        Sorted list of agent names.
    """
    return sorted(_REGISTRY.keys())


def register_agent(name: str, agent_class: Type[Agent]) -> None:
    """
    Register a new agent class.

    Args:
        name: Agent name.
        agent_class: Agent class (must inherit from Agent).

    Raises:
        ValueError: If name already registered or class is invalid.
    """
    if name in _REGISTRY:
        raise ValueError(f"agent_already_registered:{name}")
    if not issubclass(agent_class, Agent):
        raise ValueError(f"invalid_agent_class:{agent_class}")
    _REGISTRY[name] = agent_class
