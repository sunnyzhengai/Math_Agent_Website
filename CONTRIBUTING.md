# Contributing

Thanks for improving **Math Agent**! This guide explains how to work safely with tests, goldens, and API schemas.

## 0) Quick Start

```bash
# one-time
python3 -m venv .venv && source .venv/bin/activate
make install
python tools/preflight.py

# day-to-day
make ci       # lint + tests
make test     # run unit tests
make format   # black
make lint     # pylint + mypy (non-blocking)
```

---

## 1) Development Workflow (TDD first)

1. **Update the spec** (`engine/CONTRACTS.md` or `api/CONTRACTS.md`) — smallest change possible.

2. **Write failing tests**:
   * Engine tests in `tests/item/…`
   * API schema tests in `tests/api/test_schemas.py`
   * HTTP endpoint tests in `tests/api/test_endpoints.py`

3. **Implement** the smallest change to make tests pass.

4. **Run CI locally**: `make ci`

5. **Commit**: use clear, scoped messages (see below).

---

## 2) Tests

* **Unit tests (engine):** shape, determinism, and validation only.
* **API tests:** FastAPI endpoints; assert status codes + error envelopes.
* **No external I/O** in unit tests (no network, no real files).
* **Determinism:** when seeding is involved, assert deep equality.

```bash
make test
pytest tests/ -q
```

---

## 3) Golden Snapshots

Golden files lock deterministic outputs so wording/ordering doesn't silently drift.

* Files live in: `tests/goldens/`
* Example: `golden_item_quad_graph_vertex_easy_42.json`
* **Rule:** update goldens *only* when the change is intentional and documented.

### Update a golden (intentional changes only)

```bash
make update-goldens

# or manually regenerate the specific file, then:
git add tests/goldens/*.json
git commit -m "update(goldens): quad.vertex easy seed=42 snapshot matches new template"
```

> If a test fails because of a golden mismatch, first ask:
> **Did the spec change?** If not, fix the generator instead of updating the golden.

---

## 4) API Schema Changes (Server & Engine)

* **Contract-first:** edit `api/CONTRACTS.md` (request/response examples, error codes).
* Update **engine schema tests** (`tests/api/test_schemas.py`) and **endpoint tests**.
* Only then update server code (`api/server.py`).

**Error envelope** (HTTP 400):

```json
{"error": "<code>", "message": "<human readable>"}
```

Allowed codes include (subset):
`invalid_skill`, `invalid_difficulty`, `invalid_seed`, `invalid_choice_id`, `invalid_item`, `missing_field`.

---

## 5) Commit Messages

Use conventional style:

```
feat(engine): add grader with explanation text
fix(validator): NFKC normalize choice text to prevent dupes
test(api): add schema test for /items/generate defaults
docs(contracts): clarify difficulty case-sensitivity
chore(ci): add golden update make target
```

Small, focused commits are easier to review and revert.

---

## 6) When to Regenerate Goldens

Regenerate a golden **only** when:

* You intentionally change **wording**, **choice order**, or **solution mapping** for the seeded case.
* You added/remapped a template where the deterministic output (with the same seed) is expected to change.

**Do NOT** regenerate goldens to "make tests pass" if the spec didn't change.

---

## 7) Versioning & Compatibility (lightweight)

* **Patch:** bugfixes, no spec changes (`x.y.+1`)
* **Minor:** new skills/templates or non-breaking fields (`x.+1.0`)
* **Major:** breaking contract changes (update `CONTRACTS.md` prominently)

---

## 8) PR Checklist

* [ ] Spec updated (`CONTRACTS.md`) if behavior changed
* [ ] New/updated tests **fail first**, then pass
* [ ] Goldens updated **only if intentional**
* [ ] `make ci` passes locally
* [ ] Commit messages are scoped and clear

---

## 9) Troubleshooting

* **Duplicate answers surfaced** → check validator's **NFKC/strip/lower** normalization and generator choice pool.
* **Nondeterministic tests** → ensure seeded calls use local `random.Random(seed)` and no global RNG.
* **API 400s** → return the standard error envelope (`error`, `message`) and map engine `ValueError` messages accordingly.

---

*Thank you for keeping the project stable and test-driven. Small, well-tested steps win.*
