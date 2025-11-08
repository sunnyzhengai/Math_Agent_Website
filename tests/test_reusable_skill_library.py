"""
Acceptance tests for Reusable Skill Library.

Tests the foundation agent pattern for composable, transferable skills
based on Linxi Fan's (NVIDIA) approach.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agentic.agents.reusable_skill_library import (
    ReusableSkillLibrary,
    SkillAtomType,
    SkillAtom,
    SkillMolecule,
    CapabilityModule,
    ParseEquationCapability,
    ExtractVertexCapability,
    ComputeDiscriminantCapability,
    ClassifyEquationCapability,
    ExplainStepsCapability
)


def run_tests():
    print("="*70)
    print("REUSABLE SKILL LIBRARY ACCEPTANCE TESTS")
    print("="*70)
    print()

    # Test 1: Initialize library
    print("Testing library initialization...")
    library = ReusableSkillLibrary(library_dir="./test_skill_library")
    assert library is not None
    assert len(library.capabilities) == 5  # Core capabilities registered
    print(f"✓ Library initialized")
    print(f"  Core capabilities: {len(library.capabilities)}\n")

    # Test 2: Core capabilities registered
    print("Testing core capability registration...")
    expected_capabilities = [
        "parse_equation",
        "extract_vertex",
        "compute_discriminant",
        "classify_equation",
        "explain_steps"
    ]
    for cap_id in expected_capabilities:
        assert cap_id in library.capabilities
    print(f"✓ Core capabilities registered: {len(expected_capabilities)}")
    for cap in expected_capabilities:
        print(f"  • {cap}")
    print()

    # Test 3: Execute parse capability
    print("Testing parse equation capability...")
    parse_cap = library.capabilities["parse_equation"]
    result = parse_cap.execute({"equation": "y = (x - 3)^2 + 2"})
    assert result["parsed"] == True
    assert result["form"] == "vertex"
    assert result["h"] == 3
    assert result["k"] == 2
    print(f"✓ Parse capability working")
    print(f"  Equation: y = (x - 3)^2 + 2")
    print(f"  Parsed: form={result['form']}, h={result['h']}, k={result['k']}\n")

    # Test 4: Execute extract vertex capability
    print("Testing extract vertex capability...")
    extract_cap = library.capabilities["extract_vertex"]
    result = extract_cap.execute({
        "parsed_equation": {
            "form": "vertex",
            "h": 3,
            "k": 2
        }
    })
    assert result["extracted"] == True
    assert result["vertex"] == (3, 2)
    print(f"✓ Extract vertex working")
    print(f"  Vertex: {result['vertex']}\n")

    # Test 5: Execute discriminant capability
    print("Testing compute discriminant capability...")
    disc_cap = library.capabilities["compute_discriminant"]
    result = disc_cap.execute({
        "parsed_equation": {
            "form": "standard",
            "a": 1,
            "b": -5,
            "c": 6
        }
    })
    assert result["computed"] == True
    assert result["discriminant"] == 1  # (-5)^2 - 4(1)(6) = 25 - 24 = 1
    assert result["num_roots"] == 2
    print(f"✓ Compute discriminant working")
    print(f"  For ax² + bx + c with a=1, b=-5, c=6:")
    print(f"  Discriminant: {result['discriminant']}")
    print(f"  Number of roots: {result['num_roots']}\n")

    # Test 6: Execute classify capability
    print("Testing classify equation capability...")
    classify_cap = library.capabilities["classify_equation"]
    result = classify_cap.execute({
        "parsed_equation": {
            "parsed": True,
            "form": "vertex",
            "a": 2,
            "h": 3,
            "k": 1
        }
    })
    assert result["classified"] == True
    assert result["opens"] == "upward"
    assert result["stretched"] == True
    print(f"✓ Classify capability working")
    print(f"  Opens: {result['opens']}")
    print(f"  Stretched: {result['stretched']}\n")

    # Test 7: Execute explain capability
    print("Testing explain steps capability...")
    explain_cap = library.capabilities["explain_steps"]
    result = explain_cap.execute({
        "skill_type": "vertex",
        "parsed_equation": {
            "form": "vertex",
            "a": 1,
            "h": 3,
            "k": 2
        }
    })
    assert result["explained"] == True
    assert len(result["steps"]) == 4
    print(f"✓ Explain capability working")
    print(f"  Steps generated: {len(result['steps'])}")
    for i, step in enumerate(result["steps"], 1):
        print(f"    {i}. {step[:60]}...")
    print()

    # Test 8: Capability chain execution
    print("Testing capability chain execution...")
    result = library.execute_capability_chain(
        capability_ids=["parse_equation", "extract_vertex", "classify_equation"],
        initial_context={"equation": "y = 2(x - 4)^2 + 5"}
    )
    assert result.get("parsed") == True
    assert result.get("extracted") == True
    assert result.get("classified") == True
    assert result["vertex"] == (4, 5)
    print(f"✓ Capability chain working")
    print(f"  Chain: parse → extract → classify")
    print(f"  Final vertex: {result['vertex']}")
    print(f"  Classification: {result.get('opens')}\n")

    # Test 9: Register custom atom
    print("Testing custom atom registration...")

    def compute_axis_of_symmetry(context):
        vertex = context.get("vertex", (0, 0))
        return {"axis_of_symmetry": f"x = {vertex[0]}"}

    library.register_atom(
        atom_id="compute_aos",
        atom_type=SkillAtomType.COMPUTE,
        description="Compute axis of symmetry",
        inputs=["vertex"],
        outputs=["axis_of_symmetry"],
        implementation=compute_axis_of_symmetry,
        difficulty=1
    )

    assert "compute_aos" in library.atoms
    print(f"✓ Custom atom registered")
    print(f"  Atom ID: compute_aos")
    print(f"  Type: COMPUTE\n")

    # Test 10: Register molecule
    print("Testing molecule registration...")
    library.register_molecule(
        molecule_id="vertex_analysis",
        description="Complete vertex analysis workflow",
        atoms=["compute_aos"],  # Reference our custom atom
        skill_domain="quadratic",
        difficulty=2
    )

    assert "vertex_analysis" in library.molecules
    assert "quadratic" in library.skill_taxonomy
    print(f"✓ Molecule registered")
    print(f"  Molecule: vertex_analysis")
    print(f"  Domain: quadratic\n")

    # Test 11: Execute molecule
    print("Testing molecule execution...")
    result = library.execute_molecule(
        molecule_id="vertex_analysis",
        input_data={"vertex": (3, 2)}
    )
    assert result["success"] == True
    assert "axis_of_symmetry" in result["result"]
    print(f"✓ Molecule execution working")
    print(f"  Input vertex: (3, 2)")
    print(f"  Output: {result['result']['axis_of_symmetry']}\n")

    # Test 12: Agent composition
    print("Testing agent composition...")
    agent_spec = library.compose_agent(
        agent_name="QuadraticAnalyzer",
        capabilities=["parse_equation", "extract_vertex", "classify_equation"],
        skill_focus="quadratic"
    )
    assert agent_spec["success"] == True
    assert len(agent_spec["capabilities"]) == 3
    assert len(agent_spec["capability_modules"]) == 3
    print(f"✓ Agent composition working")
    print(f"  Agent: {agent_spec['agent_name']}")
    print(f"  Capabilities: {len(agent_spec['capabilities'])}")
    print(f"  Composition ID: {agent_spec['composition_id']}\n")

    # Test 13: Agent composition with missing capability
    print("Testing agent composition error handling...")
    agent_spec = library.compose_agent(
        agent_name="BadAgent",
        capabilities=["nonexistent_capability"],
        skill_focus="test"
    )
    assert agent_spec["success"] == False
    assert "error" in agent_spec
    print(f"✓ Error handling working")
    print(f"  Missing capability detected: {agent_spec['error']}\n")

    # Test 14: Domain mapping for transfer learning
    print("Testing domain mapping creation...")
    success = library.create_domain_mapping(
        source_domain="quadratic",
        target_domain="parabola",
        concept_mappings={
            "vertex": "turning_point",
            "axis_of_symmetry": "reflection_line",
            "coefficient_a": "stretch_factor"
        }
    )
    assert success == True
    assert "quadratic->parabola" in library.domain_mappings
    print(f"✓ Domain mapping created")
    print(f"  Mapped concepts: 3\n")

    # Test 15: Transfer skill to new domain
    print("Testing skill transfer...")
    success = library.transfer_skill(
        source_molecule_id="vertex_analysis",
        target_domain="parabola",
        new_molecule_id="parabola_analysis"
    )
    assert success == True
    assert "parabola_analysis" in library.molecules
    assert "parabola" in library.skill_taxonomy
    print(f"✓ Skill transfer working")
    print(f"  Transferred: vertex_analysis → parabola_analysis")
    print(f"  New domain: parabola\n")

    # Test 16: Register more molecules for pattern analysis
    print("Testing shared pattern identification...")

    # Register atoms
    def find_roots(context):
        return {"roots": "calculated"}

    def graph_parabola(context):
        return {"graph": "rendered"}

    library.register_atom(
        atom_id="find_roots",
        atom_type=SkillAtomType.COMPUTE,
        description="Find roots",
        inputs=["equation"],
        outputs=["roots"],
        implementation=find_roots,
        difficulty=3
    )

    library.register_atom(
        atom_id="graph_parabola",
        atom_type=SkillAtomType.VISUALIZE,
        description="Graph parabola",
        inputs=["equation"],
        outputs=["graph"],
        implementation=graph_parabola,
        difficulty=2
    )

    # Register molecules that share atoms
    library.register_molecule(
        molecule_id="complete_square",
        description="Complete the square",
        atoms=["compute_aos", "find_roots"],
        skill_domain="quadratic",
        difficulty=4
    )

    library.register_molecule(
        molecule_id="analyze_parabola",
        description="Full parabola analysis",
        atoms=["compute_aos", "find_roots", "graph_parabola"],
        skill_domain="quadratic",
        difficulty=5
    )

    # Identify shared patterns
    patterns = library.identify_shared_patterns([
        "vertex_analysis",
        "complete_square",
        "analyze_parabola"
    ])

    assert len(patterns) > 0
    # compute_aos is shared by all three
    shared_atom_ids = [p["atom_id"] for p in patterns]
    assert "compute_aos" in shared_atom_ids

    print(f"✓ Shared pattern identification working")
    print(f"  Analyzed skills: 3")
    print(f"  Shared atoms: {len(patterns)}")
    for pattern in patterns:
        print(f"    • {pattern['atom_id']} ({pattern['type']})")
    print()

    # Test 17: Library statistics
    print("Testing library statistics...")
    stats = library.get_library_stats()
    assert stats["total_atoms"] > 0
    assert stats["total_molecules"] > 0
    assert stats["total_capabilities"] == 5
    assert stats["compositions_created"] > 0
    print(f"✓ Library stats working")
    print(f"  Total atoms: {stats['total_atoms']}")
    print(f"  Total molecules: {stats['total_molecules']}")
    print(f"  Total capabilities: {stats['total_capabilities']}")
    print(f"  Domains: {stats['domains']}")
    print(f"  Compositions created: {stats['compositions_created']}\n")

    # Test 18: Atoms by type
    print("Testing atoms by type categorization...")
    atoms_by_type = stats["atoms_by_type"]
    assert len(atoms_by_type) > 0
    assert "compute" in atoms_by_type
    print(f"✓ Atom categorization working")
    for atom_type, count in atoms_by_type.items():
        print(f"  {atom_type}: {count}")
    print()

    # Test 19: Most used atoms
    print("Testing usage tracking...")
    # Execute molecule to increment usage
    library.execute_molecule("vertex_analysis", {"vertex": (1, 1)})
    library.execute_molecule("complete_square", {})
    library.execute_molecule("analyze_parabola", {})

    stats = library.get_library_stats()
    most_used = stats["most_used_atoms"]
    print(f"✓ Usage tracking working")
    print(f"  Most used atoms:")
    for atom_info in most_used[:3]:
        if atom_info["usage_count"] > 0:
            print(f"    • {atom_info['atom_id']}: {atom_info['usage_count']} uses")
    print()

    # Test 20: Average molecule complexity
    print("Testing complexity metrics...")
    avg_complexity = stats["avg_molecule_complexity"]
    assert avg_complexity > 0
    print(f"✓ Complexity metrics working")
    print(f"  Average molecule difficulty: {avg_complexity:.1f}/5.0\n")

    # Test 21: List capabilities
    print("Testing capability listing...")
    library.list_capabilities()

    # Test 22: List molecules
    print("Testing molecule listing...")
    library.list_molecules()

    # Test 23: Save library state
    print("Testing library persistence...")
    saved = library.save_library("test_snapshot.json")
    assert saved == True
    snapshot_file = Path("./test_skill_library/test_snapshot.json")
    assert snapshot_file.exists()
    print(f"✓ Library saved")
    print(f"  File: {snapshot_file}\n")

    # Test 24: Capability module interface
    print("Testing capability module interface...")

    class CustomCapability(CapabilityModule):
        def get_capability_id(self) -> str:
            return "custom_test"

        def execute(self, context):
            return {"custom_result": "success"}

    custom = CustomCapability()
    library.register_capability(custom)
    assert "custom_test" in library.capabilities

    result = library.capabilities["custom_test"].execute({})
    assert result["custom_result"] == "success"
    print(f"✓ Custom capability interface working\n")

    # Test 25: Atom prerequisites and dependencies
    print("Testing atom dependency tracking...")
    library.register_atom(
        atom_id="advanced_analysis",
        atom_type=SkillAtomType.COMPUTE,
        description="Advanced analysis requiring other atoms",
        inputs=["vertex", "roots"],
        outputs=["analysis"],
        implementation=lambda ctx: {"analysis": "complete"},
        difficulty=5,
        prerequisites=["compute_aos", "find_roots"]
    )

    assert "advanced_analysis" in library.atoms
    assert "advanced_analysis" in library.atom_dependencies
    assert len(library.atom_dependencies["advanced_analysis"]) == 2
    print(f"✓ Dependency tracking working")
    print(f"  Atom: advanced_analysis")
    print(f"  Prerequisites: {list(library.atom_dependencies['advanced_analysis'])}\n")

    # Cleanup
    import shutil
    shutil.rmtree("./test_skill_library", ignore_errors=True)

    print("="*70)
    print("ALL ACCEPTANCE TESTS PASSED ✓")
    print("="*70)
    print()

    # Final summary
    print("REUSABLE SKILL LIBRARY SUMMARY")
    print("="*70)
    final_stats = library.get_library_stats()
    print(f"📊 Library Composition:")
    print(f"   Atoms: {final_stats['total_atoms']}")
    print(f"   Molecules: {final_stats['total_molecules']}")
    print(f"   Capabilities: {final_stats['total_capabilities']}")
    print(f"   Domains: {final_stats['domains']}")
    print(f"   Domain mappings: {final_stats['domain_mappings']}")
    print(f"   Agent compositions: {final_stats['compositions_created']}")
    print()
    print(f"📈 Usage Metrics:")
    print(f"   Avg molecule complexity: {final_stats['avg_molecule_complexity']:.1f}/5.0")
    print()
    print(f"🎯 Capability Categories:")
    for atom_type, count in final_stats['atoms_by_type'].items():
        print(f"   {atom_type}: {count} atoms")
    print()


if __name__ == "__main__":
    run_tests()
