# tests/item/test_quadratics_math.py

import math

import pytest

from engine.templates import SKILL_TEMPLATES, generate_item

from tests._utils import parse_standard_form


# ---------- quad.standard.vertex ----------

def test_standard_vertex_spotchecks():
    """Math sanity check: vertex formula h=-b/(2a), k=a*h^2+b*h+c"""
    items = SKILL_TEMPLATES["quad.standard.vertex"]["easy"]
    
    # Pick the first template as a representative check
    q = items[0]
    parsed = parse_standard_form(q["stem"])
    assert parsed, f"Cannot parse standard form from stem: {q['stem']}"
    
    a, b, c = parsed
    h = -b / (2 * a)
    k = a * (h ** 2) + b * h + c
    
    correct_text = q["choices"][q["solution"]]
    
    # Check that vertex (h, k) appears in correct answer
    assert f"({int(h) if h == int(h) else h}, " in correct_text, \
        f"h={h} must appear in correct choice: {correct_text}"
    assert f"{int(k) if k == int(k) else k})" in correct_text, \
        f"k={k} must appear in correct choice: {correct_text}"


# ---------- quad.roots.factored ----------

def test_roots_factored_spotchecks():
    """Math sanity check: factored form lists two roots"""
    # Use deterministic seed to check structure
    item = generate_item("quad.roots.factored", "easy", seed=42)
    
    correct_id = item["solution_choice_id"]
    text = next(c["text"] for c in item["choices"] if c["id"] == correct_id)
    
    # Sanity: should contain two roots (x = ... and x = ...)
    assert text.count("x") >= 2 and (" or " in text or "," in text or " and " in text), \
        f"Expected two roots in solution text: {text}"


# ---------- quad.solve.by_factoring ----------

def test_solve_by_factoring_spotchecks():
    """Math sanity check: solving by factoring yields two solutions"""
    item = generate_item("quad.solve.by_factoring", "easy", seed=42)
    
    correct_id = item["solution_choice_id"]
    text = next(c["text"] for c in item["choices"] if c["id"] == correct_id)
    
    # Basic shape: "x = ... or x = ..."
    assert "x" in text and (" or " in text or "," in text or " and " in text), \
        f"Expected two solutions in factoring solution: {text}"


# ---------- quad.solve.by_formula ----------

@pytest.mark.skip(reason="Unskip after adding quad.solve.by_formula templates")
def test_solve_by_formula_spotchecks():
    """Math sanity check: quadratic formula produces surd or rational roots"""
    item = generate_item("quad.solve.by_formula", "medium", seed=42)
    
    correct_id = item["solution_choice_id"]
    text = next(c["text"] for c in item["choices"] if c["id"] == correct_id)
    
    # Look for square root symbol or two solutions
    assert ("√" in text or "or" in text or "," in text), \
        f"Expected surd or two rational solutions: {text}"
