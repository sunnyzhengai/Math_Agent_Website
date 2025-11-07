#!/usr/bin/env python3
"""
Telemetry completeness evaluation runner.

Validates that telemetry events contain required keys by event type.
Ensures telemetry logging is working correctly and capturing all needed data.

Usage:
  python3 -m evals.run_telemetry_eval
"""

import json
import yaml
import pathlib
from typing import Dict, Any, List, Set
import sys


def load_config() -> Dict[str, Any]:
    """Load configuration from telemetry_eval.yaml."""
    config_path = pathlib.Path(__file__).parent / "telemetry_eval.yaml"
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


def get_required_keys_by_event_type() -> Dict[str, Set[str]]:
    """
    Define required keys for each telemetry event type.
    
    Returns:
        Dict mapping event type to set of required keys
    """
    return {
        "generate": {
            "event", "ts", "server_id", "version", "skill_id", 
            "difficulty", "item_id", "choice_ids", "latency_ms"
        },
        "grade": {
            "event", "ts", "server_id", "version", "skill_id", 
            "difficulty", "item_id", "choice_id", "correct", 
            "solution_choice_id", "latency_ms"
        },
        "cycle_reset": {
            "event", "ts", "server_id", "version", "skill_id", "difficulty"
        }
    }


def validate_telemetry_completeness(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validate telemetry event completeness.
    
    Args:
        events: List of telemetry events
        
    Returns:
        Dict with validation results by event type
    """
    required_keys = get_required_keys_by_event_type()
    
    # Group events by type
    events_by_type = {}
    for event in events:
        event_type = event.get("event", "unknown")
        if event_type not in events_by_type:
            events_by_type[event_type] = []
        events_by_type[event_type].append(event)
    
    # Validate each event type
    results = {}
    overall_pass = True
    
    for event_type, required_keys_set in required_keys.items():
        if event_type not in events_by_type:
            results[event_type] = {
                "count": 0,
                "missing_keys": [],
                "completeness_pct": 0.0,
                "passed": False,
                "message": f"No {event_type} events found"
            }
            overall_pass = False
            continue
        
        type_events = events_by_type[event_type]
        
        # Check key completeness for this event type
        missing_keys_count = {}
        total_events = len(type_events)
        
        for required_key in required_keys_set:
            missing_count = sum(1 for event in type_events if required_key not in event)
            if missing_count > 0:
                missing_keys_count[required_key] = missing_count
        
        # Compute overall completeness percentage
        total_required = len(required_keys_set) * total_events
        total_present = total_required - sum(missing_keys_count.values())
        completeness_pct = (total_present / total_required * 100) if total_required > 0 else 0
        
        # Event type passes if 100% complete
        event_type_pass = completeness_pct >= 100.0
        
        if not event_type_pass:
            overall_pass = False
        
        results[event_type] = {
            "count": total_events,
            "missing_keys": dict(missing_keys_count),
            "completeness_pct": completeness_pct,
            "passed": event_type_pass,
            "message": f"{completeness_pct:.1f}% key completeness"
        }
    
    # Summary
    results["summary"] = {
        "total_events": len(events),
        "event_types_found": len(events_by_type),
        "event_types_expected": len(required_keys),
        "overall_passed": overall_pass
    }
    
    return results


def run_telemetry_eval() -> Dict[str, Any]:
    """
    Run telemetry completeness evaluation.
    
    Returns:
        Evaluation result with pass/fail status and completeness metrics.
    """
    config = load_config()
    
    try:
        # Find telemetry log file
        log_path = pathlib.Path(__file__).parent.parent / "logs" / "telemetry.jsonl"
        
        # Parse telemetry events
        events = parse_telemetry_logs(log_path)
        
        if not events:
            return {
                "eval": "telemetry",
                "passed": False,
                "error": f"No telemetry events found in {log_path}",
                "message": "Telemetry eval requires telemetry data"
            }
        
        # Validate completeness
        validation_results = validate_telemetry_completeness(events)
        
        overall_passed = validation_results.get("summary", {}).get("overall_passed", False)
        
        return {
            "eval": "telemetry",
            "passed": overall_passed,
            "validation": validation_results,
            "total_events": len(events),
            "message": f"Telemetry completeness: {'passed' if overall_passed else 'failed'}"
        }
        
    except Exception as e:
        return {
            "eval": "telemetry",
            "passed": False,
            "error": str(e),
            "message": f"Telemetry evaluation failed: {e}"
        }


def main():
    """CLI entry point."""
    result = run_telemetry_eval()
    
    # Print result
    print(json.dumps(result, indent=2))
    
    # Exit with appropriate code
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()