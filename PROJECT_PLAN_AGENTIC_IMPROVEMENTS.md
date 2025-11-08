# Agentic System Improvements - Project Plan

**Based on:** Andrew Ng's Agentic Design Patterns Code Review
**Current Agentic Maturity:** 1.5/5.0
**Target Maturity:** 4.0/5.0
**Timeline:** 8-10 weeks (3 phases)

---

## Executive Summary

The Agent_Math platform has excellent engineering foundations but operates at only 20% of its agentic potential. This plan transforms the system from a **template-based question bank** into a **truly adaptive learning system** by implementing Andrew Ng's 5 core agentic patterns:

1. ✅ **Reflection** - Agents self-critique and iteratively improve
2. ✅ **Tool Use** - Effective use of external resources and validation
3. ✅ **Planning** - Multi-step planning before execution
4. ✅ **Multi-Agent Collaboration** - Specialized agents working together
5. ✅ **Iterative Refinement** - Multiple passes to improve quality

---

## Current State Assessment

### Strengths ✅
- 14 comprehensive evaluation scripts
- Oracle Agent using Claude API for validation
- Strong parameterized question generation (9 skills)
- Robust grading and mastery tracking
- Excellent telemetry infrastructure

### Critical Gaps ❌
- **No Reflection:** Everything is one-shot (no self-critique)
- **No Planning:** Threshold logic, not true multi-step planning
- **No Multi-Agent Collaboration:** Agents work in isolation
- **No Iterative Refinement:** No improvement loops
- **Evals Don't Improve:** Measurement without action

### Key Insight
> "The system uses AI for **validation** (Oracle Agent), but not for **generation, reflection, or collaboration**."

---

## Success Metrics

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| Oracle Accuracy | 100% | 100%* | *with reflection catches answer key errors |
| Explanation Quality | 7.0/10 | 9.0/10 | explanation_quality_eval avg score |
| Question Diversity | 60% | 85% | diversity_eval unique stems |
| Student Time to Mastery | Baseline | -20% | Average attempts until mastery |
| Question Validation Rate | ~85% | 95% | Questions passing all validation agents |
| System Self-Correction | 0% | 80% | Evals triggering auto-improvements |

---

## Phase 1: Quick Wins (Weeks 1-2)

**Goal:** Immediate quality improvements with minimal architecture changes
**Pattern Focus:** Reflection + Multi-Agent Collaboration

### Task 1.1: Add Reflection to Oracle Agent ⭐ HIGH PRIORITY

**Objective:** Oracle Agent self-critiques answers and validates with multiple solving approaches.

**Implementation:**
```python
# File: agentic/agents/oracle.py

class OracleAgent:
    def choose_with_reflection(self, item: Dict[str, Any]) -> str:
        """Solve with reflection and cross-validation."""

        # ATTEMPT 1: Initial solve
        solution_1 = self._solve_once(item)

        # REFLECTION: Check confidence
        confidence = self._assess_confidence(item, solution_1)

        if confidence < 0.9:
            # ATTEMPT 2: Solve with different approach
            solution_2 = self._solve_alternate_method(item)

            if solution_1 != solution_2:
                # DEBATE: Which reasoning is stronger?
                final = self._resolve_disagreement(item, solution_1, solution_2)
                return final

            return solution_2

        return solution_1
```

**Validation Criteria:**
- [ ] Oracle maintains 100% accuracy on correctness_eval
- [ ] Catches at least 1 answer key error (if seeded into test)
- [ ] Logs confidence scores for monitoring
- [ ] Adds <5s latency to correctness_eval runtime

**Acceptance Test:**
```bash
python3 evals/run_correctness_eval.py
# Should pass with 100% accuracy
# Should log reflection events in telemetry
```

**Commit Message:**
```
Add reflection to Oracle Agent for self-validation

Implements Andrew Ng's Reflection pattern:
- Oracle solves problems twice if low confidence (<0.9)
- Uses alternate solving methods for cross-validation
- Resolves disagreements through reasoning comparison
- Catches potential answer key errors before production

Impact: Improved reliability and error detection
Pattern: Reflection (Andrew Ng Agentic Design)
```

---

### Task 1.2: Multi-Agent Question Validation Committee ⭐ HIGH PRIORITY

**Objective:** Multiple specialized agents validate each generated question before it goes live.

