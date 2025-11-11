# Julia's Current Curriculum Skills - Immediate Implementation

## Overview
Based on Julia's homework from 11/10/2025, these 5 skills match what she's learning RIGHT NOW in Honors Compacted Algebra 2.

---

## Skill 1: Completing the Square (PRIMARY FOCUS)

### Metadata
- **Skill ID:** `quad.complete.square.solve`
- **Name:** Solving by Completing the Square
- **Description:** Solve quadratic equations by completing the square method
- **Prerequisites:** `quad.complete.square` (if exists, else standalone)
- **Estimated Time:** 30 minutes

### Learning Objectives
- Rearrange equations to collect variables on one side
- Divide by leading coefficient when a ≠ 1
- Add (b/2)² to both sides to create perfect square
- Factor as perfect square trinomial
- Solve using square root property

### Sample Questions

**Easy:**
```
Solve by completing the square: x² + 6x + 5 = 0
A. x = -1 or x = -5
B. x = 1 or x = 5
C. x = -3 ± 2
D. x = 3 ± 2
```

**Medium:**
```
Solve by completing the square: x² - 8x + 3 = 0
A. x = 4 ± √13
B. x = 4 ± √19
C. x = -4 ± √13
D. x = 8 ± √13
```

**Hard:**
```
Solve by completing the square: 2x² + 12x - 10 = 0
A. x = -3 ± √14
B. x = -6 ± √46
C. x = -3 ± 4
D. x = 3 ± √14
```

