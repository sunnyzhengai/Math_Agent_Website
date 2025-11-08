# Math Agent Platform - Project Plan

**Last Updated:** 2025-11-07
**Planning Principle:** Build evals first, then implement features
**Architecture:** Agentic (adaptive) + Deterministic (reliable)

---

## 🎯 Project Vision

Build an adaptive math learning platform where:
- **Students** get personalized learning paths without repetitive questions
- **Teachers** see actionable insights on student progress
- **System** continuously improves through agent experimentation

---

## 📊 Current State Assessment

### ✅ What's Working
- **Deterministic Components:**
  - Question templates (static pool, hand-vetted)
  - Grader (objective right/wrong)
  - Validators (schema enforcement)
  - Mastery math (Bayesian formulas)
  - Cycle mode (no-repeat question delivery)

- **Infrastructure:**
  - FastAPI backend (running on :8000)
  - Next.js frontend (running on :3001)
  - Agent framework (oracle, rules, random agents)
  - Eval harness (can compare agent strategies)
  - Telemetry logging

### ❌ Critical Issues
1. **Too few templates** - Only 2-3 per skill/difficulty (causes repetition)
2. **No template diversity tracking** - Can't measure improvement
3. **Simple planner** - Just threshold-based, not a full agent
4. **No hint system** - Students struggle without guidance
5. **No parameterization** - Can't generate infinite variations

### 🔧 Recent Fixes
- ✅ PostCSS config added (Tailwind now works)
- ✅ Quiz auto-completes when templates exhausted
- ✅ Diversity eval created (measures template coverage)

---

## 📅 Project Phases

### **PHASE 0: Foundation & Measurement** (Week 1-2)
> "You can't improve what you don't measure"

**Goal:** Establish eval infrastructure before building new features

#### 0.1 Expand Evaluation Suite ✅ STARTED
**Deliverables:**
- [x] Question diversity eval (DONE)
- [ ] Question uniqueness eval (no back-to-back repeats)
- [ ] Template coverage eval (all templates get used)
- [ ] Parameter variation eval (for future parameterized questions)
- [ ] Difficulty calibration eval (is "hard" actually hard?)

**Success Criteria:**
- All evals run in CI/CD
- Baseline metrics established for all 9 skills
- Dashboard showing eval results over time

**Implementation:**
```bash
# Create evals
evals/run_uniqueness_eval.py    # Check for consecutive duplicates
evals/run_coverage_eval.py      # Verify all templates are used
evals/run_variation_eval.py     # Measure parameter diversity
evals/run_calibration_eval.py   # Compare difficulty to empirical accuracy

# Add to CI
.github/workflows/evals.yml     # Run on every commit
```

**Timeline:** 3-4 days
**Dependencies:** None
**Risk:** Low - pure measurement, no feature changes

---

#### 0.2 Template Audit & Gap Analysis
**Deliverables:**
- Comprehensive report on template counts per skill/difficulty
- Identify skills with <5 templates (critical)
- Prioritize which skills need expansion first
- Document template quality issues (ambiguous wording, incorrect answers)

**Success Criteria:**
- Know exact template counts: `make audit-templates`
- Prioritized backlog of template expansion tasks
- Quality issues logged and triaged

**Implementation:**
```python
# tools/audit_templates.py
def audit_templates():
    """Generate report on template coverage."""
    for skill in SKILL_TEMPLATES:
        for difficulty in ["easy", "medium", "hard", "applied"]:
            count = len(SKILL_TEMPLATES[skill][difficulty])
            print(f"{skill}:{difficulty} → {count} templates")
            if count < 5:
                print(f"  ⚠️  CRITICAL: Needs expansion")
```

**Timeline:** 1-2 days
**Dependencies:** Diversity eval
**Risk:** Low - analysis only

---

### **PHASE 1: Content Scaling** (Week 3-5)
> "Fix the repetition problem by expanding the question pool"

**Goal:** Increase templates from 2-3 to 10+ per skill/difficulty

#### 1.1 Template Expansion - Critical Skills
**Deliverables:**
- Expand 3 most-used skills to 10+ templates each
  - `quad.graph.vertex` (currently 2 → target 10)
  - `quad.standard.vertex` (currently 3 → target 10)
  - `quad.roots.factored` (currently 2 → target 10)

