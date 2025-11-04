#!/usr/bin/env python3
"""
Agent eval harness: compare agent strategies under deterministic test cases.

Supports multiple agents (oracle, random, always_a, etc.) with comprehensive
error categorization and per-agent reporting.

Usage:
    python3 -m agentic.evals.run_eval [--agent AGENT] [--cases PATH] [--out PATH]

Agents:
    oracle    - Always picks correct answer (upper bound / regression guard)
    random    - Picks deterministically random choice
    always_a  - Always picks choice A (sanity check)
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
from agentic.agents.registry import get_agent, list_agents


def load_jsonl(p: Path) -> List[Dict[str, Any]]:
    """Load JSONL file; skip empty lines and comments."""
    try:
        return [
            json.loads(line)
            for line in p.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
    except Exception as e:
        raise RuntimeError(f"Failed to load {p}: {e}")


def run_case(case: Dict[str, Any], agent_name: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Run a single test case with an agent.

    Steps:
    1. Generate item deterministically
    2. Agent chooses a response
    3. Grade the response
    4. Record result with latency and error info

    Args:
        case: Test case dict {id, skill_id, difficulty, seed}
        agent_name: Name of agent to use

    Returns:
        (ok: bool, row: dict) where ok=True if grading succeeded and was correct.
        Row includes: id, agent, skill_id, difficulty, seed, status, ok,
                      picked, solution, gen_ms, grade_ms, stem_hash, error
    """
    case_id = case.get("id", "unknown")
    skill_id = case.get("skill_id")
    difficulty = case.get("difficulty")
    seed = case.get("seed")

    # Initialize row with all fields
    row = {
        "id": case_id,
        "agent": agent_name,
        "skill_id": skill_id,
        "difficulty": difficulty,
        "seed": seed,
        "status": None,  # "ok" | "generate_error" | "agent_error" | "grade_error" | "incorrect"
        "ok": False,
        "picked": None,
        "solution": None,
        "gen_ms": None,
        "grade_ms": None,
        "stem_hash": None,
        "error": None,
    }

    # Step 1: Generate item deterministically
    try:
        t0 = time.time()
        item = generate_item(skill_id, difficulty, seed=seed)
        row["gen_ms"] = round((time.time() - t0) * 1000, 2)
    except Exception as e:
        row["status"] = "generate_error"
        row["error"] = str(e)
        return False, row

    # Record solution and stem hash for all cases
    try:
        row["solution"] = item["solution_choice_id"]
        stem_hash = hashlib.sha1(item.get("stem", "").encode()).hexdigest()[:10]
        row["stem_hash"] = stem_hash
    except Exception:
        pass

    # Step 2: Get agent's choice
    try:
        agent = get_agent(agent_name)
        choice_id = agent.choose(item)

        # Validate choice is in valid set
        if choice_id not in ["A", "B", "C", "D"]:
            raise ValueError(f"invalid_choice:{choice_id}")

        row["picked"] = choice_id
    except Exception as e:
        row["status"] = "agent_error"
        row["error"] = str(e)
        return False, row

    # Step 3: Grade the response
    try:
        t1 = time.time()
        result = grade_response(item, choice_id)
        row["grade_ms"] = round((time.time() - t1) * 1000, 2)
    except Exception as e:
        row["status"] = "grade_error"
        row["error"] = str(e)
        return False, row

    # Step 4: Determine outcome
    is_correct = bool(result.get("correct", False))
    if is_correct:
        row["status"] = "ok"
        row["ok"] = True
        return True, row
    else:
        row["status"] = "incorrect"
        row["error"] = f"Selected {choice_id}, correct is {row['solution']}"
        return False, row


def main():
    """Run eval harness with specified agent."""
    parser = argparse.ArgumentParser(
        description="Agent eval harness: compare strategies on seed set"
    )
    parser.add_argument(
        "--agent",
        default="oracle",
        choices=list_agents(),
        help=f"Agent to evaluate (default: oracle)",
    )
    parser.add_argument(
        "--cases",
        default="agentic/evals/seed_math.jsonl",
        help="Path to JSONL seed cases",
    )
    parser.add_argument(
        "--out",
        default="agentic/evals/report.jsonl",
        help="Path to write JSONL report",
    )

    args = parser.parse_args()

    in_path = Path(args.cases)
    out_path = Path(args.out)

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
        ok, row = run_case(c, args.agent)
        rows.append(row)
        if ok:
            passed += 1

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
    print(f"[eval] agent={args.agent:10s} {passed}/{total} passed · accuracy={acc:.2%}")
    print(f"[eval] report -> {out_path}")

    # CI gate: strict only for oracle (should be 100%)
    # Other agents are informative only
    if args.agent == "oracle" and passed < total:
        print(
            f"[eval] FAIL: oracle accuracy {acc:.2%} < 100% (regression)",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
