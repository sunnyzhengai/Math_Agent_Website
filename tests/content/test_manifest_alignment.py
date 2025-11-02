"""
Guardrail tests for /skills/manifest endpoint alignment with templates.

Ensures that the manifest accurately reflects the template counts,
so UI pool hints match reality.
"""

import sys
import os
import pytest

# Add repo root to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

try:
    from api.server import app
except (ImportError, ModuleNotFoundError):
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "api.server",
        os.path.join(os.path.dirname(__file__), '../../api/server.py')
    )
    server_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(server_module)
    app = server_module.app

from fastapi.testclient import TestClient
from engine.templates import SKILL_TEMPLATES

client = TestClient(app)


def test_manifest_endpoint_exists():
    """The /skills/manifest endpoint must exist and return 200."""
    r = client.get("/skills/manifest")
    assert r.status_code == 200, "GET /skills/manifest must return 200"
    assert isinstance(r.json(), dict), "/skills/manifest must return a dict"


def test_manifest_counts_match_templates():
    """Manifest item counts must match SKILL_TEMPLATES exactly."""
    r = client.get("/skills/manifest")
    assert r.status_code == 200
    
    manifest = r.json()
    
    # Check each skill
    for skill, diffs in SKILL_TEMPLATES.items():
        assert skill in manifest, f"Skill {skill} missing from manifest"
        
        # Check each difficulty
        for diff, items in diffs.items():
            expected_count = len(items)
            actual_count = manifest[skill].get(diff)
            
            assert actual_count is not None, (
                f"Difficulty {diff} missing from manifest for {skill}"
            )
            assert actual_count == expected_count, (
                f"Manifest mismatch for {skill}:{diff}: "
                f"expected {expected_count}, got {actual_count}"
            )


def test_manifest_no_extra_skills():
    """Manifest must not contain skills not in SKILL_TEMPLATES."""
    r = client.get("/skills/manifest")
    assert r.status_code == 200
    
    manifest = r.json()
    template_skills = set(SKILL_TEMPLATES.keys())
    manifest_skills = set(manifest.keys())
    
    extra = manifest_skills - template_skills
    assert not extra, (
        f"Manifest contains extra skills not in SKILL_TEMPLATES: {extra}"
    )


def test_manifest_structure():
    """Manifest must be well-formed: dict[str, dict[str, int]]."""
    r = client.get("/skills/manifest")
    assert r.status_code == 200
    
    manifest = r.json()
    
    for skill, diffs in manifest.items():
        assert isinstance(skill, str), f"Skill ID must be string, got {type(skill)}"
        assert isinstance(diffs, dict), f"Skill {skill} diffs must be dict"
        
        for diff, count in diffs.items():
            assert isinstance(diff, str), f"Difficulty must be string, got {type(diff)}"
            assert isinstance(count, int), f"Count must be int, got {type(count)}"
            assert count > 0, f"Count must be positive for {skill}:{diff}"
