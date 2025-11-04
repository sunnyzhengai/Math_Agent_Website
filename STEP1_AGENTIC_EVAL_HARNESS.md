# Step 1: Agent Eval Harness — Complete Implementation

**Branch:** `phase1-data-flywheel`  
**Commit:** `ec76a60` Step 1: Improved agent eval harness with robust error handling  
**Date:** 2025-11-04

---

## Overview

A **production-grade evaluation harness** for agent experimentation. This is a deterministic baseline that always picks the correct answer (100% accuracy upper bound), serving as:

1. **Regression guard** — Catches engine/validator regressions
2. **Upper bound** — Baseline for agent strategy comparison
3. **Measurement framework** — Latency, stem diversity, error categorization
4. **Extension point** — Ready for agent strategy variants (random, heuristic, etc.)

**Key Improvements over ChatGPT's proposal:**
- ✅ Flexible CLI arguments (paths, thresholds)
- ✅ Comprehensive error categorization (generate_error, grade_error, incorrect)
- ✅ Better test design (no brittle monkeypatching, explicit path passing)
- ✅ Production error handling throughout
- ✅ Configurable accuracy threshold
- ✅ Detailed latency tracking

---

## File Structure

```
agentic/
  __init__.py                           Package marker
  evals/
    __init__.py                         Subpackage marker
    seed_math.jsonl                     Deterministic seed set (6 cases)
    run_eval.py                         Main harness runner (production-grade)
    test_eval_harness.py                9 contract tests
    report.jsonl                        Latest eval report (auto-generated)
```

---

## Core Components

### 1. Seed Set (`seed_math.jsonl`)

6 deterministic test cases covering 4 skills and multiple difficulties:

```jsonl
{"id":"vtx-1","skill_id":"quad.graph.vertex","difficulty":"easy","seed":42}
{"id":"vtx-2","skill_id":"quad.graph.vertex","difficulty":"medium","seed":43}
{"id":"std-1","skill_id":"quad.standard.vertex","difficulty":"easy","seed":11}
{"id":"roots-1","skill_id":"quad.roots.factored","difficulty":"medium","seed":12}
{"id":"fact-1","skill_id":"quad.solve.by_factoring","difficulty":"easy","seed":21}
{"id":"form-1","skill_id":"quad.solve.by_formula","difficulty":"easy","seed":31}
```

**Why deterministic?** Allows comparing agent strategies across runs without variance.

---

### 2. Harness Runner (`run_eval.py`)

**Main functions:**

#### `load_jsonl(p: Path) -> List[Dict]`
- Loads JSONL files
- Skips comments (`# ...`) and empty lines
- Robust error handling

#### `run_case(case: Dict) -> Tuple[bool, Dict]`
- Generates item deterministically
- Grades with correct answer (baseline)
- Returns: `(ok: bool, row: dict)` with schema:
  ```python
  {
      "id": str,
      "skill_id": str,
      "difficulty": str,
      "seed": int,
      "status": "ok" | "generate_error" | "grade_error" | "incorrect",
      "ok": bool,
      "gen_ms": float,              # milliseconds
      "grade_ms": float,            # milliseconds
      "stem_hash": str,             # SHA1[:10]
      "error": Optional[str],
  }
  ```

#### `main(seed_path, report_path, min_accuracy, verbose) -> int`
- Orchestrates eval run
- Writes JSONL report
- Returns 0 if accuracy ≥ threshold, else 1
- Supports command-line arguments:
  ```bash
  python3 -m agentic.evals.run_eval \
    --seed-path agentic/evals/seed_math.jsonl \
    --report-path agentic/evals/report.jsonl \
    --min-accuracy 1.0 \
    -v
  ```

**Output example:**
```
[eval] 6/6 passed · accuracy=100.00%
[eval] report -> agentic/evals/report.jsonl
  vtx-1    | quad.graph.vertex         | easy     | ok
  vtx-2    | quad.graph.vertex         | medium   | ok
  ...
```

---

### 3. Report Schema

JSONL format, one JSON object per line:

```json
{
  "id": "vtx-1",
  "skill_id": "quad.graph.vertex",
  "difficulty": "easy",
  "seed": 42,
  "status": "ok",
  "ok": true,
  "gen_ms": 0.02,
  "grade_ms": 0.05,
  "stem_hash": "ce7c7133df",
  "error": null
}
```

**Fields:**
- `status`: Outcome category
  - `"ok"` — Success
  - `"generate_error"` — Item generation failed
  - `"grade_error"` — Grading failed (validator)
  - `"incorrect"` — Baseline picked wrong answer (should never happen)
- `gen_ms`, `grade_ms` — Per-step latency
- `stem_hash` — Reproducibility tracking

---

### 4. Tests (`test_eval_harness.py`)

**9 comprehensive tests:**

| Test | Purpose |
|------|---------|
| `test_seed_set_exists` | File exists and readable |
| `test_seed_set_loads` | Required fields present |
| `test_seed_set_diversity` | ≥3 skills, ≥2 difficulties |
| `test_run_case_returns_well_formed_row` | Row schema validation |
| `test_run_case_baseline_100_percent` | **Regression guard**: baseline is always correct |
| `test_main_with_temp_files` | Integration: main() produces valid report |
| `test_main_respects_min_accuracy_threshold` | Threshold logic works |
| `test_main_handles_missing_seed_file` | Graceful error handling |
| `test_load_jsonl_skips_comments_and_empty_lines` | JSONL parsing robustness |

