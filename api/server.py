"""
FastAPI server for Math Agent engine.

Exposes /items/generate and /grade endpoints.
See api/CONTRACTS.md for request/response schemas.
"""

import os
import sys
import json
import time
import asyncio
import contextlib
import tempfile
from pathlib import Path
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, Literal, Dict, Any
from collections import OrderedDict
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from engine.templates import generate_item, SKILL_TEMPLATES
from engine.grader import grade_response
from engine.validators import validate_item

# Import mastery & planner
from engine.mastery import update_progress, SkillMastery
from engine.planner import plan_next_difficulty

# Import persistence
def load_json(path: str) -> Optional[Dict[str, Any]]:
    """Load JSON from a file."""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None
    except Exception:
        return None


def save_json_atomic(path: str, data: Dict[str, Any]) -> None:
    """Save JSON to a file atomically."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        json.dump(data, f)
        f.flush()
        os.fsync(f.fileno())
    try:
        os.replace(f.name, path)
    except FileNotFoundError:
        # If the original file doesn't exist, just rename the new file
        os.rename(f.name, path)
    except Exception:
        os.remove(f.name)
        raise


# Import models (extended schemas)
try:
    from api.models import (
        ProgressGetRequest, ProgressGetResponse, SkillProgress,
        PlannerNextRequest, PlannerNextResponse,
        GradeRequestExtended
    )
except ImportError:
    # If models.py doesn't exist yet, define minimal stubs
    ProgressGetRequest = None
    ProgressGetResponse = None
    PlannerNextRequest = None
    PlannerNextResponse = None
    GradeRequestExtended = None

# Import state store
try:
    from api.state import progress_store
except ImportError:
    # Fallback: minimal in-memory store
    progress_store = None

# Import cycle_manager - use absolute import with fallback
try:
    from api.cycle_manager import cycle_bags
except ImportError:
    import importlib.util
    spec = importlib.util.spec_from_file_location("cycle_manager", os.path.join(os.path.dirname(__file__), "cycle_manager.py"))
    if spec and spec.loader:
        cycle_manager_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cycle_manager_module)
        cycle_bags = cycle_manager_module.cycle_bags
    else:
        raise ImportError("Could not load cycle_manager")

# Import telemetry - use absolute import with fallback
try:
    from api.telemetry import log_event
except ImportError:
    import importlib.util
    spec = importlib.util.spec_from_file_location("telemetry", os.path.join(os.path.dirname(__file__), "telemetry.py"))
    if spec and spec.loader:
        telemetry_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(telemetry_module)
        log_event = telemetry_module.log_event
    else:
        raise ImportError("Could not load telemetry")


# ============================================================================
# Cycle Manager (inline to avoid import issues in tests)
# ============================================================================

PoolKey = tuple  # (session_id, skill_id, difficulty)


class LRUSeenBags:
    """
    Simple LRU cache for seen stems to avoid unbounded growth.
    Keyed by (session_id, skill_id, difficulty) -> set of stems.
    """

    def __init__(self, max_entries: int = 1000):
        self.max_entries = max_entries
        self._bags: dict = {}
        self._lru: OrderedDict = OrderedDict()
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

    async def get_seen_stems(self, key: PoolKey) -> set:
        """Get the set of seen stems for this pool."""
        async with self._lock:
            self._touch(key)
            return self._bags.get(key, set()).copy()

    def _touch(self, key: PoolKey) -> None:
        """Update LRU timestamp for this key."""
        now = time.time()
        if key in self._lru:
            self._lru.move_to_end(key)
        self._lru[key] = now


# Singleton for the app lifetime
cycle_bags = LRUSeenBags(max_entries=2000)


# ============================================================================
# Persistence Configuration
# ============================================================================

PROGRESS_PATH = os.getenv("PROGRESS_PATH", "data/progress.json")
PROGRESS_AUTOSAVE_SECS = float(os.getenv("PROGRESS_AUTOSAVE_SECS", "0"))  # 0 = disabled

_autosave_task = None


async def _autosave_loop() -> None:
    """Background task to save mastery state periodically."""
    interval = PROGRESS_AUTOSAVE_SECS
    if interval <= 0:
        return

    while True:
        try:
            await asyncio.sleep(interval)
            if progress_store:
                async with progress_store._lock:
                    save_json_atomic(PROGRESS_PATH, progress_store.snapshot())
        except asyncio.CancelledError:
            break
        except Exception:
            # fail-open: never crash the server on persist errors
            pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage app lifecycle: load state on startup, save on shutdown.
    
    Environment variables:
      PROGRESS_PATH: where to persist mastery (default: data/progress.json)
      PROGRESS_AUTOSAVE_SECS: autosave interval in seconds (default: 0 = disabled)
    """
    # --- STARTUP ---
    try:
        if progress_store:
            payload = load_json(PROGRESS_PATH)
            if payload:
                async with progress_store._lock:
                    progress_store.restore(payload)
    except Exception:
        pass  # fail-open

    global _autosave_task
    if PROGRESS_AUTOSAVE_SECS > 0 and progress_store:
        _autosave_task = asyncio.create_task(_autosave_loop())

    yield

    # --- SHUTDOWN ---
    try:
        if _autosave_task:
            _autosave_task.cancel()
            with contextlib.suppress(Exception):
                await _autosave_task
    except Exception:
        pass

    try:
        if progress_store:
            async with progress_store._lock:
                save_json_atomic(PROGRESS_PATH, progress_store.snapshot())
    except Exception:
        pass  # fail-open


