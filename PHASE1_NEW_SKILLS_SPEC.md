# Phase 1: Six New Algebra 1 Skills - Detailed Specifications

## Overview
This document specifies 6 new skills to add to the Quadratic Mastery platform, expanding from 9 to 15 total Algebra 1 skills.

---

## Skill 1: Transformations

### Metadata
- **Skill ID:** `quad.transformations`
- **Name:** Quadratic Transformations
- **Description:** Identify and apply transformations (shifts, stretches, reflections) to parabolas
- **Prerequisites:** `quad.graph.vertex`
- **Estimated Time:** 25 minutes

### Learning Objectives
- Identify vertical and horizontal shifts from equations
- Determine if a parabola is stretched or compressed
- Recognize reflections across the x-axis
- Predict transformations from comparing two equations

### Sample Questions

**Easy:**
```
How does y = (x - 3)² + 5 compare to y = x²?
A. Shifted right 3, up 5
B. Shifted left 3, up 5
C. Shifted right 3, down 5
D. Shifted left 3, down 5
```

**Medium:**
```
The graph of y = 2(x + 4)² - 3 is obtained from y = x² by:
A. Vertical stretch by 2, shift left 4, down 3
B. Vertical compression by 2, shift right 4, down 3
C. Vertical stretch by 2, shift right 4, up 3
D. Horizontal stretch by 2, shift left 4, down 3
```

**Hard:**
```
Which transformation converts y = x² to y = -0.5(x - 7)² + 12?
A. Reflect, compress by 0.5, shift right 7, up 12
B. Reflect, stretch by 0.5, shift left 7, up 12
C. Compress by 0.5, shift right 7, down 12
D. Reflect, compress by 0.5, shift right 7, down 12
```

### Parameterization
- **h** (horizontal shift): -15 to 15 (easy), -30 to 30 (medium), -50 to 50 (hard)
- **k** (vertical shift): -15 to 15 (easy), -30 to 30 (medium), -50 to 50 (hard)
- **a** (stretch/compression): 0.25, 0.5, 2, 3, 4 (easy: ±2, ±3; medium: ±0.5, ±4; hard: ±0.25, ±5)
- **negative** (reflection): true/false

### Distractors
- **Easy:** Wrong sign on h (left/right confusion), wrong sign on k
- **Medium:** Confuse stretch/compression, wrong transformation type
- **Hard:** Multiple errors, confuse horizontal/vertical stretch, wrong order of operations

---

## Skill 2: Form Conversions

### Metadata
- **Skill ID:** `quad.form.conversions`
- **Name:** Converting Quadratic Forms
- **Description:** Convert between standard form, vertex form, and factored form
- **Prerequisites:** `quad.complete.square`, `quad.solve.by_factoring`
- **Estimated Time:** 30 minutes

### Learning Objectives
- Convert standard form (ax² + bx + c) to vertex form
- Convert vertex form to standard form
- Convert factored form to standard form
- Identify equivalent expressions in different forms

### Sample Questions

**Easy:**
```
Convert y = (x - 2)² + 3 to standard form.
A. y = x² - 4x + 7
B. y = x² + 4x + 7
C. y = x² - 4x - 1
D. y = x² + 4x - 1
```

**Medium:**
```
Which is the vertex form of y = 2x² - 12x + 5?
A. y = 2(x - 3)² - 13
B. y = 2(x - 3)² + 5
C. y = 2(x + 3)² - 13
D. y = 2(x - 6)² + 5
```

**Hard:**
```
Convert y = -3(x + 5)(x - 2) to vertex form.
A. y = -3(x - 1.5)² + 18.75
B. y = -3(x + 1.5)² - 18.75
C. y = -3(x - 1.5)² - 73.5
D. y = -3(x + 1.5)² + 73.5
```

### Parameterization
- **Standard → Vertex:** a (1 to 4), b (-20 to 20), c (-20 to 20)
- **Vertex → Standard:** a (1 to 4), h (-15 to 15), k (-15 to 15)
- **Factored → Standard:** a (1 to 4), r1 (-10 to 10), r2 (-10 to 10)

