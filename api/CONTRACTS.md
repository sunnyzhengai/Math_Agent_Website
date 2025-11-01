# API Contracts (Do-Not-Change Without Intent)

These schemas define the JSON shapes for the public API endpoints.

---

## Endpoint: `POST /items/generate`

Generate a new math question item.

### Request

```json
{
  "skill_id": "quad.graph.vertex",
  "difficulty": "easy",
  "seed": 42
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `skill_id` | string | ✅ Yes | Must exist in templates |
| `difficulty` | string | ❌ No | One of: `"easy"`, `"medium"`, `"hard"`, `"applied"`. Defaults to `"easy"` |
| `seed` | integer | ❌ No | For deterministic generation. If omitted, generates random item_id |

### Response (Success: 200 OK)

```json
{
  "item_id": "quad.graph.vertex:easy:42",
  "skill_id": "quad.graph.vertex",
  "difficulty": "easy",
  "stem": "For y = (x - 3)^2 + 2, what is the vertex?",
  "choices": [
    { "id": "A", "text": "(2, 3)" },
    { "id": "B", "text": "(-3, 2)" },
    { "id": "C", "text": "(3, -2)" },
    { "id": "D", "text": "(3, 2)" }
  ],
  "solution_choice_id": "D",
  "solution_text": "(3, 2)",
  "tags": ["vertex_form"]
}
```

### Error Responses

| Status | Error | Reason |
|--------|-------|--------|
| 400 | `{"error": "invalid_skill", "message": "..."}` | Unknown skill_id |
| 400 | `{"error": "invalid_difficulty", "message": "..."}` | Invalid difficulty value |
| 400 | `{"error": "invalid_seed", "message": "..."}` | seed is not an integer |

---

## Endpoint: `POST /grade`

Grade a student's response to a question.

### Request

```json
{
  "item": {
    "item_id": "quad.graph.vertex:easy:42",
    "skill_id": "quad.graph.vertex",
    "difficulty": "easy",
    "stem": "For y = (x - 3)^2 + 2, what is the vertex?",
    "choices": [
      { "id": "A", "text": "(2, 3)" },
      { "id": "B", "text": "(-3, 2)" },
      { "id": "C", "text": "(3, -2)" },
      { "id": "D", "text": "(3, 2)" }
    ],
    "solution_choice_id": "D",
    "solution_text": "(3, 2)",
    "tags": ["vertex_form"]
  },
  "choice_id": "D"
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `item` | object | ✅ Yes | Full item dict (from `/items/generate`) |
| `choice_id` | string | ✅ Yes | One of: `"A"`, `"B"`, `"C"`, `"D"` (uppercase only) |

### Response (Success: 200 OK)

```json
{
  "correct": true,
  "solution_choice_id": "D",
  "explanation": "Correct! The answer is (3, 2)."
}
```

| Field | Type | Notes |
|-------|------|-------|
| `correct` | boolean | True if choice_id matches solution_choice_id |
| `solution_choice_id` | string | The correct answer ID (always shown) |
| `explanation` | string | Pedagogical feedback (differs for correct vs incorrect) |

### Error Responses

| Status | Error | Reason |
|--------|-------|--------|
| 400 | `{"error": "invalid_item", "message": "..."}` | Item fails validation |
| 400 | `{"error": "invalid_choice_id", "message": "..."}` | choice_id not in ["A","B","C","D"] |
| 400 | `{"error": "missing_field", "message": "..."}` | Required field missing from request |

---

## Common Patterns

### Determinism

Both endpoints are deterministic:
- Same `(skill_id, difficulty, seed)` always generates identical item
- Same `(item, choice_id)` always returns identical grade

### Validation

All request bodies are validated before processing:
- Missing required fields → 400 Bad Request
- Invalid values → 400 Bad Request
- Malformed JSON → 400 Bad Request

### JSON Serialization

All responses are JSON-serializable dicts with no datetime, UUID, or other non-JSON types.
