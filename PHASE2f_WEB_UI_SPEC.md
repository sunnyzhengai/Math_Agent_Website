# PHASE2f_WEB_UI_SPEC.md

## Overview

Build a **single-page web UI** that calls the existing API to:

1. Generate a math item
2. Let the student choose A–D
3. Grade the answer and show feedback
4. Fetch next question

No frameworks. Plain HTML/CSS/JS.

## Scope (Phase 2f only)

* ✅ One page (no routing)
* ✅ Calls `POST /items/generate` and `POST /grade`
* ✅ Minimal UI state (loading, answered, next)
* ✅ Session tally (correct / attempted)
* 🚫 No auth, no persistence, no telemetry (that's Phase 2d)
* 🚫 No multiple skills selector (optional stub allowed)

---

## File Layout

```
web/
  index.html        # DOM structure only (no inline JS)
  styles.css        # tiny styling + state classes
  app.js            # fetch logic + state management
```

FastAPI must serve this directory at `/` (see "Server Mount" section).

---

## API (already implemented)

* `POST /items/generate`
  **Request**: `{"skill_id": "quad.graph.vertex", "difficulty": "easy", "seed": null}`
  **Response**: item dict (per engine contract)

* `POST /grade`
  **Request**: `{"item": <item dict>, "choice_id": "A"|"B"|"C"|"D"}`
  **Response**: `{"correct": bool, "solution_choice_id": str, "explanation": str}`

* **Errors**: HTTP 400 with JSON
  `{"error":"<code>", "message":"<human readable>"}`

---

## HTML (DOM Structure)

Create the following markup (IDs and data-attributes are **contractual**):

* Header:
  * `h1#title` → "Math Agent — Quadratics"
  * (Optional) Controls row:
    * `select#skill-select` (default value: `quad.graph.vertex`; disabled for now)
    * `select#difficulty-select` (default: `easy`; disabled for now)

* Question Area:
  * `div#stem` → question text goes here
  * `div#choices` → contains exactly 4 buttons:
    * `button.choice-btn#choice-A` with `data-choice="A"`
    * `button.choice-btn#choice-B` with `data-choice="B"`
    * `button.choice-btn#choice-C` with `data-choice="C"`
    * `button.choice-btn#choice-D` with `data-choice="D"`

* Feedback & Controls:
  * `div#feedback` → explanation + ✓/✗ styling
  * `button#next-btn` → "Next question"

* Footer:
  * `div#tally` → "Correct X of Y"
  * (Optional) `a#repo-link` → repo URL

**Notes**

* Buttons must exist in HTML; JS only fills their text and enables/disables.
* Add `aria-live="polite"` to `#feedback` for screen reader updates.

---

## CSS (Styling + States)

Create minimal, readable styles:

* Base:
  * System font, generous line-height
  * Max width ~720px; centered content
  * Buttons: large hit targets; consistent spacing

* States:
  * `.disabled` OR native `disabled` attribute dims buttons and prevents pointer events.
  * `#feedback.correct { border-left: 4px solid #3c9; }`
  * `#feedback.incorrect { border-left: 4px solid #e55; }`
  * `body.busy` may set `cursor: progress;` (optional)

* Accessibility:
  * Maintain color contrast ≥ 4.5:1
  * Focus styles on buttons (outline visible)

---

## JS (Fetch Logic + State Management)

### Module-level state

```js
let currentItem = null;     // latest generated item
let attempted = 0;          // session tally
let correct = 0;
let isBusy = false;         // blocks concurrent requests
const API_BASE = "";        // same origin; leave empty
```

### On DOMContentLoaded

1. Initialize references to all required elements (by id).
2. Attach click handlers to choice buttons and Next button.
3. Call `fetchGenerate()`.

### fetchGenerate()

* Guard: if `isBusy`, no-op.
* Set `isBusy = true`, disable choice buttons and next button, add `body.busy`.
* POST `/items/generate` with:
  ```js
  { skill_id: "quad.graph.vertex", difficulty: "easy" } // seed omitted
  ```
* On **200**:
  * Save `currentItem`.
  * Set `#stem` innerText to `item.stem`.
  * For each button A–D, set text from `item.choices[i].text`, enable it.
  * Clear `#feedback` classes/text, keep Next disabled.
* On **400** (error envelope):
  * Show `body.message` in `#feedback` (no class), keep Next enabled for retry.
* On **network error**:
  * Show "Couldn't reach server. Please try again." in `#feedback`, keep Next enabled.
* Finally: `isBusy = false`, remove `body.busy`.

### onChoiceClick(choiceId)

* Guard: if `isBusy` or `!currentItem`, no-op.
* Disable all choices, set `isBusy = true`, add `body.busy`.
* POST `/grade` with `{ item: currentItem, choice_id: choiceId }`.
* On **200**:
  * Update tally: `attempted += 1`, `if (res.correct) correct += 1`.
  * Render result into `#feedback`:
    * Add class `correct` or `incorrect`
    * Text = `res.explanation`
  * Enable Next; leave choices disabled.
  * Update `#tally` to `Correct ${correct} of ${attempted}`.
* On **400**:
  * Show error `body.message` in `#feedback` (no class), enable Next.
* On **network error**:
  * Show network message in `#feedback`, enable Next.
* Finally: `isBusy = false`, remove `body.busy`.

### onNext()

* Disable Next; call `fetchGenerate()`.

### Utilities

* `setButtonsEnabled(enabled: boolean)` → add/remove `disabled`.
* `setFeedback(text: string, cls?: "correct"|"incorrect"|null)` → sets text + class list.

**Do not** store anything in localStorage in Phase 2f.

---

## Server Mount (FastAPI)

Add a single line to serve the UI:

```python
# api/server.py

from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory="web", html=True), name="web")
```

* Keep all existing API routes working.
* Same origin (no CORS needed).

---

## Browser Smoke Test (Manual)

* Start API server.
* Visit `/`:
  * [ ] A question loads automatically.
  * [ ] Four choices show text.
  * [ ] Clicking a choice disables choices, shows ✓/✗ + explanation.
  * [ ] "Next question" fetches a new question.
  * [ ] Tally updates: "Correct X of Y".
  * [ ] No console errors.

**Error cases**

* If the server is stopped mid-session:
  * [ ] UI shows "Couldn't reach server. Please try again."
  * [ ] Next remains enabled so the user can retry after restarting.

---

## Definition of Done (DoD)

* [ ] `web/index.html`, `web/styles.css`, `web/app.js` created as specified.
* [ ] Server mounts `web/` at `/`.
* [ ] Manual smoke test passes on Chrome/Safari/Edge.
* [ ] No inline scripts in HTML; all logic in `app.js`.
* [ ] Buttons disabled during in-flight requests.
* [ ] Error envelope messages surfaced to the user.
* [ ] No new failing tests (existing suite still green).

---

## Future Hooks (don't implement now)

* Telemetry (Phase 2d): call a `logEvent(...)` inside `/items/generate` and `/grade` handlers.
* Skill picker: enable `#skill-select` and `#difficulty-select` once additional skills land.

---

## Implementation Order

1. HTML (DOM structure)
2. CSS (styling + states)
3. JS (fetch logic + state)
4. Server (mount static files)
5. Browser smoke test

**That's it—hand this spec to Cursor and let it build the UI.**
