# quadratics_solving_with_square_roots

Test script: `python3 tests/test_quadratics_solving_with_square_roots.py <template_number>`

## Templates (8 total)

### Solve with square roots
- Template 1: x² = n (where n is a perfect square, e.g., 49, 64, 81)
- Template 2: x² = n (where n is NOT a perfect square, e.g., 50, 32, 20)

### Solve two-step radical equations
- Template 3: (x - a)² = n (perfect square, a > 0, n > 0)
- Template 4: (x + a)² = n (perfect square, a > 0, n > 0)
- Template 5: (x - a)² = n (non-perfect square, a > 0, n ≤ 20)
- Template 6: (x + a)² = n (non-perfect square, a > 0, n ≤ 20)

### Check for extraneous roots
- Template 7: √(x + a) = x - b (where one solution is extraneous)
- Template 8: √(x - a) = x - b (where one solution is extraneous)

## Answer Complexity Constraints

- For perfect squares: n ∈ {4, 9, 16, 25, 36, 49, 64, 81, 100}
- For non-perfect squares: n ≤ 20
- Values a, b: between 1 and 8

## Answer Format

- Display all answers in exact form (no decimals)
- Integers: x = ±7
- Radicals: x = 3 ± √5
- Multiple solutions: x = 8 or x = -2
- Extraneous roots: x = 2 (note: x = -1 is extraneous)

## Common Mistake Patterns

- Forgetting ± when taking square root
- Not checking for extraneous solutions
