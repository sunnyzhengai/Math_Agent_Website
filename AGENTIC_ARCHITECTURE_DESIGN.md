# Agentic Math Learning Platform - Architecture Design

## Executive Summary

This document defines the architecture for an **adaptive math learning platform** that balances **agentic flexibility** (AI-driven personalization) with **deterministic reliability** (predictable, testable behavior).

**Key Principle:** Use agents where personalization matters, use deterministic systems where reliability matters.

---

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                            │
│                    (Next.js Frontend)                            │
│  [Student Dashboard] [Quiz Interface] [Progress View]           │
└───────────────────┬─────────────────────────────────────────────┘
                    │ HTTPS/REST
┌───────────────────┴─────────────────────────────────────────────┐
│                      API GATEWAY                                 │
│                    (FastAPI Backend)                             │
│  [Auth] [Rate Limiting] [Logging] [Error Handling]              │
└───────────────────┬─────────────────────────────────────────────┘
                    │
        ┌───────────┴──────────┐
        │                      │
┌───────▼──────────┐  ┌────────▼────────────────────────────────┐
│  DETERMINISTIC   │  │        AGENTIC COMPONENTS                │
│   COMPONENTS     │  │                                          │
│                  │  │  ┌────────────────────────────────────┐  │
│ • Templates      │  │  │    LEARNING PATH AGENT             │  │
│ • Grader         │  │  │  (Curriculum Sequencing)           │  │
│ • Validator      │  │  │  - Skill selection                 │  │
│ • Mastery Math   │  │  │  - Prerequisite checking           │  │
│                  │  │  │  - Adaptive pacing                 │  │
│                  │  │  └────────────────────────────────────┘  │
│                  │  │                                          │
│                  │  │  ┌────────────────────────────────────┐  │
│                  │  │  │    DIFFICULTY AGENT                │  │
│                  │  │  │  (Question Selection)              │  │
│                  │  │  │  - Mastery-based difficulty        │  │
│                  │  │  │  - Template selection              │  │
│                  │  │  │  - Repetition avoidance            │  │
│                  │  │  └────────────────────────────────────┘  │
│                  │  │                                          │
│                  │  │  ┌────────────────────────────────────┐  │
│                  │  │  │    HINT GENERATION AGENT           │  │
│                  │  │  │  (Scaffolding Support)             │  │
│                  │  │  │  - Error analysis                  │  │
│                  │  │  │  - Contextual hints                │  │
│                  │  │  │  - LLM-generated explanations      │  │
│                  │  │  └────────────────────────────────────┘  │
│                  │  │                                          │
│                  │  │  ┌────────────────────────────────────┐  │
│                  │  │  │    CONTENT GENERATION AGENT        │  │
│                  │  │  │  (Dynamic Question Creation)       │  │
│                  │  │  │  - Template-based generation       │  │
│                  │  │  │  - Parameter variation             │  │
│                  │  │  │  - Future: LLM generation          │  │
│                  │  │  └────────────────────────────────────┘  │
└──────────────────┘  └──────────────────────────────────────────┘
```

---

## Component Breakdown

### 🔒 DETERMINISTIC COMPONENTS (Pre-coded, Reliable, Testable)

These components must be **100% predictable** and are implemented with traditional code:

#### 1. **Question Templates** (`engine/templates.py`)
- **What:** Static pool of hand-crafted math questions
- **Why Deterministic:**
  - Quality control - every question is vetted
  - Consistency - same educational standards
  - Testability - can verify correctness
  - Safety - no hallucinated math
- **Current State:** ~2-3 templates per skill/difficulty (needs expansion)
- **Future:** Template-based generation with parameters

#### 2. **Grader** (`engine/grader.py`)
- **What:** Validates student answers, computes correctness
- **Why Deterministic:**
  - Must be objective and fair
  - No ambiguity in right/wrong
  - Auditable for disputes
  - Regression testable
- **Implementation:** Pure function comparing choice_id to solution

#### 3. **Validators** (`engine/validators.py`)
- **What:** Schema validation, input sanitization
- **Why Deterministic:**
  - Security - prevent injection
  - Data integrity - enforce contracts
  - Error handling - clear failures
- **Implementation:** Pydantic models, regex patterns

#### 4. **Mastery Mathematics** (`engine/mastery.py`)
- **What:** Bayesian update equations for skill mastery
- **Why Deterministic:**
  - Educational research-backed formulas
  - Reproducible results
  - Explainable to students/teachers
  - Testable with known inputs
- **Implementation:** Bayes rule with tuned priors

#### 5. **Data Layer** (Neo4j queries, Supabase auth)
- **What:** Database operations, authentication
- **Why Deterministic:**
  - ACID properties needed
  - Security requirements
  - Performance optimization
  - Compliance (COPPA, FERPA)

---

### 🤖 AGENTIC COMPONENTS (Adaptive, Personalized, Learnable)

These components should **adapt to individual students** and are implemented with agent patterns:

#### 1. **Learning Path Agent**
**Current:** `engine/planner.py` (simple rules)
**Future:** Full agent with strategy pattern

**Responsibilities:**
- Which skill to practice next?
- When to unlock prerequisites?
- When to review vs. advance?
- How to pace the curriculum?

**Why Agentic:**
- Different students need different paths
- Must adapt to learning patterns
- Can incorporate external context (time of day, recent performance)
- Benefits from experimentation (A/B testing strategies)

**Architecture:**
```python
class LearningPathAgent(Agent):
    def select_next_skill(
        self,
        student_profile: StudentProfile,
        skill_progress: List[SkillProgress],
        context: LearningContext
    ) -> SkillSelection:
        """
        Returns: (skill_id, reason, confidence)

        Strategies could include:
        - Mastery-based: practice weak skills
        - Spaced repetition: review at optimal intervals
        - Prerequisite-driven: build foundation first
        - Interest-based: follow student's chosen path
        - Mixed: blend multiple approaches
        """
        pass