**Success Criteria:**
- Diversity eval passes (>50% unique in 20 generations)
- No repetition in 10-question quizzes
- All templates validated by oracle agent (100% accuracy)

**Process:**
1. Write new templates following existing format
2. Run oracle agent to verify correctness
3. Run diversity eval to measure improvement
4. Manual review for quality
5. Merge to main

**Timeline:** 1 week (2-3 templates/day)
**Dependencies:** Template audit, oracle agent
**Risk:** Medium - requires domain expertise, QA time

---

#### 1.2 Template Expansion - Remaining Skills
**Deliverables:**
- Expand remaining 6 skills to 10+ templates each

**Success Criteria:**
- All skills pass diversity eval
- Students report no repetition in user testing
- Telemetry shows increased stem diversity

**Timeline:** 2 weeks
**Dependencies:** Phase 1.1
**Risk:** Medium - time-intensive

---

#### 1.3 Template Quality Assurance
**Deliverables:**
- Peer review process for new templates
- Style guide for template writing
- Automated quality checks (no typos, consistent formatting)

**Success Criteria:**
- 100% oracle accuracy maintained
- <5% template rejection rate in reviews
- Documentation for future template authors

**Timeline:** Parallel with 1.1 and 1.2
**Dependencies:** None
**Risk:** Low - process improvement

---

### **PHASE 2: Parameterized Generation** (Week 6-8)
> "From 10 templates to infinite variations"

**Goal:** Generate unlimited unique questions from templates

#### 2.1 Parameter System Design
**Deliverables:**
- Design doc for parameter system
- Template format with variable placeholders
- Parameter generation rules (ranges, constraints)

**Example:**
```python
# Before (static)
"Find the vertex of y = (x - 3)^2 + 2"

# After (parameterized)
template = "Find the vertex of y = (x - {h})^2 + {k}"
params = {
    "h": random.randint(-5, 5),
    "k": random.randint(-10, 10)
}
```

**Success Criteria:**
- Design reviewed and approved
- Backwards compatible with existing templates
- Clear parameter validation rules

**Timeline:** 3 days
**Dependencies:** None
**Risk:** Low - design phase

---

#### 2.2 Parameter Generator Implementation
**Deliverables:**
- `engine/parameters.py` - Parameter generation logic
- Distractor generation (wrong answer choices based on common errors)
- Validation that parameters create valid math problems

**Success Criteria:**
- Generate 100+ unique variations per template
- Oracle agent scores 100% on all generated questions
- Variation eval shows high diversity

**Implementation:**
```python
def generate_parameterized_item(template_id, seed):
    """Generate question with random parameters."""
    template = PARAM_TEMPLATES[template_id]
    params = generate_parameters(template.constraints, seed)
    stem = template.stem.format(**params)
    solution = template.solver(params)
    distractors = template.distractor_gen(params, solution)
    return create_item(stem, solution, distractors)
```

**Timeline:** 1 week
**Dependencies:** Design doc
**Risk:** Medium - math correctness critical

---

#### 2.3 Migrate Templates to Parameterized Format
**Deliverables:**
- Convert 3 pilot skills to parameterized templates
- A/B test: static vs. parameterized (same learning outcomes?)
- Documentation for migrating remaining skills

**Success Criteria:**
- No decrease in learning velocity
- 10x increase in unique questions per skill
- Students don't notice the change (seamless UX)

**Timeline:** 1 week
**Dependencies:** Parameter generator
**Risk:** High - could impact learning if bugs exist

---

### **PHASE 3: Adaptive Difficulty Agent** (Week 9-11)
> "Refactor planner into full agent with A/B testable strategies"

**Goal:** Personalize difficulty selection per student

#### 3.1 Difficulty Agent Evaluation Framework
**Deliverables:**
- Eval for comparing difficulty strategies
- Metrics: learning velocity, frustration rate, accuracy
- Replay system (test new strategies on historical data)

**Success Criteria:**
- Can replay 100+ historical student sessions
- Compare strategies without real student impact
- Clear winner criteria (e.g., 10% faster mastery)

**Timeline:** 3 days
**Dependencies:** Telemetry logs
**Risk:** Low - eval only

---

#### 3.2 Extract Current Logic into Agent
**Deliverables:**
- Refactor `engine/planner.py` into `agents/difficulty_agent.py`
- Implement "threshold_v1" strategy (current behavior)
- Maintain backwards compatibility

