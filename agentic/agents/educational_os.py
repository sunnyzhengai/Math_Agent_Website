"""
Educational OS: Unified orchestration layer for agentic learning system.

Implements Andrej Karpathy's LLM OS pattern:
- LLM as the "kernel" coordinating specialized agents
- Agent registry for discovery and management
- Resource allocation and state management
- Inter-agent communication and coordination
- Persistent learning context across sessions

This provides a unified API for the entire agentic system, managing:
- Constitutional AI validation
- Student World Model predictions
- Episodic Memory tracking
- ReAct explanations
- Least-to-Most decomposition
- Oracle reflection
- RAG knowledge retrieval
- Multi-agent committees

The OS handles orchestration logic, deciding which agents to invoke
for each learning scenario and managing data flow between them.
"""

from typing import Dict, List, Any, Optional, NamedTuple, Callable
from enum import Enum
import json
from pathlib import Path
from datetime import datetime


class AgentCapability(Enum):
    """Agent capability categories."""
    VALIDATION = "validation"          # Quality assurance
    PREDICTION = "prediction"          # Predict student behavior
    MEMORY = "memory"                  # Track learning journey
    EXPLANATION = "explanation"        # Generate explanations
    DECOMPOSITION = "decomposition"    # Break down complexity
    REFLECTION = "reflection"          # Self-critique
    RETRIEVAL = "retrieval"            # Knowledge lookup
    COORDINATION = "coordination"      # Multi-agent orchestration


class AgentStatus(Enum):
    """Agent operational status."""
    READY = "ready"
    BUSY = "busy"
    ERROR = "error"
    DISABLED = "disabled"


class AgentRegistration(NamedTuple):
    """Agent registration record."""
    agent_id: str
    agent_name: str
    capabilities: List[AgentCapability]
    priority: int  # Higher priority agents called first
    instance: Any  # The actual agent instance
    status: AgentStatus
    metadata: Dict[str, Any]


class OrchestratedResult(NamedTuple):
    """Result from orchestrated agent execution."""
    success: bool
    agents_invoked: List[str]
    results: Dict[str, Any]
    execution_time_ms: float
    errors: List[str]
    recommendations: List[str]


class LearningContext(NamedTuple):
    """Shared context for all agents."""
    student_id: str
    current_skill: str
    session_history: List[Dict[str, Any]]
    world_model_state: Optional[Dict[str, Any]]
    memory_state: Optional[Dict[str, Any]]
    preferences: Dict[str, Any]


