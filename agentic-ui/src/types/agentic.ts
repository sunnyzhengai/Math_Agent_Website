/**
 * TypeScript definitions for the Agentic Math System
 */

export type AgentType = 'oracle' | 'rules' | 'random'

export type SkillId = 
  | 'quad.graph.vertex'
  | 'quad.standard.vertex'
  | 'quad.roots.factored'
  | 'quad.solve.by_factoring'
  | 'quad.solve.by_formula'
  | 'quad.discriminant.analysis'
  | 'quad.intercepts'
  | 'quad.complete.square'
  | 'quad.axis.symmetry'

export type Difficulty = 'easy' | 'medium' | 'hard' | 'applied'

export interface Choice {
  id: string
  text: string
}

export interface MathItem {
  item_id: string
  skill_id: SkillId
  difficulty: Difficulty
  stem: string
  choices: Choice[]
  solution_choice_id: string
  solution_text: string
  tags: string[]
}

export interface AgentResponse {
  agent: AgentType
  choice: string
  confidence?: number
  reasoning?: string
}

export interface EvaluationResult {
  id: string
  agent: AgentType
  skill_id: SkillId
  difficulty: Difficulty
  seed: number
  status: 'ok' | 'incorrect' | 'agent_error'
  ok: boolean
  picked: string | null
  solution: string
  gen_ms: number
  grade_ms: number | null
  stem_hash: string
  error: string | null
}

export interface AgentPerformance {
  agent: AgentType
  total_cases: number
  correct: number
  accuracy: number
  by_skill: Record<SkillId, {
    total: number
    correct: number
    accuracy: number
  }>
  by_difficulty: Record<Difficulty, {
    total: number
    correct: number
    accuracy: number
  }>
}

export interface SkillInfo {
  id: SkillId
  name: string
  description: string
  template_count: number
  difficulties: Difficulty[]
}

export interface SeedCase {
  id: string
  skill_id: SkillId
  difficulty: Difficulty
  seed: number
}

export interface TemplateInfo {
  skill_id: SkillId
  difficulty: Difficulty
  count: number
  sample_stem?: string
}