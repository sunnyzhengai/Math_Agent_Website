"""
Phase 2c: FastAPI endpoint tests

Test the HTTP API without implementing the server yet.
Uses TestClient to call endpoints directly.
"""

import pytest
from fastapi.testclient import TestClient
from api.server import app  # Server stub (to be implemented)


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
        pass
    
    def test_generate_item_defaults_difficulty(self, client):
        """
        Test that difficulty defaults to "easy" when omitted.
        
        Checks:
        - POST without difficulty_param returns item with difficulty="easy"
        """
        pass
    
    def test_generate_item_error_unknown_skill(self, client):
        """
        Test error on unknown skill_id.
        
        Checks:
        - Returns 400 Bad Request
        - Error dict contains: error="invalid_skill", message
        """
        pass
    
    def test_generate_item_error_invalid_difficulty(self, client):
        """
        Test error on invalid difficulty.
        
        Checks:
        - Returns 400 Bad Request
        - Error dict contains: error="invalid_difficulty"
        """
        pass
    
    def test_generate_item_error_invalid_seed(self, client):
        """
        Test error when seed is not an integer.
        
        Checks:
        - Returns 400 Bad Request
        - Error dict contains: error="invalid_seed"
        """
        pass
    
    def test_generate_item_determinism_with_seed(self, client):
        """
        Test determinism: same seed produces same item.
        
        Checks:
        - Call with seed=42 twice
        - Response bodies are identical
        """
        pass


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
        pass
    
    def test_grade_incorrect_answer(self, client):
        """
        Test grading an incorrect answer.
        
        Checks:
        - POST /grade returns 200 OK
        - correct=false
        - solution_choice_id still shown
        - explanation provided
        """
        pass
    
    def test_grade_error_invalid_choice_id(self, client):
        """
        Test error on invalid choice_id.
        
        Checks:
        - choice_id="E" returns 400 Bad Request
        - choice_id="a" (lowercase) returns 400 Bad Request
        - Error dict contains: error="invalid_choice_id"
        """
        pass
    
    def test_grade_error_malformed_item(self, client):
        """
        Test error when item fails validation.
        
        Checks:
        - Missing solution_choice_id returns 400 Bad Request
        - Error dict contains: error="invalid_item"
        """
        pass
    
    def test_grade_error_missing_field(self, client):
        """
        Test error when required field missing from request.
        
        Checks:
        - Missing "item" field returns 400 Bad Request
        - Missing "choice_id" field returns 400 Bad Request
        - Error dict contains: error="missing_field"
        """
        pass


class TestRoundTrip:
    """Integration tests: generate → grade workflow"""
    
    def test_generate_and_grade_happy_path(self, client):
        """
        Test happy path: generate item, then grade correct answer.
        
        Checks:
        - Generate item returns 200 + valid item
        - Grade with correct choice returns 200 + correct=true
        """
        pass
    
    def test_generate_and_grade_wrong_answer(self, client):
        """
        Test workflow: generate, then grade wrong answer.
        
        Checks:
        - Both calls succeed
        - Grade response shows correct answer
        """
        pass
    
    def test_determinism_across_requests(self, client):
        """
        Test determinism: multiple requests with same params.
        
        Checks:
        - Call /items/generate with seed=42 three times
        - All three responses are identical
        """
        pass
