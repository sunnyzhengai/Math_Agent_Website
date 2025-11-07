import pathlib


def test_validity_eval_contract_exists():
    assert pathlib.Path("evals/validity_eval.yaml").exists()


def test_validity_eval_thresholds():
    txt = pathlib.Path("evals/validity_eval.yaml").read_text()
    assert "min_pct:" in txt


def test_validity_runner_placeholder():
    # Import and run the validity evaluator
    import sys
    import pathlib
    import importlib.util
    
    # Load the validity eval module directly
    eval_path = pathlib.Path(__file__).parent.parent.parent / "evals" / "run_validity_eval.py"
    spec = importlib.util.spec_from_file_location("run_validity_eval", eval_path)
    validity_eval = importlib.util.module_from_spec(spec)
    sys.modules["run_validity_eval"] = validity_eval
    spec.loader.exec_module(validity_eval)
    
    run_validity_eval = validity_eval.run_validity_eval
    
    # Test that validity eval runner works
    result = run_validity_eval()
    assert "passed" in result, "Validity eval must return pass/fail status"
    assert "validation_results" in result, "Validity eval must return validation results"
    assert "thresholds" in result, "Validity eval must return thresholds"
    
    # Test validation results structure
    if "validation_results" in result:
        validation = result["validation_results"]
        assert "total_sampled" in validation, "Must include total sampled count"
        assert "valid_items" in validation, "Must include valid items count"
        assert "validity_pct" in validation, "Must include validity percentage"
        
        # Test that some sampling occurred
        assert validation["total_sampled"] > 0, "Must sample some events for validation"
    
    # Test threshold structure
    if "thresholds" in result:
        assert "min_pct" in result["thresholds"], "Must include minimum percentage threshold"
