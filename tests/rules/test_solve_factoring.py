r"""
Unit tests for trinomial factoring solver: ax^2 + bx + c = 0

Tests cover:
  - Simple case (a=1): factor pairs
  - AC method (a≠1): integer factorization
  - Double roots
  - Non-factorable cases (return None)
  - Order-insensitive choice matching
"""

import pytest
from agentic.agents.rules.solve_factoring import factor_trinomial, roots_match_choice


class TestFactorTrinomial:
    """Test trinomial factoring."""

    FACTORABLE_CASES = [
        # (a, b, c, expected_roots)
        (1.0, -5.0, 6.0, (2.0, 3.0)),      # x^2 - 5x + 6 = (x-2)(x-3)
        (1.0, 5.0, 6.0, (-3.0, -2.0)),     # x^2 + 5x + 6 = (x+2)(x+3)
        (1.0, -4.0, 4.0, (2.0, 2.0)),      # x^2 - 4x + 4 = (x-2)^2 (double)
        (2.0, 7.0, 3.0, (-3.0, -0.5)),     # 2x^2 + 7x + 3 = 2(x+3)(x+0.5)
        (1.0, 1.0, 0.0, (-1.0, 0.0)),      # x^2 + x = x(x+1)
    ]

    @pytest.mark.parametrize("a, b, c, expected", FACTORABLE_CASES)
    def test_factor_factorable(self, a, b, c, expected):
        """Verify factoring of nice trinomials."""
        result = factor_trinomial(a, b, c)
        assert result is not None, f"Should factor {a}x^2 + {b}x + {c}"
        
        r1, r2 = result
        e1, e2 = expected
        
        # Check both orderings (order-insensitive)
        assert (
            (abs(r1 - e1) < 1e-6 and abs(r2 - e2) < 1e-6) or
            (abs(r1 - e2) < 1e-6 and abs(r2 - e1) < 1e-6)
        ), f"Got {result}, expected {expected}"

    NON_FACTORABLE_CASES = [
        (1.0, 1.0, 1.0),       # x^2 + x + 1 (discriminant < 0)
        (1.0, 2.0, 2.0),       # x^2 + 2x + 2 (no integer factors)
        (2.0, 1.0, 3.0),       # 2x^2 + x + 3 (discriminant < 0)
    ]

    @pytest.mark.parametrize("a, b, c", NON_FACTORABLE_CASES)
    def test_factor_non_factorable(self, a, b, c):
        """Verify non-factorable trinomials return None."""
        result = factor_trinomial(a, b, c)
        assert result is None, f"Should not factor {a}x^2 + {b}x + {c}"


class TestRootsMatchChoice:
    """Test order-insensitive root matching."""

    MATCH_CASES = [
        # (roots, choice_text, should_match)
        ((2.0, 3.0), "(2, 3)", True),
        ((2.0, 3.0), "(3, 2)", True),       # reversed
        ((-3.0, -0.5), "(-3, -0.5)", True),
        ((-3.0, -0.5), "(-0.5, -3)", True), # reversed
        ((2.0, 2.0), "(2, 2)", True),       # double root
        # Spaces
        ((2.0, 3.0), "( 2 , 3 )", True),
        # Non-matches
        ((2.0, 3.0), "(2, 4)", False),
        (None, "(2, 3)", False),
    ]

    @pytest.mark.parametrize("roots, choice_text, should_match", MATCH_CASES)
    def test_roots_match_choice(self, roots, choice_text, should_match):
        """Verify order-insensitive matching."""
        result = roots_match_choice(roots, choice_text)
        assert result == should_match


class TestIntegrationSolveFactoring:
    """Integration: factor → match choice."""

    def test_full_pipeline_example1(self):
        """Full: x^2 - 5x + 6 = 0 → (2, 3)"""
        roots = factor_trinomial(1.0, -5.0, 6.0)
        assert roots is not None

        assert roots_match_choice(roots, "(2, 3)")
        assert roots_match_choice(roots, "(3, 2)")

    def test_full_pipeline_example2(self):
        """Full: 2x^2 + 7x + 3 = 0 → (-3, -0.5)"""
        roots = factor_trinomial(2.0, 7.0, 3.0)
        assert roots is not None

        assert roots_match_choice(roots, "(-3, -0.5)")
        assert roots_match_choice(roots, "(-0.5, -3)")

    def test_full_pipeline_double_root(self):
        """Full: x^2 - 4x + 4 = 0 → (2, 2)"""
        roots = factor_trinomial(1.0, -4.0, 4.0)
        assert roots is not None

        assert roots_match_choice(roots, "(2, 2)")
