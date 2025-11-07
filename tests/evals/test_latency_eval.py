import pathlib, yaml


def test_latency_eval_contract_exists():
    assert pathlib.Path("evals/latency_eval.yaml").exists()


def test_latency_thresholds_present():
    data = yaml.safe_load(pathlib.Path("evals/latency_eval.yaml").read_text())
    assert "thresholds" in data and "generate" in data["thresholds"] and "grade" in data["thresholds"]


def test_latency_runner_placeholder():
    # Import and run the latency evaluator
    import sys
    import pathlib
    import importlib.util
    
    # Load the latency eval module directly
    eval_path = pathlib.Path(__file__).parent.parent.parent / "evals" / "run_latency_eval.py"
    spec = importlib.util.spec_from_file_location("run_latency_eval", eval_path)
    latency_eval = importlib.util.module_from_spec(spec)
    sys.modules["run_latency_eval"] = latency_eval
    spec.loader.exec_module(latency_eval)
    
    run_latency_eval = latency_eval.run_latency_eval
    
    # Test that latency eval runner works
    result = run_latency_eval()
    assert "passed" in result, "Latency eval must return pass/fail status"
    assert "metrics" in result, "Latency eval must return metrics"
    assert "thresholds" in result, "Latency eval must return thresholds"
    
    # Test that metrics include expected event types
    if "metrics" in result:
        metrics = result["metrics"]
        expected_events = ["generate", "grade"]
        for event_type in expected_events:
            if event_type in metrics and metrics[event_type]["count"] > 0:
                # Verify percentile metrics exist
                assert "p50_ms" in metrics[event_type], f"Must include p50 for {event_type}"
                assert "p90_ms" in metrics[event_type], f"Must include p90 for {event_type}"
    
    # Test that threshold results are present if thresholds exist
    if "threshold_results" in result:
        assert "overall" in result["threshold_results"], "Must include overall threshold result"
