# quadratics_completing_the_square

Test script: `python3 tests/test_quadratics_completing_the_square.py <template_number>`

## Templates (24 total)

### Standard form: x^2 + bx + c = 0
- Template 1: x^2 + bx + c = 0 (b > 0, c > 0)
- Template 2: x^2 - bx + c = 0 (b > 0, c > 0)
- Template 3: x^2 + bx - c = 0 (b > 0, c > 0)
- Template 4: x^2 - bx - c = 0 (b > 0, c > 0)

### Rearrangement form: x^2 + c = d ± bx
- Template 5: x^2 + c = d + bx (b > 0, c > 0, d > 0)
- Template 6: x^2 + c = d - bx (b > 0, c > 0, d > 0)
- Template 7: x^2 - c = d - bx (b > 0, c > 0, d > 0)
- Template 8: x^2 - c = d + bx (b > 0, c > 0, d > 0)

### With leading coefficient: ax^2 + bx + c = x^2 ± d
- Template 9: ax^2 + bx + c = x^2 + d (b > 0, c > 0, d > 0)
- Template 10: ax^2 - bx + c = x^2 + d (b > 0, c > 0, d > 0)
- Template 11: ax^2 + bx - c = x^2 + d (b > 0, c > 0, d > 0)
- Template 12: ax^2 + bx + c = x^2 - d (b > 0, c > 0, d > 0)
- Template 13: ax^2 - bx - c = x^2 + d (b > 0, c > 0, d > 0)
- Template 14: ax^2 + bx - c = x^2 - d (b > 0, c > 0, d > 0)
- Template 15: ax^2 - bx - c = x^2 + d (b > 0, c > 0, d > 0)
- Template 16: ax^2 - bx - c = x^2 - d (b > 0, c > 0, d > 0)

### With rearrangement: ax^2 + bx + c = d ± bx
- Template 17: ax^2 + bx + c = d + bx (b > 0, c > 0, d > 0)
- Template 18: ax^2 - bx + c = d + bx (b > 0, c > 0, d > 0)
- Template 19: ax^2 + bx - c = d + bx (b > 0, c > 0, d > 0)
- Template 20: ax^2 + bx + c = d - bx (b > 0, c > 0, d > 0)
- Template 21: ax^2 - bx - c = d + bx (b > 0, c > 0, d > 0)
- Template 22: ax^2 + bx - c = d - bx (b > 0, c > 0, d > 0)
- Template 23: ax^2 - bx + c = d - bx (b > 0, c > 0, d > 0)
- Template 24: ax^2 - bx - c = d - bx (b > 0, c > 0, d > 0)

## Answer Complexity Constraints

- Coefficient 'a' (templates 9-24): between 2 and 5
- Coefficients b, c, d (templates 1-8): between 1 and 8
- Coefficients b, c, d (templates 9-24): between 1 and 6
- For irrational solutions (non-perfect-square discriminant): discriminant must be ≤ 20
- This ensures radicals are simple (√2, √3, √5, √6, √7, √10, √11, √13, √14, √15, √17, √19, √20)

## Answer Format

- Display all answers in exact form (no decimals)
- Integers: x = 3
- Fractions: x = -7/2
- Radicals: x = 3 - √5 or x = (-2 + √7)/3

## Common Mistake Patterns

- Sign error when completing square: flip sign of b
- Forgetting ± when taking square root: only positive solution
- Mixed sign error: flip sign of one solution only
- Arithmetic errors in calculation
