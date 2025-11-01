#!/usr/bin/env python3
"""
Telemetry analyzer: stream JSONL and print roll-ups.

Usage:
    python tools/analyze_telemetry.py logs/telemetry.jsonl

Prints:
- Event totals by type
- Coverage: unique stem_hash counts by (skill_id, difficulty)
- Accuracy: % correct by skill_id and overall
- Latency: min/max/median by route type
"""

import json
import sys
import statistics
from collections import defaultdict
from pathlib import Path


def analyze(filepath: str) -> None:
    """Stream JSONL and compute statistics."""
    path = Path(filepath)
    
    if not path.exists():
        print(f"Error: {filepath} not found", file=sys.stderr)
        return
    
    # Counters
    event_counts = defaultdict(int)
    stem_hashes = defaultdict(set)  # (skill, difficulty) -> set of stem_hashes
    correct_counts = defaultdict(int)  # skill_id -> correct count
    total_grades = defaultdict(int)  # skill_id -> total grades
    latencies = defaultdict(list)  # event_type -> [latency_ms values]
    
    with open(path, "r") as f:
        for line_num, line in enumerate(f, 1):
            try:
                event = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Warning: line {line_num} invalid JSON: {e}", file=sys.stderr)
                continue
            
            event_type = event.get("event")
            event_counts[event_type] += 1
            
            # Track latency
            if "latency_ms" in event:
                try:
                    latencies[event_type].append(float(event["latency_ms"]))
                except (TypeError, ValueError):
                    pass
            
            # Coverage: unique stems per (skill, difficulty)
            if event_type == "generate":
                skill = event.get("skill_id", "unknown")
                difficulty = event.get("difficulty", "unknown")
                stem_hash = event.get("stem_hash")
                if stem_hash:
                    key = (skill, difficulty)
                    stem_hashes[key].add(stem_hash)
            
            # Accuracy: track correct grades per skill
            if event_type == "grade":
                skill = event.get("skill_id", "unknown")
                is_correct = event.get("correct", False)
                if is_correct:
                    correct_counts[skill] += 1
                total_grades[skill] += 1
    
    # Print results
    print("\n" + "=" * 70)
    print("TELEMETRY ANALYSIS")
    print("=" * 70)
    
    # Event totals
    print("\nEvent Totals:")
    total_events = sum(event_counts.values())
    for event_type in sorted(event_counts.keys()):
        count = event_counts[event_type]
        pct = 100 * count / total_events if total_events > 0 else 0
        print(f"  {event_type}: {count} ({pct:.1f}%)")
    print(f"  TOTAL: {total_events}")
    
    # Coverage (unique stems per pool)
    if stem_hashes:
        print("\nCoverage (unique stems by skill/difficulty):")
        for (skill, difficulty), hashes in sorted(stem_hashes.items()):
            print(f"  {skill} {difficulty}: {len(hashes)} unique")
    
    # Accuracy
    if total_grades:
        print("\nAccuracy by Skill:")
        total_correct = 0
        total_attempts = 0
        for skill in sorted(total_grades.keys()):
            correct = correct_counts.get(skill, 0)
            total = total_grades[skill]
            pct = 100 * correct / total if total > 0 else 0
            print(f"  {skill}: {correct}/{total} ({pct:.1f}%)")
            total_correct += correct
            total_attempts += total
        
        if total_attempts > 0:
            overall_pct = 100 * total_correct / total_attempts
            print(f"  OVERALL: {total_correct}/{total_attempts} ({overall_pct:.1f}%)")
    
    # Latency
    if latencies:
        print("\nLatency (ms) by Event Type:")
        for event_type in sorted(latencies.keys()):
            lats = latencies[event_type]
            if len(lats) > 0:
                print(f"  {event_type}:")
                print(f"    min: {min(lats):.2f}")
                print(f"    max: {max(lats):.2f}")
                print(f"    median: {statistics.median(lats):.2f}")
                if len(lats) > 1:
                    print(f"    stdev: {statistics.stdev(lats):.2f}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <telemetry.jsonl>", file=sys.stderr)
        sys.exit(1)
    
    analyze(sys.argv[1])
