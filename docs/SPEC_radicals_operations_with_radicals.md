# radicals_operations_with_radicals

Test script: `python3 tests/test_radicals_operations_with_radicals.py <template_number>`

## Templates (4 total)

- Template 1: Add like radicals: a√n + b√n
- Template 2: Multiply binomials with radicals: (a + √n)(a - √n) [difference of squares]
- Template 3: Rationalize denominator: a/√n
- Template 4: Rationalize denominator: a/(b + √n) [conjugate method]

## Answer Complexity Constraints

- Coefficients a, b: between 1 and 8
- Radicals n: between 2 and 20
- For difference of squares: use small values (a ≤ 5, n ≤ 10)
- For conjugates: b ≤ 5, n ≤ 10

## Answer Format

- Combined radicals: 7√2
- Difference of squares: a² - n (integer result)
- Rationalized: (a√n)/n or simplified form
- Conjugate result: (ab - a√n)/(b² - n) simplified

## Common Mistake Patterns

- Not simplifying fully after rationalization
- Multiplying by wrong conjugate
