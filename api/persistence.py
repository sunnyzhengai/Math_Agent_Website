"""
Atomic JSON persistence for mastery state.

Single-process safe: atomic writes prevent corruption on crash.
Multi-process: not thread-safe across processes; upgrade to SQLite/Redis for production multi-worker.
"""

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional


def _ensure_parent(path: Path) -> None:
    """Ensure parent directory exists."""
    path.parent.mkdir(parents=True, exist_ok=True)


def load_json(path: str) -> Optional[Dict[str, Any]]:
    """
    Load JSON if file exists and is valid.
    
    Returns None on any error (fail-open):
      - File doesn't exist
      - JSON parse error
      - Read permission error
    """
    p = Path(path)
    if not p.exists():
        return None

    try:
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None  # fail-open


def save_json_atomic(path: str, data: Dict[str, Any]) -> bool:
    """
    Atomic write: write to temp file then os.replace().
    
    Safe against crashes mid-write; prevents corruption.
    
    Returns True on success, False on error (fail-open).
    """
    p = Path(path)
    tmp_name = None

    try:
        _ensure_parent(p)

        with tempfile.NamedTemporaryFile(
            "w",
            delete=False,
            dir=str(p.parent),
            encoding="utf-8",
            suffix=".tmp",
        ) as tmp:
            json.dump(data, tmp, ensure_ascii=False, separators=(",", ":"))
            tmp.flush()
            os.fsync(tmp.fileno())
            tmp_name = tmp.name

        # Atomic replace
        os.replace(tmp_name, p)
        return True

    except Exception:
        # Clean up temp file on error
        try:
            if tmp_name and os.path.exists(tmp_name):
                os.remove(tmp_name)
        except Exception:
            pass
        return False
