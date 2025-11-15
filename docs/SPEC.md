# Math Practice Platform - Skill Specifications

## radicals_exponents_refresher

Test script: `python3 tests/test_radicals_exponents_refresher.py <template_number>`

### Templates (5 total)

- Template 1: Evaluate a^m × a^n (product rule)
- Template 2: Evaluate a^m / a^n (quotient rule)
- Template 3: Simplify a^(-n) (negative exponent)
- Template 4: Evaluate (a^m)^n (power rule)
- Template 5: Is n a perfect square? (true/false recognition)

### Answer Complexity Constraints

- Bases a: between 2 and 5
- Exponents m, n: between 2 and 6
- Perfect squares: {4, 9, 16, 25, 36, 49, 64, 81, 100}
- Non-perfect squares for recognition: {6, 8, 10, 12, 15, 18, 20, 24}

### Answer Format

- Numeric answers: integers only (e.g., 128, 27)
- Algebraic answers: x^3, x^(-2), 1/x^2
- True/false: "Yes" or "No"

### Common Mistake Patterns

- Adding instead of multiplying exponents
- Subtracting instead of dividing exponents

---

## radicals_understanding_radicals

Test script: `python3 tests/test_radicals_understanding_radicals.py <template_number>`

### Templates (4 total)

- Template 1: What is √n? (n is perfect square)
- Template 2: Solve x² = n (n is perfect square)
- Template 3: Rewrite ⁿ√(x^m) as a power (convert to rational exponent)
- Template 4: √n is between what two integers? (n is non-perfect square)

### Answer Complexity Constraints

- Perfect squares n: {4, 9, 16, 25, 36, 49, 64, 81, 100}
- Non-perfect squares n: between 2 and 50
- Root indices: 2, 3 (square root, cube root)
- Powers m: between 1 and 6

### Answer Format

- Numeric: integers (e.g., 4, 5)
- Solutions: x = ±4
- Rational exponents: x^(2/3)
- Between integers: "between 5 and 6"

### Common Mistake Patterns

- Forgetting ± when solving x² = n
- Sign errors
- Not simplifying completely

---

## radicals_simplifying_radicals

Test script: `python3 tests/test_radicals_simplifying_radicals.py <template_number>`

### Templates (4 total)

- Template 1: Simplify √n (n has perfect square factor, e.g., √50 = 5√2)
- Template 2: Simplify ³√(n·x^m) (cube root with variables)
- Template 3: Multiply and simplify √a × √b
- Template 4: Divide and simplify √a / √b

### Answer Complexity Constraints

- For √n: n between 8 and 100, must have perfect square factor
- For cube roots: n·x^m where n ∈ {8, 27, 54, 128} and m ≤ 6
- For multiplication: a, b between 2 and 12
- For division: a/b results in perfect square or simple radical

### Answer Format

- Simplified radicals: 5√2, 2√3
- With variables: 2x√(3x)
- Simplified expressions: √6, 4

### Common Mistake Patterns

- Leaving perfect square factors under radical
- Not simplifying completely

---

## radicals_operations_with_radicals

Test script: `python3 tests/test_radicals_operations_with_radicals.py <template_number>`

### Templates (4 total)

- Template 1: Add like radicals: a√n + b√n
- Template 2: Multiply binomials with radicals: (a + √n)(a - √n) [difference of squares]
- Template 3: Rationalize denominator: a/√n
- Template 4: Rationalize denominator: a/(b + √n) [conjugate method]

### Answer Complexity Constraints

- Coefficients a, b: between 1 and 8
- Radicals n: between 2 and 20
- For difference of squares: use small values (a ≤ 5, n ≤ 10)
- For conjugates: b ≤ 5, n ≤ 10

### Answer Format

- Combined radicals: 7√2
- Difference of squares: a² - n (integer result)
- Rationalized: (a√n)/n or simplified form
- Conjugate result: (ab - a√n)/(b² - n) simplified

### Common Mistake Patterns

- Not simplifying fully after rationalization
- Multiplying by wrong conjugate

---

## quadratics_completing_the_square

Test script: `python3 tests/test_quadratics_completing_the_square.py <template_number>`

### Templates (24 total)

#### Standard form: x^2 + bx + c = 0
- Template 1: x^2 + bx + c = 0 (b > 0, c > 0)
- Template 2: x^2 - bx + c = 0 (b > 0, c > 0)
- Template 3: x^2 + bx - c = 0 (b > 0, c > 0)
- Template 4: x^2 - bx - c = 0 (b > 0, c > 0)

