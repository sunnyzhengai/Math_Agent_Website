"""
Reusable Skill Library: Foundation for composable, transferable learning agents.

Implements Linxi Fan's (NVIDIA) Foundation Agents pattern:
- Skill decomposition into atomic, reusable components
- Agent composition from capability modules
- Transfer learning across mathematical domains
- Shared knowledge base for rapid skill expansion

This enables:
- Building new skills from existing components (DRY principle)
- Rapid expansion from 9 skills to 100+ without rewriting
- Knowledge transfer between related skills
- Maintainable, modular agent architecture

Philosophy: Instead of building monolithic agents for each skill,
decompose into atoms that can be recombined in novel ways.
"""

from typing import Dict, List, Any, Optional, NamedTuple, Callable, Set
from enum import Enum
from abc import ABC, abstractmethod
import json
from pathlib import Path


# ========================================================================
# SKILL ATOMS - Smallest reusable units
# ========================================================================

class SkillAtomType(Enum):
    """Types of atomic skill components."""
    PARSE = "parse"                      # Parse input (equation, expression)
    EXTRACT = "extract"                  # Extract specific values (coefficients, etc.)
    TRANSFORM = "transform"              # Transform representation (standard→vertex)
    COMPUTE = "compute"                  # Compute values (discriminant, etc.)
    CLASSIFY = "classify"                # Classify types (linear, quadratic, etc.)
    VALIDATE = "validate"                # Validate correctness
    EXPLAIN = "explain"                  # Explain steps
    VISUALIZE = "visualize"              # Generate visual representation


class SkillAtom(NamedTuple):
    """Atomic skill component - smallest reusable unit."""
    atom_id: str
    atom_type: SkillAtomType
    description: str
    inputs: List[str]                    # Required input types
    outputs: List[str]                   # Output types
    implementation: Callable             # The actual function
    difficulty: int                      # Complexity (1-5)
    prerequisites: List[str]             # Other atoms needed first


class SkillMolecule(NamedTuple):
    """Composite skill built from atoms."""
    molecule_id: str
    description: str
    atoms: List[str]                     # Atom IDs in execution order
    skill_domain: str                    # e.g., "quadratic", "linear", etc.
    difficulty: int                      # Overall difficulty


# ========================================================================
# CAPABILITY MODULES - Reusable agent behaviors
# ========================================================================

class CapabilityModule(ABC):
    """Abstract base for reusable capability modules."""

    @abstractmethod
    def get_capability_id(self) -> str:
        """Return unique capability identifier."""
        pass

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute this capability with given context."""
        pass


class ParseEquationCapability(CapabilityModule):
    """Capability: Parse mathematical equations."""

    def get_capability_id(self) -> str:
        return "parse_equation"

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Parse equation from text."""
        import re

        equation_text = context.get("equation", "")

        # Parse quadratic in vertex form: y = a(x - h)^2 + k
        vertex_match = re.search(
            r'y\s*=\s*(-?\d*\.?\d*)\s*\(\s*x\s*([+-])\s*(\d+\.?\d*)\s*\)\s*\^?\s*2\s*([+-])\s*(\d+\.?\d*)',
            equation_text
        )

        if vertex_match:
            a = float(vertex_match.group(1) or "1")
            h_sign = vertex_match.group(2)
            h_val = float(vertex_match.group(3))
            k_sign = vertex_match.group(4)
            k_val = float(vertex_match.group(5))

            h = -h_val if h_sign == "+" else h_val
            k = k_val if k_sign == "+" else -k_val

            return {
                "form": "vertex",
                "a": a,
                "h": h,
                "k": k,
                "parsed": True
            }

        # Parse standard form: y = ax^2 + bx + c
        standard_match = re.search(
            r'y\s*=\s*(-?\d*\.?\d*)\s*x\s*\^?\s*2\s*([+-])\s*(\d+\.?\d*)\s*x\s*([+-])\s*(\d+\.?\d*)',
            equation_text
        )

        if standard_match:
            return {
                "form": "standard",
                "a": float(standard_match.group(1) or "1"),
                "b": float(standard_match.group(2) + standard_match.group(3)),
                "c": float(standard_match.group(4) + standard_match.group(5)),
                "parsed": True
            }

        return {"parsed": False, "error": "Could not parse equation"}


