# Telemetry & Data Flywheel System

## Overview

The Agent_Math system now includes a comprehensive telemetry system that tracks student interactions to enable continuous improvement through real student data.

## How It Works

### 1. Data Collection

Every student interaction generates telemetry events that are logged to `logs/telemetry_YYYY-MM-DD.jsonl`:

**Event Types:**
- `question_presented`: When a question is shown to the student
- `question_answered`: When a student submits an answer
- `session_summary`: When a practice session completes

**What We Track:**
- Which skills and difficulties students practice
- Whether students answer correctly
- Which distractors students choose when wrong
- Time spent on each question
- Parameter values used in generated questions

### 2. API Endpoints

#### POST /telemetry/log
Log a telemetry event.

```bash
curl -X POST http://localhost:8000/telemetry/log \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "question_answered",
    "timestamp": "2025-01-07T10:30:45Z",
    "session_id": "session-123",
    "skill_id": "quad.roots.factored",
    "difficulty": "medium",
    "student_answer": "x = 23 and x = -15",
    "correct_answer": "x = -23 and x = 15",
    "is_correct": false,
    "distractor_type_chosen": "sign_error",
    "time_to_answer_ms": 45000
  }'
```

#### GET /telemetry/stats?days=7
Get aggregated statistics from recent telemetry data.

```bash
curl "http://localhost:8000/telemetry/stats?days=7"
```

Returns:
```json
{
  "total_events": 150,
  "questions_answered": 120,
  "overall_accuracy": 0.68,
  "by_skill": {
    "quad.roots.factored": {
      "total": 30,
      "correct": 21,
      "accuracy": 0.70
    }
  },
  "by_difficulty": {
    "easy": {"total": 40, "correct": 35, "accuracy": 0.875},
    "medium": {"total": 50, "correct": 32, "accuracy": 0.64},
    "hard": {"total": 30, "correct": 14, "accuracy": 0.467}
  }
}
```

### 3. Analysis Tools

#### analyze_telemetry.py
Comprehensive analysis script for extracting insights.

**Difficulty Calibration Report:**
Shows if difficulty levels are properly calibrated based on actual student performance.

```bash
python tools/analyze_telemetry.py --report difficulty_calibration --days 7
```

Target ranges:
- Easy: 75-90% accuracy
- Medium: 60-75% accuracy
- Hard: 45-60% accuracy

**Distractor Effectiveness Report:**
Shows which error patterns students are making.

```bash
python tools/analyze_telemetry.py --report distractor_effectiveness --days 7
```

Helps identify:
- Which distractors are never chosen (too obvious)
- Which distractors are chosen too often (too similar to correct answer)
- Common student misconceptions

**Parameter Difficulty Correlation:**
Shows how parameter values affect difficulty.

```bash
python tools/analyze_telemetry.py --report parameter_difficulty --days 7
```

Answers questions like:
- Do larger numbers make questions harder?
- Which parameter ranges produce well-calibrated questions?

## Integration Guide

### Frontend Integration

To log telemetry events from your frontend:

```javascript
// When question is presented
await fetch('/telemetry/log', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    event_type: 'question_presented',
    timestamp: new Date().toISOString(),
    session_id: sessionId,
    question_id: questionId,
    skill_id: 'quad.roots.factored',
    difficulty: 'medium',
    generation_method: 'parameterized',
    parameters: { r1: -23, r2: 15 },
    question_stem: 'Find the roots of y = (x + 23)(x - 15).',
    correct_answer: 'x = -23 and x = 15',
    choices: ['x = -23 and x = 15', 'x = 23 and x = -15', ...],
    distractor_types: [null, 'sign_error', 'off_by_one', ...]
  })
});

// When student answers
await fetch('/telemetry/log', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    event_type: 'question_answered',
    timestamp: new Date().toISOString(),
    session_id: sessionId,
    question_id: questionId,
    skill_id: 'quad.roots.factored',
    difficulty: 'medium',
    student_answer: selectedAnswer,
    correct_answer: correctAnswer,
    is_correct: selectedAnswer === correctAnswer,
    distractor_type_chosen: getDistractorType(selectedAnswer),
    time_to_answer_ms: Date.now() - questionStartTime,
    attempt_number: 1
  })
});
```

## Data-Driven Improvements

### Phase 1: Collection (Current)
- ✅ Telemetry endpoints implemented
- ✅ Analysis scripts created
- ⏳ Frontend integration pending
- ⏳ Collecting real student data

### Phase 2: Learning (Next)
Once we have sufficient data:

1. **Auto-tune difficulty ranges**
   - Adjust parameter ranges to hit target accuracy
   - Example: If medium is too hard (50% accuracy), reduce to [-25, 25]

2. **Improve distractors**
   - Replace ineffective distractors with observed student errors
   - Add new distractor types based on common mistakes

3. **Personalization**
   - Adapt difficulty to individual student level
   - Focus practice on weak areas

### Phase 3: Optimization (Future)
- A/B test different question generation strategies
- Machine learning to predict question difficulty
- Adaptive curriculum that responds to student progress

## Privacy & Ethics

- **Anonymous by default**: `user_id` is optional
- **No PII**: Only mathematical interaction data collected
- **Transparent**: Students know data is used to improve questions
- **Retention**: Telemetry data retained for 90 days

## Files

- `logs/telemetry_*.jsonl` - Daily telemetry event logs
- `logs/telemetry_schema.md` - Detailed schema documentation
- `tools/analyze_telemetry.py` - Analysis script
- `api/server.py` - Telemetry endpoints (lines 817-976)

## Next Steps

1. **Integrate telemetry into frontend** - Log events from web UI
2. **Collect baseline data** - Run for 1-2 weeks to gather sufficient data
3. **Analyze patterns** - Run analysis scripts to identify improvements
4. **Implement learnings** - Auto-tune parameters and distractors based on data
5. **Iterate** - Continuous improvement loop

---

The data flywheel is now spinning! 🎯