```

**Evaluation:**
- Compare strategies on real student data
- Metrics: time to mastery, engagement, retention
- Guardrails: must follow prerequisites, must not overwhelm

---

#### 2. **Difficulty Agent**
**Current:** `engine/planner.py:plan_next_difficulty()` (threshold-based)
**Future:** Adaptive agent

**Responsibilities:**
- Choose question difficulty (easy/medium/hard/applied)
- Select which template from available pool
- Avoid recent repetitions
- Balance challenge with success rate

**Why Agentic:**
- Optimal difficulty varies per student
- Must consider momentum (streak) and confidence
- Can learn from past selections (what worked?)
- Room for experimentation (Thompson sampling, bandit algorithms)

**Architecture:**
```python
class DifficultyAgent(Agent):
    def select_question(
        self,
        skill_id: str,
        mastery: float,
        recent_history: List[Attempt],
        available_templates: Dict[Difficulty, List[Template]]
    ) -> QuestionSelection:
        """
        Returns: (difficulty, template_id, reason)

        Strategies:
        - Threshold-based (current): if p<0.4 → easy
        - Confidence-weighted: adjust for recent streaks
        - Zone of proximal development: just-right challenge
        - Thompson sampling: explore/exploit balance
        """
        pass
```

**Evaluation:**
- Measure: learning velocity, frustration rate, accuracy
- Compare strategies on A/B cohorts
- Guardrails: max 3 consecutive failures → easier

---

#### 3. **Hint Generation Agent**
**Current:** Not implemented
**Future:** LLM-powered or rule-based

**Responsibilities:**
- Provide scaffolded hints when student struggles
- Analyze incorrect answers for misconceptions
- Generate explanations for correct solutions
- Adapt explanation complexity to student level

**Why Agentic:**
- Every student needs different support
- Must analyze unique error patterns
- LLMs excel at natural language explanations
- Can personalize tone and examples

**Architecture:**
```python
class HintAgent(Agent):
    def generate_hint(
        self,
        question: QuestionItem,
        student_answer: str,
        attempt_count: int,
        student_profile: StudentProfile
    ) -> Hint:
        """
        Returns: (hint_text, hint_level, resources)

        Strategies:
        - Level 1: Gentle nudge ("Check your signs")
        - Level 2: Worked example of similar problem
        - Level 3: Step-by-step solution
        - Level 4: Video resource or formula sheet

        LLM Prompt Example:
        "Student incorrectly answered B for: {stem}
         Their mastery level is {level}.
         Generate a hint that guides without giving the answer."
        """
        pass
