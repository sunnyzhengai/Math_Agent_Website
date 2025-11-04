"""
Tests for eval harness with agent support.

Tests verify:
- run_case works with different agents
- Row schema is complete and consistent
- Error categorization is correct
- Oracle maintains 100% accuracy regression guard
"""

import json
import pytest
from pathlib import Path
from engine.templates import generate_item
from agentic.evals.run_eval import run_case, load_jsonl


def test_run_case_with_oracle():
    """Verify run_case works with oracle agent."""
    case = {
        "id": "test-1",
        "skill_id": "quad.graph.vertex",
        "difficulty": "easy",
        "seed": 42,
    }
    ok, row = run_case(case, "oracle")
    
    # Oracle should always succeed
    assert ok is True
    assert row["ok"] is True
    assert row["status"] == "ok"
    assert row["agent"] == "oracle"
    assert row["picked"] == row["solution"]


def test_run_case_row_schema():
    """Verify row has complete schema for all agents."""
    case = {
        "id": "schema-test",
        "skill_id": "quad.graph.vertex",
        "difficulty": "easy",
        "seed": 42,
    }
    
    required_fields = {
        "id", "agent", "skill_id", "difficulty", "seed",
        "status", "ok", "picked", "solution",
        "gen_ms", "grade_ms", "stem_hash", "error"
    }
    
    for agent_name in ["oracle", "always_a", "random"]:
        ok, row = run_case(case, agent_name)
        
        for field in required_fields:
            assert field in row, f"Row missing field: {field} for agent {agent_name}"
        
        # Check types
        assert isinstance(row["id"], str)
        assert isinstance(row["agent"], str)
        assert isinstance(row["ok"], bool)
        assert isinstance(row["status"], str)
        assert row["status"] in ("ok", "generate_error", "agent_error", "grade_error", "incorrect")
        
        # For successful cases, validate additional fields
        if row["ok"]:
            assert row["picked"] in {"A", "B", "C", "D"}
            assert row["solution"] in {"A", "B", "C", "D"}
            assert row["gen_ms"] >= 0  # Can be very fast, may round to 0
            assert row["grade_ms"] >= 0  # Can be very fast, may round to 0
            assert row["stem_hash"] is not None


def test_run_case_oracle_always_correct():
    """Regression guard: oracle must achieve 100% across diverse cases."""
    test_cases = [
        {"id": "o1", "skill_id": "quad.graph.vertex", "difficulty": "easy", "seed": 42},
        {"id": "o2", "skill_id": "quad.graph.vertex", "difficulty": "medium", "seed": 43},
        {"id": "o3", "skill_id": "quad.standard.vertex", "difficulty": "easy", "seed": 11},
        {"id": "o4", "skill_id": "quad.roots.factored", "difficulty": "medium", "seed": 12},
        {"id": "o5", "skill_id": "quad.solve.by_factoring", "difficulty": "easy", "seed": 21},
    ]
    
    for case in test_cases:
        ok, row = run_case(case, "oracle")
        assert ok is True, f"Oracle failed on {case}: {row}"
        assert row["ok"] is True
        assert row["status"] == "ok"


def test_run_case_always_a_deterministic():
    """Verify AlwaysA agent always picks A."""
    for seed in range(5):
        case = {
            "id": f"a{seed}",
            "skill_id": "quad.graph.vertex",
            "difficulty": "easy",
            "seed": seed,
        }
        ok, row = run_case(case, "always_a")
        assert row["picked"] == "A", f"AlwaysA should always pick A, got {row['picked']}"


def test_run_case_error_categorization():
    """Verify error categorization is correct."""
    # Test invalid agent name (caught as agent_error, not raised)
    case = {
        "id": "err1",
        "skill_id": "quad.graph.vertex",
        "difficulty": "easy",
        "seed": 42,
    }
    
    ok, row = run_case(case, "invalid_agent")
    assert ok is False
    assert row["status"] == "agent_error"
    assert row["error"] is not None
    assert "unknown_agent" in row["error"]
    
    # Test generate error (invalid skill)
    bad_case = {
        "id": "err2",
        "skill_id": "nonexistent.skill",
        "difficulty": "easy",
        "seed": 42,
    }
    ok, row = run_case(bad_case, "oracle")
    assert ok is False
    assert row["status"] == "generate_error"
    assert row["error"] is not None


def test_run_case_picks_recorded():
    """Verify picked choice is recorded correctly."""
    case = {
        "id": "pick1",
        "skill_id": "quad.graph.vertex",
        "difficulty": "easy",
        "seed": 42,
    }
    
    # Run with each agent
    for agent_name in ["oracle", "always_a", "random"]:
        ok, row = run_case(case, agent_name)
        
        # Should have picked a choice
        assert row["picked"] is not None
        assert row["picked"] in {"A", "B", "C", "D"}
        
        # For oracle, picked should equal solution
        if agent_name == "oracle":
            assert row["picked"] == row["solution"]
        
        # For always_a, picked should always be A
        if agent_name == "always_a":
            assert row["picked"] == "A"


def test_run_case_latency_recorded():
    """Verify latency is recorded for successful cases."""
    case = {
        "id": "lat1",
        "skill_id": "quad.graph.vertex",
        "difficulty": "easy",
        "seed": 42,
    }
    ok, row = run_case(case, "oracle")
    
    assert ok is True
    assert row["gen_ms"] is not None
    assert row["gen_ms"] > 0
    assert row["gen_ms"] < 1000  # Should be under 1 second
    
    assert row["grade_ms"] is not None
    assert row["grade_ms"] > 0
    assert row["grade_ms"] < 1000


def test_run_case_stem_hash_recorded():
    """Verify stem hash is recorded."""
    case = {
        "id": "hash1",
        "skill_id": "quad.graph.vertex",
        "difficulty": "easy",
        "seed": 42,
    }
    ok, row = run_case(case, "oracle")
    
    assert row["stem_hash"] is not None
    assert isinstance(row["stem_hash"], str)
    assert len(row["stem_hash"]) == 10  # SHA1[:10]


def test_run_case_consistent_across_calls():
    """Verify run_case produces same result for same inputs."""
    case = {
        "id": "const1",
        "skill_id": "quad.graph.vertex",
        "difficulty": "easy",
        "seed": 42,
    }
    
    ok1, row1 = run_case(case, "random")
    ok2, row2 = run_case(case, "random")
    
    # Deterministic for same case
    assert ok1 == ok2
    assert row1["picked"] == row2["picked"]
    assert row1["solution"] == row2["solution"]
    assert row1["stem_hash"] == row2["stem_hash"]


def test_seed_set_loads():
    """Verify seed set JSONL loads correctly."""
    p = Path("agentic/evals/seed_math.jsonl")
    cases = load_jsonl(p)
    
    assert len(cases) >= 4
    for c in cases:
        assert "id" in c
        assert "skill_id" in c
        assert "difficulty" in c
        assert "seed" in c


def test_load_jsonl_skips_comments():
    """Verify load_jsonl skips comments and empty lines."""
    from pathlib import Path
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        p = Path(tmpdir) / "test.jsonl"
        p.write_text(
            "# Comment line\n"
            '{"id":"1","value":1}\n'
            "\n"
            '{"id":"2","value":2}\n'
            "# Another comment\n",
            encoding="utf-8"
        )
        
        rows = load_jsonl(p)
        assert len(rows) == 2
        assert rows[0]["id"] == "1"
        assert rows[1]["id"] == "2"
