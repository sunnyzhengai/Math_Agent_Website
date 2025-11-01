# Phase 2 Execution Plan (Revised Order)

**Priority:** 2f → 2d → 2e (UI first for immediate feedback, telemetry second for data, content third)

---

## Phase 2f — Minimal Web UI (generate → grade)

**Goal:** One-page app that calls your two endpoints and shows ✓/✗ with the explanation.

### Scope (MVP)

- [ ] Page layout: stem + four A–D buttons + "Next question"
- [ ] On load: POST `/items/generate` with `skill_id="quad.graph.vertex"`, `difficulty="easy"`, `seed` omitted
- [ ] On click choice: POST `/grade` with `{ item, choice_id }`; render ✅/❌ and explanation; disable buttons
- [ ] "Next question": fetch a fresh item; reset UI

### UX Niceties (still MVP)

- [ ] Disable buttons during network calls; show tiny spinner text ("scoring…")
- [ ] Keep and show session-only tally: `correct / attempted`

### API

- [ ] API stays the same (no changes to `/items/generate` or `/grade`)
- [ ] Serve static HTML from `web/` directory

### Testing

- [ ] Use FastAPI TestClient to hit `/` static route (returns 200)
- [ ] API tests already cover backend; Playwright spec optional for now
- [ ] Manual smoke test: load page → answer → see result → click Next → repeat

### Acceptance Criteria

- [ ] Manual smoke test passes (no console errors, no CORS errors)
- [ ] Buttons disabled during network calls
- [ ] Tally updates correctly after each response
- [ ] "Next question" fetches fresh item and resets UI

---

## Phase 2d — Telemetry (JSONL event capture)

**Goal:** Append one line per important action to a JSONL file for later personalization/analytics.

### Setup

- [ ] Create `var/` directory (in .gitignore)
- [ ] File: `var/events.jsonl` (create folder if missing)

### Event Schema

```json
{"ts": 1730448000.123, "user_id": "anon", "event": "item_generated", "payload": {"skill_id":"quad.graph.vertex","difficulty":"easy","seed":null,"item_id":"..."}}
{"ts": 1730448002.004, "user_id": "anon", "event": "graded", "payload": {"item_id":"...","choice_id":"A","correct":true}}
```

### Implementation

- [ ] Create `telemetry/` module with `logger` class
- [ ] Log in FastAPI handlers (after success):
  - [ ] `/items/generate` → `item_generated` event
  - [ ] `/grade` → `graded` event
- [ ] Fields to capture:
  - [ ] `ts`: Unix timestamp (injectable for testing)
  - [ ] `user_id`: "anon" for now
  - [ ] `event`: event type (item_generated, graded)
  - [ ] `payload`: event-specific data

### Testing

- [ ] Monkeypatch logger to write to temp path
- [ ] Assert exactly one JSON object per request
- [ ] Verify lines are valid JSON and match schema
- [ ] Ensure telemetry never crashes API (fail-open: if file write fails, still return 200)
- [ ] Add test: after 3 interactions, file contains 3+ lines

### Acceptance Criteria

- [ ] After 3 interactions, `var/events.jsonl` contains 3+ valid JSON lines
- [ ] Each line is parseable JSON with correct keys
- [ ] API remains 100% functional if telemetry fails (graceful degradation)
- [ ] All tests pass (46 + telemetry tests)

---

## Phase 2e — Content Expansion (Quadratics +3 skills)

**Goal:** Add at least 4 total quadratics skills with 1–2 templates each.

### New Skills to Add

- [ ] `quad.graph.opening` — Given `y = a(x-h)^2 + k`, ask "opens up or down?" (a>0 up, a<0 down)
- [ ] `quad.graph.axis_of_symmetry` — Identify `x = h` from vertex form or after completing the square
- [ ] `quad.std.vertex_from_standard` — From `ax^2+bx+c`, find vertex (complete-the-square lite)
- [ ] `quad.context.max_min_from_vertex` — Word problem: identify maximum/minimum value or its x-coordinate

### For Each Skill

- [ ] Add 1–2 templates per difficulty (start with `easy` only to ship fast)
- [ ] Keep **choices unique** and exactly 4; pass current validator
- [ ] Add questions to `engine/templates.py` SKILL_TEMPLATES
- [ ] Verify all existing tests still pass

### Golden Snapshots

- [ ] After wording stabilizes, add **one golden per skill** (`seed=42`)
- [ ] Do NOT add goldens before wording is final
- [ ] Run `make update-goldens` after finalizing all questions

### Testing

- [ ] Reuse existing generator tests (they're generic for all skills)
- [ ] Add one golden snapshot per new skill (4 new goldens total)
- [ ] Run full test suite: `make test` (should see 50+ tests)

### Manual Testing

- [ ] Load UI, manually change `skill_id` in code/URL to each new skill
- [ ] Verify each skill generates sensible questions
- [ ] Verify grading works for each skill

### Acceptance Criteria

- [ ] 4 total skills in `SKILL_TEMPLATES`
- [ ] All tests green (50+ tests passing)
- [ ] Manual smoke test: each skill generates and grades correctly
- [ ] One golden snapshot per skill (4 new golden files)

---

## Summary: Why This Order Works

1. **UI first** → Julia has something to click today; immediate feedback on backend
2. **Telemetry second** → Capture usage data from day one without touching UX again
3. **Content third** → Easy to add more skills once the UX/telemetry feel solid

---

## Integration Checklist (All Phases)

- [ ] Phase 2f: UI loads without errors, endpoints work
- [ ] Phase 2d: Events logged to `var/events.jsonl` after each interaction
- [ ] Phase 2e: UI works with new skills; telemetry captures all events

---

**Ready to hand to Cursor?** Paste this entire document, then provide code for each phase.
