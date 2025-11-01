"""
Planner: Select next skill based on learning progress.
"""

from .skills import SKILLS, SKILL_BY_ID


def select_next_skill(state: dict) -> str:
    """
    Select the next skill for the user to practice.
    
    Rules:
    1. If a skill has correct_streak >= 3, rotate to a skill that has it as prerequisite
    2. Otherwise, return the last skill or default to first skill
    
    Args:
        state: User state dict with 'skills' mapping skill_id -> {correct_streak, ...}
    
    Returns:
        skill_id to practice next
    """
    skills_state = state.get("skills", {})
    last_selected = state.get("last_selected_skill")
    
    # Check for rotation: find skill with streak >= 3
    for skill in SKILLS:
        sid = skill["id"]
        skill_data = skills_state.get(sid, {})
        streak = skill_data.get("correct_streak", 0)
        
        # Skip the skill we just rotated to (avoid ping-pong)
        if sid == last_selected:
            continue
        
        # If this skill has 3+ correct, find a skill to rotate to
        if streak >= 3:
            for candidate in SKILLS:
                cid = candidate["id"]
                
                # Skip if already rotated to this skill
                if cid == last_selected:
                    continue
                
                # Check if current skill is a prerequisite for candidate
                if sid in candidate.get("prereqs", []):
                    # Found a valid rotation target
                    return cid
    
    # No rotation triggered - stay on last skill or pick first one
    if last_selected:
        return last_selected
    
    return SKILLS[0]["id"]
