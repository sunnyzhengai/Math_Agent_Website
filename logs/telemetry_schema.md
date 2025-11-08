# Student Interaction Telemetry Schema

## Event Types

### 1. Question Presented
Logged when a question is shown to the student.

```json
{
  "event_type": "question_presented",
  "timestamp": "2025-01-07T10:30:00Z",
  "session_id": "uuid-v4",
  "user_id": "optional-user-id",
  "question_id": "generated-uuid",
  "skill_id": "quad.roots.factored",
  "difficulty": "medium",
  "generation_method": "parameterized",
  "parameters": {
    "r1": -23,
    "r2": 15
  },
  "question_stem": "Find the roots of y = (x + 23)(x - 15).",
  "correct_answer": "x = -23 and x = 15",
  "choices": [
    "x = -23 and x = 15",
    "x = 23 and x = -15",
    "x = -22 and x = 15",
    "x = -23 and x = 14"
  ],
  "distractor_types": [null, "sign_error", "off_by_one", "off_by_one"]
}
```

### 2. Question Answered
Logged when student submits an answer.

```json
{
  "event_type": "question_answered",
  "timestamp": "2025-01-07T10:30:45Z",
  "session_id": "uuid-v4",
  "user_id": "optional-user-id",
  "question_id": "generated-uuid",
  "skill_id": "quad.roots.factored",
  "difficulty": "medium",
  "student_answer": "x = 23 and x = -15",
  "correct_answer": "x = -23 and x = 15",
  "is_correct": false,
  "distractor_type_chosen": "sign_error",
  "time_to_answer_ms": 45000,
  "attempt_number": 1
}
```

### 3. Session Summary
Logged when a practice session completes.

```json
{
  "event_type": "session_summary",
  "timestamp": "2025-01-07T11:00:00Z",
  "session_id": "uuid-v4",
  "user_id": "optional-user-id",
  "total_questions": 10,
  "correct_count": 7,
  "accuracy": 0.7,
  "total_time_ms": 450000,
  "avg_time_per_question_ms": 45000,
  "skills_practiced": ["quad.roots.factored", "quad.graph.vertex"],
  "difficulty_distribution": {
    "easy": 3,
    "medium": 5,
    "hard": 2
  }
}
```

## Storage Format

- File: `logs/telemetry.jsonl` (JSON Lines format)
- One event per line for easy streaming analysis
- Rotates daily: `telemetry_YYYY-MM-DD.jsonl`

## Privacy Considerations

- `user_id` is optional (supports anonymous practice)
- No PII stored beyond user_id
- Session data aggregated for analysis
- Individual session data retained for 90 days

## Analysis Queries

### Real Accuracy by Difficulty
```sql
SELECT
  skill_id,
  difficulty,
  COUNT(*) as total,
  SUM(CASE WHEN is_correct THEN 1 ELSE 0 END) as correct,
  AVG(CASE WHEN is_correct THEN 1.0 ELSE 0.0 END) as accuracy
FROM question_answered
GROUP BY skill_id, difficulty
```

### Most Confusing Distractors
```sql
SELECT
  skill_id,
  distractor_type_chosen,
  COUNT(*) as times_chosen,
  AVG(time_to_answer_ms) as avg_time
FROM question_answered
WHERE is_correct = false
GROUP BY skill_id, distractor_type_chosen
ORDER BY times_chosen DESC
```

### Parameter Difficulty Correlation
```sql
SELECT
  skill_id,
  difficulty,
  json_extract(parameters, '$.r1') as r1_value,
  AVG(CASE WHEN is_correct THEN 1.0 ELSE 0.0 END) as accuracy
FROM question_answered
GROUP BY skill_id, difficulty, r1_value
ORDER BY ABS(r1_value) DESC
```
