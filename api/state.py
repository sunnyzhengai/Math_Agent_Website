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


# Singleton instance
progress_store = InMemoryProgressStore()
