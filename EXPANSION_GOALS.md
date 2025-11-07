# Question Pool Expansion Goals

**Eval-Driven Development Targets for Question Pool Growth**

## 📊 Current Baseline (Before Expansion)
- **Total Templates**: 31
- **Skills**: 5 quadratic skills
- **Template Density**: 1.2-2.0 per difficulty/skill
- **Seed Evaluation Set**: 6 cases
- **Coverage Evaluation**: 100% (20/20 skill-difficulty combinations)

## 🎯 PHASE 1 Goals (Immediate - Expand Existing Skills)

### Quantitative Targets:
- **Total Templates**: 31 → 50 (+19 templates)
- **Template Density**: 2.0-3.0 per difficulty/skill
- **Seed Evaluation Set**: 6 → 15 cases (+9 cases)

### Specific Expansions:
1. **Balance Difficulty Distribution**
   - Hard: 5 → 10 templates (+5)
   - Applied: 6 → 10 templates (+4)
   - Medium: 9 → 12 templates (+3)
   - Easy: 11 → 18 templates (+7)

2. **Enhance Template Variety per Skill**
   - `quad.graph.vertex`: 5 → 8 templates (+3)
   - `quad.roots.factored`: 6 → 8 templates (+2)
   - `quad.solve.by_factoring`: 6 → 8 templates (+2)
   - `quad.solve.by_formula`: 6 → 8 templates (+2)
   - `quad.standard.vertex`: 8 → 10 templates (+2)

### Mathematical Diversity:
- **Coefficient Types**: Add fractions, decimals, radicals
- **Solution Types**: Include irrational and complex roots
- **Contexts**: Physics, business, geometry applications

## 🎯 PHASE 2 Goals (Next - Add New Skills)

### New Skills to Add:
1. **`quad.discriminant.analysis`** - Analyze nature of roots
2. **`quad.intercepts`** - Find x and y intercepts  
3. **`quad.complete.square`** - Completing the square method
4. **`quad.axis.symmetry`** - Find axis of symmetry

### Expansion Metrics:
- **Skills**: 5 → 9 (+4 new skills)
- **Total Templates**: 50 → 86 (+36 templates)
- **Coverage**: 20 → 36 skill-difficulty combinations

## ✅ Success Criteria (Measurable)

### Evaluation Metrics:
1. **Coverage Evaluation**: 100% on expanded skill set
2. **Rules Agent Accuracy**: Maintain 100% on expanded seed set
3. **Template Variety**: ≥2 template variations per skill-difficulty
4. **Mathematical Rigor**: Include edge cases and complex scenarios

### Quality Gates:
- [ ] All new templates pass validation (`make test`)
- [ ] Rules agent maintains 100% accuracy on seed set
- [ ] Coverage evaluation shows 100% skill-difficulty coverage
- [ ] Validity evaluation shows ≥95% item generation success
- [ ] Template variety analysis shows improved diversity

### Performance Targets:
- **Generation Speed**: Maintain <80ms p50 latency
- **Evaluation Time**: Full seed set eval <2 seconds
- **Test Coverage**: All new templates have corresponding tests

## 🔄 Implementation Strategy

### Phase 1 Implementation Order:
1. **Expand seed evaluation set** (add hard/applied cases)
2. **Add variety to existing skills** (new coefficient patterns)
3. **Enhance applied contexts** (realistic scenarios)
4. **Validate with evaluation infrastructure**

### Quality Assurance:
- Run `make eval-all` after each template addition
- Maintain test-driven development approach
- Use git commits to track progress incrementally

## 📈 Success Metrics Timeline

**Week 1**: Complete Phase 1
- Templates: 31 → 50
- Seed cases: 6 → 15
- All evaluations passing

**Week 2**: Begin Phase 2
- Add 2 new skills
- Implement rules for new skills
- Expand seed set to cover new skills

This expansion plan follows eval-driven development principles with measurable targets and continuous validation.