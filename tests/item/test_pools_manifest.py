# tests/item/test_pools_manifest.py

import sys
import os
import pytest

# Add parent directories to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from fastapi.testclient import TestClient

try:
    from api.server import app
except (ImportError, ModuleNotFoundError):
    import importlib.util
    spec = importlib.util.spec_from_file_location("api.server", 
        os.path.join(os.path.dirname(__file__), '../../api/server.py'))
    server_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(server_module)
    app = server_module.app

from engine.templates import SKILL_TEMPLATES


client = TestClient(app)


def test_manifest_matches_templates_and_integrity():
    """Confirm /skills/manifest truth = SKILL_TEMPLATES truth.
    
    Also verifies each item has exactly 4 choices and valid solution index.
    """
    # 1) fetch manifest from server (source of truth for the web UI)
    r = client.get("/skills/manifest")
    assert r.status_code == 200, "/skills/manifest must exist and return 200"
    manifest = r.json()
    assert isinstance(manifest, dict) and manifest, "manifest must be a non-empty dict"

    # 2) derive expected counts from SKILL_TEMPLATES + check integrity
    expected = {}
    for skill_id, by_diff in SKILL_TEMPLATES.items():
        expected[skill_id] = {}
        for diff, items in by_diff.items():
            # integrity: choices=4, solution index in 0..3
            for idx, q in enumerate(items):
                assert "choices" in q and isinstance(q["choices"], list) and len(q["choices"]) == 4, \
                    f"{skill_id}/{diff} item {idx} must have exactly 4 choices"
                
                sol = q.get("solution")
                assert isinstance(sol, int) and 0 <= sol <= 3, \
                    f"{skill_id}/{diff} item {idx} solution must be 0..3"
            
            expected[skill_id][diff] = len(items)

    # 3) compare shape + counts
    # (skills present)
    assert set(manifest.keys()) == set(expected.keys()), \
        "manifest and templates must list the same skills"

    # (diff keys + counts per skill)
    for skill_id in expected:
        assert set(manifest[skill_id].keys()) == set(expected[skill_id].keys()), \
            f"manifest diffs for {skill_id} must match template diffs"
        
        for diff in expected[skill_id]:
            assert manifest[skill_id][diff] == expected[skill_id][diff], \
                f"pool size mismatch for {skill_id}/{diff}: " \
                f"manifest={manifest[skill_id][diff]} vs templates={expected[skill_id][diff]}"
