# Phase 2f — Minimal Web UI (Generate → Grade)

## File Layout (New)

```
web/
  index.html        # single page UI
  app.js            # fetch logic + simple state
  styles.css        # tiny styling
```

> We'll serve `/` from `web/index.html` via FastAPI (mount StaticFiles), but you can also open it locally for quick smoke tests if your API runs at `http://localhost:8000`.

---

## API Recap (Already Implemented)

* `POST /items/generate` → returns the item dict
* `POST /grade` → returns `{correct, solution_choice_id, explanation}`
* Error envelope: `{"error":"<code>","message":"<text>"}` with HTTP 400

---

## index.html — Required DOM Structure

* Heading + skill controls
* Question stem container
* Four answer buttons A–D (wired by `data-choice` attributes)
* Feedback area (✓/✗ + explanation)
* Next question button
* Small session tally "Correct x of y"

### DOM IDs (so app.js can query predictably)

* `#skill-select` (optional for now; default value set to `quad.graph.vertex`)
* `#difficulty-select` (optional; default `easy`)
* `#stem`
* `#choices` (container div; app.js will render four buttons with ids `choice-A`..`choice-D`)
* `#feedback`
* `#next-btn`
* `#tally`

> Keep it dead simple: static four buttons labeled A–D; app.js fills their text and enables/disables them.

---

## app.js — Behavior Spec

### Local State

```js
let currentItem = null;           // full item from /items/generate
let attempted = 0;                // session tally
let correct = 0;
let isBusy = false;
const API_BASE = "";              // same origin; if dev proxy needed you can change later
```

### On Page Load

1. Disable all choice buttons + Next button.
2. Call `fetchGenerate()` with:
   ```js
   { skill_id: "quad.graph.vertex", difficulty: "easy" } // no seed for true randomness
   ```
3. Render:
   * `#stem` = `item.stem`
   * Buttons `#choice-A`..`#choice-D` = `item.choices[i].text`
   * Clear `#feedback`
   * Enable A–D buttons; disable Next

### On Clicking a Choice Button

1. If `isBusy` or `!currentItem`, ignore.
2. Disable all choice buttons; set `isBusy = true`.
3. POST `/grade` with `{ item: currentItem, choice_id: "A"|"B"|"C"|"D" }`.
4. On success:
   * Show ✅/❌ + explanation in `#feedback`
   * Increment `attempted += 1`; if `correct`, increment `correct += 1`
   * Update `#tally` to "Correct X of Y"
   * Enable `#next-btn`; keep A–D disabled
5. On 400:
   * Show `body.message` in `#feedback`
6. Always: `isBusy = false`.

### On Next Button

1. Disable Next; call `fetchGenerate()` again.
2. Same render routine as "On page load".

### Error Handling Baseline

* If network fails → show "Couldn't reach server. Please try again." in `#feedback`; keep Next enabled so you can retry.
* Any 400 from backend shows the message returned.

### Visual States (CSS Classes)

* `.busy` on body while fetching (optional)
* `.correct` / `.incorrect` on `#feedback`
* `.disabled` on buttons (or just `disabled` attribute)

---

## styles.css — Minimal Rules

* Basic font and spacing
* `.correct { border-left: 4px solid #3c9; }`
* `.incorrect { border-left: 4px solid #e55; }`
* Disabled buttons with reduced opacity + no pointer

---

## FastAPI Static Serving (Server Note)

* Mount static at `/`:
  ```python
  app.mount("/", StaticFiles(directory="web", html=True), name="web")
  ```
* CORS: if you open HTML directly from file system, set `--` skip CORS; otherwise if hosted under same origin, no CORS needed. (If you *do* serve UI elsewhere, add CORSMiddleware allowlist.)

---

## "Done When" Checklist (Acceptance)

### Behavior

- [ ] On load, a question appears with 4 choices.
- [ ] Clicking a choice disables all choices, shows ✅/❌ + explanation.
- [ ] "Next question" fetches a new item and resets the UI.
- [ ] Session tally increments correctly (Correct X of Y).
- [ ] No runtime errors in the browser console.

### API Integration

- [ ] `/items/generate` called without seed; `/grade` called with full `item`.
- [ ] Backend error envelope renders human message in `#feedback`.

### Resilience & UX

- [ ] Buttons are disabled during in-flight requests.
- [ ] Network failure message is user-friendly; "Next question" lets user retry.

### Code Quality

- [ ] No inline business logic in HTML; all logic lives in `app.js`.
- [ ] No global mutation beyond the defined local state.
- [ ] All ids/classes match this spec.

---

## Optional (Nice-to-Have, Tiny)

* A `<select id="skill-select">` with just `quad.graph.vertex` for now (non-functional until you wire multiple skills).
* A "Retry" link shown only on fetch error that re-calls `/items/generate`.
* A footer link to your repo.

---

## Phase 2d Integration Hook Points (Future)

When Phase 2d (telemetry) is implemented, you'll add these calls in `app.js`:

* After successful `/items/generate` → log event `item_generated`
* After successful `/grade` → log event `graded`

**No changes to this UI spec;** telemetry will be injected as a background concern.

---

## Implementation Order (for Cursor)

1. **index.html** — Create DOM structure with all required ids
2. **styles.css** — Add basic styling and state classes
3. **app.js** — Implement state machine and fetch logic
4. **server.py** — Add static file serving (one line: `app.mount(...)`)
5. **Test** — Manual smoke test in browser

---

*Ready to code? Hand this spec to Cursor and ask for Phase 2f implementation.*
