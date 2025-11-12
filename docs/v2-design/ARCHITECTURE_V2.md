# V2 Architecture: Neural Pathway Formation Engine

**Date:** November 12, 2025
**Status:** Design Phase
**Goal:** Build learning system from first principles of brain science

---

## What Changed From V1

### V1 (Template-Based System)
- Hand-crafted 190 question templates
- Deterministic progression (easy → medium → hard)
- Category-based navigation
- Delayed feedback (submit → check answer)
- Metrics tracking (accuracy, questions attempted)

### V2 (Neural Pathway Formation Engine)
- Infinite question generation (LLM + constraints)
- Mental model tracking (what student understands)
- Intent-based start (natural language)
- Instant feedback (< 500ms)
- Brain state monitoring (working memory, confidence, fatigue)

---

## Core Components

### 1. Mental Model Tracker

**Purpose:** Track student's internal understanding, not just performance metrics

**What it tracks:**
```
MentalModel {
    student_id: string

    // What student understands
    mastered_concepts: Set<Concept>

    // What student is confused about
    active_misconceptions: List<Misconception>

    // What student can do automatically (no thinking)
    automated_procedures: Set<Procedure>

    // What student is currently learning (requires conscious thought)
    learning_in_progress: Set<Concept>

    // Cognitive state
    working_memory_load: 0-7  // 7±2 rule
    confidence_level: 0-1
    fatigue_level: 0-1  // inferred from pace
}
```

**API:**
- `can_learn_new_concept()` → Is working memory available?
- `needs_break()` → Is student showing cognitive fatigue?
- `ready_for_challenge()` → Is student in flow state?

**Location:** `v2/core/mental_model.py`

---

### 2. Skill Graph (Lightweight)

**Purpose:** Represent skill relationships without heavy database

**Structure:**
```
SkillGraph {
    skills: Map<SkillId, Skill>

    Skill {
        id: string
        name: string
        description: string
        prerequisites: List<SkillId>
        concepts: List<Concept>
        mastery_criteria: MasteryCriteria
        template_styles: List<TemplateStyle>
        distractor_types: List<DistractorType>
        difficulty_constraints: Map<Difficulty, Constraints>
    }
}
```

**API:**
- `get_prerequisites(skill_id)` → All prerequisites (recursive)
- `find_next_skills(mastered)` → Skills with all prereqs met
- `find_by_concept(concept)` → All skills involving concept
- `get_learning_path(target_skill)` → Ordered path to target

**Storage:** JSON file, loaded into memory at startup

**Location:** `v2/core/skill_graph.py`

---

### 3. Question Generator (Infinite)

**Purpose:** Generate unlimited question variations matching student needs

**Pipeline:**
```
generate_question(skill, difficulty, context) {
    // 1. Load constraints
    constraints = skill.difficulty_constraints[difficulty]
    style = select_style(context)

    // 2. Generate with LLM (guided by structure)
    prompt = build_prompt(skill, difficulty, style, constraints)
    raw_question = llm.generate(prompt)

    // 3. Validate mathematics
    correct_answer = sympy_validate(raw_question)

    // 4. Generate distractors (misconception-based)
    distractors = generate_distractors(
        correct_answer,
        skill.distractor_types,
        difficulty
    )

    // 5. Quality check
    oracle_validates(question, correct_answer, distractors)
    diversity_check(question, recent_questions)

    // 6. Return structured question
    return Question(...)
}
```

**Key Features:**
- Schema-guided (not free-form LLM)
- SymPy validation (math correctness)
- Oracle validation (pedagogical quality)
- Diversity checking (no repeats)
- Misconception-mapped distractors

**Location:** `v2/core/question_generator.py`

---

### 4. Feedback Loop (< 500ms)

**Purpose:** Instant feedback to trigger dopamine release

**Flow:**
```
submit_answer(question_id, selected_choice) {
    // Instant grading (< 100ms)
    result = grade(question_id, selected_choice)

    if (result.correct) {
        feedback = celebrate()
        update_mental_model(student, "success")
        next_action = "next_question"
    } else {
        misconception = identify_misconception(selected_choice)
        feedback = explain_misconception(misconception)
        update_mental_model(student, "mistake", misconception)
        next_action = "provide_hint" or "easier_question"
    }

    return {
        result: result,
        feedback: feedback,
        next_action: next_action,
        latency: elapsed_ms  // Must be < 500ms
    }
}
```

**Performance Requirement:**
- Total latency < 500ms
- Grading: < 50ms
- Misconception analysis: < 100ms
- Feedback generation: < 200ms
- Next question prep: < 150ms

**Location:** `v2/core/feedback_loop.py`

---

### 5. Intent Understanding Agent

**Purpose:** Parse natural language to skill/context

**Examples:**
```
Input: "I'm learning completing the square"
Output: {
    skill_id: "quad.complete.square.solve",
    difficulty_signal: "beginner",
    urgency: "medium",
    context: "just started learning"
}

Input: [Paste: "Solve by completing the square: 2x² + 12x - 10 = 0"]
Output: {
    skill_id: "quad.complete.square.solve",
    difficulty_signal: "hard",  // has leading coefficient
    style: "teacher_standard",
    context: "match this format"
}
```

