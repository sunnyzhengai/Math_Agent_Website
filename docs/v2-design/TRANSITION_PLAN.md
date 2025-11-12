# V1 to V2 Transition Plan

**Date:** November 12, 2025
**Strategy:** Dual-track development with gradual migration
**Timeline:** 4-6 weeks to v2 MVP

---

## Overview

We're NOT replacing v1 immediately. We're running **parallel tracks**:
- **V1:** Production system, maintenance mode, Julia's daily use
- **V2:** New architecture, active development, weekend testing

---

## Git Strategy

### Branch Structure

```
Repository: Agent_Math

Branches:
├── main (or keep as phase1-data-flywheel)
│   └── Stable, deployed to production
│
├── v1-template-based (NEW - Archive)
│   └── Snapshot of v1 before v2 work started
│   └── Frozen reference, no active development
│
├── phase1-data-flywheel (CURRENT)
│   └── V1 production branch
│   └── Maintenance only: bug fixes, keep Julia's experience stable
│
└── v2-neural-engine (NEW - Active Development)
    └── New architecture
    └── All v2 development happens here
```

### Creating Branches

```bash
# 1. Archive current v1 state
git checkout phase1-data-flywheel
git checkout -b v1-template-based
git push origin v1-template-based
# → Frozen snapshot for reference

# 2. Create v2 development branch
git checkout phase1-data-flywheel
git checkout -b v2-neural-engine
git push origin v2-neural-engine
# → Active development

# 3. phase1-data-flywheel stays as production maintenance
```

---

## Repository Structure (After Restructure)

```
/Agent_Math
│
├── v1/  (Move current implementation here)
│   ├── api/               (FastAPI backend)
│   ├── engine/            (Templates, grading)
│   ├── math-learning-platform/  (Next.js frontend)
│   ├── agentic/           (Existing agents)
│   └── README-v1.md       (V1 documentation)
│
├── v2/  (New architecture)
│   ├── docs/              (V2-specific documentation)
│   ├── core/              (Mental model, skill graph, etc.)
│   ├── agents/            (Intent, coach, generator agents)
│   ├── api/               (New FastAPI design)
│   ├── frontend/          (New Next.js app)
│   └── tests/             (V2 test suite)
│
├── shared/  (Code used by both v1 and v2)
│   ├── models/            (Student, skill types)
│   ├── utils/             (Common utilities)
│   └── config/            (Shared configuration)
│
├── docs/
│   ├── v1/                (V1 documentation)
│   └── v2-design/         (V2 design documents)
│
├── README.md              (Explains dual-track approach)
└── CONTRIBUTING.md        (Development guidelines)
```

---

## Development Phases

### Phase 0: Housekeeping (Week 1, Day 1-2)

**Goals:**
- ✅ Document first principles
- ✅ Create branch structure
- ✅ Restructure repository
- ✅ Update README

**Tasks:**
1. Create `docs/v2-design/` folder
2. Write FIRST_PRINCIPLES_ANALYSIS.md
3. Write ARCHITECTURE_V2.md
4. Write TRANSITION_PLAN.md (this document)
5. Create v1-template-based branch (archive)
6. Create v2-neural-engine branch (development)
7. Restructure repo (v1/, v2/, shared/)
8. Update main README.md
9. Commit all documentation

**Deliverable:** Clean structure, clear documentation, no code changes yet

---

### Phase 1: Foundation (Week 1, Day 3-7)

**Goals:**
- Design detailed specs for core components
- No implementation yet, just design documents

**Tasks:**

1. **Mental Model Specification**
   - File: `docs/v2-design/MENTAL_MODEL_SPEC.md`
   - Define exact data structure
   - Define update logic
   - Define query APIs

2. **Skill Graph Schema**
   - File: `docs/v2-design/SKILL_GRAPH_SCHEMA.md`
   - Define JSON schema for skills
   - Example skill spec (completing the square)
   - Validation rules

3. **Question Generation Protocol**
   - File: `docs/v2-design/QUESTION_GENERATION.md`
   - LLM prompts
   - Validation pipeline
   - Distractor generation logic

