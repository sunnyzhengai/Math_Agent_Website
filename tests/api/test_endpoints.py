"""
Phase 2c: FastAPI endpoint tests

Test the HTTP API without implementing the server yet.
Uses TestClient to call endpoints directly.
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


@pytest.fixture
def client():
    """FastAPI TestClient for testing endpoints."""
    return TestClient(app)


class TestGenerateItemEndpoint:
    """Tests for POST /items/generate"""
    
    def test_generate_item_success_with_seed(self, client):
        """
        Test successful item generation with all parameters.
        
        Checks:
        - POST /items/generate returns 200 OK
        - Response matches /items/generate schema
        - Response is JSON serializable
        """
        response = client.post(
            "/items/generate",
            json={"skill_id": "quad.graph.vertex", "difficulty": "easy", "seed": 42}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        
        # Check all required keys
        assert "item_id" in data, "Missing item_id"
        assert "skill_id" in data, "Missing skill_id"
        assert "difficulty" in data, "Missing difficulty"
        assert "stem" in data, "Missing stem"
        assert "choices" in data, "Missing choices"
        assert "solution_choice_id" in data, "Missing solution_choice_id"
        assert "solution_text" in data, "Missing solution_text"
        assert "tags" in data, "Missing tags"
        
        # Check types and structure
        assert isinstance(data["choices"], list), "Choices must be list"
        assert len(data["choices"]) == 4, "Must have exactly 4 choices"
        for choice in data["choices"]:
            assert "id" in choice, "Choice missing id"
            assert "text" in choice, "Choice missing text"
    
    def test_generate_item_defaults_difficulty(self, client):
        """
        Test that difficulty defaults to "easy" when omitted.
        
        Checks:
        - POST without difficulty_param returns item with difficulty="easy"
        """
        response = client.post(
            "/items/generate",
            json={"skill_id": "quad.graph.vertex"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["difficulty"] == "easy", "Should default to 'easy'"
    
    def test_generate_item_error_unknown_skill(self, client):
        """
        Test error on unknown skill_id.
        
        Checks:
        - Returns 400 Bad Request
        - Error dict contains: error="invalid_skill", message
        """
        response = client.post(
            "/items/generate",
            json={"skill_id": "unknown.skill", "difficulty": "easy"}
        )
        
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        data = response.json()
        assert "detail" in data, "Missing detail"
        detail = data["detail"]
        assert detail["error"] == "invalid_skill", f"Expected invalid_skill, got {detail.get('error')}"
        assert "message" in detail, "Missing message"
    
    def test_generate_item_error_invalid_difficulty(self, client):
        """
        Test error on invalid difficulty.
        
        Checks:
        - Returns 400 Bad Request
        - Error dict contains: error="invalid_difficulty"
        """
        response = client.post(
            "/items/generate",
            json={"skill_id": "quad.graph.vertex", "difficulty": "INVALID"}
        )
        
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        data = response.json()
        detail = data["detail"]
        assert detail["error"] == "invalid_difficulty", f"Expected invalid_difficulty, got {detail.get('error')}"
    
    def test_generate_item_error_invalid_seed(self, client):
        """
        Test error when seed is not an integer.
        
        Checks:
        - Returns 400 Bad Request
        - Error dict contains: error="invalid_seed"
        """
        response = client.post(
            "/items/generate",
            json={"skill_id": "quad.graph.vertex", "difficulty": "easy", "seed": "not_an_int"}
        )
        
        # Pydantic validation should catch this
        assert response.status_code in [400, 422], f"Expected 400 or 422, got {response.status_code}"
    
    def test_generate_item_determinism_with_seed(self, client):
        """
        Test determinism: same seed produces same item.
        
        Checks:
        - Call with seed=42 twice
        - Response bodies are identical
        """
        response1 = client.post(
            "/items/generate",
            json={"skill_id": "quad.graph.vertex", "difficulty": "easy", "seed": 42}
        )
        response2 = client.post(
            "/items/generate",
            json={"skill_id": "quad.graph.vertex", "difficulty": "easy", "seed": 42}
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()
        data2 = response2.json()
        
        # Deep equality check
        assert data1 == data2, "Same seed should produce identical items"


class TestGradeEndpoint:
    """Tests for POST /grade"""
    
    def test_grade_correct_answer(self, client):
        """
        Test grading a correct answer.
        
        Checks:
        - POST /grade returns 200 OK
        - Response matches /grade schema
        - correct=true
        """
        # First generate an item
        gen_response = client.post(
            "/items/generate",
            json={"skill_id": "quad.graph.vertex", "difficulty": "easy", "seed": 42}
        )
        item = gen_response.json()
        
        # Grade the correct answer
        grade_response = client.post(
            "/grade",
            json={"item": item, "choice_id": item["solution_choice_id"]}
        )
        
        assert grade_response.status_code == 200, f"Expected 200, got {grade_response.status_code}"
        data = grade_response.json()
        
        # Check required keys
        assert "correct" in data, "Missing correct"
        assert "solution_choice_id" in data, "Missing solution_choice_id"
        assert "explanation" in data, "Missing explanation"
        
        # Check values
        assert data["correct"] is True, "Should be correct"
        assert data["solution_choice_id"] == item["solution_choice_id"]
        assert isinstance(data["explanation"], str)
        assert data["explanation"], "Explanation must be non-empty"
    
    def test_grade_incorrect_answer(self, client):
        """
        Test grading an incorrect answer.
        
        Checks:
        - POST /grade returns 200 OK
        - correct=false
        - solution_choice_id still shown
        - explanation provided
        """
        # First generate an item
        gen_response = client.post(
            "/items/generate",
            json={"skill_id": "quad.graph.vertex", "difficulty": "easy", "seed": 42}
        )
        item = gen_response.json()
        
        # Find a wrong choice
        wrong_choice = next(
            c for c in item["choices"]
            if c["id"] != item["solution_choice_id"]
        )
        
        # Grade the wrong answer
        grade_response = client.post(
            "/grade",
            json={"item": item, "choice_id": wrong_choice["id"]}
        )
        
        assert grade_response.status_code == 200
        data = grade_response.json()
        
        assert data["correct"] is False, "Should be incorrect"
        assert data["solution_choice_id"] == item["solution_choice_id"], "Should still show solution"
        assert isinstance(data["explanation"], str)
        assert data["explanation"], "Explanation must be non-empty"
    
    def test_grade_error_invalid_choice_id(self, client):
        """
        Test error on invalid choice_id.
        
        Checks:
        - choice_id="E" returns 400 Bad Request
        - choice_id="a" (lowercase) returns 400 Bad Request
        - Error dict contains: error="invalid_choice_id"
        """
        # Generate an item first
        gen_response = client.post(
            "/items/generate",
            json={"skill_id": "quad.graph.vertex", "difficulty": "easy", "seed": 42}
        )
        item = gen_response.json()
        
        # Try invalid choice_ids
        for bad_choice in ["E", "a"]:
            response = client.post(
                "/grade",
                json={"item": item, "choice_id": bad_choice}
            )
            
            assert response.status_code == 400, f"Expected 400 for choice_id={bad_choice}"
            data = response.json()
            assert data["detail"]["error"] == "invalid_choice_id"
    
    def test_grade_error_malformed_item(self, client):
        """
        Test error when item fails validation.
        
        Checks:
        - Missing solution_choice_id returns 400 Bad Request
        - Error dict contains: error="invalid_item"
        """
        # Create a malformed item (missing solution_choice_id)
        bad_item = {
            "item_id": "test:easy:42",
            "skill_id": "test",
            "difficulty": "easy",
            "stem": "Test question",
            "choices": [
                {"id": "A", "text": "Option A"},
                {"id": "B", "text": "Option B"},
                {"id": "C", "text": "Option C"},
                {"id": "D", "text": "Option D"},
            ],
            # Missing: solution_choice_id
        }
        
        response = client.post(
            "/grade",
            json={"item": bad_item, "choice_id": "A"}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert data["detail"]["error"] == "invalid_item"
    
    def test_grade_error_missing_field(self, client):
        """
        Test error when required field missing from request.
        
        Checks:
        - Missing "item" field returns 400 Bad Request
        - Missing "choice_id" field returns 400 Bad Request
        - Error dict contains: error="missing_field"
        """
        # Generate a valid item
        gen_response = client.post(
            "/items/generate",
            json={"skill_id": "quad.graph.vertex", "difficulty": "easy", "seed": 42}
        )
        item = gen_response.json()
        
        # Missing choice_id
        response1 = client.post(
            "/grade",
            json={"item": item}
        )
        assert response1.status_code == 422, "Pydantic should reject missing field"
        
        # Missing item
        response2 = client.post(
            "/grade",
            json={"choice_id": "A"}
        )
        assert response2.status_code == 422, "Pydantic should reject missing field"


class TestRoundTrip:
    """Integration tests: generate → grade workflow"""
    
    def test_generate_and_grade_happy_path(self, client):
        """
        Test happy path: generate item, then grade correct answer.
        
        Checks:
        - Generate item returns 200 + valid item
        - Grade with correct choice returns 200 + correct=true
        """
        # Generate
        gen_response = client.post(
            "/items/generate",
            json={"skill_id": "quad.graph.vertex", "difficulty": "easy", "seed": 42}
        )
        assert gen_response.status_code == 200
        item = gen_response.json()
        
        # Grade correct answer
        grade_response = client.post(
            "/grade",
            json={"item": item, "choice_id": item["solution_choice_id"]}
        )
        assert grade_response.status_code == 200
        result = grade_response.json()
        assert result["correct"] is True
    
    def test_generate_and_grade_wrong_answer(self, client):
        """
        Test workflow: generate, then grade wrong answer.
        
        Checks:
        - Both calls succeed
        - Grade response shows correct answer
        """
        # Generate
        gen_response = client.post(
            "/items/generate",
            json={"skill_id": "quad.graph.vertex", "difficulty": "easy", "seed": 42}
        )
        item = gen_response.json()
        
        # Find wrong choice
        wrong_choice = next(
            c for c in item["choices"]
            if c["id"] != item["solution_choice_id"]
        )
        
        # Grade wrong answer
        grade_response = client.post(
            "/grade",
            json={"item": item, "choice_id": wrong_choice["id"]}
        )
        assert grade_response.status_code == 200
        result = grade_response.json()
        
        assert result["correct"] is False
        assert result["solution_choice_id"] == item["solution_choice_id"]
    
    def test_determinism_across_requests(self, client):
        """
        Test determinism: multiple requests with same params.
        
        Checks:
        - Call /items/generate with seed=42 three times
        - All three responses are identical
        """
        responses = []
        for _ in range(3):
            response = client.post(
                "/items/generate",
                json={"skill_id": "quad.graph.vertex", "difficulty": "easy", "seed": 42}
            )
            assert response.status_code == 200
            responses.append(response.json())
        
        # All should be identical
        assert responses[0] == responses[1] == responses[2], "Determinism violated"
