"""
Minimal mastery update logic (pure, deterministic, no mutations).

State shape (per skill):
{
  "p": float,          # mastery probability in [0,1]
  "attempts": int,     # total attempts
  "streak": int,       # consecutive correct (resets on wrong)
  "last_ts": float,    # last update timestamp (unix seconds)
}

Streak is informational only and does not boost delta (no runaway curves).
For future: use last_ts for streak decay (if gap > 24h, reset streak to 0).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class SkillMastery:
    """Immutable mastery state for a single skill."""

    p: float = 0.5  # mastery probability [0, 1]
    attempts: int = 0  # total attempts
    streak: int = 0  # consecutive correct
    last_ts: float = 0.0  # unix seconds


def update_progress(
    state: Dict[str, SkillMastery],
    skill_id: str,
    correct: bool,
    now: float,
    confidence: Optional[int] = None,
) -> Dict[str, SkillMastery]:
    """
    Pure update: returns a NEW dict; does not mutate `state`.

    Behavior:
    - If skill_id absent, initialize from default SkillMastery().
    - Increment attempts by 1.
    - If correct: streak += 1; p += 0.08 * confidence_scale (clamp to [0,1]).
    - If wrong: streak = 0; p -= 0.06 * confidence_scale (clamp to [0,1]).
    - Confidence scale: 1.0 + (confidence - 3) * 0.15 (when confidence in 1..5).
    - Streak is informational only; does not boost delta (no runaway curves).
    - Set last_ts = now (future use: streak decay if gap > 24h).

    Args:
        state: Dict[skill_id, SkillMastery]
        skill_id: The skill being practiced
        correct: Whether the answer was correct
        now: Unix timestamp (float, seconds)
        confidence: Optional confidence 1-5 (scales delta; None→1.0×)

    Returns:
        A new dict with updated SkillMastery for skill_id.

    Raises:
        ValueError("invalid_confidence") if confidence not in 1..5 (when provided)
    """
    raise NotImplementedError
