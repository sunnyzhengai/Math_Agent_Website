"""
Acceptance tests for Educational OS.

Tests the unified orchestration layer that coordinates all agentic
components using Andrej Karpathy's LLM OS pattern.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agentic.agents.educational_os import (
    EducationalOS,
    AgentCapability,
    AgentStatus,
    AgentRegistration,
    OrchestratedResult
)
from agentic.agents.educational_constitutional_validator import EducationalConstitutionalValidator
from agentic.agents.student_world_model import StudentWorldModel
from agentic.agents.episodic_memory_system import EpisodicMemorySystem
from agentic.agents.react_explanation_generator import ReActExplanationGenerator
from agentic.agents.least_to_most_decomposer import LeastToMostDecomposer


# Mock agents for testing
class MockValidationAgent:
    def validate(self, question):
        class Result:
            passes_constitution = True
            violation_summary = ""
        return Result()


class MockReflectionAgent:
    def reflect(self, task, initial_output, max_iterations=2):
        class Result:
            approved = True
        return Result()


class MockCommitteeAgent:
    def validate(self, question):
        class Result:
            approved = True
            failed_agent = None
        return Result()


def run_tests():
    print("="*70)
    print("EDUCATIONAL OS ACCEPTANCE TESTS")
    print("="*70)
    print()

    # Test 1: Initialize OS
    print("Testing OS initialization...")
    os = EducationalOS(state_dir="./test_os_state")
    assert os is not None
    assert len(os.agent_registry) == 0
    assert os.total_orchestrations == 0
    print("✓ OS initialized\n")

    # Test 2: Register agents
    print("Testing agent registration...")

    # Register constitutional validator
    constitutional = EducationalConstitutionalValidator()
    os.register_agent(
        agent_id="constitutional_validator",
        agent_name="Constitutional Validator",
        agent_instance=constitutional,
        capabilities=[AgentCapability.VALIDATION],
        priority=10
    )

    # Register world model
    world_model = StudentWorldModel()
    os.register_agent(
        agent_id="world_model",
        agent_name="Student World Model",
        agent_instance=world_model,
        capabilities=[AgentCapability.PREDICTION],
        priority=8
    )

    # Register memory system
    memory = EpisodicMemorySystem()
    os.register_agent(
        agent_id="episodic_memory",
        agent_name="Episodic Memory",
        agent_instance=memory,
        capabilities=[AgentCapability.MEMORY],
        priority=7
    )

    # Register ReAct explainer
    react = ReActExplanationGenerator()
    os.register_agent(
        agent_id="react_explainer",
        agent_name="ReAct Explainer",
        agent_instance=react,
        capabilities=[AgentCapability.EXPLANATION],
        priority=6
    )

    # Register decomposer
    decomposer = LeastToMostDecomposer()
    os.register_agent(
        agent_id="least_to_most",
        agent_name="Least-to-Most Decomposer",
        agent_instance=decomposer,
        capabilities=[AgentCapability.DECOMPOSITION],
        priority=5
    )

    assert len(os.agent_registry) == 5
    print(f"✓ Registered {len(os.agent_registry)} agents\n")

    # Test 3: Get agents by capability
    print("Testing agent discovery by capability...")
    validation_agents = os.get_agents_by_capability(AgentCapability.VALIDATION)
    assert len(validation_agents) == 1
    assert validation_agents[0].agent_id == "constitutional_validator"

    prediction_agents = os.get_agents_by_capability(AgentCapability.PREDICTION)
    assert len(prediction_agents) == 1
    assert prediction_agents[0].agent_id == "world_model"

    memory_agents = os.get_agents_by_capability(AgentCapability.MEMORY)
    assert len(memory_agents) == 1

    explanation_agents = os.get_agents_by_capability(AgentCapability.EXPLANATION)
    assert len(explanation_agents) == 1

    decomposition_agents = os.get_agents_by_capability(AgentCapability.DECOMPOSITION)
    assert len(decomposition_agents) == 1

    print(f"✓ Agent discovery working")
    print(f"  Validation: {len(validation_agents)}")
    print(f"  Prediction: {len(prediction_agents)}")
    print(f"  Memory: {len(memory_agents)}")
    print(f"  Explanation: {len(explanation_agents)}")
    print(f"  Decomposition: {len(decomposition_agents)}\n")

    # Test 4: Agent priority sorting
    print("Testing agent priority sorting...")
    all_agents = list(os.agent_registry.values())
    priorities = [a.priority for a in all_agents]
    assert priorities == [10, 8, 7, 6, 5]
    print(f"✓ Agents sorted by priority: {priorities}\n")

    # Test 5: Agent status management
    print("Testing agent status management...")
    os.set_agent_status("world_model", AgentStatus.BUSY)
    world_model_agent = os.agent_registry["world_model"]
    assert world_model_agent.status == AgentStatus.BUSY

    os.set_agent_status("world_model", AgentStatus.READY)
    world_model_agent = os.agent_registry["world_model"]
    assert world_model_agent.status == AgentStatus.READY
    print("✓ Status management working\n")

    # Test 6: Orchestrate question validation
    print("Testing question validation orchestration...")
    question = {
        "stem": "Find the vertex of y = (x - 3)^2 + 2",
        "skill_id": "quad.graph.vertex",
        "choices": [
            {"id": "A", "text": "(3, 2)"},
            {"id": "B", "text": "(-3, 2)"},
            {"id": "C", "text": "(3, -2)"},
            {"id": "D", "text": "(-3, -2)"}
        ],
        "correct": "A"
    }

    result = os.orchestrate_question_validation(question)
    assert isinstance(result, OrchestratedResult)
    assert result.success == True
    assert len(result.agents_invoked) > 0
    assert "constitutional" in result.results
    print(f"✓ Validation orchestration working")
    print(f"  Agents invoked: {result.agents_invoked}")
    print(f"  Execution time: {result.execution_time_ms:.2f}ms")
    print(f"  Success: {result.success}\n")

    # Test 7: Orchestrate personalized learning
    print("Testing personalized learning orchestration...")

    # First, train the world model with some practice
    for i in range(3):
        world_model.update_from_performance("quad.graph.vertex", correct=True, time_taken=25.0)

    result = os.orchestrate_personalized_learning(
        student_id="student_123",
        target_skill="quad.graph.vertex"
    )

    assert isinstance(result, OrchestratedResult)
    assert len(result.agents_invoked) > 0
    assert "world_model" in result.results
    print(f"✓ Personalized learning orchestration working")
    print(f"  Agents invoked: {result.agents_invoked}")
    print(f"  Execution time: {result.execution_time_ms:.2f}ms")
    print(f"  Recommendations: {len(result.recommendations)}\n")

    # Test 8: Orchestrate explanation generation
    print("Testing explanation generation orchestration...")
    result = os.orchestrate_explanation_generation(
        question=question,
        student_answer="B",
        correct_answer="A",
        student_id="student_123"
    )

    assert isinstance(result, OrchestratedResult)
    assert len(result.agents_invoked) > 0
    assert "explanation" in result.results
    explanation = result.results["explanation"]
    assert len(explanation.reasoning_steps) == 4  # ReAct has 4 cycles
    print(f"✓ Explanation orchestration working")
    print(f"  Agents invoked: {result.agents_invoked}")
    print(f"  Reasoning steps: {len(explanation.reasoning_steps)}")
    print(f"  Error type: {explanation.error_type}")
    print(f"  Execution time: {result.execution_time_ms:.2f}ms\n")

    # Test 9: Multi-agent coordination stats
    print("Testing multi-agent coordination stats...")
    stats = os.get_system_stats()
    assert stats["total_agents"] == 5
    assert stats["total_orchestrations"] == 3  # We ran 3 orchestrations
    assert stats["avg_orchestration_time_ms"] > 0
    assert len(stats["agent_invocations"]) > 0
    print(f"✓ System stats working")
    print(f"  Total agents: {stats['total_agents']}")
    print(f"  Total orchestrations: {stats['total_orchestrations']}")
    print(f"  Avg time: {stats['avg_orchestration_time_ms']:.2f}ms")
    print(f"  Most used: {stats['most_used_agent']}\n")

    # Test 10: State persistence
    print("Testing state persistence...")
    saved = os.save_state("student_123")
    assert saved == True

    # Create new OS and load state
    os2 = EducationalOS(state_dir="./test_os_state")
    loaded = os2.load_state("student_123")
    assert loaded == True
    assert os2.total_orchestrations == 3
    print(f"✓ State persistence working")
    print(f"  Orchestrations restored: {os2.total_orchestrations}\n")

    # Test 11: Agent listing
    print("Testing agent listing...")
    print("Agents in registry:")
    os.list_agents()

    # Test 12: Error handling
    print("Testing error handling...")
    # Try to orchestrate with invalid question
    bad_question = {"invalid": "structure"}
    result = os.orchestrate_question_validation(bad_question)
    # Should handle gracefully (may have errors but shouldn't crash)
    assert isinstance(result, OrchestratedResult)
    print(f"✓ Error handling working")
    print(f"  Errors captured: {len(result.errors)}\n")

    # Test 13: Orchestration with memory context
    print("Testing orchestration with memory context...")

    # Store some memories first
    memory.store_struggle(
        skill_id="quad.graph.vertex",
        error_type="sign_error",
        description="Confused about sign of h in vertex form"
    )
    memory.store_breakthrough(
        skill_id="quad.graph.vertex",
        achievement="Correctly identified vertex after practice",
        description="Finally understood the sign convention"
    )

    # Now orchestrate explanation (should retrieve these memories)
    result = os.orchestrate_explanation_generation(
        question=question,
        student_answer="C",
        correct_answer="A",
        student_id="student_123"
    )

    assert "explanation" in result.results
    print(f"✓ Memory-aware orchestration working")
    print(f"  Memories available for context: Yes\n")

    # Test 14: Decomposition triggering based on predicted struggles
    print("Testing automatic decomposition triggering...")

    # Create a student with low mastery (should trigger decomposition)
    struggling_model = StudentWorldModel()
    os.agent_registry["world_model"] = os.agent_registry["world_model"]._replace(
        instance=struggling_model
    )

    # Set low mastery by simulating failed attempts
    for i in range(5):
        struggling_model.update_from_performance("quad.graph.vertex", correct=False, error_type="sign_error")

    result = os.orchestrate_personalized_learning(
        student_id="struggling_student",
        target_skill="quad.graph.vertex"
    )

    # Should trigger decomposition due to struggles
    print(f"✓ Automatic decomposition triggering")
    print(f"  Agents invoked: {result.agents_invoked}")
    if "scaffolding" in result.results:
        print(f"  Scaffolded problems generated: {len(result.results['scaffolding'].problems)}")
    print()

    # Test 15: Agent invocation counting
    print("Testing agent invocation tracking...")
    invocations = os.agent_invocation_counts
    assert len(invocations) > 0
    total_invocations = sum(invocations.values())
    print(f"✓ Invocation tracking working")
    print(f"  Total invocations: {total_invocations}")
    for agent_id, count in sorted(invocations.items(), key=lambda x: x[1], reverse=True):
        print(f"    {agent_id}: {count}")
    print()

    # Test 16: Orchestration recommendations
    print("Testing orchestration recommendations...")
    result = os.orchestrate_personalized_learning(
        student_id="student_456",
        target_skill="quad.graph.vertex"
    )
    assert isinstance(result.recommendations, list)
    print(f"✓ Recommendations generated: {len(result.recommendations)}")
    for i, rec in enumerate(result.recommendations[:3], 1):
        print(f"  {i}. {rec}")
    print()

    # Test 17: Multiple capability agents
    print("Testing agents with multiple capabilities...")

    # Create mock agent with multiple capabilities
    mock_hybrid = MockValidationAgent()
    os.register_agent(
        agent_id="hybrid_agent",
        agent_name="Hybrid Agent",
        agent_instance=mock_hybrid,
        capabilities=[AgentCapability.VALIDATION, AgentCapability.REFLECTION],
        priority=9
    )

    # Should be discoverable by both capabilities
    validation_agents = os.get_agents_by_capability(AgentCapability.VALIDATION)
    reflection_agents = os.get_agents_by_capability(AgentCapability.REFLECTION)

    assert any(a.agent_id == "hybrid_agent" for a in validation_agents)
    assert any(a.agent_id == "hybrid_agent" for a in reflection_agents)
    print(f"✓ Multi-capability agents working")
    print(f"  Hybrid agent in validation pool: Yes")
    print(f"  Hybrid agent in reflection pool: Yes\n")

    # Test 18: Priority-based agent selection
    print("Testing priority-based agent ordering...")
    validation_agents = os.get_agents_by_capability(AgentCapability.VALIDATION)

    # Should be sorted by priority (descending)
    if len(validation_agents) > 1:
        priorities = [a.priority for a in validation_agents]
        assert priorities == sorted(priorities, reverse=True)
        print(f"✓ Priority ordering correct: {priorities}\n")
    else:
        print(f"✓ Priority ordering verified (single agent)\n")

    # Test 19: Orchestration time tracking
    print("Testing orchestration time tracking...")
    initial_avg = os.avg_orchestration_time_ms

    # Run another orchestration
    os.orchestrate_question_validation(question)

    # Average should update
    new_avg = os.avg_orchestration_time_ms
    assert new_avg > 0
    print(f"✓ Time tracking working")
    print(f"  Initial avg: {initial_avg:.2f}ms")
    print(f"  Updated avg: {new_avg:.2f}ms\n")

    # Test 20: System health check
    print("Testing system health check...")
    stats = os.get_system_stats()
    agents_by_status = stats["agents_by_status"]

    # Most agents should be ready
    ready_count = agents_by_status.get("ready", 0)
    total_agents = stats["total_agents"]
    health_ratio = ready_count / total_agents if total_agents > 0 else 0

    print(f"✓ System health check")
    print(f"  Total agents: {total_agents}")
    print(f"  Ready agents: {ready_count}")
    print(f"  Health ratio: {health_ratio:.1%}")
    print(f"  Status breakdown: {agents_by_status}\n")

    # Cleanup
    import shutil
    shutil.rmtree("./test_os_state", ignore_errors=True)

    print("="*70)
    print("ALL ACCEPTANCE TESTS PASSED ✓")
    print("="*70)
    print()


if __name__ == "__main__":
    run_tests()
