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
        ],
        "applied": [
            {
                "stem": "A ball's height is h(t) = -16(t - 2)^2 + 64. At what time is max height?",
                "choices": ["t = 2", "t = 4", "t = 0", "t = 8"],
                "solution": 0,
                "rationale": "The vertex occurs at t = 2, the maximum height.",
            },
        ],
    },
    "quad.standard.vertex": {
        "easy": [
            {
                "stem": "What is the vertex of y = x^2 - 6x + 5?",
                "choices": ["(3, -4)", "(-3, -4)", "(3, 4)", "(6, 5)"],
                "solution": 0,
                "rationale": "Vertex x = -b/(2a) = 3, substitute to get y = -4.",
            },
            {
                "stem": "Find the vertex of y = x^2 + 4x + 1.",
                "choices": ["(-2, -3)", "(2, 3)", "(-4, 1)", "(-2, 3)"],
                "solution": 0,
                "rationale": "x = -b/2a = -2, y = (-2)^2 + 4(-2) + 1 = -3.",
            },
            {
                "stem": "What is the vertex of y = x^2 - 2x + 1?",
                "choices": ["(1, 0)", "(-1, 0)", "(1, 1)", "(0, 1)"],
                "solution": 0,
                "rationale": "x = 1, y = 0; the vertex is (1, 0).",
            },
        ],
        "medium": [
            {
                "stem": "Find the vertex of y = 2x^2 - 8x + 5.",
                "choices": ["(2, -3)", "(4, -3)", "(2, 3)", "(-2, -3)"],
                "solution": 0,
                "rationale": "x = -b/(2a) = 2, substitute: y = -3.",
            },
            {
                "stem": "Find the vertex of y = -x^2 + 4x + 1.",
                "choices": ["(2, 5)", "(2, -5)", "(-2, 5)", "(1, 4)"],
                "solution": 0,
                "rationale": "x = -b/(2a) = 2, y = -4 + 8 + 1 = 5.",
            },
        ],
        "hard": [
            {
                "stem": "Find the vertex of y = 3x^2 - 12x + 7.",
                "choices": ["(2, -5)", "(4, -5)", "(2, 5)", "(-2, -5)"],
                "solution": 0,
                "rationale": "x = -b/(2a) = 2, y = 3(4) - 24 + 7 = -5.",
            },
        ],
        "applied": [
            {
                "stem": "A ball's height is modeled by h(t) = -5t^2 + 40t + 60. At what time does it reach maximum height?",
                "choices": ["t = 4", "t = 8", "t = 2", "t = 6"],
                "solution": 0,
                "rationale": "t = -b/(2a) = 4 seconds.",
            },
            {
                "stem": "For y = -16t^2 + 32t + 10, what is the maximum height?",
                "choices": ["26 feet", "10 feet", "32 feet", "42 feet"],
                "solution": 0,
                "rationale": "At t = 1, h = -16(1) + 32 + 10 = 26 feet.",
            },
        ],
    },
    "quad.roots.factored": {
        "easy": [
            {
                "stem": "Find the zeros of y = (x - 2)(x + 5).",
                "choices": ["x = 2, -5", "x = -2, 5", "x = 2, 5", "x = -2, -5"],
                "solution": 0,
                "rationale": "Set each factor to zero: x = 2 and x = -5.",
            },
            {
                "stem": "Find the zeros of y = (x + 3)(x - 7).",
                "choices": ["x = -3, 7", "x = 3, -7", "x = -7, -3", "x = 7, 3"],
                "solution": 0,
                "rationale": "x = -3 and x = 7.",
            },
        ],
        "medium": [
            {
                "stem": "Find the zeros of y = -2(x + 1)(x - 4).",
                "choices": ["x = -1, 4", "x = 1, -4", "x = -1, -4", "x = 1, 4"],
                "solution": 0,
                "rationale": "Set each factor = 0, a does not change roots.",
            },
            {
                "stem": "Find the zeros of y = 3(x - 5)(x - 2).",
                "choices": ["x = 5, 2", "x = -5, -2", "x = 5, -2", "x = 2, -5"],
                "solution": 0,
                "rationale": "x = 5 and x = 2.",
            },
        ],
        "hard": [
            {
                "stem": "Find the zeros of y = -4(x + 2)(x + 6).",
                "choices": ["x = -2, -6", "x = 2, 6", "x = 2, -6", "x = -2, 6"],
                "solution": 0,
                "rationale": "x = -2 and x = -6.",
            },
        ],
        "applied": [
            {
                "stem": "The height of a ball is modeled by h(t) = -5(t - 1)(t - 6). When does the ball hit the ground?",
                "choices": ["t = 1 s and t = 6 s", "t = -1 s and t = 6 s", "t = 5 s and t = 7 s", "t = 0 s and t = 6 s"],
                "solution": 0,
                "rationale": "h = 0 at t = 1 and t = 6.",
            },
        ],
    },
    "quad.solve.by_factoring": {
        "easy": [
            {
                "stem": "Solve x^2 - 3x - 10 = 0.",
                "choices": ["x = 5, -2", "x = -5, 2", "x = 5, 2", "x = -5, -2"],
                "solution": 0,
                "rationale": "(x - 5)(x + 2) = 0 → x = 5, -2.",
            },
            {
                "stem": "Solve x^2 + x - 6 = 0.",
                "choices": ["x = 2, -3", "x = -2, 3", "x = -2, -3", "x = 3, 2"],
                "solution": 0,
                "rationale": "(x + 3)(x - 2) = 0 → x = -3, 2.",
            },
        ],
        "medium": [
            {
                "stem": "Solve 2x^2 + 7x + 3 = 0.",
                "choices": ["x = -1/2, -3", "x = 1/2, 3", "x = -3, -7", "x = -1, -2"],
                "solution": 0,
                "rationale": "(2x + 1)(x + 3) = 0 → x = -1/2, -3.",
            },
            {
                "stem": "Solve 3x^2 - 12x + 9 = 0.",
                "choices": ["x = 1, 3", "x = -1, -3", "x = 1, -3", "x = 0, 3"],
                "solution": 0,
                "rationale": "Divide by 3, factor (x - 1)(x - 3) = 0.",
            },
        ],
        "hard": [
            {
                "stem": "Solve 2x^2 - 5x - 3 = 0.",
                "choices": ["x = 3, -1/2", "x = -3, 1/2", "x = 1/3, -2", "x = -1, 3/2"],
                "solution": 0,
                "rationale": "(2x + 1)(x - 3) = 0 → x = -1/2, 3.",
            },
        ],
        "applied": [
            {
                "stem": "A rectangle has area x^2 + 5x + 6 = 0 when length is (x + 2). What are the roots?",
                "choices": ["x = -2, -3", "x = 2, 3", "x = -1, -6", "x = -2, 3"],
                "solution": 0,
                "rationale": "(x + 2)(x + 3) = 0 → x = -2, -3.",
            },
        ],
    },
    "quad.solve.by_formula": {
        "easy": [
            {
                "stem": "Solve x^2 - 5x + 6 = 0 using the quadratic formula.",
                "choices": ["x = 2, 3", "x = -2, -3", "x = 1, 6", "x = 3, -6"],
                "solution": 0,
                "rationale": "Discriminant = 25 - 24 = 1 → x = (5 ± 1)/2 = 2, 3.",
            },
            {
                "stem": "Solve x^2 - 4x + 3 = 0.",
                "choices": ["x = 1, 3", "x = -1, -3", "x = 1, -3", "x = 0, 3"],
                "solution": 0,
                "rationale": "x = (4 ± √(16 - 12))/2 = (4 ± 2)/2 → x = 1, 3.",
            },
        ],
        "medium": [
            {
                "stem": "Solve x^2 - 2x - 3 = 0 using the quadratic formula.",
                "choices": ["x = 3, -1", "x = -3, 1", "x = 2, 3", "x = -2, -3"],
                "solution": 0,
                "rationale": "Discriminant = 4 + 12 = 16 → x = (2 ± 4)/2 = 3, -1.",
            },
            {
                "stem": "Solve x^2 + 4x + 2 = 0.",
                "choices": ["x = -2 ± √2", "x = 2 ± √2", "x = -4 ± √2", "x = -2 ± 2√2"],
                "solution": 0,
                "rationale": "x = (-4 ± √(16 - 8))/2 = (-4 ± √8)/2 = -2 ± √2.",
            },
        ],
        "hard": [
            {
                "stem": "Solve 2x^2 + 3x + 7 = 0.",
                "choices": ["x = (-3 ± i√47)/4", "x = (-3 ± √47)/4", "x = (-3 ± i√43)/4", "x = (3 ± i√47)/4"],
                "solution": 0,
                "rationale": "Discriminant = 9 - 56 = -47 → complex roots x = (-3 ± i√47)/4.",
            },
        ],
        "applied": [
            {
                "stem": "A projectile follows h = -4.9t^2 + 20t + 1. When does it hit the ground (h=0)?",
                "choices": ["t ≈ 0.05 s and t ≈ 4.1 s", "t ≈ -0.05 s and t ≈ 4.1 s", "t ≈ 1 s and t ≈ 3 s", "t ≈ 0.5 s and t ≈ 2 s"],
                "solution": 0,
                "rationale": "Set h=0; use quadratic formula → t ≈ 0.05, 4.1.",
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
