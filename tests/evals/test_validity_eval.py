import pathlib


def test_validity_eval_contract_exists():
    assert pathlib.Path("evals/validity_eval.yaml").exists()


def test_validity_eval_thresholds():
    txt = pathlib.Path("evals/validity_eval.yaml").read_text()
    assert "min_pct:" in txt


def test_validity_runner_placeholder():
    raise NotImplementedError("Implement validity eval: sample generate events → revalidate items → % ≥ threshold")
