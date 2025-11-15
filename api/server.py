#!/usr/bin/env python3
"""
Math Practice Platform - Multi-Skill API Server

Endpoints:
- GET / - Serves the web UI
- GET /api/skills - Returns list of available skills
- GET /api/question - Returns a random question with multiple choice answers
- POST /api/submit - Records answer result
- POST /api/reset - Resets the template pool
"""

import sys
import os
import random
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from uuid import uuid4

# Add code directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "code"))

# Import all available skill modules
import radicals_exponents_refresher
import radicals_understanding_radicals
import radicals_simplifying_radicals
import radicals_operations_with_radicals
import quadratics_completing_the_square
import quadratics_solving_with_square_roots
import quadratics_vertex_form
import quadratics_quadratic_formula
import quadratics_graphing_and_application

# Skill registry: maps skill_id to (module, template_count, display_name)
SKILLS = {
    "radicals.exponents": {
        "module": radicals_exponents_refresher,
        "template_count": 5,
        "name": "Exponents Refresher",
        "category": "Radicals"
    },
    "radicals.understanding": {
        "module": radicals_understanding_radicals,
        "template_count": 4,
        "name": "Understanding Radicals",
        "category": "Radicals"
    },
    "radicals.simplifying": {
        "module": radicals_simplifying_radicals,
        "template_count": 4,
        "name": "Simplifying Radicals",
        "category": "Radicals"
    },
    "radicals.operations": {
        "module": radicals_operations_with_radicals,
        "template_count": 4,
        "name": "Operations with Radicals",
        "category": "Radicals"
    },
    "quad.completing_square": {
        "module": quadratics_completing_the_square,
        "template_count": 24,
        "name": "Completing the Square",
        "category": "Quadratics"
    },
    "quad.solving": {
        "module": quadratics_solving_with_square_roots,
        "template_count": 8,
        "name": "Solving with Square Roots",
        "category": "Quadratics"
    },
    "quad.vertex_form": {
        "module": quadratics_vertex_form,
        "template_count": 8,
        "name": "Vertex Form",
        "category": "Quadratics"
    },
    "quad.formula": {
        "module": quadratics_quadratic_formula,
        "template_count": 12,
        "name": "Quadratic Formula",
        "category": "Quadratics"
    },
    "quad.graphing": {
        "module": quadratics_graphing_and_application,
        "template_count": 10,
        "name": "Graphing and Application",
        "category": "Quadratics"
    }
}

app = FastAPI(title="Math Practice Platform")

# Mount static files (web directory)
web_dir = Path(__file__).parent.parent / "web"
if web_dir.exists():
    app.mount("/static", StaticFiles(directory=str(web_dir)), name="static")

# Session storage: {
#   session_id: {
#     "skill_id": "...",
#     "remaining": [...],
#     "correct": 0,
#     "total": 0,
#     "seen_questions": set()  # Track actual questions to prevent duplicates
#   }
# }
sessions = {}


class SkillInfo(BaseModel):
    """Information about a skill"""
    skill_id: str
    name: str
    category: str
    template_count: int


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
    return {"message": "Math Practice Platform API", "docs": "/docs"}


@app.get("/api/skills")
async def get_skills():
    """Get list of available skills grouped by category"""
    # Group skills by category
    categories = {}
    for skill_id, skill_data in SKILLS.items():
        category = skill_data["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append({
            "skill_id": skill_id,
            "name": skill_data["name"],
            "template_count": skill_data["template_count"]
        })
    return categories


@app.get("/api/question", response_model=QuestionResponse)
async def get_question(skill_id: str = "quad.completing_square", session_id: str = None):
    """Generate a random question for the specified skill

    Tracks templates to ensure all are seen before repeating.
    Pass session_id to maintain progress across requests.
    """
    # Validate skill_id
    if skill_id not in SKILLS:
        raise HTTPException(status_code=400, detail=f"Invalid skill_id: {skill_id}")

    skill = SKILLS[skill_id]
    template_count = skill["template_count"]

    # Initialize or get session
    if not session_id or session_id not in sessions:
        session_id = str(uuid4())
        sessions[session_id] = {
            "skill_id": skill_id,
            "remaining": list(range(1, template_count + 1)),
            "correct": 0,
            "total": 0,
            "seen_questions": set()  # Track questions to avoid repeats
        }
        random.shuffle(sessions[session_id]["remaining"])

    # Get session data
    session = sessions[session_id]
    remaining = session["remaining"]

    # If pool exhausted, refill and shuffle
    if not remaining:
        session["remaining"] = list(range(1, template_count + 1))
        random.shuffle(session["remaining"])
        remaining = session["remaining"]

    # Pick next template from pool
    template_num = remaining.pop(0)
    module = skill["module"]
    template_func = getattr(module, f'template_{template_num}')

    # Generate question, retry up to 10 times if we get a duplicate
    max_attempts = 10
    equation = None
    seen_questions = session.get("seen_questions", set())

    for attempt in range(max_attempts):
        equation, correct_letter, choices = template_func()

        # Check if this exact question was seen before
        if equation not in seen_questions:
            # New question! Track it and use it
            seen_questions.add(equation)
            break

        # Duplicate detected, try again (unless it's the last attempt)
        if attempt < max_attempts - 1:
            continue
        else:
            # Give up after max attempts and use whatever we got
            # This can happen if the template has limited variation
            break

    # Update session's seen questions
    session["seen_questions"] = seen_questions

    # Calculate progress
    questions_answered = template_count - len(remaining)

    return QuestionResponse(
        equation=equation,
        choices=choices,
        correct_answer=correct_letter,
        progress={
            "current": questions_answered,
            "total": template_count,
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
