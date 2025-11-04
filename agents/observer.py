"""
Observer: consumes datasets/telemetry_latest.jsonl and emits recommendations to logs/observer.jsonl

Recs examples:
- Low coverage for (skill,diff) → "add N templates"
- Low correctness → "review distractors or tune difficulty"
"""

from pathlib import Path
import json, time


DATASET = Path("datasets/telemetry_latest.jsonl")
OUT = Path("logs/observer.jsonl")


def observe():
    if not DATASET.exists():
        raise FileNotFoundError("datasets/telemetry_latest.jsonl not found. Run `make export` first.")

    # TODO: implement aggregation & heuristics
    raise NotImplementedError("Implement observer aggregation & recommendations")


if __name__ == "__main__":
    observe()
