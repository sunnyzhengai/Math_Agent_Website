# radicals_simplifying_radicals

Test script: `python3 tests/test_radicals_simplifying_radicals.py <template_number>`

## Templates (4 total)

- Template 1: Simplify √n (n has perfect square factor, e.g., √50 = 5√2)
- Template 2: Simplify ³√(n·x^m) (cube root with variables)
- Template 3: Multiply and simplify √a × √b
- Template 4: Divide and simplify √a / √b

## Answer Complexity Constraints

- For √n: n between 8 and 100, must have perfect square factor
- For cube roots: n·x^m where n ∈ {8, 27, 54, 128} and m ≤ 6
- For multiplication: a, b between 2 and 12
- For division: a/b results in perfect square or simple radical

## Answer Format

- Simplified radicals: 5√2, 2√3
- With variables: 2x√(3x)
- Simplified expressions: √6, 4

## Common Mistake Patterns

- Leaving perfect square factors under radical
- Not simplifying completely
