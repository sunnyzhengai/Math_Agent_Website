// API Types matching FastAPI backend

export interface Choice {
  id: string
  text: string
  tags_on_select: string[]
}

export interface Item {
  item_id: string
  skill_id: string
  difficulty: 'easy' | 'medium' | 'hard' | 'applied'
  stem: string
  choices: Choice[]
  hints?: string[]
  explanation?: string
  confidence_target?: number
}

export interface Skill {
  id: string
  name: string
  description?: string
  difficulty?: string
  prerequisites?: string[]
}

export interface NextItemResponse {
  item: Item
  reason: string
  difficulty: string
  learner_mastery_before: number
}

export interface GradeResponse {
  correct: boolean
  tags: string[]
  p_mastery_after: number
  attempts_on_skill: number
  next_due_at?: string | null
  suggested_resource_url?: string | null
}

export interface SkillProgress {
  skill_id: string
  name: string
  p_mastery: number
  attempts: number
  correct_count: number
  streak: number
  last_attempt?: string | null
  due_at?: string | null
  top_errors?: Array<{ tag: string; count: number }>
}

export interface ProgressResponse {
  user_id: string
  domain: string
  skills: SkillProgress[]
  top_misconceptions: Array<{
    tag: string
    count: number
    skill_ids: string[]
  }>
  weekly_stats: {
    attempts_this_week: number
    correct_this_week: number
    accuracy_this_week: number
    skills_with_progress: number
  }
  due_today: SkillProgress[]
}

export interface UserSession {
  user_id: string
  email: string
  role: 'student' | 'teacher' | 'admin'
  authenticated_at: string
}