#### Rearrangement form: x^2 + c = d ± bx
- Template 5: x^2 + c = d + bx (b > 0, c > 0, d > 0)
- Template 6: x^2 + c = d - bx (b > 0, c > 0, d > 0)
- Template 7: x^2 - c = d - bx (b > 0, c > 0, d > 0)
- Template 8: x^2 - c = d + bx (b > 0, c > 0, d > 0)

#### With leading coefficient: ax^2 + bx + c = x^2 ± d
- Template 9: ax^2 + bx + c = x^2 + d (b > 0, c > 0, d > 0)
- Template 10: ax^2 - bx + c = x^2 + d (b > 0, c > 0, d > 0)
- Template 11: ax^2 + bx - c = x^2 + d (b > 0, c > 0, d > 0)
- Template 12: ax^2 + bx + c = x^2 - d (b > 0, c > 0, d > 0)
- Template 13: ax^2 - bx - c = x^2 + d (b > 0, c > 0, d > 0)
- Template 14: ax^2 + bx - c = x^2 - d (b > 0, c > 0, d > 0)
- Template 15: ax^2 - bx - c = x^2 + d (b > 0, c > 0, d > 0)
- Template 16: ax^2 - bx - c = x^2 - d (b > 0, c > 0, d > 0)

#### With rearrangement: ax^2 + bx + c = d ± bx
- Template 17: ax^2 + bx + c = d + bx (b > 0, c > 0, d > 0)
- Template 18: ax^2 - bx + c = d + bx (b > 0, c > 0, d > 0)
- Template 19: ax^2 + bx - c = d + bx (b > 0, c > 0, d > 0)
- Template 20: ax^2 + bx + c = d - bx (b > 0, c > 0, d > 0)
- Template 21: ax^2 - bx - c = d + bx (b > 0, c > 0, d > 0)
- Template 22: ax^2 + bx - c = d - bx (b > 0, c > 0, d > 0)
- Template 23: ax^2 - bx + c = d - bx (b > 0, c > 0, d > 0)
- Template 24: ax^2 - bx - c = d - bx (b > 0, c > 0, d > 0)

### Answer Complexity Constraints

- Coefficient 'a' (templates 9-24): between 2 and 5
- Coefficients b, c, d (templates 1-8): between 1 and 8
- Coefficients b, c, d (templates 9-24): between 1 and 6
- For irrational solutions (non-perfect-square discriminant): discriminant must be ≤ 20
- This ensures radicals are simple (√2, √3, √5, √6, √7, √10, √11, √13, √14, √15, √17, √19, √20)

### Answer Format

- Display all answers in exact form (no decimals)
- Integers: x = 3
- Fractions: x = -7/2
- Radicals: x = 3 - √5 or x = (-2 + √7)/3

### Common Mistake Patterns

- Sign error when completing square: flip sign of b
- Forgetting ± when taking square root: only positive solution
- Mixed sign error: flip sign of one solution only
- Arithmetic errors in calculation

---

## quadratics_solving_with_square_roots

Test script: `python3 tests/test_quadratics_solving_with_square_roots.py <template_number>`

### Templates (8 total)

#### Solve with square roots
- Template 1: x² = n (where n is a perfect square, e.g., 49, 64, 81)
- Template 2: x² = n (where n is NOT a perfect square, e.g., 50, 32, 20)

#### Solve two-step radical equations
- Template 3: (x - a)² = n (perfect square, a > 0, n > 0)
- Template 4: (x + a)² = n (perfect square, a > 0, n > 0)
- Template 5: (x - a)² = n (non-perfect square, a > 0, n ≤ 20)
- Template 6: (x + a)² = n (non-perfect square, a > 0, n ≤ 20)

#### Check for extraneous roots
- Template 7: √(x + a) = x - b (where one solution is extraneous)
- Template 8: √(x - a) = x - b (where one solution is extraneous)

### Answer Complexity Constraints

- For perfect squares: n ∈ {4, 9, 16, 25, 36, 49, 64, 81, 100}
- For non-perfect squares: n ≤ 20
- Values a, b: between 1 and 8

### Answer Format

- Display all answers in exact form (no decimals)
- Integers: x = ±7
- Radicals: x = 3 ± √5
- Multiple solutions: x = 8 or x = -2
- Extraneous roots: x = 2 (note: x = -1 is extraneous)

### Common Mistake Patterns

- Forgetting ± when taking square root
- Not checking for extraneous solutions

---

## quadratics_vertex_form

Test script: `python3 tests/test_quadratics_vertex_form.py <template_number>`

### Templates (8 total)

