/**
 * TypeScript definitions for the Student Learning Platform
 */

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
  // Julia's Current Curriculum (Immediate Priority)
  | 'quad.complete.square.solve'
  | 'quad.solve.square_root_property'
  | 'quad.solve.factoring'
  | 'quad.factoring.review'
  | 'quad.solutions.graphical'
  // New Algebra 1 Skills (Phase 1 - PAUSED)
  | 'quad.transformations'
  | 'quad.form.conversions'
  | 'quad.solve.inequalities'
  | 'quad.applications.maxmin'
  | 'quad.domain.range'
  | 'quad.solutions.count'

export type Difficulty = 'easy' | 'medium' | 'hard' | 'applied'

export type MasteryLevel = 'beginner' | 'developing' | 'proficient' | 'advanced' | 'expert'

export interface Choice {
  id: string
  text: string
}

export interface Question {
  item_id: string
  skill_id: SkillId
  difficulty: Difficulty
  stem: string
  choices: Choice[]
  solution_choice_id: string
  solution_text: string
  tags: string[]
  pool_exhausted?: boolean  // True when all templates have been seen
  templates_remaining?: number  // How many templates left in pool
}

export interface StudentResponse {
  question_id: string
  selected_choice: string
  time_taken: number
  confidence?: number
}

export interface QuestionResult {
  correct: boolean
  solution_choice_id: string
  explanation: string
  time_taken: number
}

export interface SkillProgress {
  skill_id: SkillId
  mastery_level: MasteryLevel
  progress_percentage: number
  questions_attempted: number
  questions_correct: number
  current_streak: number
  best_streak: number
  total_time_spent: number
  last_activity: string
}

export interface StudentProfile {
  id: string
  name: string
  grade_level?: string
  total_questions: number
  total_correct: number
  overall_accuracy: number
  total_time_spent: number
  skills_mastered: number
  current_streak: number
  best_streak: number
  badges_earned: string[]
  last_login: string
  created_at: string
}

export interface LearningSession {
  id: string
  student_id: string
  skill_id: SkillId
  questions_answered: number
  questions_correct: number
  time_spent: number
  started_at: string
  completed_at?: string
}

export interface Badge {
  id: string
  name: string
  description: string
  icon: string
  criteria: string
  rarity: 'common' | 'rare' | 'epic' | 'legendary'
}

export interface SkillDefinition {
  id: SkillId
  name: string
  description: string
  learning_objectives: string[]
  prerequisites: SkillId[]
  difficulty_progression: Difficulty[]
  estimated_time: number // minutes
  icon: string
}

// Learning analytics
export interface PerformanceMetrics {
  accuracy_trend: { date: string; accuracy: number }[]
  speed_trend: { date: string; avg_time: number }[]
  skill_mastery: { skill_id: SkillId; level: MasteryLevel }[]
  daily_progress: { date: string; questions: number; correct: number }[]
}

// Adaptive learning
export interface AdaptiveRecommendation {
  next_skill: SkillId
  next_difficulty: Difficulty
  reason: string
  confidence: number
}