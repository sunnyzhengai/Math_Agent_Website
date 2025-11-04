#!/usr/bin/env python3
"""
Agent eval harness: deterministic baseline for regression testing.

Usage:
    python3 -m agentic.evals.run_eval [--seed-path PATH] [--report-path PATH] [--min-accuracy PCT]

Baseline: Always picks the correct option (upper bound for agent strategies).
Output: JSONL with per-case results and overall accuracy.

See: agentic/evals/seed_math.jsonl (test cases)
     agentic/evals/test_eval_harness.py (contract tests)
"""

import json
import sys
import time
import hashlib
import argparse
from pathlib import Path
from typing import Dict, Any, List, Tuple

from engine.templates import generate_item
from engine.grader import grade_response


def load_jsonl(p: Path) -> List[Dict[str, Any]]:
    """Load JSONL file; skip empty lines."""
    try:
        return [
            json.loads(line)
            for line in p.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
    except Exception as e:
        raise RuntimeError(f"Failed to load {p}: {e}")


def run_case(case: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
    """
    Run a single test case: generate item, grade with correct answer, measure latency.

    Args:
        case: {id, skill_id, difficulty, seed}

    Returns:
        (ok: bool, row: dict) where ok=True if grading succeeded and was correct,
        row includes: id, skill_id, difficulty, seed, status, ok, gen_ms, grade_ms, stem_hash, [error]
    """
    case_id = case.get("id", "unknown")
    skill_id = case.get("skill_id")
    difficulty = case.get("difficulty")
    seed = case.get("seed")

    row = {
        "id": case_id,
        "skill_id": skill_id,
        "difficulty": difficulty,
        "seed": seed,
        "status": None,  # "ok" | "generate_error" | "grade_error" | "incorrect"
        "ok": False,
        "gen_ms": None,
        "grade_ms": None,
        "stem_hash": None,
        "error": None,
    }

    # Step 1: Generate item deterministically
    try:
        t0 = time.time()
        item = generate_item(skill_id, difficulty, seed=seed)
        gen_ms = (time.time() - t0) * 1000.0
        row["gen_ms"] = round(gen_ms, 2)
    except Exception as e:
        row["status"] = "generate_error"
        row["error"] = str(e)
        return False, row

    # Compute stem hash (first 10 chars of SHA1)
    try:
        stem_hash = hashlib.sha1(item.get("stem", "").encode()).hexdigest()[:10]
        row["stem_hash"] = stem_hash
    except Exception:
        pass

    # Step 2: Grade with correct answer (baseline: 100% accuracy upper bound)
    # This proves the engine is working; real agents will score lower.
    try:
        t1 = time.time()
        correct_choice = item.get("solution_choice_id")
        result = grade_response(item, correct_choice)
        grade_ms = (time.time() - t1) * 1000.0
        row["grade_ms"] = round(grade_ms, 2)
    except Exception as e:
        row["status"] = "grade_error"
        row["error"] = str(e)
        return False, row

    # Step 3: Check correctness
    is_correct = result.get("correct", False)
    if is_correct:
        row["status"] = "ok"
        row["ok"] = True
        return True, row
    else:
        row["status"] = "incorrect"
        row["error"] = f"Expected correct, got: {result.get('explanation', 'unknown')}"
        return False, row


def main(
    seed_path: str = "agentic/evals/seed_math.jsonl",
    report_path: str = "agentic/evals/report.jsonl",
    min_accuracy: float = 1.0,
    verbose: bool = False,
) -> int:
    """
    Run eval harness on seed set.

    Args:
        seed_path: Path to JSONL seed file
        report_path: Path to write JSONL report
        min_accuracy: Minimum accuracy threshold (0.0-1.0); fail if below
        verbose: Print per-case results

    Returns:
        0 if accuracy >= min_accuracy, else 1
    """
    in_path = Path(seed_path)
    out_path = Path(report_path)

    # Ensure output directory exists
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Load test cases
    try:
        cases = load_jsonl(in_path)
    except Exception as e:
        print(f"[eval] ERROR: {e}", file=sys.stderr)
        return 1

    if not cases:
        print(f"[eval] ERROR: No test cases found in {in_path}", file=sys.stderr)
        return 1

    # Run all cases
    rows = []
    passed = 0

    for c in cases:
        ok, row = run_case(c)
        rows.append(row)
        if ok:
            passed += 1

        if verbose:
            status = row["status"]
            print(
                f"  {row['id']:8s} | {row['skill_id']:25s} | {row['difficulty']:8s} | {status:15s}",
                file=sys.stderr,
            )

    # Write report
    try:
        report_lines = [json.dumps(r, ensure_ascii=False) for r in rows]
        out_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    except Exception as e:
        print(f"[eval] ERROR writing report: {e}", file=sys.stderr)
        return 1

    # Print summary
    total = len(rows)
    acc = passed / total if total else 0.0
    print(f"[eval] {passed}/{total} passed · accuracy={acc:.2%}")
    print(f"[eval] report -> {out_path}")

    # Check threshold
    if acc < min_accuracy:
        print(
            f"[eval] FAIL: accuracy {acc:.2%} < threshold {min_accuracy:.2%}",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agent eval harness baseline")
    parser.add_argument(
        "--seed-path",
        default="agentic/evals/seed_math.jsonl",
        help="Path to JSONL seed file",
    )
    parser.add_argument(
        "--report-path",
        default="agentic/evals/report.jsonl",
        help="Path to write JSONL report",
    )
    parser.add_argument(
        "--min-accuracy",
        type=float,
        default=1.0,
        help="Minimum accuracy threshold (0.0-1.0)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print per-case results"
    )

    args = parser.parse_args()
    exit_code = main(
        seed_path=args.seed_path,
        report_path=args.report_path,
        min_accuracy=args.min_accuracy,
        verbose=args.verbose,
    )
    sys.exit(exit_code)
