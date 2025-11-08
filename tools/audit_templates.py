#!/usr/bin/env python3
"""
Template Audit Tool

Generates a comprehensive report on question template inventory.
Used for prioritizing template expansion in Phase 1.

Reports:
- Template counts per skill/difficulty
- Critical gaps (<5 templates)
- Total coverage across all skills
- Recommendations for expansion priorities
"""

import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.templates import SKILL_TEMPLATES


def audit_templates(output_file: str = None):
    """Audit all question templates and generate report."""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("=" * 70)
    print("QUESTION TEMPLATE AUDIT REPORT")
    print("=" * 70)
    print(f"Generated: {timestamp}\n")

    # Collect statistics
    total_templates = 0
    critical_gaps = []  # <5 templates
    low_coverage = []   # 5-9 templates
    good_coverage = []  # 10+ templates
    
    difficulty_totals = defaultdict(int)
    skill_totals = {}

    # Analyze each skill
    for skill_id in sorted(SKILL_TEMPLATES.keys()):
        print(f"\n📚 {skill_id}")
        print("-" * 70)
        
        skill_total = 0
        skill_breakdown = {}
        
        for difficulty in ["easy", "medium", "hard", "applied"]:
            if difficulty in SKILL_TEMPLATES[skill_id]:
                count = len(SKILL_TEMPLATES[skill_id][difficulty])
                skill_breakdown[difficulty] = count
                skill_total += count
                total_templates += count
                difficulty_totals[difficulty] += count

                # Status indicator
                if count < 5:
                    status = "🔴 CRITICAL"
                    critical_gaps.append((skill_id, difficulty, count))
                elif count < 10:
                    status = "🟡 LOW"
                    low_coverage.append((skill_id, difficulty, count))
                else:
                    status = "🟢 GOOD"
                    good_coverage.append((skill_id, difficulty, count))

                print(f"  {difficulty:10} → {count:3} templates  {status}")
            else:
                print(f"  {difficulty:10} → N/A")
                skill_breakdown[difficulty] = 0

        skill_totals[skill_id] = skill_total
        print(f"  {'TOTAL':10} → {skill_total:3} templates")

    # Summary statistics
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    print(f"\n📊 Overall Statistics:")
    print(f"  Total templates: {total_templates}")
    print(f"  Total skills: {len(SKILL_TEMPLATES)}")
    print(f"  Avg templates per skill: {total_templates / len(SKILL_TEMPLATES):.1f}")
    
    print(f"\n📊 By Difficulty:")
    for difficulty in ["easy", "medium", "hard", "applied"]:
        count = difficulty_totals[difficulty]
        avg = count / len(SKILL_TEMPLATES) if len(SKILL_TEMPLATES) > 0 else 0
        print(f"  {difficulty.capitalize():10} → {count:3} total ({avg:.1f} avg per skill)")

    # Critical issues
    print(f"\n🔴 CRITICAL GAPS (<5 templates): {len(critical_gaps)}")
    if critical_gaps:
        print("  Priority for Phase 1 expansion:")
        for skill, diff, count in sorted(critical_gaps, key=lambda x: x[2])[:10]:
            print(f"    • {skill}:{diff} ({count} templates)")
        if len(critical_gaps) > 10:
            print(f"    ... and {len(critical_gaps) - 10} more")

    print(f"\n🟡 LOW COVERAGE (5-9 templates): {len(low_coverage)}")
    if low_coverage:
        print("  Should expand in Phase 1:")
        for skill, diff, count in sorted(low_coverage, key=lambda x: x[2])[:5]:
            print(f"    • {skill}:{diff} ({count} templates)")

    print(f"\n🟢 GOOD COVERAGE (10+ templates): {len(good_coverage)}")

    # Recommendations
    print("\n" + "=" * 70)
    print("RECOMMENDATIONS")
    print("=" * 70)
    
    print("\n📋 Phase 1 Priorities:")
    print("  1. Fix CRITICAL gaps first (target: 10+ per skill/difficulty)")
    print("  2. Improve LOW coverage areas")
    print("  3. Maintain GOOD coverage areas")
    
    print("\n🎯 Suggested Expansion Order:")
    # Sort by: criticality (fewer templates first), then by usage (popular skills first)
    usage_priority = [
        "quad.graph.vertex",
        "quad.standard.vertex", 
        "quad.roots.factored",
        "quad.solve.by_factoring",
        "quad.solve.by_formula"
    ]
    
    expansion_queue = []
    for skill in usage_priority:
        for diff in ["easy", "medium", "hard", "applied"]:
            if (skill, diff) in [(s, d) for s, d, c in critical_gaps]:
                count = next(c for s, d, c in critical_gaps if s == skill and d == diff)
                expansion_queue.append((skill, diff, count, "CRITICAL"))
    
    for i, (skill, diff, count, priority) in enumerate(expansion_queue[:10], 1):
        needed = 10 - count
        print(f"  {i:2}. {skill}:{diff}")
        print(f"      Current: {count} → Target: 10 (+{needed} needed)")

    print(f"\n💡 Estimated Effort:")
    total_needed = sum(max(0, 10 - count) for _, _, count in critical_gaps + low_coverage)
    print(f"  Templates to write: ~{total_needed}")
    print(f"  At 3 templates/day: ~{total_needed / 3:.0f} days")
    print(f"  At 5 templates/day: ~{total_needed / 5:.0f} days")

    # Save to file if specified
    if output_file:
        # TODO: Generate structured JSON/CSV report
        print(f"\n📝 Report saved to: {output_file}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    output_file = sys.argv[1] if len(sys.argv) > 1 else None
    audit_templates(output_file)
