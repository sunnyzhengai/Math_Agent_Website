### Phase 1: Create 24 question templates for "quadratic equations by completing the square"
## ME
in tests/ folder: create a test script test_quadratics_completing_the_square.py. when we run the test with a parameter number, it should generate a template with that number: e.g. python3 test_quadratic_equations-by_completing_the_square.py 9 should return a question that looks like ax^2 + bx + c = x^2 + d (b > 0, c > 0, d > 0) with its 4 multiple choices.

# Example 𝑥^2 − 6𝑥 + 4 = 0 
- create test template 1: x^2 + bx + c = 0 (b > 0, c > 0)
- create test template 2: x^2 - bx + c = 0 (b > 0, c > 0)
- create test template 3: x^2 + bx - c = 0 (b > 0, c > 0)
- create test template 4: x^2 - bx - c = 0 (b > 0, c > 0)

# Example 𝑥^2 − 5 = 2 − 2𝑥
- create test template 5: x^2 + c = d + bx (b > 0, c > 0, d > 0) 
- create test template 6: x^2 + c = d - bx (b > 0, c > 0, d > 0) 
- create test template 8: x^2 - c = d + bx (b > 0, c > 0, d > 0) 
- create test template 7: x^2 - c = d - bx (b > 0, c > 0, d > 0) 

# Example 5𝑥^2 + 32𝑥 + 2 = 𝑥^2 − 78
- create test template 9: ax^2 + bx + c = x^2 + d (b > 0, c > 0, d > 0)
- create test template 10: ax^2 - bx + c = x^2 + d (b > 0, c > 0, d > 0)
- create test template 11: ax^2 + bx - c = x^2 + d (b > 0, c > 0, d > 0)
- create test template 12: ax^2 + bx + c = x^2 - d (b > 0, c > 0, d > 0)
- create test template 13: ax^2 - bx - c = x^2 + d (b > 0, c > 0, d > 0)
- create test template 14: ax^2 + bx - c = x^2 - d (b > 0, c > 0, d > 0)
- create test template 15: ax^2 - bx - c = x^2 + d (b > 0, c > 0, d > 0)
- create test template 16: ax^2 - bx - c = x^2 - d (b > 0, c > 0, d > 0)
- create test template 17: ax^2 + bx + c = d + bx (b > 0, c > 0, d > 0) 
- create test template 18: ax^2 - bx + c = d + bx (b > 0, c > 0, d > 0) 
- create test template 19: ax^2 + bx - c = d + bx (b > 0, c > 0, d > 0) 
- create test template 20: ax^2 + bx + c = d - bx (b > 0, c > 0, d > 0) 
- create test template 21: ax^2 - bx - c = d + bx (b > 0, c > 0, d > 0) 
- create test template 22: ax^2 + bx - c = d - bx (b > 0, c > 0, d > 0) 
- create test template 23: ax^2 - bx + c = d - bx (b > 0, c > 0, d > 0) 
- create test template 24: ax^2 - bx - c = d - bx (b > 0, c > 0, d > 0) 

in code/ folder: create a python script quadratics_completing_the_square.py
- create functions that will return the 24 templates as listed above. when called with a parameter, it should return an equation of that template.
- coefficients a, b, c, d should all be positive numbers
- Answer Complexity Constraints (to ensure student-friendly problems):
  * Coefficient 'a' (templates 9-24): between 2 and 5 (reduced from 2-12)
  * Coefficients b, c, d (templates 1-8): between 1 and 8 (reduced from 1-10)
  * Coefficients b, c, d (templates 9-24): between 1 and 6 (reduced from 1-10)
  * For irrational solutions (non-perfect-square discriminant): discriminant must be ≤ 20
  * This ensures radicals are simple (√2, √3, √5, √6, √7, √10, √11, √13, √14, √15, √17, √19, √20)
  * Answers will be: integers, simple fractions, or radicals with small numbers under the square root
