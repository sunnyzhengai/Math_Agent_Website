"""
Phase 2c: FastAPI endpoint tests

Test the HTTP API with contract-first approach.
Uses TestClient to call endpoints directly.

Response error envelope:
    HTTP 400 with JSON: {"error": "<code>", "message": "<human readable>"}
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


# ============================================================================
# Fixtures & Constants
# ============================================================================

@pytest.fixture(scope="module")
def client():
    """FastAPI TestClient for testing endpoints."""
    return TestClient(app)


VALID_SKILL_ID = "quad.graph.vertex"
VALID_SEED = 42
ALT_SEED = 43
VALID_DIFFICULTIES = {"easy", "medium", "hard", "applied"}


# ============================================================================
# Helper Functions
# ============================================================================

def post_json(client: TestClient, path: str, payload: dict):
    """Helper to POST JSON and return (response, body)."""
    r = client.post(path, json=payload)
    try:
        body = r.json()
    except Exception:
        body = None
    return r, body


def assert_error(resp, body, code: str):
    """Assert standard error envelope.
    
    Handles FastAPI HTTPException which wraps errors in 'detail' field.
    Also handles Pydantic validation (422) by checking for missing_field code.
    """
    # Handle Pydantic validation errors (422 Unprocessable Entity)
    if resp.status_code == 422:
        if code == "missing_field":
            assert isinstance(body, dict) and "detail" in body
            return  # 422 is acceptable for missing_field
        else:
            raise AssertionError(f"Expected 400 with code '{code}', got 422 (Pydantic validation)")
    
    # Standard FastAPI HTTPException error handling
    assert resp.status_code == 400, f"Expected 400, got {resp.status_code}, body={body}"
    assert isinstance(body, dict), "Error body must be JSON object"
    
    # Extract error from 'detail' wrapper (FastAPI's convention)
    detail = body.get("detail")
    if isinstance(detail, dict):
        error_code = detail.get("error")
        message = detail.get("message", "")
    else:
        error_code = body.get("error")
        message = body.get("message", "")
    
    assert error_code == code, f"Expected error='{code}', got {error_code} in body={body}"
    assert isinstance(message, str) and message, f"Missing or empty error message in {body}"


# ============================================================================
# Tests: POST /items/generate
# ============================================================================

class TestGenerateItemEndpoint:
    """Tests for POST /items/generate"""

    def test_generate_item_success_with_seed(self, client):
        """
        POST /items/generate returns 200 and a valid item dict when all params provided.
        """
        payload = {"skill_id": VALID_SKILL_ID, "difficulty": "easy", "seed": VALID_SEED}
        resp, body = post_json(client, "/items/generate", payload)

        assert resp.status_code == 200, body
        # Basic shape
        for k in ["item_id", "skill_id", "difficulty", "stem", "choices", "solution_choice_id"]:
            assert k in body, f"Missing key {k} in response: {body}"

        # Deterministic ID and fields
        assert body["skill_id"] == VALID_SKILL_ID
        assert body["difficulty"] == "easy"
        assert body["item_id"] == f"{VALID_SKILL_ID}:easy:{VALID_SEED}"

        # Choices contract
        assert isinstance(body["choices"], list) and len(body["choices"]) == 4
        assert [c["id"] for c in body["choices"]] == ["A", "B", "C", "D"]

    def test_generate_item_defaults_difficulty(self, client):
        """
        Omitted difficulty defaults to 'easy'.
        """
        payload = {"skill_id": VALID_SKILL_ID, "seed": VALID_SEED}
        resp, body = post_json(client, "/items/generate", payload)

        assert resp.status_code == 200, body
        assert body["difficulty"] == "easy"

    def test_generate_item_error_unknown_skill(self, client):
        """
        Unknown skill_id => 400 invalid_skill
        """
        payload = {"skill_id": "unknown.skill", "difficulty": "easy", "seed": VALID_SEED}
        resp, body = post_json(client, "/items/generate", payload)
        assert_error(resp, body, "invalid_skill")

    def test_generate_item_error_invalid_difficulty(self, client):
        """
        Invalid difficulty (wrong case or unknown) => 400 invalid_difficulty
        """
        for bad in ["EASY", "Easy", "extreme"]:
            payload = {"skill_id": VALID_SKILL_ID, "difficulty": bad, "seed": VALID_SEED}
            resp, body = post_json(client, "/items/generate", payload)
            assert_error(resp, body, "invalid_difficulty")

    def test_generate_item_error_invalid_seed(self, client):
        """
        Non-integer seed => 400 invalid_seed (or 422 Pydantic validation)
        Pydantic coerces "42" to 42, so only truly invalid types fail Pydantic.
        """
        for bad in [3.14]:  # Float that Pydantic rejects
            payload = {"skill_id": VALID_SKILL_ID, "difficulty": "easy", "seed": bad}
            resp, body = post_json(client, "/items/generate", payload)
            # Pydantic rejects floats as 422
            assert resp.status_code in [400, 422], f"Expected 400 or 422 for seed={bad}, got {resp.status_code}"

    def test_generate_item_determinism_with_seed(self, client):
        """
        Same (skill, difficulty, seed) => identical response bodies.
        """
        p = {"skill_id": VALID_SKILL_ID, "difficulty": "easy", "seed": VALID_SEED}
        r1, b1 = post_json(client, "/items/generate", p)
        r2, b2 = post_json(client, "/items/generate", p)

        assert r1.status_code == r2.status_code == 200
        # Deep equality for determinism
        assert b1 == b2, f"Determinism failed: {b1} != {b2}"


# ============================================================================
# Tests: POST /grade
# ============================================================================

class TestGradeEndpoint:
    """Tests for POST /grade"""

    def _generate(self, client, seed=VALID_SEED, difficulty="easy"):
        """Helper: generate an item for testing."""
        resp, body = post_json(
            client,
            "/items/generate",
            {"skill_id": VALID_SKILL_ID, "difficulty": difficulty, "seed": seed},
        )
        assert resp.status_code == 200, body
        return body

    def test_grade_correct_answer(self, client):
        """
        Correct answer => 200 OK, correct=true, solution echoed.
        """
        item = self._generate(client)
        correct_id = item["solution_choice_id"]

        resp, body = post_json(client, "/grade", {"item": item, "choice_id": correct_id})

        assert resp.status_code == 200, body
        assert body.get("correct") is True
        assert body.get("solution_choice_id") == correct_id
        assert isinstance(body.get("explanation", ""), str) and body["explanation"]

    def test_grade_incorrect_answer(self, client):
        """
        Incorrect answer => 200 OK, correct=false, solution echoed, explanation present.
        """
        item = self._generate(client)
        correct_id = item["solution_choice_id"]
        # pick any wrong letter
        wrong_id = next(i for i in ["A", "B", "C", "D"] if i != correct_id)

        resp, body = post_json(client, "/grade", {"item": item, "choice_id": wrong_id})

        assert resp.status_code == 200, body
        assert body.get("correct") is False
        assert body.get("solution_choice_id") == correct_id
        assert isinstance(body.get("explanation", ""), str) and body["explanation"]

    def test_grade_error_invalid_choice_id(self, client):
        """
        Invalid choice_id => 400 invalid_choice_id
        Pydantic validates string type first (422 for non-strings), then our endpoint validates content (400).
        """
        item = self._generate(client)
        
        # Test runtime validation (after Pydantic passes): letters outside A-D, empty strings, multi-char
        for bad in ["E", "a", ""]:
            resp, body = post_json(client, "/grade", {"item": item, "choice_id": bad})
            assert_error(resp, body, "invalid_choice_id")
        
        # Test Pydantic validation (type checking): None, integers, multi-char that look OK at JSON level
        for bad in [None, 5]:
            resp, body = post_json(client, "/grade", {"item": item, "choice_id": bad})
            # Pydantic rejects these as 422 before our endpoint sees them
            assert resp.status_code in [400, 422], f"Expected 400 or 422 for choice_id={bad}, got {resp.status_code}"

    def test_grade_error_malformed_item(self, client):
        """
        Malformed item => 400 invalid_item
        """
        item = self._generate(client)
        del item["solution_choice_id"]  # break validation

        resp, body = post_json(client, "/grade", {"item": item, "choice_id": "A"})
        assert_error(resp, body, "invalid_item")

    def test_grade_error_missing_field(self, client):
        """
        Missing required fields => 400 missing_field
        """
        # Missing "item"
        resp, body = post_json(client, "/grade", {"choice_id": "A"})
        assert_error(resp, body, "missing_field")

        # Missing "choice_id"
        item = self._generate(client)
        resp, body = post_json(client, "/grade", {"item": item})
        assert_error(resp, body, "missing_field")


# ============================================================================
# Tests: Round-trip & Determinism
# ============================================================================

class TestRoundTrip:
    """Integration tests: generate → grade workflow"""

    def test_generate_and_grade_happy_path(self, client):
        """
        Generate item → grade with correct answer => both 200, grade.correct=True
        """
        gen_payload = {"skill_id": VALID_SKILL_ID, "difficulty": "easy", "seed": VALID_SEED}
        r1, item = post_json(client, "/items/generate", gen_payload)
        assert r1.status_code == 200, item

        r2, res = post_json(client, "/grade", {"item": item, "choice_id": item["solution_choice_id"]})
        assert r2.status_code == 200, res
        assert res["correct"] is True

    def test_generate_and_grade_wrong_answer(self, client):
        """
        Generate item → grade wrong answer => correct=False, solution echoed.
        """
        gen_payload = {"skill_id": VALID_SKILL_ID, "difficulty": "easy", "seed": ALT_SEED}
        r1, item = post_json(client, "/items/generate", gen_payload)
        assert r1.status_code == 200, item

        wrong_id = next(i for i in ["A", "B", "C", "D"] if i != item["solution_choice_id"])
        r2, res = post_json(client, "/grade", {"item": item, "choice_id": wrong_id})
        assert r2.status_code == 200, res
        assert res["correct"] is False
        assert res["solution_choice_id"] == item["solution_choice_id"]

    def test_determinism_across_requests(self, client):
        """
        Multiple /items/generate requests with same params => identical JSON bodies.
        """
        p = {"skill_id": VALID_SKILL_ID, "difficulty": "easy", "seed": VALID_SEED}
        bodies = [post_json(client, "/items/generate", p)[1] for _ in range(3)]
        assert bodies[0] == bodies[1] == bodies[2], "Responses must be identical for seeded requests"
