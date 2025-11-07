import pathlib


def test_telemetry_eval_contract_exists():
    assert pathlib.Path("evals/telemetry_eval.yaml").exists()


def test_telemetry_runner_placeholder():
    # Import and run the telemetry evaluator
    import sys
    import pathlib
    import importlib.util
    
    # Load the telemetry eval module directly
    eval_path = pathlib.Path(__file__).parent.parent.parent / "evals" / "run_telemetry_eval.py"
    spec = importlib.util.spec_from_file_location("run_telemetry_eval", eval_path)
    telemetry_eval = importlib.util.module_from_spec(spec)
    sys.modules["run_telemetry_eval"] = telemetry_eval
    spec.loader.exec_module(telemetry_eval)
    
    run_telemetry_eval = telemetry_eval.run_telemetry_eval
    
    # Test that telemetry eval runner works
    result = run_telemetry_eval()
    assert "passed" in result, "Telemetry eval must return pass/fail status"
    assert "validation" in result, "Telemetry eval must return validation results"
    assert "total_events" in result, "Telemetry eval must return total event count"
    
    # Test validation structure
    if "validation" in result:
        validation = result["validation"]
        assert "summary" in validation, "Must include validation summary"
        
        # Check that expected event types are validated
        expected_events = ["generate", "grade", "cycle_reset"]
        for event_type in expected_events:
            if event_type in validation:
                event_validation = validation[event_type]
                assert "count" in event_validation, f"Must include count for {event_type}"
                assert "completeness_pct" in event_validation, f"Must include completeness % for {event_type}"
                assert "passed" in event_validation, f"Must include pass/fail for {event_type}"
