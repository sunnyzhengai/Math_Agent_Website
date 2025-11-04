"""
Tests for agent strategies and registry.

Contract tests:
- All agents return valid choices
- Oracle always picks the correct answer
- Registry is initialized with expected agents
"""

import pytest
from engine.templates import generate_item
from agentic.agents.registry import get_agent, list_agents, register_agent
from agentic.agents.base import Agent


def test_registry_initialized():
    """Verify registry has expected agents."""
    names = list_agents()
    assert len(names) >= 3, f"Expected >= 3 agents, got {len(names)}"
    assert "oracle" in names
    assert "always_a" in names
    assert "random" in names


def test_registry_is_sorted():
    """Verify list_agents returns sorted list."""
    names = list_agents()
    assert names == sorted(names)


@pytest.mark.parametrize("agent_name", ["oracle", "always_a", "random"])
def test_agents_return_valid_choice(agent_name):
    """Verify each agent returns a valid choice ID."""
    item = generate_item("quad.graph.vertex", "easy", seed=42)
    agent = get_agent(agent_name)
    choice = agent.choose(item)
    
    assert isinstance(choice, str), f"{agent_name}.choose() must return str, got {type(choice)}"
    assert choice in {"A", "B", "C", "D"}, f"{agent_name} returned invalid choice: {choice}"


@pytest.mark.parametrize("agent_name", ["oracle", "always_a", "random"])
def test_agents_work_across_skills_and_difficulties(agent_name):
    """Verify agents work for different skills and difficulties."""
    test_cases = [
        ("quad.graph.vertex", "easy"),
        ("quad.standard.vertex", "medium"),
        ("quad.roots.factored", "hard"),
    ]
    
    for skill, difficulty in test_cases:
        item = generate_item(skill, difficulty, seed=42)
        agent = get_agent(agent_name)
        choice = agent.choose(item)
        assert choice in {"A", "B", "C", "D"}


def test_oracle_always_correct():
    """Regression guard: oracle must always pick the correct answer."""
    test_cases = [
        ("quad.graph.vertex", "easy", 42),
        ("quad.graph.vertex", "medium", 43),
        ("quad.standard.vertex", "easy", 11),
        ("quad.roots.factored", "medium", 12),
    ]
    
    agent = get_agent("oracle")
    for skill, difficulty, seed in test_cases:
        item = generate_item(skill, difficulty, seed=seed)
        choice = agent.choose(item)
        assert choice == item["solution_choice_id"], \
            f"Oracle should pick {item['solution_choice_id']}, got {choice}"


def test_always_a_always_returns_a():
    """Verify AlwaysA agent always returns 'A'."""
    agent = get_agent("always_a")
    
    for seed in range(10):
        item = generate_item("quad.graph.vertex", "easy", seed=seed)
        choice = agent.choose(item)
        assert choice == "A", f"AlwaysA should return 'A', got {choice}"


def test_random_deterministic_per_item():
    """Verify RandomGuess agent is deterministic for same item."""
    agent = get_agent("random")
    
    # Same seed should generate same item_id
    item1 = generate_item("quad.graph.vertex", "easy", seed=42)
    item2 = generate_item("quad.graph.vertex", "easy", seed=42)
    
    # Same item should get same choice from agent
    choice1 = agent.choose(item1)
    choice2 = agent.choose(item2)
    
    assert choice1 == choice2, \
        f"Random agent should be deterministic per item, got {choice1} vs {choice2}"


def test_random_varies_across_items():
    """Verify RandomGuess agent can pick different choices for different items."""
    agent = get_agent("random")
    
    choices = set()
    for seed in range(20):
        item = generate_item("quad.graph.vertex", "easy", seed=seed)
        choice = agent.choose(item)
        choices.add(choice)
    
    # Should have picked at least 2 different choices (very high probability)
    assert len(choices) >= 2, \
        f"Random agent should pick variety, got only: {choices}"


def test_get_agent_invalid_name():
    """Verify get_agent raises ValueError for unknown agent."""
    with pytest.raises(ValueError, match="unknown_agent"):
        get_agent("nonexistent_agent")


def test_register_agent():
    """Verify register_agent can add new agents."""
    from agentic.agents.base import Agent
    
    # Create a test agent
    class TestAgent(Agent):
        name = "test"
        def choose(self, item):
            return "B"
    
    # Register it
    register_agent("test", TestAgent)
    
    # Should be accessible
    agent = get_agent("test")
    assert isinstance(agent, TestAgent)
    
    # Should appear in list
    assert "test" in list_agents()
    
    # Clean up
    from agentic.agents import registry
    del registry._REGISTRY["test"]


def test_register_agent_duplicate():
    """Verify register_agent rejects duplicate names."""
    from agentic.agents.base import Agent
    
    class DummyAgent(Agent):
        name = "dummy"
        def choose(self, item):
            return "A"
    
    # Try to register as existing name
    with pytest.raises(ValueError, match="agent_already_registered"):
        register_agent("oracle", DummyAgent)


def test_register_agent_invalid_class():
    """Verify register_agent rejects non-Agent classes."""
    class NotAnAgent:
        pass
    
    with pytest.raises(ValueError, match="invalid_agent_class"):
        register_agent("invalid", NotAnAgent)
