"""
Acceptance tests for Episodic Memory System.

Validates Lilian Weng's Memory Systems architecture:
- Short-term memory (limited capacity, recent)
- Long-term memory (consolidated, unlimited)
- Memory consolidation (important → long-term)
- Context-aware retrieval
- Personalized narrative generation
"""

import sys
from pathlib import Path
import time

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agentic.agents.episodic_memory_system import EpisodicMemorySystem


def test_initialization():
    """Test that memory system initializes correctly."""
    memory = EpisodicMemorySystem(short_term_capacity=20)

    assert memory.short_term_capacity == 20, "Should set capacity"
    assert len(memory.short_term_memory) == 0, "Should start empty"
    assert len(memory.long_term_memory) == 0, "Should start empty"
    assert memory.total_events_stored == 0, "Should have 0 events"

    print("✓ Memory system initialized")
    print(f"  Short-term capacity: {memory.short_term_capacity}")


def test_stores_struggle_memories():
    """Test storing struggle/error memories."""
    memory = EpisodicMemorySystem()

    event_id = memory.store_struggle(
        skill_id="quad.graph.vertex",
        error_type="sign_error",
        description="Student confused vertex sign in (x - h) form",
        context={"question_id": "q123", "wrong_answer": "B"}
    )

    assert event_id, "Should return event ID"
    assert len(memory.short_term_memory) == 1, "Should store in short-term"

    stored_memory = memory.short_term_memory[0]
    assert stored_memory.event_type == "struggle", "Should be struggle type"
    assert stored_memory.skill_id == "quad.graph.vertex", "Should track skill"
    assert stored_memory.emotional_valence < 0, "Struggles should be negative"

    print("✓ Stores struggle memories")
    print(f"  Event ID: {event_id}")
    print(f"  Importance: {stored_memory.importance}")
    print(f"  Emotional valence: {stored_memory.emotional_valence}")


def test_stores_breakthrough_memories():
    """Test storing breakthrough/success memories."""
    memory = EpisodicMemorySystem()

    event_id = memory.store_breakthrough(
        skill_id="quad.graph.vertex",
        achievement="first_correct",
        description="Successfully identified vertex on first try",
        context={"mastery_level": 0.8}
    )

    assert event_id, "Should return event ID"

    stored_memory = memory.short_term_memory[0]
    assert stored_memory.event_type == "breakthrough", "Should be breakthrough type"
    assert stored_memory.emotional_valence > 0, "Breakthroughs should be positive"
    assert stored_memory.importance >= 0.9, "Breakthroughs very important"

    print("✓ Stores breakthrough memories")
    print(f"  Achievement: {stored_memory.context.get('mastery_level')}")
    print(f"  Emotional valence: {stored_memory.emotional_valence}")


def test_stores_pattern_memories():
    """Test storing learning pattern memories."""
    memory = EpisodicMemorySystem()

    event_id = memory.store_pattern(
        pattern_type="repeated_error",
        description="Student consistently makes sign errors in vertex form",
        related_skills=["quad.graph.vertex", "quad.standard.vertex"],
        context={"frequency": 5, "sessions": 3}
    )

    assert event_id, "Should return event ID"

    stored_memory = memory.short_term_memory[0]
    assert stored_memory.event_type == "pattern", "Should be pattern type"
    assert "pattern" in stored_memory.tags, "Should tag as pattern"

    print("✓ Stores pattern memories")
    print(f"  Pattern type: repeated_error")
    print(f"  Related skills: {stored_memory.context['related_skills']}")


def test_stores_milestone_memories():
    """Test storing milestone achievement memories."""
    memory = EpisodicMemorySystem()

    event_id = memory.store_milestone(
        skill_id="quad.graph.vertex",
        milestone="skill_completed",
        description="Achieved 85% mastery on vertex identification",
        context={"mastery_level": 0.85, "total_attempts": 20}
    )

    assert event_id, "Should return event ID"

    stored_memory = memory.short_term_memory[0]
    assert stored_memory.event_type == "milestone", "Should be milestone type"
    assert stored_memory.importance == 1.0, "Milestones most important"
    assert stored_memory.emotional_valence == 1.0, "Milestones very positive"

    print("✓ Stores milestone memories")
    print(f"  Milestone: skill_completed")
    print(f"  Importance: {stored_memory.importance}")


