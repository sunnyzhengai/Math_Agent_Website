#!/usr/bin/env python3
"""
User Tracking Tests

Tests to ensure user tracking functionality works correctly:
1. Tracking data is correctly updated after answers
2. Category stats are accumulated properly
3. Skill stats are accumulated properly
4. Accuracy calculations are correct
5. Multiple users are tracked independently
"""

import sys
import pytest
from pathlib import Path
from fastapi.testclient import TestClient

# Add api directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "api"))

from server import app

client = TestClient(app)


# ============================================================================
# Test 1: Basic Tracking Initialization
# ============================================================================

def test_tracking_new_user():
    """New users should have empty tracking data"""
    response = client.get("/api/tracking?user_id=test_user_new")
    assert response.status_code == 200
    data = response.json()

    assert data["total_questions"] == 0
    assert data["total_correct"] == 0
    assert data["categories"] == {}
    assert data["skills"] == {}


# ============================================================================
# Test 2: Tracking Updates After Correct Answer
# ============================================================================

def test_tracking_correct_answer():
    """Tracking should update correctly after a correct answer"""
    user_id = "test_user_correct"

    # Get a question to create a session
    question_response = client.get("/api/question?skill_id=radicals.exponents")
    assert question_response.status_code == 200
    session_id = question_response.json()["progress"]["session_id"]

    # Submit correct answer
    submit_response = client.post("/api/submit", json={
        "session_id": session_id,
        "is_correct": True,
        "user_id": user_id
    })
    assert submit_response.status_code == 200

    # Check tracking data
    tracking_response = client.get(f"/api/tracking?user_id={user_id}")
    tracking = tracking_response.json()

    # Verify totals
    assert tracking["total_questions"] == 1
    assert tracking["total_correct"] == 1

    # Verify category stats
    assert "Radicals" in tracking["categories"]
    assert tracking["categories"]["Radicals"]["questions"] == 1
    assert tracking["categories"]["Radicals"]["correct"] == 1

    # Verify skill stats
    assert "radicals.exponents" in tracking["skills"]
    assert tracking["skills"]["radicals.exponents"]["questions"] == 1
    assert tracking["skills"]["radicals.exponents"]["correct"] == 1
    assert tracking["skills"]["radicals.exponents"]["name"] == "Exponents Refresher"


# ============================================================================
# Test 3: Tracking Updates After Incorrect Answer
# ============================================================================

def test_tracking_incorrect_answer():
    """Tracking should update correctly after an incorrect answer"""
    user_id = "test_user_incorrect"

    # Get a question
    question_response = client.get("/api/question?skill_id=quad.completing_square")
    session_id = question_response.json()["progress"]["session_id"]

    # Submit incorrect answer
    client.post("/api/submit", json={
        "session_id": session_id,
        "is_correct": False,
        "user_id": user_id
    })

    # Check tracking data
    tracking = client.get(f"/api/tracking?user_id={user_id}").json()

    # Verify totals
    assert tracking["total_questions"] == 1
    assert tracking["total_correct"] == 0

    # Verify category stats
    assert "Quadratics" in tracking["categories"]
    assert tracking["categories"]["Quadratics"]["questions"] == 1
    assert tracking["categories"]["Quadratics"]["correct"] == 0


# ============================================================================
# Test 4: Accumulation Across Multiple Questions
# ============================================================================