**Success Criteria:**
- Existing behavior unchanged (regression test)
- Code is cleaner, more testable
- Easy to add new strategies

**Implementation:**
```python
class ThresholdDifficultyAgent(Agent):
    """Current behavior: static thresholds."""
    name = "threshold_v1"

    def decide(self, context):
        p = context["mastery"]
        if p < 0.4: return ("easy", "Building confidence")
        if p <= 0.7: return ("medium", "Mixed practice")
        return ("hard", "Push challenge")
```

**Timeline:** 2 days
**Dependencies:** None
**Risk:** Low - refactoring only

---

#### 3.3 Implement Alternative Strategies
**Deliverables:**
- `adaptive_v1`: Adjust thresholds based on recent streak
- `confidence_v1`: Weight by student confidence scores
- `zopd_v1`: Zone of proximal development (target 70% accuracy)

**Success Criteria:**
- All strategies implemented and tested
- Replay eval shows measurable differences
- At least one strategy beats baseline

**Timeline:** 4 days
**Dependencies:** Agent framework, eval
**Risk:** Medium - new algorithms

---

#### 3.4 A/B Test in Production
**Deliverables:**
- Feature flag system for agent selection
- 20% of users get new strategy
- Monitor metrics: mastery gain, engagement, satisfaction

**Success Criteria:**
- No degradation in learning outcomes
- Winner strategy identified within 2 weeks
- Rollout to 100% if successful

**Timeline:** 2 weeks (monitoring period)
**Dependencies:** Phase 3.3
**Risk:** High - real user impact

---

### **PHASE 4: Learning Path Agent** (Week 12-15)
> "From manual skill selection to adaptive curriculum"

**Goal:** Automatically sequence skills for optimal learning

#### 4.1 Learning Path Evaluation Framework
**Deliverables:**
- Eval comparing learning path strategies
- Metrics: time to mastery, retention, prerequisite gaps
- Simulator for testing paths on synthetic students

**Success Criteria:**
- Can simulate 1000+ student learning journeys
- Identify optimal sequencing for skill progression
- Measure long-term retention (30-day follow-up)

**Timeline:** 5 days
**Dependencies:** Historical data
**Risk:** Medium - simulation complexity

---

#### 4.2 Learning Path Agent Implementation
**Deliverables:**
- `agents/learning_path_agent.py`
- Strategies:
  - `mastery_based`: Focus on weakest skills
  - `spaced_repetition`: Review at optimal intervals
  - `prerequisite_driven`: Build foundation first
  - `mixed`: Blend approaches

**Success Criteria:**
- All strategies produce valid learning sequences
- Simulator shows improvements over random selection
- Prerequisite enforcement never violated

**Implementation:**
```python
class LearningPathAgent(Agent):
    def select_next_skill(self, profile, skills, context):
        """Choose next skill to practice."""
        # Filter: only unlocked skills
        available = [s for s in skills if self.is_unlocked(s, profile)]

        # Strategy-specific selection
        return self.strategy(available, profile, context)
```

**Timeline:** 1 week
**Dependencies:** Eval framework
**Risk:** Medium - complex logic

---

#### 4.3 Rollout with Safety Guards
**Deliverables:**
- Gradual rollout: 10% → 50% → 100%
- Safety checks: must follow prerequisites
- Fallback to manual selection if agent fails

**Success Criteria:**
- No prerequisite violations logged
- Improved mastery trajectories
- Positive student feedback

**Timeline:** 2 weeks
**Dependencies:** Phase 4.2
**Risk:** High - changes core learning flow

---

### **PHASE 5: Hint System** (Week 16-18)
> "Provide scaffolded support when students struggle"

**Goal:** Help students without giving away answers

#### 5.1 Hint System Design & Eval
**Deliverables:**
- Design doc for hint levels (gentle → explicit)
- Eval: does hint lead to correct answer on next attempt?
- Error pattern analysis (common misconceptions)

**Success Criteria:**
- Clear hint progression: nudge → example → solution
- 60%+ success rate after receiving hint
- No direct answer reveals in Level 1-2 hints

**Timeline:** 3 days
**Dependencies:** Error telemetry
**Risk:** Low - design phase

---

#### 5.2 Rule-Based Hint Generation (v1)
**Deliverables:**
- Pre-written hints for common error patterns
- Triggered by incorrect answer + error tags
- 3-level hint system per skill