**Applied (like homework #11):**
```
Solve by completing the square: x² - 5x = 12 - 2x
A. x = 3/2 ± √57/2
B. x = -3/2 ± √57/2
C. x = 3 ± √57
D. x = 1.5 ± 3.75
```

### Parameterization
- **Easy:** a = 1, b even (2,4,6,8), c small (-10 to 10), ensures real rational solutions
- **Medium:** a = 1, b even, irrational solutions (discriminant > 0 but not perfect square)
- **Hard:** a = 2, 3, or 4 (requiring division step), b even, mixed solution types
- **Applied:** Needs rearranging first (terms on both sides)

### Distractors
- **Easy:** Wrong sign on solutions, forgot ± symbol, arithmetic errors
- **Medium:** (b/2)² calculated wrong, forgot to add to both sides, square root errors
- **Hard:** Didn't divide by a, wrong order of operations, sign errors after dividing by a

---

## Skill 2: Square Root Property

### Metadata
- **Skill ID:** `quad.solve.square_root_property`
- **Name:** Solving with Square Root Property
- **Description:** Solve equations in the form (x - h)² = k using square roots
- **Prerequisites:** None
- **Estimated Time:** 20 minutes

### Learning Objectives
- Recognize equations already in perfect square form
- Apply square root to both sides
- Remember ± symbol for two solutions
- Simplify radical answers
- Handle cases where k < 0 (no real solutions)

### Sample Questions

**Easy:**
```
Solve: (x - 3)² = 16
A. x = 7 or x = -1
B. x = 7 or x = 1
C. x = -7 or x = 1
D. x = 19
```

**Medium:**
```
Solve: (x + 5)² = 12
A. x = -5 ± 2√3
B. x = 5 ± 2√3
C. x = -5 ± √12
D. x = -5 ± 6
```

**Hard:**
```
Solve: 3(x - 2)² = 48
A. x = 2 ± 4
B. x = 2 ± √16
C. x = -2 ± 4
D. x = 2 ± 6.93
```

**No Real Solutions:**
```
Solve: (x + 1)² = -25
A. x = -1 ± 5
B. x = 1 ± 5
C. No real solutions
D. x = -26 or x = 24
```

### Parameterization
- **h** (horizontal shift): -10 to 10
- **k** (perfect squares): 1, 4, 9, 16, 25, 36, 49, 64, 81, 100 (easy)
- **k** (non-perfect): 2, 3, 5, 6, 7, 8, 10, 11, 12, 15, 18, 20 (medium)
- **k** (negative): -4, -9, -16, -25 (hard - no real solutions)
- **coefficient**: 1 (easy), 2-4 (medium), 5+ (hard)

### Distractors
- **Easy:** Forgot ± symbol, wrong arithmetic
- **Medium:** Didn't simplify radical, wrong sign on h
- **Hard:** Didn't divide by coefficient first, calculation errors
- **No solutions:** Tried to take square root of negative

---

## Skill 3: Solving by Factoring (Review)

### Metadata
- **Skill ID:** `quad.solve.factoring`
- **Name:** Solving by Factoring
- **Description:** Solve quadratic equations by factoring and using zero product property
- **Prerequisites:** `quad.factoring.trinomials`
- **Estimated Time:** 25 minutes

### Learning Objectives
- Rearrange equation to standard form (= 0)
- Factor the quadratic expression
- Apply zero product property
- Solve for all x-values

### Sample Questions

**Easy:**
```
Solve by factoring: x² + 7x + 12 = 0
A. x = -3 or x = -4
B. x = 3 or x = 4
C. x = -3 or x = 4
D. x = 3 or x = -4
```

**Medium:**
```
Solve by factoring: 2x² - 8x - 10 = 0
A. x = 5 or x = -1
B. x = -5 or x = 1
C. x = 5 or x = 1
D. x = -5 or x = -1
```

**Hard:**
```
Solve by factoring: 5x² + 32x - 70 = -7x
A. x = -5.6 or x = 2.5
B. x = -7 or x = 2
C. x = 7 or x = -2
D. x = -2 or x = 5
```

### Parameterization
- **Easy:** a = 1, factorable with small integers, already in standard form
- **Medium:** a = 2, 3, or 4, GCF to factor out first
- **Hard:** Not in standard form (rearranging required), larger numbers

### Distractors
- **Easy:** Wrong signs on factors, forgot to set = 0
- **Medium:** Didn't factor out GCF first, arithmetic errors
- **Hard:** Didn't rearrange properly, wrong factorization

---

## Skill 4: Factoring Review

### Metadata
- **Skill ID:** `quad.factoring.review`
- **Name:** Factoring Quadratics
- **Description:** Factor quadratic expressions (trinomials, difference of squares, GCF)
- **Prerequisites:** None
- **Estimated Time:** 25 minutes

### Learning Objectives
- Factor trinomials (x² + bx + c)
- Factor difference of squares (x² - k²)
- Factor out GCF
- Factor perfect square trinomials

### Sample Questions

**Easy - Simple Trinomial:**
```
Factor: x² + 7x + 12
A. (x + 3)(x + 4)
B. (x - 3)(x - 4)
C. (x + 2)(x + 6)
D. (x - 2)(x - 6)
```

**Easy - Difference of Squares:**
```
Factor: x² - 9
A. (x - 3)(x - 3)
B. (x + 3)(x + 3)
C. (x - 9)(x + 1)
D. (x - 3)(x + 3)
```

**Medium - GCF First:**
```
Factor: x² - 40x
A. x(x - 40)
B. (x - 20)(x - 2)
C. x(x + 40)
D. Cannot be factored
```

**Hard - Trinomial with Negatives:**
```
Factor: x² - 3x - 10
A. (x - 5)(x + 2)
B. (x + 5)(x - 2)
C. (x - 10)(x + 1)
D. (x + 10)(x - 1)
```

### Parameterization
- **Trinomials:** b and c range from -20 to 20
- **Difference of squares:** Perfect squares 4, 9, 16, 25, 36, 49, 64, 81, 100
- **GCF:** Multiples of x, 2x, 3x, etc.
- **Perfect squares:** (x + k)² patterns

### Distractors
- Sign errors on factors
- Wrong factor pairs
- Forgot GCF
- Incomplete factorization

---

## Skill 5: Number of Solutions (Graphical)

### Metadata
- **Skill ID:** `quad.solutions.graphical`
- **Name:** Number of Real Solutions from Graph
- **Description:** Determine if a quadratic has 0, 1, or 2 real solutions from its graph
- **Prerequisites:** None
- **Estimated Time:** 15 minutes

### Learning Objectives
- Count x-intercepts from parabola graph
- Connect x-intercepts to real solutions
- Identify 0 solutions (doesn't cross x-axis)
- Identify 1 solution (touches x-axis at vertex)
- Identify 2 solutions (crosses x-axis twice)

### Sample Questions

**Easy:**
```
[Graph showing parabola crossing x-axis at two points]
How many real solutions does this quadratic equation have?
A. 0
B. 1
C. 2
D. 3
```

**Medium:**
```
[Graph showing parabola with vertex on x-axis]
How many real solutions does this quadratic equation have?
A. 0
B. 1
C. 2
D. Infinitely many
```

**Hard:**
```
[Graph showing parabola entirely above x-axis, opening upward]
How many real solutions does this quadratic equation have?
A. 0
B. 1
C. 2
D. Cannot determine from graph
```

### Parameterization
- **Two solutions:** Vertex below x-axis (opens up) or above (opens down)
- **One solution:** Vertex exactly on x-axis
- **Zero solutions:** Vertex above x-axis (opens up) or below (opens down)

### Distractors
- Confusing y-intercept with number of solutions
- Counting vertex as two solutions
- Wrong for no real solutions case

---

## Implementation Plan

### Priority Order (Based on Homework):
1. **Completing the Square** - HIGHEST PRIORITY (main current lesson)
2. **Square Root Property** - Prerequisite and standalone skill
3. **Factoring Review** - Foundation skill
4. **Solving by Factoring** - Builds on factoring
5. **Number of Solutions (Graphical)** - Conceptual understanding

### Next Steps:
1. Update TypeScript types with 5 new skill IDs
2. Create templates in `engine/templates.py` for each skill
3. Create parameterized generators in `engine/parameters.py`
4. Update frontend skill definitions in `SkillExplorer.tsx`
5. Test locally with Julia's actual homework problems
6. Deploy to production

### Notes:
- These skills directly match Julia's current homework
- Questions mirror the exact style and difficulty from her worksheets
- Completing the square is the clear focus and should have most templates
- After Julia masters these, we can return to the Phase 1 expansion plan