**Implementation:**
```python
# File: agentic/agents/question_validation_committee.py

class QuestionValidationCommittee:
    """Multi-agent system for collaborative question validation."""

    def __init__(self):
        self.oracle_agent = OracleAgent()           # Correctness
        self.clarity_agent = ClarityAgent()         # Readability
        self.difficulty_agent = DifficultyAgent()   # Calibration
        self.distractor_agent = DistractorAgent()   # Wrong answer quality

    def validate_question(self, question: QuestionItem) -> ValidationResult:
        """All agents must approve. Returns detailed feedback."""

        # AGENT 1: Correctness validation
        oracle_result = self.oracle_agent.solve(question)
        if not oracle_result.correct:
            return ValidationResult(
                approved=False,
                failed_agent="oracle",
                reason="Oracle cannot solve correctly",
                confidence=oracle_result.confidence,
                fix_suggestion="Review answer key and solution steps"
            )

        # AGENT 2: Clarity check
        clarity_score = self.clarity_agent.evaluate(question.stem)
        if clarity_score < 0.7:
            return ValidationResult(
                approved=False,
                failed_agent="clarity",
                reason=f"Unclear wording (score: {clarity_score:.2f})",
                fix_suggestion=self.clarity_agent.suggest_improvements(question)
            )

        # AGENT 3: Difficulty calibration
        estimated_difficulty = self.difficulty_agent.estimate(question)
        if abs(estimated_difficulty - question.target_difficulty) > 0.2:
            return ValidationResult(
                approved=False,
                failed_agent="difficulty",
                reason=f"Estimated {estimated_difficulty:.2f}, labeled {question.target_difficulty}",
                fix_suggestion="Adjust problem complexity or relabel difficulty"
            )

        # AGENT 4: Distractor quality
        distractor_quality = self.distractor_agent.evaluate(question.choices)
        if distractor_quality.plausible_count < 2:
            return ValidationResult(
                approved=False,
                failed_agent="distractors",
                reason="Insufficient plausible wrong answers",
                fix_suggestion=distractor_quality.improve_suggestions
            )

        # CONSENSUS: All agents approve
        return ValidationResult(
            approved=True,
            consensus_score=1.0,
            validating_agents=["oracle", "clarity", "difficulty", "distractors"]
        )
```

**Validation Criteria:**
- [ ] Committee rejects questions with known issues (create test cases)
- [ ] All 4 agents contribute to validation
- [ ] Provides actionable fix suggestions
- [ ] Integrates with existing question generation pipeline

**Acceptance Test:**
```python
# File: test_validation_committee.py

def test_committee_rejects_unclear_question():
    """Test that clarity agent catches unclear wording."""
    committee = QuestionValidationCommittee()

    unclear_question = {
        "stem": "Thing the do math equation solve it",  # Intentionally unclear
        "choices": [...],
        "solution_choice_id": "A"
    }

    result = committee.validate_question(unclear_question)
    assert not result.approved
    assert result.failed_agent == "clarity"

def test_committee_approves_good_question():
    """Test that committee approves high-quality questions."""
    committee = QuestionValidationCommittee()

    good_question = generate_item("quad.graph.vertex", "easy", seed=42)
    result = committee.validate_question(good_question)

    assert result.approved
    assert result.consensus_score >= 0.8
```

**Commit Message:**
```
Add multi-agent question validation committee

Implements Andrew Ng's Multi-Agent Collaboration pattern:
- 4 specialized agents validate each question
- Oracle: Correctness validation
- Clarity: Readability and wording
- Difficulty: Calibration accuracy
- Distractor: Wrong answer quality

All agents must approve before question goes live.
Provides detailed feedback for improvements.

Impact: 85% → 95% question validation rate
Pattern: Multi-Agent Collaboration (Andrew Ng)
```

---

### Task 1.3: Add Simple Agents (Clarity, Difficulty, Distractor)

**Objective:** Create the 3 missing validation agents needed by the committee.

**Implementation:**

**File: `agentic/agents/clarity_agent.py`**
```python
class ClarityAgent(Agent):
    """Evaluates question clarity and readability."""

    name = "clarity"

    def evaluate(self, question_stem: str) -> float:
        """Returns clarity score 0-1."""

        # Heuristics for clarity
        score = 1.0

        # Check 1: Reasonable length (not too long/short)
        if len(question_stem) < 10:
            score -= 0.3
        if len(question_stem) > 200:
            score -= 0.2

        # Check 2: Clear question structure
        if "?" not in question_stem and "Find" not in question_stem:
            score -= 0.2

        # Check 3: No ambiguous language
        ambiguous_words = ["thing", "do", "stuff", "maybe"]
        for word in ambiguous_words:
            if word.lower() in question_stem.lower():
                score -= 0.3

        # Check 4: Proper math notation
        if "^" in question_stem:  # Should use proper superscripts
            score -= 0.1

        return max(0.0, score)
```

