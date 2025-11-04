# SPEC.md — Phase 1 (Foundations: MVP → Data Flywheel, Agentic Framework)

**Project:** Math Agent  
**Phase:** 1 — Foundations (Agentic MVP to Data Flywheel)  
**Owner:** Sunny / Core Team  
**Date:** 2025-11-03

## 1) Purpose & Outcomes

- Telemetry → Evals → Dataset → Observer → Dashboard.
- No LLM in prod, no contract drift.

## 2) Scope

- Evals contracts (.yaml)
- Telemetry already in place; use it as input
- Skill graph V2 surfacing pool sizes via `/skills/manifest`
- ETL → `datasets/telemetry_latest.jsonl`
- Observer emits recs to `logs/observer.jsonl`
- Minimal dashboard (later)

## 3) Telemetry Schema (authoritative)

See `docs/TELEMETRY_SCHEMA.md`.

## 4) Config & Ops

- `TELEMETRY_ENABLED=true`, rotation 5MB
- `make evals`, `make export`, `make observe`, `make analyze-telemetry`

## 5) Dataset Fields

- session_id, item_id, skill_id, difficulty, stem_hash, choice_id, correct, latency_ms, ts

## 6) Evals & Thresholds

| Eval | Threshold |
|------|-----------|
| Coverage | ≥ 95% pools present |
| Validity | ≥ 90% pass validators |
| Latency (generate) | p50 < 80ms, p90 < 200ms |
| Telemetry completeness | ≥ 95% fields present |
| Dataset freshness | < 24h |

## 7) Risks & Mitigations

- Concurrency → single-process lock; note multi-worker caveat.
- PII → allowlist + stem hashing.
- Eval brittleness → deterministic seeds.

## 8) Deliverables & Layout

Matches this scaffold.

## 9) Acceptance

- `make evals` green in CI.
- Observer produces at least one recommendation when something is low.
