#!/usr/bin/env python3
"""
Coverage evaluation runner.

Checks coverage of (skill_id, difficulty) combinations against manifest.
Must satisfy min_pct threshold defined in coverage_eval.yaml.

Usage:
  python3 -m evals.run_coverage_eval
"""

import json
import yaml
import pathlib
from typing import Dict, Any, List
import requests
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from engine.templates import SKILL_TEMPLATES


def load_config() -> Dict[str, Any]:
    """Load configuration from coverage_eval.yaml."""
    config_path = pathlib.Path(__file__).parent / "coverage_eval.yaml"
    return yaml.safe_load(config_path.read_text())


def get_skills_manifest() -> Dict[str, Any]:
    """
    Get skills manifest either from HTTP endpoint or engine directly.
    
    Returns:
        Dict with skills and their available difficulties.
    """
    config = load_config()
    
    # Try HTTP route first (if running)
    for input_spec in config.get("inputs", []):
        if input_spec.get("type") == "http":
            route = input_spec.get("route", "/skills/manifest")
            try:
                # Try localhost:8000 first
                response = requests.get(f"http://localhost:8000{route}", timeout=2)
                if response.status_code == 200:
                    return response.json()
            except requests.RequestException:
                pass
    
    # Fallback: generate manifest from engine directly
    return generate_manifest_from_engine()


def generate_manifest_from_engine() -> Dict[str, Any]:
    """Generate manifest by querying engine directly."""
    difficulties = ["easy", "medium", "hard", "applied"]
    
    manifest = {}
    for skill_id, skill_data in SKILL_TEMPLATES.items():
        manifest[skill_id] = {}
        for difficulty in difficulties:
            # Count available templates for this skill/difficulty
            templates = skill_data.get(difficulty, [])
            count = len(templates) if templates else 0
            available = count > 0
            
            # Double-check by trying to generate an item
            try:
                from engine.templates import generate_item
                generate_item(skill_id, difficulty, seed=42)
            except Exception:
                available = False
                count = 0
            
            manifest[skill_id][difficulty] = {"available": available, "count": count}
    
    return manifest


def compute_coverage_metrics(manifest: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compute coverage metrics from manifest.
    
    Args:
        manifest: Skills manifest with availability data (either direct or wrapped in "skills" key)
        
    Returns:
        Dict with coverage metrics and per-skill breakdown
    """
    # Handle both direct manifest and wrapped format
    skills = manifest.get("skills", manifest) if "skills" in manifest else manifest
    difficulties = ["easy", "medium", "hard", "applied"]
    
    total_combinations = 0
    covered_combinations = 0
    coverage_by_skill = {}
    coverage_by_difficulty = {}
    
    # Initialize difficulty counters
    for diff in difficulties:
        coverage_by_difficulty[diff] = {"total": 0, "covered": 0}
    
    # Analyze each skill
    for skill_id, skill_data in skills.items():
        skill_total = 0
        skill_covered = 0
        
        for difficulty in difficulties:
            total_combinations += 1
            skill_total += 1
            coverage_by_difficulty[difficulty]["total"] += 1
            
            diff_data = skill_data.get(difficulty, {})
            
            # Handle different formats: int (HTTP API) vs dict (engine fallback)
            if isinstance(diff_data, int):
                count = diff_data
                is_covered = count >= 1
            elif isinstance(diff_data, dict):
                count = diff_data.get("count", 0)
                is_covered = diff_data.get("available", False) and count >= 1
            else:
                count = 0
                is_covered = False
            
            if is_covered:
                covered_combinations += 1
                skill_covered += 1
                coverage_by_difficulty[difficulty]["covered"] += 1
        
        coverage_by_skill[skill_id] = {
            "total": skill_total,
            "covered": skill_covered,
            "pct": (skill_covered / skill_total * 100) if skill_total > 0 else 0
        }
    
    # Compute overall coverage
    overall_pct = (covered_combinations / total_combinations * 100) if total_combinations > 0 else 0
    
    # Compute difficulty coverage
    for diff in difficulties:
        d = coverage_by_difficulty[diff]
        d["pct"] = (d["covered"] / d["total"] * 100) if d["total"] > 0 else 0
    
    return {
        "overall": {
            "total": total_combinations,
            "covered": covered_combinations,
            "pct": overall_pct
        },
        "by_skill": coverage_by_skill,
        "by_difficulty": coverage_by_difficulty
    }


def run_coverage_eval() -> Dict[str, Any]:
    """
    Run coverage evaluation.
    
    Returns:
        Evaluation result with pass/fail status and metrics.
    """
    config = load_config()
    min_pct = config.get("thresholds", {}).get("min_pct", 0.95) * 100
    
    try:
        # Get skills manifest
        manifest = get_skills_manifest()
        
        # Compute coverage metrics
        metrics = compute_coverage_metrics(manifest)
        
        # Check threshold
        actual_pct = metrics["overall"]["pct"]
        passed = actual_pct >= min_pct
        
        return {
            "eval": "coverage",
            "passed": passed,
            "metrics": metrics,
            "thresholds": {
                "min_pct": min_pct
            },
            "message": f"Coverage {actual_pct:.1f}% {'≥' if passed else '<'} {min_pct:.1f}% threshold"
        }
        
    except Exception as e:
        return {
            "eval": "coverage",
            "passed": False,
            "error": str(e),
            "message": f"Coverage evaluation failed: {e}"
        }


def main():
    """CLI entry point."""
    result = run_coverage_eval()
    
    # Print result
    print(json.dumps(result, indent=2))
    
    # Exit with appropriate code
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()