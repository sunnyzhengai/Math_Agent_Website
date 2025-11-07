import json, os, re, pathlib


def test_coverage_eval_contract_exists():
    path = pathlib.Path("evals/coverage_eval.yaml")
    assert path.exists(), "coverage_eval.yaml must exist"


def test_coverage_eval_thresholds():
    txt = pathlib.Path("evals/coverage_eval.yaml").read_text()
    assert "min_pct:" in txt, "coverage eval must declare thresholds.min_pct"


def test_manifest_contract_keys_present():
    # This is a contract test; use a minimal fixture expectation the runner must fulfill.
    # The eval implementation can read /skills/manifest or fixture, but must include these keys.
    required = ["easy","medium","hard","applied"]
    
    # Import and run the coverage evaluator
    import sys
    import pathlib
    import importlib.util
    
    # Load the coverage eval module directly
    eval_path = pathlib.Path(__file__).parent.parent.parent / "evals" / "run_coverage_eval.py"
    spec = importlib.util.spec_from_file_location("run_coverage_eval", eval_path)
    coverage_eval = importlib.util.module_from_spec(spec)
    sys.modules["run_coverage_eval"] = coverage_eval
    spec.loader.exec_module(coverage_eval)
    
    run_coverage_eval = coverage_eval.run_coverage_eval
    get_skills_manifest = coverage_eval.get_skills_manifest
    
    # Test that manifest includes required difficulty keys
    manifest = get_skills_manifest()
    # Handle both direct format and wrapped format
    skills = manifest.get("skills", manifest) if "skills" in manifest else manifest
    
    # Check that at least one skill has all required difficulties
    assert len(skills) > 0, "Must have at least one skill in manifest"
    
    # Check that all difficulties are represented across all skills
    all_difficulties = set()
    for skill_id, skill_data in skills.items():
        all_difficulties.update(skill_data.keys())
    
    for required_diff in required:
        assert required_diff in all_difficulties, f"Required difficulty '{required_diff}' not found in manifest"
    
    # Test that eval runner works
    result = run_coverage_eval()
    assert "passed" in result, "Coverage eval must return pass/fail status"
    assert "metrics" in result, "Coverage eval must return metrics"