**Technology:**
- Claude Sonnet 3.5
- Few-shot prompting
- Structured output (JSON)

**Location:** `v2/agents/intent_agent.py`

---

### 6. Adaptive Coach Agent

**Purpose:** Real-time adaptation to student state

**Decision Logic:**
```
decide_next_action(session_state) {
    if (current_streak >= 5) {
        return "increase_difficulty"
    }

    if (wrong_in_row >= 3) {
        return "decrease_difficulty"
    }

    if (time_on_question > 120s) {
        return "offer_hint"
    }

    if (session_duration > 30min) {
        return "suggest_break"
    }

    if (mastery_achieved) {
        return "celebrate_and_summarize"
    }

    return "next_question_same_level"
}
```

**Location:** `v2/agents/coach_agent.py`

---

## Data Flow

### Session Start
```
1. Student: "I'm learning completing the square"
   ↓
2. Intent Agent: Parse → skill_id + context
   ↓
3. Mental Model: Load student's current state
   ↓
4. Skill Graph: Get skill spec + prerequisites
   ↓
5. Coach Agent: Decide starting point
   ↓
6. Question Generator: Create first question
   ↓
7. Return to student (< 2 seconds total)
```

### Answer Submission
```
1. Student submits answer
   ↓
2. Instant grading (< 50ms)
   ↓
3. Mental Model: Update (< 100ms)
   ↓
4. If wrong: Identify misconception (< 100ms)
   ↓
5. Coach Agent: Decide next action (< 100ms)
   ↓
6. Generate feedback + next question (< 200ms)
   ↓
7. Return to student (< 500ms total)
```

---

## Technology Stack

### Backend
- **Language:** Python 3.11+
- **Framework:** FastAPI (async, high performance)
- **LLM:** Anthropic Claude Sonnet 3.5
- **Math Validation:** SymPy
- **Data Storage:** PostgreSQL (student data) + JSON (skill specs)
- **Caching:** Redis (session state, generated questions)

### Frontend
- **Framework:** Next.js 14 (React)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **State Management:** React hooks + context
- **Real-time:** WebSocket for instant feedback

### Infrastructure
- **Hosting:** Render (backend + frontend)
- **Database:** Render PostgreSQL
- **Monitoring:** Built-in logging + telemetry

---

## API Design

### Session Endpoints

```
POST /v2/session/start
Body: {
    student_id: string,
    input: string  // Natural language or pasted question
}
Response: {
    session_id: string,
    skill_id: string,
    first_question: Question,
    mental_model_summary: string
}

POST /v2/session/{session_id}/submit
Body: {
    question_id: string,
    selected_choice: string,
    time_taken: number
}
Response: {
    result: "correct" | "incorrect",
    feedback: string,
    next_action: "next_question" | "hint" | "mastered",
    next_question?: Question,
    hint?: Hint,
    latency_ms: number
}

GET /v2/session/{session_id}/status
Response: {
    questions_attempted: number,
    questions_correct: number,
    current_streak: number,
    mastery_progress: MasteryProgress,
    session_duration_seconds: number
}
```

---

## Quality Assurance

### Question Validation Pipeline
1. **LLM Generation** → Raw question
2. **SymPy Validation** → Correct answer verified
3. **Oracle Agent** → Solves question, checks correctness
4. **Diversity Check** → Not too similar to recent questions
5. **Distractor Validation** → Each represents actual misconception
6. **Human Review** → Sample 10% for quality checks

### Performance Monitoring
- Track: Latency, error rates, LLM costs
- Alert if: Latency > 500ms, errors > 1%, costs spike
- Dashboard: Real-time session metrics

---

## What's Reused From V1

**Keep:**
- ✅ Skill taxonomy (20 skills)
- ✅ Template patterns (for distractor generation)
- ✅ Oracle agents (for validation)
- ✅ Julia's progress data (bootstrap mental model)

**Rewrite:**
- 🔄 Question delivery (static → generated)
- 🔄 Student tracking (metrics → mental model)
- 🔄 UI flow (categories → intent)
- 🔄 Feedback (delayed → instant)

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| LLM generates wrong math | High | SymPy + Oracle validation |
| High latency (> 500ms) | High | Caching, async processing |
| High LLM costs | Medium | Smart caching, rate limits |
| Question quality inconsistent | Medium | Human review sampling |
| Mental model inaccurate | Medium | Validation against test data |

---

## Success Metrics

### Learning Outcomes
- Time to mastery (target: < 50% of v1)
- Questions needed (target: adaptive, not fixed 20)
- Long-term retention (test 1 week later)
- Student satisfaction (Julia's feedback)

### System Performance
- Feedback latency (target: < 500ms, p99)
- Question quality (oracle pass rate > 95%)
- Diversity score (no similar questions in session)
- Cost per session (target: < $0.30)

---

## Next Steps

1. See `TRANSITION_PLAN.md` for implementation roadmap
2. See `MENTAL_MODEL_SPEC.md` for detailed mental model design
3. See `SKILL_GRAPH_SCHEMA.md` for skill specification format
