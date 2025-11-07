#!/usr/bin/env python3
"""
Dataset freshness evaluation runner.

Checks that dataset files are fresh (modified within threshold time).
Useful for ensuring data pipelines are running correctly.

Usage:
  python3 -m evals.run_dataset_freshness_eval
"""

import json
import yaml
import pathlib
import time
import os
from typing import Dict, Any


def load_config() -> Dict[str, Any]:
    """Load configuration from dataset_freshness_eval.yaml."""
    config_path = pathlib.Path(__file__).parent / "dataset_freshness_eval.yaml"
    return yaml.safe_load(config_path.read_text())


def check_file_freshness(file_path: pathlib.Path, max_age_seconds: int) -> Dict[str, Any]:
    """
    Check if a file is fresh (modified within max_age_seconds).
    
    Args:
        file_path: Path to the file to check
        max_age_seconds: Maximum age in seconds
        
    Returns:
        Dict with freshness check results
    """
    try:
        if not file_path.exists():
            return {
                "exists": False,
                "fresh": False,
                "age_seconds": None,
                "error": f"File does not exist: {file_path}"
            }
        
        # Get file modification time
        mtime = file_path.stat().st_mtime
        current_time = time.time()
        age_seconds = current_time - mtime
        
        # Check if fresh
        is_fresh = age_seconds <= max_age_seconds
        
        return {
            "exists": True,
            "fresh": is_fresh,
            "age_seconds": age_seconds,
            "age_hours": age_seconds / 3600,
            "max_age_seconds": max_age_seconds,
            "max_age_hours": max_age_seconds / 3600,
            "mtime": mtime,
            "error": None
        }
        
    except Exception as e:
        return {
            "exists": None,
            "fresh": False,
            "age_seconds": None,
            "error": str(e)
        }


def run_dataset_freshness_eval() -> Dict[str, Any]:
    """
    Run dataset freshness evaluation.
    
    Returns:
        Evaluation result with pass/fail status and file details.
    """
    config = load_config()
    max_age_seconds = config.get("thresholds", {}).get("max_age_seconds", 86400)  # 24h default
    
    try:
        # Get file inputs from config
        file_results = {}
        all_fresh = True
        
        for input_spec in config.get("inputs", []):
            if input_spec.get("type") == "file":
                file_path = pathlib.Path(input_spec.get("path", ""))
                
                # Make path relative to project root if not absolute
                if not file_path.is_absolute():
                    file_path = pathlib.Path(__file__).parent.parent / file_path
                
                result = check_file_freshness(file_path, max_age_seconds)
                file_results[str(file_path)] = result
                
                if not result["fresh"]:
                    all_fresh = False
        
        # Handle case where no file inputs are specified
        if not file_results:
            return {
                "eval": "dataset_freshness",
                "passed": False,
                "error": "No file inputs specified in configuration",
                "message": "Dataset freshness eval requires file inputs"
            }
        
        # Compute overall result
        fresh_count = sum(1 for r in file_results.values() if r["fresh"])
        total_count = len(file_results)
        
        return {
            "eval": "dataset_freshness",
            "passed": all_fresh,
            "files": file_results,
            "summary": {
                "total_files": total_count,
                "fresh_files": fresh_count,
                "stale_files": total_count - fresh_count
            },
            "thresholds": {
                "max_age_seconds": max_age_seconds,
                "max_age_hours": max_age_seconds / 3600
            },
            "message": f"Dataset freshness: {fresh_count}/{total_count} files fresh"
        }
        
    except Exception as e:
        return {
            "eval": "dataset_freshness",
            "passed": False,
            "error": str(e),
            "message": f"Dataset freshness evaluation failed: {e}"
        }


def main():
    """CLI entry point."""
    result = run_dataset_freshness_eval()
    
    # Print result
    print(json.dumps(result, indent=2))
    
    # Exit with appropriate code
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    import sys
    main()