### Distractors
- **Easy:** Arithmetic errors in expansion, wrong signs
- **Medium:** Forget to complete the square correctly, wrong vertex calculation
- **Hard:** Multiple transformation errors, coefficient errors

---

## Skill 3: Solving Inequalities

### Metadata
- **Skill ID:** `quad.solve.inequalities`
- **Name:** Quadratic Inequalities
- **Description:** Solve quadratic inequalities and express solutions using interval notation
- **Prerequisites:** `quad.solve.by_factoring`, `quad.roots.factored`
- **Estimated Time:** 28 minutes

### Learning Objectives
- Solve inequalities like x² + 5x + 6 > 0
- Determine solution intervals using test points
- Express solutions in interval notation
- Connect graphical and algebraic representations

### Sample Questions

**Easy:**
```
Solve: (x - 2)(x + 3) > 0
A. x < -3 or x > 2
B. -3 < x < 2
C. x < 2
D. x > -3
```

**Medium:**
```
Solve: x² - 5x - 14 ≤ 0
A. -2 ≤ x ≤ 7
B. x ≤ -2 or x ≥ 7
C. -7 ≤ x ≤ 2
D. x ≤ -7 or x ≥ 2
```

**Hard:**
```
Solve: 2x² + 3x - 20 < 0
A. -4 < x < 2.5
B. x < -4 or x > 2.5
C. -2.5 < x < 4
D. x < -2.5 or x > 4
```

### Parameterization
- **Roots:** r1, r2 (factorizable quadratics)
- **Inequality type:** <, >, ≤, ≥
- **Leading coefficient:** 1 (easy), 2-4 (medium/hard)

### Distractors
- **Easy:** Wrong inequality direction, endpoints wrong
- **Medium:** Forget to reverse inequality when multiplying by negative
- **Hard:** Critical points wrong, test point errors

---

## Skill 4: Max/Min Applications

### Metadata
- **Skill ID:** `quad.applications.maxmin`
- **Name:** Optimization with Quadratics
- **Description:** Solve real-world max/min problems using quadratic functions
- **Prerequisites:** `quad.graph.vertex`, `quad.standard.vertex`
- **Estimated Time:** 30 minutes

### Learning Objectives
- Find maximum/minimum values from quadratic models
- Solve area optimization problems
- Solve projectile motion problems
- Interpret vertex in context of word problems

### Sample Questions

**Easy:**
```
A ball is thrown upward with height h(t) = -16t² + 48t + 4 (feet).
What is the maximum height?
A. 40 feet
B. 52 feet
C. 64 feet
D. 48 feet
```

**Medium:**
```
A farmer has 100 meters of fence to enclose a rectangular area against a barn.
If the barn forms one side (no fence needed), what is the maximum area?
A. 1250 m²
B. 2500 m²
C. 1000 m²
D. 2000 m²
```

**Hard:**
```
A company's profit is modeled by P(x) = -2x² + 200x - 3000, where x is
units sold (in hundreds). How many units maximize profit?
A. 5000 units
B. 50 units
C. 100 units
D. 10000 units
```

### Parameterization
- **Projectile:** a = -16 or -4.9, v0 (initial velocity), h0 (initial height)
- **Area:** perimeter or one side given
- **Revenue/Profit:** quadratic coefficients based on realistic scenarios

### Distractors
- **Easy:** Find vertex but report wrong coordinate (x instead of y)
- **Medium:** Arithmetic errors, setup errors
- **Hard:** Units confusion, interpretation errors

---

## Skill 5: Domain & Range

### Metadata
- **Skill ID:** `quad.domain.range`
- **Name:** Domain and Range of Quadratics
- **Description:** Determine domain and range of quadratic functions
- **Prerequisites:** `quad.graph.vertex`
- **Estimated Time:** 20 minutes

### Learning Objectives
- Identify domain of quadratic functions (always all real numbers)
- Find range using vertex and direction of opening
- Express domain and range in interval notation
- Connect to graphical representation

### Sample Questions

**Easy:**
```
What is the range of y = (x - 3)² + 5?
A. [5, ∞)
B. (-∞, 5]
C. (-∞, ∞)
D. [3, ∞)
```