4. **API Specification**
   - File: `docs/v2-design/API_SPEC_V2.md`
   - Endpoint definitions
   - Request/response schemas
   - Error handling

**Deliverable:** Complete design documents, ready to implement

---

### Phase 2: Core Implementation (Week 2-3)

**Goals:**
- Implement core components (no UI yet)
- Unit tests for each component
- Integration tests

**Tasks:**

**Week 2:**
1. Implement Mental Model Tracker (`v2/core/mental_model.py`)
2. Implement Skill Graph (`v2/core/skill_graph.py`)
3. Create skill spec for 1 skill (completing the square)
4. Unit tests for mental model
5. Unit tests for skill graph

**Week 3:**
6. Implement Question Generator (`v2/core/question_generator.py`)
7. Integrate LLM (Claude API)
8. Integrate SymPy validation
9. Integrate Oracle validation (reuse from v1)
10. Generate 10 test questions, validate quality
11. Unit tests for generator

**Deliverable:** Core engine working, can generate valid questions

---

### Phase 3: API Layer (Week 3-4)

**Goals:**
- Build FastAPI endpoints
- Session management
- Instant feedback loop

**Tasks:**

1. Set up FastAPI project (`v2/api/`)
2. Implement session start endpoint
3. Implement answer submission endpoint
4. Implement mental model tracking
5. Add caching (Redis)
6. Performance optimization (< 500ms target)
7. API tests
8. Load testing

**Deliverable:** Working API, can be tested with curl/Postman

---

### Phase 4: Minimal UI (Week 4-5)

**Goals:**
- Build simplest possible UI to test with Julia
- Focus on core experience, not polish

**Tasks:**

1. Set up Next.js project (`v2/frontend/`)
2. Build landing page (natural language input)
3. Build quiz interface (question → answer → feedback)
4. Build progress display
5. Connect to API
6. Deploy to v2-preview.themathagent.com

**Deliverable:** Functional UI, ready for Julia to test

---

### Phase 5: Real-World Testing (Week 5-6)

**Goals:**
- Julia tests v2 on weekends
- Measure vs v1
- Iterate based on feedback

**Tasks:**

1. Julia tries v2 for 1 skill (completing the square)
2. Collect data:
   - Time to mastery
   - Questions needed
   - Satisfaction (ask Julia!)
   - Long-term retention (test 1 week later)
3. Compare to v1 baseline
4. Iterate on question quality
5. Iterate on feedback loop
6. Iterate on UI flow

**Deliverable:** Validated approach, data showing improvement

---

### Phase 6: Expansion (Week 6+)

**Goals:**
- Add more skills
- Polish UI
- Prepare for full migration

**Tasks:**