app = FastAPI(title="Math Agent API", version="0.1.0", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add security headers middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    # Core security headers (conservative defaults)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    
    # CSP – strict (no inline scripts/styles, safe for our static-only UI)
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self'; "
        "img-src 'self' data:; "
        "connect-src 'self'; "
        "font-src 'self'; "
        "object-src 'none'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self'"
    )
    return response


# ============================================================================
# Request/Response Models (Pydantic)
# ============================================================================

class GenerateItemRequest(BaseModel):
    """Request schema for POST /items/generate"""
    skill_id: str
    difficulty: Optional[str] = None
    seed: Optional[int] = None
    mode: Literal["random", "cycle"] = "random"
    session_id: Optional[str] = None
    use_parameterized: bool = False  # Enable infinite question variations


class ChoiceSchema(BaseModel):
    """Choice object in item"""
    id: str
    text: str


class GenerateItemResponse(BaseModel):
    """Response schema for POST /items/generate"""
    item_id: str
    skill_id: str
    difficulty: str
    stem: str
    choices: List[ChoiceSchema]
    solution_choice_id: str
    solution_text: str
    tags: List[str]
    pool_exhausted: Optional[bool] = False  # True when all templates have been seen
    templates_remaining: Optional[int] = None  # How many templates left in pool


class GradeRequest(BaseModel):
    """Request schema for POST /grade"""
    item: dict
    choice_id: str
    # NEW (optional): for mastery tracking
    session_id: Optional[str] = None
    confidence: Optional[int] = None  # 1-5, None for neutral


class GradeResponse(BaseModel):
    """Response schema for POST /grade"""
    correct: bool
    solution_choice_id: str
    explanation: str


class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str
    message: str


class TelemetryEvent(BaseModel):
    """Telemetry event for student interactions"""
    event_type: Literal["question_presented", "question_answered", "session_summary"]
    timestamp: str
    session_id: str
    user_id: Optional[str] = None
    question_id: Optional[str] = None
    skill_id: Optional[str] = None
    difficulty: Optional[str] = None
    generation_method: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    question_stem: Optional[str] = None
    correct_answer: Optional[str] = None
    choices: Optional[List[str]] = None
    distractor_types: Optional[List[Optional[str]]] = None
    student_answer: Optional[str] = None
    is_correct: Optional[bool] = None
    distractor_type_chosen: Optional[str] = None
    time_to_answer_ms: Optional[int] = None
    attempt_number: Optional[int] = None
    # Session summary fields
    total_questions: Optional[int] = None
    correct_count: Optional[int] = None
    accuracy: Optional[float] = None
    total_time_ms: Optional[int] = None
    avg_time_per_question_ms: Optional[float] = None
    skills_practiced: Optional[List[str]] = None
    difficulty_distribution: Optional[Dict[str, int]] = None


class TelemetryResponse(BaseModel):
    """Response for telemetry logging"""
    success: bool
    message: str


# ============================================================================
# Endpoints
# ============================================================================

