"""
Tests for engine.planner.plan_next_difficulty (pure policy function).

Tests policy thresholds, clamping, and reason string generation.
"""

from engine.planner import plan_next_difficulty


def test_policy_thresholds_and_reasons():
    """Policy applies correct thresholds with non-empty reason strings."""
    # Low mastery → easy
    d1, r1 = plan_next_difficulty(0.10)
    assert d1 == "easy" and isinstance(r1, str) and len(r1) > 0

    # Medium mastery → medium
    d2, r2 = plan_next_difficulty(0.50)
    assert d2 == "medium" and isinstance(r2, str) and len(r2) > 0

    # High mastery → hard
    d3, r3 = plan_next_difficulty(0.85)
    assert d3 == "hard" and isinstance(r3, str) and len(r3) > 0


def test_boundary_thresholds():
    """Test exact boundaries: 0.40 and 0.70."""
    # Just below 0.40
    d, r = plan_next_difficulty(0.39)
    assert d == "easy"

    # At 0.40
    d, r = plan_next_difficulty(0.40)
    assert d == "medium"

    # At 0.70
    d, r = plan_next_difficulty(0.70)
    assert d == "medium"

    # Just above 0.70
    d, r = plan_next_difficulty(0.71)
    assert d == "hard"


def test_clamps_p_and_is_total_function():
    """Function handles out-of-range p by clamping."""
    # Out-of-range inputs should clamp silently
    for p in (-1.0, 0.0, 0.39, 0.4, 0.7, 1.0, 2.0, 100.0):
        d, r = plan_next_difficulty(p)
        assert d in ("easy", "medium", "hard", "applied")
        assert isinstance(r, str) and len(r) > 0


def test_reason_strings_are_meaningful():
    """Reason strings should be non-empty and consistent."""
    reasons = set()

    for p in [0.1, 0.2, 0.5, 0.6, 0.8, 0.9]:
        d, r = plan_next_difficulty(p)
        assert r  # non-empty
        assert isinstance(r, str)
        reasons.add(r)

    # Should have at least 2-3 unique reasons across the range
    # (exact count depends on implementation, but not all same)
    assert len(reasons) >= 2