**All 9 tests pass ✅**

---

## Makefile Targets

```bash
make eval              # Run baseline (verbose mode)
make eval-test        # Run contract tests only
make eval-ci          # Run both tests + harness (CI gate)
```

Example:
```bash
$ make eval-ci
🧪 Running eval harness contract tests...
====== 9 passed in 0.02s ======
🤖 Running agent eval harness (baseline)...
[eval] 6/6 passed · accuracy=100.00%
✅ Agent eval CI passed!
```

---

## Test Results

```
Eval tests:           9 passed ✅
Baseline accuracy:    100.00% ✅
Existing tests:       97 passed, 1 skipped ✅ (no regressions)
Total latency:        ~0.4ms per case ⚡
```

---

## Key Design Decisions

### 1. Deterministic Seeds
- Enables reproducible agent comparison
- Catches non-deterministic bugs
- Seed values intentionally scattered (42, 43, 11, 12, 21, 31) to avoid clustering

### 2. Status Categorization
- `generate_error` — Engine bug (skill missing, invalid seed, etc.)
- `grade_error` — Validator bug (item failed post-generation validation)
- `incorrect` — Agent logic bug (baseline only; impossible in prod)
- This allows targeting fixes at the right layer

### 3. Flexible Paths & Thresholds
- CLI arguments make testing easy (tmpdir, custom thresholds)
- Default 100% threshold for baseline regression guard
- Can be lowered for agent experiments (e.g., `--min-accuracy 0.5`)

### 4. Side-car Under `agentic/`
- Separate from core eval framework (`tests/evals/`)
- `agentic/` = agent experimentation layer
- `tests/evals/` = core eval infrastructure
- Both feed data to same telemetry pipeline

---

## Next Steps (Step 2)

When ready, add **agent strategy variants**:

```python
# agentic/agents/strategies.py
def random_agent(item) -> str:
    """Randomly pick a choice."""
    return random.choice(["A", "B", "C", "D"])

def majority_label_agent(item) -> str:
    """Heuristic: pick most common word in choices."""
    # Simple baseline for comparison
    ...

def rule_based_agent(item) -> str:
    """Simple pattern matching on stem."""
    # E.g., if "vertex" in stem, try to extract coordinates
    ...
```

Then compare all strategies under the same harness:

```bash
$ make eval-strategies
[eval-baseline]  6/6 passed · accuracy=100.00%
[eval-random]    0/6 passed · accuracy=0.00%
[eval-majority]  1/6 passed · accuracy=16.67%
[eval-rule]      3/6 passed · accuracy=50.00%
```

---

## Improvements Made Over Original Proposal

| Issue | Original | Improved |
|-------|----------|----------|
| **Path flexibility** | Hardcoded paths | CLI args + defaults |
| **Error handling** | None; crashes on failure | Comprehensive try/except |
| **Error detail** | Generic "ok" or fail | 4-way categorization |
| **Test design** | Brittle monkeypatch | Explicit path passing |
| **Accuracy threshold** | Strict 100% | Configurable via `--min-accuracy` |
| **Latency tracking** | Basic | Per-step (gen_ms, grade_ms) |
| **Production readiness** | Proof of concept | Ready for extension |

---

## How to Use

### Run baseline once
```bash
make eval
```

### Run tests (no harness)
```bash
make eval-test
```

### Run full CI gate
```bash
make eval-ci
```

### Custom paths & threshold
```bash
python3 -m agentic.evals.run_eval \
  --seed-path custom/seeds.jsonl \
  --report-path /tmp/eval_report.jsonl \
  --min-accuracy 0.95 \
  -v
```

### Integration with CI pipeline
In `.github/workflows/ci.yml`, add:
```yaml
- name: Agent Eval (seed set)
  run: make eval-ci
```

---

## File Locations

- **Main harness:** `agentic/evals/run_eval.py` (196 lines)
- **Tests:** `agentic/evals/test_eval_harness.py` (246 lines)
- **Seeds:** `agentic/evals/seed_math.jsonl` (6 lines)
- **Latest report:** `agentic/evals/report.jsonl` (auto-generated)
- **Makefile targets:** Updated to include `eval`, `eval-test`, `eval-ci`

---

## Verification Checklist

- ✅ All 9 contract tests pass
- ✅ Baseline achieves 100% accuracy (6/6)
- ✅ Report JSONL is well-formed
- ✅ No regressions in existing tests (97 pass, 1 skipped)
- ✅ Makefile targets work: `make eval`, `make eval-test`, `make eval-ci`
- ✅ Error handling robust (tested missing seed file, threshold logic)
- ✅ Latency measured (sub-millisecond per case)
- ✅ Seed set covers 4 skills, 2+ difficulties

---

## Branch & Commit Info

- **Branch:** `phase1-data-flywheel`
- **Latest commit:** `ec76a60` Step 1: Improved agent eval harness
- **Previous commits:** Phase 1 scaffold (baseline evals contracts, telemetry schema, observer stub)
- **Ready for:** Step 2 (agent strategy variants)
