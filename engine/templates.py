"""
Template engine for generating math question items.

See engine/CONTRACTS.md for the full specification.
"""

import random
import uuid
from typing import Optional


# Skill templates: skill_id -> difficulty -> list of questions
SKILL_TEMPLATES = {
    "quad.graph.vertex": {
        "easy": [
            {
                "stem": "For y = (x - 3)^2 + 2, what is the vertex?",
                "choices": ["(3, 2)", "(-3, 2)", "(3, -2)", "(2, 3)"],
                "solution": 0,
                "rationale": "The vertex form is y = a(x - h)^2 + k with vertex (h, k).",
            },
            {
                "stem": "What is the vertex of y = (x + 1)^2 - 5?",
                "choices": ["(-1, -5)", "(1, -5)", "(-1, 5)", "(1, 5)"],
                "solution": 0,
                "rationale": "From the vertex form, h = -1 and k = -5.",
            },
        ],
        "medium": [
            {
                "stem": "Find the vertex of y = 2(x - 1)^2 + 3.",
                "choices": ["(1, 3)", "(1, -3)", "(-1, 3)", "(-1, -3)"],
                "solution": 0,
                "rationale": "The vertex form y = a(x - h)^2 + k has vertex (h, k).",
            },
        ],
        "hard": [
            {
                "stem": "The vertex of y = 2x^2 - 8x + 5 is at what point?",
                "choices": ["(2, -3)", "(2, 3)", "(-2, 5)", "(1, -1)"],
                "solution": 0,
                "rationale": "Complete the square: y = 2(x - 2)^2 - 3.",
            },
            {
                "stem": "Find the vertex of y = -0.5(x + 3)^2 - 4.",
                "choices": ["(-3, -4)", "(3, -4)", "(-3, 4)", "(0.5, -4)"],
                "solution": 0,
                "rationale": "From vertex form y = a(x - h)^2 + k, vertex is (h, k) = (-3, -4).",
            },
            {
                "stem": "What is the vertex of y = 3(x - 0.5)^2 + 2.25?",
                "choices": ["(0.5, 2.25)", "(-0.5, 2.25)", "(3, 2.25)", "(0.5, -2.25)"],
                "solution": 0,
                "rationale": "Vertex form gives h = 0.5, k = 2.25, so vertex is (0.5, 2.25).",
            },
        ],
        "applied": [
            {
                "stem": "A ball's height is h(t) = -16(t - 2)^2 + 64. At what time is max height?",
                "choices": ["t = 2", "t = 4", "t = 0", "t = 8"],
                "solution": 0,
                "rationale": "The vertex occurs at t = 2, the maximum height.",
            },
            {
                "stem": "A rocket's height is y = -5(x - 4)^2 + 80. What is the vertex?",
                "choices": ["(4, 80)", "(-4, 80)", "(5, 80)", "(4, -80)"],
                "solution": 0,
                "rationale": "From vertex form, the vertex is (4, 80).",
            },
            {
                "stem": "Profit is P(x) = -2(x - 15)^2 + 450. What x gives max profit?",
                "choices": ["x = 15", "x = -15", "x = 2", "x = 450"],
                "solution": 0,
                "rationale": "Maximum occurs at the vertex x = 15.",
            },
        ],
    },
    "quad.standard.vertex": {
        "easy": [
            {
                "stem": "Find the vertex of y = x^2 - 4x + 1.",
                "choices": ["(2, -3)", "(2, 3)", "(-2, -3)", "(-2, 3)"],
                "solution": 0,
                "rationale": "For y = ax^2 + bx + c, vertex is (h,k) with h = -b/(2a); k = f(h). Here a=1, b=-4, c=1 ⇒ h=2, k=-3.",
            },
            {
                "stem": "Find the vertex of y = x^2 + 6x + 5.",
                "choices": ["(-3, -4)", "(-3, 4)", "(3, -4)", "(-6, 5)"],
                "solution": 0,
                "rationale": "a=1, b=6, c=5 ⇒ h=-6/(2)= -3; k = 1·9 + 6·(-3) + 5 = -4.",
            },
            {
                "stem": "Find the vertex of y = -x^2 + 4x + 1.",
                "choices": ["(2, 5)", "(2, -5)", "(-2, 5)", "(1, 4)"],
                "solution": 0,
                "rationale": "a=-1, b=4, c=1 ⇒ h = -4/(2·-1)=2; k = -4 + 8 + 1 = 5.",
            },
        ],
        "medium": [
            {
                "stem": "Find the vertex of y = 2x^2 - 8x + 3.",
                "choices": ["(2, -5)", "(2, 5)", "(-2, -5)", "(4, -5)"],
                "solution": 0,
                "rationale": "a=2, b=-8, c=3 ⇒ h= -(-8)/(4)=2; k = 2·4 + (-8)·2 + 3 = -5.",
            },
            {
                "stem": "Find the vertex of y = -3x^2 - 6x + 1.",
                "choices": ["(-1, 4)", "(-1, -4)", "(1, 4)", "(-2, 4)"],
                "solution": 0,
                "rationale": "a=-3, b=-6 ⇒ h= -(-6)/(2·-3)= -1; k = -3·1 + (-6)·(-1) + 1 = 4.",
            },
        ],
        "hard": [
            {
                "stem": "Find the vertex of y = 5x^2 + 10x + 7.",
                "choices": ["(-1, 2)", "(-1, -2)", "(1, 2)", "(-2, 1)"],
                "solution": 0,
                "rationale": "a=5, b=10 ⇒ h = -10/(2·5) = -1; k = 5·1 + 10·(-1) + 7 = 2.",
            },
            {
                "stem": "Find the vertex of y = 0.5x^2 - 3x + 5.",
                "choices": ["(3, 0.5)", "(3, -4.5)", "(-3, 0.5)", "(1.5, 2.75)"],
                "solution": 1,
                "rationale": "a=0.5, b=-3 ⇒ h = -(-3)/(2·0.5) = 3; k = 0.5·9 - 3·3 + 5 = -4.5.",
            },
            {
                "stem": "Find the vertex of y = -2x^2 + 8x - 3.",
                "choices": ["(2, 5)", "(-2, 5)", "(2, -5)", "(4, -3)"],
                "solution": 0,
                "rationale": "a=-2, b=8 ⇒ h = -8/(2·-2) = 2; k = -2·4 + 8·2 - 3 = 5.",
            },
        ],
        "applied": [
            {
                "stem": "A projectile's height is h(t) = -16t^2 + 32t + 5. At what time is the maximum height reached?",
                "choices": ["t = 1", "t = 2", "t = 0", "t = 3"],
                "solution": 0,
                "rationale": "Vertex time is -b/(2a) with a=-16, b=32 ⇒ t=1.",
            },
            {
                "stem": "A company's profit is P(x) = -2x^2 + 12x + 1. For which x is profit maximized?",
                "choices": ["x = 3", "x = 2", "x = 4", "x = 6"],
                "solution": 0,
                "rationale": "a=-2, b=12 ⇒ x = -b/(2a) = -12/(-4) = 3.",
            },
        ],
    },
    "quad.roots.factored": {
        "easy": [
            {
                "stem": "Find the roots of y = (x - 2)(x + 5).",
                "choices": [
                    "x = -5 and x = 2",
                    "x = 5 and x = -2",
                    "x = -2 and x = 5",
                    "x = 2 and x = 5"
                ],
                "solution": 0,
                "rationale": "Set each factor to zero: x−2=0 ⇒ x=2; x+5=0 ⇒ x=−5.",
            },
            {
                "stem": "Find the roots of y = (x + 1)(x + 4).",
                "choices": [
                    "x = -1 and x = -4",
                    "x = 1 and x = 4",
                    "x = -1 and x = 4",
                    "x = 1 and x = -4"
                ],
                "solution": 0,
                "rationale": "x+1=0 ⇒ x=−1; x+4=0 ⇒ x=−4.",
            },
        ],
        "medium": [
            {
                "stem": "Find the roots of y = 2(x - 3)(x + 2).",
                "choices": [
                    "x = 3 and x = -2",
                    "x = -3 and x = 2",
                    "x = -3 and x = -2",
                    "x = 3 and x = 2"
                ],
                "solution": 0,
                "rationale": "Leading coefficient 2 doesn't change roots: x−3=0 ⇒ 3; x+2=0 ⇒ −2.",
            },
            {
                "stem": "Find the roots of y = -3(x + 1)(x + 5).",
                "choices": [
                    "x = -1 and x = -5",
                    "x = 1 and x = -5",
                    "x = -1 and x = 5",
                    "x = 1 and x = 5"
                ],
                "solution": 0,
                "rationale": "−3 scales vertically, roots from factors: x=−1, x=−5.",
            },
        ],
        "hard": [
            {
                "stem": "Find the distinct real roots of y = (x - 4)^2 (x + 1).",
                "choices": [
                    "x = 4 and x = -1",
                    "x = 4 only",
                    "x = -1 only",
                    "x = -4 and x = 1"
                ],
                "solution": 0,
                "rationale": "(x−4)^2 gives a repeated root at x=4; (x+1) ⇒ x=−1. Distinct roots: 4 and −1.",
            },
            {
                "stem": "Find the roots of y = 0.25(x + 2)(x - 8).",
                "choices": [
                    "x = -2 and x = 8",
                    "x = 2 and x = -8",
                    "x = -0.25 and x = 8",
                    "x = -2 and x = -8"
                ],
                "solution": 0,
                "rationale": "Leading coefficient 0.25 doesn't affect roots: x+2=0 ⇒ x=−2; x−8=0 ⇒ x=8.",
            },
            {
                "stem": "Find the distinct real roots of y = (x + 3)^3 (x - 1).",
                "choices": [
                    "x = -3 and x = 1",
                    "x = 3 and x = -1", 
                    "x = -3 only",
                    "x = 1 only"
                ],
                "solution": 0,
                "rationale": "(x+3)^3 gives repeated root at x=−3; (x−1) ⇒ x=1. Distinct roots: −3 and 1.",
            },
        ],
        "applied": [
            {
                "stem": "A ball's height is h(t) = -5(t - 1)(t - 6). When is it on the ground?",
                "choices": [
                    "t = 1 and t = 6",
                    "t = -1 and t = 6",
                    "t = 1 and t = -6",
                    "t = 0 and t = 6"
                ],
                "solution": 0,
                "rationale": "Ground at h(t)=0 ⇒ t−1=0 or t−6=0 ⇒ t=1,6.",
            },
        ],
    },
    "quad.solve.by_factoring": {
        "easy": [
            {
                "stem": "Solve by factoring: x^2 - 7x + 12 = 0.",
                "choices": [
                    "x = 3 and x = 4",
                    "x = -3 and x = -4",
                    "x = -3 and x = 4",
                    "x = 3 and x = -4"
                ],
                "solution": 0,
                "rationale": "x^2 - 7x + 12 = (x - 3)(x - 4)=0 ⇒ x=3,4.",
            },
            {
                "stem": "Solve by factoring: x^2 + 5x + 6 = 0.",
                "choices": [
                    "x = -2 and x = -3",
                    "x = 2 and x = 3",
                    "x = -2 and x = 3",
                    "x = 2 and x = -3"
                ],
                "solution": 0,
                "rationale": "x^2 + 5x + 6 = (x + 2)(x + 3)=0 ⇒ x=−2,−3.",
            },
        ],
        "medium": [
            {
                "stem": "Solve by factoring: 2x^2 + 7x + 3 = 0.",
                "choices": [
                    "x = -\tfrac{1}{2} and x = -3",
                    "x = \tfrac{1}{2} and x = 3",
                    "x = -\tfrac{3}{2} and x = -1",
                    "x = \tfrac{3}{2} and x = 1"
                ],
                "solution": 0,
                "rationale": "2x^2 + 7x + 3 = (2x + 1)(x + 3)=0 ⇒ x=−1/2,−3.",
            },
            {
                "stem": "Solve by factoring: 3x^2 - x - 10 = 0.",
                "choices": [
                    "x = 2 and x = -\tfrac{5}{3}",
                    "x = -2 and x = \tfrac{5}{3}",
                    "x = -2 and x = -\tfrac{5}{3}",
                    "x = 2 and x = \tfrac{5}{3}"
                ],
                "solution": 0,
                "rationale": "3x^2 − x − 10 = (3x + 5)(x − 2)=0 ⇒ x=2, −5/3.",
            },
        ],
        "hard": [
            {
                "stem": "Solve by factoring: 4x^2 - 12x + 9 = 0.",
                "choices": [
                    "x = \tfrac{3}{2}",
                    "x = -\tfrac{3}{2}",
                    "x = 3 and x = -3",
                    "No real solutions"
                ],
                "solution": 0,
                "rationale": "4x^2 − 12x + 9 = (2x − 3)^2=0 ⇒ x=3/2 (double root).",
            },
            {
                "stem": "Solve by factoring: 6x^2 + 13x + 6 = 0.",
                "choices": [
                    "x = -\tfrac{2}{3} and x = -\tfrac{3}{2}",
                    "x = \tfrac{2}{3} and x = \tfrac{3}{2}",
                    "x = -2 and x = -3",
                    "x = 2 and x = 3"
                ],
                "solution": 0,
                "rationale": "6x^2 + 13x + 6 = (3x + 2)(2x + 3)=0 ⇒ x=−2/3, −3/2.",
            },
            {
                "stem": "Solve by factoring: 9x^2 - 6x + 1 = 0.",
                "choices": [
                    "x = \tfrac{1}{3}",
                    "x = -\tfrac{1}{3}",
                    "x = 1 and x = -1",
                    "x = 3 and x = -3"
                ],
                "solution": 0,
                "rationale": "9x^2 − 6x + 1 = (3x − 1)^2=0 ⇒ x=1/3 (double root).",
            },
        ],
        "applied": [
            {
                "stem": "A rectangle has side lengths x and x+5 with area 24. Find the positive value of x.",
                "choices": [
                    "x = 3",
                    "x = 8",
                    "x = 4",
                    "x = 6"
                ],
                "solution": 0,
                "rationale": "x(x+5)=24 ⇒ x^2+5x−24=0 ⇒ (x+8)(x−3)=0 ⇒ x=−8 or 3. Positive length ⇒ x=3.",
            },
        ],
    },
    "quad.solve.by_formula": {
        "easy": [
            {
                "stem": "Solve using the quadratic formula: x^2 - 5x + 6 = 0.",
                "choices": [
                    "x = 2 and x = 3",
                    "x = -2 and x = -3",
                    "x = -2 and x = 3",
                    "x = 2 and x = -3"
                ],
                "solution": 0,
                "rationale": "a=1,b=−5,c=6 ⇒ Δ=b^2−4ac=25−24=1 ⇒ x=(5±1)/2 ⇒ 2,3.",
            },
            {
                "stem": "Solve using the quadratic formula: x^2 + 4x + 3 = 0.",
                "choices": [
                    "x = -1 and x = -3",
                    "x = 1 and x = 3",
                    "x = -1 and x = 3",
                    "x = 1 and x = -3"
                ],
                "solution": 0,
                "rationale": "a=1,b=4,c=3 ⇒ Δ=16−12=4 ⇒ x=(−4±2)/2 ⇒ −1,−3.",
            },
        ],
        "medium": [
            {
                "stem": "Solve using the quadratic formula: x^2 - 2x - 1 = 0.",
                "choices": [
                    "x = 1 + √2 and x = 1 - √2",
                    "x = 1 + √3 and x = 1 - √3",
                    "x = -1 + √2 and x = -1 - √2",
                    "x = 1 + 2√2 and x = 1 - 2√2"
                ],
                "solution": 0,
                "rationale": "a=1,b=−2,c=−1 ⇒ Δ=4+4=8 ⇒ x=(2±√8)/2=1±√2.",
            },
            {
                "stem": "Solve using the quadratic formula: 2x^2 + x - 3 = 0.",
                "choices": [
                    "x = 1 and x = -\\tfrac{3}{2}",
                    "x = -1 and x = \\tfrac{3}{2}",
                    "x = \\tfrac{1}{2} and x = -3",
                    "x = -\\tfrac{1}{2} and x = 3"
                ],
                "solution": 0,
                "rationale": "a=2,b=1,c=−3 ⇒ Δ=1+24=25 ⇒ x=(−1±5)/4 ⇒ 1, −3/2.",
            },
        ],
        "hard": [
            {
                "stem": "Solve using the quadratic formula: 3x^2 - 4x + 7 = 0.",
                "choices": [
                    "No real solutions",
                    "x = \\tfrac{2 + \\sqrt{5}}{3} and x = \\tfrac{2 - \\sqrt{5}}{3}",
                    "x = 1 + √2 and x = 1 - √2",
                    "x = -\\tfrac{7}{3} and x = 1"
                ],
                "solution": 0,
                "rationale": "a=3,b=−4,c=7 ⇒ Δ=b^2−4ac=16−84=−68<0 ⇒ no real roots.",
            },
            {
                "stem": "Solve using the quadratic formula: 2x^2 - 6x + 3 = 0.",
                "choices": [
                    "x = \\tfrac{3 + \\sqrt{3}}{2} and x = \\tfrac{3 - \\sqrt{3}}{2}",
                    "x = 3 + \\sqrt{3} and x = 3 - \\sqrt{3}",
                    "x = \\tfrac{6 + \\sqrt{12}}{4} and x = \\tfrac{6 - \\sqrt{12}}{4}",
                    "x = 1 and x = \\tfrac{3}{2}"
                ],
                "solution": 0,
                "rationale": "a=2,b=−6,c=3 ⇒ Δ=36−24=12 ⇒ x=(6±√12)/4=(6±2√3)/4=(3±√3)/2.",
            },
            {
                "stem": "Solve using the quadratic formula: x^2 + 2x - 8 = 0.",
                "choices": [
                    "x = 2 and x = -4",
                    "x = -2 and x = 4",
                    "x = 1 + \\sqrt{9} and x = 1 - \\sqrt{9}",
                    "x = -1 + 3 and x = -1 - 3"
                ],
                "solution": 0,
                "rationale": "a=1,b=2,c=−8 ⇒ Δ=4+32=36 ⇒ x=(−2±6)/2 ⇒ 2, −4.",
            },
        ],
        "applied": [
            {
                "stem": "A projectile's height is h(t) = -16t^2 + 32t + 48. When does it hit the ground (h=0)?",
                "choices": [
                    "t = 3 seconds",
                    "t = 1 second",
                    "t = 4 seconds",
                    "t = 6 seconds"
                ],
                "solution": 0,
                "rationale": "Set −16t^2+32t+48=0 ⇒ divide by −16 ⇒ t^2−2t−3=0 ⇒ t=3 or −1; time ≥0 ⇒ 3 s.",
            },
        ],
    },
    "quad.discriminant.analysis": {
        "easy": [
            {
                "stem": "For x^2 + 5x + 6 = 0, what is the discriminant?",
                "choices": ["1", "-1", "25", "36"],
                "solution": 0,
                "rationale": "Δ = b² - 4ac = 5² - 4(1)(6) = 25 - 24 = 1.",
            },
            {
                "stem": "For x^2 - 4x + 4 = 0, what is the discriminant?",
                "choices": ["0", "4", "16", "-8"],
                "solution": 0,
                "rationale": "Δ = b² - 4ac = (-4)² - 4(1)(4) = 16 - 16 = 0.",
            },
        ],
        "medium": [
            {
                "stem": "For 2x^2 + 3x - 1 = 0, what is the discriminant?",
                "choices": ["17", "9", "1", "-7"],
                "solution": 0,
                "rationale": "Δ = b² - 4ac = 3² - 4(2)(-1) = 9 + 8 = 17.",
            },
            {
                "stem": "Analyze the nature of roots for x^2 - 6x + 9 = 0.",
                "choices": [
                    "One repeated real root",
                    "Two distinct real roots",
                    "No real roots",
                    "Infinitely many roots"
                ],
                "solution": 0,
                "rationale": "Δ = (-6)² - 4(1)(9) = 36 - 36 = 0. Since Δ = 0, one repeated root.",
            },
        ],
        "hard": [
            {
                "stem": "For 3x^2 - 2x + 5 = 0, what can you conclude about the roots?",
                "choices": [
                    "No real roots",
                    "Two distinct real roots",
                    "One repeated real root",
                    "Two rational roots"
                ],
                "solution": 0,
                "rationale": "Δ = (-2)² - 4(3)(5) = 4 - 60 = -56 < 0. No real roots.",
            },
            {
                "stem": "For ax^2 + bx + c = 0 with Δ = 25, which statement is true?",
                "choices": [
                    "Two distinct real roots",
                    "One repeated real root", 
                    "No real roots",
                    "Cannot determine"
                ],
                "solution": 0,
                "rationale": "Since Δ = 25 > 0, there are two distinct real roots.",
            },
        ],
        "applied": [
            {
                "stem": "A ball's path is h(t) = -5t^2 + 20t + 1. Does it reach maximum height?",
                "choices": [
                    "Yes, at one specific time",
                    "Yes, at two different times",
                    "No, it only decreases",
                    "Cannot determine"
                ],
                "solution": 0,
                "rationale": "Since a = -5 < 0, parabola opens down, so one maximum exists.",
            },
        ],
    },
    "quad.intercepts": {
        "easy": [
            {
                "stem": "Find the y-intercept of y = x^2 + 3x + 2.",
                "choices": ["2", "-2", "3", "0"],
                "solution": 0,
                "rationale": "Y-intercept occurs at x = 0: y = 0² + 3(0) + 2 = 2.",
            },
            {
                "stem": "Find the x-intercepts of y = (x - 1)(x - 3).",
                "choices": [
                    "x = 1 and x = 3",
                    "x = -1 and x = -3", 
                    "x = 0 and x = 4",
                    "x = 2 only"
                ],
                "solution": 0,
                "rationale": "Set y = 0: (x-1)(x-3) = 0 ⇒ x = 1 or x = 3.",
            },
        ],
        "medium": [
            {
                "stem": "Find the x-intercepts of y = x^2 - 5x + 6.",
                "choices": [
                    "x = 2 and x = 3",
                    "x = -2 and x = -3",
                    "x = 1 and x = 6",
                    "x = 5 and x = 6"
                ],
                "solution": 0,
                "rationale": "Set y = 0: x² - 5x + 6 = 0 ⇒ (x-2)(x-3) = 0 ⇒ x = 2, 3.",
            },
            {
                "stem": "Find both intercepts of y = 2x^2 + 4x - 6.",
                "choices": [
                    "y-int: -6; x-ints: x = -3, 1", 
                    "y-int: 6; x-ints: x = 3, -1",
                    "y-int: -6; x-ints: x = 2, -3",
                    "y-int: 4; x-ints: x = -2, 3"
                ],
                "solution": 0,
                "rationale": "y-int: y(0) = -6. x-ints: 2x²+4x-6=0 ⇒ x²+2x-3=0 ⇒ (x+3)(x-1)=0.",
            },
        ],
        "hard": [
            {
                "stem": "Find the x-intercepts of y = 3x^2 - 12x + 12.",
                "choices": [
                    "x = 2 only",
                    "x = -2 and x = 2",
                    "x = 3 and x = 4", 
                    "No real x-intercepts"
                ],
                "solution": 0,
                "rationale": "3x² - 12x + 12 = 0 ⇒ x² - 4x + 4 = 0 ⇒ (x-2)² = 0 ⇒ x = 2 (repeated).",
            },
            {
                "stem": "For y = -x^2 + 2x + k, what value of k makes the y-intercept equal to 5?",
                "choices": ["5", "-5", "2", "3"],
                "solution": 0,
                "rationale": "y-intercept occurs at x = 0: y = -0² + 2(0) + k = k. So k = 5.",
            },
        ],
        "applied": [
            {
                "stem": "A projectile's height is h(t) = -16t^2 + 48t. When does it hit the ground?",
                "choices": [
                    "t = 0 and t = 3",
                    "t = 3 only",
                    "t = 48 only", 
                    "t = 16 only"
                ],
                "solution": 0,
                "rationale": "Ground level: h = 0. So -16t² + 48t = 0 ⇒ t(-16t + 48) = 0 ⇒ t = 0, 3.",
            },
        ],
    },
    "quad.complete.square": {
        "easy": [
            {
                "stem": "Complete the square for x^2 + 6x.",
                "choices": [
                    "(x + 3)^2 - 9",
                    "(x + 3)^2 + 9", 
                    "(x - 3)^2 - 9",
                    "(x + 6)^2 - 36"
                ],
                "solution": 0,
                "rationale": "x² + 6x = (x + 3)² - 9. Take half of 6, square it: (6/2)² = 9.",
            },
            {
                "stem": "Complete the square for x^2 - 8x.",
                "choices": [
                    "(x - 4)^2 - 16",
                    "(x + 4)^2 - 16",
                    "(x - 4)^2 + 16", 
                    "(x - 8)^2 - 64"
                ],
                "solution": 0,
                "rationale": "x² - 8x = (x - 4)² - 16. Take half of -8, square it: (-8/2)² = 16.",
            },
        ],
        "medium": [
            {
                "stem": "Complete the square for x^2 + 5x + 3.",
                "choices": [
                    "(x + \\tfrac{5}{2})^2 - \\tfrac{13}{4}",
                    "(x + \\tfrac{5}{2})^2 + \\tfrac{13}{4}",
                    "(x - \\tfrac{5}{2})^2 - \\tfrac{13}{4}",
                    "(x + 5)^2 - 22"
                ],
                "solution": 0,
                "rationale": "x² + 5x + 3 = (x + 5/2)² - 25/4 + 3 = (x + 5/2)² - 13/4.",
            },
            {
                "stem": "Complete the square for 2x^2 + 8x + 1.",
                "choices": [
                    "2(x + 2)^2 - 7",
                    "2(x + 2)^2 + 7",
                    "2(x - 2)^2 - 7",
                    "(x + 4)^2 - 15"
                ],
                "solution": 0,
                "rationale": "2x² + 8x + 1 = 2(x² + 4x) + 1 = 2((x + 2)² - 4) + 1 = 2(x + 2)² - 7.",
            },
        ],
        "hard": [
            {
                "stem": "Complete the square for 3x^2 - 12x + 5.",
                "choices": [
                    "3(x - 2)^2 - 7",
                    "3(x - 2)^2 + 7",
                    "3(x + 2)^2 - 7",
                    "(x - 4)^2 - 11"
                ],
                "solution": 0,
                "rationale": "3x² - 12x + 5 = 3(x² - 4x) + 5 = 3((x - 2)² - 4) + 5 = 3(x - 2)² - 7.",
            },
            {
                "stem": "Complete the square for -x^2 + 6x - 2.",
                "choices": [
                    "-(x - 3)^2 + 7",
                    "-(x + 3)^2 + 7",
                    "-(x - 3)^2 - 7",
                    "-(x - 6)^2 + 34"
                ],
                "solution": 0,
                "rationale": "-x² + 6x - 2 = -(x² - 6x) - 2 = -((x - 3)² - 9) - 2 = -(x - 3)² + 7.",
            },
        ],
        "applied": [
            {
                "stem": "A ball's height is h(t) = -16t^2 + 32t + 5. Complete the square to find vertex form.",
                "choices": [
                    "-16(t - 1)^2 + 21",
                    "-16(t + 1)^2 + 21", 
                    "-16(t - 1)^2 - 11",
                    "-16(t - 2)^2 + 69"
                ],
                "solution": 0,
                "rationale": "-16t² + 32t + 5 = -16(t² - 2t) + 5 = -16((t - 1)² - 1) + 5 = -16(t - 1)² + 21.",
            },
        ],
    },
    "quad.axis.symmetry": {
        "easy": [
            {
                "stem": "Find the axis of symmetry for y = x^2 + 4x + 1.",
                "choices": ["x = -2", "x = 2", "x = -4", "x = 1"],
                "solution": 0,
                "rationale": "Axis of symmetry: x = -b/(2a) = -4/(2·1) = -2.",
            },
            {
                "stem": "Find the axis of symmetry for y = x^2 - 6x + 5.",
                "choices": ["x = 3", "x = -3", "x = 6", "x = -6"],
                "solution": 0,
                "rationale": "Axis of symmetry: x = -b/(2a) = -(-6)/(2·1) = 3.",
            },
        ],
        "medium": [
            {
                "stem": "Find the axis of symmetry for y = 2x^2 + 8x - 3.",
                "choices": ["x = -2", "x = 2", "x = -4", "x = 4"],
                "solution": 0,
                "rationale": "Axis of symmetry: x = -b/(2a) = -8/(2·2) = -2.",
            },
            {
                "stem": "Find the axis of symmetry for y = -3x^2 + 6x + 1.",
                "choices": ["x = 1", "x = -1", "x = 2", "x = -2"],
                "solution": 0,
                "rationale": "Axis of symmetry: x = -b/(2a) = -6/(2·-3) = 1.",
            },
        ],
        "hard": [
            {
                "stem": "Find the axis of symmetry for y = 0.5x^2 - 3x + 7.",
                "choices": ["x = 3", "x = -3", "x = 1.5", "x = 6"],
                "solution": 0,
                "rationale": "Axis of symmetry: x = -b/(2a) = -(-3)/(2·0.5) = 3.",
            },
            {
                "stem": "For y = ax^2 + 6x + c, if the axis of symmetry is x = -1, what is a?",
                "choices": ["a = 3", "a = -3", "a = 6", "a = -6"],
                "solution": 0,
                "rationale": "x = -b/(2a) = -1, so -6/(2a) = -1, therefore a = 3.",
            },
        ],
        "applied": [
            {
                "stem": "A projectile's path is h(t) = -16t^2 + 64t + 10. At what time is maximum height?",
                "choices": ["t = 2", "t = 4", "t = 1", "t = 8"],
                "solution": 0,
                "rationale": "Maximum at axis of symmetry: t = -b/(2a) = -64/(2·-16) = 2.",
            },
        ],
    },
}