class EducationalOS:
    """
    Unified operating system for agentic learning platform.

    Coordinates all AI agents, manages shared state, and provides
    a clean API for orchestrating complex learning experiences.

    Architecture inspired by Andrej Karpathy's LLM OS:
    - OS as orchestration kernel
    - Agents as specialized processes
    - Shared memory and state
    - Inter-process communication
    """

    def __init__(self, state_dir: Optional[str] = None):
        """
        Initialize Educational OS.

        Args:
            state_dir: Directory for persisting state (default: ./os_state)
        """
        self.agent_registry: Dict[str, AgentRegistration] = {}
        self.learning_contexts: Dict[str, LearningContext] = {}
        self.state_dir = Path(state_dir or "./os_state")
        self.state_dir.mkdir(exist_ok=True)

        # Orchestration stats
        self.total_orchestrations = 0
        self.agent_invocation_counts: Dict[str, int] = {}
        self.avg_orchestration_time_ms = 0.0

        # Shared resources
        self.shared_memory: Dict[str, Any] = {}
        self.resource_locks: Dict[str, bool] = {}

    # ========================================================================
    # AGENT REGISTRATION & MANAGEMENT
    # ========================================================================

    def register_agent(
        self,
        agent_id: str,
        agent_name: str,
        agent_instance: Any,
        capabilities: List[AgentCapability],
        priority: int = 5,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Register an agent with the OS.

        Args:
            agent_id: Unique agent identifier
            agent_name: Human-readable name
            agent_instance: The actual agent object
            capabilities: List of capabilities this agent provides
            priority: Priority level (1-10, higher = more important)
            metadata: Additional agent info

        Returns:
            True if registration successful
        """
        if agent_id in self.agent_registry:
            print(f"⚠️ Agent {agent_id} already registered, updating...")

        registration = AgentRegistration(
            agent_id=agent_id,
            agent_name=agent_name,
            capabilities=capabilities,
            priority=priority,
            instance=agent_instance,
            status=AgentStatus.READY,
            metadata=metadata or {}
        )

        self.agent_registry[agent_id] = registration
        self.agent_invocation_counts[agent_id] = 0

        print(f"✓ Registered agent: {agent_name} ({agent_id})")
        print(f"  Capabilities: {[c.value for c in capabilities]}")
        print(f"  Priority: {priority}")

        return True

    def get_agents_by_capability(
        self,
        capability: AgentCapability,
        status: AgentStatus = AgentStatus.READY
    ) -> List[AgentRegistration]:
        """Get all agents with specific capability."""
        agents = [
            agent for agent in self.agent_registry.values()
            if capability in agent.capabilities and agent.status == status
        ]
        # Sort by priority (descending)
        return sorted(agents, key=lambda a: a.priority, reverse=True)

    def set_agent_status(self, agent_id: str, status: AgentStatus) -> None:
        """Update agent status."""
        if agent_id in self.agent_registry:
            agent = self.agent_registry[agent_id]
            updated = agent._replace(status=status)
            self.agent_registry[agent_id] = updated

    # ========================================================================
    # ORCHESTRATION - Core OS Logic
    # ========================================================================

    def orchestrate_question_validation(
        self,
        question: Dict[str, Any],
        context: Optional[LearningContext] = None
    ) -> OrchestratedResult:
        """
        Orchestrate question validation using multiple agents.

        Coordinates:
        1. Constitutional Validator - Quality checks
        2. Reflection Oracle - Self-critique
        3. Validation Committee - Multi-agent consensus

        Returns:
            OrchestratedResult with validation decision
        """
        start_time = datetime.now()
        agents_invoked = []
        results = {}
        errors = []
        recommendations = []

        # STEP 1: Constitutional validation (highest priority)
        constitutional_agents = self.get_agents_by_capability(AgentCapability.VALIDATION)

        for agent in constitutional_agents:
            if "constitutional" in agent.agent_id.lower():
                try:
                    self.set_agent_status(agent.agent_id, AgentStatus.BUSY)
                    result = agent.instance.validate(question)
                    agents_invoked.append(agent.agent_id)
                    results["constitutional"] = result
                    self.agent_invocation_counts[agent.agent_id] += 1
                    self.set_agent_status(agent.agent_id, AgentStatus.READY)

                    if not result.passes_constitution:
                        recommendations.append(
                            f"Constitutional violation: {result.violation_summary}"
                        )
                except Exception as e:
                    errors.append(f"{agent.agent_id}: {str(e)}")
                    self.set_agent_status(agent.agent_id, AgentStatus.ERROR)

        # STEP 2: Reflection oracle (if available)
        reflection_agents = self.get_agents_by_capability(AgentCapability.REFLECTION)

        for agent in reflection_agents:
            try:
                self.set_agent_status(agent.agent_id, AgentStatus.BUSY)
                # Oracle reflection on question quality
                result = agent.instance.reflect(
                    task="validate_question",
                    initial_output=question,
                    max_iterations=2
                )
                agents_invoked.append(agent.agent_id)
                results["reflection"] = result
                self.agent_invocation_counts[agent.agent_id] += 1
                self.set_agent_status(agent.agent_id, AgentStatus.READY)
            except Exception as e:
                errors.append(f"{agent.agent_id}: {str(e)}")
                self.set_agent_status(agent.agent_id, AgentStatus.ERROR)

        # STEP 3: Multi-agent committee (if available)
        coordination_agents = self.get_agents_by_capability(AgentCapability.COORDINATION)

        for agent in coordination_agents:
            if "committee" in agent.agent_id.lower():
                try:
                    self.set_agent_status(agent.agent_id, AgentStatus.BUSY)
                    result = agent.instance.validate(question)
                    agents_invoked.append(agent.agent_id)
                    results["committee"] = result
                    self.agent_invocation_counts[agent.agent_id] += 1
                    self.set_agent_status(agent.agent_id, AgentStatus.READY)
                except Exception as e:
                    errors.append(f"{agent.agent_id}: {str(e)}")
                    self.set_agent_status(agent.agent_id, AgentStatus.ERROR)

        # Compute final decision
        success = self._compute_validation_decision(results)

        execution_time = (datetime.now() - start_time).total_seconds() * 1000
        self.total_orchestrations += 1
        self._update_avg_orchestration_time(execution_time)

        return OrchestratedResult(
            success=success,
            agents_invoked=agents_invoked,
            results=results,
            execution_time_ms=execution_time,
            errors=errors,
            recommendations=recommendations
        )

    def orchestrate_personalized_learning(
        self,
        student_id: str,
        target_skill: str,
        current_question: Optional[Dict[str, Any]] = None
    ) -> OrchestratedResult:
        """
        Orchestrate personalized learning experience.

        Coordinates:
        1. Student World Model - Predict struggles
        2. Episodic Memory - Recall past experiences
        3. Least-to-Most Decomposer - Break down complexity

        Returns:
            OrchestratedResult with personalized recommendations
        """
        start_time = datetime.now()
        agents_invoked = []
        results = {}
        errors = []
        recommendations = []

        # Get or create learning context
        context = self.learning_contexts.get(student_id)

        # STEP 1: Check world model predictions
        prediction_agents = self.get_agents_by_capability(AgentCapability.PREDICTION)

        for agent in prediction_agents:
            try:
                self.set_agent_status(agent.agent_id, AgentStatus.BUSY)
                prediction = agent.instance.predict_struggle(target_skill)
                agents_invoked.append(agent.agent_id)
                results["world_model"] = prediction
                self.agent_invocation_counts[agent.agent_id] += 1
                self.set_agent_status(agent.agent_id, AgentStatus.READY)

                if len(prediction.predicted_struggle_concepts) > 0:
                    recommendations.extend(prediction.intervention_suggestions)
            except Exception as e:
                errors.append(f"{agent.agent_id}: {str(e)}")
                self.set_agent_status(agent.agent_id, AgentStatus.ERROR)

        # STEP 2: Retrieve relevant memories
        memory_agents = self.get_agents_by_capability(AgentCapability.MEMORY)

        for agent in memory_agents:
            try:
                self.set_agent_status(agent.agent_id, AgentStatus.BUSY)
                memories = agent.instance.retrieve_relevant_memories(
                    context_tags=[target_skill, "struggle"],
                    limit=5
                )
                agents_invoked.append(agent.agent_id)
                results["memories"] = memories
                self.agent_invocation_counts[agent.agent_id] += 1
                self.set_agent_status(agent.agent_id, AgentStatus.READY)

                # Use memories to inform recommendations
                if len(memories) > 0:
                    recommendations.append(
                        f"Found {len(memories)} relevant past experiences"
                    )
            except Exception as e:
                errors.append(f"{agent.agent_id}: {str(e)}")
                self.set_agent_status(agent.agent_id, AgentStatus.ERROR)

        # STEP 3: Decompose if needed (based on predicted struggles)
        if results.get("world_model") and len(results["world_model"].predicted_struggle_concepts) > 2:
            decomposition_agents = self.get_agents_by_capability(AgentCapability.DECOMPOSITION)

            for agent in decomposition_agents:
                try:
                    self.set_agent_status(agent.agent_id, AgentStatus.BUSY)

                    # Generate scaffolded practice
                    scaffolded = agent.instance.generate_scaffolded_practice(
                        skill_id=target_skill,
                        start_level=1,
                        end_level=3,  # Start easier
                        problems_per_level=2
                    )

                    agents_invoked.append(agent.agent_id)
                    results["scaffolding"] = scaffolded
                    self.agent_invocation_counts[agent.agent_id] += 1
                    self.set_agent_status(agent.agent_id, AgentStatus.READY)

                    recommendations.append(
                        f"Generated {len(scaffolded.problems)} scaffolded problems "
                        f"(levels {scaffolded.difficulty_progression[0]}-"
                        f"{scaffolded.difficulty_progression[-1]})"
                    )
                except Exception as e:
                    errors.append(f"{agent.agent_id}: {str(e)}")
                    self.set_agent_status(agent.agent_id, AgentStatus.ERROR)

        execution_time = (datetime.now() - start_time).total_seconds() * 1000
        self.total_orchestrations += 1
        self._update_avg_orchestration_time(execution_time)

        return OrchestratedResult(
            success=len(errors) == 0,
            agents_invoked=agents_invoked,
            results=results,
            execution_time_ms=execution_time,
            errors=errors,
            recommendations=recommendations
        )

    def orchestrate_explanation_generation(
        self,
        question: Dict[str, Any],
        student_answer: str,
        correct_answer: str,
        student_id: Optional[str] = None
    ) -> OrchestratedResult:
        """
        Orchestrate explanation generation with context.

        Coordinates:
        1. Episodic Memory - Get relevant past errors
        2. ReAct Explainer - Generate transparent reasoning
        3. Episodic Memory - Store this learning event

        Returns:
            OrchestratedResult with explanation
        """
        start_time = datetime.now()
        agents_invoked = []
        results = {}
        errors = []
        recommendations = []

        context_data = {}

        # STEP 1: Get relevant memories (if student_id provided)
        if student_id:
            memory_agents = self.get_agents_by_capability(AgentCapability.MEMORY)

            for agent in memory_agents:
                try:
                    self.set_agent_status(agent.agent_id, AgentStatus.BUSY)
                    memories = agent.instance.retrieve_relevant_memories(
                        context_tags=[question.get("skill_id", ""), "error"],
                        limit=3
                    )
                    agents_invoked.append(agent.agent_id)
                    context_data["past_errors"] = memories
                    self.agent_invocation_counts[agent.agent_id] += 1
                    self.set_agent_status(agent.agent_id, AgentStatus.READY)
                except Exception as e:
                    errors.append(f"{agent.agent_id}: {str(e)}")
                    self.set_agent_status(agent.agent_id, AgentStatus.ERROR)

        # STEP 2: Generate ReAct explanation
        explanation_agents = self.get_agents_by_capability(AgentCapability.EXPLANATION)

        for agent in explanation_agents:
            try:
                self.set_agent_status(agent.agent_id, AgentStatus.BUSY)
                explanation = agent.instance.generate_explanation_with_react(
                    question=question,
                    student_answer=student_answer,
                    correct_answer=correct_answer,
                    context=context_data
                )
                agents_invoked.append(agent.agent_id)
                results["explanation"] = explanation
                self.agent_invocation_counts[agent.agent_id] += 1
                self.set_agent_status(agent.agent_id, AgentStatus.READY)

                recommendations.append(
                    f"Generated {len(explanation.reasoning_steps)}-step ReAct explanation"
                )
            except Exception as e:
                errors.append(f"{agent.agent_id}: {str(e)}")
                self.set_agent_status(agent.agent_id, AgentStatus.ERROR)

        # STEP 3: Store learning event in memory
        if student_id and "explanation" in results:
            memory_agents = self.get_agents_by_capability(AgentCapability.MEMORY)

            for agent in memory_agents:
                try:
                    explanation = results["explanation"]
                    agent.instance.store_struggle(
                        skill_id=question.get("skill_id", "unknown"),
                        error_type=explanation.error_type,
                        description=f"Student chose {student_answer} instead of {correct_answer}"
                    )
                except Exception as e:
                    errors.append(f"Memory storage: {str(e)}")

        execution_time = (datetime.now() - start_time).total_seconds() * 1000
        self.total_orchestrations += 1
        self._update_avg_orchestration_time(execution_time)

        return OrchestratedResult(
            success=len(errors) == 0,
            agents_invoked=agents_invoked,
            results=results,
            execution_time_ms=execution_time,
            errors=errors,
            recommendations=recommendations
        )

    # ========================================================================
    # STATE PERSISTENCE
    # ========================================================================

    def save_state(self, student_id: str) -> bool:
        """Save OS state for a student to disk."""
        try:
            state_file = self.state_dir / f"{student_id}_state.json"

            state = {
                "student_id": student_id,
                "timestamp": datetime.now().isoformat(),
                "shared_memory": self.shared_memory,
                "orchestration_stats": {
                    "total_orchestrations": self.total_orchestrations,
                    "agent_invocations": self.agent_invocation_counts,
                    "avg_time_ms": self.avg_orchestration_time_ms
                }
            }

            with open(state_file, "w") as f:
                json.dump(state, f, indent=2)

            return True
        except Exception as e:
            print(f"❌ Failed to save state: {e}")
            return False

    def load_state(self, student_id: str) -> bool:
        """Load OS state for a student from disk."""
        try:
            state_file = self.state_dir / f"{student_id}_state.json"

            if not state_file.exists():
                return False

            with open(state_file, "r") as f:
                state = json.load(f)

            self.shared_memory = state.get("shared_memory", {})
            stats = state.get("orchestration_stats", {})
            self.total_orchestrations = stats.get("total_orchestrations", 0)
            self.agent_invocation_counts = stats.get("agent_invocations", {})
            self.avg_orchestration_time_ms = stats.get("avg_time_ms", 0.0)

            return True
        except Exception as e:
            print(f"❌ Failed to load state: {e}")
            return False

    # ========================================================================
    # UTILITIES
    # ========================================================================

    def _compute_validation_decision(self, results: Dict[str, Any]) -> bool:
        """Compute final validation decision from agent results."""
        # Constitutional validator has veto power
        if "constitutional" in results:
            if not results["constitutional"].passes_constitution:
                return False

        # Committee decision
        if "committee" in results:
            if not results["committee"].approved:
                return False

        # Reflection oracle
        if "reflection" in results:
            if not results["reflection"].approved:
                return False

        return True

    def _update_avg_orchestration_time(self, new_time: float) -> None:
        """Update rolling average orchestration time."""
        n = self.total_orchestrations
        if n == 1:
            self.avg_orchestration_time_ms = new_time
        else:
            self.avg_orchestration_time_ms = (
                (self.avg_orchestration_time_ms * (n - 1) + new_time) / n
            )

    def get_system_stats(self) -> Dict[str, Any]:
        """Get OS statistics."""
        return {
            "total_agents": len(self.agent_registry),
            "agents_by_status": self._count_agents_by_status(),
            "total_orchestrations": self.total_orchestrations,
            "avg_orchestration_time_ms": round(self.avg_orchestration_time_ms, 2),
            "agent_invocations": self.agent_invocation_counts,
            "most_used_agent": max(
                self.agent_invocation_counts.items(),
                key=lambda x: x[1]
            )[0] if self.agent_invocation_counts else None
        }

    def _count_agents_by_status(self) -> Dict[str, int]:
        """Count agents by status."""
        counts = {}
        for agent in self.agent_registry.values():
            status = agent.status.value
            counts[status] = counts.get(status, 0) + 1
        return counts

    def list_agents(self) -> None:
        """Print all registered agents."""
        print(f"\n{'='*70}")
        print(f"EDUCATIONAL OS - AGENT REGISTRY")
        print(f"{'='*70}\n")

        if not self.agent_registry:
            print("No agents registered.\n")
            return

        for agent in sorted(self.agent_registry.values(), key=lambda a: a.priority, reverse=True):
            print(f"📦 {agent.agent_name} ({agent.agent_id})")
            print(f"   Status: {agent.status.value}")
            print(f"   Priority: {agent.priority}")
            print(f"   Capabilities: {[c.value for c in agent.capabilities]}")
            print(f"   Invocations: {self.agent_invocation_counts.get(agent.agent_id, 0)}")
            print()
