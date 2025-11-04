"""
Contract tests for agent eval harness.

These tests ensure:
1. Seed set is well-formed and loadable
2. Eval runner produces well-formed reports with required fields
3. Baseline (100% accuracy) is maintained as regression guard
"""

from pathlib import Path
import json
import pytest

from agentic.evals.run_eval import load_jsonl, run_case, main


def test_seed_set_exists():
    """Verify seed set file exists and is readable."""
    p = Path("agentic/evals/seed_math.jsonl")
    assert p.exists(), "seed_math.jsonl must exist"
    assert p.stat().st_size > 0, "seed_math.jsonl must not be empty"


def test_seed_set_loads():
    """Verify seed set loads without errors and has required fields."""
    p = Path("agentic/evals/seed_math.jsonl")
    cases = load_jsonl(p)
    
    assert len(cases) >= 4, f"seed set should have >= 4 cases, got {len(cases)}"
    
    for c in cases:
        assert "id" in c, f"Case {c} missing 'id'"
        assert "skill_id" in c, f"Case {c} missing 'skill_id'"
        assert "difficulty" in c, f"Case {c} missing 'difficulty'"
        assert "seed" in c, f"Case {c} missing 'seed'"


def test_seed_set_diversity():
    """Verify seed set covers multiple skills and difficulties."""
    p = Path("agentic/evals/seed_math.jsonl")
    cases = load_jsonl(p)
    
    skills = {c["skill_id"] for c in cases}
    difficulties = {c["difficulty"] for c in cases}
    
    assert len(skills) >= 3, f"seed set should have >= 3 skills, got {len(skills)}: {skills}"
    assert len(difficulties) >= 2, f"seed set should have >= 2 difficulties, got {len(difficulties)}"


def test_run_case_returns_well_formed_row():
    """Verify run_case() returns a dict with all required fields."""
    # Use an easy case from seed set
    case = {
        "id": "test-1",
        "skill_id": "quad.graph.vertex",
        "difficulty": "easy",
        "seed": 42,
    }
    ok, row = run_case(case)
    
    # Check required fields
    required = ["id", "skill_id", "difficulty", "seed", "status", "ok", "gen_ms", "grade_ms", "stem_hash"]
    for key in required:
        assert key in row, f"Row missing key: {key}"
    
    # Check types
    assert isinstance(row["id"], str)
    assert isinstance(row["ok"], bool)
    assert row["status"] in ("ok", "generate_error", "grade_error", "incorrect", None)
    
    # For successful case, check values
    if row["ok"]:
        assert row["status"] == "ok"
        assert row["gen_ms"] > 0
        assert row["grade_ms"] > 0
        assert row["stem_hash"] is not None


def test_run_case_baseline_100_percent():
    """Verify baseline (correct answer) achieves 100% accuracy."""
    # Test a few cases from different skills
    test_cases = [
        {"id": "base-1", "skill_id": "quad.graph.vertex", "difficulty": "easy", "seed": 42},
        {"id": "base-2", "skill_id": "quad.standard.vertex", "difficulty": "easy", "seed": 11},
        {"id": "base-3", "skill_id": "quad.roots.factored", "difficulty": "medium", "seed": 12},
    ]
    
    for case in test_cases:
        ok, row = run_case(case)
        assert ok is True, f"Baseline should always be correct; case {case['id']} failed: {row.get('error', 'unknown')}"
        assert row["ok"] is True
        assert row["status"] == "ok"


def test_main_with_temp_files(tmp_path):
    """Integration test: main() produces a valid report."""
    # Create a minimal seed file
    seed_file = tmp_path / "seed.jsonl"
    seed_file.write_text(
        '{"id":"t1","skill_id":"quad.graph.vertex","difficulty":"easy","seed":42}\n'
        '{"id":"t2","skill_id":"quad.graph.vertex","difficulty":"easy","seed":43}\n',
        encoding="utf-8"
    )
    
    report_file = tmp_path / "report.jsonl"
    
    # Run main with custom paths
    exit_code = main(
        seed_path=str(seed_file),
        report_path=str(report_file),
        min_accuracy=1.0,  # 100% for baseline
        verbose=False,
    )
    
    # Check exit code (0 = success)
    assert exit_code == 0, f"main() should succeed with baseline; got exit code {exit_code}"
    
    # Check report was written
    assert report_file.exists(), f"Report file {report_file} not created"
    
    # Verify report content
    lines = report_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2, f"Report should have 2 lines, got {len(lines)}"
    
    for line in lines:
        row = json.loads(line)
        assert "id" in row
        assert "ok" in row
        assert "status" in row
        assert "gen_ms" in row
        assert row["ok"] is True, f"Baseline case {row['id']} should pass"


def test_main_respects_min_accuracy_threshold(tmp_path):
    """Verify main() respects min_accuracy parameter."""
    # Create seed file (will pass 100%)
    seed_file = tmp_path / "seed.jsonl"
    seed_file.write_text(
        '{"id":"t1","skill_id":"quad.graph.vertex","difficulty":"easy","seed":42}\n',
        encoding="utf-8"
    )
    report_file = tmp_path / "report.jsonl"
    
    # Should pass with threshold 100%
    exit_code_100 = main(
        seed_path=str(seed_file),
        report_path=str(report_file),
        min_accuracy=1.0,
        verbose=False,
    )
    assert exit_code_100 == 0
    
    # Should pass with threshold 50%
    exit_code_50 = main(
        seed_path=str(seed_file),
        report_path=str(report_file),
        min_accuracy=0.5,
        verbose=False,
    )
    assert exit_code_50 == 0
    
    # Should fail with threshold 101% (impossible)
    exit_code_101 = main(
        seed_path=str(seed_file),
        report_path=str(report_file),
        min_accuracy=1.01,
        verbose=False,
    )
    assert exit_code_101 == 1


def test_main_handles_missing_seed_file(tmp_path):
    """Verify main() handles missing seed file gracefully."""
    seed_file = tmp_path / "nonexistent.jsonl"
    report_file = tmp_path / "report.jsonl"
    
    exit_code = main(
        seed_path=str(seed_file),
        report_path=str(report_file),
        min_accuracy=1.0,
        verbose=False,
    )
    
    # Should fail
    assert exit_code == 1, "main() should fail if seed file missing"


def test_load_jsonl_skips_comments_and_empty_lines():
    """Verify load_jsonl skips comment lines (starting with #) and empty lines."""
    from pathlib import Path
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        p = Path(tmpdir) / "test.jsonl"
        p.write_text(
            "# This is a comment\n"
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