```

**Evaluation:**
- Did hint lead to correct answer on next attempt?
- Time to mastery improvement
- Student satisfaction surveys
- Guardrails: no direct answers, must explain reasoning

---

#### 4. **Content Generation Agent**
**Current:** `engine/templates.py:generate_item()` (template selection)
**Near-term:** Parameter variation
**Long-term:** LLM generation

**Responsibilities:**
- Generate new question variations
- Ensure mathematical correctness
- Maintain educational quality
- Create diverse problem contexts

**Why Agentic:**
- Need infinite question variety (current: 2-3 per skill!)
- Can leverage LLMs for creative problem contexts
- Learns what types of questions are effective
- Personalizes problem contexts (sports, cooking, video games)

**Architecture:**
```python
class ContentAgent(Agent):
    def generate_question(
        self,
        skill_id: str,
        difficulty: Difficulty,
        constraints: QuestionConstraints,
        student_interests: List[str]
    ) -> QuestionItem:
        """
        Phase 1: Template with parameters
        - Pick template: "Find vertex of y = a(x-h)²+k"
        - Vary parameters: a ∈ [-3,-1,1,2,3], h ∈ [-5..5], k ∈ [-10..10]
        - Generate distractors based on common errors

        Phase 2: LLM generation (future)
        - Prompt: "Generate a {difficulty} quadratic vertex problem"
        - Validate: Check answer with symbolic math
        - Evaluate: Test on oracle agent (must get 100%)
        """
        pass
```

**Evaluation:**
- Must pass oracle agent (100% correct grading)
- Diversity eval (no repetition)
- Difficulty calibration (empirical accuracy matches target)
- Guardrails: all generated questions validated before serving

---

## Decision Framework: Agentic vs. Deterministic

Use this decision tree:

```
Is the component responsible for RIGHT/WRONG judgments?
├─ YES → DETERMINISTIC (grader, validator, auth)
└─ NO → Continue

Does it need to be identical for all students?
├─ YES → DETERMINISTIC (templates, mastery math, schema)
└─ NO → Continue

Would personalization improve learning outcomes?
├─ YES → AGENTIC (difficulty selection, learning path, hints)
└─ NO → Continue

Do we have enough data to test different strategies?
├─ YES → AGENTIC (can evaluate in production)
└─ NO → DETERMINISTIC (implement simple version first)
```

---

## Agent Implementation Pattern

All agents follow this contract:

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, TypeVar, Generic

T = TypeVar('T')  # Return type varies by agent

class Agent(ABC, Generic[T]):
    """Base class for all adaptive agents."""

    name: str
    version: str

    @abstractmethod
    def decide(self, context: Dict[str, Any]) -> T:
        """Make a decision based on context."""
        pass

    def explain(self, decision: T, context: Dict[str, Any]) -> str:
        """Explain why this decision was made (for transparency)."""
        return f"Agent {self.name} decided: {decision}"

    def evaluate(self, decision: T, outcome: Any) -> float:
        """Score how good this decision was (for learning)."""
        return 0.0  # Override in subclass
```

### Agent Registry Pattern

```python
# agents/registry.py
from typing import Dict, Type
from .base import Agent
from .learning_path import LearningPathAgent
from .difficulty import DifficultyAgent
from .hint import HintAgent

AGENT_REGISTRY: Dict[str, Type[Agent]] = {
    "learning_path": LearningPathAgent,
    "difficulty": DifficultyAgent,
    "hint": HintAgent,
}

def get_agent(name: str, **config) -> Agent:
    """Factory to instantiate agents with configuration."""
    if name not in AGENT_REGISTRY:
        raise ValueError(f"Unknown agent: {name}")
    return AGENT_REGISTRY[name](**config)
```

---

## Data Flow: Deterministic + Agentic

### Example: Student requests next question

