"""
In-memory mastery state store (per-session, per-skill).

⚠️  Single-process, volatile: mastery lost on server restart.

TODO: Add optional persistence (Redis/SQLite) for production.
TODO: Implement per-skill locking for concurrent updates (currently uses global lock).
"""

from __future__ import annotations

import asyncio
from typing import Dict

from engine.mastery import SkillMastery


class InMemoryProgressStore:
    """
    Per-session mastery store:
      sessions: Dict[session_id, Dict[skill_id, SkillMastery]]

    Thread-safe with asyncio.Lock.
    """

    def __init__(self) -> None:
        self._sessions: Dict[str, Dict[str, SkillMastery]] = {}
        self._lock = asyncio.Lock()

    async def get_session(self, session_id: str) -> Dict[str, SkillMastery]:
        """Get a copy of all mastery state for a session."""
        async with self._lock:
            return dict(self._sessions.get(session_id, {}))

    async def upsert_skill(
        self, session_id: str, skill_id: str, mastery: SkillMastery
    ) -> None:
        """Update a single skill's mastery state (atomic at session level)."""
        async with self._lock:
            if session_id not in self._sessions:
                self._sessions[session_id] = {}
            self._sessions[session_id][skill_id] = mastery

    def snapshot(self) -> dict:
        """
        Return a JSON-serializable snapshot of all sessions.
        
        Converts SkillMastery dataclass objects to dicts.
        Shape: {"sessions": {session_id: {skill_id: {p, attempts, streak, last_ts}}}}
        
        Note: NOT async; caller should hold lock if needed.
        """
        sessions_dict = {}
        for session_id, skills in self._sessions.items():
            sessions_dict[session_id] = {}
            for skill_id, mastery in skills.items():
                sessions_dict[session_id][skill_id] = {
                    "p": mastery.p,
                    "attempts": mastery.attempts,
                    "streak": mastery.streak,
                    "last_ts": mastery.last_ts,
                }
        return {"sessions": sessions_dict}

    def restore(self, payload: dict) -> None:
        """
        Restore state from persisted JSON payload.
        
        Converts dict representations back to SkillMastery dataclass objects.
        
        Note: NOT async; caller should hold lock if needed.
        Idempotent: replaces current state entirely.
        """
        try:
            sessions = payload.get("sessions", {})
            if not isinstance(sessions, dict):
                return

            restored = {}
            for session_id, skills in sessions.items():
                if not isinstance(skills, dict):
                    continue
                restored[session_id] = {}
                for skill_id, mastery_dict in skills.items():
                    if not isinstance(mastery_dict, dict):
                        continue
                    try:
                        restored[session_id][skill_id] = SkillMastery(
                            p=float(mastery_dict.get("p", 0.5)),
                            attempts=int(mastery_dict.get("attempts", 0)),
                            streak=int(mastery_dict.get("streak", 0)),
                            last_ts=float(mastery_dict.get("last_ts", 0.0)),
                        )
                    except (ValueError, TypeError):
                        # Skip malformed entries
                        continue

            self._sessions = restored
        except Exception:
            # Fail-open: don't crash on restore errors
            pass


# Singleton instance
progress_store = InMemoryProgressStore()
