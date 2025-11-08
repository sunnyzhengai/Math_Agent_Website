/**
 * API client for the Student Learning Platform
 */

import axios, { AxiosInstance } from 'axios'
import { 
  Question, 
  StudentResponse, 
  QuestionResult, 
  SkillProgress, 
  StudentProfile,
  SkillId, 
  Difficulty,
  AdaptiveRecommendation 
} from '@/types/learning'

class LearningApiClient {
  private client: AxiosInstance
  private difficultyProgression: Map<string, number> = new Map() // Track progress per skill

  constructor() {
    const baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

    this.client = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }

  // Student management
  async getStudentProfile(studentId: string): Promise<StudentProfile> {
    // TODO: Implement endpoint
    return this.mockStudentProfile(studentId)
  }

  async updateStudentProfile(studentId: string, updates: Partial<StudentProfile>): Promise<StudentProfile> {
    // TODO: Implement endpoint
    return this.mockStudentProfile(studentId)
  }

  // Adaptive question generation
  async getNextQuestion(studentId: string, skillId?: SkillId): Promise<Question> {
    try {
      // If skill specified, use it; otherwise get adaptive recommendation
      const targetSkill = skillId || await this.getAdaptiveRecommendation(studentId)
      const skill = typeof targetSkill === 'string' ? targetSkill : targetSkill.next_skill

      // Get current difficulty for this skill (cycles through easy→medium→hard)
      // Note: Removed 'applied' - using parameterized generation for infinite variations instead
      const difficulties: Difficulty[] = ['easy', 'medium', 'hard']
      const sessionKey = `${studentId}_${skill}`

      // Get the current difficulty index for this session (defaults to 0 = 'easy')
      const currentDifficultyIndex = this.difficultyProgression.get(sessionKey) || 0
      const currentDifficulty = difficulties[currentDifficultyIndex]

      const response = await this.client.post('/items/generate', {
        skill_id: skill,
        difficulty: typeof targetSkill === 'string' ? currentDifficulty : targetSkill.next_difficulty,
        mode: 'cycle',
        session_id: sessionKey,
        use_parameterized: true  // Enable infinite question variations with difficulty-aware distractors
      })

      const question = response.data

      // Check if we've exhausted the current difficulty level
      if (question.pool_exhausted) {
        // Move to next difficulty level
        const nextIndex = (currentDifficultyIndex + 1) % difficulties.length
        this.difficultyProgression.set(sessionKey, nextIndex)
        console.log(`[Quiz] Completed ${currentDifficulty}, moving to ${difficulties[nextIndex]}`)
      }

      return question
    } catch (error) {
      console.error('Error getting next question:', error)
      return this.mockQuestion()
    }
  }

  // Question submission and grading
  async submitAnswer(
    studentId: string, 
    question: Question, 
    response: StudentResponse
  ): Promise<QuestionResult> {
    try {
      const gradeResponse = await this.client.post('/grade', {
        item: question,
        choice_id: response.selected_choice,
        session_id: `student_${studentId}`
      })

      // Update student progress (this would be handled by backend)
      await this.updateProgress(studentId, question.skill_id, gradeResponse.data.correct, response.time_taken)

      return {
        correct: gradeResponse.data.correct,
        solution_choice_id: gradeResponse.data.solution_choice_id,
        explanation: gradeResponse.data.explanation,
        time_taken: response.time_taken
      }
    } catch (error) {
      console.error('Error submitting answer:', error)
      return this.mockQuestionResult()
    }
  }

  // Progress tracking
  async getSkillProgress(studentId: string, skillId?: SkillId): Promise<SkillProgress[]> {
    // TODO: Implement endpoint
    return this.mockSkillProgress()
  }

  async updateProgress(
    studentId: string, 
    skillId: SkillId, 
    correct: boolean, 
    timeTaken: number
  ): Promise<void> {
    // TODO: Implement endpoint - this would update mastery levels
    console.log(`Updating progress for ${studentId}: ${skillId} - ${correct ? 'correct' : 'incorrect'}`)
  }