class ExtractVertexCapability(CapabilityModule):
    """Capability: Extract vertex from equation."""

    def get_capability_id(self) -> str:
        return "extract_vertex"

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract vertex coordinates."""
        # Check if we have parsed_equation dict (explicit format)
        parsed = context.get("parsed_equation", {})

        # Or check if parse results are directly in context
        if not parsed and context.get("parsed"):
            parsed = {
                "form": context.get("form"),
                "a": context.get("a"),
                "b": context.get("b"),
                "c": context.get("c"),
                "h": context.get("h"),
                "k": context.get("k")
            }

        if parsed.get("form") == "vertex":
            return {
                "vertex": (parsed.get("h", 0), parsed.get("k", 0)),
                "extracted": True
            }

        if parsed.get("form") == "standard":
            # Convert standard to vertex first
            a = parsed.get("a", 1)
            b = parsed.get("b", 0)
            c = parsed.get("c", 0)

            if a == 0:
                return {"extracted": False, "error": "Not a quadratic (a=0)"}

            h = -b / (2 * a)
            k = c - (b * b) / (4 * a)

            return {
                "vertex": (h, k),
                "extracted": True,
                "conversion": "standard_to_vertex"
            }

        return {"extracted": False, "error": "Invalid equation form"}


class ComputeDiscriminantCapability(CapabilityModule):
    """Capability: Compute discriminant for quadratic."""

    def get_capability_id(self) -> str:
        return "compute_discriminant"

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Compute discriminant b² - 4ac."""
        parsed = context.get("parsed_equation", {})

        if parsed.get("form") == "standard":
            a = parsed.get("a", 1)
            b = parsed.get("b", 0)
            c = parsed.get("c", 0)

            discriminant = b * b - 4 * a * c

            return {
                "discriminant": discriminant,
                "num_roots": 2 if discriminant > 0 else (1 if discriminant == 0 else 0),
                "computed": True
            }

        return {"computed": False, "error": "Requires standard form"}


class ClassifyEquationCapability(CapabilityModule):
    """Capability: Classify equation type and properties."""

    def get_capability_id(self) -> str:
        return "classify_equation"

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Classify equation characteristics."""
        # Check if we have parsed_equation dict (explicit format)
        parsed = context.get("parsed_equation", {})

        # Or check if parse results are directly in context
        if not parsed and context.get("parsed"):
            parsed = {
                "parsed": context.get("parsed"),
                "form": context.get("form"),
                "a": context.get("a"),
                "b": context.get("b"),
                "c": context.get("c"),
                "h": context.get("h"),
                "k": context.get("k")
            }

        if not parsed.get("parsed"):
            return {"classified": False, "error": "Equation not parsed"}

        classification = {
            "form": parsed.get("form"),
            "classified": True
        }

        if parsed.get("form") == "vertex":
            a = parsed.get("a", 1)
            classification["opens"] = "upward" if a > 0 else "downward"
            classification["vertex_at_origin"] = (parsed.get("h") == 0 and parsed.get("k") == 0)
            classification["stretched"] = abs(a) != 1
            classification["compressed"] = abs(a) < 1 and abs(a) > 0

        return classification


class ExplainStepsCapability(CapabilityModule):
    """Capability: Generate step-by-step explanations."""

    def get_capability_id(self) -> str:
        return "explain_steps"

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate explanation of solution steps."""
        skill_type = context.get("skill_type", "")
        parsed = context.get("parsed_equation", {})

        steps = []

        if "vertex" in skill_type and parsed.get("form") == "vertex":
            steps.append("Step 1: Identify the equation is in vertex form y = a(x - h)² + k")
            steps.append(f"Step 2: Read the values: a = {parsed.get('a')}, h = {parsed.get('h')}, k = {parsed.get('k')}")
            steps.append(f"Step 3: The vertex is at point (h, k) = ({parsed.get('h')}, {parsed.get('k')})")
            steps.append("Step 4: Remember: the sign of h is OPPOSITE to what appears in the equation")

        return {
            "steps": steps,
            "explained": True
        }


