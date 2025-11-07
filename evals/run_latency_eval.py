#!/usr/bin/env python3
"""
Latency evaluation runner.

Analyzes telemetry logs to compute p50/p90 latency metrics for API endpoints.
Compares against configured thresholds.

Usage:
  python3 -m evals.run_latency_eval
"""

import json
import yaml
import pathlib
import statistics
from typing import Dict, Any, List
import sys


def load_config() -> Dict[str, Any]:
    """Load configuration from latency_eval.yaml."""
    config_path = pathlib.Path(__file__).parent / "latency_eval.yaml"
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


def compute_latency_metrics(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compute latency metrics from telemetry events.
    
    Args:
        events: List of telemetry events
        
    Returns:
        Dict with latency metrics by event type
    """
    # Group latencies by event type
    latencies = {
        "generate": [],
        "grade": []
    }
    
    for event in events:
        event_type = event.get("event")
        latency_ms = event.get("latency_ms")
        
        if event_type in latencies and latency_ms is not None:
            try:
                latencies[event_type].append(float(latency_ms))
            except (ValueError, TypeError):
                continue
    
    # Compute percentiles
    metrics = {}
    
    for event_type, values in latencies.items():
        if not values:
            metrics[event_type] = {
                "count": 0,
                "p50_ms": None,
                "p90_ms": None,
                "min_ms": None,
                "max_ms": None,
                "mean_ms": None
            }
        else:
            sorted_values = sorted(values)
            metrics[event_type] = {
                "count": len(values),
                "p50_ms": statistics.quantiles(sorted_values, n=100)[49] if len(values) >= 2 else sorted_values[0],
                "p90_ms": statistics.quantiles(sorted_values, n=100)[89] if len(values) >= 2 else sorted_values[0],
                "min_ms": min(values),
                "max_ms": max(values),
                "mean_ms": statistics.mean(values)
            }
    
    return metrics


def check_latency_thresholds(metrics: Dict[str, Any], thresholds: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check latency metrics against thresholds.
    
    Args:
        metrics: Computed latency metrics
        thresholds: Threshold configuration
        
    Returns:
        Dict with pass/fail results per metric
    """
    results = {}
    overall_pass = True
    
    for event_type, event_metrics in metrics.items():
        if event_type not in thresholds:
            continue
            
        event_thresholds = thresholds[event_type]
        event_results = {}
        
        # Check p50 threshold
        p50_ms = event_metrics.get("p50_ms")
        p50_threshold = event_thresholds.get("p50_ms")
        
        if p50_ms is not None and p50_threshold is not None:
            p50_pass = p50_ms <= p50_threshold
            event_results["p50"] = {
                "actual_ms": p50_ms,
                "threshold_ms": p50_threshold,
                "passed": p50_pass
            }
            if not p50_pass:
                overall_pass = False
        
        # Check p90 threshold
        p90_ms = event_metrics.get("p90_ms")
        p90_threshold = event_thresholds.get("p90_ms")
        
        if p90_ms is not None and p90_threshold is not None:
            p90_pass = p90_ms <= p90_threshold
            event_results["p90"] = {
                "actual_ms": p90_ms,
                "threshold_ms": p90_threshold,
                "passed": p90_pass
            }
            if not p90_pass:
                overall_pass = False
        
        results[event_type] = event_results
    
    results["overall"] = {"passed": overall_pass}
    return results


def run_latency_eval() -> Dict[str, Any]:
    """
    Run latency evaluation.
    
    Returns:
        Evaluation result with pass/fail status and latency metrics.
    """
    config = load_config()
    
    try:
        # Find telemetry log file
        log_path = pathlib.Path(__file__).parent.parent / "logs" / "telemetry.jsonl"
        
        # Parse telemetry events
        events = parse_telemetry_logs(log_path)
        
        if not events:
            return {
                "eval": "latency",
                "passed": False,
                "error": f"No telemetry events found in {log_path}",
                "message": "Latency eval requires telemetry data"
            }
        
        # Compute metrics
        metrics = compute_latency_metrics(events)
        
        # Check thresholds
        thresholds = config.get("thresholds", {})
        threshold_results = check_latency_thresholds(metrics, thresholds)
        
        overall_passed = threshold_results.get("overall", {}).get("passed", False)
        
        return {
            "eval": "latency",
            "passed": overall_passed,
            "metrics": metrics,
            "thresholds": thresholds,
            "threshold_results": threshold_results,
            "total_events": len(events),
            "message": f"Latency eval: {'passed' if overall_passed else 'failed'} threshold checks"
        }
        
    except Exception as e:
        return {
            "eval": "latency",
            "passed": False,
            "error": str(e),
            "message": f"Latency evaluation failed: {e}"
        }


def main():
    """CLI entry point."""
    result = run_latency_eval()
    
    # Print result
    print(json.dumps(result, indent=2))
    
    # Exit with appropriate code
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()