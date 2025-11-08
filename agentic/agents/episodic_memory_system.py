"""
Episodic Memory System: Long-term memory of student's learning journey.

Implements Lilian Weng's Memory Systems architecture:
- Short-term memory: Recent interactions (limited capacity)
- Long-term memory: Consolidated important events (unlimited)
- Episodic memory: Specific learning moments with context
- Memory consolidation: Moving important events to long-term
- Retrieval: Finding relevant memories based on current context

Memory types tracked:
- Struggle moments (errors, misconceptions)
- Breakthrough moments (aha moments, mastery)
- Pattern events (repeated errors, learning strategies)
- Milestone events (skill completions, achievements)
"""

from typing import Dict, List, Set, Any, NamedTuple, Optional
from collections import deque
import time
import hashlib


class MemoryEvent(NamedTuple):
    """A single memory event in the student's learning journey."""
    event_id: str
    timestamp: float
    event_type: str  # "struggle", "breakthrough", "pattern", "milestone"
    skill_id: str
    description: str
    context: Dict[str, Any]
    importance: float  # 0-1, how important this memory is
    emotional_valence: float  # -1 to 1, negative (struggle) to positive (success)
    tags: List[str]


class MemoryRetrieval(NamedTuple):
    """Result of memory retrieval with relevance scores."""
    memories: List[MemoryEvent]
    relevance_scores: List[float]
    retrieval_reason: str


class PersonalizedContext(NamedTuple):
    """Personalized context generated from memories."""
    similar_past_struggles: List[str]
    past_breakthroughs: List[str]
    learning_patterns: List[str]
    motivational_references: List[str]
    narrative: str


