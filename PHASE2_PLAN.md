# Phase 2 Roadmap: From Engine to API to Web

## Overview

Build incrementally: **engine → contracts → API → telemetry → content → UI**.

Each step is independently testable and TDD'd.

---

## 2a: Grader (Pure Function)

**Goal:** Grade student responses deterministically.

**Contract:** `engine.grader.grade_response(item, choice_id) -> dict`

**Tests:** 8 (correct, incorrect, validation, determinism, generated items)

**Status:** ⏳ Test stubs ready (`tests/item/test_grader.py`)

---

## 2b: API Contracts

**Goal:** Lock JSON request/response shapes before writing server.

**Endpoints:**
- `POST /items/generate` → full item dict
- `POST /grade` → {correct, solution_choice_id, explanation}

**Tests:** Schema validation + round-trip tests

**Location:** `api/CONTRACTS.md` + `tests/schemas/`

---

## 2c: FastAPI Implementation

**Goal:** Thin server layer that calls engine functions.

**Tests:**
- `TestClient` for `/items/generate` and `/grade`
- Happy path + error cases
- Determinism with seeds

**Location:** `api/server.py` + `tests/api/test_endpoints.py`

---

## 2d: Telemetry (JSONL Logging)

**Goal:** Simple event logging for analytics.

**Event shape:** `{"ts": ..., "user_id": ..., "event": ..., "payload": ...}`

**Storage:** `var/events.jsonl`

**Tests:** File writes verified; no PII

---

## 2e: Content Expansion

**Goal:** Add 4+ quadratics skills with multiple items each.

**Skills to add:**
- `quad.graph.opening` (opens up/down)
- `quad.graph.axis_of_symmetry`
- `quad.algebra.vertex_from_standard`
- `quad.roots.from_vertex_and_point`

**Golden:** Add 1 golden snapshot per skill once stable

---

## 2f: Web UI

**Goal:** Minimal page: generate → render → grade → show result.

**Tech:** HTML + fetch() or React (minimal)

**Tests:** Manual smoke + Playwright (optional later)

---

## Acceptance Checklist

- [ ] 2a: Grader tests all pass
- [ ] 2b: API contracts documented + schema tests green
- [ ] 2c: FastAPI endpoints tested (happy + error paths)
- [ ] 2d: Telemetry logged + file writes verified
- [ ] 2e: Content expanded (4+ skills)
- [ ] 2f: UI loads, generates, grades, displays result

---

## Why This Order

1. **Engine first** (grader) — pure logic, no infrastructure
2. **Contracts second** — lock shapes before implementation
3. **API third** — thin layer calling engine
4. **Telemetry fourth** — passive, non-blocking
5. **Content fifth** — quality over breadth
6. **UI last** — only after API is solid

Each step unblocks the next without surprises.
