"""
Engine Service: Bridge between FastAPI routes and Python learning engine.

This module wraps the engine functions and handles:
- Item generation (adaptive difficulty)
- Grading (validation + misconception detection)
- Neo4j queries (skills, learner state, mastery updates)
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
import random

# Add quadratics_mvp to path so we can import engine modules
QUADRATICS_MVP_PATH = Path("/Users/sunnyzheng/Agent_Math/quadratics_mvp")
if str(QUADRATICS_MVP_PATH) not in sys.path:
    sys.path.insert(0, str(QUADRATICS_MVP_PATH))

# Import engine modules
try:
    from engine.templates import generate_item
    from engine.grader import grade
    from engine.planner import generate_adaptive_item, next_skill
    from engine.state import load_user_state, save_user_state, update_after_answer
    IMPORTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Warning: Could not import engine modules. {e}")
    print("   This is expected in development. Mock data will be used.")
    generate_item = None
    grade = None
    generate_adaptive_item = None
    next_skill = None
    IMPORTS_AVAILABLE = False

# In-memory cache of generated items (user_id -> item_id -> item)
_ITEM_CACHE = {}


class EngineService:
    """Service to integrate Python engine with FastAPI."""
    
    @staticmethod
    def _cache_item(user_id: str, item: Dict[str, Any]) -> None:
        """Store item in memory cache for later grading."""
        if user_id not in _ITEM_CACHE:
            _ITEM_CACHE[user_id] = {}
        item_id = item.get("item_id")
        _ITEM_CACHE[user_id][item_id] = item
    
    @staticmethod
    def _get_cached_item(user_id: str, item_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached item."""
        return _ITEM_CACHE.get(user_id, {}).get(item_id)
    
    @staticmethod
    def _normalize_item(item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize item from engine to API contract.
        - Add choice IDs if missing (use a, b, c, d, ...)
        - Normalize field names (id → item_id, rationale → explanation)
        """
        # Ensure choices have IDs
        choices = item.get("choices", [])
        choice_ids = ["a", "b", "c", "d", "e", "f", "g", "h"]
        for i, choice in enumerate(choices):
            if "id" not in choice:
                choice["id"] = choice_ids[i] if i < len(choice_ids) else f"choice_{i}"
        
        return item
    
    @staticmethod
    def list_skills(domain: str = "Quadratics") -> List[Dict[str, Any]]:
        """
        List all available skills in a domain.
        
        In production, this queries Neo4j skill nodes.
        For now, returns from skills.json.
        """
        skills_map = {
            "Quadratics": [
                {
                    "id": "quad.identify",
                    "name": "Identify Quadratic",
                    "description": "Determine if an expression is quadratic",
                    "prerequisites": []
                },
                {
                    "id": "quad.vertex.form",
                    "name": "Convert to Vertex Form",
                    "description": "Write quadratic in vertex form a(x-h)² + k",
                    "prerequisites": ["quad.identify"]
                },
                {
                    "id": "quad.factor.a1",
                    "name": "Factor Quadratics (a=1)",
                    "description": "Factor quadratic trinomials with leading coefficient 1",
                    "prerequisites": ["quad.identify"]
                },
                {
                    "id": "quad.discriminant",
                    "name": "Use Discriminant",
                    "description": "Determine number of real solutions using discriminant",
                    "prerequisites": ["quad.identify"]
                },
            ]
        }
        return skills_map.get(domain, [])
    
    @staticmethod
    def generate_next_item(
        user_id: str,
        domain: str = "Quadratics",
        seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate next item for student.
        
        Calls engine.planner.generate_adaptive_item() to:
        1. Load learner state from file (development) or Neo4j (production)
        2. Select next skill using adaptive planner logic
        3. Generate item with adaptive difficulty
        
        Args:
            user_id: UUID of student
            domain: Skill domain (default: Quadratics)
            seed: Optional seed for deterministic generation (testing)
        
        Returns:
            {
                "item_id": "item_xxx",
                "skill_id": "quad.vertex.form",
                "difficulty": "medium",
                "stem": "Write x²+2x+1 in vertex form...",
                "choices": [...],
                "explanation": "...",
                "reason": "Remediation: you had 2 sign_error tags",
                "learner_mastery_before": 0.6
            }
        """
        if seed is not None:
            random.seed(seed)
        
        try:
            if not IMPORTS_AVAILABLE:
                raise ImportError("Engine modules not available")
            
            # Load learner state from file (or create new state if doesn't exist)
            try:
                state = load_user_state(user_id)
            except Exception:
                # First time user: create empty state
                state = {
                    "user_id": user_id,
                    "skills": {},
                    "attempts": 0,
                    "created_at": datetime.utcnow().isoformat()
                }
            
            # Select next skill using adaptive planner
            skill_id = next_skill(state)
            
            if not skill_id:
                # Fallback: default to quad.identify
                skill_id = "quad.identify"
            
            # Generate item with adaptive difficulty
            item_data = generate_adaptive_item(
                skill_id=skill_id,
                state=state,
                seed=seed
            )
            
            # Normalize: add choice IDs if missing
            item_data = EngineService._normalize_item(item_data)
            
            # Cache the item so grader can retrieve it later
            EngineService._cache_item(user_id, item_data)
            
            return {
                "item_id": item_data.get("item_id") or item_data.get("id"),
                "skill_id": item_data.get("skill_id"),
                "difficulty": item_data.get("difficulty", "medium"),
                "stem": item_data.get("stem"),
                "choices": item_data.get("choices", []),
                "explanation": item_data.get("rationale") or item_data.get("explanation"),
                "reason": item_data.get("reason", "Continue practicing"),
                "learner_mastery_before": item_data.get("learner_mastery_before") or item_data.get("learner_mastery", 0.5)
            }
        
        except Exception as e:
            # Fallback: return a simple mock question
            print(f"⚠️  Warning: Failed to generate item from engine: {e}")
            
            # Simple fallback mock
            return {
                "item_id": f"mock_{user_id}_{int(datetime.utcnow().timestamp())}",
                "skill_id": "quad.identify",
                "difficulty": "easy",
                "stem": "Is x² + 2x + 1 a quadratic expression?",
                "choices": [
                    {"id": "c1", "text": "Yes", "tags_on_select": ["correct"]},
                    {"id": "c2", "text": "No", "tags_on_select": ["wrong"]},
                    {"id": "c3", "text": "Maybe", "tags_on_select": ["wrong"]},
                    {"id": "c4", "text": "Unclear", "tags_on_select": ["wrong"]},
                ],
                "explanation": "A quadratic has degree 2. This expression is x² + 2x + 1, which is degree 2.",
                "reason": "Mock item (engine not available)",
                "learner_mastery_before": 0.5
            }
    
    @staticmethod
    def grade_response(
        user_id: str,
        item_id: str,
        selected_choice_id: str,
        time_ms: int = 0,
        confidence: float = 0.5,
        seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Grade student response and update mastery.
        
        Calls engine.grader.grade() to:
        1. Retrieve cached item
        2. Validate selected choice
        3. Detect misconception tags (sign_error, wrong_degree, etc.)
        4. Update mastery equation: p_mastery_after = f(p_mastery, correct, confidence)
        5. Update HAS_PROGRESS edge + misconception counters
        
        Args:
            user_id: Student ID
            item_id: Item ID just answered
            selected_choice_id: Choice ID they selected
            time_ms: Time spent (milliseconds)
            confidence: 0-1 self-assessed confidence
            seed: Optional seed for tests
        
        Returns:
            {
                "correct": true,
                "tags": ["correct"],
                "p_mastery_after": 0.68,
                "attempts_on_skill": 5,
                "next_due_at": "2025-11-07T...",
                "suggested_resource_url": null
            }
        """
        if seed is not None:
            random.seed(seed)
        
        try:
            if not IMPORTS_AVAILABLE:
                raise ImportError("Engine modules not available")
            
            # Retrieve cached item
            item = EngineService._get_cached_item(user_id, item_id)
            if not item:
                raise ValueError(f"Item {item_id} not found in cache")
            
            # Call engine grader
            result = grade(item=item, choice_id=selected_choice_id)
            correct, tags, chosen_text, score = result
            
            # Load learner state
            state = load_user_state(user_id)
            skill_id = item.get("skill_id", "unknown")
            
            # Update mastery (stochastic update)
            p_mastery_before = state.get("skills", {}).get(skill_id, {}).get("p_mastery", 0.5)
            
            # Simple mastery update: +0.05 if correct, -0.03 if wrong
            p_mastery_after = p_mastery_before + (0.05 if correct else -0.03)
            p_mastery_after = max(0.0, min(1.0, p_mastery_after))  # Clamp to [0, 1]
            
            # Update attempt count
            attempts = state.get("skills", {}).get(skill_id, {}).get("attempts", 0) + 1
            
            # Save updated state
            if "skills" not in state:
                state["skills"] = {}
            if skill_id not in state["skills"]:
                state["skills"][skill_id] = {}
                
            state["skills"][skill_id] = {
                "p_mastery": p_mastery_after,
                "attempts": attempts,
                "last_attempt": datetime.utcnow().isoformat(),
                "correct_count": state.get("skills", {}).get(skill_id, {}).get("correct_count", 0) + (1 if correct else 0)
            }
            save_user_state(user_id, state)
            
            # Determine next_due_at (spaced review)
            next_due_at = None
            if correct and p_mastery_after >= 0.9:
                # Schedule review in 7 days
                from datetime import timedelta
                next_due_at = (datetime.utcnow() + timedelta(days=7)).isoformat()
            
            # Suggest resource if misconception detected
            suggested_url = None
            if not correct and tags and "correct" not in tags:
                # Map tags to resources
                tag = tags[0]  # First tag
                resource_map = {
                    "sign_error": "https://www.khanacademy.org/math/algebra/x2f8bb11595b61c86:quadratics-multiplying-factoring",
                    "wrong_degree": "https://www.khanacademy.org/math/algebra/x2f8bb11595b61c86:quadratics-intro",
                }
                suggested_url = resource_map.get(tag)
            
            return {
                "correct": correct,
                "tags": tags,
                "p_mastery_after": round(p_mastery_after, 2),
                "attempts_on_skill": attempts,
                "next_due_at": next_due_at,
                "suggested_resource_url": suggested_url
            }
        
        except Exception as e:
            # Fallback: use mock grading for development
            print(f"⚠️  Warning: Failed to grade with engine: {e}")
            is_correct = selected_choice_id == "c1"  # c1 is always correct in mock
            
            return {
                "correct": is_correct,
                "tags": ["correct"] if is_correct else ["wrong"],
                "p_mastery_after": round(0.55 if is_correct else 0.45, 2),
                "attempts_on_skill": 1,
                "next_due_at": None,
                "suggested_resource_url": None if is_correct else "https://www.khanacademy.org/math/algebra/x2f8bb11595b61c86:quadratics-intro"
            }
    
    @staticmethod
    def get_progress(user_id: str, domain: str = "Quadratics") -> Dict[str, Any]:
        """
        Get learner progress dashboard data.
        
        Queries Neo4j for:
        1. All HAS_PROGRESS edges (mastery, attempts, streak, last_attempt)
        2. Recent Attempt nodes (for weekly stats)
        3. HAS_ERROR relationships (misconception counts)
        
        Args:
            user_id: Student ID
            domain: Skill domain
        
        Returns:
            {
                "user_id": "...",
                "domain": "Quadratics",
                "skills": [...],
                "top_misconceptions": [...],
                "weekly_stats": {...},
                "due_today": [...]
            }
        """
        try:
            # Load learner state
            state = load_user_state(user_id)
            
            # Map state to SkillProgress format
            skills = []
            for skill_id, skill_data in state.get("skills", {}).items():
                skills.append({
                    "skill_id": skill_id,
                    "name": EngineService._get_skill_name(skill_id),
                    "p_mastery": skill_data.get("p_mastery", 0.5),
                    "attempts": skill_data.get("attempts", 0),
                    "correct_count": skill_data.get("correct_count", 0),
                    "streak": skill_data.get("streak", 0),
                    "last_attempt": skill_data.get("last_attempt"),
                    "due_at": skill_data.get("due_at"),
                    "top_errors": []
                })
            
            # Calculate weekly stats
            total_attempts = sum(s.get("attempts", 0) for s in skills)
            total_correct = sum(s.get("correct_count", 0) for s in skills)
            
            return {
                "user_id": user_id,
                "domain": domain,
                "skills": skills,
                "top_misconceptions": [],
                "weekly_stats": {
                    "attempts_this_week": total_attempts,
                    "correct_this_week": total_correct,
                    "accuracy_this_week": total_correct / total_attempts if total_attempts > 0 else 0.0,
                    "skills_with_progress": len(skills)
                },
                "due_today": [s for s in skills if s.get("due_at") and s["due_at"] <= datetime.utcnow().isoformat()]
            }
        
        except Exception as e:
            raise ValueError(f"Failed to get progress: {e}")
    
    @staticmethod
    def _get_skill_name(skill_id: str) -> str:
        """Map skill ID to human-readable name."""
        names = {
            "quad.identify": "Identify Quadratic",
            "quad.vertex.form": "Convert to Vertex Form",
            "quad.factor.a1": "Factor Quadratics (a=1)",
            "quad.discriminant": "Use Discriminant",
        }
        return names.get(skill_id, skill_id)
