### Phase 1: Create 24 question templates
## ME
in tests/ folder: create a test script test_quadratic_equations_by_completing_the_square.py. when we run the test with a parameter number, it should generate a template with that number: e.g. python3 test_quadratic_equations-by_completing_the_square.py 9 should return a question that looks like ax^2 + bx + c = x^2 + d (b > 0, c > 0, d > 0) with its 4 multiple choices.

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

in code/ folder: create a python script quadratic_equations_by_completing_the_square.py
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
  1. code/quadratic_equations_by_completing_the_square.py
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

  2. tests/test_quadratic_equations_by_completing_the_square.py
    - Imports from code/quadratic_equations_by_completing_the_square.py
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
  $ python3 tests/test_quadratic_equations_by_completing_the_square.py 9

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