1. Add 4 more skills (Julia's current curriculum)
2. Polish UI design
3. Add session summaries
4. Add metacognitive reflections
5. Performance monitoring
6. Cost optimization

**Deliverable:** V2 ready for primary use

---

## Deployment Strategy

### Current State (V1)
```
Production: themathagent.com → v1
Branch: phase1-data-flywheel
Julia uses: Daily
```

### During Development (Dual-Track)
```
Production: themathagent.com → v1 (stable)
Preview: v2-preview.themathagent.com → v2 (experimental)

Julia uses:
- Weekdays: v1 (homework support, reliable)
- Weekends: v2 (testing, feedback)
```

### After Validation (Migration)
```
Production: themathagent.com → v2
Archive: v1.themathagent.com → v1 (for reference)

Julia uses: v2 exclusively
```

---

## What to Preserve From V1

### Data to Migrate
✅ **Julia's progress data**
- Questions attempted/correct
- Time spent per skill
- Historical performance
- Use to bootstrap v2 mental model

✅ **Skill taxonomy**
- 20 skill definitions
- Prerequisite relationships
- Becomes v2 skill graph

✅ **Template patterns**
- Mine for distractor types
- Common misconceptions
- Use to inform v2 question generation

### Code to Reuse
✅ **Oracle agents** (`v1/agentic/agents/oracle.py`)
- Use for v2 question validation

✅ **Skill IDs and types** (`v1/api/models/`)
- Reuse in v2 shared models

✅ **Authentication** (if implemented)
- Reuse in v2

### Code to Rewrite
🔄 **Question generation** (static → dynamic)
🔄 **Student tracking** (metrics → mental model)
🔄 **UI flow** (categories → intent)
🔄 **Feedback loop** (delayed → instant)

---

## Risk Management

### Risk 1: V2 Takes Longer Than Expected
**Mitigation:** Keep v1 running, no pressure to switch
**Fallback:** Julia continues using v1 indefinitely if needed

### Risk 2: V2 Doesn't Perform Better
**Mitigation:** A/B test before full migration
**Fallback:** Abandon v2, continue improving v1

### Risk 3: High LLM Costs
**Mitigation:** Aggressive caching, rate limits
**Fallback:** Hybrid approach (templates + generation)

### Risk 4: Question Quality Issues
**Mitigation:** Oracle validation, human review
**Fallback:** Use v1 templates as fallback

### Risk 5: Julia Doesn't Like V2
**Mitigation:** Iterate based on her feedback
**Fallback:** Keep v1 as her primary, v2 as experiment

---

## Success Criteria

### Must Have (Before Migration)
- ✅ Question generation quality ≥ v1 templates
- ✅ Feedback latency < 500ms (p99)
- ✅ Julia prefers v2 over v1
- ✅ Cost per session < $0.50
- ✅ No critical bugs

### Nice to Have (Can Add Post-Launch)
- Spaced repetition
- Multiple students
- Teacher dashboard
- Advanced analytics

---

## Communication Plan

### With Julia (User Testing)
- Week 1: "We're redesigning the practice system from scratch"
- Week 4: "Want to try the new version this weekend?"
- Week 5: "Which one do you like better? Why?"
- Week 6: "Ready to switch to the new version full-time?"

### Documentation Updates
- Keep v1 README updated (maintenance mode)
- Update main README with dual-track status
- Add v2 development progress (this document)

---

## Decision Points

### Week 2 Checkpoint
**Question:** Is the core architecture sound?
**Criteria:** Mental model + skill graph + generator all work independently
**Go/No-Go:** If fundamentals broken, revisit design before continuing

### Week 4 Checkpoint
**Question:** Is the API performant?
**Criteria:** < 500ms latency, questions validate correctly
**Go/No-Go:** If performance issues, optimize before building UI

### Week 6 Checkpoint
**Question:** Does Julia like it better than v1?
**Criteria:** Julia's qualitative feedback, learning metrics
**Go/No-Go:** If Julia prefers v1, rethink approach

---

## Current Status

**Phase:** 0 - Housekeeping
**Date:** November 12, 2025
**Completed:**
- ✅ FIRST_PRINCIPLES_ANALYSIS.md
- ✅ ARCHITECTURE_V2.md
- ✅ TRANSITION_PLAN.md (this document)

**Next:**
- [ ] Create branch structure
- [ ] Restructure repository
- [ ] Update main README
- [ ] Commit documentation
- [ ] Begin Phase 1 design documents

---

## Questions & Decisions Log

| Date | Question | Decision | Rationale |
|------|----------|----------|-----------|
| 2025-11-12 | New repo or same repo? | Same repo, dual-track | Easier to reference v1, share code |
| 2025-11-12 | Throw away v1? | No, keep running | Julia needs stable system |
| 2025-11-12 | Start coding now? | No, design first | Get architecture right before implementing |

---

## Resources

- **V1 System:** `/Agent_Math/v1/`
- **V2 Design:** `/Agent_Math/docs/v2-design/`
- **Shared Code:** `/Agent_Math/shared/`
- **This Document:** `/Agent_Math/docs/v2-design/TRANSITION_PLAN.md`

---

**Last Updated:** November 12, 2025
**Next Review:** After Phase 1 completion (Week 1)