def test_retrieves_similar_memories():
    """Test retrieving relevant memories based on context."""
    memory = EpisodicMemorySystem()

    # Store several memories
    memory.store_struggle("quad.graph.vertex", "sign_error", "Sign error in vertex")
    memory.store_struggle("quad.graph.vertex", "coordinate_swap", "Swapped coordinates")
    memory.store_breakthrough("quad.graph.vertex", "first_correct", "First correct answer")
    memory.store_struggle("quad.solve.by_factoring", "factoring_error", "Factoring error")

    # Retrieve memories for vertex skill
    retrieval = memory.retrieve_similar_memories("quad.graph.vertex", limit=3)

    assert len(retrieval.memories) > 0, "Should find memories"
    assert len(retrieval.memories) <= 3, "Should respect limit"
    assert len(retrieval.relevance_scores) == len(retrieval.memories), "Should have scores"

    # Most relevant should be from same skill
    assert retrieval.memories[0].skill_id == "quad.graph.vertex", "Most relevant should be same skill"

    print("✓ Retrieves similar memories")
    print(f"  Found: {len(retrieval.memories)} memories")
    print(f"  Relevance scores: {[f'{s:.2f}' for s in retrieval.relevance_scores]}")
    print(f"  Reason: {retrieval.retrieval_reason}")


def test_filters_by_event_type():
    """Test filtering memories by event type."""
    memory = EpisodicMemorySystem()

    # Store different types
    memory.store_struggle("quad.graph.vertex", "error", "Error 1")
    memory.store_struggle("quad.graph.vertex", "error", "Error 2")
    memory.store_breakthrough("quad.graph.vertex", "success", "Success 1")

    # Retrieve only struggles
    struggles = memory.retrieve_similar_memories("quad.graph.vertex", event_type="struggle")

    assert len(struggles.memories) == 2, "Should find 2 struggles"
    assert all(m.event_type == "struggle" for m in struggles.memories), "All should be struggles"

    # Retrieve only breakthroughs
    breakthroughs = memory.retrieve_similar_memories("quad.graph.vertex", event_type="breakthrough")

    assert len(breakthroughs.memories) == 1, "Should find 1 breakthrough"

    print("✓ Filters memories by event type")
    print(f"  Struggles: {len(struggles.memories)}")
    print(f"  Breakthroughs: {len(breakthroughs.memories)}")


def test_consolidates_to_long_term():
    """Test memory consolidation from short-term to long-term."""
    memory = EpisodicMemorySystem(short_term_capacity=5)

    # Store many important memories (more than capacity)
    for i in range(10):
        memory.store_milestone(
            skill_id=f"skill_{i}",
            milestone="achievement",
            description=f"Milestone {i}"
        )

    # Should have consolidated important memories
    assert len(memory.long_term_memory) > 0, "Should consolidate to long-term"
    assert memory.consolidation_count > 0, "Should track consolidations"

    # Short-term should be at capacity
    assert len(memory.short_term_memory) <= 5, "Short-term should respect capacity"

    print("✓ Consolidates to long-term memory")
    print(f"  Short-term: {len(memory.short_term_memory)}")
    print(f"  Long-term: {len(memory.long_term_memory)}")
    print(f"  Consolidations: {memory.consolidation_count}")


def test_generates_personalized_context():
    """Test generating personalized context from memories."""
    memory = EpisodicMemorySystem()

    # Build a learning history
    memory.store_struggle("quad.graph.vertex", "sign_error", "Struggled with sign in (x-h)")
    memory.store_struggle("quad.graph.vertex", "coordinate_swap", "Swapped x and y")
    memory.store_breakthrough("quad.graph.vertex", "mastery", "Mastered vertex identification")

    # Generate context
    context = memory.generate_personalized_context("quad.graph.vertex")

    assert len(context.similar_past_struggles) > 0, "Should reference past struggles"
    assert len(context.past_breakthroughs) > 0, "Should reference breakthroughs"
    assert len(context.motivational_references) > 0, "Should provide motivation"
    assert context.narrative, "Should build narrative"

    print("✓ Generates personalized context")
    print(f"  Past struggles: {len(context.similar_past_struggles)}")
    print(f"  Breakthroughs: {len(context.past_breakthroughs)}")
    print(f"  Motivational refs: {len(context.motivational_references)}")
    print(f"  Narrative: {context.narrative[:80]}...")