  // Adaptive recommendations
  async getAdaptiveRecommendation(studentId: string): Promise<AdaptiveRecommendation> {
    // TODO: Implement endpoint that analyzes student progress and recommends next skill/difficulty
    return this.mockAdaptiveRecommendation()
  }

  // Learning analytics
  async getStudentAnalytics(studentId: string, timeframe: string = '30d') {
    // TODO: Implement endpoint
    return this.mockAnalytics()
  }

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    const response = await this.client.get('/health')
    return response.data
  }

  // Mock implementations (replace with real endpoints)
  private mockStudentProfile(studentId: string): StudentProfile {
    return {
      id: studentId,
      name: 'Julia Student',
      grade_level: '9th Grade',
      total_questions: 47,
      total_correct: 32,
      overall_accuracy: 68.1,
      total_time_spent: 2340, // seconds
      skills_mastered: 3,
      current_streak: 4,
      best_streak: 8,
      badges_earned: ['first_correct', 'speed_demon', 'persistent_learner'],
      last_login: new Date().toISOString(),
      created_at: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString()
    }
  }

  private mockQuestion(): Question {
    return {
      item_id: 'mock_question_1',
      skill_id: 'quad.graph.vertex',
      difficulty: 'easy',
      stem: 'For y = (x - 3)² + 2, what is the vertex?',
      choices: [
        { id: 'A', text: '(3, 2)' },
        { id: 'B', text: '(-3, 2)' },
        { id: 'C', text: '(3, -2)' },
        { id: 'D', text: '(2, 3)' }
      ],
      solution_choice_id: 'A',
      solution_text: '(3, 2)',
      tags: ['vertex_form']
    }
  }

  private mockQuestionResult(): QuestionResult {
    return {
      correct: Math.random() > 0.3, // 70% chance of being correct
      solution_choice_id: 'A',
      explanation: 'The vertex form y = a(x - h)² + k has vertex (h, k).',
      time_taken: 15000
    }
  }

  private mockSkillProgress(): SkillProgress[] {
    const skills: SkillId[] = [
      'quad.graph.vertex',
      'quad.standard.vertex', 
      'quad.roots.factored',
      'quad.solve.by_factoring',
      'quad.solve.by_formula'
    ]

    return skills.map(skill => ({
      skill_id: skill,
      mastery_level: ['beginner', 'developing', 'proficient', 'advanced'][Math.floor(Math.random() * 4)] as any,
      progress_percentage: Math.floor(Math.random() * 100),
      questions_attempted: Math.floor(Math.random() * 20) + 5,
      questions_correct: Math.floor(Math.random() * 15) + 2,
      current_streak: Math.floor(Math.random() * 8),
      best_streak: Math.floor(Math.random() * 12) + 3,
      total_time_spent: Math.floor(Math.random() * 1800) + 300,
      last_activity: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString()
    }))
  }

  private mockAdaptiveRecommendation(): AdaptiveRecommendation {
    const skills: SkillId[] = ['quad.graph.vertex', 'quad.standard.vertex', 'quad.solve.by_factoring']
    const difficulties: Difficulty[] = ['easy', 'medium', 'hard']
    
    return {
      next_skill: skills[Math.floor(Math.random() * skills.length)],
      next_difficulty: difficulties[Math.floor(Math.random() * difficulties.length)],
      reason: 'Based on your recent performance, this will help strengthen your foundation.',
      confidence: 0.85
    }
  }

  private mockAnalytics() {
    return {
      accuracy_trend: Array.from({ length: 7 }, (_, i) => ({
        date: new Date(Date.now() - i * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        accuracy: Math.random() * 40 + 60
      })),
      questions_per_day: Array.from({ length: 7 }, (_, i) => ({
        date: new Date(Date.now() - i * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        count: Math.floor(Math.random() * 10) + 2
      }))
    }
  }
}

export const learningApi = new LearningApiClient()
export default learningApi