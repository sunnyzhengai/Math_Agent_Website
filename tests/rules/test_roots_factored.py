r"""
Unit tests for extracting roots from factored form: a(x - r₁)(x - r₂) = 0

Tests cover:
  - Parsing factored forms with leading scalars
  - Handling zero roots
  - Order-insensitive choice matching
  - Edge cases (spaces, Unicode dashes)
"""

import pytest
from agentic.agents.rules.roots_factored import parse_factored_roots, roots_match_choice


class TestParseFactoredRoots:
    """Test parsing roots from factored form."""

    VALID_CASES = [
        ("(x - 3)(x + 2) = 0", (3.0, -2.0)),
        ("(x + 4)(x - 1) = 0", (-4.0, 1.0)),
        ("(x - 1)(x - 2) = 0", (1.0, 2.0)),
        ("(x + 5)(x + 3) = 0", (-5.0, -3.0)),
        # With leading scalar
        ("2(x - 3)(x + 2) = 0", (3.0, -2.0)),
        ("2 (x + 4)(x - 1) = 0", (-4.0, 1.0)),
        ("-2(x - 3)(x + 2) = 0", (3.0, -2.0)),
        ("- (x + 5)(x - 1) = 0", (-5.0, 1.0)),
        # With zero root
        ("(x)(x - 3) = 0", (0.0, 3.0)),
        ("(x)(x + 2) = 0", (0.0, -2.0)),
        ("(x - 5)(x) = 0", (5.0, 0.0)),
        # Extra spaces
        ("( x - 3 ) ( x + 2 ) = 0", (3.0, -2.0)),
        # Without explicit = 0
        ("(x - 3)(x + 2)", (3.0, -2.0)),
    ]

    @pytest.mark.parametrize("stem, expected", VALID_CASES)
    def test_parse_valid(self, stem, expected):
        """Verify parsing valid factored forms."""
        result = parse_factored_roots(stem)
        assert result is not None
        r1, r2 = result
        e1, e2 = expected
        # Check both orderings (order-insensitive)
        assert (
            (abs(r1 - e1) < 1e-9 and abs(r2 - e2) < 1e-9) or
            (abs(r1 - e2) < 1e-9 and abs(r2 - e1) < 1e-9)
        )

    INVALID_CASES = [
        "y = (x - 3)^2 + 2",      # vertex form, not factored
        "x^2 - 5x + 6",           # standard form, no parentheses
        "5x + 7",                 # not quadratic
    ]

    @pytest.mark.parametrize("stem", INVALID_CASES)
    def test_parse_invalid(self, stem):
        """Verify parsing rejects invalid forms."""
        result = parse_factored_roots(stem)
        assert result is None


class TestRootsMatchChoice:
    """Test order-insensitive root matching against choices."""

    MATCH_CASES = [
        # (roots, choice_text, should_match)
        ((3.0, -2.0), "(3, -2)", True),
        ((3.0, -2.0), "(-2, 3)", True),       # reversed order
        ((3.0, -2.0), "{3, -2}", True),      # braces
        ((3.0, -2.0), "{-2, 3}", True),      # braces reversed
        ((-4.0, 1.0), "(-4, 1)", True),
        ((-4.0, 1.0), "(1, -4)", True),
        ((0.0, 3.0), "(0, 3)", True),
        ((0.0, 3.0), "(3, 0)", True),
        # Negatives
        ((-5.0, -3.0), "(-5, -3)", True),
        ((-5.0, -3.0), "(-3, -5)", True),
        # Spaces in choice text
        ((3.0, -2.0), "( 3 , -2 )", True),
        # Non-matches
        ((3.0, -2.0), "(3, 2)", False),      # wrong second root
        ((3.0, -2.0), "(3, -3)", False),     # wrong second root
    ]

    @pytest.mark.parametrize("roots, choice_text, should_match", MATCH_CASES)
    def test_roots_match_choice(self, roots, choice_text, should_match):
        """Verify order-insensitive matching."""
        result = roots_match_choice(roots, choice_text)
        assert result == should_match


class TestIntegrationRootsFactored:
    """Integration: parse → match choice."""

    def test_full_pipeline_example1(self):
        """Full pipeline: (x - 3)(x + 2) = 0."""
        stem = "(x - 3)(x + 2) = 0"
        roots = parse_factored_roots(stem)
        assert roots is not None

        # Should match both orders
        assert roots_match_choice(roots, "(3, -2)")
        assert roots_match_choice(roots, "(-2, 3)")

    def test_full_pipeline_example2(self):
        """Full pipeline: 2(x + 4)(x - 1) = 0."""
        stem = "2(x + 4)(x - 1) = 0"
        roots = parse_factored_roots(stem)
        assert roots is not None

        # Should match (-4, 1)
        assert roots_match_choice(roots, "(-4, 1)")
        assert roots_match_choice(roots, "(1, -4)")

    def test_full_pipeline_zero_root(self):
        """Full pipeline: (x)(x - 3) = 0."""
        stem = "(x)(x - 3) = 0"
        roots = parse_factored_roots(stem)
        assert roots is not None

        assert roots_match_choice(roots, "(0, 3)")
        assert roots_match_choice(roots, "(3, 0)")
