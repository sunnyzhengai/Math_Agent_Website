#!/usr/bin/env python3
"""
Minimal FastAPI server for Quadratic Equations Practice

Endpoints:
- GET / - Serves the web UI
- GET /api/question - Returns a random question with multiple choice answers
- POST /api/reset - Resets the template pool
"""

import sys
import os
import random
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from uuid import uuid4

# Add code directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "code"))
import quadratic_equations_by_completing_the_square as qe

app = FastAPI(title="Quadratic Equations Practice")

# Mount static files (web directory)
web_dir = Path(__file__).parent.parent / "web"
if web_dir.exists():
    app.mount("/static", StaticFiles(directory=str(web_dir)), name="static")

# Session storage: {session_id: {"remaining": [...], "correct": 0, "total": 0}}
sessions = {}


class QuestionResponse(BaseModel):
    """Response model for question endpoint"""
    equation: str
    choices: list[str]
    correct_answer: str
    progress: dict  # {"current": 5, "total": 24, "correct": 3, "answered": 5, "session_id": "..."}


class SubmitAnswerRequest(BaseModel):
    """Request model for submitting an answer"""
    session_id: str
    is_correct: bool


class SubmitAnswerResponse(BaseModel):
    """Response model for submitting an answer"""
    correct: int
    total: int


class ResetResponse(BaseModel):
    """Response model for reset endpoint"""
    message: str
    session_id: str


@app.get("/")
async def root():
    """Serve the main web page"""
    index_path = web_dir / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "Quadratic Equations Practice API", "docs": "/docs"}


@app.get("/api/question", response_model=QuestionResponse)
async def get_question(session_id: str = None):
    """Generate a random quadratic equation question

    Tracks templates to ensure all 24 are seen before repeating.
    Pass session_id to maintain progress across requests.
    """
    # Initialize or get session
    if not session_id or session_id not in sessions:
        session_id = str(uuid4())
        sessions[session_id] = {
            "remaining": list(range(1, 25)),
            "correct": 0,
            "total": 0
        }
        random.shuffle(sessions[session_id]["remaining"])

    # Get session data
    session = sessions[session_id]
    remaining = session["remaining"]

    # If pool exhausted, refill and shuffle
    if not remaining:
        session["remaining"] = list(range(1, 25))
        random.shuffle(session["remaining"])
        remaining = session["remaining"]

    # Pick next template from pool
    template_num = remaining.pop(0)
    template_func = getattr(qe, f'template_{template_num}')

    # Generate question
    equation, correct_letter, choices = template_func()

    # Calculate progress
    questions_answered = 24 - len(remaining)

    return QuestionResponse(
        equation=equation,
        choices=choices,
        correct_answer=correct_letter,
        progress={
            "current": questions_answered,
            "total": 24,
            "correct": session["correct"],
            "answered": session["total"],
            "session_id": session_id
        }
    )


@app.post("/api/submit", response_model=SubmitAnswerResponse)
async def submit_answer(request: SubmitAnswerRequest):
    """Record answer result and update score"""
    session_id = request.session_id

    if session_id not in sessions:
        # Session doesn't exist, return zeros
        return SubmitAnswerResponse(correct=0, total=0)

    session = sessions[session_id]
    session["total"] += 1
    if request.is_correct:
        session["correct"] += 1

    return SubmitAnswerResponse(
        correct=session["correct"],
        total=session["total"]
    )


@app.post("/api/reset", response_model=ResetResponse)
async def reset_session(session_id: str = None):
    """Reset the template pool for a session"""
    new_session_id = str(uuid4())
    sessions[new_session_id] = {
        "remaining": list(range(1, 25)),
        "correct": 0,
        "total": 0
    }
    random.shuffle(sessions[new_session_id]["remaining"])

    # Clean up old session if provided
    if session_id and session_id in sessions:
        del sessions[session_id]

    return ResetResponse(
        message="Session reset successfully",
        session_id=new_session_id
    )


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
