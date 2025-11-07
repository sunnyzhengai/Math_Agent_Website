# Agentic Math UI

Modern web interface for the comprehensive rule-based mathematical agent system.

## Features

### 🎯 Agent Playground
- Interactive testing of rule-based agents (Oracle, Rules, Random)
- Real-time question generation across 9 quadratic skills
- 4 difficulty levels with comprehensive template coverage
- Live agent response testing and accuracy feedback

### 📚 Skill Explorer  
- Browse 71 mathematical templates across 9 skills
- Skill-by-skill breakdown with template counts
- Difficulty distribution visualization
- Direct links to playground testing

### 🧪 Evaluation Center
- Comprehensive 36-case seed evaluation
- Agent performance analytics by skill and difficulty
- Detailed test case results with timing metrics
- Reproducible evaluation framework

### 📊 System Overview
- **9 Quadratic Skills**: Complete domain coverage
- **71 Templates**: Extensive question variety  
- **36 Seed Cases**: Comprehensive evaluation dataset
- **69% Rules Accuracy**: Proven performance metrics

## Architecture

### Tech Stack
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Modern styling system
- **Heroicons** - Professional icon library

### Agent System Integration
- **Rule-Based Agents**: Deterministic mathematical reasoning
- **Template Engine**: 71 templates across skill matrix
- **Evaluation Framework**: 36-case comprehensive testing
- **Performance Analytics**: Real-time accuracy tracking

## Development

### Prerequisites
- Node.js 18+
- Backend API running on port 8000

### Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Open browser to http://localhost:3000
```

### Environment Variables
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000  # Backend API URL
```

### Build & Deploy
```bash
# Production build
npm run build

# Start production server
npm start
```

## Backend Integration

The UI connects to the agentic math backend for:
- Question generation via `/items/generate`
- Response grading via `/grade` 
- Skills manifest via `/skills/manifest`
- Agent evaluation (planned endpoint)

## Skill Coverage

### Core Quadratic Skills (9)
1. **quad.graph.vertex** - Vertex from graph form
2. **quad.standard.vertex** - Vertex from standard form  
3. **quad.roots.factored** - Extract roots from factored form
4. **quad.solve.by_factoring** - Solve by factoring method
5. **quad.solve.by_formula** - Quadratic formula solver
6. **quad.discriminant.analysis** - Discriminant calculation
7. **quad.intercepts** - X/Y intercept finding
8. **quad.complete.square** - Completing the square
9. **quad.axis.symmetry** - Axis of symmetry calculation

### Template Distribution
- **Easy**: 18 templates
- **Medium**: 17 templates  
- **Hard**: 18 templates
- **Applied**: 18 templates
- **Total**: 71 comprehensive templates

## Agent Performance

### Current Metrics (Phase 3)
- **Rules Agent**: 69.44% accuracy (25/36 cases)
- **Oracle Agent**: 100% accuracy (ground truth)
- **Random Agent**: ~25% accuracy (baseline)

### Evaluation Framework
- **36 Seed Cases**: Deterministic evaluation set
- **Full Coverage**: All skills × all difficulties
- **Reproducible**: Fixed seeds for consistent testing
- **Comprehensive**: Covers edge cases and complexity

Built with modern web technologies to showcase the sophisticated mathematical reasoning capabilities of our rule-based agent system.