def test_tracking_accumulation():
    """Tracking should accumulate across multiple questions"""
    user_id = "test_user_accumulation"

    # Answer 3 questions: 2 correct, 1 incorrect
    for i, (skill_id, is_correct) in enumerate([
        ("radicals.exponents", True),
        ("radicals.simplifying", True),
        ("quad.completing_square", False)
    ]):
        question_response = client.get(f"/api/question?skill_id={skill_id}")
        session_id = question_response.json()["progress"]["session_id"]

        client.post("/api/submit", json={
            "session_id": session_id,
            "is_correct": is_correct,
            "user_id": user_id
        })

    # Check tracking data
    tracking = client.get(f"/api/tracking?user_id={user_id}").json()

    # Verify totals
    assert tracking["total_questions"] == 3
    assert tracking["total_correct"] == 2

    # Verify category accumulation
    assert tracking["categories"]["Radicals"]["questions"] == 2
    assert tracking["categories"]["Radicals"]["correct"] == 2
    assert tracking["categories"]["Quadratics"]["questions"] == 1
    assert tracking["categories"]["Quadratics"]["correct"] == 0

    # Verify individual skills
    assert tracking["skills"]["radicals.exponents"]["questions"] == 1
    assert tracking["skills"]["radicals.simplifying"]["questions"] == 1
    assert tracking["skills"]["quad.completing_square"]["questions"] == 1


# ============================================================================
# Test 5: Same Skill Multiple Times
# ============================================================================

def test_tracking_same_skill_multiple_times():
    """Tracking should accumulate stats for the same skill"""
    user_id = "test_user_same_skill"
    skill_id = "radicals.exponents"

    # Answer the same skill 3 times: 2 correct, 1 incorrect
    for is_correct in [True, True, False]:
        question_response = client.get(f"/api/question?skill_id={skill_id}")
        session_id = question_response.json()["progress"]["session_id"]

        client.post("/api/submit", json={
            "session_id": session_id,
            "is_correct": is_correct,
            "user_id": user_id
        })

    # Check tracking data
    tracking = client.get(f"/api/tracking?user_id={user_id}").json()

    # Verify totals
    assert tracking["total_questions"] == 3
    assert tracking["total_correct"] == 2

    # Verify skill stats accumulated correctly
    assert tracking["skills"]["radicals.exponents"]["questions"] == 3
    assert tracking["skills"]["radicals.exponents"]["correct"] == 2

    # Verify category stats
    assert tracking["categories"]["Radicals"]["questions"] == 3
    assert tracking["categories"]["Radicals"]["correct"] == 2


# ============================================================================
# Test 6: Multiple Users Independence
# ============================================================================

def test_tracking_multiple_users():
    """Different users should have independent tracking"""
    user1 = "test_user_1"
    user2 = "test_user_2"

    # User 1 answers 1 question correctly
    q1 = client.get("/api/question?skill_id=radicals.exponents")
    client.post("/api/submit", json={
        "session_id": q1.json()["progress"]["session_id"],
        "is_correct": True,
        "user_id": user1
    })

    # User 2 answers 2 questions incorrectly
    for _ in range(2):
        q2 = client.get("/api/question?skill_id=quad.completing_square")
        client.post("/api/submit", json={
            "session_id": q2.json()["progress"]["session_id"],
            "is_correct": False,
            "user_id": user2
        })

    # Check user 1 tracking
    tracking1 = client.get(f"/api/tracking?user_id={user1}").json()
    assert tracking1["total_questions"] == 1
    assert tracking1["total_correct"] == 1

    # Check user 2 tracking
    tracking2 = client.get(f"/api/tracking?user_id={user2}").json()
    assert tracking2["total_questions"] == 2
    assert tracking2["total_correct"] == 0

    # Verify they don't affect each other
    assert "Quadratics" not in tracking1["categories"]
    assert "Radicals" not in tracking2["categories"]


# ============================================================================
# Test 7: Default User ID
# ============================================================================

def test_tracking_default_user_id():
    """Submit should default to 'julia' if user_id not provided"""
    # Get a question
    question_response = client.get("/api/question?skill_id=radicals.exponents")
    session_id = question_response.json()["progress"]["session_id"]

    # Submit without user_id (should default to 'julia')
    client.post("/api/submit", json={
        "session_id": session_id,
        "is_correct": True
    })

    # Check tracking for 'julia'
    tracking = client.get("/api/tracking?user_id=julia").json()

    # Should have at least this submission
    assert tracking["total_questions"] >= 1


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