**Medium:**
```
Find the range of y = -2(x + 4)² + 7.
A. (-∞, 7]
B. [7, ∞)
C. (-∞, -4]
D. [-4, ∞)
```

**Hard:**
```
What is the range of y = 3x² - 12x + 8?
A. [-4, ∞)
B. [8, ∞)
C. (-∞, 8]
D. (-∞, -4]
```

### Parameterization
- **a:** positive or negative (determines opening direction)
- **h, k:** vertex coordinates
- Domain is always (-∞, ∞) for unrestricted quadratics

### Distractors
- **Easy:** Confuse domain and range
- **Medium:** Wrong inequality direction based on opening
- **Hard:** Need to find vertex first, arithmetic errors

---

## Skill 6: Number of Solutions

### Metadata
- **Skill ID:** `quad.solutions.count`
- **Name:** Counting Solutions/Roots
- **Description:** Determine number of real solutions using discriminant or graph
- **Prerequisites:** `quad.discriminant.analysis`
- **Estimated Time:** 22 minutes

### Learning Objectives
- Use discriminant to determine number of real roots
- Count x-intercepts from a graph
- Distinguish between real and complex solutions
- Connect discriminant sign to number of solutions

### Sample Questions

**Easy:**
```
How many real solutions does x² - 6x + 9 = 0 have?
A. 0 solutions
B. 1 solution
C. 2 solutions
D. 3 solutions
```

**Medium:**
```
How many x-intercepts does y = 2x² - 5x + 7 have?
A. 0
B. 1
C. 2
D. 3
```

**Hard:**
```
For what value of k does x² + kx + 25 = 0 have exactly one real solution?
A. k = 10
B. k = ±10
C. k = 5
D. k = ±5
```

### Parameterization
- **Discriminant cases:**
  - b² - 4ac > 0 (2 solutions)
  - b² - 4ac = 0 (1 solution)
  - b² - 4ac < 0 (0 real solutions)

### Distractors
- **Easy:** Off by one error
- **Medium:** Calculate discriminant incorrectly
- **Hard:** Algebraic manipulation errors when solving for parameter

---

## Implementation Priority

1. **Transformations** - Most visual, builds intuition
2. **Domain & Range** - Quick win, reinforces vertex concept
3. **Number of Solutions** - Extends discriminant skill
4. **Form Conversions** - Core algebraic skill
5. **Solving Inequalities** - Important but more complex
6. **Max/Min Applications** - Most advanced, needs previous skills

---

## Frontend Integration

### New Skill Definitions (SkillExplorer.tsx)
```typescript
'quad.transformations': {
  name: 'Quadratic Transformations',
  description: 'Identify shifts, stretches, and reflections',
  prerequisites: ['quad.graph.vertex'],
  estimated_time: 25
},
'quad.form.conversions': {
  name: 'Converting Forms',
  description: 'Convert between standard, vertex, and factored forms',
  prerequisites: ['quad.complete.square', 'quad.solve.by_factoring'],
  estimated_time: 30
},
// ... etc
```

### Prerequisites Logic
- Transformations unlocks after mastering vertex from graph
- Form conversions requires completing square AND factoring proficiency
- Inequalities requires factoring skills
- Applications requires vertex identification
- Domain/Range builds on vertex
- Solutions count extends discriminant

---

## Questions for Review

1. **Content Accuracy:** Do these align with what your daughter is learning in Algebra 1?
2. **Difficulty Levels:** Are easy/medium/hard examples appropriate?
3. **Prerequisites:** Do the prerequisite chains make sense?
4. **Priority Order:** Should we implement in a different order?
5. **Missing Topics:** Any critical skills I've missed?
6. **Word Problems:** Need more real-world contexts for applications?

---

## Next Steps After Approval

1. Implement backend templates in `engine/templates.py`
2. Create parameterized generators in `engine/parameters.py`
3. Update frontend skill definitions
4. Test each skill thoroughly
5. Deploy to production
6. Your daughter tests and provides feedback

**Please review and provide feedback on these specifications!**
