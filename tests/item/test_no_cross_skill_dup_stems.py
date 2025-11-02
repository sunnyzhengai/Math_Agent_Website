# tests/item/test_no_cross_skill_dup_stems.py

import pytest

from engine.templates import SKILL_TEMPLATES

from tests._utils import norm_stem


def test_no_duplicate_stems_across_pools():
    """Ensure stems remain unique across all skills/difficulties.
    
    Catches copy/paste accidents and ensures learners never see the same
    exact question twice even if they cycle through multiple skills.
    """
    seen = {}
    
    for skill_id, by_diff in SKILL_TEMPLATES.items():
        for diff, items in by_diff.items():
            for i, q in enumerate(items):
                s = norm_stem(q.get("stem", ""))
                
                assert s, f"Empty stem at {skill_id}/{diff} index {i}"
                
                key = (skill_id, diff, i)
                
                if s in seen:
                    prev = seen[s]
                    pytest.fail(
                        f"Duplicate stem between {prev} and {key}:\n"
                        f"  {q.get('stem')!r}"
                    )
                
                seen[s] = key
