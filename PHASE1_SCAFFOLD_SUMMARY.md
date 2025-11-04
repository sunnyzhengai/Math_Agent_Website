# Phase 1 Scaffold — Summary & Handoff

**Branch:** `phase1-data-flywheel`  
**Commit:** `bc4d912` Phase 1 scaffold: evals contracts, telemetry schema, observer agent, test stubs  
**Date:** 2025-11-04

---

## What Was Created

A **clean, side-car scaffold** for Phase 1 (Data Flywheel) that won't touch any existing web/API code. Everything is opt-in and ready for incremental Cursor implementation.

### File Structure

```
docs/
  SPEC_PHASE1.md              # High-level phase goals & acceptance criteria
  TELEMETRY_SCHEMA.md         # Authoritative event schema (source of truth)
  EVALS_GUIDE.md              # How to run & interpret evals

evals/
  coverage_eval.yaml          # (skill, difficulty) pool coverage ≥ 95%
  validity_eval.yaml          # Sampled generate items pass validators ≥ 90%
  latency_eval.yaml           # p50/p90 latency thresholds
  telemetry_eval.yaml         # Required fields present ≥ 95%
  dataset_freshness_eval.py   # Dataset age < 24h

tests/evals/
  test_coverage_eval.py       # 3 tests: 2 pass (contract), 1 red (impl stub)
  test_validity_eval.py       # 3 tests: 2 pass, 1 red
  test_latency_eval.py        # 3 tests: 2 pass, 1 red
  test_telemetry_eval.py      # 2 tests: 1 pass, 1 red
  test_dataset_freshness_eval.py # 2 tests: 1 pass, 1 red

tools/
  export_dataset.py           # ETL stub: telemetry → datasets/telemetry_latest.jsonl
  analyze_telemetry.py        # ✅ Already implemented; quick stats on telemetry

agents/
  observer.py                 # Stub: consume dataset → emit recommendations
```

---

## Test Status

```
============================= test session starts ==============================
tests/evals/test_coverage_eval.py::test_coverage_eval_contract_exists PASSED
tests/evals/test_coverage_eval.py::test_coverage_eval_thresholds PASSED
tests/evals/test_coverage_eval.py::test_manifest_contract_keys_present FAILED ❌ (NotImplementedError)
tests/evals/test_dataset_freshness_eval.py::test_dataset_freshness_eval_contract_exists PASSED
tests/evals/test_dataset_freshness_eval.py::test_dataset_freshness_runner_placeholder FAILED ❌ (NotImplementedError)
tests/evals/test_latency_eval.py::test_latency_eval_contract_exists PASSED
tests/evals/test_latency_eval.py::test_latency_thresholds_present PASSED
tests/evals/test_latency_eval.py::test_latency_runner_placeholder FAILED ❌ (NotImplementedError)
tests/evals/test_telemetry_eval.py::test_telemetry_eval_contract_exists PASSED
tests/evals/test_telemetry_eval.py::test_telemetry_runner_placeholder FAILED ❌ (NotImplementedError)
tests/evals/test_validity_eval.py::test_validity_eval_contract_exists PASSED
tests/evals/test_validity_eval.py::test_validity_eval_thresholds PASSED
tests/evals/test_validity_eval.py::test_validity_runner_placeholder FAILED ❌ (NotImplementedError)

8 PASSED ✅ (contract tests)
5 FAILED ❌ (red by design; ready for impl)
```

---

## Evals Defined

| Name | Threshold | Input | Purpose |
|------|-----------|-------|---------|
| **coverage** | ≥ 95% | `/skills/manifest` | Ensure (skill,difficulty) pools exist |
| **validity** | ≥ 90% | `generate` events + validators | Catch data quality regressions |
| **latency** | p50<80ms, p90<200ms | telemetry | Track performance (generate/grade) |
| **telemetry** | ≥ 95% completeness | all events | Catch missing field bugs |
| **freshness** | < 24h old | `datasets/telemetry_latest.jsonl` | Detect stale exports |

---

## Ready for Implementation

### Workflow

1. **Run one failing test:**
   ```bash
   python3 -m pytest tests/evals/test_coverage_eval.py::test_manifest_contract_keys_present -xvs
   ```

2. **Fix the first failing test only.** Do not:
   - Change API/web contracts
   - Refactor other tests
   - Pre-implement later evals
   - Keep diffs under ~200 LOC

3. **Commit each step** with a clear message.

### Example First Step: Coverage Eval

The first failing test (`test_manifest_contract_keys_present`) expects the coverage eval to:
- Read `/skills/manifest` (or fixture)
- Compute % of (skill, difficulty) pools with size ≥ 1
- Check threshold: ≥ 95%
- Print scorecard or fail with non-zero exit

---

## No Breaking Changes

- ✅ No existing API endpoints modified
- ✅ No telemetry schema changes
- ✅ No web UI touches
- ✅ All new code is in `docs/`, `evals/`, `tests/evals/`, `agents/`, `tools/`
- ✅ Existing tests unaffected: `python3 -m pytest tests/ -k 'not evals'` is clean

---

## Next Steps for Cursor

Hand the repo to Cursor with **one instruction at a time**:

> "Fix the first failing test: `test_manifest_contract_keys_present`. Implement a coverage eval that reads `/skills/manifest` via pytest fixture or live HTTP, validates (skill,difficulty) pool coverage ≥ 95%, and raise AssertionError if threshold fails. Keep the diff under 200 LOC."

Then for each subsequent failing test, repeat with a similar focused instruction.

---

## Reference Files

- **Phase spec:** `docs/SPEC_PHASE1.md`
- **Schema source of truth:** `docs/TELEMETRY_SCHEMA.md`
- **Eval guide:** `docs/EVALS_GUIDE.md`
- **Example data:** `logs/telemetry.jsonl` (generated during normal operation)

---

## Quick Checks

```bash
# Verify scaffold is in place
ls -la docs/SPEC_PHASE1.md evals/*.yaml tests/evals/test_*.py agents/observer.py

# Run just the evals tests
python3 -m pytest tests/evals/ -v

# Verify no side effects on existing tests
python3 -m pytest tests/ -k 'not evals' --co -q | wc -l
```

---

## Branch Info

- **Branch name:** `phase1-data-flywheel`
- **Base:** `main` (all previous phases included)
- **Status:** Ready for handoff to Cursor
- **Merge strategy:** Squash + merge back to `main` after all evals pass