```
1. [DETERMINISTIC] API receives request
   ├─ Validate auth token (Supabase JWT)
   ├─ Rate limit check (10 req/min)
   └─ Validate request schema

2. [DETERMINISTIC] Load student data
   ├─ Query Neo4j: mastery values, recent attempts
   ├─ Compute: current streak, accuracy, time spent
   └─ Return: StudentProfile

3. [AGENTIC] Learning Path Agent decides skill
   ├─ Input: StudentProfile, available skills, prerequisites
   ├─ Strategy: "Spaced repetition" (recently configured)
   ├─ Output: skill_id="quad.graph.vertex", reason="Review before mastery decay"
   └─ Log decision for evaluation

4. [AGENTIC] Difficulty Agent chooses question
   ├─ Input: skill_id, mastery=0.65, recent_history=[✓,✓,✗]
   ├─ Strategy: "Adaptive threshold" with anti-repetition
   ├─ Output: difficulty="medium", template_id=7, reason="Maintain challenge"
   └─ Check: Ensure template_id not in last 5 questions

5. [DETERMINISTIC] Generate question
   ├─ Call: generate_item(skill_id, difficulty, seed=hash(user+timestamp))
   ├─ Shuffle choices deterministically
   ├─ Validate: schema compliance
   └─ Return: QuestionItem

6. [DETERMINISTIC] Log telemetry
   ├─ Record: agent decisions, latencies, question metadata
   ├─ Write to: logs/telemetry.jsonl
   └─ Enable: A/B analysis, agent evaluation

7. [DETERMINISTIC] Return to student
   ├─ JSON response with question
   ├─ Include: agent explanations (transparency)
   └─ Measure: API latency < 200ms
```

---

## Evaluation Infrastructure

### Agent Evaluation Loop

```python
# evals/agent_eval.py

def evaluate_agent_strategy(
    agent_name: str,
    strategy_name: str,
    cohort_size: int = 100,
    duration_days: int = 30
) -> EvalReport:
    """
    A/B test a new agent strategy against current baseline.

    Steps:
    1. Randomly assign students to control/test groups
    2. Control: uses baseline strategy
    3. Test: uses new strategy
    4. Collect outcomes: mastery gains, time to proficiency, engagement
    5. Statistical test: is new strategy significantly better?
    6. Guard: rollback if metrics degrade > 5%
    """
    pass
```

### Metrics by Agent Type

| Agent | Primary Metric | Secondary Metrics | Guardrails |
|-------|---------------|-------------------|------------|
| Learning Path | Time to skill mastery | Engagement, retention | Must respect prerequisites |
| Difficulty | Accuracy rate 60-80% | Frustration rate, completion | Max 3 consecutive fails |
| Hint | Post-hint success rate | Time saved, satisfaction | No direct answers |
| Content Gen | Question diversity | Oracle accuracy 100% | All questions validated |

---

## Migration Path: Current → Agentic

### Phase 1: Extract Current Logic into Agents ✅ (Partially Done)

```python
# Current: Hardcoded thresholds
def plan_next_difficulty(p: float) -> Difficulty:
    if p < 0.4: return "easy"
    if p <= 0.7: return "medium"
    return "hard"

# Refactor: Agent with strategy
class ThresholdDifficultyAgent(Agent):
    name = "threshold_v1"

    def decide(self, context):
        p = context["mastery"]
        if p < 0.4: return ("easy", "Building confidence")
        if p <= 0.7: return ("medium", "Mixed practice")
        return ("hard", "Push challenge")
```

### Phase 2: Add Alternative Strategies

```python
class AdaptiveDifficultyAgent(Agent):
    """Adjusts thresholds based on recent performance."""
    name = "adaptive_v1"

    def decide(self, context):
        p = context["mastery"]
        streak = context["recent_streak"]

        # If on hot streak, push harder
        if streak >= 5:
            return self._select_harder(p)

        # If struggling, ease up
        if streak <= -3:
            return self._select_easier(p)

        # Default thresholds
        return self._select_default(p)
```

### Phase 3: Evaluation & Selection

