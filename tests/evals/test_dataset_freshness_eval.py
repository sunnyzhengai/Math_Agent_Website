import pathlib


def test_dataset_freshness_eval_contract_exists():
    assert pathlib.Path("evals/dataset_freshness_eval.yaml").exists()


def test_dataset_freshness_runner_placeholder():
    # Import and run the dataset freshness evaluator
    import sys
    import pathlib
    import importlib.util
    
    # Load the dataset freshness eval module directly
    eval_path = pathlib.Path(__file__).parent.parent.parent / "evals" / "run_dataset_freshness_eval.py"
    spec = importlib.util.spec_from_file_location("run_dataset_freshness_eval", eval_path)
    freshness_eval = importlib.util.module_from_spec(spec)
    sys.modules["run_dataset_freshness_eval"] = freshness_eval
    spec.loader.exec_module(freshness_eval)
    
    run_dataset_freshness_eval = freshness_eval.run_dataset_freshness_eval
    
    # Test that freshness eval runner works
    result = run_dataset_freshness_eval()
    assert "passed" in result, "Dataset freshness eval must return pass/fail status"
    assert "files" in result, "Dataset freshness eval must return file results"
    assert "summary" in result, "Dataset freshness eval must return summary"
    
    # Test that it handles the expected file structure
    if result["passed"]:
        assert result["summary"]["fresh_files"] > 0, "Should have at least one fresh file if passed"
    
    # Test that thresholds are present
    assert "thresholds" in result, "Must include thresholds"
    assert "max_age_seconds" in result["thresholds"], "Must include max age threshold"