def test_narrative_adapts_to_history():
    """Test that narrative adapts based on learning history."""
    memory = EpisodicMemorySystem()

    # Test narrative with no history
    context_empty = memory.generate_personalized_context("quad.graph.vertex")
    assert "Starting fresh" in context_empty.narrative, "Should indicate fresh start"

    # Add only struggles
    memory.store_struggle("quad.graph.vertex", "error", "Struggled with concept")
    context_struggles = memory.generate_personalized_context("quad.graph.vertex")
    assert "work through this together" in context_struggles.narrative.lower(), "Should offer support"

    # Add breakthrough
    memory.store_breakthrough("quad.graph.vertex", "success", "Mastered the concept")
    context_mixed = memory.generate_personalized_context("quad.graph.vertex")
    assert "growth" in context_mixed.narrative.lower(), "Should acknowledge growth"

    print("✓ Narrative adapts to history")
    print(f"  Empty: {context_empty.narrative[:50]}...")
    print(f"  Struggles: {context_struggles.narrative[:50]}...")
    print(f"  Mixed: {context_mixed.narrative[:50]}...")


def test_memory_summary():
    """Test memory system summary statistics."""
    memory = EpisodicMemorySystem()

    # Add various memories
    memory.store_struggle("quad.graph.vertex", "error", "Error 1")
    memory.store_struggle("quad.graph.vertex", "error", "Error 2")
    memory.store_breakthrough("quad.graph.vertex", "success", "Success 1")
    memory.store_milestone("quad.graph.vertex", "achievement", "Milestone 1")

    summary = memory.get_memory_summary()

    assert summary["total_events"] == 4, "Should count all events"
    assert "event_types" in summary, "Should break down by type"
    assert "avg_importance" in summary, "Should calculate average importance"
    assert "emotional_balance" in summary, "Should track emotional balance"

    print("✓ Provides memory summary")
    print(f"  Total events: {summary['total_events']}")
    print(f"  Event types: {summary['event_types']}")
    print(f"  Avg importance: {summary['avg_importance']:.2f}")
    print(f"  Emotional balance: {summary['emotional_balance']:.2f}")


def test_learning_journey():
    """Test chronological learning journey extraction."""
    memory = EpisodicMemorySystem()

    # Create a sequence of events
    memory.store_struggle("quad.graph.vertex", "error", "Day 1: First struggle")
    time.sleep(0.01)
    memory.store_struggle("quad.graph.vertex", "error", "Day 2: Another error")
    time.sleep(0.01)
    memory.store_breakthrough("quad.graph.vertex", "success", "Day 3: Breakthrough!")
    time.sleep(0.01)
    memory.store_milestone("quad.graph.vertex", "mastery", "Day 4: Mastery achieved")

    journey = memory.get_learning_journey(limit=10)

    assert len(journey) == 4, "Should return all events"
    # Most recent should be first
    assert "Day 4" in journey[0]["description"], "Most recent should be first"
    assert "Day 1" in journey[-1]["description"], "Oldest should be last"

    print("✓ Provides learning journey")
    print(f"  Events: {len(journey)}")
    for i, event in enumerate(journey):
        print(f"    {i+1}. {event['event_type']}: {event['description'][:40]}")


def test_relevance_scoring():
    """Test that relevance scoring works correctly."""
    memory = EpisodicMemorySystem()

    # Store memories at different times
    memory.store_struggle("quad.graph.vertex", "error", "Old error")
    time.sleep(0.1)
    memory.store_struggle("quad.graph.vertex", "error", "Recent error")

    retrieval = memory.retrieve_similar_memories("quad.graph.vertex")

    # Recent memories should score higher
    assert retrieval.relevance_scores[0] >= retrieval.relevance_scores[1], \
        "Recent memories should be more relevant"

    print("✓ Relevance scoring works")
    print(f"  Recent score: {retrieval.relevance_scores[0]:.3f}")
    print(f"  Older score: {retrieval.relevance_scores[1]:.3f}")


