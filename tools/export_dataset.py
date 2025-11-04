#!/usr/bin/env python3
"""
Export latest telemetry to datasets/telemetry_latest.jsonl (append-safe).

- Reads logs/telemetry.jsonl (+ rotated files optional).
- Emits deduped rows with fields:
  session_id, item_id, skill_id, difficulty, stem_hash, choice_id, correct, latency_ms, ts
"""

from pathlib import Path
import json, sys

OUT = Path("datasets/telemetry_latest.jsonl")
SRC = Path("logs/telemetry.jsonl")


def main():
    if not SRC.exists():
        print("no telemetry file found at logs/telemetry.jsonl", file=sys.stderr)
        raise NotImplementedError("Implement export_dataset ETL")

    # TODO: implement streaming read, filter allowlisted fields, dedupe, write OUT
    raise NotImplementedError("Implement export_dataset ETL")


if __name__ == "__main__":
    main()
