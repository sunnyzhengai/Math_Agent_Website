 Errors Encountered During Implementation

  1. Data Structure Mismatch

  - Error: Functions expected tuples (x1, x2) but received dictionaries with solution info
  - Location: All template functions calling solve_by_completing_square(), generate_wrong_answers(), and generate_choices()
  - Cause: Changed return type of solve_by_completing_square() without updating all call sites
  - Fix: Bulk find-replace to update function signatures across all 24 templates

  2. Incorrect Solution Formatting (Integer Solutions)

  - Error: Equation x² + 6x + 5 = 0 displayed as x = -3 or x = 1 instead of correct x = -5 or x = -1
  - Location: format_solution_pair() function, specifically in the perfect square discriminant branch
  - Cause: Wrong formula in format_exact_solution() - used numerator + sqrt_disc but passed wrong numerator value
  - Fix: Rewrote rational solution formatting to directly compute (-b ± sqrt(disc))/(2a) and simplify

  3. Solution Ordering Issues

  - Error: Solutions displayed in wrong order (larger value first instead of smaller)
  - Location: format_solution_pair() return statement
  - Cause: Inconsistent handling of which solution is x1 vs x2
  - Fix: Added explicit float value comparison and use_flipped flag to ensure consistent ordering

  4. Duplicate Wrong Answers

  - Error: Multiple choice showing identical options (e.g., "A) x = 1 or x = 1", "B) x = -1 or x = -1", "C) x = -1 or x = -1")
  - Location: generate_wrong_answers() function
  - Cause: Common mistake patterns (sign flip, forget ±) sometimes produce identical results
  - Status: Partially addressed but still occurs in edge cases (perfect square discriminants, zero solutions, etc.)

  5. Formatting Artifacts

  - Error: Displayed "+5" instead of "5", "-0" instead of "0"
  - Location: String building in wrong answer generation
  - Cause: Simple string manipulation errors when flipping signs
  - Status: Still present in some wrong answers

  6. Division by Zero in GCD

  - Error: Potential gcd(0, n) calls
  - Location: format_solution_pair() when simplifying radicals
  - Cause: Edge case when b=0 in equations
  - Fix: Added if g == 0: g = 1 guard

  7. Wrong Answer Generation Complexity

  - Error: Wrong answers sometimes don't represent realistic student mistakes
  - Location: generate_wrong_answers() - overly complex logic trying to manipulate exact form strings
  - Cause: Attempted to generate wrong answers by string manipulation instead of mathematical transformations
  - Status: Works but could be simplified

  8. Incomplete Template Function Updates

  - Error: After changing core function signatures, 23 out of 24 templates still used old signatures
  - Location: Templates 2-24
  - Cause: Updated template_1 manually but forgot to apply same changes to others
  - Fix: Used regex bulk replacement script

    9. Incomplete Discriminant Validation

  - Error: Templates with "always positive" discriminants (templates 3, 4, 7, 8, 11, 13, 15, 19, 21, 22, 24) had no validation to ensure simple discriminants
  - Location: Templates where discriminant formula b² + 4c or similar is always ≥ 0
  - Cause: Comment said "always positive, so always real solutions" - developer stopped there and didn't add simplicity check
  - Example: Template 4 generated x² - 8x - 6 = 0 with discriminant = 88, producing √22 (too complex)
  - Fix: Added while not is_simple_discriminant(disc): loops to these templates
  - Status: Fixed for templates 3, 4, 7; remaining templates 8, 11, 13, 15, 19, 21, 22, 24 need same fix

  10. Overly Broad Coefficient Ranges

  - Error: Original SPEC allowed coefficients that produced extremely complex answers
  - Location: All templates - coefficient ranges were too large (a: 2-12, b/c/d: 1-10)
  - Cause: SPEC didn't consider the downstream effect on discriminant size
  - Example: Large coefficients like a=12, b=5, c=9, d=4 → discriminant = 597
  - Fix: Reduced ranges in SPEC.md and implementation:
    - a: 2-12 → 2-5 (templates 9-24)
    - b/c/d: 1-10 → 1-8 (templates 1-8)
    - b/c/d: 1-10 → 1-6 (templates 9-24)
  - Status: Completed

  11. Missing Pedagogical Constraints in SPEC

  - Error: Original SPEC focused on mathematical correctness (real solutions) but not pedagogical appropriateness (student-friendly complexity)
  - Location: SPEC.md
  - Cause: Requirements didn't specify answer complexity level for Honors Algebra 2
  - Impact: Questions were technically correct but too difficult/tedious for learning completing the square
  - Fix: Added explicit constraint: "discriminant ≤ 20 for non-perfect squares"
  - Status: SPEC updated, implementation partially complete

  Summary for SPEC_ERRORS_TO_AVOID.md:

  These three errors represent a class of Requirements Incompleteness issues:
  - Real solutions ≠ Simple solutions
  - "Always positive" ≠ "Simple enough for students"
  - Mathematical correctness ≠ Pedagogical appropriateness

  Lesson: When building educational tools, SPEC must include both technical constraints (real solutions) AND user-experience constraints (simple answers appropriate for skill level).

  12. Missing Variable Updates in Validation Loops

  - Error: Derived variables (like new_b, new_c, new_a) calculated before while loop but not recalculated inside loop after regenerating base coefficients
  - Location: Templates with multiple derived variables (templates 18, 20, 21, 22, possibly others)
  - Cause: Forgot to recalculate derived variables inside the validation while loop
  - Impact: solve_by_completing_square() called with stale values, leading to None return or incorrect solutions
  - Example: Template 20 calculates new_b = 2*b before loop, but when b changes in loop, new_b isn't updated
  - Fix: Recalculate all derived variables inside the while loop
  - Status: Identified by evals, needs fixing

  13. Coefficient of 1 Display Formatting

  - Error: Coefficient of 1 displayed as "1x" or "1x²" instead of "x" or "x²"
  - Location: All 24 templates - equation string formatting
  - Cause: Direct string interpolation without checking if coefficient is 1
  - Impact: Unprofessional display, violates mathematical convention
  - Example: "5x² + 1x - 1 = 6 + 1x" instead of "5x² + x - 1 = 6 + x"
  - Fix: Created format_coefficient(coef, var) helper function that omits coefficient when it equals 1
  - Status: Fixed

  Recommended SPEC_ERRORS_TO_AVOID.md Sections

  1. Type Contract Violations - Changing function return types without updating all callers
  2. Mathematical Correctness - Formula implementation errors in solution calculation
  3. Edge Cases - Division by zero, identical solutions, zero coefficients
  4. Display Formatting - Sign artifacts, redundant symbols in string output
  5. Data Consistency - Solution ordering, deterministic choice generation
  6. Test Coverage Gaps - Not testing all 24 templates after core changes

  Recommended EVALS

  1. Correctness Eval: For each template (1-24), verify computed solutions match expected values
    - Test case: x² + 6x + 5 = 0 should give x = -5 or x = -1
  2. Format Eval: Verify exact form display (no decimals)
    - Integer: x = 3 not x = 3.0
    - Fraction: x = -7/2 not x = -3.5
    - Radical: x = 3 - √11 not x = -0.32
  3. Choice Uniqueness Eval: Verify all 4 multiple choice options are distinct
  4. Sign Formatting Eval: No "+5" or "-0" artifacts in output
  5. Discriminant Coverage Eval: Test templates with:
    - Perfect square discriminant (integer/fraction solutions)
    - Non-perfect square (radical solutions)
    - Zero discriminant (repeated root)
  6. Integration Eval: Run all 24 templates successfully without errors