VALID_DIFFICULTIES = {"easy", "medium", "hard", "applied"}


def generate_item(
    skill_id: str, difficulty: Optional[str] = None, seed: Optional[int] = None
) -> dict:
    """
    Generate a math question item per contract.

    Args:
        skill_id: Skill identifier (e.g., "quad.graph.vertex")
        difficulty: One of {"easy", "medium", "hard", "applied"}, or None (defaults to "easy")
        seed: Optional seed for deterministic generation; if provided, item is fully deterministic

    Returns:
        A dict with keys: item_id, skill_id, difficulty, stem, choices, solution_choice_id, solution_text, tags

    Raises:
        ValueError: If skill_id is unknown, difficulty is invalid, or seed is not an int
    """
    # Validate and normalize difficulty
    if difficulty is None:
        difficulty = "easy"
    
    if difficulty not in VALID_DIFFICULTIES:
        raise ValueError("invalid_difficulty")
    
    # Validate skill_id
    if skill_id not in SKILL_TEMPLATES:
        raise ValueError("unknown_skill")
    
    # Check difficulty exists for this skill (belt & suspenders)
    if difficulty not in SKILL_TEMPLATES[skill_id]:
        raise ValueError("invalid_difficulty")
    
    # Validate seed type
    if seed is not None and not isinstance(seed, int):
        raise ValueError("invalid_seed")
    
    # Initialize deterministic RNG
    rng = random.Random(seed)
    
    # Get questions for this skill/difficulty
    questions = SKILL_TEMPLATES[skill_id][difficulty]
    
    # Pick a question (deterministically)
    question = questions[rng.randint(0, len(questions) - 1)]
    
    # Generate item_id
    if seed is not None:
        item_id = f"{skill_id}:{difficulty}:{seed}"
    else:
        # Using UUID4; format not validated in Phase-1 beyond non-empty uniqueness.
        item_id = str(uuid.uuid4())
    
    # Shuffle choices deterministically, track correct answer
    choices_with_idx = list(enumerate(question["choices"]))
    rng.shuffle(choices_with_idx)
    
    shuffled_choices = [text for _, text in choices_with_idx]
    solution_idx_after_shuffle = next(i for i, (orig_idx, _) in enumerate(choices_with_idx) if orig_idx == question["solution"])
    solution_choice_id = chr(ord("A") + solution_idx_after_shuffle)
    
    return {
        "item_id": item_id,
        "skill_id": skill_id,
        "difficulty": difficulty,
        "stem": question["stem"],
        "choices": [
            {"id": chr(ord("A") + i), "text": text}
            for i, text in enumerate(shuffled_choices)
        ],
        "solution_choice_id": solution_choice_id,
        "solution_text": shuffled_choices[solution_idx_after_shuffle],
        "tags": ["vertex_form"],
    }
