# Telemetry JSONL Schema

## Common fields

- `event` ∈ {"generate","grade","cycle_reset"}
- `ts` (float, seconds)
- `server_id` (str)
- `version` (str)

## Generate

- `session_id` (str)
- `mode` ∈ {"random","cycle"}
- `skill_id` (str)
- `difficulty` ∈ {"easy","medium","hard","applied"}
- `item_id` (str)
- `stem_hash` (str, "sha1:...")
- `choice_ids` (["A","B","C","D"])
- `latency_ms` (float)

## Grade

- `session_id` (str|null)
- `skill_id`, `difficulty`, `item_id`
- `choice_id` ∈ {"A","B","C","D"}
- `correct` (bool)
- `solution_choice_id` (str)
- `latency_ms` (float)

## Cycle Reset

- `session_id`, `skill_id`, `difficulty`