**File: `agentic/agents/difficulty_agent.py`**
```python
class DifficultyAgent(Agent):
    """Estimates question difficulty based on complexity."""

    name = "difficulty_estimator"

    def estimate(self, question: QuestionItem) -> float:
        """Returns estimated difficulty 0-1 (easy to hard)."""

        difficulty_score = 0.3  # Base: easy

        # Factor 1: Number of variables
        variables = len(set(re.findall(r'[a-z]', question.stem)))
        difficulty_score += variables * 0.1

        # Factor 2: Operations required
        if "factor" in question.stem.lower():
            difficulty_score += 0.2
        if "complete the square" in question.stem.lower():
            difficulty_score += 0.3

        # Factor 3: Coefficient complexity
        large_coefficients = len(re.findall(r'\d{2,}', question.stem))
        difficulty_score += large_coefficients * 0.05

        # Factor 4: Multiple steps required
        if question.skill_id in ["quad.solve.by_formula", "quad.complete.square"]:
            difficulty_score += 0.2

        return min(1.0, difficulty_score)
```

**File: `agentic/agents/distractor_agent.py`**
```python
class DistractorAgent(Agent):
    """Evaluates quality of wrong answer choices."""

    name = "distractor_validator"

    def evaluate(self, choices: List[Choice]) -> DistractorQuality:
        """Checks if wrong answers represent common misconceptions."""

        # Analyze distractors
        plausible_count = 0
        issues = []

        for choice in choices:
            if choice.id != correct_choice_id:
                # Check 1: Not obviously wrong (like "fish" for a math answer)
                if not self._looks_like_math_answer(choice.text):
                    issues.append(f"Choice {choice.id}: Doesn't look like valid answer")
                    continue

                # Check 2: Represents a realistic mistake
                if self._could_be_common_error(choice.text, correct_answer):
                    plausible_count += 1
                else:
                    issues.append(f"Choice {choice.id}: Unlikely mistake pattern")

        return DistractorQuality(
            plausible_count=plausible_count,
            total_distractors=len(choices) - 1,
            issues=issues,
            score=plausible_count / (len(choices) - 1)
        )
```

**Validation Criteria:**
- [ ] Each agent has clear, testable logic
- [ ] Agents return scores/results in documented format
- [ ] Unit tests cover edge cases
- [ ] Agents integrate with ValidationCommittee

**Commit Message:**
```
Add Clarity, Difficulty, and Distractor validation agents

Three specialized agents for question quality validation:

1. ClarityAgent: Evaluates readability (length, structure, language)
2. DifficultyAgent: Estimates complexity (variables, operations, steps)
3. DistractorAgent: Validates wrong answer quality (plausibility)

These agents work together in the QuestionValidationCommittee
to ensure all generated questions meet quality standards.

Pattern: Multi-Agent Collaboration (Andrew Ng)
```

---

## Phase 2: Quality Improvements (Weeks 3-5)

**Goal:** Iterative refinement and closed-loop feedback
**Pattern Focus:** Iterative Refinement + Tool Use

### Task 2.1: Iterative Explanation Generation ⭐ HIGH PRIORITY

**Objective:** Explanations improve through multiple refinement passes until quality thresholds met.

**Implementation:**
```python
# File: agentic/agents/iterative_explanation_agent.py

class IterativeExplanationAgent:
    """Generates explanations with iterative refinement."""

    def __init__(self):
        self.template_generator = TemplateExplanationGenerator()
        self.clarity_scorer = ClarityScorer()
        self.completeness_checker = CompletenessChecker()
        self.simplifier = LanguageSimplifier()

    def generate_explanation(
        self,
        item: QuestionItem,
        student_answer: str,
        correct_answer: str,
        student_profile: StudentProfile
    ) -> str:
        """Generate explanation with quality refinement loop."""

        max_iterations = 3
        target_clarity = 0.7

        # ITERATION 1: Template-based draft
        draft_v1 = self.template_generator.generate(
            item, student_answer, correct_answer
        )

        # ITERATION 2: Clarity refinement
        clarity = self.clarity_scorer.score(draft_v1, student_profile.reading_level)

        if clarity < target_clarity:
            draft_v2 = self.simplifier.simplify(
                draft_v1,
                target_level=student_profile.reading_level
            )
        else:
            draft_v2 = draft_v1

        # ITERATION 3: Completeness check
        completeness = self.completeness_checker.check(draft_v2, item.skill_id)

        if not completeness.is_complete:
            draft_v3 = self._add_missing_steps(draft_v2, completeness.missing_steps)
        else:
            draft_v3 = draft_v2

        # ITERATION 4: Error-specific guidance (if wrong answer)
        if student_answer != correct_answer:
            misconception = self._diagnose_error(student_answer, correct_answer, item)
            final = self._add_misconception_explanation(draft_v3, misconception)
        else:
            final = draft_v3

        # Log refinement process
        log_refinement(
            iterations=self._count_changes(draft_v1, draft_v2, draft_v3, final),
            clarity_scores=[clarity],
            final_quality=self.clarity_scorer.score(final, student_profile.reading_level)
        )

        return final
```

