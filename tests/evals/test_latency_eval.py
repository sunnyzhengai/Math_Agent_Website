import pathlib, yaml


def test_latency_eval_contract_exists():
    assert pathlib.Path("evals/latency_eval.yaml").exists()


def test_latency_thresholds_present():
    data = yaml.safe_load(pathlib.Path("evals/latency_eval.yaml").read_text())
    assert "thresholds" in data and "generate" in data["thresholds"] and "grade" in data["thresholds"]


def test_latency_runner_placeholder():
    raise NotImplementedError("Implement latency eval: compute p50/p90 per route from telemetry")