- Answer Format:
  * Display all answers in exact form (no decimals)
  * Integers: x = 3
  * Fractions: x = -7/2
  * Radicals: x = 3 - √5 or x = (-2 + √7)/3

## Claude
 Detailed Implementation Plan:

  Files to create:
  1. code/quadratics_completing_the_square.py
    - 24 functions: template_1() through template_24()
    - Each returns: (equation_string, correct_letter, [choice_A, choice_B, choice_C, choice_D])
    - Helper functions:
      * solve_by_completing_square(a, b, c) - returns dict with 'solutions', 'discriminant', 'a', 'b'
      * format_solution_pair(a, b, discriminant) - returns (x1_str, x2_str, x1_float, x2_float) in exact form
      * generate_wrong_answers(solution_info) - generates 3 common mistake answers
      * is_simple_discriminant(disc) - checks if disc is perfect square OR disc ≤ 20
    - Constraints:
      * Ensure discriminant ≥ 0 for real solutions
      * Ensure discriminant ≤ 20 for non-perfect-square (simple radicals only)
      * Coefficient ranges as specified above
    - Answer formatting:
      * No decimals - all answers in exact form
      * Integers: x = -5
      * Fractions: x = -7/2 (simplified)
      * Radicals: x = 3 - √5 or x = (-2 + √7)/3 (simplified)

  2. tests/test_quadratics_completing_the_square.py
    - Imports from code/quadratics_completing_the_square.py
    - Accepts template number (1-24) as command line argument
    - Calls appropriate template function
    - Displays formatted question + 4 choices
    - Shows correct answer for debugging

  3. tests/evals.py (optional but recommended)
    - Comprehensive evaluation suite testing all error categories
    - 9 evals covering: correctness, formatting, uniqueness, complexity, etc.
    - Run to verify no regressions after changes

  Common mistake patterns for wrong answers:
  - Sign error when completing square: flip sign of b
  - Forgetting ± when taking square root: only positive solution
  - Mixed sign error: flip sign of one solution only
  - Arithmetic errors in calculation

  Example output:
  $ python3 tests/test_quadratics_completing_the_square.py 9

  ============================================================
  Solve by completing the square:

    3x² + 1x + 4 = x² + 5

  Multiple Choice Options:
    A) x = -1 or x = 1/2
    B) x = -1 or x = -1/2
    C) x = -1/2 or x = 1
    D) x = 5/4 or x = 5/4
  ============================================================

  [Debug] Correct answer: A

### Phase 2: Radical Foundations
Create question templates for radical foundations (exponents, understanding, simplifying, operations)

## ME
in tests/ folder: create a test script test_radicals_exponents_refresher.py. when we run the test with a parameter number, it should generate a template with that number: e.g. python3 test_radicals_exponents_refresher.py 1 should return a question with 4 multiple choices.

# Exponent Rules
- create test template 1: Evaluate a^m × a^n (product rule)
- create test template 2: Evaluate a^m / a^n (quotient rule)
- create test template 3: Simplify a^(-n) (negative exponent)
- create test template 4: Evaluate (a^m)^n (power rule)
- create test template 5: Is n a perfect square? (true/false recognition)

in code/ folder: create a python script radicals_exponents_refresher.py
- create functions that will return the 5 templates as listed above
- coefficients a, m, n should all be positive numbers
- Answer Complexity Constraints:
  * Bases a: between 2 and 5
  * Exponents m, n: between 2 and 6
  * Perfect squares: {4, 9, 16, 25, 36, 49, 64, 81, 100}
  * Non-perfect squares for recognition: {6, 8, 10, 12, 15, 18, 20, 24}
- Answer Format:
  * Numeric answers: integers only (e.g., 128, 27)
  * Algebraic answers: x^3, x^(-2), 1/x^2
  * True/false: "Yes" or "No"

in tests/ folder: create a test script test_radicals_understanding_radicals.py. when we run the test with a parameter number, it should generate a template with that number: e.g. python3 test_radicals_understanding_radicals.py 1 should return a question with 4 multiple choices.

