"""
Simple state management for learning engine.
Stores user skill progress as JSON files.
"""
import json
import os
from pathlib import Path


def get_data_dir():
    """Get the data directory for state files."""
    base = Path(__file__).parent.parent.parent.parent.parent  # Navigate to Agent_Math/
    data_dir = base / "quadratics_mvp" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def load_state(user_id: str) -> dict:
    """Load user state from disk, or return default empty state."""
    path = get_data_dir() / f"{user_id}.json"
    
    if not path.exists():
        return {
            "user_id": user_id,
            "skills": {},
            "history": []
        }
    
    with open(path, 'r') as f:
        return json.load(f)


def save_state(user_id: str, state: dict) -> None:
    """Save user state to disk."""
    path = get_data_dir() / f"{user_id}.json"
    
    with open(path, 'w') as f:
        json.dump(state, f, indent=2)


def get_skill_state(state: dict, skill_id: str) -> dict:
    """Get or create state for a specific skill."""
    if 'skills' not in state:
        state['skills'] = {}
    
    if skill_id not in state['skills']:
        state['skills'][skill_id] = {
            "p_mastery": 0.6,
            "correct_streak": 0,
            "attempts": 0,
            "correct_count": 0
        }
    
    return state['skills'][skill_id]