#### Create perfect square trinomials
- Template 1: Complete the square: x² + bx + ___ = (x + ___)² (b even, b > 0)
- Template 2: Complete the square: x² - bx + ___ = (x - ___)² (b even, b > 0)
- Template 3: What value completes the square: x² + bx (b > 0)
- Template 4: What value completes the square: x² - bx (b > 0)

#### Rewrite equations in vertex form
- Template 5: y = x² + bx + c → y = (x + h)² + k (b even, b > 0, c > 0)
- Template 6: y = x² - bx + c → y = (x - h)² + k (b even, b > 0, c > 0)
- Template 7: y = x² + bx - c → y = (x + h)² + k (b even, b > 0, c > 0)
- Template 8: y = x² - bx - c → y = (x - h)² + k (b even, b > 0, c > 0)

### Answer Complexity Constraints

- b must be even (to ensure b/2 is an integer)
- b: between 2 and 10
- c: between 1 and 8

### Answer Format

- Display all answers in exact form
- Perfect squares: (x + 3)²
- Vertex form: y = (x - 2)² - 5 (note: using "- 5" instead of "+ -5")
- Values: b/2 = 3, (b/2)² = 9

### Common Mistake Patterns

- Using b instead of (b/2)²
- Sign errors when converting to vertex form

---

## quadratics_quadratic_formula

Test script: `python3 tests/test_quadratics_quadratic_formula.py <template_number>`

### Templates (12 total)

#### Apply quadratic formula
- Template 1: Solve ax² + bx + c = 0 using quadratic formula (discriminant is perfect square)
- Template 2: Solve ax² - bx + c = 0 using quadratic formula (discriminant is perfect square)
- Template 3: Solve ax² + bx - c = 0 using quadratic formula (discriminant is perfect square)
- Template 4: Solve ax² + bx + c = 0 using quadratic formula (discriminant ≤ 20, non-perfect)

#### Compute discriminant
- Template 5: What is the discriminant of ax² + bx + c = 0?
- Template 6: What is the discriminant of ax² - bx - c = 0?

#### Interpret discriminant
- Template 7: Given discriminant = 25, how many real solutions?
- Template 8: Given discriminant = 0, how many real solutions?
- Template 9: Given discriminant = -5, how many real solutions?
- Template 10: For ax² + bx + c = 0, what discriminant means 2 real solutions?

#### Simplify radical in solution
- Template 11: Simplify x = (-b ± √discriminant)/(2a) where discriminant = 48
- Template 12: Simplify x = (-b ± √discriminant)/(2a) where discriminant = 50

### Answer Complexity Constraints

- a: between 1 and 5
- b, c: between 1 and 8
- For non-perfect square discriminants: discriminant ≤ 20

### Answer Format

- Display all answers in exact form
- Discriminant values: integers
- Solutions: x = (-3 ± √17)/4
- Number of roots: "2 real solutions", "1 real solution", "0 real solutions"

### Common Mistake Patterns

- Forgetting negative sign on b
- Forgetting to multiply by 4 in discriminant
- Not simplifying radicals

---

## quadratics_graphing_and_application

Test script: `python3 tests/test_quadratics_graphing_and_application.py <template_number>`

### Templates (10 total)

#### Find x-intercepts via radicals
- Template 1: Find x-intercepts of y = x² - n (n perfect square)
- Template 2: Find x-intercepts of y = x² - n (n ≤ 20, non-perfect square)
- Template 3: Find x-intercepts of y = x² + bx + c (discriminant perfect square)
- Template 4: Find x-intercepts of y = ax² + bx + c (discriminant perfect square)

#### Estimate radical roots
- Template 5: √n is between what two integers? (n not perfect square, n ≤ 50)
- Template 6: Approximate √n to 1 decimal place (n ≤ 20)

#### Link discriminant to graph type
- Template 7: If b² - 4ac > 0, how many x-intercepts does the graph have?
- Template 8: If b² - 4ac = 0, how many x-intercepts does the graph have?
- Template 9: If b² - 4ac < 0, how many x-intercepts does the graph have?
- Template 10: For y = ax² + bx + c, if discriminant = 49, how many x-intercepts?

### Answer Complexity Constraints

- n: between 1 and 50
- a: between 1 and 5
- b, c: between 1 and 8
- For non-perfect square discriminants: discriminant ≤ 20

### Answer Format

- x-intercepts: x = ±√5 or x = -1 or x = 3
- Between integers: "between 5 and 6"
- Approximations: "approximately 4.5"
- Number of intercepts: "2 x-intercepts", "1 x-intercept", "0 x-intercepts"

### Common Mistake Patterns

- Not recognizing discriminant determines number of x-intercepts
- Forgetting ± when solving for x-intercepts
