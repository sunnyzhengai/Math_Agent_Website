"""
Tests for engine.mastery.update_progress (pure function).

Tests immutability, delta calculations, confidence scaling, and error cases.
"""

import pytest

from engine.mastery import SkillMastery, update_progress


def test_correct_increases_p_and_streak_and_attempts():
    """Correct answer: p increases, streak+1, attempts+1."""
    now = 1_700_000_000.0
    s0 = {"quad.graph.vertex": SkillMastery(p=0.5, attempts=3, streak=0, last_ts=0.0)}
    s1 = update_progress(s0, "quad.graph.vertex", correct=True, now=now, confidence=None)

    # Immutability check
    assert s1 is not s0
    assert s0["quad.graph.vertex"].p == 0.5  # unchanged

    # Update check
    sm = s1["quad.graph.vertex"]
    assert sm.attempts == 4
    assert sm.streak == 1
    assert sm.last_ts == now
    assert 0.5 < sm.p <= 1.0


def test_wrong_decreases_p_and_resets_streak():
    """Wrong answer: p decreases, streak resets, attempts+1."""
    now = 1_700_000_001.0
    s0 = {"quad.standard.vertex": SkillMastery(p=0.05, attempts=1, streak=2, last_ts=0.0)}
    s1 = update_progress(s0, "quad.standard.vertex", correct=False, now=now, confidence=None)

    sm = s1["quad.standard.vertex"]
    assert sm.attempts == 2
    assert sm.streak == 0
    assert 0.0 <= sm.p < 0.05  # decreased but clamped >= 0
    assert sm.last_ts == now


def test_confidence_scales_delta():
    """Confidence (1-5) scales delta: low→weak, high→strong."""
    now = 1_700_000_002.0
    s0 = {"quad.roots.factored": SkillMastery(p=0.5)}

    s_low = update_progress(s0, "quad.roots.factored", correct=True, now=now, confidence=2)
    s_hi = update_progress(s0, "quad.roots.factored", correct=True, now=now, confidence=5)

    assert s_low["quad.roots.factored"].p < s_hi["quad.roots.factored"].p


def test_invalid_confidence_raises():
    """Confidence must be 1-5 (or None); else raise ValueError."""
    now = 1_700_000_003.0
    s0 = {}

    with pytest.raises(ValueError, match="invalid_confidence"):
        update_progress(s0, "x", correct=True, now=now, confidence=0)

    with pytest.raises(ValueError, match="invalid_confidence"):
        update_progress(s0, "x", correct=True, now=now, confidence=6)


def test_other_skills_unchanged_and_immutable():
    """Update to skill A doesn't mutate skill B; both remain immutable."""
    now = 1_700_000_004.0
    s0 = {
        "a": SkillMastery(p=0.9, attempts=10, streak=5, last_ts=0.0),
        "b": SkillMastery(p=0.2, attempts=3, streak=0, last_ts=0.0),
    }

    s1 = update_progress(s0, "a", correct=False, now=now, confidence=None)

    assert s1 is not s0
    assert s1["b"] == s0["b"]  # untouched (identity check)
    assert s1["b"] is s0["b"]  # same frozen object


def test_new_skill_starts_from_default():
    """First attempt on new skill initializes from SkillMastery() default."""
    now = 1_700_000_005.0
    s0 = {}

    s1 = update_progress(s0, "brand.new.skill", correct=True, now=now, confidence=None)

    assert "brand.new.skill" in s1
    assert s1["brand.new.skill"].attempts == 1
    assert s1["brand.new.skill"].streak == 1
    assert 0.5 < s1["brand.new.skill"].p <= 1.0


def test_streak_is_informational_only():
    """Streak does NOT boost delta (no runaway curves)."""
    now = 1_700_000_006.0
    s0 = {}

    # Multiple correct answers
    s1 = update_progress(s0, "skill", correct=True, now=now, confidence=None)
    s2 = update_progress(s1, "skill", correct=True, now=now, confidence=None)
    s3 = update_progress(s2, "skill", correct=True, now=now, confidence=None)

    # Deltas should be consistent (+0.08 each), not accelerating
    assert s3["skill"].streak == 3
    assert s1["skill"].p < s2["skill"].p < s3["skill"].p
    # Each step is +0.08, so deltas should be roughly equal
    d1 = s1["skill"].p - 0.5
    d2 = s2["skill"].p - s1["skill"].p
    d3 = s3["skill"].p - s2["skill"].p
    assert abs(d1 - d2) < 0.001  # deltas consistent
    assert abs(d2 - d3) < 0.001


def test_p_clamped_to_01():
    """Mastery p is always in [0, 1], even with extreme deltas."""
    now = 1_700_000_007.0

    # Start high, keep losing
    s = {"skill": SkillMastery(p=0.99)}
    for _ in range(100):
        s = update_progress(s, "skill", correct=False, now=now, confidence=5)

    assert 0.0 <= s["skill"].p <= 1.0

    # Start low, keep winning
    s = {"skill": SkillMastery(p=0.01)}
    for _ in range(100):
        s = update_progress(s, "skill", correct=True, now=now, confidence=5)

    assert 0.0 <= s["skill"].p <= 1.0
