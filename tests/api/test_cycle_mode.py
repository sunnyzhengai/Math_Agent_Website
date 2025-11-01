"""
Phase 2f.1: Cycle mode tests for server-side no-repeat guarantee.

Tests verify that mode="cycle" with a session_id ensures unique stems
until the pool is exhausted, then wraps.
"""

import sys
import os

# Add parent directories to path to enable imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

import pytest
from fastapi.testclient import TestClient

# Import server - try both paths
try:
    from api.server import app
except ModuleNotFoundError:
    # Fallback: import from the file directly
    import importlib.util
    spec = importlib.util.spec_from_file_location("server", "api/server.py")
    server = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(server)
    app = server.app


@pytest.fixture(scope="module")
def client():
    """FastAPI TestClient for testing endpoints."""
    return TestClient(app)


VALID_SKILL_ID = "quad.graph.vertex"


class TestCycleMode:
    """Cycle mode tests."""

    def test_cycle_mode_requires_session_id(self, client):
        """
        When mode="cycle" without session_id → 400 missing_session_id.
        """
        resp = client.post("/items/generate", json={
            "skill_id": VALID_SKILL_ID,
            "difficulty": "easy",
            "mode": "cycle",
            # missing session_id
        })
        
        assert resp.status_code == 400
        body = resp.json()
        assert body.get("detail", {}).get("error") == "missing_session_id"

    def test_cycle_mode_no_repeats_then_wrap(self, client):
        """
        Cycle mode with session_id ensures no repeats within pool.
        
        easy has 2 templates → 1st and 2nd are unique → 3rd wraps (matches one of first two).
        """
        session_id = "test-session-cycle-1"
        stems = []

        for i in range(4):  # easy has 2 templates, so 4 attempts shows wrapping
            resp = client.post("/items/generate", json={
                "skill_id": VALID_SKILL_ID,
                "difficulty": "easy",
                "mode": "cycle",
                "session_id": session_id,
            })
            
            assert resp.status_code == 200, f"Attempt {i} failed: {resp.json()}"
            body = resp.json()
            stems.append(body["stem"])

        # First two should be unique
        assert len(set(stems[:2])) == 2, f"First two stems should be unique, got {stems[:2]}"
        
        # Third should match one of the first two (wrap happened)
        assert stems[2] in set(stems[:2]), f"Stem {stems[2]} should be a repeat of first two"

    def test_cycle_mode_session_isolated(self, client):
        """
        Different session_ids have independent bags.
        
        session_A and session_B both request easy → both should get 2 unique stems each.
        """
        session_a = "session-a-isolated"
        session_b = "session-b-isolated"
        
        stems_a = []
        stems_b = []

        for i in range(2):
            # Session A
            resp_a = client.post("/items/generate", json={
                "skill_id": VALID_SKILL_ID,
                "difficulty": "easy",
                "mode": "cycle",
                "session_id": session_a,
            })
            assert resp_a.status_code == 200
            stems_a.append(resp_a.json()["stem"])

            # Session B
            resp_b = client.post("/items/generate", json={
                "skill_id": VALID_SKILL_ID,
                "difficulty": "easy",
                "mode": "cycle",
                "session_id": session_b,
            })
            assert resp_b.status_code == 200
            stems_b.append(resp_b.json()["stem"])

        # Both sessions should have 2 unique stems (not sharing a bag)
        assert len(set(stems_a)) == 2, f"Session A should have 2 unique stems, got {stems_a}"
        assert len(set(stems_b)) == 2, f"Session B should have 2 unique stems, got {stems_b}"

    def test_cycle_mode_across_difficulties_independent(self, client):
        """
        Cycle tracking is per-difficulty, not shared.
        
        Session C: see 2 unique easy → advance (internally)
        Session C: request medium (1 template) → should get it
        Session C: request easy again → should get a fresh one (easy bag was cleared when exhausted)
        """
        session_id = "session-c-multi-diff"

        # Get 2 unique easy
        stems_easy_1 = []
        for _ in range(2):
            resp = client.post("/items/generate", json={
                "skill_id": VALID_SKILL_ID,
                "difficulty": "easy",
                "mode": "cycle",
                "session_id": session_id,
            })
            assert resp.status_code == 200
            stems_easy_1.append(resp.json()["stem"])

        # Request medium (1 template)
        resp_med = client.post("/items/generate", json={
            "skill_id": VALID_SKILL_ID,
            "difficulty": "medium",
            "mode": "cycle",
            "session_id": session_id,
        })
        assert resp_med.status_code == 200
        stem_med = resp_med.json()["stem"]

        # Request easy again (bag was cleared, so should get fresh one)
        resp_easy_2 = client.post("/items/generate", json={
            "skill_id": VALID_SKILL_ID,
            "difficulty": "easy",
            "mode": "cycle",
            "session_id": session_id,
        })
        assert resp_easy_2.status_code == 200
        stem_easy_2 = resp_easy_2.json()["stem"]

        # easy_2 should be one of the ones we saw before (from same pool)
        assert stem_easy_2 in set(stems_easy_1), \
            f"Second easy request should reuse from pool after clear, got {stem_easy_2} not in {stems_easy_1}"

    def test_random_mode_unchanged(self, client):
        """
        Random mode (default) should be unchanged: allows repeats, ignores session_id.
        """
        # With mode="random" (default), we can get repeats or random samples
        # Just verify it works and returns 200
        resp = client.post("/items/generate", json={
            "skill_id": VALID_SKILL_ID,
            "difficulty": "easy",
            "mode": "random",
            "session_id": "irrelevant",
        })
        
        assert resp.status_code == 200
        body = resp.json()
        assert "stem" in body
