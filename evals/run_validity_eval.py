#!/usr/bin/env python3
"""
Validity evaluation runner.

Samples generate events from telemetry, regenerates items, and validates them.
Ensures that the question generation pipeline produces valid items consistently.

Usage:
  python3 -m evals.run_validity_eval
"""

import json
import yaml
import pathlib
import random
from typing import Dict, Any, List
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))


def load_config() -> Dict[str, Any]:
    """Load configuration from validity_eval.yaml."""
    config_path = pathlib.Path(__file__).parent / "validity_eval.yaml"
    return yaml.safe_load(config_path.read_text())


def parse_telemetry_logs(log_path: pathlib.Path) -> List[Dict[str, Any]]:
    """
    Parse telemetry logs from JSONL file.
    
    Args:
        log_path: Path to the telemetry log file
        
    Returns:
        List of parsed telemetry events
    """
    events = []
    
    if not log_path.exists():
        return events
    
    try:
        with open(log_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        event = json.loads(line)
                        events.append(event)
                    except json.JSONDecodeError:
                        continue  # Skip malformed lines
    except Exception:
        pass  # Return empty list on error
    
    return events


def sample_generate_events(events: List[Dict[str, Any]], sample_size: int = 50) -> List[Dict[str, Any]]:
    """
    Sample generate events from telemetry for validation.
    
    Args:
        events: List of all telemetry events
        sample_size: Number of events to sample
        
    Returns:
        List of sampled generate events
    """
    generate_events = [e for e in events if e.get("event") == "generate"]
    
    if not generate_events:
        return []
    
    # Sample random events, or all if fewer than sample_size
    sample_size = min(sample_size, len(generate_events))
    return random.sample(generate_events, sample_size)


def validate_item_wrapper(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate a generated item using the engine validator.
    
    Args:
        item: Generated item to validate
        
    Returns:
        Dict with validation result
    """
    try:
        from engine.validators import validate_item
        
        # Run validation (returns tuple: (valid, error_message))
        valid, error_message = validate_item(item)
        
        return {
            "valid": valid,
            "errors": [error_message] if error_message else [],
            "error": None
        }
        
    except Exception as e:
        return {
            "valid": False,
            "errors": [],
            "error": str(e)
        }


def revalidate_sample(sample_events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Regenerate and revalidate items from sample events.
    
    Args:
        sample_events: List of generate events to revalidate
        
    Returns:
        Dict with revalidation results
    """
    from engine.templates import generate_item
    
    results = []
    valid_count = 0
    error_count = 0
    
    for event in sample_events:
        skill_id = event.get("skill_id")
        difficulty = event.get("difficulty") 
        
        # Extract seed from item_id (deterministic regeneration)
        # For now, use a fixed seed to test validation
        seed = 42
        
        result = {
            "event": event,
            "skill_id": skill_id,
            "difficulty": difficulty,
            "seed": seed
        }
        
        try:
            # Regenerate item
            item = generate_item(skill_id, difficulty, seed=seed)
            
            # Validate regenerated item
            validation = validate_item_wrapper(item)
            
            result.update({
                "regenerated": True,
                "validation": validation,
                "item_valid": validation.get("valid", False)
            })
            
            if validation.get("valid", False):
                valid_count += 1
            
        except Exception as e:
            error_count += 1
            result.update({
                "regenerated": False,
                "validation": {"valid": False, "errors": [], "error": str(e)},
                "item_valid": False,
                "generation_error": str(e)
            })
        
        results.append(result)
    
    total_count = len(sample_events)
    validity_pct = (valid_count / total_count * 100) if total_count > 0 else 0
    
    return {
        "total_sampled": total_count,
        "valid_items": valid_count,
        "invalid_items": total_count - valid_count - error_count,
        "generation_errors": error_count,
        "validity_pct": validity_pct,
        "results": results
    }


def run_validity_eval() -> Dict[str, Any]:
    """
    Run validity evaluation.
    
    Returns:
        Evaluation result with pass/fail status and validity metrics.
    """
    config = load_config()
    min_pct = config.get("thresholds", {}).get("min_pct", 0.95) * 100
    
    try:
        # Find telemetry log file
        log_path = pathlib.Path(__file__).parent.parent / "logs" / "telemetry.jsonl"
        
        # Parse telemetry events
        events = parse_telemetry_logs(log_path)
        
        if not events:
            return {
                "eval": "validity",
                "passed": False,
                "error": f"No telemetry events found in {log_path}",
                "message": "Validity eval requires telemetry data"
            }
        
        # Sample generate events
        sample_events = sample_generate_events(events, sample_size=50)
        
        if not sample_events:
            return {
                "eval": "validity",
                "passed": False,
                "error": "No generate events found in telemetry",
                "message": "Validity eval requires generate events"
            }
        
        # Revalidate sample
        validation_results = revalidate_sample(sample_events)
        
        # Check threshold
        actual_pct = validation_results["validity_pct"]
        passed = actual_pct >= min_pct
        
        return {
            "eval": "validity",
            "passed": passed,
            "validation_results": validation_results,
            "thresholds": {
                "min_pct": min_pct
            },
            "total_events": len(events),
            "message": f"Validity {actual_pct:.1f}% {'≥' if passed else '<'} {min_pct:.1f}% threshold"
        }
        
    except Exception as e:
        return {
            "eval": "validity",
            "passed": False,
            "error": str(e),
            "message": f"Validity evaluation failed: {e}"
        }


def main():
    """CLI entry point."""
    result = run_validity_eval()
    
    # Print result
    print(json.dumps(result, indent=2))
    
    # Exit with appropriate code
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()