**Example:**
```python
# Student answers B for vertex question (correct is A)
# Error analysis: sign_error tag detected

hints = {
    "level_1": "Check the signs in the vertex form carefully.",
    "level_2": "In y = (x - h)^2 + k, the vertex is (h, k), not (-h, k).",
    "level_3": "Step-by-step: y = (x - 3)^2 + 2 has h=3, k=2, so vertex is (3,2)."
}
```

**Success Criteria:**
- 70%+ students answer correctly after Level 1-2 hint
- <10% need Level 3 (full solution)
- Positive user feedback on helpfulness

**Timeline:** 1 week
**Dependencies:** Error tagging system
**Risk:** Medium - requires domain expertise

---

#### 5.3 LLM Hint Generation (v2 - Future)
**Deliverables:**
- GPT-4 integration for dynamic hint generation
- Validation: hints never give direct answer
- Cost optimization (cache common hints)

**Success Criteria:**
- Comparable effectiveness to rule-based
- <$0.01 per hint (cost constraint)
- No hallucinations or incorrect math

**Timeline:** 1 week
**Dependencies:** Phase 5.2, LLM API access
**Risk:** High - LLM unpredictability

---

### **PHASE 6: Content Generation Agent** (Week 19-22)
> "From hand-written to AI-generated questions"

**Goal:** Infinite question generation with quality control

#### 6.1 LLM Question Generation Proof of Concept
**Deliverables:**
- Prompt engineering for question generation
- Validation pipeline (oracle must score 100%)
- Quality rubric (clarity, difficulty calibration)

**Example Prompt:**
```
Generate a {difficulty} quadratic vertex question.
Format: Multiple choice, 4 options, one correct.
Include common distractor errors.
Provide full solution explanation.
```

**Success Criteria:**
- Oracle agent scores 100% on all generated questions
- Human reviewers rate 80%+ as "would use"
- Diversity eval shows no duplication

**Timeline:** 5 days
**Dependencies:** OpenAI API, oracle agent
**Risk:** High - quality control critical

---

#### 6.2 Automated Validation Pipeline
**Deliverables:**
- Multi-stage validation before serving to students
  1. Oracle agent (correctness)
  2. Diversity check (uniqueness)
  3. Difficulty calibration (empirical testing)
  4. Human spot-check (10% sample)

**Success Criteria:**
- 99%+ questions pass oracle validation
- <1% false positive rate (correct question rejected)
- Pipeline runs in <5 seconds per question

**Timeline:** 4 days
**Dependencies:** Phase 6.1
**Risk:** Medium - automation complexity

---

#### 6.3 Limited Rollout with Human Review
**Deliverables:**
- Generate 100 questions across all skills
- Human expert review and approval
- A/B test: AI-generated vs. hand-written

**Success Criteria:**
- No quality complaints from students
- Learning outcomes equivalent to hand-written
- Cost <$0.50 per question (economical)

**Timeline:** 1 week
**Dependencies:** Validation pipeline
**Risk:** High - first AI content for students

---

## 📈 Success Metrics

### Learning Outcomes
- **Time to mastery:** Reduce by 20% (baseline: 30 min/skill)
- **Retention:** 80%+ accuracy 30 days after mastery
- **Engagement:** 50%+ students complete 5+ skills
- **Frustration rate:** <10% quit after repeated failures

### Technical Metrics
- **Question diversity:** 80%+ unique in 20-question sample
- **Template coverage:** All templates used within 50 questions
- **API latency:** <200ms for question generation
- **Agent accuracy:** Oracle 100%, Rules 85%+

### Business Metrics
- **User growth:** 100 active students by end of Phase 3
- **Completion rate:** 60%+ finish a full skill
- **Cost per question:** <$0.10 (including LLM costs)
- **Teacher satisfaction:** 4.5/5 stars on dashboard usefulness

---

## 🚨 Risk Management

### High-Risk Items
1. **Phase 2.3:** Parameterized migration could break learning
   - **Mitigation:** Extensive testing, gradual rollout, quick rollback
2. **Phase 3.4:** Difficulty agent A/B test affects real students
   - **Mitigation:** Safety guardrails, small cohort first, monitor closely
3. **Phase 6.3:** AI-generated questions could have errors
   - **Mitigation:** Human review, oracle validation, phased introduction