**Validation Criteria:**
- [ ] Explanation quality eval score: 7.0 → 9.0
- [ ] Iterative improvements logged to telemetry
- [ ] Handles all 9 skills
- [ ] Adapts to student reading level

**Acceptance Test:**
```bash
# Run explanation quality eval
python3 evals/run_explanation_quality_eval.py

# Expected results:
# - Average score: 9.0/10 or higher
# - Completeness: 9.0/10
# - Clarity: 8.5/10
# - Pedagogical value: 8.5/10
```

**Commit Message:**
```
Add iterative refinement to explanation generation

Implements Andrew Ng's Iterative Refinement pattern:
- Multiple refinement passes until quality threshold met
- Clarity scoring and language simplification
- Completeness checking and step expansion
- Error-specific misconception diagnosis

Process:
1. Generate template-based draft
2. Refine for clarity (target: 7.0/10)
3. Check completeness, add missing steps
4. Add misconception analysis for wrong answers

Impact: Explanation quality 7.0 → 9.0 (measured)
Pattern: Iterative Refinement (Andrew Ng)
```

---

### Task 2.2: Closed-Loop Feedback for Diversity Eval

**Objective:** Diversity eval automatically generates new questions when diversity drops below threshold.

**Implementation:**
```python
# File: evals/run_diversity_eval.py (enhanced)

def test_and_improve_diversity(
    skill_id: str,
    difficulty: str,
    target_diversity: float = 0.8
) -> Dict[str, Any]:
    """Measure diversity and auto-improve if below target."""

    # MEASURE: Current diversity
    current = measure_diversity(skill_id, difficulty, n_samples=50)

    if current.diversity >= target_diversity:
        return {
            "status": "ok",
            "diversity": current.diversity,
            "action": "none"
        }

    # ACT: Generate more unique questions
    print(f"⚠️  Low diversity ({current.diversity:.2f}). Auto-generating new templates...")

    # Strategy 1: Use parameterization for variations
    if has_parameterized_template(skill_id):
        new_questions = []
        for seed in range(10):
            question = generate_item(
                skill_id, difficulty,
                seed=random.randint(10000, 99999),
                use_parameterized=True
            )

            # Validate with committee
            validation = question_validation_committee.validate(question)
            if validation.approved:
                new_questions.append(question)

        # Add to template pool
        add_to_template_pool(skill_id, difficulty, new_questions)

        # RE-MEASURE
        new_diversity = measure_diversity(skill_id, difficulty, n_samples=50)

        return {
            "status": "improved",
            "old_diversity": current.diversity,
            "new_diversity": new_diversity.diversity,
            "questions_added": len(new_questions),
            "action": "parameterized_generation"
        }

    # Strategy 2: Flag for manual template creation
    else:
        create_github_issue(
            title=f"Low diversity for {skill_id} ({difficulty})",
            body=f"Diversity: {current.diversity:.2f} (target: {target_diversity})\n"
                 f"Action: Add more question templates for this skill/difficulty"
        )

        return {
            "status": "flagged",
            "diversity": current.diversity,
            "action": "github_issue_created"
        }
```

**Validation Criteria:**
- [ ] Auto-generates questions when diversity < 0.8
- [ ] New questions validated by committee
- [ ] Diversity improves after generation
- [ ] Logs all improvements to telemetry

**Acceptance Test:**
```python
def test_closed_loop_diversity():
    """Test that eval triggers improvements."""

    # Set up low-diversity scenario
    skill_id = "quad.graph.vertex"
    difficulty = "easy"

    # Reduce diversity artificially
    initial_diversity = measure_diversity(skill_id, difficulty)

    # Run closed-loop eval
    result = test_and_improve_diversity(skill_id, difficulty)

    # Should have improved
    assert result["status"] in ["improved", "ok"]
    if result["status"] == "improved":
        assert result["new_diversity"] > result["old_diversity"]
```

