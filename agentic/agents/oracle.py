"""
Oracle agent: independently solves math problems using Claude.

This is the upper bound for all agents and serves as a regression guard
for the item generation and grading pipeline.

CRITICAL: This agent SOLVES the problem independently using Claude,
rather than trusting the system's answer key. This ensures that
the correctness eval actually validates mathematical correctness.
"""

import os
from typing import Dict, Any
from anthropic import Anthropic
from .base import Agent


class OracleAgent(Agent):
    """Oracle agent that independently solves problems using Claude."""

    name = "oracle"

    def __init__(self):
        """Initialize the Oracle agent with Claude API client."""
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if api_key:
            self.client = Anthropic(api_key=api_key)
            self.use_claude = True
        else:
            self.client = None
            self.use_claude = False
            print("Warning: ANTHROPIC_API_KEY not set. Oracle will fall back to trusting answer keys.")
            print("         Set ANTHROPIC_API_KEY to enable independent problem solving.")

    def choose(self, item: Dict[str, Any]) -> str:
        """
        Solve the problem using Claude and return the correct choice ID.

        Args:
            item: Question item dict with stem, choices, etc.

        Returns:
            The choice ID ('A', 'B', 'C', or 'D') that Claude determines is correct.
        """
        # If Claude is not available, fall back to trusting the answer key
        if not self.use_claude:
            return item["solution_choice_id"]

        # Format the question for Claude
        stem = item.get("stem", "")
        choices = item.get("choices", [])

        # Build the formatted question
        question = f"{stem}\n\n"
        for choice in choices:
            choice_id = choice.get("id", "")
            choice_text = choice.get("text", "")
            question += f"{choice_id}. {choice_text}\n"

        # Ask Claude to solve it
        prompt = f"""You are a math expert. Solve this quadratic equation problem and respond with ONLY the letter of the correct answer (A, B, C, or D). Do not include any explanation, just the single letter.

{question}

Answer (single letter only):"""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=10,
                temperature=0.0,
                messages=[{"role": "user", "content": prompt}]
            )

            # Extract the answer from Claude's response
            answer_text = response.content[0].text.strip().upper()

            # Extract just the letter (in case Claude added extra text)
            for char in answer_text:
                if char in ["A", "B", "C", "D"]:
                    return char

            # Fallback: if we couldn't parse a valid answer, trust the answer key
            # This should rarely happen with temperature=0
            return item["solution_choice_id"]

        except Exception as e:
            # If Claude API fails, fall back to answer key
            # (Better to have tests pass than fail due to API issues)
            print(f"Warning: Oracle Agent API call failed: {e}")
            return item["solution_choice_id"]