# Basic Radical Understanding
- create test template 1: What is √n? (n is perfect square)
- create test template 2: Solve x² = n (n is perfect square)
- create test template 3: Rewrite ⁿ√(x^m) as a power (convert to rational exponent)
- create test template 4: √n is between what two integers? (n is non-perfect square)

in code/ folder: create a python script radicals_understanding_radicals.py
- create functions that will return the 4 templates as listed above
- coefficients n, m should all be positive numbers
- Answer Complexity Constraints:
  * Perfect squares n: {4, 9, 16, 25, 36, 49, 64, 81, 100}
  * Non-perfect squares n: between 2 and 50
  * Root indices: 2, 3 (square root, cube root)
  * Powers m: between 1 and 6
- Answer Format:
  * Numeric: integers (e.g., 4, 5)
  * Solutions: x = ±4
  * Rational exponents: x^(2/3)
  * Between integers: "between 5 and 6"

in tests/ folder: create a test script test_radicals_simplifying_radicals.py. when we run the test with a parameter number, it should generate a template with that number: e.g. python3 test_radicals_simplifying_radicals.py 1 should return a question with 4 multiple choices.

# Simplifying Radicals
- create test template 1: Simplify √n (n has perfect square factor, e.g., √50 = 5√2)
- create test template 2: Simplify ³√(n·x^m) (cube root with variables)
- create test template 3: Multiply and simplify √a × √b
- create test template 4: Divide and simplify √a / √b

in code/ folder: create a python script radicals_simplifying_radicals.py
- create functions that will return the 4 templates as listed above
- coefficients a, b, n, m should all be positive numbers
- Answer Complexity Constraints:
  * For √n: n between 8 and 100, must have perfect square factor
  * For cube roots: n·x^m where n ∈ {8, 27, 54, 128} and m ≤ 6
  * For multiplication: a, b between 2 and 12
  * For division: a/b results in perfect square or simple radical
- Answer Format:
  * Simplified radicals: 5√2, 2√3
  * With variables: 2x√(3x)
  * Simplified expressions: √6, 4

in tests/ folder: create a test script test_radicals_operations_with_radicals.py. when we run the test with a parameter number, it should generate a template with that number: e.g. python3 test_radicals_operations_with_radicals.py 1 should return a question with 4 multiple choices.

# Operations with Radicals
- create test template 1: Add like radicals: a√n + b√n
- create test template 2: Multiply binomials with radicals: (a + √n)(a - √n) [difference of squares]
- create test template 3: Rationalize denominator: a/√n
- create test template 4: Rationalize denominator: a/(b + √n) [conjugate method]

in code/ folder: create a python script radicals_operations_with_radicals.py
- create functions that will return the 4 templates as listed above
- coefficients a, b, n should all be positive numbers
- Answer Complexity Constraints:
  * Coefficients a, b: between 1 and 8
  * Radicals n: between 2 and 20
  * For difference of squares: use small values (a ≤ 5, n ≤ 10)
  * For conjugates: b ≤ 5, n ≤ 10
- Answer Format:
  * Combined radicals: 7√2
  * Difference of squares: a² - n (integer result)
  * Rationalized: (a√n)/n or simplified form
  * Conjugate result: (ab - a√n)/(b² - n) simplified

## Claude
Detailed Implementation Plan:

For each of the 4 skills (17 templates total):

1. **test_radicals_exponents_refresher.py** (5 templates)
   - Imports from code/radicals_exponents_refresher.py
   - Displays formatted question with 4 choices
   - Shows correct answer for debugging

2. **test_radicals_understanding_radicals.py** (4 templates)
   - Imports from code/radicals_understanding_radicals.py
   - Displays formatted question with 4 choices
   - Shows correct answer for debugging

3. **test_radicals_simplifying_radicals.py** (4 templates)
   - Imports from code/radicals_simplifying_radicals.py
   - Displays formatted question with 4 choices
   - Shows correct answer for debugging

