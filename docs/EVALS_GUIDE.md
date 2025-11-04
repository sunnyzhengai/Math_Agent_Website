# EVALS Guide

Run all evals:

```bash
make evals
```

Inputs:

* Telemetry JSONL: `logs/telemetry.jsonl` (+ rotated)
* Manifest: `/skills/manifest` response (test fixtures allowed)

Outputs:

* Console scorecard
* Non-zero exit if thresholds not met

Implementation rule:

* Fix the first failing test only. No contract changes unless the test mandates it.
