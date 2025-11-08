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

interface ProgressTracker {
  difficulty_index: number
  consecutive_correct: number
  total_attempts: number
  mastered: boolean
}

class LearningApiClient {
  private client: AxiosInstance
  private progressTrackers: Map<string, ProgressTracker> = new Map() // Track progress per skill
  private studentProfiles: Map<string, StudentProfile> = new Map() // Store student profiles
  private skillProgressData: Map<string, SkillProgress[]> = new Map() // Store skill progress per student
  private readonly MASTERY_THRESHOLD = 3 // Number of consecutive correct to advance
  private readonly DIFFICULTIES: Difficulty[] = ['easy', 'medium', 'hard']

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

      const sessionKey = `${studentId}_${skill}`

      // Get or initialize progress tracker for this skill
      let tracker = this.progressTrackers.get(sessionKey)
      if (!tracker) {
        tracker = {
          difficulty_index: 0,
          consecutive_correct: 0,
          total_attempts: 0,
          mastered: false
        }
        this.progressTrackers.set(sessionKey, tracker)
      }

      // Check if skill is fully mastered (all difficulties completed)
      if (tracker.mastered) {
        console.log(`[Quiz] Skill ${skill} fully mastered, recommending different skill`)
        // Get a different skill recommendation
        const recommendation = await this.getAdaptiveRecommendation(studentId)
        return this.getNextQuestion(studentId, typeof recommendation === 'string' ? recommendation : recommendation.next_skill)
      }

      const currentDifficulty = this.DIFFICULTIES[tracker.difficulty_index]

      const response = await this.client.post('/items/generate', {
        skill_id: skill,
        difficulty: typeof targetSkill === 'string' ? currentDifficulty : targetSkill.next_difficulty,
        mode: 'cycle',
        session_id: sessionKey,
        use_parameterized: true  // Enable infinite question variations with difficulty-aware distractors
      })

      return response.data
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

      // Update local progress tracker based on result
      this.updateProgressTracker(studentId, question.skill_id, gradeResponse.data.correct)

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
    return this.mockSkillProgress(studentId)
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

  // Private helper: Update progress tracker based on answer correctness
  private updateProgressTracker(studentId: string, skillId: SkillId, correct: boolean): void {
    const sessionKey = `${studentId}_${skillId}`
    let tracker = this.progressTrackers.get(sessionKey)

    if (!tracker) {
      tracker = {
        difficulty_index: 0,
        consecutive_correct: 0,
        total_attempts: 0,
        mastered: false
      }
      this.progressTrackers.set(sessionKey, tracker)
    }

    tracker.total_attempts++

    if (correct) {
      tracker.consecutive_correct++

      // Check if mastery threshold reached for current difficulty
      if (tracker.consecutive_correct >= this.MASTERY_THRESHOLD) {
        const currentDifficulty = this.DIFFICULTIES[tracker.difficulty_index]

        // Advance to next difficulty
        if (tracker.difficulty_index < this.DIFFICULTIES.length - 1) {
          tracker.difficulty_index++
          tracker.consecutive_correct = 0 // Reset streak for new difficulty
          const nextDifficulty = this.DIFFICULTIES[tracker.difficulty_index]
          console.log(`[Adaptive] ✓ Mastered ${currentDifficulty} for ${skillId}! Advancing to ${nextDifficulty}`)
        } else {
          // Completed all difficulties - mark as fully mastered
          tracker.mastered = true
          console.log(`[Adaptive] ⭐ Fully mastered ${skillId} at all difficulty levels!`)
        }
      }
    } else {
      // Wrong answer - reset consecutive streak but stay at current difficulty
      if (tracker.consecutive_correct > 0) {
        console.log(`[Adaptive] Streak broken for ${skillId}, resetting to 0 (was ${tracker.consecutive_correct})`)
      }
      tracker.consecutive_correct = 0
    }
  }

  // Mock implementations (replace with real endpoints)
  private mockStudentProfile(studentId: string): StudentProfile {
    // Check if profile already exists
    const existing = this.studentProfiles.get(studentId)
    if (existing) {
      // Update last login and return
      existing.last_login = new Date().toISOString()
      return existing
    }

    // Create new profile for this student
    // Extract name from studentId (format: "student_first_last" or "teacher_name")
    let name = 'Student'
    const parts = studentId.split('_')
    if (parts.length > 1) {
      // Convert "student_john_doe" to "John Doe"
      name = parts.slice(1)
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
    }

    const newProfile: StudentProfile = {
      id: studentId,
      name: name,
      grade_level: '9th Grade',
      total_questions: 0,
      total_correct: 0,
      overall_accuracy: 0,
      total_time_spent: 0,
      skills_mastered: 0,
      current_streak: 0,
      best_streak: 0,
      badges_earned: [],
      last_login: new Date().toISOString(),
      created_at: new Date().toISOString()
    }

    // Store the new profile
    this.studentProfiles.set(studentId, newProfile)
    return newProfile
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

  private mockSkillProgress(studentId: string): SkillProgress[] {
    // Check if progress already exists for this student
    const existing = this.skillProgressData.get(studentId)
    if (existing) {
      return existing
    }

    // Create fresh progress for new student - all skills start with no progress
    const skills: SkillId[] = [
      'quad.graph.vertex',
      'quad.standard.vertex',
      'quad.roots.factored',
      'quad.solve.by_factoring',
      'quad.solve.by_formula',
      'quad.discriminant.analysis',
      'quad.intercepts',
      'quad.complete.square',
      'quad.axis.symmetry'
    ]

    const freshProgress: SkillProgress[] = skills.map(skill => ({
      skill_id: skill,
      mastery_level: 'beginner' as any,
      progress_percentage: 0,
      questions_attempted: 0,
      questions_correct: 0,
      current_streak: 0,
      best_streak: 0,
      total_time_spent: 0,
      last_activity: new Date().toISOString()
    }))

    // Store the new progress
    this.skillProgressData.set(studentId, freshProgress)
    return freshProgress
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