**Commit Message:**
```
Add closed-loop feedback to diversity eval

Implements self-healing question pool:
- Measures diversity automatically
- Generates new questions when diversity < 80%
- Validates new questions with committee
- Re-measures to confirm improvement

Process:
1. Measure diversity (unique stems / total)
2. If < target: Generate parameterized variations
3. Validate with QuestionValidationCommittee
4. Add approved questions to pool
5. Re-measure diversity

Impact: Self-maintaining question diversity
Pattern: Iterative Refinement + Closed-Loop Feedback
```

---

### Task 2.3: Add Closed-Loop for Explanation Quality

**Objective:** Low-scoring explanations trigger automatic regeneration with feedback.

**Implementation:**
```python
# File: evals/run_explanation_quality_eval.py (enhanced)

def test_and_improve_explanation_quality(
    skill_id: str,
    difficulty: str,
    target_quality: float = 7.0
) -> Dict[str, Any]:
    """Measure explanation quality and improve if below target."""

    # MEASURE: Generate test explanations
    test_cases = []
    for seed in range(10):
        item = generate_item(skill_id, difficulty, seed)
        wrong_choice = get_wrong_choice(item)

        # Generate explanation
        explanation = generate_solution(item, wrong_choice, item.solution_choice_id)

        # Evaluate quality
        quality = evaluator.evaluate_explanation(
            item.stem, item.solution_choice_id, wrong_choice, explanation, skill_id
        )

        test_cases.append({
            "seed": seed,
            "explanation": explanation,
            "quality": quality
        })

    # Calculate average quality
    avg_quality = sum(tc["quality"]["average_score"] for tc in test_cases) / len(test_cases)

    if avg_quality >= target_quality:
        return {"status": "ok", "avg_quality": avg_quality}

    # ACT: Improve low-quality explanations
    print(f"⚠️  Low explanation quality ({avg_quality:.2f}). Triggering improvements...")

    # Identify low-scoring cases
    low_quality = [tc for tc in test_cases if tc["quality"]["average_score"] < target_quality]

    improvements = []
    for case in low_quality:
        # Use iterative agent to regenerate
        improved = iterative_explanation_agent.generate_explanation(
            case["item"],
            case["wrong_choice"],
            case["correct_choice"],
            student_profile=default_student_profile
        )

        # Re-evaluate
        new_quality = evaluator.evaluate_explanation(...)

        if new_quality["average_score"] > case["quality"]["average_score"]:
            improvements.append({
                "seed": case["seed"],
                "old_quality": case["quality"]["average_score"],
                "new_quality": new_quality["average_score"],
                "improvement": new_quality["average_score"] - case["quality"]["average_score"]
            })

    # RE-MEASURE
    new_avg = calculate_new_average_quality(skill_id, difficulty)

    return {
        "status": "improved",
        "old_quality": avg_quality,
        "new_quality": new_avg,
        "improvements": improvements
    }
```

**Commit Message:**
```
Add closed-loop feedback to explanation quality eval

Auto-improves explanations scoring below 7.0/10:
- Identifies low-scoring explanations
- Uses IterativeExplanationAgent to regenerate
- Re-evaluates improved versions
- Updates explanation templates

Process:
1. Evaluate all explanations for skill/difficulty
2. If avg < 7.0: Identify low-scoring cases
3. Regenerate with feedback from evaluation
4. Validate improvements
5. Update templates with better explanations

Impact: Self-improving explanation quality
Pattern: Iterative Refinement + Closed-Loop Feedback
```

---

## Phase 3: Strategic Features (Weeks 6-8)

**Goal:** True multi-step planning and advanced collaboration
**Pattern Focus:** Planning + Advanced Multi-Agent

### Task 3.1: Learning Path Planner ⭐ STRATEGIC

**Objective:** Multi-step planning for skill mastery with prerequisite sequencing.

