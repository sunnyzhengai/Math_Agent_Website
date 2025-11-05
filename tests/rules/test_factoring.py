r"""
Unit tests for factoring rule: solve ax^2 + bx + c = 0 by finding integer roots

Tests cover:
  - Parsing standard form from stems
  - Finding factor pairs (a=1 case)
  - Solving and formatting roots
"""

import pytest
from agentic.agents.rules.factoring import (
    parse_quadratic_standard,
    factor_a1,
    factor_general_ac,
    solve_by_factoring_a1,
    format_roots,
)


class TestParseQuadraticStandard:
    """Test parsing ax^2 + bx + c = 0 from stems."""

    VALID_CASES = [
        ("Solve: x^2 + 5x + 6 = 0", (1, 5, 6)),
        ("Solve using factoring: x^2 - x - 6 = 0", (1, -1, -6)),
        ("x^2 + 7x + 12 = 0", (1, 7, 12)),
        # Implicit coefficient
        ("Solve: x^2 + x + 1 = 0", (1, 1, 1)),
        # Extra whitespace
        ("Solve: x^2  +  5x  +  6 = 0", (1, 5, 6)),
        # Missing linear term
        ("x^2 + 5x = 0", (1, 5, 0)),
    ]

    @pytest.mark.parametrize("stem, expected", VALID_CASES)
    def test_parse_valid(self, stem, expected):
        """Verify parsing valid standard-form stems."""
        result = parse_quadratic_standard(stem)
        assert result == expected


class TestFactorA1:
    """Test finding (p, q) such that p*q = c and p+q = b."""

    CASES = [
        # (b, c, expected)
        (5, 6, (2, 3)),           # x^2 + 5x + 6 = (x+2)(x+3)
        (-1, -6, (-3, 2)),        # x^2 - x - 6 = (x-3)(x+2)
        (7, 12, (3, 4)),          # x^2 + 7x + 12 = (x+3)(x+4)
        (-4, 4, (-2, -2)),        # x^2 - 4x + 4 = (x-2)^2
        (5, 0, (0, 5)),           # x^2 + 5x = x(x+5)
    ]

    @pytest.mark.parametrize("b, c, expected", CASES)
    def test_factor_a1_valid(self, b, c, expected):
        """Verify factor_a1 finds correct pairs."""
        result = factor_a1(b, c)
        assert result == expected

    NO_FACTOR_CASES = [
        (0, 1),      # x^2 + 1: no real roots
        (1, 1),      # x^2 + x + 1: no real integer roots
        (-1, 1),     # x^2 - x + 1: discriminant negative
    ]

    @pytest.mark.parametrize("b, c", NO_FACTOR_CASES)
    def test_factor_a1_no_factors(self, b, c):
        """Verify factor_a1 returns None for non-factorable cases."""
        result = factor_a1(b, c)
        assert result is None


class TestSolveByFactoringA1:
    """Test complete factoring solver (a=1 case)."""

    CASES = [
        # (b, c, expected_roots)
        (5, 6, (-3, -2)),        # x^2 + 5x + 6 = 0 → x = -2, -3
        (-1, -6, (-2, 3)),       # x^2 - x - 6 = 0 → x = -2, 3
        (7, 12, (-4, -3)),       # x^2 + 7x + 12 = 0 → x = -3, -4
        (-4, 4, (2, 2)),         # x^2 - 4x + 4 = 0 → x = 2 (double root, sorted)
        (5, 0, (-5, 0)),         # x^2 + 5x = 0 → x = 0, -5
    ]

    @pytest.mark.parametrize("b, c, expected", CASES)
    def test_solve_a1_valid(self, b, c, expected):
        """Verify solve_by_factoring_a1 returns sorted roots."""
        result = solve_by_factoring_a1(b, c)
        assert result == expected

    def test_solve_a1_no_solution(self):
        """Verify solve returns None for non-factorable."""
        result = solve_by_factoring_a1(0, 1)
        assert result is None


class TestFormatRoots:
    """Test formatting roots as choice text."""

    CASES = [
        ((2, 3), "x = 2 and x = 3"),
        ((-2, -3), "x = -3 and x = -2"),
        ((0, 5), "x = 0 and x = 5"),
        ((-5, 0), "x = -5 and x = 0"),
        ((2, 2), "x = 2 and x = 2"),
    ]

    @pytest.mark.parametrize("roots, expected", CASES)
    def test_format_roots(self, roots, expected):
        """Verify roots format to choice text."""
        result = format_roots(roots)
        assert result == expected


class TestIntegrationFactoring:
    """Integration: parse stem → factor → format."""

    def test_full_pipeline_example1(self):
        """Full pipeline: x^2 + 5x + 6 = 0."""
        stem = "Solve using factoring: x^2 + 5x + 6 = 0"
        a, b, c = parse_quadratic_standard(stem)
        assert a == 1

        roots = solve_by_factoring_a1(b, c)
        assert roots == (-3, -2)

        formatted = format_roots(roots)
        assert formatted == "x = -3 and x = -2"

    def test_full_pipeline_example2(self):
        """Full pipeline: x^2 - x - 6 = 0."""
        stem = "x^2 - x - 6 = 0"
        a, b, c = parse_quadratic_standard(stem)
        roots = solve_by_factoring_a1(b, c)
        assert roots == (-2, 3)
        formatted = format_roots(roots)
        assert formatted == "x = -2 and x = 3"
