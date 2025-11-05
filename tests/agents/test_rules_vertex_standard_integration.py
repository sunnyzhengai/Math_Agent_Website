"""
Integration test: Rules agent correctly solves standard-form vertex problems

CONTRACT:
  The rules agent, when given a standard-form vertex item, should:
  1. Detect the standard form y = ax^2 + bx + c
  2. Call parse_standard_quadratic + vertex_from_standard to get (h, k)
  3. Find the choice text matching f"({h:g}, {k:g})"
  4. Return the choice ID (A/B/C/D) corresponding to that choice

This test verifies the integration without unit-testing the parser itself.
"""

import pytest
from engine.templates import generate_item
from engine.grader import grade_response
from agentic.agents.registry import get_agent


class TestRulesAgentStandardVertexIntegration:
    """Integration: rules agent solves standard-form vertex problems."""

    def test_rules_agent_solves_standard_vertex_known_case(self):
        """
        Test case: "Find the vertex of y = -x^2 + 4x + 1."
        Expected vertex: (2, 5)
        Correct choice should have text "(2, 5)"
        """
        # Generate a known item
        item = generate_item("quad.standard.vertex", "easy", seed=11)
        
        # Get the rules agent
        agent = get_agent("rules")
        
        # Agent should pick the correct choice
        choice_id = agent.choose(item)
        
        # Verify the choice is valid
        assert choice_id in {"A", "B", "C", "D"}, f"Invalid choice: {choice_id}"
        
        # Verify grading confirms the choice is correct
        result = grade_response(item, choice_id)
        assert result["correct"] is True, \
            f"Rules agent chose {choice_id}, but it's incorrect. " \
            f"Correct answer is {item['solution_choice_id']}"

    @pytest.mark.parametrize("seed", [11, 12, 13, 14, 15])
    def test_rules_agent_solves_multiple_standard_vertex_cases(self, seed):
        """Verify rules agent works across multiple seeds for standard vertex."""
        item = generate_item("quad.standard.vertex", "easy", seed=seed)
        agent = get_agent("rules")
        choice_id = agent.choose(item)
        
        # Verify the choice is valid
        assert choice_id in {"A", "B", "C", "D"}
        
        # Verify the choice is correct
        result = grade_response(item, choice_id)
        assert result["correct"] is True, \
            f"Seed {seed}: agent chose {choice_id} but correct is {item['solution_choice_id']}"

    def test_rules_agent_returns_valid_choice_for_unsupported_skills(self):
        """
        Verify that if rules agent hits an unsupported skill,
        it falls back gracefully (returns a valid choice).
        """
        # Use a skill that doesn't have a rule yet
        item = generate_item("quad.roots.factored", "easy", seed=42)
        agent = get_agent("rules")
        choice_id = agent.choose(item)
        
        # Should return a valid choice (may or may not be correct)
        assert choice_id in {"A", "B", "C", "D"}
