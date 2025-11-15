# radicals_understanding_radicals

Test script: `python3 tests/test_radicals_understanding_radicals.py <template_number>`

## Templates (4 total)

- Template 1: What is √n? (n is perfect square)
- Template 2: Solve x² = n (n is perfect square)
- Template 3: Rewrite ⁿ√(x^m) as a power (convert to rational exponent)
- Template 4: √n is between what two integers? (n is non-perfect square)

## Answer Complexity Constraints

- Perfect squares n: {4, 9, 16, 25, 36, 49, 64, 81, 100}
- Non-perfect squares n: between 2 and 50
- Root indices: 2, 3 (square root, cube root)
- Powers m: between 1 and 6

## Answer Format

- Numeric: integers (e.g., 4, 5)
- Solutions: x = ±4
- Rational exponents: x^(2/3)
- Between integers: "between 5 and 6"

## Common Mistake Patterns

- Forgetting ± when solving x² = n
- Sign errors
- Not simplifying completely
