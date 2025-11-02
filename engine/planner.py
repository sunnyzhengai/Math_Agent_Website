"""
Simple planner policy to pick next difficulty from mastery p.

Policy (deterministic thresholds):
- p < 0.4   → "easy" with reason "building confidence"
- 0.4 ≤ p ≤ 0.7  → "medium" with reason "mixed practice"
- p > 0.7   → "hard" with reason "push challenge"

TODO: Query SKILL_TEMPLATES availability to pick "hard" or "applied" based on pool size.
For now, always return "hard" for p > 0.70.

TODO: Internationalize reason strings (e.g., "reason.building_confidence").
"""

from typing import Literal, Tuple

Difficulty = Literal["easy", "medium", "hard", "applied"]


def plan_next_difficulty(p: float) -> Tuple[Difficulty, str]:
    """
    Returns (difficulty, reason) based on mastery probability.

    Always returns a non-empty reason string explaining the choice.
    Clamps input p into [0, 1] for robustness.

    Args:
        p: Mastery probability (float, will be clamped to [0, 1])

    Returns:
        Tuple of (difficulty, reason_string)
        - difficulty: one of "easy", "medium", "hard"
        - reason: short explanation for UI/telemetry (e.g., "building confidence")
    """
    raise NotImplementedError
