# Math Agent (Web Rebuild)

Clean, test-driven rebuild of the Math Agent website.

## Development

### One-command pipeline

```bash
make ci        # Run all tests and linting
make test      # Run tests only
make serve     # Run FastAPI server (localhost:8000)
```

## Project Status

### Phase 1: Item Generation & Validation ✅ **COMPLETE**

- ✅ `engine.templates.generate_item()` — Deterministic math question generation
- ✅ `engine.validators.validate_item()` — Structural validation with Unicode normalization
- ✅ Golden snapshot test (`seed=42`)

**Test Results:**
```
8 generator tests ✅
7 validator tests ✅
1 snapshot test ✅
Total: 16/16 passing
```

### Phase 2a: Grader ✅ **COMPLETE**

- ✅ `engine.grader.grade_response()` — Deterministic grading with pedagogical feedback
- ✅ Type guards on input (rejects non-string choice_id, None, int, etc.)
- ✅ Error code propagation for debugging
- ✅ Purity verified (no mutation of input)

**Test Results:**
```
10 grader tests ✅ (ChatGPT 6-scenario coverage)
- Happy path: correct/incorrect answers
- Invalid choice IDs: out-of-range, lowercase, edge cases
- Malformed items: broken choices, missing fields
- Determinism & purity: identical outputs, input unchanged
- Validator consistency: generated items pass grading

Total Phase 1+2a: 26/26 passing
```

### Phase 2b: API Contracts ✅ **COMPLETE**

- ✅ `api/CONTRACTS.md` — JSON request/response schemas
  - `POST /items/generate` (skill_id, difficulty?, seed?) → full item
  - `POST /grade` (item, choice_id) → correct, solution_choice_id, explanation
- ✅ Error codes defined (invalid_skill, invalid_difficulty, invalid_seed, invalid_choice_id, invalid_item, missing_field)
- ✅ Determinism & JSON serialization rules locked

### Phase 2c: FastAPI Implementation ✅ **COMPLETE**

- ✅ `api/server.py` — Fully functional FastAPI endpoints
  - `/items/generate` — Generates items with proper error handling
  - `/grade` — Grades responses with validation
  - `/health` — Health check endpoint
- ✅ Error mapping from engine to HTTP 400 responses
- ✅ Error code propagation for debugging logs
- ✅ 14 endpoint tests + 6 schema tests = 20/20 ✅

**Test Results:**
```
14 endpoint tests ✅ (6 generate + 5 grade + 3 round-trip)
- Happy path: success, defaults, correct/incorrect grading
- Error handling: validation, malformed items, missing fields
- Determinism: identical responses with same seed
- Round-trip: end-to-end workflow testing

6 schema tests ✅ (engine signature validation)

Total Phase 2c: 20/20 passing
```

**TOTAL: 46/46 tests passing** ✅

### Phase 2d-2f: Pending

- 🔜 **2d** Telemetry: JSONL event logging
- 🔜 **2e** Content: Expand quadratics skill set
- 🔜 **2f** Web UI: Minimal generate + grade UI

## Contracts & Docs

- `engine/CONTRACTS.md` — Core engine API (generate, validate, grade)
- `api/CONTRACTS.md` — HTTP API (endpoints, request/response schemas)
- `CONTRIBUTING.md` — Development workflow, testing discipline, golden snapshot policy

## API Usage

### Generate a question

```bash
curl -X POST http://localhost:8000/items/generate \
  -H "Content-Type: application/json" \
  -d '{"skill_id": "quad.graph.vertex", "difficulty": "easy", "seed": 42}'
```

### Grade a response

```bash
curl -X POST http://localhost:8000/grade \
  -H "Content-Type: application/json" \
  -d '{"item": {...}, "choice_id": "A"}'
```

### Health check

```bash
curl http://localhost:8000/health
```

## Phase-based Plan

Guardrails → **1) Domain Data** ✅ → **2) Item Engine** ✅ → **3) API** ✅ → 4) Mastery & Planner → 5) State & Neo4j → 6) Web API → 7) Frontend → 8) Obs/Safety → 9) Deploy → 10) E2E

## Development Environment

- **Python 3.11.x** (pytest, pylint, mypy, black, fastapi, uvicorn, pydantic)
- **Node 20.x** (planned for frontend)
- All dependencies pinned in `requirements.txt`

## Determinism

- ✅ Seed-based RNG (local `random.Random(seed)`, no global state)
- ✅ Deterministic choice shuffling
- ✅ Injectable time (planned for Phase 3)
- ✅ Pure functions (no side effects, input unchanged)
- ✅ Error code propagation (for debugging and testing)

## Testing Discipline

- **TDD first:** Tests → stubs → implementation
- **Single truth:** `make ci` must be green locally before pushing
- **Fix one failing test:** No fix-forward from red states
- **Golden snapshots:** Locked against accidental drift; only update on explicit request
- **46/46 tests:** Phase 1 + 2a generator + grader + Phase 2c API implementation