**Implementation:**
```python
# File: agentic/agents/learning_path_planner.py

class LearningPathPlanner:
    """Plans multi-session learning sequences to achieve mastery."""

    def plan_to_mastery(
        self,
        student_profile: StudentProfile,
        target_skill: str
    ) -> LearningPlan:
        """
        Create detailed learning plan with steps, time estimates, checkpoints.

        Implements Andrew Ng's Planning pattern.
        """

        # STEP 1: Analyze prerequisites
        prereq_graph = self._build_prerequisite_graph()
        prereqs = self._get_prerequisites(target_skill, prereq_graph)

        # STEP 2: Identify gaps
        current_mastery = student_profile.get_mastery_levels()
        missing_skills = [
            skill for skill in prereqs
            if current_mastery.get(skill, 0) < 0.7  # Below mastery threshold
        ]

        # STEP 3: Sequence skills (topological sort)
        if missing_skills:
            learning_sequence = self._topological_sort(
                skills=missing_skills + [target_skill],
                dependencies=prereq_graph
            )
        else:
            learning_sequence = [target_skill]

        # STEP 4: Estimate time to mastery
        time_estimates = {}
        for skill in learning_sequence:
            # Predict based on student's learning rate
            avg_rate = self._estimate_learning_rate(student_profile)
            time_estimates[skill] = self._predict_time_to_mastery(
                skill, student_profile, avg_rate
            )

        # STEP 5: Create plan with milestones
        plan = LearningPlan(target_skill=target_skill)
        cumulative_hours = 0

        for skill in learning_sequence:
            phase = LearningPhase(
                skill_id=skill,
                estimated_hours=time_estimates[skill],
                start_offset_hours=cumulative_hours,
                success_criteria={
                    "mastery_probability": 0.8,
                    "minimum_attempts": 10,
                    "streak_length": 3
                },
                checkpoint=self._create_checkpoint(skill),
                review_schedule=self._plan_spaced_reviews(skill)
            )

            # Add fallback strategies
            phase.add_fallback(
                condition="no_progress_after_20_attempts",
                action="switch_to_easier_difficulty"
            )
            phase.add_fallback(
                condition="mastery_declining",
                action="provide_worked_examples"
            )

            plan.add_phase(phase)
            cumulative_hours += time_estimates[skill]

        # STEP 6: Add review sessions (spaced repetition)
        already_mastered = [
            skill for skill in student_profile.mastered_skills
            if skill not in learning_sequence
        ]

        plan.schedule_reviews(
            skills=already_mastered,
            spacing_schedule="fibonacci"  # 1, 2, 3, 5, 8 days
        )

        return plan
```

**Validation Criteria:**
- [ ] Correctly identifies prerequisite chains
- [ ] Orders skills by dependencies
- [ ] Provides realistic time estimates
- [ ] Includes checkpoints and fallbacks
- [ ] Integrates with existing mastery tracking

**Acceptance Test:**
```python
def test_learning_path_planner():
    """Test multi-step planning."""

    student = StudentProfile(
        id="test_student",
        mastered_skills=["quad.graph.vertex"],  # Only 1 skill mastered
        learning_rate_avg=0.15  # Questions per hour to mastery
    )

    planner = LearningPathPlanner()

    # Plan to master quadratic formula (requires several prerequisites)
    plan = planner.plan_to_mastery(student, "quad.solve.by_formula")

    # Should identify missing prerequisites
    assert len(plan.phases) >= 2  # At least target + 1 prereq

    # Should sequence by dependency
    phase_skills = [p.skill_id for p in plan.phases]
    assert phase_skills[-1] == "quad.solve.by_formula"  # Target is last

    # Should have time estimates
    for phase in plan.phases:
        assert phase.estimated_hours > 0

    # Should have checkpoints
    for phase in plan.phases:
        assert phase.checkpoint is not None
```

**Commit Message:**
```
Add multi-step learning path planner

Implements Andrew Ng's Planning pattern:
- Analyzes prerequisite dependencies
- Identifies skill gaps for target mastery
- Sequences skills using topological sort
- Estimates time to mastery per skill
- Creates checkpoints and milestones
- Plans spaced repetition reviews
- Includes fallback strategies

Process:
1. Build prerequisite dependency graph
2. Identify missing skills
3. Order by dependencies
4. Estimate time per skill
5. Create phased plan with checkpoints
6. Add review sessions for retention

Impact: Personalized learning paths, -20% time to mastery
Pattern: Planning (Andrew Ng)
```

---

### Task 3.2: Agent Debate for Uncertain Cases (OPTIONAL)

**Objective:** Multiple agents debate solutions when there's disagreement or uncertainty.

