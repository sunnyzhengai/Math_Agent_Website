# quadratics_quadratic_formula

Test script: `python3 tests/test_quadratics_quadratic_formula.py <template_number>`

## Templates (12 total)

### Apply quadratic formula
- Template 1: Solve ax² + bx + c = 0 using quadratic formula (discriminant is perfect square)
- Template 2: Solve ax² - bx + c = 0 using quadratic formula (discriminant is perfect square)
- Template 3: Solve ax² + bx - c = 0 using quadratic formula (discriminant is perfect square)
- Template 4: Solve ax² + bx + c = 0 using quadratic formula (discriminant ≤ 20, non-perfect)

### Compute discriminant
- Template 5: What is the discriminant of ax² + bx + c = 0?
- Template 6: What is the discriminant of ax² - bx - c = 0?

### Interpret discriminant
- Template 7: Given discriminant = 25, how many real solutions?
- Template 8: Given discriminant = 0, how many real solutions?
- Template 9: Given discriminant = -5, how many real solutions?
- Template 10: For ax² + bx + c = 0, what discriminant means 2 real solutions?

### Simplify radical in solution
- Template 11: Simplify x = (-b ± √discriminant)/(2a) where discriminant = 48
- Template 12: Simplify x = (-b ± √discriminant)/(2a) where discriminant = 50

## Answer Complexity Constraints

- a: between 1 and 5
- b, c: between 1 and 8
- For non-perfect square discriminants: discriminant ≤ 20

## Answer Format

- Display all answers in exact form
- Discriminant values: integers
- Solutions: x = (-3 ± √17)/4
- Number of roots: "2 real solutions", "1 real solution", "0 real solutions"

## Common Mistake Patterns

- Forgetting negative sign on b
- Forgetting to multiply by 4 in discriminant
- Not simplifying radicals