class EpisodicMemorySystem:
    """
    Manages student's episodic memory across learning sessions.

    Implements Lilian Weng's Memory Systems:
    - Separate short-term and long-term storage
    - Automatic consolidation of important memories
    - Context-aware retrieval
    - Personalized narrative generation
    """

    def __init__(self, short_term_capacity: int = 20):
        """
        Initialize episodic memory system.

        Args:
            short_term_capacity: Max items in short-term memory before consolidation
        """
        self.short_term_capacity = short_term_capacity

        # Short-term memory: Recent events (FIFO queue)
        self.short_term_memory: deque = deque(maxlen=short_term_capacity)

        # Long-term memory: Consolidated important events
        self.long_term_memory: List[MemoryEvent] = []

        # Index for fast retrieval
        self.skill_index: Dict[str, List[str]] = {}  # skill_id -> [event_ids]
        self.tag_index: Dict[str, List[str]] = {}    # tag -> [event_ids]

        # Statistics
        self.total_events_stored = 0
        self.consolidation_count = 0

    def store_struggle(
        self,
        skill_id: str,
        error_type: str,
        description: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store a struggle/error memory.

        Args:
            skill_id: Skill where struggle occurred
            error_type: Type of error (e.g., "sign_error", "conceptual_misunderstanding")
            description: Human-readable description
            context: Additional context (question_id, time_taken, etc.)

        Returns:
            Event ID of stored memory
        """
        event_id = self._generate_event_id("struggle", skill_id)

        memory = MemoryEvent(
            event_id=event_id,
            timestamp=time.time(),
            event_type="struggle",
            skill_id=skill_id,
            description=description,
            context=context or {},
            importance=0.7,  # Struggles are important for learning
            emotional_valence=-0.5,  # Negative (struggle)
            tags=["error", error_type, skill_id]
        )

        self._store_memory(memory)
        return event_id

    def store_breakthrough(
        self,
        skill_id: str,
        achievement: str,
        description: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store a breakthrough/success memory.

        Args:
            skill_id: Skill where breakthrough occurred
            achievement: What was achieved (e.g., "first_correct", "mastery_reached")
            description: Human-readable description
            context: Additional context

        Returns:
            Event ID of stored memory
        """
        event_id = self._generate_event_id("breakthrough", skill_id)

        memory = MemoryEvent(
            event_id=event_id,
            timestamp=time.time(),
            event_type="breakthrough",
            skill_id=skill_id,
            description=description,
            context=context or {},
            importance=0.9,  # Breakthroughs are very important
            emotional_valence=0.8,  # Very positive
            tags=["success", achievement, skill_id]
        )

        self._store_memory(memory)
        return event_id

    def store_pattern(
        self,
        pattern_type: str,
        description: str,
        related_skills: List[str],
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store a learning pattern observation.

        Args:
            pattern_type: Type of pattern (e.g., "repeated_error", "learning_strategy")
            description: Human-readable description
            related_skills: Skills involved in pattern
            context: Additional context

        Returns:
            Event ID of stored memory
        """
        event_id = self._generate_event_id("pattern", pattern_type)

        memory = MemoryEvent(
            event_id=event_id,
            timestamp=time.time(),
            event_type="pattern",
            skill_id=related_skills[0] if related_skills else "general",
            description=description,
            context={"related_skills": related_skills, **(context or {})},
            importance=0.8,  # Patterns are very important
            emotional_valence=0.0,  # Neutral
            tags=["pattern", pattern_type] + related_skills
        )

        self._store_memory(memory)
        return event_id

    def store_milestone(
        self,
        skill_id: str,
        milestone: str,
        description: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store a milestone achievement.

        Args:
            skill_id: Skill where milestone was reached
            milestone: Milestone type (e.g., "skill_completed", "level_up")
            description: Human-readable description
            context: Additional context

        Returns:
            Event ID of stored memory
        """
        event_id = self._generate_event_id("milestone", skill_id)

        memory = MemoryEvent(
            event_id=event_id,
            timestamp=time.time(),
            event_type="milestone",
            skill_id=skill_id,
            description=description,
            context=context or {},
            importance=1.0,  # Milestones are most important
            emotional_valence=1.0,  # Very positive
            tags=["milestone", milestone, skill_id]
        )

        self._store_memory(memory)
        return event_id

    def retrieve_similar_memories(
        self,
        skill_id: str,
        event_type: Optional[str] = None,
        limit: int = 5
    ) -> MemoryRetrieval:
        """
        Retrieve memories similar to current context.

        Args:
            skill_id: Current skill context
            event_type: Optional filter by event type
            limit: Max memories to return

        Returns:
            MemoryRetrieval with relevant memories and scores
        """
        # Search both short-term and long-term memory
        all_memories = list(self.short_term_memory) + self.long_term_memory

        if not all_memories:
            return MemoryRetrieval(
                memories=[],
                relevance_scores=[],
                retrieval_reason="No memories stored yet"
            )

        # Calculate relevance scores
        scored_memories = []
        for memory in all_memories:
            # Filter by event type if specified
            if event_type and memory.event_type != event_type:
                continue

            # Calculate relevance score
            relevance = self._calculate_relevance(memory, skill_id)
            scored_memories.append((memory, relevance))

        # Sort by relevance
        scored_memories.sort(key=lambda x: x[1], reverse=True)

        # Take top N
        top_memories = scored_memories[:limit]

        if not top_memories:
            return MemoryRetrieval(
                memories=[],
                relevance_scores=[],
                retrieval_reason=f"No memories found for {skill_id}"
            )

        memories = [m for m, _ in top_memories]
        scores = [s for _, s in top_memories]

        return MemoryRetrieval(
            memories=memories,
            relevance_scores=scores,
            retrieval_reason=f"Found {len(memories)} relevant memories for {skill_id}"
        )

    def generate_personalized_context(self, skill_id: str) -> PersonalizedContext:
        """
        Generate personalized context from memories for current skill.

        Args:
            skill_id: Current skill being practiced

        Returns:
            PersonalizedContext with narrative and references
        """
        # Retrieve different types of memories
        struggles = self.retrieve_similar_memories(skill_id, event_type="struggle", limit=3)
        breakthroughs = self.retrieve_similar_memories(skill_id, event_type="breakthrough", limit=3)
        patterns_retrieval = self.retrieve_similar_memories(skill_id, event_type="pattern", limit=2)

        # Extract descriptions
        past_struggles = [m.description for m in struggles.memories]
        past_breakthroughs = [m.description for m in breakthroughs.memories]
        learning_patterns = [m.description for m in patterns_retrieval.memories]

        # Generate motivational references
        motivational = []
        if breakthroughs.memories:
            most_recent_breakthrough = breakthroughs.memories[0]
            motivational.append(
                f"Remember when you {most_recent_breakthrough.description}? You can do this!"
            )

        if struggles.memories and breakthroughs.memories:
            motivational.append(
                f"You've overcome {len(struggles.memories)} challenges in similar topics before"
            )

        # Build narrative
        narrative = self._build_narrative(skill_id, struggles.memories, breakthroughs.memories)

        return PersonalizedContext(
            similar_past_struggles=past_struggles,
            past_breakthroughs=past_breakthroughs,
            learning_patterns=learning_patterns,
            motivational_references=motivational,
            narrative=narrative
        )

    def consolidate_memories(self):
        """
        Consolidate important short-term memories to long-term.

        This implements memory consolidation - moving important
        short-term memories to permanent long-term storage.
        """
        if len(self.short_term_memory) < self.short_term_capacity:
            return  # Not full yet

        # Evaluate importance of each short-term memory
        for memory in list(self.short_term_memory):
            # High importance memories get consolidated
            if memory.importance >= 0.7:
                # Move to long-term if not already there
                if memory.event_id not in [m.event_id for m in self.long_term_memory]:
                    self.long_term_memory.append(memory)
                    self.consolidation_count += 1

        # Short-term memory automatically removes oldest (deque maxlen)

    def get_memory_summary(self) -> Dict[str, Any]:
        """Get summary of memory system state."""
        all_memories = list(self.short_term_memory) + self.long_term_memory

        if not all_memories:
            return {
                "total_events": 0,
                "short_term_count": 0,
                "long_term_count": 0
            }

        event_types = {}
        for memory in all_memories:
            event_types[memory.event_type] = event_types.get(memory.event_type, 0) + 1

        return {
            "total_events": len(all_memories),
            "short_term_count": len(self.short_term_memory),
            "long_term_count": len(self.long_term_memory),
            "consolidation_count": self.consolidation_count,
            "event_types": event_types,
            "skills_tracked": len(self.skill_index),
            "avg_importance": sum(m.importance for m in all_memories) / len(all_memories),
            "emotional_balance": sum(m.emotional_valence for m in all_memories) / len(all_memories)
        }

    def get_learning_journey(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get chronological learning journey.

        Args:
            limit: Max events to return

        Returns:
            List of events in chronological order
        """
        all_memories = list(self.short_term_memory) + self.long_term_memory

        # Sort by timestamp (most recent first)
        sorted_memories = sorted(all_memories, key=lambda m: m.timestamp, reverse=True)

        journey = []
        for memory in sorted_memories[:limit]:
            journey.append({
                "timestamp": memory.timestamp,
                "event_type": memory.event_type,
                "skill_id": memory.skill_id,
                "description": memory.description,
                "emotional_valence": memory.emotional_valence
            })

        return journey

    # Private helper methods

    def _store_memory(self, memory: MemoryEvent):
        """Store memory in short-term and update indices."""
        self.short_term_memory.append(memory)
        self.total_events_stored += 1

        # Update indices
        if memory.skill_id not in self.skill_index:
            self.skill_index[memory.skill_id] = []
        self.skill_index[memory.skill_id].append(memory.event_id)

        for tag in memory.tags:
            if tag not in self.tag_index:
                self.tag_index[tag] = []
            self.tag_index[tag].append(memory.event_id)

        # Auto-consolidate if short-term is full
        if len(self.short_term_memory) >= self.short_term_capacity:
            self.consolidate_memories()

    def _generate_event_id(self, event_type: str, identifier: str) -> str:
        """Generate unique event ID."""
        data = f"{event_type}_{identifier}_{time.time()}_{self.total_events_stored}"
        return hashlib.md5(data.encode()).hexdigest()[:12]

    def _calculate_relevance(self, memory: MemoryEvent, current_skill: str) -> float:
        """
        Calculate relevance score for a memory.

        Factors:
        - Skill similarity (same skill = high relevance)
        - Recency (recent memories more relevant)
        - Importance (important memories more relevant)
        - Emotional valence (struggles for context, successes for motivation)
        """
        score = 0.0

        # Skill similarity (most important)
        if memory.skill_id == current_skill:
            score += 0.5
        elif current_skill in memory.tags:
            score += 0.3

        # Recency (exponential decay)
        age_hours = (time.time() - memory.timestamp) / 3600
        recency_score = 0.3 * (0.95 ** age_hours)  # Decay over time
        score += recency_score

        # Importance
        score += 0.2 * memory.importance

        return min(1.0, score)

    def _build_narrative(
        self,
        skill_id: str,
        struggles: List[MemoryEvent],
        breakthroughs: List[MemoryEvent]
    ) -> str:
        """Build narrative of learning journey for this skill."""
        if not struggles and not breakthroughs:
            return f"Starting fresh with {skill_id}. Let's learn together!"

        if breakthroughs and not struggles:
            return f"You've been doing great with {skill_id}! Keep up the excellent work."

        if struggles and not breakthroughs:
            most_recent_struggle = struggles[0]
            return (
                f"I see you've been working on {skill_id}. "
                f"You encountered {most_recent_struggle.description}. "
                f"Let's work through this together - persistence is key!"
            )

        # Both struggles and breakthroughs
        return (
            f"Your journey with {skill_id} has had ups and downs. "
            f"You've overcome {len(struggles)} challenges and achieved {len(breakthroughs)} breakthroughs. "
            f"That shows real growth! Let's keep building on that progress."
        )
