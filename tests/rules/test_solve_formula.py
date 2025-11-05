r"""
Unit tests for quadratic formula solver: ax^2 + bx + c = 0

Tests cover:
  - Parsing coefficients from standard form
  - Computing roots via quadratic formula
  - Order-insensitive choice matching
  - Edge cases (double roots, spaces, Unicode)
"""

import pytest
import math
from agentic.agents.rules.solve_formula import (
    parse_quadratic_coeffs,
    quadratic_roots,
    roots_match_choice,
)


class TestParseQuadraticCoeffs:
    """Test parsing a, b, c from quadratic stems."""

    VALID_CASES = [
        ("Solve: x^2 - 5x + 6 = 0", (1.0, -5.0, 6.0)),
        ("2x^2 + 4x - 30 = 0", (2.0, 4.0, -30.0)),
        ("x^2 - 4x + 4 = 0", (1.0, -4.0, 4.0)),
        ("x^2 + x + 1 = 0", (1.0, 1.0, 1.0)),
        ("-x^2 + 3x - 2 = 0", (-1.0, 3.0, -2.0)),
        # With extra spaces
        ("x^2  -  5x  +  6 = 0", (1.0, -5.0, 6.0)),
        # Without "= 0"
        ("x^2 - 5x + 6", (1.0, -5.0, 6.0)),
    ]

    @pytest.mark.parametrize("stem, expected", VALID_CASES)
    def test_parse_valid(self, stem, expected):
        """Verify parsing valid quadratic equations."""
        result = parse_quadratic_coeffs(stem)
        assert result is not None
        a, b, c = result
        ea, eb, ec = expected
        assert abs(a - ea) < 1e-9
        assert abs(b - eb) < 1e-9
        assert abs(c - ec) < 1e-9

    INVALID_CASES = [
        "5x + 7",           # linear
        "x^3 - 3x + 1",    # cubic
    ]

    @pytest.mark.parametrize("stem", INVALID_CASES)
    def test_parse_invalid(self, stem):
        """Verify parsing rejects invalid forms."""
        result = parse_quadratic_coeffs(stem)
        assert result is None


class TestQuadraticRoots:
    """Test quadratic formula computation."""

    REAL_ROOTS_CASES = [
        # (a, b, c, expected_roots)
        (1.0, -5.0, 6.0, (2.0, 3.0)),      # x^2 - 5x + 6 = (x-2)(x-3)
        (1.0, -4.0, 4.0, (2.0, 2.0)),      # x^2 - 4x + 4 = (x-2)^2 (double)
        (2.0, 4.0, -30.0, (-5.0, 3.0)),    # 2x^2 + 4x - 30
        (1.0, 1.0, 1.0, None),             # x^2 + x + 1 (complex roots)
    ]

    @pytest.mark.parametrize("a, b, c, expected", REAL_ROOTS_CASES)
    def test_quadratic_roots(self, a, b, c, expected):
        """Verify quadratic formula computation."""
        result = quadratic_roots(a, b, c)
        assert result == expected or (
            expected is not None and result is not None and
            abs(result[0] - expected[0]) < 1e-6 and
            abs(result[1] - expected[1]) < 1e-6
        )

    def test_zero_discriminant(self):
        """Test double root (discriminant = 0)."""
        # (x - 2)^2 = x^2 - 4x + 4
        r = quadratic_roots(1.0, -4.0, 4.0)
        assert r is not None
        assert abs(r[0] - 2.0) < 1e-9
        assert abs(r[1] - 2.0) < 1e-9

    def test_negative_discriminant(self):
        """Test complex roots (discriminant < 0)."""
        # x^2 + x + 1 has discriminant = 1 - 4 = -3 < 0
        r = quadratic_roots(1.0, 1.0, 1.0)
        assert r is None


class TestRootsMatchChoice:
    """Test order-insensitive root matching."""

    MATCH_CASES = [
        # (roots, choice_text, should_match)
        ((2.0, 3.0), "(2, 3)", True),
        ((2.0, 3.0), "(3, 2)", True),       # reversed
        ((2.0, 3.0), "{2, 3}", True),      # braces
        ((2.0, 3.0), "{3, 2}", True),      # braces reversed
        ((-5.0, 3.0), "(-5, 3)", True),
        ((-5.0, 3.0), "(3, -5)", True),
        ((2.0, 2.0), "(2, 2)", True),      # double root
        # Spaces
        ((2.0, 3.0), "( 2 , 3 )", True),
        # Non-matches
        ((2.0, 3.0), "(2, 4)", False),
        ((2.0, 3.0), "(1, 3)", False),
    ]

    @pytest.mark.parametrize("roots, choice_text, should_match", MATCH_CASES)
    def test_roots_match_choice(self, roots, choice_text, should_match):
        """Verify order-insensitive matching."""
        result = roots_match_choice(roots, choice_text)
        assert result == should_match

    def test_none_roots(self):
        """Verify None roots never match."""
        assert roots_match_choice(None, "(2, 3)") is False


class TestIntegrationSolveFormula:
    """Integration: parse → compute → match."""

    def test_full_pipeline_example1(self):
        """Full: x^2 - 5x + 6 = 0 → (2, 3)"""
        stem = "Solve: x^2 - 5x + 6 = 0"
        coeffs = parse_quadratic_coeffs(stem)
        assert coeffs is not None

        roots = quadratic_roots(*coeffs)
        assert roots is not None

        assert roots_match_choice(roots, "(2, 3)")
        assert roots_match_choice(roots, "(3, 2)")

    def test_full_pipeline_example2(self):
        """Full: 2x^2 + 4x - 30 = 0 → (-5, 3)"""
        stem = "2x^2 + 4x - 30 = 0"
        coeffs = parse_quadratic_coeffs(stem)
        assert coeffs is not None

        roots = quadratic_roots(*coeffs)
        assert roots is not None

        assert roots_match_choice(roots, "(-5, 3)")
        assert roots_match_choice(roots, "(3, -5)")

    def test_full_pipeline_double_root(self):
        """Full: x^2 - 4x + 4 = 0 → (2, 2)"""
        stem = "x^2 - 4x + 4 = 0"
        coeffs = parse_quadratic_coeffs(stem)
        assert coeffs is not None

        roots = quadratic_roots(*coeffs)
        assert roots is not None

        assert roots_match_choice(roots, "(2, 2)")
