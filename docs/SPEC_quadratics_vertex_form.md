# quadratics_vertex_form

Test script: `python3 tests/test_quadratics_vertex_form.py <template_number>`

## Templates (8 total)

### Create perfect square trinomials
- Template 1: Complete the square: x² + bx + ___ = (x + ___)² (b even, b > 0)
- Template 2: Complete the square: x² - bx + ___ = (x - ___)² (b even, b > 0)
- Template 3: What value completes the square: x² + bx (b > 0)
- Template 4: What value completes the square: x² - bx (b > 0)

### Rewrite equations in vertex form
- Template 5: y = x² + bx + c → y = (x + h)² + k (b even, b > 0, c > 0)
- Template 6: y = x² - bx + c → y = (x - h)² + k (b even, b > 0, c > 0)
- Template 7: y = x² + bx - c → y = (x + h)² + k (b even, b > 0, c > 0)
- Template 8: y = x² - bx - c → y = (x - h)² + k (b even, b > 0, c > 0)

## Answer Complexity Constraints

- b must be even (to ensure b/2 is an integer)
- b: between 2 and 10
- c: between 1 and 8

## Answer Format

- Display all answers in exact form
- Perfect squares: (x + 3)²
- Vertex form: y = (x - 2)² - 5 (note: using "- 5" instead of "+ -5")
- Values: b/2 = 3, (b/2)² = 9

## Common Mistake Patterns

- Using b instead of (b/2)²
- Sign errors when converting to vertex form