### Dependencies
- **LLM API access** (Phases 5.3, 6.x) - get approval early
- **Student cohort** for A/B testing - recruit by Phase 3
- **Domain expert** for template writing - allocate time in Phase 1

### Contingencies
- If Phase 2 (parameterization) fails → Continue template expansion manually
- If Phase 3 agents don't beat baseline → Keep current planner
- If Phase 6 (LLM generation) too expensive → Stick with parameterized templates

---

## 🎯 Milestones

### Month 1 (Weeks 1-4)
- ✅ Eval infrastructure complete
- ✅ Template audit done
- ✅ 3 critical skills expanded to 10+ templates
- 🎉 **Milestone:** No more repetition complaints

### Month 2 (Weeks 5-8)
- ✅ All skills have 10+ templates
- ✅ Parameterized generation working
- ✅ 100x increase in unique questions
- 🎉 **Milestone:** Infinite question variety

### Month 3 (Weeks 9-12)
- ✅ Difficulty agent rolled out
- ✅ Learning path agent deployed
- ✅ 20% improvement in learning velocity
- 🎉 **Milestone:** Truly adaptive system

### Month 4+ (Weeks 13-22)
- ✅ Hint system helping struggling students
- ✅ AI-generated content passing quality bar
- ✅ 100 active students, high satisfaction
- 🎉 **Milestone:** Production-ready platform

---

## 🔄 Iteration Process

### Weekly Cadence
- **Monday:** Review metrics, plan week's tasks
- **Wednesday:** Mid-week check-in, unblock issues
- **Friday:** Demo progress, run evals, retrospective

### Decision Points
After each phase, evaluate:
1. Did we hit success criteria?
2. What did we learn?
3. Should we continue, pivot, or skip next phase?

### Continuous Improvement
- Run full eval suite nightly
- Track metrics dashboard daily
- Student feedback reviewed weekly
- Quarterly architecture review

---

## 📚 Documentation Requirements

### For Each Phase
- [ ] Design doc (before implementation)
- [ ] API contracts (if endpoints change)
- [ ] Eval results (before and after)
- [ ] User guide updates (if UX changes)
- [ ] Runbook for rollback (if risky)

### Living Documents
- This project plan (update weekly)
- Architecture design (update when patterns change)
- Metrics dashboard (auto-updated)

---

## 🎓 Knowledge Transfer

### Key Roles
- **Agent Developer:** Implement new strategies, run evals
- **Content Creator:** Write templates, validate questions
- **DevOps:** Deploy, monitor, scale infrastructure
- **Product Manager:** Prioritize, measure outcomes, user research

### Handoff Checklist
- [ ] Code walkthrough (architecture, patterns)
- [ ] Demo all agents (how to add new strategies)
- [ ] Eval system tutorial (how to create new evals)
- [ ] Production access (monitoring, rollback procedures)

---

## ✅ Getting Started

### Today (Week 1, Day 1)
```bash
# 1. Run existing diversity eval
python3 evals/run_diversity_eval.py

# 2. Create uniqueness eval
cp evals/run_diversity_eval.py evals/run_uniqueness_eval.py
# Modify to check for consecutive duplicates

# 3. Audit templates
python3 tools/audit_templates.py > reports/template_audit_$(date +%F).txt

# 4. Prioritize skills for expansion
# Based on: most used + lowest template count
```

### This Week (Week 1)
- Complete Phase 0.1 (eval suite)
- Complete Phase 0.2 (template audit)
- Start Phase 1.1 (expand 3 critical skills)

### This Month (Weeks 1-4)
- Finish Phase 1 (all skills expanded)
- Begin Phase 2 (parameterization design)

---

## 📝 Notes

### Design Principles (from Architecture Doc)
1. **Eval First:** Build measurement before features
2. **Deterministic Core:** Grading, validation, auth must be 100% reliable
3. **Agentic Personalization:** Difficulty, paths, hints adapt per student
4. **Explainability:** All agent decisions logged with reasoning
5. **Safety:** Gradual rollouts, A/B tests, quick rollback capability

### Questions to Answer
- [ ] What's the ideal template count per skill? (Target: 10-15)
- [ ] How often should we A/B test new agents? (Suggestion: monthly)
- [ ] What's acceptable cost per question? (Target: <$0.10)
- [ ] When do we need human review? (All new content initially)

---

**Next Review:** End of Week 1
**Owner:** Update this plan based on learnings