@app.post("/items/generate", response_model=GenerateItemResponse)
async def generate_item_endpoint(request: GenerateItemRequest):
    """
    Generate a new math question item.
    
    Supports two modes:
    - "random" (default): standard random generation
    - "cycle": deterministic no-repeat within (session_id, skill_id, difficulty)
    
    See api/CONTRACTS.md for full specification.
    
    Args:
        request: GenerateItemRequest with skill_id, difficulty (optional), seed (optional), mode, session_id
    
    Returns:
        GenerateItemResponse matching the item schema
    
    Raises:
        HTTPException 400: invalid_skill, invalid_difficulty, invalid_seed, missing_session_id
    """
    # Validate cycle mode parameters
    if request.mode == "cycle" and not request.session_id:
        raise HTTPException(
            status_code=400,
            detail={"error": "missing_session_id", "message": "session_id is required when mode='cycle'"}
        )
    
    # Fast path: random mode (unchanged)
    if request.mode != "cycle":
        try:
            t0 = time.time()
            item = generate_item(
                skill_id=request.skill_id,
                difficulty=request.difficulty,
                seed=request.seed,
                use_parameterized=request.use_parameterized,
            )
            latency_ms = float((time.time() - t0) * 1000.0)
            
            # Log telemetry (async, don't await in sync path; fire-and-forget)
            try:
                asyncio.create_task(log_event(
                    "generate",
                    session_id=request.session_id,
                    mode="random",
                    skill_id=item["skill_id"],
                    difficulty=item["difficulty"],
                    item_id=item["item_id"],
                    stem=item["stem"],
                    choice_ids=[c["id"] for c in item["choices"]],
                    latency_ms=latency_ms,
                ))
            except Exception:
                pass  # fail-open: don't crash if telemetry fails
            
            return GenerateItemResponse(**item)
        except ValueError as e:
            error_msg = str(e)
            
            # Map engine errors to API errors
            if error_msg == "unknown_skill":
                raise HTTPException(
                    status_code=400,
                    detail={"error": "invalid_skill", "message": f"Unknown skill_id: {request.skill_id}"}
                )
            elif error_msg == "invalid_difficulty":
                raise HTTPException(
                    status_code=400,
                    detail={"error": "invalid_difficulty", "message": f"Invalid difficulty: {request.difficulty}"}
                )
            elif error_msg == "invalid_seed":
                raise HTTPException(
                    status_code=400,
                    detail={"error": "invalid_seed", "message": f"Seed must be an integer, got {type(request.seed).__name__}"}
                )
            else:
                raise HTTPException(status_code=500, detail={"error": "internal_error", "message": str(e)})
    
    # Cycle mode: guarantee no repeats until pool exhausted
    difficulty = request.difficulty or "easy"
    
    # Validate skill and difficulty exist
    
    skill_templates = SKILL_TEMPLATES.get(request.skill_id)
    if not skill_templates:
        raise HTTPException(
            status_code=400,
            detail={"error": "invalid_skill", "message": f"Unknown skill_id: {request.skill_id}"}
        )
    
    if difficulty not in skill_templates:
        raise HTTPException(
            status_code=400,
            detail={"error": "invalid_difficulty", "message": f"Invalid difficulty: {difficulty}"}
        )
    
    pool = skill_templates[difficulty]
    if not pool:
        raise HTTPException(
            status_code=400,
            detail={"error": "invalid_difficulty", "message": f"No templates for {difficulty}"}
        )
    
    # Cycle mode logic
    t0 = time.time()
    pool_key = (request.session_id, request.skill_id, difficulty)  # type: ignore
    pool_size = len(pool)
    
    # If bag is full, clear it (start a new cycle) and emit cycle_reset
    current_seen_size = await cycle_bags.size(pool_key)
    if current_seen_size >= pool_size:
        await cycle_bags.clear(pool_key)
        # Emit cycle_reset event
        try:
            await log_event(
                "cycle_reset",
                session_id=request.session_id,
                skill_id=request.skill_id,
                difficulty=difficulty,
            )
        except Exception:
            pass  # fail-open
    
    # Get seen stems and pass to generate_item for efficient filtering
    seen_stems = await cycle_bags.get_seen_stems(pool_key)

    # Generate item with excluded stems (efficient - filters before selection)
    item = generate_item(
        skill_id=request.skill_id,
        difficulty=difficulty,
        seed=None,  # randomness within cycle mode
        excluded_stems=seen_stems if seen_stems else None,
        use_parameterized=request.use_parameterized,
    )
    stem = item.get("stem", "")

    # Mark this stem as seen
    await cycle_bags.mark_seen(pool_key, stem)
    latency_ms = float((time.time() - t0) * 1000.0)

    # Check if pool will be exhausted after this question
    new_seen_size = await cycle_bags.size(pool_key)
    templates_remaining = pool_size - new_seen_size
    pool_exhausted = (new_seen_size >= pool_size)

    # Log telemetry
    try:
        await log_event(
            "generate",
            session_id=request.session_id,
            mode="cycle",
            skill_id=item["skill_id"],
            difficulty=item["difficulty"],
            item_id=item["item_id"],
            stem=item["stem"],
            choice_ids=[c["id"] for c in item["choices"]],
            latency_ms=latency_ms,
            pool_exhausted=pool_exhausted,
            templates_remaining=templates_remaining,
        )
    except Exception:
        pass  # fail-open

    return GenerateItemResponse(
        **item,
        pool_exhausted=pool_exhausted,
        templates_remaining=templates_remaining
    )


