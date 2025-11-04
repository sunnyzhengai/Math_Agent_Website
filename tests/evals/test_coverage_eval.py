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
    # This test intentionally fails until the eval runner is implemented.
    raise NotImplementedError("Implement coverage eval runner to satisfy manifest contract & thresholds")
