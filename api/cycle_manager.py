"""
Cycle mode manager: tracks "seen" question stems per (session_id, skill_id, difficulty).

Prevents repeats within a pool until exhausted, then wraps and starts fresh.
Uses LRU eviction to avoid unbounded memory growth in long-running servers.
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Dict, Set, Tuple
import asyncio
import time


PoolKey = Tuple[str, str, str]  # (session_id, skill_id, difficulty)


class LRUSeenBags:
    """
    Simple LRU cache for seen stems to avoid unbounded growth.
    Keyed by (session_id, skill_id, difficulty) -> set of stems.
    """

    def __init__(self, max_entries: int = 1000):
        self.max_entries = max_entries
        self._bags: Dict[PoolKey, Set[str]] = {}
        self._lru: OrderedDict[PoolKey, float] = OrderedDict()
        self._lock = asyncio.Lock()

    async def mark_seen(self, key: PoolKey, stem: str) -> None:
        """Mark a stem as seen in this pool."""
        async with self._lock:
            bag = self._bags.setdefault(key, set())
            bag.add(stem)
            self._touch(key)

    async def has_seen(self, key: PoolKey, stem: str) -> bool:
        """Check if a stem has been seen in this pool."""
        async with self._lock:
            self._touch(key)
            return stem in self._bags.get(key, set())

    async def size(self, key: PoolKey) -> int:
        """Get the number of unique stems seen in this pool."""
        async with self._lock:
            self._touch(key)
            return len(self._bags.get(key, set()))

    async def clear(self, key: PoolKey) -> None:
        """Clear all seen stems for this pool (start a new cycle)."""
        async with self._lock:
            self._bags[key] = set()
            self._touch(key)

    async def ensure_room(self) -> None:
        """Evict LRU entry if at capacity."""
        async with self._lock:
            while len(self._bags) > self.max_entries:
                # evict least recently used
                old_key, _ = self._lru.popitem(last=False)
                self._bags.pop(old_key, None)

    def _touch(self, key: PoolKey) -> None:
        """Update LRU timestamp for this key."""
        now = time.time()
        if key in self._lru:
            self._lru.move_to_end(key)
        self._lru[key] = now


# Singleton for the app lifetime
cycle_bags = LRUSeenBags(max_entries=2000)
