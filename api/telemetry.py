"""
Telemetry logging utility for Math Agent.

Captures generate/grade/cycle_reset events to append-only JSONL.
Features: async-safe writes, size-based rotation, sampling, stem hashing, redaction.

Configuration via environment variables:
  TELEMETRY_ENABLED: bool (default true)
  TELEMETRY_PATH: str (default logs/telemetry.jsonl)
  TELEMETRY_MAX_BYTES: int (default 5242880 / 5MB)
  TELEMETRY_SAMPLE_RATE: float 0-1.0 (default 1.0)
  SERVER_ID: str (default local-dev)
  APP_VERSION: str (default 0.1.0)

Note on multi-process: rotation uses asyncio.Lock (single-process safe).
For multi-worker deployment, add file locking (e.g., fcntl/portalocker).
"""

import os
import json
import time
import hashlib
import random
import asyncio
from pathlib import Path
from typing import Dict, Any


class TelemetryLogger:
    """
    Async-safe JSONL logger with rotation, sampling, and redaction.
    
    Design: fail-silently. Any I/O error is logged to stderr but does not raise.
    Note: uses sync file I/O (acceptable for dev/MVP; upgrade to aiofiles if traffic grows).
    """
    
    VALID_EVENTS = {"generate", "grade", "cycle_reset"}
    
    def __init__(self):
        # Configuration from environment with validation
        self.enabled = os.getenv("TELEMETRY_ENABLED", "true").lower() == "true"
        self.path = Path(os.getenv("TELEMETRY_PATH", "logs/telemetry.jsonl"))
        
        # Validate and clamp max_bytes
        try:
            max_bytes = int(os.getenv("TELEMETRY_MAX_BYTES", str(5 * 1024 * 1024)))
            self.max_bytes = max(1, max_bytes)  # At least 1 byte
        except ValueError:
            self.max_bytes = 5 * 1024 * 1024
        
        # Validate and clamp sample_rate to [0.0, 1.0]
        try:
            sr = float(os.getenv("TELEMETRY_SAMPLE_RATE", "1.0"))
            self.sample_rate = max(0.0, min(1.0, sr))
        except ValueError:
            self.sample_rate = 1.0
        
        self.server_id = os.getenv("SERVER_ID", "local-dev")
        self.app_version = os.getenv("APP_VERSION", "0.1.0")
        
        # Thread/async safety
        self._lock = asyncio.Lock()
        
        # Ensure directory exists
        self.path.parent.mkdir(parents=True, exist_ok=True)

    async def log_event(self, event: str, **kwargs) -> None:
        """
        Log an event as a JSON line.
        
        Args:
            event: event type ("generate", "grade", "cycle_reset")
            **kwargs: event-specific fields (stem will be hashed automatically)
                     Unknown keys are dropped by _redact() based on event type allowlist.
        
        Never raises; logs errors to stderr instead.
        """
        if not self.enabled:
            return
        
        # Validate event type early
        if event not in self.VALID_EVENTS:
            print(f"[telemetry] invalid event type: {event}", file=__import__("sys").stderr)
            return
        
        # Random sampling (not time-correlated)
        if self.sample_rate < 1.0 and random.random() > self.sample_rate:
            return
        
        try:
            # Build base event with metadata
            base = {
                "event": event,
                "ts": time.time(),
                "server_id": self.server_id,
                "version": self.app_version,
            }
            payload = dict(kwargs)
            
            # --- Transform stem → stem_hash BEFORE filtering ---
            # This ensures stem is never stored plaintext
            if "stem" in payload and "stem_hash" not in payload:
                payload["stem_hash"] = self.hash_stem(payload.pop("stem"))
            
            # Merge and redact to allowed fields
            log_entry = self._redact({**base, **payload})
            
            # Async-safe append + rotate
            async with self._lock:
                await self._append_line(log_entry)
                await self._rotate_if_needed()
        except Exception as e:
            # Fail-open: print to stderr but don't raise
            print(f"[telemetry] error: {e}", file=__import__("sys").stderr)

    def hash_stem(self, stem: str) -> str:
        """Hash a stem for privacy (no plaintext storage)."""
        return f"sha1:{hashlib.sha1(stem.encode()).hexdigest()}"

    def _redact(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove or transform sensitive fields.
        
        Rules:
        - Keep only fields in the whitelist for this event type
        - Drop anything else (e.g., solution_text, student_name)
        - stem should already be converted to stem_hash before calling this
        """
        allowed_fields = {
            "generate": {
                "event", "ts", "session_id", "mode", "skill_id", "difficulty",
                "item_id", "stem_hash", "choice_ids", "latency_ms", "server_id", "version"
            },
            "grade": {
                "event", "ts", "session_id", "skill_id", "difficulty",
                "item_id", "choice_id", "correct", "solution_choice_id", "latency_ms", "server_id", "version"
            },
            "cycle_reset": {
                "event", "ts", "session_id", "skill_id", "difficulty", "server_id", "version"
            },
        }
        
        allowed = allowed_fields.get(event.get("event"), set())
        return {k: v for k, v in event.items() if k in allowed}

    async def _append_line(self, event: Dict[str, Any]) -> None:
        """
        Append a JSON line to the log file with UTF-8 encoding.
        
        Pre-checks file size to minimize unnecessary rotations.
        """
        line = json.dumps(event, ensure_ascii=False) + "\n"
        
        # Pre-rotation check: if appending would exceed limit, rotate first
        try:
            if self.path.exists():
                current_size = self.path.stat().st_size
                if current_size + len(line.encode("utf-8")) > self.max_bytes:
                    await self._rotate_if_needed()
        except Exception:
            pass  # Ignore pre-check errors; try to write anyway
        
        # Write with explicit encoding (UTF-8, no line-ending translation)
        with open(self.path, "a", encoding="utf-8", newline="\n") as f:
            f.write(line)

    async def _rotate_if_needed(self) -> None:
        """
        Check file size and rotate if > max_bytes.
        
        Rotated files move to logs/telemetry.rotate/telemetry.TIMESTAMP.jsonl
        
        Note: single-process only (asyncio.Lock). Multi-worker deployment
        requires file locking (fcntl/portalocker).
        """
        try:
            if not self.path.exists():
                return
            
            file_size = self.path.stat().st_size
            if file_size <= self.max_bytes:
                return
            
            # Rotation needed
            rotate_dir = self.path.parent / "telemetry.rotate"
            rotate_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate rotated filename with timestamp
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            rotated_path = rotate_dir / f"telemetry.{timestamp}.jsonl"
            
            # Move current file to rotated location
            self.path.rename(rotated_path)
        except Exception as e:
            # Fail-open: don't crash if rotation fails
            print(f"[telemetry] rotation error: {e}", file=__import__("sys").stderr)


# Global singleton
_logger = TelemetryLogger()


# Public API
async def log_event(event: str, **kwargs) -> None:
    """Log an event. This is the main entry point."""
    await _logger.log_event(event, **kwargs)


def hash_stem(stem: str) -> str:
    """Hash a stem for privacy."""
    return _logger.hash_stem(stem)