4. **test_radicals_operations_with_radicals.py** (4 templates)
   - Imports from code/radicals_operations_with_radicals.py
   - Displays formatted question with 4 choices
   - Shows correct answer for debugging

Common mistake patterns for wrong answers:
- Exponents: adding instead of multiplying, subtracting instead of dividing
- Radicals: not simplifying completely, sign errors, forgetting ±
- Simplification: leaving perfect square factors under radical
- Rationalization: multiplying by wrong conjugate, not simplifying fully

Example output:
$ python3 tests/test_radicals_exponents_refresher.py 1

============================================================
Evaluate:

  2³ × 2⁴

Multiple Choice Options:
  A) 2⁷
  B) 2¹²
  C) 128
  D) 4⁷
============================================================

[Debug] Correct answer: C

### Phase 3: Stage 5 - Solving Equations Using Radicals
## ME
in tests/ folder: create a test script test_quadratics_solving_with_square_roots.py. when we run the test with a parameter number, it should generate a template with that number: e.g. python3 test_quadratics_solving_with_square_roots.py 1 should return a question with 4 multiple choices.

# Solve with square roots
- create test template 1: x² = n (where n is a perfect square, e.g., 49, 64, 81)
- create test template 2: x² = n (where n is NOT a perfect square, e.g., 50, 32, 20)

# Solve two-step radical equations
- create test template 3: (x - a)² = n (perfect square, a > 0, n > 0)
- create test template 4: (x + a)² = n (perfect square, a > 0, n > 0)
- create test template 5: (x - a)² = n (non-perfect square, a > 0, n ≤ 20)
- create test template 6: (x + a)² = n (non-perfect square, a > 0, n ≤ 20)

# Check for extraneous roots
- create test template 7: √(x + a) = x - b (where one solution is extraneous)
- create test template 8: √(x - a) = x - b (where one solution is extraneous)

in code/ folder: create a python script quadratics_solving_with_square_roots.py
- create functions that will return the 8 templates as listed above
- coefficients a, b, n should all be positive numbers
- Answer Complexity Constraints:
  * For perfect squares: n ∈ {4, 9, 16, 25, 36, 49, 64, 81, 100}
  * For non-perfect squares: n ≤ 20
  * Values a, b: between 1 and 8
- Answer Format:
  * Display all answers in exact form (no decimals)
  * Integers: x = ±7
  * Radicals: x = 3 ± √5
  * Multiple solutions: x = 8 or x = -2
  * Extraneous roots: x = 2 (note: x = -1 is extraneous)

### Phase 4: Stage 6 - Completing the Square for Vertex Form
## ME
in tests/ folder: create a test script test_quadratics_vertex_form.py. when we run the test with a parameter number, it should generate a template with that number: e.g. python3 test_quadratics_vertex_form.py 1 should return a question with 4 multiple choices.

# Create perfect square trinomials
- create test template 1: x² + bx + ? = (x + ?)² (b even, b > 0)
- create test template 2: x² - bx + ? = (x - ?)² (b even, b > 0)
- create test template 3: What value completes the square: x² + bx (b > 0)
- create test template 4: What value completes the square: x² - bx (b > 0)

# Rewrite equations in vertex form
- create test template 5: y = x² + bx + c → y = (x + h)² + k (b even, b > 0, c > 0)
- create test template 6: y = x² - bx + c → y = (x - h)² + k (b even, b > 0, c > 0)
- create test template 7: y = x² + bx - c → y = (x + h)² + k (b even, b > 0, c > 0)
- create test template 8: y = x² - bx - c → y = (x - h)² + k (b even, b > 0, c > 0)

in code/ folder: create a python script quadratics_vertex_form.py
- create functions that will return the 8 templates as listed above
- coefficients b, c should all be positive numbers
- Answer Complexity Constraints:
  * b must be even (to ensure b/2 is an integer)
  * b: between 2 and 10
  * c: between 1 and 8
- Answer Format:
  * Display all answers in exact form
  * Perfect squares: (x + 3)²
  * Vertex form: y = (x - 2)² + 5
  * Values: b/2 = 3, (b/2)² = 9

