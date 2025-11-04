# Agentic Framework — Architecture & Flow Guide

## 📋 Table of Contents

1. [High-Level Architecture](#architecture)
2. [Component Breakdown](#components)
3. [Data Flow](#data-flow)
4. [How to Add a New Agent](#adding-agents)
5. [Running & Testing](#running)
6. [Performance Summary](#performance)

---

## Architecture

The agentic framework is designed for **comparing different solving strategies** on deterministic test cases. Here's the big picture:

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENTIC FRAMEWORK                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  [Seed Set] → [Eval Runner] → [Agent Registry] → [Results] │
│                                   ↓                          │
│                            Agent Strategies:                │
│                    ┌─────────────────────────┐              │
│                    │ • Oracle (100% upper)   │              │
│                    │ • Rules (83% real math) │              │
│                    │ • Random (67% baseline) │              │
│                    │ • AlwaysA (33% sanity)  │              │
│                    └─────────────────────────┘              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Components

### 1. **Base Agent Interface** (`agents/base.py`)

The abstract base class all agents inherit from:

```python
class Agent(ABC):
    name: str = "base"
    
    @abstractmethod
    def choose(self, item: Dict[str, Any]) -> str:
        """Return one of 'A', 'B', 'C', 'D'."""
        raise NotImplementedError
```

**Key idea:** All agents have the same interface—they take a question item and return a choice ID.

---

### 2. **Agent Strategies** (`agents/`)

We have **4 agent strategies**, each with different sophistication levels:

#### **Oracle Agent** (`oracle.py`)
```python
class OracleAgent(Agent):
    name = "oracle"
    
    def choose(self, item: Dict[str, Any]) -> str:
        return item["solution_choice_id"]  # Always correct
```
- **Accuracy:** 100% (regression guard)
- **Purpose:** Verify the engine/grader work correctly
- **Use case:** Baseline proof that questions are valid

---

#### **AlwaysA Agent** (`always_a.py`)
```python
class AlwaysAAgent(Agent):
    name = "always_a"
    
    def choose(self, item: Dict[str, Any]) -> str:
        return "A"  # Always first choice
```
- **Accuracy:** ~33% (on shuffled answers)
- **Purpose:** Sanity check; catches broken shuffle logic
- **Use case:** Verify choice distribution isn't biased

---

#### **RandomGuess Agent** (`random_guess.py`)
```python
class RandomGuessAgent(Agent):
    name = "random"
    
    def choose(self, item: Dict[str, Any]) -> str:
        sid = item.get("item_id") or f"{item.get('skill_id')}_{item.get('difficulty')}_0"
        seed_hex = hashlib.sha256(sid.encode()).hexdigest()[:8]
        seed = int(seed_hex, 16) % (2**32)
        rng = random.Random(seed)
        return rng.choice(["A", "B", "C", "D"])
```
- **Accuracy:** 67% (deterministic random on seed set)
- **Purpose:** Chance baseline
- **Key feature:** Deterministic via SHA256—same output across runs

---

#### **Rules Agent** (`rule_router.py` + `rules/`)
```python
class RuleRouterAgent(Agent):
    name = "rules"
    
    def choose(self, item: Dict[str, Any]) -> str:
        skill_id = item.get("skill_id", "")
        
        if skill_id == "quad.graph.vertex":
            return _VTXFORM.choose(item)  # Vertex form parser
        
        if skill_id == "quad.standard.vertex":
            return _STD.choose(item)  # Standard form parser
        
        return _RAND.choose(item)  # Fallback to random
```
- **Accuracy:** 83% (real math!)
- **Purpose:** Domain-specific solving strategies
- **Key features:**
  - Regex parsing of question stems
  - Mathematical computation (vertex formula)
  - Graceful fallback to random

**Rule implementations:**
- `rules/vertex_from_vertexform.py`: Parse `y=a(x-h)²+k` to extract vertex
- `rules/standard_vertex.py`: Parse `y=ax²+bx+c` and compute vertex via formula

---

### 3. **Agent Registry** (`agents/registry.py`)

Central **factory pattern** for agent instantiation:

```python
_REGISTRY: Dict[str, Type[Agent]] = {
    "oracle": OracleAgent,
    "always_a": AlwaysAAgent,
    "random": RandomGuessAgent,
    "rules": RuleRouterAgent,
}

def get_agent(name: str) -> Agent:
    if name not in _REGISTRY:
        raise ValueError(f"unknown_agent:{name}")
    return _REGISTRY[name]()  # Instantiate on demand
```

**Why factory pattern?**
- Creates new instance each time → no shared state
- Easy to extend: just add to `_REGISTRY`
- Testable: can mock agents

---

### 4. **Eval Harness** (`evals/run_eval.py`)

The **orchestrator** that runs tests with any agent:

```python
def run_case(case: Dict[str, Any], agent_name: str) -> Tuple[bool, Dict[str, Any]]:
    """
    1. Generate item deterministically
    2. Get agent's choice
    3. Validate choice
    4. Grade response
    5. Record result with latency & error info
    """
    # Step 1: Generate item
    try:
        item = generate_item(skill_id, difficulty, seed=seed)
    except Exception as e:
        return False, {"status": "generate_error", "error": str(e), ...}
    
    # Step 2: Get agent's choice
    try:
        agent = get_agent(agent_name)
        choice_id = agent.choose(item)
        if choice_id not in ["A", "B", "C", "D"]:
            raise ValueError(f"invalid_choice:{choice_id}")
    except Exception as e:
        return False, {"status": "agent_error", "error": str(e), ...}
    
    # Step 3: Grade
    try:
        result = grade_response(item, choice_id)
    except Exception as e:
        return False, {"status": "grade_error", "error": str(e), ...}
    
    # Step 4: Record
    ok = result["correct"]
    return ok, {
        "id": case_id,
        "agent": agent_name,
        "status": "ok" if ok else "incorrect",
        "ok": ok,
        "picked": choice_id,
        "solution": item["solution_choice_id"],
        "gen_ms": ...,
        "grade_ms": ...,
        "stem_hash": ...,
        "error": None if ok else "...",
    }
```

**Report schema** (JSONL format):
```json
{
  "id": "vtx-1",
  "agent": "rules",
  "skill_id": "quad.graph.vertex",
  "difficulty": "easy",
  "seed": 42,
  "status": "ok",
  "ok": true,
  "picked": "D",
  "solution": "D",
  "gen_ms": 0.02,
  "grade_ms": 0.05,
  "stem_hash": "ce7c7133df",
  "error": null
}
```

---

### 5. **Seed Set** (`evals/seed_math.jsonl`)

6 deterministic test cases across 4 skills:

```jsonl
{"id":"vtx-1","skill_id":"quad.graph.vertex","difficulty":"easy","seed":42}
{"id":"std-1","skill_id":"quad.standard.vertex","difficulty":"easy","seed":11}
{"id":"roots-1","skill_id":"quad.roots.factored","difficulty":"medium","seed":12}
{"id":"fact-1","skill_id":"quad.solve.by_factoring","difficulty":"easy","seed":21}
{"id":"form-1","skill_id":"quad.solve.by_formula","difficulty":"easy","seed":31}
```

**Why deterministic?**
- Same seeds always generate same questions
- Enables comparing agents without variance
- Same results across machines, runs, processes

---

## Data Flow

### Typical Run: `make eval-agent agent=rules`

```
1. CLI: Makefile target
   └─ make eval-agent agent=rules

2. Load Registry
   └─ get_agent("rules") → RuleRouterAgent instance

3. Load Seed Set
   └─ agentic/evals/seed_math.jsonl → 6 test cases

4. For each test case:
   a. run_case(case, "rules")
      ├─ Generate item: generate_item("quad.graph.vertex", "easy", seed=42)
      ├─ Agent chooses: agent.choose(item) → "D"
      ├─ Grade: grade_response(item, "D") → {"correct": True}
      └─ Record: {"id": "vtx-1", "ok": True, "picked": "D", ...}
   
   b. Store result in list

5. Write report
   └─ agentic/evals/report.jsonl ← all results as JSONL

6. Print summary
   └─ "[eval] agent=rules  5/6 passed · accuracy=83.33%"
```

### Multi-Agent Comparison: `make eval-matrix`

```
Runs 4 agents sequentially:
├─ oracle    → report.oracle.jsonl    (100%)
├─ rules     → report.rules.jsonl     (83%)
├─ random    → report.random.jsonl    (67%)
└─ always_a  → report.always_a.jsonl  (33%)
```

Then summarize:
```
Agent         Cases  Passed  Accuracy
─────────────────────────────────────
oracle        6      6       100.00%
rules         6      5       83.33%
random        6      4       66.67%
always_a      6      2       33.33%
```

---

## How to Add a New Agent

### Step 1: Create agent class

Create `agentic/agents/my_agent.py`:

```python
from typing import Dict, Any
from .base import Agent

class MyAgent(Agent):
    name = "my_agent"
    
    def choose(self, item: Dict[str, Any]) -> str:
        # Your logic here
        # Return one of 'A', 'B', 'C', 'D'
        return "A"
```

### Step 2: Register it

Edit `agentic/agents/registry.py`:

```python
from .my_agent import MyAgent

_REGISTRY: Dict[str, Type[Agent]] = {
    "oracle": OracleAgent,
    "rules": RuleRouterAgent,
    "my_agent": MyAgent,  # <- ADD THIS
    # ...
}
```

### Step 3: Use it

```bash
make eval-agent agent=my_agent
```

---

## Running

### Run specific agent:
```bash
make eval-agent agent=rules         # Default
make eval-agent agent=random        # 67% baseline
make eval-agent agent=oracle        # 100% regression guard
make eval-agent agent=always_a      # 33% sanity check
```

### Compare all agents:
```bash
make eval-matrix
```

### Run tests:
```bash
make eval-test  # Contracts + integration tests
```

### Run full CI:
```bash
make eval-ci    # Tests + all agents
```

---

## Performance Summary

| Agent | Accuracy | Type | Purpose |
|-------|----------|------|---------|
| **oracle** | 100.00% | Regression guard | Verify engine/grader work |
| **rules** | 83.33% | Real math | Domain-specific solving |
| **random** | 66.67% | Baseline | Chance level |
| **always_a** | 33.33% | Sanity check | Verify shuffle isn't broken |

**Key insight:** Rules beats random by 16.7pp—real domain knowledge works!

---

## Test Coverage

- **16 agent tests** (`test_agents.py`): Registry, oracle, random, always_a
- **20 rule tests** (`test_rule_agents.py`): Parsing, math, integration
- **11 eval tests** (`test_eval_agents.py`): Harness contracts, error categorization, consistency
- **Total: 47 tests, all passing** ✅

---

## Next Steps

### Step 3: LLM Agent (Future)

```python
class LLMAgent(Agent):
    name = "llm"
    
    def choose(self, item: Dict[str, Any]) -> str:
        # Call GPT-4 with the question
        prompt = f"Question: {item['stem']}\nChoices: {[c['text'] for c in item['choices']]}\nAnswer:"
        response = client.chat.completions.create(...)
        # Extract choice A/B/C/D from response
        return parse_choice(response.content)
```

Would need:
- Cost tracking
- Eval gate: must beat rules (83%) + stay under budget
- Error handling for API failures
- Fallback to rules if API is down

---

## Summary

**The agentic framework is:**
- ✅ **Modular:** Each agent is a standalone class
- ✅ **Testable:** 47 comprehensive tests
- ✅ **Extensible:** Add agents in 3 simple steps
- ✅ **Deterministic:** SHA256 seeding, no randomness across runs
- ✅ **Measurable:** Accurate comparisons via identical test cases
- ✅ **Isolated:** No interference with live web/API code

**Current agents ready to use:**
- Oracle (100%) → Regression guard
- Rules (83%) → Real math
- Random (67%) → Baseline
- AlwaysA (33%) → Sanity check