# ============================================================================
# Telemetry Helper
# ============================================================================

def log_telemetry(event: str, **kwargs) -> None:
    """
    Log event to telemetry JSONL file (non-blocking, fail-open).
    
    Args:
        event: Event type (e.g., "cycle_generate", "graded")
        **kwargs: Additional fields to log
    """
    try:
        log_dir = Path(__file__).parent.parent / "var"
        log_dir.mkdir(exist_ok=True)
        
        log_entry = {
            "t": time.time(),
            "event": event,
            **kwargs
        }
        
        with open(log_dir / "events.jsonl", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception:
        # Fail open: don't crash the API if telemetry fails
        pass


@app.post("/grade", response_model=GradeResponse)
async def grade_endpoint(request: GradeRequest):
    """
    Grade a student's response to a question.
    
    See api/CONTRACTS.md for full specification.
    
    Args:
        request: GradeRequest with item dict and choice_id
    
    Returns:
        GradeResponse with correct flag, solution_choice_id, and explanation
    
    Raises:
        HTTPException 400: invalid_item, invalid_choice_id, missing_field
    """
    # Validate that required fields are present
    if "item" not in request.__dict__ or request.item is None:
        raise HTTPException(
            status_code=400,
            detail={"error": "missing_field", "message": "Missing required field: item"}
        )
    if "choice_id" not in request.__dict__ or request.choice_id is None:
        raise HTTPException(
            status_code=400,
            detail={"error": "missing_field", "message": "Missing required field: choice_id"}
        )
    
    try:
        t0 = time.time()
        result = grade_response(item=request.item, choice_id=request.choice_id)
        latency_ms = float((time.time() - t0) * 1000.0)
        
        # NEW: Update mastery if session_id and skill_id are provided
        session_id = request.session_id or "anon"
        skill_id = request.item.get("skill_id")
        
        if skill_id and progress_store:
            try:
                # Get current state snapshot
                current_state = await progress_store.get_session(session_id)
                
                # Update mastery using pure function
                updated_state = update_progress(
                    state=current_state,
                    skill_id=skill_id,
                    correct=bool(result["correct"]),
                    now=time.time(),
                    confidence=request.confidence,
                )
                
                # Persist updated skill state
                await progress_store.upsert_skill(
                    session_id, skill_id, updated_state[skill_id]
                )
            except Exception as e:
                # Fail-open: don't crash if mastery update fails
                pass
        
        # Log telemetry (async, fire-and-forget)
        try:
            asyncio.create_task(log_event(
                "grade",
                session_id=request.session_id,
                skill_id=request.item.get("skill_id"),
                difficulty=request.item.get("difficulty"),
                item_id=request.item.get("item_id"),
                choice_id=request.choice_id,
                correct=result["correct"],
                solution_choice_id=result["solution_choice_id"],
                latency_ms=latency_ms,
            ))
        except Exception:
            pass  # fail-open: don't crash if telemetry fails
        
        return GradeResponse(**result)
    except ValueError as e:
        error_msg = str(e)
        
        # Map engine errors to API errors
        if error_msg == "invalid_choice_id":
            raise HTTPException(
                status_code=400,
                detail={"error": "invalid_choice_id", "message": f"choice_id must be A-D, got: {request.choice_id}"}
            )
        elif error_msg.startswith("invalid_item"):
            # Extract error code if propagated: "invalid_item:<code>"
            error_code = error_msg.split(":")[1] if ":" in error_msg else "unknown"
            raise HTTPException(
                status_code=400,
                detail={"error": "invalid_item", "message": f"Item validation failed: {error_code}"}
            )
        else:
            # Unexpected error
            raise HTTPException(status_code=500, detail={"error": "internal_error", "message": str(e)})


# ============================================================================
# Health check (for sanity testing)
# ============================================================================

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/healthz")
async def healthz():
    """Kubernetes-compatible health check endpoint."""
    return {"status": "ok"}


@app.get("/skills/manifest")
async def skills_manifest() -> Dict[str, Dict[str, int]]:
    """
    Get pool sizes for all skills and difficulties.
    
    Useful for UI to dynamically set POOL_SIZE_HINT without hardcoding.
    
    Returns:
        {
            "quad.graph.vertex": {"easy": 2, "medium": 1, "hard": 1, "applied": 1},
            ...
        }
    """
    return {
        skill_id: {difficulty: len(templates) for difficulty, templates in skill_templates.items()}
        for skill_id, skill_templates in SKILL_TEMPLATES.items()
    }


# ============================================================================
# Mastery & Planner Endpoints (NEW)
# ============================================================================

@app.post("/progress/get")
async def get_progress(req: Dict[str, str]):
    """
    Retrieve mastery state for a session.
    
    Request: {"session_id": "..."}
    Response: {"session_id": "...", "skills": {"skill_id": {"p": 0.5, "attempts": 2, "streak": 1, "last_ts": 123.45}, ...}}
    """
    if not progress_store:
        raise HTTPException(status_code=503, detail="Progress store not available")
    
    session_id = req.get("session_id")
    if not session_id:
        raise HTTPException(status_code=400, detail="Missing session_id")
    
    sess = await progress_store.get_session(session_id)
    skills_data = {}
    for skill_id, mastery in sess.items():
        skills_data[skill_id] = {
            "p": mastery.p,
            "attempts": mastery.attempts,
            "streak": mastery.streak,
            "last_ts": mastery.last_ts,
        }
    
    return {
        "session_id": session_id,
        "skills": skills_data,
    }


@app.post("/planner/next")
async def planner_next(req: Dict[str, Any]):
    """
    Get recommended next difficulty for a skill based on mastery.
    
    Request: {"skill_id": "quad.graph.vertex", "session_id": "...", "p_override": null}
    Response: {"difficulty": "easy", "reason": "...", "p_used": 0.5}
    
    Priority for p value: p_override > session state > default (0.5)
    """
    skill_id = req.get("skill_id")
    if not skill_id:
        raise HTTPException(status_code=400, detail="Missing skill_id")
    
    # Determine p to use: override → session → default
    p_used = 0.5
    
    if req.get("p_override") is not None:
        try:
            p_used = float(req.get("p_override"))
        except (TypeError, ValueError):
            raise HTTPException(status_code=400, detail="Invalid p_override")
    elif req.get("session_id") and progress_store:
        sess = await progress_store.get_session(req.get("session_id"))
        if skill_id in sess:
            p_used = sess[skill_id].p
    
    # Get recommendation from planner
    difficulty, reason = plan_next_difficulty(p_used)
    
    return {
        "difficulty": difficulty,
        "reason": reason,
        "p_used": p_used,
    }


# ============================================================================
# Persistence Endpoint (Optional: read persisted progress)
# ============================================================================

@app.get("/progress")
async def get_all_progress(session_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Read persisted mastery state (debugging / admin endpoint).
    
    Query params:
      session_id (optional): if provided, return only this session's progress
    
    Returns:
      {"sessions": {session_id: {skill_id: {p, attempts, streak, last_ts}, ...}, ...}}
    
    If session_id is provided:
      {"sessions": {session_id: {skill_id: {...}, ...}}}
    
    Note: No authentication; use with caution in production.
    """
    if not progress_store:
        raise HTTPException(status_code=503, detail="Progress store not available")
    
    async with progress_store._lock:
        snap = progress_store.snapshot()
    
    if session_id:
        subset = snap.get("sessions", {}).get(session_id, {})
        return {"sessions": {session_id: subset}}
    
    return snap


# ============================================================================
# Telemetry Endpoints (Data Collection)
# ============================================================================

# Telemetry log file path
TELEMETRY_DIR = Path(__file__).parent.parent / "logs"
TELEMETRY_DIR.mkdir(exist_ok=True)


def get_telemetry_file() -> Path:
    """Get current telemetry file (rotates daily)"""
    today = datetime.now().strftime("%Y-%m-%d")
    return TELEMETRY_DIR / f"telemetry_{today}.jsonl"


@app.post("/telemetry/log", response_model=TelemetryResponse)
async def log_telemetry(event: TelemetryEvent):
    """
    Log a student interaction event for analysis and learning.

    Events are stored in JSONL format (one JSON object per line) for easy streaming analysis.
    Files rotate daily: logs/telemetry_YYYY-MM-DD.jsonl

    Example events:
    - question_presented: When a question is shown
    - question_answered: When student submits an answer
    - session_summary: When a practice session completes

    Returns:
      {"success": true, "message": "Event logged"}
    """
    try:
        telemetry_file = get_telemetry_file()

        # Append event as single JSON line
        with open(telemetry_file, 'a') as f:
            f.write(json.dumps(event.dict()) + '\n')

        return TelemetryResponse(
            success=True,
            message=f"Event logged to {telemetry_file.name}"
        )

    except Exception as e:
        # Log error but don't fail the request (fail-open for telemetry)
        print(f"Telemetry logging error: {e}", file=sys.stderr)
        return TelemetryResponse(
            success=False,
            message=f"Failed to log event: {str(e)}"
        )


@app.get("/telemetry/stats")
async def get_telemetry_stats(days: int = 1):
    """
    Get aggregated statistics from telemetry data.

    Query params:
      days: Number of recent days to include (default: 1)

    Returns aggregated metrics:
    - Total events by type
    - Accuracy by skill and difficulty
    - Most chosen distractors
    - Average time per question

    Note: This is a simple aggregation. For complex analysis, use the analysis scripts.
    """
    try:
        from collections import defaultdict
        from datetime import timedelta

        stats = {
            "total_events": 0,
            "events_by_type": defaultdict(int),
            "questions_answered": 0,
            "overall_accuracy": 0.0,
            "by_skill": {},
            "by_difficulty": {},
        }

        # Read telemetry files for last N days
        end_date = datetime.now()
        dates_to_check = [
            (end_date - timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range(days)
        ]

        total_correct = 0
        total_answered = 0

        for date_str in dates_to_check:
            telemetry_file = TELEMETRY_DIR / f"telemetry_{date_str}.jsonl"

            if not telemetry_file.exists():
                continue

            with open(telemetry_file, 'r') as f:
                for line in f:
                    try:
                        event = json.loads(line)
                        stats["total_events"] += 1
                        stats["events_by_type"][event.get("event_type", "unknown")] += 1

                        if event.get("event_type") == "question_answered":
                            stats["questions_answered"] += 1
                            total_answered += 1

                            if event.get("is_correct"):
                                total_correct += 1

                            # Track by skill
                            skill_id = event.get("skill_id")
                            if skill_id:
                                if skill_id not in stats["by_skill"]:
                                    stats["by_skill"][skill_id] = {
                                        "total": 0,
                                        "correct": 0,
                                        "accuracy": 0.0
                                    }
                                stats["by_skill"][skill_id]["total"] += 1
                                if event.get("is_correct"):
                                    stats["by_skill"][skill_id]["correct"] += 1

                            # Track by difficulty
                            difficulty = event.get("difficulty")
                            if difficulty:
                                if difficulty not in stats["by_difficulty"]:
                                    stats["by_difficulty"][difficulty] = {
                                        "total": 0,
                                        "correct": 0,
                                        "accuracy": 0.0
                                    }
                                stats["by_difficulty"][difficulty]["total"] += 1
                                if event.get("is_correct"):
                                    stats["by_difficulty"][difficulty]["correct"] += 1

                    except json.JSONDecodeError:
                        continue  # Skip malformed lines

        # Calculate accuracies
        if total_answered > 0:
            stats["overall_accuracy"] = total_correct / total_answered

        for skill_data in stats["by_skill"].values():
            if skill_data["total"] > 0:
                skill_data["accuracy"] = skill_data["correct"] / skill_data["total"]

        for diff_data in stats["by_difficulty"].values():
            if diff_data["total"] > 0:
                diff_data["accuracy"] = diff_data["correct"] / diff_data["total"]

        # Convert defaultdict to regular dict for JSON serialization
        stats["events_by_type"] = dict(stats["events_by_type"])

        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to compute stats: {str(e)}")


# ============================================================================
# Static Files (Web UI)
# ============================================================================

# Resolve web directory relative to project root
WEB_DIR = str(Path(__file__).parent.parent / "web")

# Mount static files at root with SPA support (html=True serves index.html for any route)
app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="web")
