# quadratics_graphing_and_application

Test script: `python3 tests/test_quadratics_graphing_and_application.py <template_number>`

## Templates (10 total)

### Find x-intercepts via radicals
- Template 1: Find x-intercepts of y = x² - n (n perfect square)
- Template 2: Find x-intercepts of y = x² - n (n ≤ 20, non-perfect square)
- Template 3: Find x-intercepts of y = x² + bx + c (discriminant perfect square)
- Template 4: Find x-intercepts of y = ax² + bx + c (discriminant perfect square)

### Estimate radical roots
- Template 5: √n is between what two integers? (n not perfect square, n ≤ 50)
- Template 6: Approximate √n to 1 decimal place (n ≤ 20)

### Link discriminant to graph type
- Template 7: If b² - 4ac > 0, how many x-intercepts does the graph have?
- Template 8: If b² - 4ac = 0, how many x-intercepts does the graph have?
- Template 9: If b² - 4ac < 0, how many x-intercepts does the graph have?
- Template 10: For y = ax² + bx + c, if discriminant = 49, how many x-intercepts?

## Answer Complexity Constraints

- n: between 1 and 50
- a: between 1 and 5
- b, c: between 1 and 8
- For non-perfect square discriminants: discriminant ≤ 20

## Answer Format

- x-intercepts: x = ±√5 or x = -1 or x = 3
- Between integers: "between 5 and 6"
- Approximations: "approximately 4.5"
- Number of intercepts: "2 x-intercepts", "1 x-intercept", "0 x-intercepts"

## Common Mistake Patterns

- Not recognizing discriminant determines number of x-intercepts
- Forgetting ± when solving for x-intercepts
