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
            {
                "stem": "Find the vertex of y = (x - 5)^2 + 1.",
                "choices": ["(5, 1)", "(-5, 1)", "(5, -1)", "(1, 5)"],
                "solution": 0,
                "rationale": "In vertex form y = (x - h)^2 + k, the vertex is (h, k) = (5, 1).",
            },
            {
                "stem": "What is the vertex of y = (x + 4)^2 + 3?",
                "choices": ["(-4, 3)", "(4, 3)", "(-4, -3)", "(3, -4)"],
                "solution": 0,
                "rationale": "From y = (x - h)^2 + k, we have h = -4 and k = 3.",
            },
            {
                "stem": "For y = (x - 2)^2 - 7, what is the vertex?",
                "choices": ["(2, -7)", "(-2, -7)", "(2, 7)", "(-7, 2)"],
                "solution": 0,
                "rationale": "The vertex form gives vertex (h, k) = (2, -7).",
            },
            {
                "stem": "Find the vertex of y = (x + 6)^2 - 2.",
                "choices": ["(-6, -2)", "(6, -2)", "(-6, 2)", "(-2, -6)"],
                "solution": 0,
                "rationale": "From y = (x - h)^2 + k with x + 6 = x - (-6), vertex is (-6, -2).",
            },
            {
                "stem": "What is the vertex of y = (x - 7)^2 + 4?",
                "choices": ["(7, 4)", "(-7, 4)", "(7, -4)", "(4, 7)"],
                "solution": 0,
                "rationale": "In y = (x - h)^2 + k, h = 7 and k = 4, so vertex is (7, 4).",
            },
            {
                "stem": "For y = (x + 2)^2 + 8, find the vertex.",
                "choices": ["(-2, 8)", "(2, 8)", "(-2, -8)", "(8, -2)"],
                "solution": 0,
                "rationale": "The vertex form y = (x - h)^2 + k has h = -2, k = 8.",
            },
            {
                "stem": "Find the vertex of y = (x - 1)^2 - 3.",
                "choices": ["(1, -3)", "(-1, -3)", "(1, 3)", "(-3, 1)"],
                "solution": 0,
                "rationale": "From vertex form, the vertex is (1, -3).",
            },
            {
                "stem": "What is the vertex of y = (x + 5)^2 + 6?",
                "choices": ["(-5, 6)", "(5, 6)", "(-5, -6)", "(6, -5)"],
                "solution": 0,
                "rationale": "In y = (x - h)^2 + k, we have vertex (h, k) = (-5, 6).",
            },
        ],
        "medium": [
            {
                "stem": "Find the vertex of y = 2(x - 1)^2 + 3.",
                "choices": ["(1, 3)", "(1, -3)", "(-1, 3)", "(-1, -3)"],
                "solution": 0,
                "rationale": "The vertex form y = a(x - h)^2 + k has vertex (h, k).",
            },
            {
                "stem": "What is the vertex of y = -3(x + 2)^2 + 5?",
                "choices": ["(-2, 5)", "(2, 5)", "(-2, -5)", "(-3, 5)"],
                "solution": 0,
                "rationale": "In vertex form y = a(x - h)^2 + k, the vertex is (h, k) = (-2, 5). The coefficient a = -3 affects the shape, not the vertex.",
            },
            {
                "stem": "Find the vertex of y = 0.5(x - 4)^2 - 2.",
                "choices": ["(4, -2)", "(-4, -2)", "(4, 2)", "(0.5, -2)"],
                "solution": 0,
                "rationale": "From y = a(x - h)^2 + k, the vertex is (h, k) = (4, -2).",
            },
            {
                "stem": "The parabola y = -2(x + 5)^2 + 1 has vertex at:",
                "choices": ["(-5, 1)", "(5, 1)", "(-5, -1)", "(-2, 1)"],
                "solution": 0,
                "rationale": "Vertex form gives h = -5 and k = 1, so vertex is (-5, 1).",
            },
            {
                "stem": "What is the vertex of y = 4(x - 3)^2 - 8?",
                "choices": ["(3, -8)", "(-3, -8)", "(3, 8)", "(4, -8)"],
                "solution": 0,
                "rationale": "In y = a(x - h)^2 + k, the vertex is at (h, k) = (3, -8).",
            },
            {
                "stem": "Find the vertex of y = -0.5(x + 6)^2 + 7.",
                "choices": ["(-6, 7)", "(6, 7)", "(-6, -7)", "(-0.5, 7)"],
                "solution": 0,
                "rationale": "The vertex form shows h = -6 and k = 7, giving vertex (-6, 7).",
            },
            {
                "stem": "The vertex of y = 3(x - 7)^2 + 2 is located at:",
                "choices": ["(7, 2)", "(-7, 2)", "(7, -2)", "(3, 2)"],
                "solution": 0,
                "rationale": "From vertex form y = a(x - h)^2 + k, the vertex is (h, k) = (7, 2).",
            },
            {
                "stem": "What is the vertex of y = -5(x + 1)^2 - 3?",
                "choices": ["(-1, -3)", "(1, -3)", "(-1, 3)", "(-5, -3)"],
                "solution": 0,
                "rationale": "In vertex form, h = -1 and k = -3, so the vertex is (-1, -3).",
            },
            {
                "stem": "Find the vertex of y = 1.5(x - 8)^2 + 4.",
                "choices": ["(8, 4)", "(-8, 4)", "(8, -4)", "(1.5, 4)"],
                "solution": 0,
                "rationale": "The vertex form y = a(x - h)^2 + k has vertex at (h, k) = (8, 4).",
            },
            {
                "stem": "The parabola y = -4(x + 9)^2 - 6 has its vertex at:",
                "choices": ["(-9, -6)", "(9, -6)", "(-9, 6)", "(-4, -6)"],
                "solution": 0,
                "rationale": "From y = a(x - h)^2 + k, the vertex is (h, k) = (-9, -6).",
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
            {
                "stem": "Find the vertex of y = x^2 + 6x + 11.",
                "choices": ["(-3, 2)", "(3, 2)", "(-3, -2)", "(6, 11)"],
                "solution": 0,
                "rationale": "Complete the square: y = (x + 3)^2 + 2. Vertex is (-3, 2).",
            },
            {
                "stem": "What is the vertex of y = -2x^2 + 12x - 10?",
                "choices": ["(3, 8)", "(-3, 8)", "(3, -8)", "(6, -10)"],
                "solution": 0,
                "rationale": "Complete the square: y = -2(x - 3)^2 + 8. Vertex is (3, 8).",
            },
            {
                "stem": "The vertex of y = 3x^2 - 12x + 7 is located at:",
                "choices": ["(2, -5)", "(-2, -5)", "(2, 5)", "(4, 7)"],
                "solution": 0,
                "rationale": "Complete the square: y = 3(x - 2)^2 - 5. Vertex is (2, -5).",
            },
            {
                "stem": "Find the vertex of y = -x^2 - 4x + 3.",
                "choices": ["(-2, 7)", "(2, 7)", "(-2, -7)", "(-4, 3)"],
                "solution": 0,
                "rationale": "Complete the square: y = -(x + 2)^2 + 7. Vertex is (-2, 7).",
            },
            {
                "stem": "What is the vertex of y = 0.5x^2 + 3x + 2?",
                "choices": ["(-3, -2.5)", "(3, -2.5)", "(-3, 2.5)", "(1.5, 2)"],
                "solution": 0,
                "rationale": "Complete the square: y = 0.5(x + 3)^2 - 2.5. Vertex is (-3, -2.5).",
            },
            {
                "stem": "The parabola y = 4x^2 - 16x + 19 has vertex at:",
                "choices": ["(2, 3)", "(-2, 3)", "(2, -3)", "(4, 19)"],
                "solution": 0,
                "rationale": "Complete the square: y = 4(x - 2)^2 + 3. Vertex is (2, 3).",
            },
            {
                "stem": "Find the vertex of y = -3x^2 + 18x - 21.",
                "choices": ["(3, 6)", "(-3, 6)", "(3, -6)", "(6, -21)"],
                "solution": 0,
                "rationale": "Complete the square: y = -3(x - 3)^2 + 6. Vertex is (3, 6).",
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
            {
                "stem": "A water fountain's arc is h(d) = -0.5(d - 6)^2 + 18. What is the maximum height?",
                "choices": ["18 feet", "6 feet", "0.5 feet", "12 feet"],
                "solution": 0,
                "rationale": "The vertex is (6, 18), so the maximum height is 18 feet.",
            },
            {
                "stem": "A company's revenue is R(x) = -3(x - 8)^2 + 192. At what production level x is revenue maximized?",
                "choices": ["x = 8 units", "x = -8 units", "x = 3 units", "x = 192 units"],
                "solution": 0,
                "rationale": "The vertex form shows maximum at x = 8 units.",
            },
            {
                "stem": "A basketball's trajectory is y = -16(t - 1.5)^2 + 36. When does the ball reach its highest point?",
                "choices": ["t = 1.5 seconds", "t = -1.5 seconds", "t = 16 seconds", "t = 36 seconds"],
                "solution": 0,
                "rationale": "The vertex is at t = 1.5 seconds, when height is maximum.",
            },
            {
                "stem": "A bridge's cable forms y = 0.02(x - 50)^2 + 10. What is the lowest point of the cable?",
                "choices": ["(50, 10)", "(-50, 10)", "(50, -10)", "(0.02, 10)"],
                "solution": 0,
                "rationale": "The vertex is (50, 10), representing the minimum point of the cable.",
            },
            {
                "stem": "A dolphin's jump path is h(t) = -5(t - 3)^2 + 45. What are the time and height at the peak?",
                "choices": ["(3, 45)", "(-3, 45)", "(3, -45)", "(5, 45)"],
                "solution": 0,
                "rationale": "The vertex (3, 45) gives the time (3 sec) and maximum height (45 ft).",
            },
            {
                "stem": "A farmer's crop yield is Y(f) = -2(f - 12)^2 + 288. What fertilizer amount f maximizes yield?",
                "choices": ["f = 12 lbs", "f = -12 lbs", "f = 2 lbs", "f = 288 lbs"],
                "solution": 0,
                "rationale": "The vertex is at f = 12, where yield is maximized.",
            },
            {
                "stem": "An arch's height is h(x) = -0.25(x - 20)^2 + 100. What is the vertex of the arch?",
                "choices": ["(20, 100)", "(-20, 100)", "(20, -100)", "(0.25, 100)"],
                "solution": 0,
                "rationale": "The vertex form shows the highest point at (20, 100).",
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
            {
                "stem": "Find the vertex of y = x^2 + 2x - 3.",
                "choices": ["(-1, -4)", "(-1, 4)", "(1, -4)", "(-2, -3)"],
                "solution": 0,
                "rationale": "a=1, b=2, c=-3 ⇒ h = -2/(2·1) = -1; k = 1 - 2 - 3 = -4.",
            },
            {
                "stem": "Find the vertex of y = x^2 - 8x + 10.",
                "choices": ["(4, -6)", "(4, 6)", "(-4, -6)", "(-8, 10)"],
                "solution": 0,
                "rationale": "a=1, b=-8, c=10 ⇒ h = -(-8)/(2·1) = 4; k = 16 - 32 + 10 = -6.",
            },
            {
                "stem": "Find the vertex of y = -x^2 - 2x + 8.",
                "choices": ["(-1, 9)", "(-1, -9)", "(1, 9)", "(-2, 8)"],
                "solution": 0,
                "rationale": "a=-1, b=-2, c=8 ⇒ h = -(-2)/(2·-1) = -1; k = -1 + 2 + 8 = 9.",
            },
            {
                "stem": "Find the vertex of y = x^2 + 10x + 21.",
                "choices": ["(-5, -4)", "(-5, 4)", "(5, -4)", "(-10, 21)"],
                "solution": 0,
                "rationale": "a=1, b=10, c=21 ⇒ h = -10/(2·1) = -5; k = 25 - 50 + 21 = -4.",
            },
            {
                "stem": "Find the vertex of y = -x^2 + 6x - 5.",
                "choices": ["(3, 4)", "(3, -4)", "(-3, 4)", "(-6, -5)"],
                "solution": 0,
                "rationale": "a=-1, b=6, c=-5 ⇒ h = -6/(2·-1) = 3; k = -9 + 18 - 5 = 4.",
            },
            {
                "stem": "Find the vertex of y = x^2 - 2x - 8.",
                "choices": ["(1, -9)", "(1, 9)", "(-1, -9)", "(-2, -8)"],
                "solution": 0,
                "rationale": "a=1, b=-2, c=-8 ⇒ h = -(-2)/(2·1) = 1; k = 1 - 2 - 8 = -9.",
            },
            {
                "stem": "Find the vertex of y = -x^2 + 8x - 12.",
                "choices": ["(4, 4)", "(4, -4)", "(-4, 4)", "(-8, -12)"],
                "solution": 0,
                "rationale": "a=-1, b=8, c=-12 ⇒ h = -8/(2·-1) = 4; k = -16 + 32 - 12 = 4.",
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
            {
                "stem": "Find the vertex of y = 3x^2 + 12x + 5.",
                "choices": ["(-2, -7)", "(-2, 7)", "(2, -7)", "(-4, 5)"],
                "solution": 0,
                "rationale": "a=3, b=12, c=5 ⇒ h = -12/(2·3) = -2; k = 3·4 - 24 + 5 = -7.",
            },
            {
                "stem": "Find the vertex of y = -2x^2 + 4x + 6.",
                "choices": ["(1, 8)", "(1, -8)", "(-1, 8)", "(-2, 6)"],
                "solution": 0,
                "rationale": "a=-2, b=4, c=6 ⇒ h = -4/(2·-2) = 1; k = -2 + 4 + 6 = 8.",
            },
            {
                "stem": "Find the vertex of y = 4x^2 - 16x + 10.",
                "choices": ["(2, -6)", "(2, 6)", "(-2, -6)", "(-4, 10)"],
                "solution": 0,
                "rationale": "a=4, b=-16, c=10 ⇒ h = -(-16)/(2·4) = 2; k = 16 - 32 + 10 = -6.",
            },
            {
                "stem": "Find the vertex of y = -5x^2 + 10x - 3.",
                "choices": ["(1, 2)", "(1, -2)", "(-1, 2)", "(-5, -3)"],
                "solution": 0,
                "rationale": "a=-5, b=10, c=-3 ⇒ h = -10/(2·-5) = 1; k = -5 + 10 - 3 = 2.",
            },
            {
                "stem": "Find the vertex of y = 0.5x^2 + 2x - 1.",
                "choices": ["(-2, -3)", "(-2, 3)", "(2, -3)", "(0.5, -1)"],
                "solution": 0,
                "rationale": "a=0.5, b=2, c=-1 ⇒ h = -2/(2·0.5) = -2; k = 0.5·4 - 4 - 1 = -3.",
            },
            {
                "stem": "Find the vertex of y = -4x^2 + 24x - 32.",
                "choices": ["(3, 4)", "(3, -4)", "(-3, 4)", "(-4, -32)"],
                "solution": 0,
                "rationale": "a=-4, b=24, c=-32 ⇒ h = -24/(2·-4) = 3; k = -36 + 72 - 32 = 4.",
            },
            {
                "stem": "Find the vertex of y = 6x^2 - 18x + 9.",
                "choices": ["(1.5, -4.5)", "(1.5, 4.5)", "(-1.5, -4.5)", "(-3, 9)"],
                "solution": 0,
                "rationale": "a=6, b=-18, c=9 ⇒ h = -(-18)/(2·6) = 1.5; k = 6·2.25 - 27 + 9 = -4.5.",
            },
            {
                "stem": "Find the vertex of y = -0.5x^2 - 4x + 2.",
                "choices": ["(-4, 10)", "(-4, -10)", "(4, 10)", "(-0.5, 2)"],
                "solution": 0,
                "rationale": "a=-0.5, b=-4, c=2 ⇒ h = -(-4)/(2·-0.5) = -4; k = -8 + 16 + 2 = 10.",
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
            {
                "stem": "Find the vertex of y = 3x^2 - 15x + 12.",
                "choices": ["(2.5, -6.75)", "(2.5, 6.75)", "(-2.5, -6.75)", "(-5, 12)"],
                "solution": 0,
                "rationale": "a=3, b=-15 ⇒ h = -(-15)/(2·3) = 2.5; k = 3·6.25 - 37.5 + 12 = -6.75.",
            },
            {
                "stem": "Find the vertex of y = -4x^2 - 12x + 5.",
                "choices": ["(-1.5, 14)", "(-1.5, -14)", "(1.5, 14)", "(-3, 5)"],
                "solution": 0,
                "rationale": "a=-4, b=-12 ⇒ h = -(-12)/(2·-4) = -1.5; k = -9 + 18 + 5 = 14.",
            },
            {
                "stem": "Find the vertex of y = 7x^2 + 28x - 10.",
                "choices": ["(-2, -38)", "(-2, 38)", "(2, -38)", "(-4, -10)"],
                "solution": 0,
                "rationale": "a=7, b=28 ⇒ h = -28/(2·7) = -2; k = 28 - 56 - 10 = -38.",
            },
            {
                "stem": "Find the vertex of y = -0.25x^2 + 3x - 8.",
                "choices": ["(6, 1)", "(6, -1)", "(-6, 1)", "(-0.25, -8)"],
                "solution": 0,
                "rationale": "a=-0.25, b=3 ⇒ h = -3/(2·-0.25) = 6; k = -9 + 18 - 8 = 1.",
            },
            {
                "stem": "Find the vertex of y = 8x^2 - 24x + 10.",
                "choices": ["(1.5, -8)", "(1.5, 8)", "(-1.5, -8)", "(-3, 10)"],
                "solution": 0,
                "rationale": "a=8, b=-24 ⇒ h = -(-24)/(2·8) = 1.5; k = 18 - 36 + 10 = -8.",
            },
            {
                "stem": "Find the vertex of y = -6x^2 + 30x - 25.",
                "choices": ["(2.5, 12.5)", "(2.5, -12.5)", "(-2.5, 12.5)", "(-5, -25)"],
                "solution": 0,
                "rationale": "a=-6, b=30 ⇒ h = -30/(2·-6) = 2.5; k = -37.5 + 75 - 25 = 12.5.",
            },
            {
                "stem": "Find the vertex of y = 1.5x^2 + 9x + 6.",
                "choices": ["(-3, -7.5)", "(-3, 7.5)", "(3, -7.5)", "(1.5, 6)"],
                "solution": 0,
                "rationale": "a=1.5, b=9 ⇒ h = -9/(2·1.5) = -3; k = 13.5 - 27 + 6 = -7.5.",
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
            {
                "stem": "A football is kicked with trajectory h(t) = -5t^2 + 20t + 1. When does it reach maximum height?",
                "choices": ["t = 2 seconds", "t = 4 seconds", "t = 1 second", "t = 5 seconds"],
                "solution": 0,
                "rationale": "a=-5, b=20 ⇒ t = -20/(2·-5) = 2 seconds.",
            },
            {
                "stem": "Revenue from selling x items is R(x) = -3x^2 + 24x + 100. What quantity maximizes revenue?",
                "choices": ["x = 4 items", "x = 8 items", "x = 3 items", "x = 12 items"],
                "solution": 0,
                "rationale": "a=-3, b=24 ⇒ x = -24/(2·-3) = 4 items.",
            },
            {
                "stem": "A diver's depth is d(t) = 4t^2 - 16t + 20. At what time is the diver at minimum depth?",
                "choices": ["t = 2 seconds", "t = 4 seconds", "t = 1 second", "t = 8 seconds"],
                "solution": 0,
                "rationale": "a=4, b=-16 ⇒ t = -(-16)/(2·4) = 2 seconds.",
            },
            {
                "stem": "A company's cost is C(x) = 0.5x^2 - 10x + 200. At what production level x is cost minimized?",
                "choices": ["x = 10 units", "x = 20 units", "x = 5 units", "x = 100 units"],
                "solution": 0,
                "rationale": "a=0.5, b=-10 ⇒ x = -(-10)/(2·0.5) = 10 units.",
            },
            {
                "stem": "A rocket's altitude is h(t) = -4.9t^2 + 49t + 10. When does it reach peak altitude?",
                "choices": ["t = 5 seconds", "t = 10 seconds", "t = 2.5 seconds", "t = 49 seconds"],
                "solution": 0,
                "rationale": "a=-4.9, b=49 ⇒ t = -49/(2·-4.9) = 5 seconds.",
            },
            {
                "stem": "Temperature T(h) = -2h^2 + 8h + 15 varies with hours h after sunrise. When is temperature maximum?",
                "choices": ["h = 2 hours", "h = 4 hours", "h = 1 hour", "h = 8 hours"],
                "solution": 0,
                "rationale": "a=-2, b=8 ⇒ h = -8/(2·-2) = 2 hours.",
            },
            {
                "stem": "A store's daily sales S(p) = -10p^2 + 300p - 1000 depend on price p. What price maximizes sales?",
                "choices": ["p = $15", "p = $30", "p = $10", "p = $150"],
                "solution": 0,
                "rationale": "a=-10, b=300 ⇒ p = -300/(2·-10) = $15.",
            },
            {
                "stem": "A farmer's yield Y(f) = -0.25f^2 + 5f + 80 depends on fertilizer f (lbs). What amount maximizes yield?",
                "choices": ["f = 10 lbs", "f = 20 lbs", "f = 5 lbs", "f = 40 lbs"],
                "solution": 0,
                "rationale": "a=-0.25, b=5 ⇒ f = -5/(2·-0.25) = 10 lbs.",
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
            {
                "stem": "Find the roots of y = (x - 3)(x - 7).",
                "choices": [
                    "x = 3 and x = 7",
                    "x = -3 and x = -7",
                    "x = 3 and x = -7",
                    "x = -3 and x = 7"
                ],
                "solution": 0,
                "rationale": "x−3=0 ⇒ x=3; x−7=0 ⇒ x=7.",
            },
            {
                "stem": "Find the roots of y = (x + 6)(x - 1).",
                "choices": [
                    "x = -6 and x = 1",
                    "x = 6 and x = -1",
                    "x = -6 and x = -1",
                    "x = 6 and x = 1"
                ],
                "solution": 0,
                "rationale": "x+6=0 ⇒ x=−6; x−1=0 ⇒ x=1.",
            },
            {
                "stem": "Find the roots of y = (x - 5)(x + 3).",
                "choices": [
                    "x = 5 and x = -3",
                    "x = -5 and x = 3",
                    "x = 5 and x = 3",
                    "x = -5 and x = -3"
                ],
                "solution": 0,
                "rationale": "x−5=0 ⇒ x=5; x+3=0 ⇒ x=−3.",
            },
            {
                "stem": "Find the roots of y = (x + 8)(x + 2).",
                "choices": [
                    "x = -8 and x = -2",
                    "x = 8 and x = 2",
                    "x = -8 and x = 2",
                    "x = 8 and x = -2"
                ],
                "solution": 0,
                "rationale": "x+8=0 ⇒ x=−8; x+2=0 ⇒ x=−2.",
            },
            {
                "stem": "Find the roots of y = (x - 4)(x - 9).",
                "choices": [
                    "x = 4 and x = 9",
                    "x = -4 and x = -9",
                    "x = 4 and x = -9",
                    "x = -4 and x = 9"
                ],
                "solution": 0,
                "rationale": "x−4=0 ⇒ x=4; x−9=0 ⇒ x=9.",
            },
            {
                "stem": "Find the roots of y = (x + 7)(x - 2).",
                "choices": [
                    "x = -7 and x = 2",
                    "x = 7 and x = -2",
                    "x = -7 and x = -2",
                    "x = 7 and x = 2"
                ],
                "solution": 0,
                "rationale": "x+7=0 ⇒ x=−7; x−2=0 ⇒ x=2.",
            },
            {
                "stem": "Find the roots of y = (x - 6)(x + 4).",
                "choices": [
                    "x = 6 and x = -4",
                    "x = -6 and x = 4",
                    "x = 6 and x = 4",
                    "x = -6 and x = -4"
                ],
                "solution": 0,
                "rationale": "x−6=0 ⇒ x=6; x+4=0 ⇒ x=−4.",
            },
            {
                "stem": "Find the roots of y = (x + 9)(x - 5).",
                "choices": [
                    "x = -9 and x = 5",
                    "x = 9 and x = -5",
                    "x = -9 and x = -5",
                    "x = 9 and x = 5"
                ],
                "solution": 0,
                "rationale": "x+9=0 ⇒ x=−9; x−5=0 ⇒ x=5.",
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
            {
                "stem": "Find the roots of y = 5(x - 4)(x - 1).",
                "choices": [
                    "x = 4 and x = 1",
                    "x = -4 and x = -1",
                    "x = 4 and x = -1",
                    "x = -4 and x = 1"
                ],
                "solution": 0,
                "rationale": "The coefficient 5 doesn't affect roots: x−4=0 ⇒ x=4; x−1=0 ⇒ x=1.",
            },
            {
                "stem": "Find the roots of y = -2(x + 6)(x - 3).",
                "choices": [
                    "x = -6 and x = 3",
                    "x = 6 and x = -3",
                    "x = -6 and x = -3",
                    "x = 6 and x = 3"
                ],
                "solution": 0,
                "rationale": "The −2 coefficient doesn't change roots: x+6=0 ⇒ x=−6; x−3=0 ⇒ x=3.",
            },
            {
                "stem": "Find the roots of y = 4(x - 7)(x + 2).",
                "choices": [
                    "x = 7 and x = -2",
                    "x = -7 and x = 2",
                    "x = 7 and x = 2",
                    "x = -7 and x = -2"
                ],
                "solution": 0,
                "rationale": "Leading coefficient 4 is irrelevant to roots: x−7=0 ⇒ x=7; x+2=0 ⇒ x=−2.",
            },
            {
                "stem": "Find the roots of y = -5(x + 4)(x + 8).",
                "choices": [
                    "x = -4 and x = -8",
                    "x = 4 and x = 8",
                    "x = -4 and x = 8",
                    "x = 4 and x = -8"
                ],
                "solution": 0,
                "rationale": "−5 scales the parabola but doesn't affect roots: x=−4, x=−8.",
            },
            {
                "stem": "Find the roots of y = 0.5(x - 5)(x + 9).",
                "choices": [
                    "x = 5 and x = -9",
                    "x = -5 and x = 9",
                    "x = 5 and x = 9",
                    "x = -5 and x = -9"
                ],
                "solution": 0,
                "rationale": "The coefficient 0.5 doesn't change roots: x−5=0 ⇒ x=5; x+9=0 ⇒ x=−9.",
            },
            {
                "stem": "Find the roots of y = -6(x - 2)(x - 8).",
                "choices": [
                    "x = 2 and x = 8",
                    "x = -2 and x = -8",
                    "x = 2 and x = -8",
                    "x = -2 and x = 8"
                ],
                "solution": 0,
                "rationale": "−6 coefficient doesn't affect roots: x−2=0 ⇒ x=2; x−8=0 ⇒ x=8.",
            },
            {
                "stem": "Find the roots of y = 3(x + 7)(x - 6).",
                "choices": [
                    "x = -7 and x = 6",
                    "x = 7 and x = -6",
                    "x = -7 and x = -6",
                    "x = 7 and x = 6"
                ],
                "solution": 0,
                "rationale": "The 3 scales vertically only: x+7=0 ⇒ x=−7; x−6=0 ⇒ x=6.",
            },
            {
                "stem": "Find the roots of y = -0.25(x + 3)(x + 10).",
                "choices": [
                    "x = -3 and x = -10",
                    "x = 3 and x = 10",
                    "x = -3 and x = 10",
                    "x = 3 and x = -10"
                ],
                "solution": 0,
                "rationale": "The −0.25 coefficient doesn't affect where the roots are: x=−3, x=−10.",
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
            {
                "stem": "Find the distinct real roots of y = 2(x - 5)^2 (x + 6).",
                "choices": [
                    "x = 5 and x = -6",
                    "x = 5 only",
                    "x = -6 only",
                    "x = -5 and x = 6"
                ],
                "solution": 0,
                "rationale": "(x−5)^2 gives repeated root at x=5; (x+6) ⇒ x=−6. Distinct roots: 5 and −6.",
            },
            {
                "stem": "Find the roots of y = -0.5(x - 1)(x + 7).",
                "choices": [
                    "x = 1 and x = -7",
                    "x = -1 and x = 7",
                    "x = 1 and x = 7",
                    "x = -1 and x = -7"
                ],
                "solution": 0,
                "rationale": "−0.5 coefficient doesn't change roots: x−1=0 ⇒ x=1; x+7=0 ⇒ x=−7.",
            },
            {
                "stem": "Find the distinct real roots of y = -(x + 2)^2 (x - 9).",
                "choices": [
                    "x = -2 and x = 9",
                    "x = -2 only",
                    "x = 9 only",
                    "x = 2 and x = -9"
                ],
                "solution": 0,
                "rationale": "(x+2)^2 gives repeated root at x=−2; (x−9) ⇒ x=9. Distinct roots: −2 and 9.",
            },
            {
                "stem": "Find the roots of y = 1.5(x + 4)(x - 12).",
                "choices": [
                    "x = -4 and x = 12",
                    "x = 4 and x = -12",
                    "x = -4 and x = -12",
                    "x = 4 and x = 12"
                ],
                "solution": 0,
                "rationale": "1.5 coefficient doesn't affect roots: x+4=0 ⇒ x=−4; x−12=0 ⇒ x=12.",
            },
            {
                "stem": "Find the distinct real roots of y = 3(x - 7)^2 (x + 5).",
                "choices": [
                    "x = 7 and x = -5",
                    "x = 7 only",
                    "x = -5 only",
                    "x = -7 and x = 5"
                ],
                "solution": 0,
                "rationale": "(x−7)^2 gives repeated root at x=7; (x+5) ⇒ x=−5. Distinct roots: 7 and −5.",
            },
            {
                "stem": "Find the distinct real roots of y = -4(x + 8)^3 (x - 2).",
                "choices": [
                    "x = -8 and x = 2",
                    "x = 8 and x = -2",
                    "x = -8 only",
                    "x = 2 only"
                ],
                "solution": 0,
                "rationale": "(x+8)^3 gives repeated root at x=−8; (x−2) ⇒ x=2. Distinct roots: −8 and 2.",
            },
            {
                "stem": "Find the roots of y = -2.5(x - 6)(x + 11).",
                "choices": [
                    "x = 6 and x = -11",
                    "x = -6 and x = 11",
                    "x = 6 and x = 11",
                    "x = -6 and x = -11"
                ],
                "solution": 0,
                "rationale": "−2.5 coefficient doesn't affect roots: x−6=0 ⇒ x=6; x+11=0 ⇒ x=−11.",
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
            {
                "stem": "A rocket's path is h(t) = -16(t - 2)(t - 8). When does it hit the ground?",
                "choices": [
                    "t = 2 and t = 8",
                    "t = -2 and t = 8",
                    "t = 2 and t = -8",
                    "t = 0 and t = 10"
                ],
                "solution": 0,
                "rationale": "The rocket hits the ground when h(t)=0 ⇒ t=2 and t=8 seconds.",
            },
            {
                "stem": "Profit is P(x) = 3(x - 5)(x - 15). When is profit zero?",
                "choices": [
                    "x = 5 and x = 15",
                    "x = -5 and x = -15",
                    "x = 5 and x = -15",
                    "x = 0 and x = 20"
                ],
                "solution": 0,
                "rationale": "Break-even points occur when P(x)=0 ⇒ x=5 and x=15 units.",
            },
            {
                "stem": "A projectile's height is h(t) = -4.9(t - 0)(t - 10). When is it at ground level?",
                "choices": [
                    "t = 0 and t = 10",
                    "t = -10 and t = 0",
                    "t = 5 only",
                    "t = 0 only"
                ],
                "solution": 0,
                "rationale": "At ground level h(t)=0 ⇒ t=0 (launch) and t=10 seconds (landing).",
            },
            {
                "stem": "A bridge arch has height h(x) = -2(x - 10)(x - 40). Where does it meet the ground?",
                "choices": [
                    "x = 10 and x = 40",
                    "x = -10 and x = -40",
                    "x = 10 and x = -40",
                    "x = 25 only"
                ],
                "solution": 0,
                "rationale": "The arch meets ground when h(x)=0 ⇒ x=10 and x=40 meters.",
            },
            {
                "stem": "Revenue is R(x) = -0.5(x - 4)(x - 20). When is revenue zero?",
                "choices": [
                    "x = 4 and x = 20",
                    "x = -4 and x = -20",
                    "x = 4 and x = -20",
                    "x = 12 only"
                ],
                "solution": 0,
                "rationale": "Zero revenue occurs at x=4 and x=20 units.",
            },
            {
                "stem": "A diver's depth is d(t) = 2(t - 3)(t - 12). When is the diver at the surface (depth = 0)?",
                "choices": [
                    "t = 3 and t = 12",
                    "t = -3 and t = -12",
                    "t = 3 and t = -12",
                    "t = 7.5 only"
                ],
                "solution": 0,
                "rationale": "At surface, d(t)=0 ⇒ t=3 and t=12 seconds.",
            },
            {
                "stem": "A football is kicked with trajectory h(t) = -16(t - 0.5)(t - 4.5). When is it on the ground?",
                "choices": [
                    "t = 0.5 and t = 4.5",
                    "t = -0.5 and t = 4.5",
                    "t = 0.5 and t = -4.5",
                    "t = 2.5 only"
                ],
                "solution": 0,
                "rationale": "Ground level at h(t)=0 ⇒ t=0.5 and t=4.5 seconds.",
            },
            {
                "stem": "A company's loss function is L(x) = 4(x - 8)(x - 25). When does the company break even?",
                "choices": [
                    "x = 8 and x = 25",
                    "x = -8 and x = -25",
                    "x = 8 and x = -25",
                    "x = 16.5 only"
                ],
                "solution": 0,
                "rationale": "Break-even when L(x)=0 ⇒ x=8 and x=25 units.",
            },
            {
                "stem": "A pendulum's displacement is d(t) = -3(t - 1)(t - 7). When is it at equilibrium (d = 0)?",
                "choices": [
                    "t = 1 and t = 7",
                    "t = -1 and t = -7",
                    "t = 1 and t = -7",
                    "t = 4 only"
                ],
                "solution": 0,
                "rationale": "At equilibrium d(t)=0 ⇒ t=1 and t=7 seconds.",
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
            {
                "stem": "Solve by factoring: x^2 - 5x + 4 = 0.",
                "choices": [
                    "x = 1 and x = 4",
                    "x = -1 and x = -4",
                    "x = -1 and x = 4",
                    "x = 1 and x = -4"
                ],
                "solution": 0,
                "rationale": "x^2 - 5x + 4 = (x - 1)(x - 4)=0 ⇒ x=1,4.",
            },
            {
                "stem": "Solve by factoring: x^2 + 7x + 10 = 0.",
                "choices": [
                    "x = -2 and x = -5",
                    "x = 2 and x = 5",
                    "x = -2 and x = 5",
                    "x = 2 and x = -5"
                ],
                "solution": 0,
                "rationale": "x^2 + 7x + 10 = (x + 2)(x + 5)=0 ⇒ x=−2,−5.",
            },
            {
                "stem": "Solve by factoring: x^2 - 9x + 20 = 0.",
                "choices": [
                    "x = 4 and x = 5",
                    "x = -4 and x = -5",
                    "x = -4 and x = 5",
                    "x = 4 and x = -5"
                ],
                "solution": 0,
                "rationale": "x^2 - 9x + 20 = (x - 4)(x - 5)=0 ⇒ x=4,5.",
            },
            {
                "stem": "Solve by factoring: x^2 + 8x + 15 = 0.",
                "choices": [
                    "x = -3 and x = -5",
                    "x = 3 and x = 5",
                    "x = -3 and x = 5",
                    "x = 3 and x = -5"
                ],
                "solution": 0,
                "rationale": "x^2 + 8x + 15 = (x + 3)(x + 5)=0 ⇒ x=−3,−5.",
            },
            {
                "stem": "Solve by factoring: x^2 - x - 6 = 0.",
                "choices": [
                    "x = 3 and x = -2",
                    "x = -3 and x = 2",
                    "x = 3 and x = 2",
                    "x = -3 and x = -2"
                ],
                "solution": 0,
                "rationale": "x^2 - x - 6 = (x - 3)(x + 2)=0 ⇒ x=3,−2.",
            },
            {
                "stem": "Solve by factoring: x^2 + 3x - 10 = 0.",
                "choices": [
                    "x = 2 and x = -5",
                    "x = -2 and x = 5",
                    "x = 2 and x = 5",
                    "x = -2 and x = -5"
                ],
                "solution": 0,
                "rationale": "x^2 + 3x - 10 = (x + 5)(x - 2)=0 ⇒ x=−5,2.",
            },
            {
                "stem": "Solve by factoring: x^2 - 6x + 8 = 0.",
                "choices": [
                    "x = 2 and x = 4",
                    "x = -2 and x = -4",
                    "x = -2 and x = 4",
                    "x = 2 and x = -4"
                ],
                "solution": 0,
                "rationale": "x^2 - 6x + 8 = (x - 2)(x - 4)=0 ⇒ x=2,4.",
            },
            {
                "stem": "Solve by factoring: x^2 + 9x + 14 = 0.",
                "choices": [
                    "x = -2 and x = -7",
                    "x = 2 and x = 7",
                    "x = -2 and x = 7",
                    "x = 2 and x = -7"
                ],
                "solution": 0,
                "rationale": "x^2 + 9x + 14 = (x + 2)(x + 7)=0 ⇒ x=−2,−7.",
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
            {
                "stem": "Solve by factoring: 2x^2 - 5x - 3 = 0.",
                "choices": [
                    "x = 3 and x = -\tfrac{1}{2}",
                    "x = -3 and x = \tfrac{1}{2}",
                    "x = 3 and x = \tfrac{1}{2}",
                    "x = -3 and x = -\tfrac{1}{2}"
                ],
                "solution": 0,
                "rationale": "2x^2 - 5x - 3 = (2x + 1)(x - 3)=0 ⇒ x=−1/2,3.",
            },
            {
                "stem": "Solve by factoring: 3x^2 + 10x + 8 = 0.",
                "choices": [
                    "x = -\tfrac{4}{3} and x = -2",
                    "x = \tfrac{4}{3} and x = 2",
                    "x = -\tfrac{2}{3} and x = -4",
                    "x = \tfrac{2}{3} and x = 4"
                ],
                "solution": 0,
                "rationale": "3x^2 + 10x + 8 = (3x + 4)(x + 2)=0 ⇒ x=−4/3,−2.",
            },
            {
                "stem": "Solve by factoring: 2x^2 + 9x + 4 = 0.",
                "choices": [
                    "x = -\tfrac{1}{2} and x = -4",
                    "x = \tfrac{1}{2} and x = 4",
                    "x = -\tfrac{4}{2} and x = -1",
                    "x = \tfrac{4}{2} and x = 1"
                ],
                "solution": 0,
                "rationale": "2x^2 + 9x + 4 = (2x + 1)(x + 4)=0 ⇒ x=−1/2,−4.",
            },
            {
                "stem": "Solve by factoring: 5x^2 + 13x + 6 = 0.",
                "choices": [
                    "x = -\tfrac{2}{5} and x = -3",
                    "x = \tfrac{2}{5} and x = 3",
                    "x = -\tfrac{3}{5} and x = -2",
                    "x = \tfrac{3}{5} and x = 2"
                ],
                "solution": 0,
                "rationale": "5x^2 + 13x + 6 = (5x + 3)(x + 2)=0 ⇒ x=−3/5,−2.",
            },
            {
                "stem": "Solve by factoring: 3x^2 - 11x + 6 = 0.",
                "choices": [
                    "x = 3 and x = \tfrac{2}{3}",
                    "x = -3 and x = -\tfrac{2}{3}",
                    "x = 3 and x = -\tfrac{2}{3}",
                    "x = -3 and x = \tfrac{2}{3}"
                ],
                "solution": 0,
                "rationale": "3x^2 - 11x + 6 = (3x - 2)(x - 3)=0 ⇒ x=2/3,3.",
            },
            {
                "stem": "Solve by factoring: 4x^2 + 11x + 6 = 0.",
                "choices": [
                    "x = -\tfrac{3}{4} and x = -2",
                    "x = \tfrac{3}{4} and x = 2",
                    "x = -\tfrac{2}{4} and x = -3",
                    "x = \tfrac{2}{4} and x = 3"
                ],
                "solution": 0,
                "rationale": "4x^2 + 11x + 6 = (4x + 3)(x + 2)=0 ⇒ x=−3/4,−2.",
            },
            {
                "stem": "Solve by factoring: 2x^2 - 7x + 5 = 0.",
                "choices": [
                    "x = \tfrac{5}{2} and x = 1",
                    "x = -\tfrac{5}{2} and x = -1",
                    "x = \tfrac{5}{2} and x = -1",
                    "x = -\tfrac{5}{2} and x = 1"
                ],
                "solution": 0,
                "rationale": "2x^2 - 7x + 5 = (2x - 5)(x - 1)=0 ⇒ x=5/2,1.",
            },
            {
                "stem": "Solve by factoring: 3x^2 + 7x + 2 = 0.",
                "choices": [
                    "x = -\tfrac{1}{3} and x = -2",
                    "x = \tfrac{1}{3} and x = 2",
                    "x = -\tfrac{2}{3} and x = -1",
                    "x = \tfrac{2}{3} and x = 1"
                ],
                "solution": 0,
                "rationale": "3x^2 + 7x + 2 = (3x + 1)(x + 2)=0 ⇒ x=−1/3,−2.",
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
            {
                "stem": "Solve by factoring: 4x^2 + 4x + 1 = 0.",
                "choices": [
                    "x = -\tfrac{1}{2}",
                    "x = \tfrac{1}{2}",
                    "x = -1 and x = -1",
                    "x = 1 and x = 1"
                ],
                "solution": 0,
                "rationale": "4x^2 + 4x + 1 = (2x + 1)^2=0 ⇒ x=−1/2 (double root).",
            },
            {
                "stem": "Solve by factoring: 8x^2 - 14x + 3 = 0.",
                "choices": [
                    "x = \tfrac{3}{2} and x = \tfrac{1}{4}",
                    "x = -\tfrac{3}{2} and x = -\tfrac{1}{4}",
                    "x = \tfrac{3}{4} and x = \tfrac{1}{2}",
                    "x = -\tfrac{3}{4} and x = -\tfrac{1}{2}"
                ],
                "solution": 0,
                "rationale": "8x^2 - 14x + 3 = (4x - 1)(2x - 3)=0 ⇒ x=1/4, 3/2.",
            },
            {
                "stem": "Solve by factoring: 6x^2 - 17x + 5 = 0.",
                "choices": [
                    "x = \tfrac{1}{3} and x = \tfrac{5}{2}",
                    "x = -\tfrac{1}{3} and x = -\tfrac{5}{2}",
                    "x = \tfrac{1}{2} and x = \tfrac{5}{3}",
                    "x = -\tfrac{1}{2} and x = -\tfrac{5}{3}"
                ],
                "solution": 0,
                "rationale": "6x^2 - 17x + 5 = (6x - 5)(x - 1) = (2x - 5)(3x - 1)=0 ⇒ x=5/2, 1/3.",
            },
            {
                "stem": "Solve by factoring: 25x^2 - 10x + 1 = 0.",
                "choices": [
                    "x = \tfrac{1}{5}",
                    "x = -\tfrac{1}{5}",
                    "x = 5 and x = -5",
                    "x = 1 and x = -1"
                ],
                "solution": 0,
                "rationale": "25x^2 - 10x + 1 = (5x - 1)^2=0 ⇒ x=1/5 (double root).",
            },
            {
                "stem": "Solve by factoring: 12x^2 + 17x + 6 = 0.",
                "choices": [
                    "x = -\tfrac{2}{3} and x = -\tfrac{3}{4}",
                    "x = \tfrac{2}{3} and x = \tfrac{3}{4}",
                    "x = -\tfrac{3}{2} and x = -\tfrac{4}{3}",
                    "x = \tfrac{3}{2} and x = \tfrac{4}{3}"
                ],
                "solution": 0,
                "rationale": "12x^2 + 17x + 6 = (3x + 2)(4x + 3)=0 ⇒ x=−2/3, −3/4.",
            },
            {
                "stem": "Solve by factoring: 10x^2 - 19x + 6 = 0.",
                "choices": [
                    "x = \tfrac{2}{5} and x = \tfrac{3}{2}",
                    "x = -\tfrac{2}{5} and x = -\tfrac{3}{2}",
                    "x = \tfrac{5}{2} and x = \tfrac{2}{3}",
                    "x = -\tfrac{5}{2} and x = -\tfrac{2}{3}"
                ],
                "solution": 0,
                "rationale": "10x^2 - 19x + 6 = (5x - 2)(2x - 3)=0 ⇒ x=2/5, 3/2.",
            },
            {
                "stem": "Solve by factoring: 16x^2 + 8x + 1 = 0.",
                "choices": [
                    "x = -\tfrac{1}{4}",
                    "x = \tfrac{1}{4}",
                    "x = -4 and x = 4",
                    "x = -2 and x = 2"
                ],
                "solution": 0,
                "rationale": "16x^2 + 8x + 1 = (4x + 1)^2=0 ⇒ x=−1/4 (double root).",
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
            {
                "stem": "A garden has dimensions x and x+7 with area 60 square feet. What is the positive value of x?",
                "choices": [
                    "x = 5",
                    "x = 12",
                    "x = 10",
                    "x = 6"
                ],
                "solution": 0,
                "rationale": "x(x+7)=60 ⇒ x^2+7x−60=0 ⇒ (x+12)(x−5)=0 ⇒ x=−12 or 5. Positive length ⇒ x=5.",
            },
            {
                "stem": "A box has length 2x and width x with area 32. Find the positive value of x.",
                "choices": [
                    "x = 4",
                    "x = 8",
                    "x = 16",
                    "x = 2"
                ],
                "solution": 0,
                "rationale": "2x·x=32 ⇒ 2x^2=32 ⇒ x^2=16 ⇒ x^2−16=0 ⇒ (x−4)(x+4)=0 ⇒ x=4.",
            },
            {
                "stem": "The product of two consecutive integers is 56. Find the positive integer.",
                "choices": [
                    "x = 7",
                    "x = 8",
                    "x = 14",
                    "x = 4"
                ],
                "solution": 0,
                "rationale": "x(x+1)=56 ⇒ x^2+x−56=0 ⇒ (x+8)(x−7)=0 ⇒ x=−8 or 7. Positive ⇒ x=7.",
            },
            {
                "stem": "A triangle has base x and height x+3 with area 27. Find x.",
                "choices": [
                    "x = 6",
                    "x = 9",
                    "x = 3",
                    "x = 12"
                ],
                "solution": 0,
                "rationale": "Area = (1/2)·x·(x+3)=27 ⇒ x(x+3)=54 ⇒ x^2+3x−54=0 ⇒ (x+9)(x−6)=0 ⇒ x=6.",
            },
            {
                "stem": "A square has side length x. If the area is 49, what is x?",
                "choices": [
                    "x = 7",
                    "x = 49",
                    "x = 14",
                    "x = 24.5"
                ],
                "solution": 0,
                "rationale": "x^2=49 ⇒ x^2−49=0 ⇒ (x−7)(x+7)=0 ⇒ x=7 (positive).",
            },
            {
                "stem": "The product of two consecutive even integers is 80. Find the smaller positive integer.",
                "choices": [
                    "x = 8",
                    "x = 10",
                    "x = 6",
                    "x = 4"
                ],
                "solution": 0,
                "rationale": "x(x+2)=80 ⇒ x^2+2x−80=0 ⇒ (x+10)(x−8)=0 ⇒ x=8.",
            },
            {
                "stem": "A rectangular field has length 3x and width x with area 75. Find x.",
                "choices": [
                    "x = 5",
                    "x = 15",
                    "x = 25",
                    "x = 3"
                ],
                "solution": 0,
                "rationale": "3x·x=75 ⇒ 3x^2=75 ⇒ x^2=25 ⇒ x^2−25=0 ⇒ (x−5)(x+5)=0 ⇒ x=5.",
            },
            {
                "stem": "A projectile's height follows h(t) = -16t^2 + 64t. When does it hit the ground (h=0)?",
                "choices": [
                    "t = 4 seconds",
                    "t = 2 seconds",
                    "t = 8 seconds",
                    "t = 16 seconds"
                ],
                "solution": 0,
                "rationale": "−16t^2+64t=0 ⇒ −16t(t−4)=0 ⇒ t=0 or t=4. Ground return ⇒ t=4 s.",
            },
            {
                "stem": "The sum of a number and its square is 72. Find the positive number.",
                "choices": [
                    "x = 8",
                    "x = 9",
                    "x = 6",
                    "x = 12"
                ],
                "solution": 0,
                "rationale": "x+x^2=72 ⇒ x^2+x−72=0 ⇒ (x+9)(x−8)=0 ⇒ x=8 (positive).",
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
            {
                "stem": "Solve using the quadratic formula: x^2 - 7x + 12 = 0.",
                "choices": [
                    "x = 3 and x = 4",
                    "x = -3 and x = -4",
                    "x = 3 and x = -4",
                    "x = -3 and x = 4"
                ],
                "solution": 0,
                "rationale": "a=1,b=−7,c=12 ⇒ Δ=49−48=1 ⇒ x=(7±1)/2 ⇒ 3,4.",
            },
            {
                "stem": "Solve using the quadratic formula: x^2 + 2x - 3 = 0.",
                "choices": [
                    "x = 1 and x = -3",
                    "x = -1 and x = 3",
                    "x = 1 and x = 3",
                    "x = -1 and x = -3"
                ],
                "solution": 0,
                "rationale": "a=1,b=2,c=−3 ⇒ Δ=4+12=16 ⇒ x=(−2±4)/2 ⇒ 1,−3.",
            },
            {
                "stem": "Solve using the quadratic formula: x^2 - 9x + 20 = 0.",
                "choices": [
                    "x = 4 and x = 5",
                    "x = -4 and x = -5",
                    "x = 2 and x = 10",
                    "x = -2 and x = -10"
                ],
                "solution": 0,
                "rationale": "a=1,b=−9,c=20 ⇒ Δ=81−80=1 ⇒ x=(9±1)/2 ⇒ 4,5.",
            },
            {
                "stem": "Solve using the quadratic formula: x^2 + 6x + 8 = 0.",
                "choices": [
                    "x = -2 and x = -4",
                    "x = 2 and x = 4",
                    "x = -2 and x = 4",
                    "x = 2 and x = -4"
                ],
                "solution": 0,
                "rationale": "a=1,b=6,c=8 ⇒ Δ=36−32=4 ⇒ x=(−6±2)/2 ⇒ −2,−4.",
            },
            {
                "stem": "Solve using the quadratic formula: x^2 - 3x + 2 = 0.",
                "choices": [
                    "x = 1 and x = 2",
                    "x = -1 and x = -2",
                    "x = 1 and x = -2",
                    "x = -1 and x = 2"
                ],
                "solution": 0,
                "rationale": "a=1,b=−3,c=2 ⇒ Δ=9−8=1 ⇒ x=(3±1)/2 ⇒ 1,2.",
            },
            {
                "stem": "Solve using the quadratic formula: x^2 + 8x + 15 = 0.",
                "choices": [
                    "x = -3 and x = -5",
                    "x = 3 and x = 5",
                    "x = -3 and x = 5",
                    "x = 3 and x = -5"
                ],
                "solution": 0,
                "rationale": "a=1,b=8,c=15 ⇒ Δ=64−60=4 ⇒ x=(−8±2)/2 ⇒ −3,−5.",
            },
            {
                "stem": "Solve using the quadratic formula: x^2 - x - 6 = 0.",
                "choices": [
                    "x = 3 and x = -2",
                    "x = -3 and x = 2",
                    "x = 3 and x = 2",
                    "x = -3 and x = -2"
                ],
                "solution": 0,
                "rationale": "a=1,b=−1,c=−6 ⇒ Δ=1+24=25 ⇒ x=(1±5)/2 ⇒ 3,−2.",
            },
            {
                "stem": "Solve using the quadratic formula: x^2 - 8x + 15 = 0.",
                "choices": [
                    "x = 3 and x = 5",
                    "x = -3 and x = -5",
                    "x = 2 and x = 6",
                    "x = 1 and x = 15"
                ],
                "solution": 0,
                "rationale": "a=1,b=−8,c=15 ⇒ Δ=64−60=4 ⇒ x=(8±2)/2 ⇒ 3,5.",
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
            {
                "stem": "Solve using the quadratic formula: x^2 + 4x + 1 = 0.",
                "choices": [
                    "x = -2 + √3 and x = -2 - √3",
                    "x = 2 + √3 and x = 2 - √3",
                    "x = -4 + √3 and x = -4 - √3",
                    "x = -2 + √5 and x = -2 - √5"
                ],
                "solution": 0,
                "rationale": "a=1,b=4,c=1 ⇒ Δ=16−4=12 ⇒ x=(−4±√12)/2=(−4±2√3)/2=−2±√3.",
            },
            {
                "stem": "Solve using the quadratic formula: x^2 - 6x + 7 = 0.",
                "choices": [
                    "x = 3 + √2 and x = 3 - √2",
                    "x = -3 + √2 and x = -3 - √2",
                    "x = 3 + √3 and x = 3 - √3",
                    "x = 6 + √2 and x = 6 - √2"
                ],
                "solution": 0,
                "rationale": "a=1,b=−6,c=7 ⇒ Δ=36−28=8 ⇒ x=(6±√8)/2=(6±2√2)/2=3±√2.",
            },
            {
                "stem": "Solve using the quadratic formula: 3x^2 - 2x - 2 = 0.",
                "choices": [
                    "x = \\tfrac{1 + \\sqrt{7}}{3} and x = \\tfrac{1 - \\sqrt{7}}{3}",
                    "x = 1 + √7 and x = 1 - √7",
                    "x = \\tfrac{2 + \\sqrt{7}}{3} and x = \\tfrac{2 - \\sqrt{7}}{3}",
                    "x = \\tfrac{1 + \\sqrt{5}}{3} and x = \\tfrac{1 - \\sqrt{5}}{3}"
                ],
                "solution": 0,
                "rationale": "a=3,b=−2,c=−2 ⇒ Δ=4+24=28 ⇒ x=(2±√28)/6=(2±2√7)/6=(1±√7)/3.",
            },
            {
                "stem": "Solve using the quadratic formula: x^2 + 2x - 5 = 0.",
                "choices": [
                    "x = -1 + √6 and x = -1 - √6",
                    "x = 1 + √6 and x = 1 - √6",
                    "x = -1 + √5 and x = -1 - √5",
                    "x = -2 + √6 and x = -2 - √6"
                ],
                "solution": 0,
                "rationale": "a=1,b=2,c=−5 ⇒ Δ=4+20=24 ⇒ x=(−2±√24)/2=(−2±2√6)/2=−1±√6.",
            },
            {
                "stem": "Solve using the quadratic formula: 2x^2 - 4x - 1 = 0.",
                "choices": [
                    "x = \\tfrac{2 + \\sqrt{6}}{2} and x = \\tfrac{2 - \\sqrt{6}}{2}",
                    "x = 2 + √6 and x = 2 - √6",
                    "x = 1 + √6 and x = 1 - √6",
                    "x = \\tfrac{1 + \\sqrt{6}}{2} and x = \\tfrac{1 - \\sqrt{6}}{2}"
                ],
                "solution": 0,
                "rationale": "a=2,b=−4,c=−1 ⇒ Δ=16+8=24 ⇒ x=(4±√24)/4=(4±2√6)/4=(2±√6)/2.",
            },
            {
                "stem": "Solve using the quadratic formula: x^2 - 8x + 14 = 0.",
                "choices": [
                    "x = 4 + √2 and x = 4 - √2",
                    "x = 8 + √2 and x = 8 - √2",
                    "x = 4 + √3 and x = 4 - √3",
                    "x = -4 + √2 and x = -4 - √2"
                ],
                "solution": 0,
                "rationale": "a=1,b=−8,c=14 ⇒ Δ=64−56=8 ⇒ x=(8±√8)/2=(8±2√2)/2=4±√2.",
            },
            {
                "stem": "Solve using the quadratic formula: 3x^2 + 6x - 1 = 0.",
                "choices": [
                    "x = \\tfrac{-3 + \\sqrt{12}}{3} and x = \\tfrac{-3 - \\sqrt{12}}{3}",
                    "x = -1 + √12 and x = -1 - √12",
                    "x = \\tfrac{-6 + \\sqrt{12}}{6} and x = \\tfrac{-6 - \\sqrt{12}}{6}",
                    "x = \\tfrac{3 + \\sqrt{12}}{3} and x = \\tfrac{3 - \\sqrt{12}}{3}"
                ],
                "solution": 0,
                "rationale": "a=3,b=6,c=−1 ⇒ Δ=36+12=48 ⇒ x=(−6±√48)/6=(−6±4√3)/6=(−3±2√3)/3.",
            },
            {
                "stem": "Solve using the quadratic formula: x^2 + 10x + 23 = 0.",
                "choices": [
                    "x = -5 + √2 and x = -5 - √2",
                    "x = 5 + √2 and x = 5 - √2",
                    "x = -10 + √2 and x = -10 - √2",
                    "x = -5 + √3 and x = -5 - √3"
                ],
                "solution": 0,
                "rationale": "a=1,b=10,c=23 ⇒ Δ=100−92=8 ⇒ x=(−10±√8)/2=(−10±2√2)/2=−5±√2.",
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
            {
                "stem": "Solve using the quadratic formula: 5x^2 + 2x + 3 = 0.",
                "choices": [
                    "No real solutions",
                    "x = \\tfrac{-1 + \\sqrt{14}}{5} and x = \\tfrac{-1 - \\sqrt{14}}{5}",
                    "x = \\tfrac{-2 + \\sqrt{56}}{10} and x = \\tfrac{-2 - \\sqrt{56}}{10}",
                    "x = -\\tfrac{3}{5} and x = -1"
                ],
                "solution": 0,
                "rationale": "a=5,b=2,c=3 ⇒ Δ=4−60=−56<0 ⇒ no real roots.",
            },
            {
                "stem": "Solve using the quadratic formula: 4x^2 - 12x + 9 = 0.",
                "choices": [
                    "x = \\tfrac{3}{2} (double root)",
                    "x = \\tfrac{3}{4} and x = 3",
                    "x = 3 and x = -\\tfrac{3}{4}",
                    "x = \\tfrac{9}{4} and x = 1"
                ],
                "solution": 0,
                "rationale": "a=4,b=−12,c=9 ⇒ Δ=144−144=0 ⇒ x=12/8=3/2 (repeated root).",
            },
            {
                "stem": "Solve using the quadratic formula: \\tfrac{1}{2}x^2 + x - 3 = 0.",
                "choices": [
                    "x = -1 + √7 and x = -1 - √7",
                    "x = 1 + √7 and x = 1 - √7",
                    "x = -2 + √7 and x = -2 - √7",
                    "x = 2 and x = -3"
                ],
                "solution": 0,
                "rationale": "a=1/2,b=1,c=−3 ⇒ Δ=1+6=7 ⇒ x=(−1±√7)/1=−1±√7.",
            },
            {
                "stem": "Solve using the quadratic formula: 2x^2 + 5x + 4 = 0.",
                "choices": [
                    "No real solutions",
                    "x = \\tfrac{-5 + \\sqrt{7}}{4} and x = \\tfrac{-5 - \\sqrt{7}}{4}",
                    "x = -1 and x = -2",
                    "x = \\tfrac{-5}{4} and x = -1"
                ],
                "solution": 0,
                "rationale": "a=2,b=5,c=4 ⇒ Δ=25−32=−7<0 ⇒ no real roots.",
            },
            {
                "stem": "Solve using the quadratic formula: 9x^2 - 6x + 1 = 0.",
                "choices": [
                    "x = \\tfrac{1}{3} (double root)",
                    "x = \\tfrac{1}{3} and x = \\tfrac{1}{9}",
                    "x = 1 and x = \\tfrac{1}{9}",
                    "x = 3 and x = -\\tfrac{1}{3}"
                ],
                "solution": 0,
                "rationale": "a=9,b=−6,c=1 ⇒ Δ=36−36=0 ⇒ x=6/18=1/3 (repeated root).",
            },
            {
                "stem": "Solve using the quadratic formula: 3x^2 + 5x - 1 = 0.",
                "choices": [
                    "x = \\tfrac{-5 + \\sqrt{37}}{6} and x = \\tfrac{-5 - \\sqrt{37}}{6}",
                    "x = \\tfrac{5 + \\sqrt{37}}{6} and x = \\tfrac{5 - \\sqrt{37}}{6}",
                    "x = \\tfrac{-5 + \\sqrt{13}}{6} and x = \\tfrac{-5 - \\sqrt{13}}{6}",
                    "x = \\tfrac{1}{3} and x = -1"
                ],
                "solution": 0,
                "rationale": "a=3,b=5,c=−1 ⇒ Δ=25+12=37 ⇒ x=(−5±√37)/6.",
            },
            {
                "stem": "Solve using the quadratic formula: x^2 - 4x + 5 = 0.",
                "choices": [
                    "No real solutions",
                    "x = 2 + i and x = 2 - i",
                    "x = 2 + √5 and x = 2 - √5",
                    "x = 1 and x = 5"
                ],
                "solution": 0,
                "rationale": "a=1,b=−4,c=5 ⇒ Δ=16−20=−4<0 ⇒ no real roots.",
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
            {
                "stem": "A rectangular garden has area 60 m^2. If length is 7 m more than width w, find w using w(w+7)=60.",
                "choices": [
                    "w = 5 meters",
                    "w = 4 meters",
                    "w = 6 meters",
                    "w = 8 meters"
                ],
                "solution": 0,
                "rationale": "w^2+7w−60=0 ⇒ a=1,b=7,c=−60 ⇒ Δ=49+240=289 ⇒ w=(−7±17)/2 ⇒ 5 or −12; w>0 ⇒ 5 m.",
            },
            {
                "stem": "A ball is thrown upward with h(t) = -5t^2 + 20t. When does it reach height 15 meters?",
                "choices": [
                    "t = 1 and t = 3 seconds",
                    "t = 2 seconds only",
                    "t = 0.5 and t = 3.5 seconds",
                    "t = 1.5 and t = 2.5 seconds"
                ],
                "solution": 0,
                "rationale": "Set −5t^2+20t=15 ⇒ −5t^2+20t−15=0 ⇒ t^2−4t+3=0 ⇒ Δ=16−12=4 ⇒ t=(4±2)/2 ⇒ 1,3 s.",
            },
            {
                "stem": "The profit P (in thousands) from selling x items is P(x) = -2x^2 + 16x - 24. How many items maximize profit?",
                "choices": [
                    "x = 4 items",
                    "x = 2 items",
                    "x = 6 items",
                    "x = 8 items"
                ],
                "solution": 0,
                "rationale": "Vertex formula: x=−b/(2a)=−16/(−4)=4. Or set derivative 0: −4x+16=0 ⇒ x=4.",
            },
            {
                "stem": "A farmer has 100 m of fence to enclose a rectangular area. If area A = x(50-x), what width x gives area 600 m^2?",
                "choices": [
                    "x = 20 or x = 30 meters",
                    "x = 15 or x = 40 meters",
                    "x = 10 or x = 50 meters",
                    "x = 25 meters"
                ],
                "solution": 0,
                "rationale": "x(50−x)=600 ⇒ 50x−x^2=600 ⇒ x^2−50x+600=0 ⇒ Δ=2500−2400=100 ⇒ x=(50±10)/2 ⇒ 20,30 m.",
            },
            {
                "stem": "An object falls from height h(t) = -4.9t^2 + 44.1t + 10. When is it at height 58.8 meters?",
                "choices": [
                    "t = 2 and t = 7 seconds",
                    "t = 3 and t = 6 seconds",
                    "t = 1 and t = 8 seconds",
                    "t = 4 and t = 5 seconds"
                ],
                "solution": 0,
                "rationale": "Set −4.9t^2+44.1t+10=58.8 ⇒ −4.9t^2+44.1t−48.8=0 ⇒ divide by −0.1 ⇒ 49t^2−441t+488=0 ⇒ 7t^2−63t+140=0 ⇒ t=2,7.",
            },
            {
                "stem": "A company's revenue R (in millions) is R(x) = -x^2 + 10x - 16, where x is years since 2020. When is R = 0?",
                "choices": [
                    "x = 2 and x = 8 (years 2022 and 2028)",
                    "x = 4 and x = 6 (years 2024 and 2026)",
                    "x = 1 and x = 9 (years 2021 and 2029)",
                    "x = 3 and x = 7 (years 2023 and 2027)"
                ],
                "solution": 0,
                "rationale": "Set −x^2+10x−16=0 ⇒ x^2−10x+16=0 ⇒ Δ=100−64=36 ⇒ x=(10±6)/2 ⇒ 2,8.",
            },
            {
                "stem": "A bridge's arch follows y = -0.5x^2 + 4x. At what horizontal distances x does the arch meet the ground (y=0)?",
                "choices": [
                    "x = 0 and x = 8 meters",
                    "x = 2 and x = 6 meters",
                    "x = 1 and x = 7 meters",
                    "x = 4 meters only"
                ],
                "solution": 0,
                "rationale": "Set −0.5x^2+4x=0 ⇒ x(−0.5x+4)=0 ⇒ x=0 or x=8. Or factor: −0.5x^2+4x=0 ⇒ x=0,8 m.",
            },
            {
                "stem": "A product's price P and demand D satisfy D = -2P^2 + 20P - 32. At what prices is demand zero?",
                "choices": [
                    "P = $2 and P = $8",
                    "P = $4 and P = $6",
                    "P = $1 and P = $9",
                    "P = $3 and P = $7"
                ],
                "solution": 0,
                "rationale": "Set −2P^2+20P−32=0 ⇒ P^2−10P+16=0 ⇒ Δ=100−64=36 ⇒ P=(10±6)/2 ⇒ 2,8.",
            },
            {
                "stem": "A diver's depth below surface is d(t) = 2t^2 - 12t + 10 meters. When is the diver at the surface (d=0)?",
                "choices": [
                    "t = 1 and t = 5 seconds",
                    "t = 2 and t = 4 seconds",
                    "t = 3 seconds only",
                    "Never reaches surface"
                ],
                "solution": 0,
                "rationale": "Set 2t^2−12t+10=0 ⇒ t^2−6t+5=0 ⇒ Δ=36−20=16 ⇒ t=(6±4)/2 ⇒ 1,5 s.",
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
            {
                "stem": "For x^2 + 3x + 2 = 0, what is the discriminant?",
                "choices": ["1", "9", "5", "-7"],
                "solution": 0,
                "rationale": "Δ = b² - 4ac = 3² - 4(1)(2) = 9 - 8 = 1.",
            },
            {
                "stem": "For x^2 - 6x + 9 = 0, what is the discriminant?",
                "choices": ["0", "36", "9", "-9"],
                "solution": 0,
                "rationale": "Δ = b² - 4ac = (-6)² - 4(1)(9) = 36 - 36 = 0.",
            },
            {
                "stem": "For x^2 + 2x - 3 = 0, what is the discriminant?",
                "choices": ["16", "4", "10", "-8"],
                "solution": 0,
                "rationale": "Δ = b² - 4ac = 2² - 4(1)(-3) = 4 + 12 = 16.",
            },
            {
                "stem": "For x^2 - 2x + 1 = 0, what is the discriminant?",
                "choices": ["0", "4", "1", "-4"],
                "solution": 0,
                "rationale": "Δ = b² - 4ac = (-2)² - 4(1)(1) = 4 - 4 = 0.",
            },
            {
                "stem": "For x^2 + 7x + 10 = 0, what is the discriminant?",
                "choices": ["9", "49", "40", "1"],
                "solution": 0,
                "rationale": "Δ = b² - 4ac = 7² - 4(1)(10) = 49 - 40 = 9.",
            },
            {
                "stem": "For x^2 - 8x + 16 = 0, what is the discriminant?",
                "choices": ["0", "64", "16", "-16"],
                "solution": 0,
                "rationale": "Δ = b² - 4ac = (-8)² - 4(1)(16) = 64 - 64 = 0.",
            },
            {
                "stem": "For x^2 + 4x = 0, what is the discriminant?",
                "choices": ["16", "0", "4", "8"],
                "solution": 0,
                "rationale": "Δ = b² - 4ac = 4² - 4(1)(0) = 16 - 0 = 16.",
            },
            {
                "stem": "For x^2 - 10x + 25 = 0, what is the discriminant?",
                "choices": ["0", "100", "25", "-25"],
                "solution": 0,
                "rationale": "Δ = b² - 4ac = (-10)² - 4(1)(25) = 100 - 100 = 0.",
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
            {
                "stem": "What is the nature of roots for 2x^2 + 5x + 2 = 0?",
                "choices": [
                    "Two distinct real roots",
                    "One repeated real root",
                    "No real roots",
                    "Cannot determine"
                ],
                "solution": 0,
                "rationale": "Δ = 5² - 4(2)(2) = 25 - 16 = 9 > 0. Two distinct real roots.",
            },
            {
                "stem": "What is the nature of roots for x^2 + 2x + 5 = 0?",
                "choices": [
                    "No real roots",
                    "Two distinct real roots",
                    "One repeated real root",
                    "Two rational roots"
                ],
                "solution": 0,
                "rationale": "Δ = 2² - 4(1)(5) = 4 - 20 = -16 < 0. No real roots.",
            },
            {
                "stem": "For 3x^2 - 6x + 3 = 0, what is the discriminant?",
                "choices": ["0", "36", "12", "-12"],
                "solution": 0,
                "rationale": "Δ = (-6)² - 4(3)(3) = 36 - 36 = 0.",
            },
            {
                "stem": "What is the nature of roots for 4x^2 - 4x + 1 = 0?",
                "choices": [
                    "One repeated real root",
                    "Two distinct real roots",
                    "No real roots",
                    "Two irrational roots"
                ],
                "solution": 0,
                "rationale": "Δ = (-4)² - 4(4)(1) = 16 - 16 = 0. One repeated root.",
            },
            {
                "stem": "For x^2 + 3x + 3 = 0, what can you conclude about the roots?",
                "choices": [
                    "No real roots",
                    "Two distinct real roots",
                    "One repeated real root",
                    "Two rational roots"
                ],
                "solution": 0,
                "rationale": "Δ = 3² - 4(1)(3) = 9 - 12 = -3 < 0. No real roots.",
            },
            {
                "stem": "What is the nature of roots for 2x^2 - 8x + 8 = 0?",
                "choices": [
                    "One repeated real root",
                    "Two distinct real roots",
                    "No real roots",
                    "Cannot determine"
                ],
                "solution": 0,
                "rationale": "Δ = (-8)² - 4(2)(8) = 64 - 64 = 0. One repeated root.",
            },
            {
                "stem": "For 5x^2 + 4x - 1 = 0, what is the discriminant?",
                "choices": ["36", "16", "4", "-4"],
                "solution": 0,
                "rationale": "Δ = 4² - 4(5)(-1) = 16 + 20 = 36.",
            },
            {
                "stem": "What is the nature of roots for x^2 - 4x + 7 = 0?",
                "choices": [
                    "No real roots",
                    "Two distinct real roots",
                    "One repeated real root",
                    "Two rational roots"
                ],
                "solution": 0,
                "rationale": "Δ = (-4)² - 4(1)(7) = 16 - 28 = -12 < 0. No real roots.",
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
            {
                "stem": "For x^2 + kx + 9 = 0 to have exactly one real root, what must k equal?",
                "choices": [
                    "k = ±6",
                    "k = 3",
                    "k = 9",
                    "k = 0"
                ],
                "solution": 0,
                "rationale": "For one root: Δ = 0 ⇒ k² - 4(1)(9) = 0 ⇒ k² = 36 ⇒ k = ±6.",
            },
            {
                "stem": "If 2x^2 + bx + 8 = 0 has Δ = 0, what is the value of b?",
                "choices": [
                    "b = ±8",
                    "b = 4",
                    "b = 16",
                    "b = ±4"
                ],
                "solution": 0,
                "rationale": "Δ = 0 ⇒ b² - 4(2)(8) = 0 ⇒ b² - 64 = 0 ⇒ b = ±8.",
            },
            {
                "stem": "For x^2 - 6x + c = 0 to have two distinct real roots, what condition must c satisfy?",
                "choices": [
                    "c < 9",
                    "c > 9",
                    "c = 9",
                    "c ≠ 9"
                ],
                "solution": 0,
                "rationale": "Δ > 0 ⇒ (-6)² - 4(1)(c) > 0 ⇒ 36 - 4c > 0 ⇒ c < 9.",
            },
            {
                "stem": "If mx^2 - 4x + 1 = 0 has no real roots, what condition must m satisfy?",
                "choices": [
                    "m > 4",
                    "m < 4",
                    "m = 4",
                    "m ≠ 0"
                ],
                "solution": 0,
                "rationale": "Δ < 0 ⇒ (-4)² - 4(m)(1) < 0 ⇒ 16 - 4m < 0 ⇒ m > 4.",
            },
            {
                "stem": "For what value of k does kx^2 - 6x + k = 0 have exactly one real root?",
                "choices": [
                    "k = 3",
                    "k = 6",
                    "k = 9",
                    "k = ±3"
                ],
                "solution": 0,
                "rationale": "Δ = 0 ⇒ (-6)² - 4(k)(k) = 0 ⇒ 36 - 4k² = 0 ⇒ k² = 9 ⇒ k = ±3. Since equation requires k ≠ 0, k = 3 works (k = -3 also works).",
            },
            {
                "stem": "If x^2 + px + 25 = 0 has a repeated root, what are the possible values of p?",
                "choices": [
                    "p = ±10",
                    "p = 5",
                    "p = 25",
                    "p = ±5"
                ],
                "solution": 0,
                "rationale": "Δ = 0 ⇒ p² - 4(1)(25) = 0 ⇒ p² = 100 ⇒ p = ±10.",
            },
            {
                "stem": "For ax^2 + 4x + 1 = 0 to have two distinct real roots, what condition must a satisfy (a > 0)?",
                "choices": [
                    "0 < a < 4",
                    "a > 4",
                    "a < 4",
                    "a = 4"
                ],
                "solution": 0,
                "rationale": "Δ > 0 ⇒ 4² - 4(a)(1) > 0 ⇒ 16 - 4a > 0 ⇒ a < 4. With a > 0: 0 < a < 4.",
            },
            {
                "stem": "If 4x^2 + 12x + k = 0 has no real roots, what is the range of k?",
                "choices": [
                    "k > 9",
                    "k < 9",
                    "k = 9",
                    "k ≥ 9"
                ],
                "solution": 0,
                "rationale": "Δ < 0 ⇒ 12² - 4(4)(k) < 0 ⇒ 144 - 16k < 0 ⇒ k > 9.",
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
            {
                "stem": "A projectile's height is h(t) = -16t^2 + 64t. At how many times does it reach ground level?",
                "choices": [
                    "Two times",
                    "One time",
                    "Never",
                    "Infinitely many times"
                ],
                "solution": 0,
                "rationale": "Set h = 0: -16t² + 64t = 0. Δ = 64² - 4(-16)(0) = 4096 > 0. Two distinct times (t = 0 and t = 4).",
            },
            {
                "stem": "A company's profit is P(x) = -2x^2 + 8x + 10. How many break-even points exist?",
                "choices": [
                    "Two break-even points",
                    "One break-even point",
                    "No break-even points",
                    "Cannot determine"
                ],
                "solution": 0,
                "rationale": "Set P = 0: -2x² + 8x + 10 = 0. Δ = 8² - 4(-2)(10) = 64 + 80 = 144 > 0. Two break-even points.",
            },
            {
                "stem": "A bridge arch is modeled by y = -x^2 + 6x - 9. How many points touch the ground (y = 0)?",
                "choices": [
                    "One point",
                    "Two points",
                    "No points",
                    "Three points"
                ],
                "solution": 0,
                "rationale": "Set y = 0: -x² + 6x - 9 = 0. Δ = 6² - 4(-1)(-9) = 36 - 36 = 0. One point (tangent).",
            },
            {
                "stem": "A rocket's altitude is h(t) = -4.9t^2 + 49t + 100. Does it return to ground level?",
                "choices": [
                    "Yes, Δ > 0 indicates two intersections with ground",
                    "No, Δ < 0 means it never returns",
                    "Yes, exactly once at Δ = 0",
                    "Cannot determine"
                ],
                "solution": 0,
                "rationale": "Set h = 0: -4.9t² + 49t + 100 = 0. Δ = 49² - 4(-4.9)(100) = 2401 + 1960 = 4361 > 0. Two real solutions.",
            },
            {
                "stem": "A product's demand is D(p) = -p^2 + 10p + 11. At what price is demand zero?",
                "choices": [
                    "Two price points",
                    "One price point",
                    "No such price exists",
                    "All prices give zero demand"
                ],
                "solution": 0,
                "rationale": "Set D = 0: -p² + 10p + 11 = 0. Δ = 10² - 4(-1)(11) = 100 + 44 = 144 > 0. Two prices.",
            },
            {
                "stem": "A ball is thrown from ground level with h(t) = -16t^2 + 32t. When does it land?",
                "choices": [
                    "At t = 0 and t = 2",
                    "At t = 2 only",
                    "Never lands",
                    "At t = 1 only"
                ],
                "solution": 0,
                "rationale": "Set h = 0: -16t² + 32t = 0 ⇒ t(-16t + 32) = 0. Δ = 32² - 0 = 1024 > 0. Two times: t = 0 (launch), t = 2 (landing).",
            },
            {
                "stem": "A cable hangs as y = 0.5x^2 - 4x + 8. Does it touch the x-axis?",
                "choices": [
                    "Yes, at exactly one point",
                    "Yes, at two points",
                    "No, it stays above the x-axis",
                    "Cannot determine"
                ],
                "solution": 0,
                "rationale": "Set y = 0: 0.5x² - 4x + 8 = 0. Δ = (-4)² - 4(0.5)(8) = 16 - 16 = 0. Touches once (tangent).",
            },
            {
                "stem": "A diver's depth is d(t) = t^2 - 6t + 10. Does the diver return to the surface (d = 0)?",
                "choices": [
                    "No, Δ < 0 means depth never reaches zero",
                    "Yes, at two times",
                    "Yes, at one time",
                    "Cannot determine"
                ],
                "solution": 0,
                "rationale": "Set d = 0: t² - 6t + 10 = 0. Δ = (-6)² - 4(1)(10) = 36 - 40 = -4 < 0. No real solution (never surfaces).",
            },
            {
                "stem": "A bridge support cable follows y = 0.2x^2 - 2x + 5. Can vehicles pass under at y = 0?",
                "choices": [
                    "No, cable never reaches y = 0",
                    "Yes, at one point",
                    "Yes, at two points",
                    "Yes, at all points"
                ],
                "solution": 0,
                "rationale": "Set y = 0: 0.2x² - 2x + 5 = 0. Δ = (-2)² - 4(0.2)(5) = 4 - 4 = 0. Touches ground at one point only (barely clears).",
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
            {
                "stem": "Find the y-intercept of y = 2x^2 - 5x + 7.",
                "choices": ["7", "-7", "2", "5"],
                "solution": 0,
                "rationale": "Y-intercept occurs at x = 0: y = 2(0)² - 5(0) + 7 = 7.",
            },
            {
                "stem": "Find the x-intercepts of y = (x + 2)(x + 5).",
                "choices": [
                    "x = -2 and x = -5",
                    "x = 2 and x = 5",
                    "x = -2 and x = 5",
                    "x = 2 and x = -5"
                ],
                "solution": 0,
                "rationale": "Set y = 0: (x+2)(x+5) = 0 ⇒ x = -2 or x = -5.",
            },
            {
                "stem": "Find the y-intercept of y = -3x^2 + 4x - 1.",
                "choices": ["-1", "1", "-3", "4"],
                "solution": 0,
                "rationale": "Y-intercept occurs at x = 0: y = -3(0)² + 4(0) - 1 = -1.",
            },
            {
                "stem": "Find the x-intercepts of y = x(x - 4).",
                "choices": [
                    "x = 0 and x = 4",
                    "x = 0 and x = -4",
                    "x = 4 only",
                    "x = 0 only"
                ],
                "solution": 0,
                "rationale": "Set y = 0: x(x-4) = 0 ⇒ x = 0 or x = 4.",
            },
            {
                "stem": "Find the y-intercept of y = x^2 - 6x + 9.",
                "choices": ["9", "-9", "6", "3"],
                "solution": 0,
                "rationale": "Y-intercept occurs at x = 0: y = 0² - 6(0) + 9 = 9.",
            },
            {
                "stem": "Find the x-intercepts of y = (x - 2)(x + 7).",
                "choices": [
                    "x = 2 and x = -7",
                    "x = -2 and x = 7",
                    "x = 2 and x = 7",
                    "x = -2 and x = -7"
                ],
                "solution": 0,
                "rationale": "Set y = 0: (x-2)(x+7) = 0 ⇒ x = 2 or x = -7.",
            },
            {
                "stem": "Find the y-intercept of y = 5x^2 + 2x - 8.",
                "choices": ["-8", "8", "5", "2"],
                "solution": 0,
                "rationale": "Y-intercept occurs at x = 0: y = 5(0)² + 2(0) - 8 = -8.",
            },
            {
                "stem": "Find the x-intercepts of y = 3(x - 1)(x + 3).",
                "choices": [
                    "x = 1 and x = -3",
                    "x = -1 and x = 3",
                    "x = 1 and x = 3",
                    "x = -1 and x = -3"
                ],
                "solution": 0,
                "rationale": "Set y = 0: 3(x-1)(x+3) = 0 ⇒ x = 1 or x = -3 (the 3 is non-zero).",
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
            {
                "stem": "Find the x-intercepts of y = x^2 + 7x + 12.",
                "choices": [
                    "x = -3 and x = -4",
                    "x = 3 and x = 4",
                    "x = -2 and x = -6",
                    "x = 2 and x = 6"
                ],
                "solution": 0,
                "rationale": "Set y = 0: x² + 7x + 12 = 0 ⇒ (x+3)(x+4) = 0 ⇒ x = -3, -4.",
            },
            {
                "stem": "Find the x-intercepts of y = x^2 - 9.",
                "choices": [
                    "x = -3 and x = 3",
                    "x = -9 and x = 9",
                    "x = 0 and x = 9",
                    "x = 3 only"
                ],
                "solution": 0,
                "rationale": "Set y = 0: x² - 9 = 0 ⇒ (x-3)(x+3) = 0 ⇒ x = -3, 3.",
            },
            {
                "stem": "Find the x-intercepts of y = 2x^2 - 8x + 6.",
                "choices": [
                    "x = 1 and x = 3",
                    "x = -1 and x = -3",
                    "x = 2 and x = 4",
                    "x = -2 and x = -4"
                ],
                "solution": 0,
                "rationale": "Set y = 0: 2x² - 8x + 6 = 0 ⇒ x² - 4x + 3 = 0 ⇒ (x-1)(x-3) = 0 ⇒ x = 1, 3.",
            },
            {
                "stem": "Find both intercepts of y = x^2 + 2x - 8.",
                "choices": [
                    "y-int: -8; x-ints: x = -4, 2",
                    "y-int: 8; x-ints: x = 4, -2",
                    "y-int: -8; x-ints: x = 4, -2",
                    "y-int: 2; x-ints: x = -4, 2"
                ],
                "solution": 0,
                "rationale": "y-int: y(0) = -8. x-ints: x² + 2x - 8 = 0 ⇒ (x+4)(x-2) = 0 ⇒ x = -4, 2.",
            },
            {
                "stem": "Find the x-intercepts of y = 3x^2 - 3x - 6.",
                "choices": [
                    "x = -1 and x = 2",
                    "x = 1 and x = -2",
                    "x = -3 and x = 6",
                    "x = 3 and x = -6"
                ],
                "solution": 0,
                "rationale": "Set y = 0: 3x² - 3x - 6 = 0 ⇒ x² - x - 2 = 0 ⇒ (x+1)(x-2) = 0 ⇒ x = -1, 2.",
            },
            {
                "stem": "Find the x-intercepts of y = x^2 - 16.",
                "choices": [
                    "x = -4 and x = 4",
                    "x = -16 and x = 16",
                    "x = -2 and x = 2",
                    "x = 4 only"
                ],
                "solution": 0,
                "rationale": "Set y = 0: x² - 16 = 0 ⇒ (x-4)(x+4) = 0 ⇒ x = -4, 4.",
            },
            {
                "stem": "Find both intercepts of y = -x^2 + 4x + 5.",
                "choices": [
                    "y-int: 5; x-ints: x = -1, 5",
                    "y-int: -5; x-ints: x = 1, -5",
                    "y-int: 5; x-ints: x = 1, -5",
                    "y-int: 4; x-ints: x = -1, 5"
                ],
                "solution": 0,
                "rationale": "y-int: y(0) = 5. x-ints: -x² + 4x + 5 = 0 ⇒ x² - 4x - 5 = 0 ⇒ (x-5)(x+1) = 0.",
            },
            {
                "stem": "Find the x-intercepts of y = x^2 + x - 12.",
                "choices": [
                    "x = -4 and x = 3",
                    "x = 4 and x = -3",
                    "x = -2 and x = 6",
                    "x = 2 and x = -6"
                ],
                "solution": 0,
                "rationale": "Set y = 0: x² + x - 12 = 0 ⇒ (x+4)(x-3) = 0 ⇒ x = -4, 3.",
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
            {
                "stem": "Find the x-intercepts of y = x^2 + 4x + 5.",
                "choices": [
                    "No real x-intercepts",
                    "x = -2 and x = -3",
                    "x = -1 and x = -5",
                    "x = -2 only"
                ],
                "solution": 0,
                "rationale": "Discriminant: Δ = 16 - 20 = -4 < 0. No real roots, so no x-intercepts.",
            },
            {
                "stem": "Find both intercepts of y = 2x^2 - 4x + 2.",
                "choices": [
                    "y-int: 2; x-int: x = 1 only",
                    "y-int: 2; x-ints: x = 0, 2",
                    "y-int: -2; x-int: x = 1 only",
                    "y-int: 2; x-ints: x = -1, 1"
                ],
                "solution": 0,
                "rationale": "y-int: y(0) = 2. x-ints: 2x² - 4x + 2 = 0 ⇒ x² - 2x + 1 = 0 ⇒ (x-1)² = 0 ⇒ x = 1.",
            },
            {
                "stem": "For what value of c does y = x^2 + 6x + c have x-intercepts at x = -2 and x = -4?",
                "choices": ["8", "-8", "6", "24"],
                "solution": 0,
                "rationale": "If x-ints are -2, -4, then y = (x+2)(x+4) = x² + 6x + 8. So c = 8.",
            },
            {
                "stem": "Find the x-intercepts of y = x^2 - 2x + 3.",
                "choices": [
                    "No real x-intercepts",
                    "x = 1 and x = 3",
                    "x = -1 and x = -3",
                    "x = 1 only"
                ],
                "solution": 0,
                "rationale": "Discriminant: Δ = 4 - 12 = -8 < 0. No real roots, so no x-intercepts.",
            },
            {
                "stem": "Find both intercepts of y = -2x^2 + 8x - 8.",
                "choices": [
                    "y-int: -8; x-int: x = 2 only",
                    "y-int: -8; x-ints: x = 1, 4",
                    "y-int: 8; x-int: x = 2 only",
                    "y-int: -8; x-ints: x = -2, 2"
                ],
                "solution": 0,
                "rationale": "y-int: y(0) = -8. x-ints: -2x² + 8x - 8 = 0 ⇒ x² - 4x + 4 = 0 ⇒ (x-2)² = 0.",
            },
            {
                "stem": "How many x-intercepts does y = 4x^2 + 12x + 9 have?",
                "choices": [
                    "One (repeated root)",
                    "Two distinct intercepts",
                    "No x-intercepts",
                    "Three intercepts"
                ],
                "solution": 0,
                "rationale": "4x² + 12x + 9 = (2x + 3)² = 0 ⇒ x = -3/2 (one repeated root).",
            },
            {
                "stem": "For y = x^2 - 4x + c, what value of c makes the graph tangent to the x-axis?",
                "choices": ["4", "-4", "2", "0"],
                "solution": 0,
                "rationale": "Tangent to x-axis means one repeated root: Δ = 0 ⇒ 16 - 4c = 0 ⇒ c = 4.",
            },
            {
                "stem": "Find both intercepts of y = -x^2 + 6x - 9.",
                "choices": [
                    "y-int: -9; x-int: x = 3 only",
                    "y-int: -9; x-ints: x = 1, 9",
                    "y-int: 9; x-int: x = 3 only",
                    "y-int: -9; x-ints: x = -3, 3"
                ],
                "solution": 0,
                "rationale": "y-int: y(0) = -9. x-ints: -x² + 6x - 9 = 0 ⇒ x² - 6x + 9 = 0 ⇒ (x-3)² = 0.",
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
            {
                "stem": "A company's profit is P(x) = -2x^2 + 50x - 200 dollars. What sales levels give break-even (P = 0)?",
                "choices": [
                    "x = 5 and x = 20",
                    "x = 10 only",
                    "x = 4 and x = 25",
                    "x = 2 and x = 50"
                ],
                "solution": 0,
                "rationale": "Break-even: -2x² + 50x - 200 = 0 ⇒ x² - 25x + 100 = 0. Use quadratic formula or factor: (x-5)(x-20) = 0 ⇒ x = 5, 20.",
            },
            {
                "stem": "A ball is thrown with height h(t) = -5t^2 + 20t. At what times is the ball at ground level?",
                "choices": [
                    "t = 0 and t = 4",
                    "t = 4 only",
                    "t = 0 and t = 20",
                    "t = 5 only"
                ],
                "solution": 0,
                "rationale": "Ground level: h = 0. So -5t² + 20t = 0 ⇒ -5t(t - 4) = 0 ⇒ t = 0, 4.",
            },
            {
                "stem": "A bridge arch is modeled by h(x) = -0.5x^2 + 8 where h is height. What are the x-intercepts?",
                "choices": [
                    "x = -4 and x = 4",
                    "x = -8 and x = 8",
                    "x = -16 and x = 16",
                    "x = 0 and x = 8"
                ],
                "solution": 0,
                "rationale": "At ground: h = 0. So -0.5x² + 8 = 0 ⇒ x² = 16 ⇒ x = ±4.",
            },
            {
                "stem": "Revenue is R(p) = -3p^2 + 60p dollars at price p. What prices give zero revenue?",
                "choices": [
                    "p = 0 and p = 20",
                    "p = 20 only",
                    "p = 0 and p = 60",
                    "p = 3 only"
                ],
                "solution": 0,
                "rationale": "Zero revenue: R = 0. So -3p² + 60p = 0 ⇒ -3p(p - 20) = 0 ⇒ p = 0, 20.",
            },
            {
                "stem": "A diver's depth is d(t) = t^2 - 10t + 24 feet. When is the diver at the surface (d = 0)?",
                "choices": [
                    "t = 4 and t = 6",
                    "t = 3 and t = 8",
                    "t = 2 and t = 12",
                    "t = 5 only"
                ],
                "solution": 0,
                "rationale": "Surface: d = 0. So t² - 10t + 24 = 0 ⇒ (t-4)(t-6) = 0 ⇒ t = 4, 6.",
            },
            {
                "stem": "A rocket's altitude is h(t) = -16t^2 + 64t feet. What is the initial height (y-intercept)?",
                "choices": [
                    "0 feet",
                    "64 feet",
                    "16 feet",
                    "48 feet"
                ],
                "solution": 0,
                "rationale": "Initial height at t = 0: h(0) = -16(0)² + 64(0) = 0 feet.",
            },
            {
                "stem": "Cost to produce x items is C(x) = x^2 - 12x + 32 dollars. For what x values is cost zero?",
                "choices": [
                    "x = 4 and x = 8",
                    "x = 2 and x = 16",
                    "x = 3 and x = 10",
                    "x = 6 only"
                ],
                "solution": 0,
                "rationale": "Zero cost: C = 0. So x² - 12x + 32 = 0 ⇒ (x-4)(x-8) = 0 ⇒ x = 4, 8.",
            },
            {
                "stem": "A fountain's water height is h(x) = -x^2 + 4x + 5. What is the height at the center (x = 0)?",
                "choices": [
                    "5 units",
                    "4 units",
                    "9 units",
                    "0 units"
                ],
                "solution": 0,
                "rationale": "At center x = 0: h(0) = -0² + 4(0) + 5 = 5 units (y-intercept).",
            },
            {
                "stem": "A ball's path is h(t) = -4.9t^2 + 19.6t. When does it return to ground level?",
                "choices": [
                    "t = 0 and t = 4",
                    "t = 4 only",
                    "t = 0 and t = 19.6",
                    "t = 2 only"
                ],
                "solution": 0,
                "rationale": "Ground level: h = 0. So -4.9t² + 19.6t = 0 ⇒ t(-4.9t + 19.6) = 0 ⇒ t = 0, 4.",
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
            {
                "stem": "Complete the square for x^2 + 4x.",
                "choices": [
                    "(x + 2)^2 - 4",
                    "(x + 2)^2 + 4",
                    "(x - 2)^2 - 4",
                    "(x + 4)^2 - 16"
                ],
                "solution": 0,
                "rationale": "x² + 4x = (x + 2)² - 4. Take half of 4, square it: (4/2)² = 4.",
            },
            {
                "stem": "Complete the square for x^2 - 10x.",
                "choices": [
                    "(x - 5)^2 - 25",
                    "(x + 5)^2 - 25",
                    "(x - 5)^2 + 25",
                    "(x - 10)^2 - 100"
                ],
                "solution": 0,
                "rationale": "x² - 10x = (x - 5)² - 25. Take half of -10, square it: (-10/2)² = 25.",
            },
            {
                "stem": "Complete the square for x^2 + 2x.",
                "choices": [
                    "(x + 1)^2 - 1",
                    "(x + 1)^2 + 1",
                    "(x - 1)^2 - 1",
                    "(x + 2)^2 - 4"
                ],
                "solution": 0,
                "rationale": "x² + 2x = (x + 1)² - 1. Take half of 2, square it: (2/2)² = 1.",
            },
            {
                "stem": "Complete the square for x^2 - 12x.",
                "choices": [
                    "(x - 6)^2 - 36",
                    "(x + 6)^2 - 36",
                    "(x - 6)^2 + 36",
                    "(x - 12)^2 - 144"
                ],
                "solution": 0,
                "rationale": "x² - 12x = (x - 6)² - 36. Take half of -12, square it: (-12/2)² = 36.",
            },
            {
                "stem": "Complete the square for x^2 + 8x + 7.",
                "choices": [
                    "(x + 4)^2 - 9",
                    "(x + 4)^2 + 9",
                    "(x - 4)^2 - 9",
                    "(x + 8)^2 - 57"
                ],
                "solution": 0,
                "rationale": "x² + 8x + 7 = (x + 4)² - 16 + 7 = (x + 4)² - 9.",
            },
            {
                "stem": "Complete the square for x^2 - 6x + 5.",
                "choices": [
                    "(x - 3)^2 - 4",
                    "(x + 3)^2 - 4",
                    "(x - 3)^2 + 4",
                    "(x - 6)^2 - 31"
                ],
                "solution": 0,
                "rationale": "x² - 6x + 5 = (x - 3)² - 9 + 5 = (x - 3)² - 4.",
            },
            {
                "stem": "Complete the square for x^2 + 10x + 9.",
                "choices": [
                    "(x + 5)^2 - 16",
                    "(x + 5)^2 + 16",
                    "(x - 5)^2 - 16",
                    "(x + 10)^2 - 91"
                ],
                "solution": 0,
                "rationale": "x² + 10x + 9 = (x + 5)² - 25 + 9 = (x + 5)² - 16.",
            },
            {
                "stem": "Complete the square for x^2 - 4x + 3.",
                "choices": [
                    "(x - 2)^2 - 1",
                    "(x + 2)^2 - 1",
                    "(x - 2)^2 + 1",
                    "(x - 4)^2 - 13"
                ],
                "solution": 0,
                "rationale": "x² - 4x + 3 = (x - 2)² - 4 + 3 = (x - 2)² - 1.",
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
            {
                "stem": "Complete the square for x^2 + 7x + 2.",
                "choices": [
                    "(x + 	frac{7}{2})^2 - 	frac{41}{4}",
                    "(x + 	frac{7}{2})^2 + 	frac{41}{4}",
                    "(x - 	frac{7}{2})^2 - 	frac{41}{4}",
                    "(x + 7)^2 - 47"
                ],
                "solution": 0,
                "rationale": "x² + 7x + 2 = (x + 7/2)² - 49/4 + 2 = (x + 7/2)² - 41/4.",
            },
            {
                "stem": "Complete the square for x^2 - 3x + 1.",
                "choices": [
                    "(x - 	frac{3}{2})^2 - 	frac{5}{4}",
                    "(x - 	frac{3}{2})^2 + 	frac{5}{4}",
                    "(x + 	frac{3}{2})^2 - 	frac{5}{4}",
                    "(x - 3)^2 - 8"
                ],
                "solution": 0,
                "rationale": "x² - 3x + 1 = (x - 3/2)² - 9/4 + 1 = (x - 3/2)² - 5/4.",
            },
            {
                "stem": "Complete the square for 3x^2 + 6x + 2.",
                "choices": [
                    "3(x + 1)^2 - 1",
                    "3(x + 1)^2 + 1",
                    "3(x - 1)^2 - 1",
                    "(x + 2)^2 - 2"
                ],
                "solution": 0,
                "rationale": "3x² + 6x + 2 = 3(x² + 2x) + 2 = 3((x + 1)² - 1) + 2 = 3(x + 1)² - 1.",
            },
            {
                "stem": "Complete the square for x^2 + 9x + 4.",
                "choices": [
                    "(x + 	frac{9}{2})^2 - 	frac{65}{4}",
                    "(x + 	frac{9}{2})^2 + 	frac{65}{4}",
                    "(x - 	frac{9}{2})^2 - 	frac{65}{4}",
                    "(x + 9)^2 - 77"
                ],
                "solution": 0,
                "rationale": "x² + 9x + 4 = (x + 9/2)² - 81/4 + 4 = (x + 9/2)² - 65/4.",
            },
            {
                "stem": "Complete the square for 2x^2 - 12x + 5.",
                "choices": [
                    "2(x - 3)^2 - 13",
                    "2(x - 3)^2 + 13",
                    "2(x + 3)^2 - 13",
                    "(x - 6)^2 - 31"
                ],
                "solution": 0,
                "rationale": "2x² - 12x + 5 = 2(x² - 6x) + 5 = 2((x - 3)² - 9) + 5 = 2(x - 3)² - 13.",
            },
            {
                "stem": "Complete the square for x^2 - 5x - 2.",
                "choices": [
                    "(x - 	frac{5}{2})^2 - 	frac{33}{4}",
                    "(x - 	frac{5}{2})^2 + 	frac{33}{4}",
                    "(x + 	frac{5}{2})^2 - 	frac{33}{4}",
                    "(x - 5)^2 - 27"
                ],
                "solution": 0,
                "rationale": "x² - 5x - 2 = (x - 5/2)² - 25/4 - 2 = (x - 5/2)² - 33/4.",
            },
            {
                "stem": "Complete the square for 4x^2 + 16x + 3.",
                "choices": [
                    "4(x + 2)^2 - 13",
                    "4(x + 2)^2 + 13",
                    "4(x - 2)^2 - 13",
                    "(x + 4)^2 - 13"
                ],
                "solution": 0,
                "rationale": "4x² + 16x + 3 = 4(x² + 4x) + 3 = 4((x + 2)² - 4) + 3 = 4(x + 2)² - 13.",
            },
            {
                "stem": "Complete the square for x^2 + 11x + 6.",
                "choices": [
                    "(x + 	frac{11}{2})^2 - 	frac{97}{4}",
                    "(x + 	frac{11}{2})^2 + 	frac{97}{4}",
                    "(x - 	frac{11}{2})^2 - 	frac{97}{4}",
                    "(x + 11)^2 - 115"
                ],
                "solution": 0,
                "rationale": "x² + 11x + 6 = (x + 11/2)² - 121/4 + 6 = (x + 11/2)² - 97/4.",
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
            {
                "stem": "Complete the square for 2x^2 - 8x + 3.",
                "choices": [
                    "2(x - 2)^2 - 5",
                    "2(x - 2)^2 + 5",
                    "2(x + 2)^2 - 5",
                    "(x - 4)^2 - 13"
                ],
                "solution": 0,
                "rationale": "2x² - 8x + 3 = 2(x² - 4x) + 3 = 2((x - 2)² - 4) + 3 = 2(x - 2)² - 5.",
            },
            {
                "stem": "Complete the square for -2x^2 + 12x - 5.",
                "choices": [
                    "-2(x - 3)^2 + 13",
                    "-2(x + 3)^2 + 13",
                    "-2(x - 3)^2 - 13",
                    "-(x - 6)^2 + 31"
                ],
                "solution": 0,
                "rationale": "-2x² + 12x - 5 = -2(x² - 6x) - 5 = -2((x - 3)² - 9) - 5 = -2(x - 3)² + 13.",
            },
            {
                "stem": "Complete the square for 5x^2 + 20x + 7.",
                "choices": [
                    "5(x + 2)^2 - 13",
                    "5(x + 2)^2 + 13",
                    "5(x - 2)^2 - 13",
                    "(x + 4)^2 - 9"
                ],
                "solution": 0,
                "rationale": "5x² + 20x + 7 = 5(x² + 4x) + 7 = 5((x + 2)² - 4) + 7 = 5(x + 2)² - 13.",
            },
            {
                "stem": "Complete the square for -3x^2 + 18x - 10.",
                "choices": [
                    "-3(x - 3)^2 + 17",
                    "-3(x + 3)^2 + 17",
                    "-3(x - 3)^2 - 17",
                    "-(x - 6)^2 + 26"
                ],
                "solution": 0,
                "rationale": "-3x² + 18x - 10 = -3(x² - 6x) - 10 = -3((x - 3)² - 9) - 10 = -3(x - 3)² + 17.",
            },
            {
                "stem": "Complete the square for 4x^2 - 16x + 11.",
                "choices": [
                    "4(x - 2)^2 - 5",
                    "4(x - 2)^2 + 5",
                    "4(x + 2)^2 - 5",
                    "(x - 4)^2 - 5"
                ],
                "solution": 0,
                "rationale": "4x² - 16x + 11 = 4(x² - 4x) + 11 = 4((x - 2)² - 4) + 11 = 4(x - 2)² - 5.",
            },
            {
                "stem": "Complete the square for -x^2 - 8x + 3.",
                "choices": [
                    "-(x + 4)^2 + 19",
                    "-(x - 4)^2 + 19",
                    "-(x + 4)^2 - 19",
                    "-(x + 8)^2 + 67"
                ],
                "solution": 0,
                "rationale": "-x² - 8x + 3 = -(x² + 8x) + 3 = -((x + 4)² - 16) + 3 = -(x + 4)² + 19.",
            },
            {
                "stem": "Complete the square for 6x^2 + 24x + 5.",
                "choices": [
                    "6(x + 2)^2 - 19",
                    "6(x + 2)^2 + 19",
                    "6(x - 2)^2 - 19",
                    "(x + 4)^2 - 11"
                ],
                "solution": 0,
                "rationale": "6x² + 24x + 5 = 6(x² + 4x) + 5 = 6((x + 2)² - 4) + 5 = 6(x + 2)² - 19.",
            },
            {
                "stem": "Complete the square for -4x^2 + 16x - 9.",
                "choices": [
                    "-4(x - 2)^2 + 7",
                    "-4(x + 2)^2 + 7",
                    "-4(x - 2)^2 - 7",
                    "-(x - 4)^2 + 7"
                ],
                "solution": 0,
                "rationale": "-4x² + 16x - 9 = -4(x² - 4x) - 9 = -4((x - 2)² - 4) - 9 = -4(x - 2)² + 7.",
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
            {
                "stem": "A projectile's height is h(t) = -16t^2 + 64t + 10. Complete the square to find maximum height.",
                "choices": [
                    "-16(t - 2)^2 + 74",
                    "-16(t + 2)^2 + 74",
                    "-16(t - 2)^2 - 54",
                    "-16(t - 4)^2 + 266"
                ],
                "solution": 0,
                "rationale": "-16t² + 64t + 10 = -16(t² - 4t) + 10 = -16((t - 2)² - 4) + 10 = -16(t - 2)² + 74. Max height is 74.",
            },
            {
                "stem": "A garden arch follows y = -0.5x^2 + 4x + 3. Complete the square to find vertex form.",
                "choices": [
                    "-0.5(x - 4)^2 + 11",
                    "-0.5(x + 4)^2 + 11",
                    "-0.5(x - 4)^2 - 5",
                    "-0.5(x - 2)^2 + 5"
                ],
                "solution": 0,
                "rationale": "-0.5x² + 4x + 3 = -0.5(x² - 8x) + 3 = -0.5((x - 4)² - 16) + 3 = -0.5(x - 4)² + 11.",
            },
            {
                "stem": "Profit is P(x) = -2x^2 + 20x - 15 thousand dollars. Complete the square to find maximum profit.",
                "choices": [
                    "-2(x - 5)^2 + 35",
                    "-2(x + 5)^2 + 35",
                    "-2(x - 5)^2 - 65",
                    "-2(x - 10)^2 + 185"
                ],
                "solution": 0,
                "rationale": "-2x² + 20x - 15 = -2(x² - 10x) - 15 = -2((x - 5)² - 25) - 15 = -2(x - 5)² + 35. Max profit is $35k.",
            },
            {
                "stem": "A suspension bridge cable follows y = 0.25x^2 - 3x + 12. Complete the square to find the lowest point.",
                "choices": [
                    "0.25(x - 6)^2 + 3",
                    "0.25(x + 6)^2 + 3",
                    "0.25(x - 6)^2 - 9",
                    "0.25(x - 3)^2 + 9.75"
                ],
                "solution": 0,
                "rationale": "0.25x² - 3x + 12 = 0.25(x² - 12x) + 12 = 0.25((x - 6)² - 36) + 12 = 0.25(x - 6)² + 3. Lowest at y = 3.",
            },
            {
                "stem": "Temperature varies as T(h) = -h^2 + 8h + 20 degrees. Complete the square to find maximum temperature.",
                "choices": [
                    "-(h - 4)^2 + 36",
                    "-(h + 4)^2 + 36",
                    "-(h - 4)^2 - 12",
                    "-(h - 8)^2 + 84"
                ],
                "solution": 0,
                "rationale": "-h² + 8h + 20 = -(h² - 8h) + 20 = -((h - 4)² - 16) + 20 = -(h - 4)² + 36. Max temp is 36°.",
            },
            {
                "stem": "A rocket's height is h(t) = -5t^2 + 40t + 15 meters. Complete the square to find vertex form.",
                "choices": [
                    "-5(t - 4)^2 + 95",
                    "-5(t + 4)^2 + 95",
                    "-5(t - 4)^2 - 65",
                    "-5(t - 8)^2 + 335"
                ],
                "solution": 0,
                "rationale": "-5t² + 40t + 15 = -5(t² - 8t) + 15 = -5((t - 4)² - 16) + 15 = -5(t - 4)² + 95.",
            },
            {
                "stem": "A parabolic mirror has equation y = 0.5x^2 - 6x + 20. Complete the square to locate the focus.",
                "choices": [
                    "0.5(x - 6)^2 + 2",
                    "0.5(x + 6)^2 + 2",
                    "0.5(x - 6)^2 - 18",
                    "0.5(x - 3)^2 + 15.5"
                ],
                "solution": 0,
                "rationale": "0.5x² - 6x + 20 = 0.5(x² - 12x) + 20 = 0.5((x - 6)² - 36) + 20 = 0.5(x - 6)² + 2. Vertex at (6, 2).",
            },
            {
                "stem": "Revenue is R(p) = -3p^2 + 30p + 12 dollars. Complete the square to find optimal price.",
                "choices": [
                    "-3(p - 5)^2 + 87",
                    "-3(p + 5)^2 + 87",
                    "-3(p - 5)^2 - 63",
                    "-3(p - 10)^2 + 312"
                ],
                "solution": 0,
                "rationale": "-3p² + 30p + 12 = -3(p² - 10p) + 12 = -3((p - 5)² - 25) + 12 = -3(p - 5)² + 87. Optimal at p = 5.",
            },
            {
                "stem": "A water fountain's stream follows h(x) = -x^2 + 10x + 5. Complete the square to find peak height.",
                "choices": [
                    "-(x - 5)^2 + 30",
                    "-(x + 5)^2 + 30",
                    "(x - 5)^2 - 20",
                    "-(x - 10)^2 + 105"
                ],
                "solution": 0,
                "rationale": "-x² + 10x + 5 = -(x² - 10x) + 5 = -((x - 5)² - 25) + 5 = -(x - 5)² + 30. Peak at h = 30.",
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
            {
                "stem": "Find the axis of symmetry for y = (x - 5)^2 + 3.",
                "choices": ["x = 5", "x = -5", "x = 3", "x = -3"],
                "solution": 0,
                "rationale": "In vertex form y = (x - h)^2 + k, axis of symmetry is x = h, so x = 5.",
            },
            {
                "stem": "Find the axis of symmetry for y = (x + 2)^2 - 1.",
                "choices": ["x = -2", "x = 2", "x = -1", "x = 1"],
                "solution": 0,
                "rationale": "In vertex form y = (x - h)^2 + k, axis is x = h. Here h = -2, so x = -2.",
            },
            {
                "stem": "Find the axis of symmetry for y = x^2 + 8x + 7.",
                "choices": ["x = -4", "x = 4", "x = -8", "x = 8"],
                "solution": 0,
                "rationale": "Axis of symmetry: x = -b/(2a) = -8/(2·1) = -4.",
            },
            {
                "stem": "Find the axis of symmetry for y = x^2 - 10x + 12.",
                "choices": ["x = 5", "x = -5", "x = 10", "x = -10"],
                "solution": 0,
                "rationale": "Axis of symmetry: x = -b/(2a) = -(-10)/(2·1) = 5.",
            },
            {
                "stem": "Find the axis of symmetry for y = (x - 1)^2 + 4.",
                "choices": ["x = 1", "x = -1", "x = 4", "x = -4"],
                "solution": 0,
                "rationale": "In vertex form y = (x - h)^2 + k, axis of symmetry is x = h = 1.",
            },
            {
                "stem": "Find the axis of symmetry for y = x^2 + 2x - 8.",
                "choices": ["x = -1", "x = 1", "x = -2", "x = 2"],
                "solution": 0,
                "rationale": "Axis of symmetry: x = -b/(2a) = -2/(2·1) = -1.",
            },
            {
                "stem": "Find the axis of symmetry for y = (x + 4)^2 + 7.",
                "choices": ["x = -4", "x = 4", "x = -7", "x = 7"],
                "solution": 0,
                "rationale": "In vertex form y = (x - h)^2 + k, axis is x = h. Here h = -4, so x = -4.",
            },
            {
                "stem": "Find the axis of symmetry for y = x^2 - 12x + 20.",
                "choices": ["x = 6", "x = -6", "x = 12", "x = -12"],
                "solution": 0,
                "rationale": "Axis of symmetry: x = -b/(2a) = -(-12)/(2·1) = 6.",
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
            {
                "stem": "Find the axis of symmetry for y = 4x^2 - 12x + 5.",
                "choices": ["x = 1.5", "x = -1.5", "x = 3", "x = -3"],
                "solution": 0,
                "rationale": "Axis of symmetry: x = -b/(2a) = -(-12)/(2·4) = 12/8 = 1.5.",
            },
            {
                "stem": "Find the axis of symmetry for y = -2x^2 - 16x + 7.",
                "choices": ["x = -4", "x = 4", "x = -8", "x = 8"],
                "solution": 0,
                "rationale": "Axis of symmetry: x = -b/(2a) = -(-16)/(2·-2) = -16/4 = -4.",
            },
            {
                "stem": "Find the axis of symmetry for y = 5x^2 + 20x - 1.",
                "choices": ["x = -2", "x = 2", "x = -4", "x = 4"],
                "solution": 0,
                "rationale": "Axis of symmetry: x = -b/(2a) = -20/(2·5) = -20/10 = -2.",
            },
            {
                "stem": "Find the axis of symmetry for y = -x^2 + 7x - 10.",
                "choices": ["x = 3.5", "x = -3.5", "x = 7", "x = -7"],
                "solution": 0,
                "rationale": "Axis of symmetry: x = -b/(2a) = -7/(2·-1) = 7/2 = 3.5.",
            },
            {
                "stem": "Find the axis of symmetry for y = 3x^2 - 18x + 9.",
                "choices": ["x = 3", "x = -3", "x = 6", "x = -6"],
                "solution": 0,
                "rationale": "Axis of symmetry: x = -b/(2a) = -(-18)/(2·3) = 18/6 = 3.",
            },
            {
                "stem": "Find the axis of symmetry for y = -4x^2 + 8x + 11.",
                "choices": ["x = 1", "x = -1", "x = 2", "x = -2"],
                "solution": 0,
                "rationale": "Axis of symmetry: x = -b/(2a) = -8/(2·-4) = -8/(-8) = 1.",
            },
            {
                "stem": "Find the axis of symmetry for y = 6x^2 + 24x - 5.",
                "choices": ["x = -2", "x = 2", "x = -4", "x = 4"],
                "solution": 0,
                "rationale": "Axis of symmetry: x = -b/(2a) = -24/(2·6) = -24/12 = -2.",
            },
            {
                "stem": "Find the axis of symmetry for y = -5x^2 - 30x + 2.",
                "choices": ["x = -3", "x = 3", "x = -6", "x = 6"],
                "solution": 0,
                "rationale": "Axis of symmetry: x = -b/(2a) = -(-30)/(2·-5) = 30/(-10) = -3.",
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
            {
                "stem": "Find the axis of symmetry for y = \\tfrac{1}{3}x^2 + 2x - 5.",
                "choices": ["x = -3", "x = 3", "x = -6", "x = 6"],
                "solution": 0,
                "rationale": "Axis of symmetry: x = -b/(2a) = -2/(2·1/3) = -2/(2/3) = -3.",
            },
            {
                "stem": "Find the axis of symmetry for y = -\\tfrac{2}{5}x^2 + 4x + 1.",
                "choices": ["x = 5", "x = -5", "x = 2.5", "x = -2.5"],
                "solution": 0,
                "rationale": "Axis of symmetry: x = -b/(2a) = -4/(2·-2/5) = -4/(-4/5) = 5.",
            },
            {
                "stem": "For y = 2x^2 + bx - 3, if the axis of symmetry is x = 4, what is b?",
                "choices": ["b = -16", "b = 16", "b = -8", "b = 8"],
                "solution": 0,
                "rationale": "x = -b/(2a) = 4, so -b/(2·2) = 4, thus -b/4 = 4, so b = -16.",
            },
            {
                "stem": "Find the axis of symmetry for y = 1.25x^2 - 5x + 8.",
                "choices": ["x = 2", "x = -2", "x = 4", "x = -4"],
                "solution": 0,
                "rationale": "Axis of symmetry: x = -b/(2a) = -(-5)/(2·1.25) = 5/2.5 = 2.",
            },
            {
                "stem": "For y = -3x^2 + cx + 7, if the axis of symmetry is x = -2, what is c?",
                "choices": ["c = -12", "c = 12", "c = -6", "c = 6"],
                "solution": 0,
                "rationale": "x = -b/(2a) = -2, so -c/(2·-3) = -2, thus c/6 = -2, so c = -12.",
            },
            {
                "stem": "Find the axis of symmetry for y = \\tfrac{3}{4}x^2 - 6x + 10.",
                "choices": ["x = 4", "x = -4", "x = 8", "x = -8"],
                "solution": 0,
                "rationale": "Axis of symmetry: x = -b/(2a) = -(-6)/(2·3/4) = 6/(3/2) = 4.",
            },
            {
                "stem": "Find the axis of symmetry for y = -0.25x^2 - 3x + 5.",
                "choices": ["x = -6", "x = 6", "x = -12", "x = 12"],
                "solution": 0,
                "rationale": "Axis of symmetry: x = -b/(2a) = -(-3)/(2·-0.25) = 3/(-0.5) = -6.",
            },
            {
                "stem": "For y = kx^2 - 10x + 8, if the axis of symmetry is x = 2.5, what is k?",
                "choices": ["k = 2", "k = -2", "k = 5", "k = -5"],
                "solution": 0,
                "rationale": "x = -b/(2a) = 2.5, so -(-10)/(2k) = 2.5, thus 10/(2k) = 2.5, so 5k = 10, k = 2.",
            },
        ],
        "applied": [
            {
                "stem": "A projectile's path is h(t) = -16t^2 + 64t + 10. At what time is maximum height?",
                "choices": ["t = 2", "t = 4", "t = 1", "t = 8"],
                "solution": 0,
                "rationale": "Maximum at axis of symmetry: t = -b/(2a) = -64/(2·-16) = 2.",
            },
            {
                "stem": "A bridge arch follows y = -0.1x^2 + 4x, where x is horizontal distance. At what x is the peak?",
                "choices": ["x = 20 m", "x = 40 m", "x = 10 m", "x = 5 m"],
                "solution": 0,
                "rationale": "Peak at axis of symmetry: x = -b/(2a) = -4/(2·-0.1) = -4/(-0.2) = 20 m.",
            },
            {
                "stem": "A fountain's water path is h(d) = -2d^2 + 8d + 1. At what distance d is max height?",
                "choices": ["d = 2 ft", "d = 4 ft", "d = 1 ft", "d = 8 ft"],
                "solution": 0,
                "rationale": "Maximum at axis of symmetry: d = -b/(2a) = -8/(2·-2) = 2 ft.",
            },
            {
                "stem": "A company's profit is P(x) = -5x^2 + 200x - 1500 where x is units (in hundreds). What x maximizes profit?",
                "choices": ["x = 20", "x = 40", "x = 10", "x = 50"],
                "solution": 0,
                "rationale": "Maximum at axis of symmetry: x = -b/(2a) = -200/(2·-5) = 20.",
            },
            {
                "stem": "A diver's trajectory is h(t) = -4.9t^2 + 9.8t + 3. When does the diver reach peak height?",
                "choices": ["t = 1 s", "t = 2 s", "t = 0.5 s", "t = 3 s"],
                "solution": 0,
                "rationale": "Peak at axis of symmetry: t = -b/(2a) = -9.8/(2·-4.9) = 1 s.",
            },
            {
                "stem": "A cable hangs in shape y = 0.02x^2 - 1.6x + 40. At what x is the cable lowest?",
                "choices": ["x = 40 m", "x = 80 m", "x = 20 m", "x = 10 m"],
                "solution": 0,
                "rationale": "Minimum at axis of symmetry: x = -b/(2a) = -(-1.6)/(2·0.02) = 1.6/0.04 = 40 m.",
            },
            {
                "stem": "A ball's height is h(t) = -5t^2 + 30t + 2. At what time t does it reach maximum height?",
                "choices": ["t = 3 s", "t = 6 s", "t = 1.5 s", "t = 15 s"],
                "solution": 0,
                "rationale": "Maximum at axis of symmetry: t = -b/(2a) = -30/(2·-5) = 3 s.",
            },
            {
                "stem": "A garden path's cross-section is y = -x^2 + 12x where y is depth. At what x is it deepest?",
                "choices": ["x = 6 ft", "x = 12 ft", "x = 3 ft", "x = 24 ft"],
                "solution": 0,
                "rationale": "Maximum depth at axis of symmetry: x = -b/(2a) = -12/(2·-1) = 6 ft.",
            },
            {
                "stem": "An antenna's signal strength is S(d) = -0.5d^2 + 10d + 50. At what distance d is it strongest?",
                "choices": ["d = 10 m", "d = 20 m", "d = 5 m", "d = 25 m"],
                "solution": 0,
                "rationale": "Maximum at axis of symmetry: d = -b/(2a) = -10/(2·-0.5) = 10 m.",
            },
            {
                "stem": "A skateboarder's ramp height is h(x) = -0.25x^2 + 3x where x is horizontal distance. Where is the peak?",
                "choices": ["x = 6 m", "x = 12 m", "x = 3 m", "x = 24 m"],
                "solution": 0,
                "rationale": "Peak at axis of symmetry: x = -b/(2a) = -3/(2·-0.25) = 3/0.5 = 6 m.",
            },
        ],
    },
}

VALID_DIFFICULTIES = {"easy", "medium", "hard", "applied"}


def generate_item(
    skill_id: str,
    difficulty: Optional[str] = None,
    seed: Optional[int] = None,
    excluded_stems: Optional[set] = None,
    use_parameterized: bool = False
) -> dict:
    """
    Generate a math question item per contract.

    Args:
        skill_id: Skill identifier (e.g., "quad.graph.vertex")
        difficulty: One of {"easy", "medium", "hard", "applied"}, or None (defaults to "easy")
        seed: Optional seed for deterministic generation; if provided, item is fully deterministic
        excluded_stems: Optional set of stem strings to avoid (for anti-repetition)
        use_parameterized: If True, use parameterized generation (Phase 2 feature)

    Returns:
        A dict with keys: item_id, skill_id, difficulty, stem, choices, solution_choice_id, solution_text, tags

    Raises:
        ValueError: If skill_id is unknown, difficulty is invalid, or seed is not an int
    """
    # Phase 2: Try parameterized generation first if enabled
    if use_parameterized:
        try:
            from engine.parameters import generate_parameterized_item, PARAMETERIZED_TEMPLATES

            # Check if parameterized template exists
            if (skill_id in PARAMETERIZED_TEMPLATES and
                (difficulty or "easy") in PARAMETERIZED_TEMPLATES[skill_id]):
                return generate_parameterized_item(skill_id, difficulty or "easy", seed)
        except (ImportError, ValueError):
            # Fall back to static templates
            pass
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

    # Filter out excluded stems if provided
    if excluded_stems:
        filtered_questions = [q for q in questions if q["stem"] not in excluded_stems]
        # If filtering removed all questions, fall back to full set
        if filtered_questions:
            questions = filtered_questions

    # Pick a question (deterministically from filtered set)
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
