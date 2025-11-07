/**
 * Skills configuration and utilities
 */

import { SkillId, SkillInfo } from '@/types/agentic'

export const SKILL_DEFINITIONS: Record<SkillId, SkillInfo> = {
  'quad.graph.vertex': {
    id: 'quad.graph.vertex',
    name: 'Vertex from Graph',
    description: 'Find vertex coordinates from vertex form equations',
    template_count: 9,
    difficulties: ['easy', 'medium', 'hard', 'applied']
  },
  'quad.standard.vertex': {
    id: 'quad.standard.vertex',
    name: 'Vertex from Standard',
    description: 'Calculate vertex from standard form using formula',
    template_count: 10,
    difficulties: ['easy', 'medium', 'hard', 'applied']
  },
  'quad.roots.factored': {
    id: 'quad.roots.factored',
    name: 'Factored Roots',
    description: 'Extract roots from factored quadratic expressions',
    template_count: 8,
    difficulties: ['easy', 'medium', 'hard', 'applied']
  },
  'quad.solve.by_factoring': {
    id: 'quad.solve.by_factoring',
    name: 'Solve by Factoring',
    description: 'Solve quadratic equations using factoring method',
    template_count: 8,
    difficulties: ['easy', 'medium', 'hard', 'applied']
  },
  'quad.solve.by_formula': {
    id: 'quad.solve.by_formula',
    name: 'Quadratic Formula',
    description: 'Solve using the quadratic formula',
    template_count: 8,
    difficulties: ['easy', 'medium', 'hard', 'applied']
  },
  'quad.discriminant.analysis': {
    id: 'quad.discriminant.analysis',
    name: 'Discriminant Analysis',
    description: 'Calculate discriminant and analyze nature of roots',
    template_count: 7,
    difficulties: ['easy', 'medium', 'hard', 'applied']
  },
  'quad.intercepts': {
    id: 'quad.intercepts',
    name: 'X/Y Intercepts',
    description: 'Find x-intercepts and y-intercepts of quadratics',
    template_count: 7,
    difficulties: ['easy', 'medium', 'hard', 'applied']
  },
  'quad.complete.square': {
    id: 'quad.complete.square',
    name: 'Complete the Square',
    description: 'Transform to perfect square form',
    template_count: 7,
    difficulties: ['easy', 'medium', 'hard', 'applied']
  },
  'quad.axis.symmetry': {
    id: 'quad.axis.symmetry',
    name: 'Axis of Symmetry',
    description: 'Find axis of symmetry and solve parameter problems',
    template_count: 7,
    difficulties: ['easy', 'medium', 'hard', 'applied']
  }
}

export const AGENT_DEFINITIONS = {
  oracle: {
    name: 'Oracle Agent',
    description: 'Always knows the correct answer (ground truth)',
    color: 'bg-green-500',
    textColor: 'text-green-700'
  },
  rules: {
    name: 'Rules Agent',
    description: 'Deterministic rule-based mathematical reasoning',
    color: 'bg-blue-500',
    textColor: 'text-blue-700'
  },
  random: {
    name: 'Random Agent',
    description: 'Selects answers randomly (baseline comparison)',
    color: 'bg-purple-500',
    textColor: 'text-purple-700'
  }
}

export const DIFFICULTY_DEFINITIONS = {
  easy: { name: 'Easy', color: 'bg-green-100 text-green-800' },
  medium: { name: 'Medium', color: 'bg-yellow-100 text-yellow-800' },
  hard: { name: 'Hard', color: 'bg-red-100 text-red-800' },
  applied: { name: 'Applied', color: 'bg-purple-100 text-purple-800' }
}

export function getSkillName(skillId: SkillId): string {
  return SKILL_DEFINITIONS[skillId]?.name || skillId
}

export function getSkillDescription(skillId: SkillId): string {
  return SKILL_DEFINITIONS[skillId]?.description || ''
}

export function getAllSkills(): SkillInfo[] {
  return Object.values(SKILL_DEFINITIONS)
}

export function getTotalTemplates(): number {
  return Object.values(SKILL_DEFINITIONS).reduce(
    (sum, skill) => sum + skill.template_count, 
    0
  )
}