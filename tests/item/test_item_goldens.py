# tests/item/test_item_goldens.py

import json

import pathlib

import pytest

from engine.templates import generate_item


GOLDENS = pathlib.Path(__file__).parent.parent / "goldens"


def _load(path: pathlib.Path):
    """Load a golden JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _cmp(skill_id: str, difficulty: str, seed: int, golden_file: str):
    """Compare generated item to golden file."""
    item = generate_item(skill_id, difficulty, seed=seed)
    golden = _load(GOLDENS / golden_file)
    assert item == golden, \
        f"{skill_id}/{difficulty}/seed={seed} must match golden {golden_file}"


def test_golden_quad_graph_vertex_easy_42():
    """Golden: quad.graph.vertex easy seed=42"""
    _cmp("quad.graph.vertex", "easy", 42, "golden_item_quad_graph_vertex_easy_42.json")


@pytest.mark.skip(reason="Unskip after adding quad.standard.vertex golden")
def test_golden_quad_standard_vertex_easy_42():
    """Golden: quad.standard.vertex easy seed=42"""
    _cmp("quad.standard.vertex", "easy", 42, "golden_item_quad_standard_vertex_easy_42.json")


@pytest.mark.skip(reason="Unskip after adding quad.roots.factored golden")
def test_golden_quad_roots_factored_easy_42():
    """Golden: quad.roots.factored easy seed=42"""
    _cmp("quad.roots.factored", "easy", 42, "golden_item_quad_roots_factored_easy_42.json")


@pytest.mark.skip(reason="Unskip after adding quad.solve.by_factoring golden")
def test_golden_quad_solve_by_factoring_easy_42():
    """Golden: quad.solve.by_factoring easy seed=42"""
    _cmp("quad.solve.by_factoring", "easy", 42, "golden_item_quad_solve_by_factoring_easy_42.json")


@pytest.mark.skip(reason="Unskip after adding quad.solve.by_formula golden")
def test_golden_quad_solve_by_formula_easy_42():
    """Golden: quad.solve.by_formula easy seed=42"""
    _cmp("quad.solve.by_formula", "easy", 42, "golden_item_quad_solve_by_formula_easy_42.json")
