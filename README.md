# Agent Math Learning Platform

**AI-native adaptive math learning system focused on building permanent neural pathways**

---

## 🚀 Project Status: Dual-Track Development

This repository contains **two parallel implementations** as we transition from template-based to neural pathway formation approach:

### ✅ V1: Template-Based System (Production - Stable)
- **Branch:** `phase1-data-flywheel` (production), `v1-template-based` (archive)
- **Status:** Production, maintenance mode
- **URL:** https://themathagent.com
- **Approach:** Hand-crafted templates, deterministic progression
- **Users:** Julia (daily homework support)

### 🔬 V2: Neural Pathway Formation Engine (Development - Experimental)
- **Branch:** `v2-neural-engine`
- **Status:** Active development
- **Approach:** First-principles learning science, AI-native question generation
- **Goal:** Build mathematical neural pathways optimally, not just deliver questions

---

## 📚 Documentation

### V2 Design (Read This First!)
- **[First Principles Analysis](docs/v2-design/FIRST_PRINCIPLES_ANALYSIS.md)** - Why we're rebuilding from scratch
- **[V2 Architecture](docs/v2-design/ARCHITECTURE_V2.md)** - Technical design
- **[Transition Plan](docs/v2-design/TRANSITION_PLAN.md)** - Development roadmap

### V1 Documentation
- See existing docs for v1 system

---

## 🌿 Branch Strategy

```
Repository: Agent_Math

Branches:
├── main
│   └── Stable baseline
│
├── phase1-data-flywheel (V1 Production)
│   └── Current production system
│   └── Maintenance only (bug fixes, keep stable for Julia)
│
├── v1-template-based (V1 Archive)
│   └── Frozen snapshot of v1 before v2 development
│   └── Reference only, no active development
│
└── v2-neural-engine (V2 Development) ⭐
    └── New architecture based on first principles
    └── Active development
```

---

## 🏃 Quick Start

### Run V1 (Current Production)

```bash
# Backend (FastAPI)
cd /Users/sunnyzheng/Agent_Math
make serve  # Runs on http://localhost:8000

# Frontend (Next.js)
cd math-learning-platform
npm run dev -- -p 3001  # Runs on http://localhost:3001
```

### Run V2 (When Ready)

```bash
cd /Users/sunnyzheng/Agent_Math/v2
# Instructions will be added as v2 is built
```

---

## 🎯 Why V2? (The First Principles Rethink)

### The Problem with V1
- ✅ Works well for first exposure
- ❌ Questions become repetitive (limited template pool)
- ❌ Doesn't adapt to individual learning patterns
- ❌ Doesn't understand student's mental model
- ❌ Generic feedback, not diagnostic

### The V2 Vision
- ✅ Infinite question variations (never repetitive)
- ✅ Tracks student's mental model (not just metrics)
- ✅ Instant feedback (< 500ms, triggers dopamine)
- ✅ Diagnostic misconception identification
- ✅ Adapts to individual neural pathway formation
- ✅ Natural language intent understanding
- ✅ Matches teacher's style when needed

**Read the full analysis:** [First Principles](docs/v2-design/FIRST_PRINCIPLES_ANALYSIS.md)

---

## 📊 Current Stats

### V1 System
- **Skills:** 20 quadratic skills
- **Templates:** 190 hand-crafted questions
- **Students:** 1 (Julia)
- **Status:** Production-ready, deployed

### V2 System
- **Status:** Design phase (Week 1)
- **Timeline:** 4-6 weeks to MVP
- **Testing:** Weekend experiments with Julia

---

## 🏗️ Project Structure (Current)

```
/Agent_Math
├── api/                    # V1 FastAPI backend
├── engine/                 # V1 question templates & grading
├── math-learning-platform/ # V1 Next.js frontend
├── agentic/               # Existing agent infrastructure
│
├── docs/
│   ├── v2-design/         # V2 design documents ⭐
│   └── ...                # V1 documentation
│
├── data/                  # Student progress data
├── logs/                  # Telemetry
└── tests/                 # Test suites
```

**Future structure (after v2 starts):**
```
/Agent_Math
├── v1/                    # Current system (moved here)
├── v2/                    # New architecture
├── shared/                # Code used by both
└── docs/                  # All documentation
```

---

## 🔬 Development Workflow

### For V1 (Maintenance)
```bash
git checkout phase1-data-flywheel
# Make bug fixes only
# Keep Julia's experience stable
git push origin phase1-data-flywheel
# Auto-deploys to themathagent.com
```

### For V2 (Active Development)
```bash
git checkout v2-neural-engine
# Build new architecture
# Test with Julia on weekends
git push origin v2-neural-engine
# Will deploy to v2-preview.themathagent.com (when ready)
```

---

## 📈 Success Metrics

### V1 Baseline (To Beat)
- Time to mastery: ~2 weeks per skill
- Questions needed: Fixed 20 per skill
- Julia's feedback: "Questions feel repetitive"

### V2 Goals
- Time to mastery: < 1 week per skill (50% reduction)
- Questions needed: Adaptive (until automaticity achieved)
- Julia's feedback: "Feels personalized and fresh"
- Measurable: Speed of response (automatic = < 60s per question)

---

## 🤝 Contributing

### Philosophy
This project is built on **first principles thinking**:
1. Question conventional education approaches
2. Start from brain science (how learning actually works)
3. Optimize for neural pathway formation, not test scores
4. Use AI where it adds value (generation, adaptation)
5. Keep deterministic what should be deterministic (grading, validation)

### Before Contributing
- Read [First Principles Analysis](docs/v2-design/FIRST_PRINCIPLES_ANALYSIS.md)
- Understand the "why" before the "how"
- V1: Maintenance only (bug fixes)
- V2: Open to design discussion

---

## 📞 Contact

**User:** Julia (10th grade, Honors Compacted Algebra 2)
**Developer:** Sunny Zheng
**Status:** Private project, not yet open source

---

## 🗺️ Roadmap

### Phase 0: Housekeeping ✅ (Week 1, Days 1-2)
- ✅ Document first principles
- ✅ Create branch structure
- ✅ Update README (this document)

### Phase 1: Foundation (Week 1, Days 3-7)
- [ ] Mental model specification
- [ ] Skill graph schema
- [ ] Question generation protocol
- [ ] API specification

### Phase 2-3: Core + API (Weeks 2-3)
- [ ] Implement core components
- [ ] Build API layer
- [ ] Performance optimization (< 500ms)

### Phase 4: Minimal UI (Week 4-5)
- [ ] Natural language landing page
- [ ] Instant feedback quiz interface
- [ ] Deploy to v2-preview

### Phase 5-6: Testing + Expansion (Weeks 5-6+)
- [ ] Julia tests v2 vs v1
- [ ] Measure and iterate
- [ ] Add more skills
- [ ] Prepare for migration

---

## 📝 License

Private project - All rights reserved

---

**Last Updated:** November 12, 2025
**Current Focus:** V2 Design Phase