### Phase 5: Stage 7 - Quadratic Formula and Discriminant
## ME
in tests/ folder: create a test script test_quadratics_quadratic_formula.py. when we run the test with a parameter number, it should generate a template with that number: e.g. python3 test_quadratics_quadratic_formula.py 1 should return a question with 4 multiple choices.

# Apply quadratic formula
- create test template 1: Solve ax² + bx + c = 0 using quadratic formula (discriminant is perfect square)
- create test template 2: Solve ax² - bx + c = 0 using quadratic formula (discriminant is perfect square)
- create test template 3: Solve ax² + bx - c = 0 using quadratic formula (discriminant is perfect square)
- create test template 4: Solve ax² + bx + c = 0 using quadratic formula (discriminant ≤ 20, non-perfect)

# Compute discriminant
- create test template 5: What is the discriminant of ax² + bx + c = 0?
- create test template 6: What is the discriminant of ax² - bx - c = 0?

# Interpret discriminant
- create test template 7: Given discriminant = 25, how many real solutions?
- create test template 8: Given discriminant = 0, how many real solutions?
- create test template 9: Given discriminant = -5, how many real solutions?
- create test template 10: For ax² + bx + c = 0, what discriminant means 2 real solutions?

# Simplify radical in solution
- create test template 11: Simplify x = (-b ± √discriminant)/(2a) where discriminant = 48
- create test template 12: Simplify x = (-b ± √discriminant)/(2a) where discriminant = 50

in code/ folder: create a python script quadratics_quadratic_formula.py
- create functions that will return the 12 templates as listed above
- coefficients a, b, c should all be positive numbers
- Answer Complexity Constraints:
  * a: between 1 and 5
  * b, c: between 1 and 8
  * For non-perfect square discriminants: discriminant ≤ 20
- Answer Format:
  * Display all answers in exact form
  * Discriminant values: integers
  * Solutions: x = (-3 ± √17)/4
  * Number of roots: "2 real solutions", "1 real solution", "2 complex solutions"

### Phase 6: Stage 8 - Application and Graphing
## ME
in tests/ folder: create a test script test_quadratics_graphing_and_application.py. when we run the test with a parameter number, it should generate a template with that number: e.g. python3 test_quadratics_graphing_and_application.py 1 should return a question with 4 multiple choices.

# Find x-intercepts via radicals
- create test template 1: Find x-intercepts of y = x² - n (n perfect square)
- create test template 2: Find x-intercepts of y = x² - n (n ≤ 20, non-perfect square)
- create test template 3: Find x-intercepts of y = x² + bx + c (discriminant perfect square)
- create test template 4: Find x-intercepts of y = ax² + bx + c (discriminant perfect square)

# Estimate radical roots
- create test template 5: √n is between what two integers? (n not perfect square, n ≤ 50)
- create test template 6: Approximate √n to 1 decimal place (n ≤ 20)

# Link discriminant to graph type
- create test template 7: If b² - 4ac > 0, how many x-intercepts does the graph have?
- create test template 8: If b² - 4ac = 0, how many x-intercepts does the graph have?
- create test template 9: If b² - 4ac < 0, how many x-intercepts does the graph have?
- create test template 10: For y = ax² + bx + c, if discriminant = 49, how many x-intercepts?

in code/ folder: create a python script quadratics_graphing_and_application.py
- create functions that will return the 10 templates as listed above
- coefficients a, b, c should all be positive numbers
- Answer Complexity Constraints:
  * n: between 1 and 50
  * a: between 1 and 5
  * b, c: between 1 and 8
  * For non-perfect square discriminants: discriminant ≤ 20
- Answer Format:
  * x-intercepts: x = ±√5 or x = -1 or x = 3
  * Between integers: "between 5 and 6"
  * Approximations: "approximately 4.5"
  * Number of intercepts: "2 x-intercepts", "1 x-intercept", "0 x-intercepts"


