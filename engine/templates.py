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
    }
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
