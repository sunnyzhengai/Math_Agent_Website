# Contributing Rules

- **Single truth:** `make ci` must be green locally before pushing.
- **Fix the FIRST failing test only.** No "fix-forward" from red states.
- **Do NOT change public contracts** (see `engine/CONTRACTS.md`) unless a step explicitly says so.
- **Do NOT edit golden snapshots** unless a PR explicitly requests "update goldens".

## Workflow

1. `git checkout -b feature/<thing>`
2. `make ci`
3. If red: run the single failing test, apply a minimal patch (<200 LOC, ≤2 files), re-run.
4. If still red: revert to last green, rethink scope.

## Golden Snapshot Files

Snapshot tests (`test_*_snapshot.py`) guard against accidental drift in deterministic outputs.

### Viewing Current Baselines

Golden snapshots are stored in `tests/goldens/` as JSON files:
- `golden_item_quad_graph_vertex_easy_42.json` — Phase-1 baseline for seed=42

### Updating Goldens (Rare)

Only update goldens when you **intentionally** change question content or structure:

```bash
# Review the changes first
git diff tests/goldens/

# Then regenerate (with reviewer approval)
make update-goldens

# Verify tests pass
make test
```

**Rule:** Snapshot updates must be:
1. Reviewers explicitly request "update goldens"
2. Committed separately with message: `refactor: Update golden snapshots for [reason]`
3. Never auto-generated or bundled with logic changes

## Environment

- Python 3.11.x, Node 20.x
- Exact deps pinned in `requirements.txt` and `pyproject.toml`

## Phases

Guardrails → 1) Domain Data → 2) Item Engine → 3) Mastery & Planner → 4) API → 5) State & Neo4j → 6) Web API → 7) Frontend → 8) Obs/Safety → 9) Deploy → 10) E2E

## Determinism

Python 3.11.x, Node 20 LTS

RNG-seeded generators; time is injectable (now)