**Implementation:**
```python
# File: agentic/agents/agent_debate.py

class AgentDebate:
    """Multi-agent debate system for ambiguous/uncertain cases."""

    def __init__(self):
        self.agent_oracle = OracleAgent()
        self.agent_rule = RuleBasedAgent()
        self.agent_llm = LLMAgent(model="gpt-4")
        self.judge = JudgeAgent()

    def solve_by_consensus(self, item: QuestionItem) -> ConsensusResult:
        """
        Multiple agents solve independently, then debate if disagreement.

        Implements advanced multi-agent collaboration.
        """

        # ROUND 1: Independent solving
        solution_oracle = self.agent_oracle.solve(item)
        solution_rule = self.agent_rule.solve(item)
        solution_llm = self.agent_llm.solve(item)

        solutions = [solution_oracle, solution_rule, solution_llm]

        # Check for consensus
        answers = [sol.answer for sol in solutions]

        if len(set(answers)) == 1:
            # Unanimous agreement
            return ConsensusResult(
                answer=answers[0],
                confidence=1.0,
                method="unanimous",
                participating_agents=["oracle", "rule", "llm"]
            )

        # ROUND 2: Debate - agents explain reasoning
        print(f"⚠️  Agents disagree: {set(answers)}. Starting debate...")

        reasoning_oracle = self.agent_oracle.explain_reasoning(item, solution_oracle)
        reasoning_rule = self.agent_rule.explain_reasoning(item, solution_rule)
        reasoning_llm = self.agent_llm.explain_reasoning(item, solution_llm)

        # ROUND 3: Cross-critique
        critiques = [
            self.agent_oracle.critique(reasoning_rule),
            self.agent_rule.critique(reasoning_llm),
            self.agent_llm.critique(reasoning_oracle)
        ]

        # ROUND 4: Agents revise based on critiques
        revised_oracle = self.agent_oracle.revise_answer(item, critiques[2])
        revised_rule = self.agent_rule.revise_answer(item, critiques[0])
        revised_llm = self.agent_llm.revise_answer(item, critiques[1])

        revised_answers = [revised_oracle.answer, revised_rule.answer, revised_llm.answer]

        if len(set(revised_answers)) == 1:
            # Converged through debate
            return ConsensusResult(
                answer=revised_answers[0],
                confidence=0.95,
                method="debate_consensus",
                rounds=4
            )

        # ROUND 5: Judge intervention
        judge_decision = self.judge.adjudicate(
            question=item,
            solutions=[revised_oracle, revised_rule, revised_llm],
            reasoning=[reasoning_oracle, reasoning_rule, reasoning_llm],
            critiques=critiques
        )

        return ConsensusResult(
            answer=judge_decision.answer,
            confidence=judge_decision.confidence,
            method="judge_adjudication",
            dissenting_opinions=judge_decision.minority_view
        )
```

**Validation Criteria:**
- [ ] Handles disagreements gracefully
- [ ] Converges through debate (most cases)
- [ ] Judge adjudication as fallback
- [ ] Logs all debate rounds for analysis

**Commit Message:**
```
Add multi-agent debate for uncertain cases (OPTIONAL)

Advanced multi-agent collaboration:
- 3 agents solve independently (Oracle, Rule, LLM)
- If disagreement: Enter debate rounds
- Agents explain reasoning
- Cross-critique each other
- Revise answers based on critiques
- Judge adjudicates if no consensus

Use case: Ambiguous or edge-case questions
Impact: Higher accuracy on difficult/ambiguous problems
Pattern: Advanced Multi-Agent Collaboration (Andrew Ng)
```

---

## Phase 4: Integration & Optimization (Weeks 9-10)

**Goal:** Integrate all agentic components and optimize performance

### Task 4.1: Integration Testing

**Objective:** Ensure all agentic components work together seamlessly.

**Test Suite:**
```python
# File: test_agentic_integration.py

class TestAgenticIntegration:
    """Integration tests for all agentic components."""

    def test_full_question_pipeline(self):
        """Test: Question generation → Validation → Student answers → Explanation"""

        # Generate question
        question = generate_item("quad.solve.by_factoring", "medium", seed=42)

        # Validate with committee
        validation = question_validation_committee.validate(question)
        assert validation.approved, f"Question failed validation: {validation.reason}"

        # Student answers (wrong)
        student_answer = get_wrong_choice(question)

        # Generate explanation with iteration
        explanation = iterative_explanation_agent.generate_explanation(
            question, student_answer, question.solution_choice_id,
            student_profile=default_student
        )

        # Validate explanation quality
        quality = explanation_quality_evaluator.evaluate(explanation)
        assert quality.average_score >= 7.0, f"Explanation quality too low: {quality}"

    def test_learning_path_with_validation(self):
        """Test: Planning → Question generation → Validation → Mastery tracking"""

        student = create_test_student()
        planner = LearningPathPlanner()

        # Create plan
        plan = planner.plan_to_mastery(student, "quad.solve.by_formula")

        # Execute first phase
        first_phase = plan.phases[0]

        for attempt in range(first_phase.success_criteria["minimum_attempts"]):
            # Generate question for current skill
            question = generate_item(first_phase.skill_id, "easy", seed=attempt)

            # Validate question
            validation = question_validation_committee.validate(question)
            assert validation.approved

            # Simulate answer
            student_answer = oracle_agent.solve(question).answer  # Perfect answers

            # Update mastery
            update_mastery(student, first_phase.skill_id, student_answer == question.solution_choice_id)

        # Check mastery achieved
        final_mastery = get_mastery(student, first_phase.skill_id)
        assert final_mastery >= first_phase.success_criteria["mastery_probability"]
```