def test_emotional_valence_tracking():
    """Test that emotional valence is tracked correctly."""
    memory = EpisodicMemorySystem()

    memory.store_struggle("quad.graph.vertex", "error", "Frustrating error")
    memory.store_milestone("quad.graph.vertex", "success", "Amazing achievement!")

    struggle = list(memory.short_term_memory)[0]
    milestone = list(memory.short_term_memory)[1]

    assert struggle.emotional_valence < 0, "Struggles should be negative"
    assert milestone.emotional_valence > 0, "Milestones should be positive"

    summary = memory.get_memory_summary()
    # Should be balanced (one negative, one positive)
    assert -1 <= summary["emotional_balance"] <= 1, "Should be within range"

    print("✓ Emotional valence tracked")
    print(f"  Struggle valence: {struggle.emotional_valence}")
    print(f"  Milestone valence: {milestone.emotional_valence}")
    print(f"  Overall balance: {summary['emotional_balance']:.2f}")


def test_skill_indexing():
    """Test that memories are indexed by skill for fast retrieval."""
    memory = EpisodicMemorySystem()

    memory.store_struggle("quad.graph.vertex", "error", "Vertex error")
    memory.store_struggle("quad.solve.by_factoring", "error", "Factoring error")
    memory.store_breakthrough("quad.graph.vertex", "success", "Vertex success")

    # Check index
    assert "quad.graph.vertex" in memory.skill_index, "Should index vertex skill"
    assert "quad.solve.by_factoring" in memory.skill_index, "Should index factoring skill"
    assert len(memory.skill_index["quad.graph.vertex"]) == 2, "Should have 2 vertex events"

    print("✓ Skill indexing works")
    print(f"  Skills tracked: {len(memory.skill_index)}")
    print(f"  Skills: {list(memory.skill_index.keys())}")


def test_tag_indexing():
    """Test that memories are indexed by tags."""
    memory = EpisodicMemorySystem()

    memory.store_struggle("quad.graph.vertex", "sign_error", "Sign error")
    memory.store_struggle("quad.standard.vertex", "sign_error", "Another sign error")

    # Check tag index
    assert "sign_error" in memory.tag_index, "Should index by error type"
    assert len(memory.tag_index["sign_error"]) == 2, "Should track both sign errors"

    print("✓ Tag indexing works")
    print(f"  Tags: {len(memory.tag_index)}")
    print(f"  Sign errors tracked: {len(memory.tag_index['sign_error'])}")


def test_motivational_references():
    """Test that system generates motivational references."""
    memory = EpisodicMemorySystem()

    # Build success history
    memory.store_breakthrough("quad.graph.vertex", "first_correct", "Got first question right!")
    memory.store_milestone("quad.graph.vertex", "mastery", "Reached 80% mastery")

    context = memory.generate_personalized_context("quad.graph.vertex")

    assert len(context.motivational_references) > 0, "Should generate motivation"

    # Check content
    motivation = context.motivational_references[0]
    assert "Remember when" in motivation or "overcome" in motivation.lower(), \
        "Should reference past success"

    print("✓ Generates motivational references")
    print(f"  References: {len(context.motivational_references)}")
    for ref in context.motivational_references:
        print(f"    - {ref}")


def test_handles_empty_retrieval():
    """Test that retrieval handles empty memory gracefully."""
    memory = EpisodicMemorySystem()

    # Try to retrieve from empty memory
    retrieval = memory.retrieve_similar_memories("quad.graph.vertex")

    assert len(retrieval.memories) == 0, "Should return empty list"
    assert "No memories" in retrieval.retrieval_reason, "Should explain why empty"

    print("✓ Handles empty retrieval gracefully")
    print(f"  Reason: {retrieval.retrieval_reason}")


if __name__ == "__main__":
    print("=" * 70)
    print("EPISODIC MEMORY SYSTEM ACCEPTANCE TESTS")
    print("=" * 70)
    print()

    # Run all tests
    test_initialization()
    print()

    test_stores_struggle_memories()
    print()

    test_stores_breakthrough_memories()
    print()

    test_stores_pattern_memories()
    print()

    test_stores_milestone_memories()
    print()

    test_retrieves_similar_memories()
    print()

    test_filters_by_event_type()
    print()

    test_consolidates_to_long_term()
    print()

    test_generates_personalized_context()
    print()

    test_narrative_adapts_to_history()
    print()

    test_memory_summary()
    print()

    test_learning_journey()
    print()

    test_relevance_scoring()
    print()

    test_emotional_valence_tracking()
    print()

    test_skill_indexing()
    print()

    test_tag_indexing()
    print()

    test_motivational_references()
    print()

    test_handles_empty_retrieval()
    print()

    print("=" * 70)
    print("ALL ACCEPTANCE TESTS PASSED ✓")
    print("=" * 70)