# ========================================================================
# REUSABLE SKILL LIBRARY
# ========================================================================

class ReusableSkillLibrary:
    """
    Central library for reusable skill components and agent capabilities.

    Enables:
    - Skill decomposition into atoms
    - Agent composition from capabilities
    - Transfer learning across domains
    - Rapid skill expansion
    """

    def __init__(self, library_dir: Optional[str] = None):
        """
        Initialize skill library.

        Args:
            library_dir: Directory for storing library data
        """
        self.library_dir = Path(library_dir or "./skill_library")
        self.library_dir.mkdir(exist_ok=True)

        # Registries
        self.atoms: Dict[str, SkillAtom] = {}
        self.molecules: Dict[str, SkillMolecule] = {}
        self.capabilities: Dict[str, CapabilityModule] = {}

        # Knowledge graph
        self.atom_dependencies: Dict[str, Set[str]] = {}
        self.skill_taxonomy: Dict[str, List[str]] = {}

        # Transfer learning
        self.domain_mappings: Dict[str, Dict[str, str]] = {}
        self.shared_patterns: List[Dict[str, Any]] = []

        # Usage tracking
        self.atom_usage_count: Dict[str, int] = {}
        self.composition_count = 0

        # Initialize core capabilities
        self._register_core_capabilities()

    # ====================================================================
    # CAPABILITY REGISTRATION
    # ====================================================================

    def _register_core_capabilities(self):
        """Register core reusable capabilities."""
        capabilities = [
            ParseEquationCapability(),
            ExtractVertexCapability(),
            ComputeDiscriminantCapability(),
            ClassifyEquationCapability(),
            ExplainStepsCapability()
        ]

        for cap in capabilities:
            self.register_capability(cap)

    def register_capability(self, capability: CapabilityModule) -> bool:
        """Register a capability module."""
        cap_id = capability.get_capability_id()
        self.capabilities[cap_id] = capability
        print(f"✓ Registered capability: {cap_id}")
        return True

    def register_atom(
        self,
        atom_id: str,
        atom_type: SkillAtomType,
        description: str,
        inputs: List[str],
        outputs: List[str],
        implementation: Callable,
        difficulty: int = 1,
        prerequisites: Optional[List[str]] = None
    ) -> bool:
        """Register a skill atom."""
        atom = SkillAtom(
            atom_id=atom_id,
            atom_type=atom_type,
            description=description,
            inputs=inputs,
            outputs=outputs,
            implementation=implementation,
            difficulty=difficulty,
            prerequisites=prerequisites or []
        )

        self.atoms[atom_id] = atom
        self.atom_usage_count[atom_id] = 0

        # Track dependencies
        if prerequisites:
            self.atom_dependencies[atom_id] = set(prerequisites)

        return True

    def register_molecule(
        self,
        molecule_id: str,
        description: str,
        atoms: List[str],
        skill_domain: str,
        difficulty: int = 3
    ) -> bool:
        """Register a skill molecule (composite)."""
        # Validate all atoms exist
        for atom_id in atoms:
            if atom_id not in self.atoms:
                print(f"⚠️ Warning: Atom {atom_id} not found")
                return False

        molecule = SkillMolecule(
            molecule_id=molecule_id,
            description=description,
            atoms=atoms,
            skill_domain=skill_domain,
            difficulty=difficulty
        )

        self.molecules[molecule_id] = molecule

        # Add to taxonomy
        if skill_domain not in self.skill_taxonomy:
            self.skill_taxonomy[skill_domain] = []
        self.skill_taxonomy[skill_domain].append(molecule_id)

        return True

    # ====================================================================
    # AGENT COMPOSITION
    # ====================================================================

    def compose_agent(
        self,
        agent_name: str,
        capabilities: List[str],
        skill_focus: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Compose a new agent from capability modules.

        Args:
            agent_name: Name for composed agent
            capabilities: List of capability IDs to include
            skill_focus: Optional skill domain focus

        Returns:
            Composed agent specification
        """
        # Validate capabilities exist
        missing = [c for c in capabilities if c not in self.capabilities]
        if missing:
            return {
                "success": False,
                "error": f"Missing capabilities: {missing}"
            }

        self.composition_count += 1

        return {
            "success": True,
            "agent_name": agent_name,
            "capabilities": capabilities,
            "skill_focus": skill_focus,
            "composition_id": f"composed_{self.composition_count}",
            "capability_modules": [self.capabilities[c] for c in capabilities]
        }

    def execute_capability_chain(
        self,
        capability_ids: List[str],
        initial_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a chain of capabilities, passing output to next input.

        Args:
            capability_ids: Ordered list of capability IDs
            initial_context: Starting context

        Returns:
            Final context after all capabilities execute
        """
        context = initial_context.copy()

        for cap_id in capability_ids:
            if cap_id not in self.capabilities:
                context["error"] = f"Capability {cap_id} not found"
                return context

            capability = self.capabilities[cap_id]

            try:
                result = capability.execute(context)
                context.update(result)  # Merge results into context
            except Exception as e:
                context["error"] = f"Error in {cap_id}: {str(e)}"
                return context

        return context

    # ====================================================================
    # SKILL EXECUTION
    # ====================================================================

    def execute_molecule(
        self,
        molecule_id: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a skill molecule (composite skill)."""
        if molecule_id not in self.molecules:
            return {"success": False, "error": f"Molecule {molecule_id} not found"}

        molecule = self.molecules[molecule_id]
        context = input_data.copy()

        # Execute atoms in sequence
        for atom_id in molecule.atoms:
            atom = self.atoms.get(atom_id)
            if not atom:
                continue

            try:
                result = atom.implementation(context)
                context.update(result)
                self.atom_usage_count[atom_id] += 1
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Error in atom {atom_id}: {str(e)}"
                }

        return {
            "success": True,
            "molecule_id": molecule_id,
            "result": context
        }

    # ====================================================================
    # TRANSFER LEARNING
    # ====================================================================

    def create_domain_mapping(
        self,
        source_domain: str,
        target_domain: str,
        concept_mappings: Dict[str, str]
    ) -> bool:
        """
        Create mapping between domains for transfer learning.

        Example: Map "quadratic vertex" concepts to "parabola vertex" concepts

        Args:
            source_domain: Source skill domain
            target_domain: Target skill domain
            concept_mappings: Dict mapping source concepts to target concepts

        Returns:
            Success boolean
        """
        mapping_key = f"{source_domain}->{target_domain}"
        self.domain_mappings[mapping_key] = concept_mappings

        print(f"✓ Created domain mapping: {source_domain} → {target_domain}")
        print(f"  Mapped {len(concept_mappings)} concepts")

        return True

    def transfer_skill(
        self,
        source_molecule_id: str,
        target_domain: str,
        new_molecule_id: str
    ) -> bool:
        """
        Transfer a skill molecule to a new domain.

        Uses domain mappings to adapt atoms to new context.

        Args:
            source_molecule_id: Source molecule to transfer
            target_domain: Target domain
            new_molecule_id: ID for new molecule

        Returns:
            Success boolean
        """
        if source_molecule_id not in self.molecules:
            return False

        source_molecule = self.molecules[source_molecule_id]
        source_domain = source_molecule.skill_domain

        # Find mapping
        mapping_key = f"{source_domain}->{target_domain}"
        if mapping_key not in self.domain_mappings:
            print(f"⚠️ No mapping found for {source_domain} → {target_domain}")
            return False

        # Create new molecule with same structure, new domain
        self.register_molecule(
            molecule_id=new_molecule_id,
            description=f"{source_molecule.description} (transferred to {target_domain})",
            atoms=source_molecule.atoms,  # Reuse same atoms
            skill_domain=target_domain,
            difficulty=source_molecule.difficulty
        )

        print(f"✓ Transferred {source_molecule_id} → {new_molecule_id}")
        return True

    def identify_shared_patterns(
        self,
        skill_ids: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Identify patterns shared across multiple skills.

        Useful for finding common atoms that could be extracted.

        Args:
            skill_ids: List of skill molecule IDs

        Returns:
            List of shared patterns
        """
        if len(skill_ids) < 2:
            return []

        # Get atom sets for each skill
        atom_sets = []
        for skill_id in skill_ids:
            if skill_id in self.molecules:
                atoms = set(self.molecules[skill_id].atoms)
                atom_sets.append(atoms)

        if not atom_sets:
            return []

        # Find intersection (atoms used by ALL skills)
        shared_atoms = set.intersection(*atom_sets)

        patterns = []
        for atom_id in shared_atoms:
            atom = self.atoms.get(atom_id)
            if atom:
                patterns.append({
                    "atom_id": atom_id,
                    "type": atom.atom_type.value,
                    "used_by": skill_ids,
                    "usage_count": self.atom_usage_count.get(atom_id, 0)
                })

        self.shared_patterns = patterns
        return patterns

    # ====================================================================
    # ANALYTICS & INSIGHTS
    # ====================================================================

    def get_library_stats(self) -> Dict[str, Any]:
        """Get library statistics."""
        return {
            "total_atoms": len(self.atoms),
            "total_molecules": len(self.molecules),
            "total_capabilities": len(self.capabilities),
            "domains": len(self.skill_taxonomy),
            "domain_mappings": len(self.domain_mappings),
            "compositions_created": self.composition_count,
            "atoms_by_type": self._count_atoms_by_type(),
            "most_used_atoms": self._get_most_used_atoms(5),
            "avg_molecule_complexity": self._avg_molecule_complexity()
        }

    def _count_atoms_by_type(self) -> Dict[str, int]:
        """Count atoms by type."""
        counts = {}
        for atom in self.atoms.values():
            type_name = atom.atom_type.value
            counts[type_name] = counts.get(type_name, 0) + 1
        return counts

    def _get_most_used_atoms(self, limit: int) -> List[Dict[str, Any]]:
        """Get most frequently used atoms."""
        sorted_atoms = sorted(
            self.atom_usage_count.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]

        return [
            {"atom_id": atom_id, "usage_count": count}
            for atom_id, count in sorted_atoms
        ]

    def _avg_molecule_complexity(self) -> float:
        """Calculate average molecule complexity."""
        if not self.molecules:
            return 0.0

        total = sum(m.difficulty for m in self.molecules.values())
        return total / len(self.molecules)

    def list_capabilities(self) -> None:
        """Print all registered capabilities."""
        print(f"\n{'='*70}")
        print("CAPABILITY MODULES")
        print(f"{'='*70}\n")

        for cap_id, capability in self.capabilities.items():
            print(f"🔧 {cap_id}")
            print(f"   Type: {type(capability).__name__}")
            print()

    def list_molecules(self) -> None:
        """Print all registered skill molecules."""
        print(f"\n{'='*70}")
        print("SKILL MOLECULES")
        print(f"{'='*70}\n")

        for domain, molecule_ids in self.skill_taxonomy.items():
            print(f"📚 Domain: {domain}")
            for mol_id in molecule_ids:
                molecule = self.molecules[mol_id]
                print(f"   • {mol_id}: {molecule.description}")
                print(f"     Atoms: {len(molecule.atoms)}, Difficulty: {molecule.difficulty}")
            print()

    def save_library(self, filename: str = "library_snapshot.json") -> bool:
        """Save library state to disk."""
        try:
            filepath = self.library_dir / filename

            state = {
                "atoms": {
                    atom_id: {
                        "atom_type": atom.atom_type.value,
                        "description": atom.description,
                        "difficulty": atom.difficulty,
                        "prerequisites": atom.prerequisites
                    }
                    for atom_id, atom in self.atoms.items()
                },
                "molecules": {
                    mol_id: {
                        "description": mol.description,
                        "atoms": mol.atoms,
                        "domain": mol.skill_domain,
                        "difficulty": mol.difficulty
                    }
                    for mol_id, mol in self.molecules.items()
                },
                "stats": self.get_library_stats()
            }

            with open(filepath, "w") as f:
                json.dump(state, f, indent=2)

            return True
        except Exception as e:
            print(f"❌ Failed to save library: {e}")
            return False