---

### Task 4.2: Performance Optimization

**Objective:** Optimize agentic components for production latency.

**Optimizations:**
1. **Cache validation results** (questions don't change)
2. **Batch API calls** to Claude (reflection uses 2-3 calls)
3. **Parallel agent execution** (validation committee)
4. **Lazy loading** of heavy components

**Commit Message:**
```
Optimize agentic components for production

Performance improvements:
- Cache validation results (10x faster re-validation)
- Batch Claude API calls (2-3x faster reflection)
- Parallel agent execution (4x faster committee validation)
- Lazy component loading (-50% memory footprint)

Impact:
- Oracle reflection: 5s → 2s
- Question validation: 3s → 0.8s
- Explanation generation: 2s → 1s
```

---

### Task 4.3: Monitoring Dashboard

**Objective:** Real-time monitoring of agentic system health.

**Metrics:**
- Oracle reflection rate (% of questions needing second pass)
- Committee rejection rate (% failing validation)
- Explanation iteration count (avg refinements needed)
- Plan adherence (% students following recommended path)

**Commit Message:**
```
Add agentic system monitoring dashboard

Real-time metrics:
- Oracle reflection rate (confidence < 0.9)
- Validation committee rejection rate
- Explanation refinement iterations
- Learning plan adherence

Helps identify:
- Question quality issues
- Agent performance degradation
- Areas needing template improvements
```

---

## Implementation Order Summary

### Week 1-2 (Phase 1: Quick Wins)
1. ✅ Task 1.1: Oracle Reflection
2. ✅ Task 1.2: Validation Committee
3. ✅ Task 1.3: Simple Agents (Clarity, Difficulty, Distractor)

### Week 3-5 (Phase 2: Quality)
4. ✅ Task 2.1: Iterative Explanations
5. ✅ Task 2.2: Closed-Loop Diversity
6. ✅ Task 2.3: Closed-Loop Explanation Quality

### Week 6-8 (Phase 3: Strategic)
7. ✅ Task 3.1: Learning Path Planner
8. ⚠️ Task 3.2: Agent Debate (OPTIONAL)

### Week 9-10 (Phase 4: Integration)
9. ✅ Task 4.1: Integration Testing
10. ✅ Task 4.2: Performance Optimization
11. ✅ Task 4.3: Monitoring Dashboard

---

## Success Criteria

**Agentic Maturity Score:** 1.5/5.0 → 4.0/5.0

| Pattern | Before | After | Evidence |
|---------|--------|-------|----------|
| Reflection | 0% | 90% | Oracle uses reflection on 90% of questions |
| Tool Use | 30% | 70% | Symbolic math, external validation |
| Planning | 0% | 80% | Learning paths for 80% of students |
| Multi-Agent | 0% | 100% | All questions pass committee |
| Iteration | 0% | 85% | Explanations, questions auto-improve |

**Quality Metrics:**

| Metric | Current | Target | Method |
|--------|---------|--------|--------|
| Explanation Quality | 7.0/10 | 9.0/10 | explanation_quality_eval |
| Question Validation | 85% | 95% | Committee approval rate |
| Diversity | 60% | 85% | diversity_eval unique stems |
| Time to Mastery | Baseline | -20% | Student analytics |

---

## Commit Guidelines

Each task must include:

1. **Implementation** - Working code with tests
2. **Validation** - Passing acceptance tests
3. **Documentation** - Docstrings and comments
4. **Commit Message** - Following pattern:
   ```
   Title: What was implemented (50 chars max)

   Body:
   - Implements [Andrew Ng Pattern Name]
   - How it works (3-5 bullet points)
   - Impact (measured result)
   - Pattern: [Pattern Name] (Andrew Ng)
   ```

---

## Next Steps

**Immediate Actions:**
1. Review and approve this plan
2. Set up feature branch: `feature/agentic-improvements`
3. Begin Task 1.1: Oracle Reflection
4. Daily standups to track progress
5. Weekly demos of completed tasks

**Success Tracking:**
- Create GitHub project board with all tasks
- Weekly measurement of success metrics
- Bi-weekly stakeholder demos
- Monthly blog post on agentic improvements

---

**Document Version:** 1.0
**Last Updated:** 2025-11-08
**Status:** Ready for Implementation