```python
# evals/difficulty_eval.py

def compare_difficulty_strategies():
    """Test multiple strategies on historical data."""

    strategies = [
        "threshold_v1",    # Baseline
        "adaptive_v1",     # Streak-aware
        "confidence_v1",   # Confidence-weighted
        "zopd_v1",         # Zone of proximal development
    ]

    for strategy in strategies:
        agent = get_agent("difficulty", strategy=strategy)
        results = replay_student_sessions(agent)
        report_metrics(strategy, results)

    # Output: Which strategy maximizes learning velocity?
```

### Phase 4: Production A/B Testing

```python
# api/app/services/learning.py

def get_next_question(student_id: str):
    # Feature flag determines which agent version
    agent_version = ab_test_assignment(student_id, "difficulty_agent")

    agent = get_agent("difficulty", version=agent_version)
    decision = agent.decide(context)

    # Log for later analysis
    log_agent_decision(student_id, agent_version, decision)

    return generate_question(decision)
```

---

## Implementation Priorities

### ✅ Already Implemented
1. Base agent infrastructure (oracle, rules, random)
2. Eval harness for agent comparison
3. Deterministic question generation (template-based)
4. Grading and mastery math

### 🚧 In Progress
1. Diversity eval (just created!)
2. Modern Next.js UI (needs PostCSS fix)

### 🎯 Next Steps (Priority Order)

#### Immediate (Fix Current Pain Points)
1. **Expand question templates** - Add 10+ templates per skill/difficulty
   - Fixes repetition issue you experienced
   - Deterministic, safe, high-impact
   - Use diversity eval to track progress

2. **Anti-repetition system** - Track last N questions
   - Simple deterministic filter
   - Prevents back-to-back duplicates
   - Low complexity, high UX impact

#### Short-term (Better Personalization)
3. **Refactor planner into DifficultyAgent**
   - Extract current logic
   - Add alternative strategies
   - Enable A/B testing

4. **Learning Path Agent**
   - Skill selection logic
   - Prerequisite management
   - Spaced repetition

#### Medium-term (Content Scaling)
5. **Parameterized question generation**
   - Templates with variable coefficients
   - Generates 100s of unique questions per template
   - Validated by oracle agent

6. **Hint system v1** (rule-based)
   - Common error patterns
   - Pre-written hints per misconception
   - No LLM needed yet

#### Long-term (Advanced Features)
7. **LLM Hint Agent**
   - Dynamic explanation generation
   - Personalized to student level
   - Cost-optimized (cache common hints)

8. **LLM Content Generation**
   - Generate novel question contexts
   - Validate with symbolic math
   - Oracle agent must score 100%

---

## Risk Mitigation

### Agent Risks & Guards

| Risk | Mitigation |
|------|-----------|
| Agent makes bad decisions | Always log decisions; enable rollback; A/B test before full deploy |
| LLM generates wrong math | Validate all LLM output with deterministic grader; oracle must score 100% |
| Agent creates unfair experience | Evaluation metrics must include equity checks; compare across demographics |
| System becomes too complex | Each agent has single responsibility; clear interfaces; comprehensive tests |
| Can't explain decisions to stakeholders | All agents must implement `explain()` method; decisions logged with reasoning |

### Fallback Strategy

Every agentic component must have a deterministic fallback:

```python
def get_next_question_safe(student_id: str):
    try:
        # Try agentic path
        agent = get_agent("learning_path")
        skill = agent.select_skill(student_profile)
    except Exception as e:
        log_error("agent_failure", e)
        # Fallback: deterministic round-robin
        skill = select_skill_round_robin(student_profile)

    return generate_question(skill)
```

---

## Summary: The Agentic Philosophy

**Agentic components** = Personalization, Adaptation, Experimentation
- Where students differ (learning paths, hint needs, interests)
- Where we can test and improve (A/B tests, strategy evolution)
- Where explainability is key (agent decisions logged and explained)

**Deterministic components** = Reliability, Fairness, Trust
- Where correctness matters (grading, validation, auth)
- Where consistency matters (mastery math, question quality)
- Where auditability matters (compliance, disputes, research)

**The balance:**
```
                 Agentic
                    ↑
                    |
    Personalized ---|--- Predictable
                    |
                    ↓
               Deterministic
```

Agents choose the path, deterministic systems execute it reliably.

---

**Version:** 1.0
**Last Updated:** 2025-11-07
**Status:** Living document - update as architecture evolves
