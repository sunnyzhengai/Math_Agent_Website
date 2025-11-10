'use client'

import { useState, useEffect } from 'react'
import { StudentProfile, SkillProgress, SkillId } from '@/types/learning'
import { learningApi } from '@/lib/learning-api'
import StudentDashboard from '@/components/StudentDashboard'
import SkillExplorer from '@/components/SkillExplorer'
import QuizInterface from '@/components/QuizInterface'
import StudentNavigation from '@/components/StudentNavigation'
import LoginPage from '@/components/LoginPage'
import ProgressDashboard from '@/components/ProgressDashboard'
import TeacherDashboard from '@/components/TeacherDashboard'

type ViewMode = 'dashboard' | 'skills' | 'quiz' | 'progress'
type UserRole = 'student' | 'teacher'

interface AuthState {
  isAuthenticated: boolean
  userId: string
  userName: string
  role: UserRole
}

export default function HomePage() {
  const [auth, setAuth] = useState<AuthState>({
    isAuthenticated: false,
    userId: '',
    userName: '',
    role: 'student'
  })
  const [currentView, setCurrentView] = useState<ViewMode>('skills')
  const [studentProfile, setStudentProfile] = useState<StudentProfile | null>(null)
  const [skillProgress, setSkillProgress] = useState<SkillProgress[]>([])
  const [selectedSkill, setSelectedSkill] = useState<SkillId | null>(null)
  const [loading, setLoading] = useState(true)

  // Teacher dashboard data
  const [students, setStudents] = useState<StudentProfile[]>([])
  const [classProgress, setClassProgress] = useState<Record<string, SkillProgress[]>>({})

  // Check for saved session on mount
  useEffect(() => {
    const savedAuth = localStorage.getItem('quadratic_mastery_auth')
    if (savedAuth) {
      try {
        const authData = JSON.parse(savedAuth)
        setAuth({ ...authData, isAuthenticated: true })
      } catch (error) {
        console.error('Error parsing saved auth:', error)
        localStorage.removeItem('quadratic_mastery_auth')
      }
    }
    setLoading(false)
  }, [])

  // Load data when authenticated
  useEffect(() => {
    if (auth.isAuthenticated) {
      if (auth.role === 'student') {
        loadStudentData()
      } else {
        loadTeacherData()
      }
    }
  }, [auth.isAuthenticated, auth.role])

  const handleLogin = (userId: string, userName: string, role: UserRole) => {
    const authData = { userId, userName, role }
    localStorage.setItem('quadratic_mastery_auth', JSON.stringify(authData))
    setAuth({ ...authData, isAuthenticated: true })
  }

  const handleLogout = () => {
    localStorage.removeItem('quadratic_mastery_auth')
    setAuth({ isAuthenticated: false, userId: '', userName: '', role: 'student' })
    setStudentProfile(null)
    setSkillProgress([])
    setCurrentView('skills')
  }

  const loadStudentData = async () => {
    try {
      setLoading(true)
      const [profile, progress] = await Promise.all([
        learningApi.getStudentProfile(auth.userId),
        learningApi.getSkillProgress(auth.userId)
      ])
      setStudentProfile(profile)
      setSkillProgress(progress)
    } catch (error) {
      console.error('Error loading student data:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadTeacherData = async () => {
    try {
      setLoading(true)
      // Mock data for demonstration - in production, this would come from the backend
      const mockStudents: StudentProfile[] = [
        {
          id: 'student_001',
          name: 'Julia Student',
          grade_level: '9th Grade',
          total_questions: 47,
          total_correct: 32,
          overall_accuracy: 68.1,
          total_time_spent: 2340,
          skills_mastered: 3,
          current_streak: 4,
          best_streak: 8,
          badges_earned: ['first_correct', 'speed_demon'],
          last_login: new Date().toISOString(),
          created_at: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString()
        },
        {
          id: 'student_002',
          name: 'Marcus Chen',
          grade_level: '9th Grade',
          total_questions: 63,
          total_correct: 51,
          overall_accuracy: 81.0,
          total_time_spent: 3120,
          skills_mastered: 5,
          current_streak: 7,
          best_streak: 12,
          badges_earned: ['first_correct', 'speed_demon', 'persistent_learner', 'perfect_score'],
          last_login: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
          created_at: new Date(Date.now() - 45 * 24 * 60 * 60 * 1000).toISOString()
        },
        {
          id: 'student_003',
          name: 'Sophia Rodriguez',
          grade_level: '9th Grade',
          total_questions: 28,
          total_correct: 14,
          overall_accuracy: 50.0,
          total_time_spent: 1540,
          skills_mastered: 1,
          current_streak: 2,
          best_streak: 4,
          badges_earned: ['first_correct'],
          last_login: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
          created_at: new Date(Date.now() - 20 * 24 * 60 * 60 * 1000).toISOString()
        },
        {
          id: 'student_004',
          name: 'Ethan Williams',
          grade_level: '9th Grade',
          total_questions: 55,
          total_correct: 42,
          overall_accuracy: 76.4,
          total_time_spent: 2880,
          skills_mastered: 4,
          current_streak: 5,
          best_streak: 9,
          badges_earned: ['first_correct', 'speed_demon', 'persistent_learner'],
          last_login: new Date(Date.now() - 0).toISOString(),
          created_at: new Date(Date.now() - 35 * 24 * 60 * 60 * 1000).toISOString()
        },
        {
          id: 'student_005',
          name: 'Olivia Brown',
          grade_level: '9th Grade',
          total_questions: 8,
          total_correct: 3,
          overall_accuracy: 37.5,
          total_time_spent: 480,
          skills_mastered: 0,
          current_streak: 0,
          best_streak: 2,
          badges_earned: [],
          last_login: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000).toISOString(),
          created_at: new Date(Date.now() - 15 * 24 * 60 * 60 * 1000).toISOString()
        },
        {
          id: 'student_006',
          name: 'Aiden Davis',
          grade_level: '9th Grade',
          total_questions: 71,
          total_correct: 59,
          overall_accuracy: 83.1,
          total_time_spent: 3600,
          skills_mastered: 6,
          current_streak: 9,
          best_streak: 15,
          badges_earned: ['first_correct', 'speed_demon', 'persistent_learner', 'perfect_score', 'mastery_milestone'],
          last_login: new Date(Date.now() - 0).toISOString(),
          created_at: new Date(Date.now() - 50 * 24 * 60 * 60 * 1000).toISOString()
        }
      ]

      // Generate mock skill progress for each student
      const mockClassProgress: Record<string, SkillProgress[]> = {}
      mockStudents.forEach(student => {
        mockClassProgress[student.id] = learningApi['mockSkillProgress'](student.id)
      })

      setStudents(mockStudents)
      setClassProgress(mockClassProgress)
    } catch (error) {
      console.error('Error loading teacher data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleStartQuiz = (skillId?: SkillId) => {
    setSelectedSkill(skillId || null)
    setCurrentView('quiz')
  }

  const handleQuizComplete = () => {
    // Refresh data after quiz completion
    loadStudentData()
    setCurrentView('skills')
  }

  // Show login page if not authenticated
  if (!auth.isAuthenticated) {
    return <LoginPage onLogin={handleLogin} />
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your {auth.role === 'teacher' ? 'dashboard' : 'learning journey'}...</p>
        </div>
      </div>
    )
  }

  // Teacher View
  if (auth.role === 'teacher') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-pink-50">
        {/* Teacher Navigation */}
        <nav className="bg-white shadow-sm border-b border-gray-200 fixed top-0 w-full z-50">
          <div className="container mx-auto px-4">
            <div className="flex items-center justify-between h-16">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-lg">QM</span>
                </div>
                <div>
                  <h1 className="text-xl font-bold text-gray-900">Quadratic Mastery</h1>
                  <p className="text-xs text-gray-500">Teacher Dashboard</p>
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-600">{auth.userName}</span>
                <button
                  onClick={handleLogout}
                  className="text-sm text-gray-600 hover:text-gray-900 font-medium"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </nav>

        <main className="pt-24 pb-8">
          <TeacherDashboard students={students} classProgress={classProgress} />
        </main>
      </div>
    )
  }

  // Student View
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <StudentNavigation
        currentView={currentView}
        onViewChange={setCurrentView}
        studentProfile={studentProfile}
        onLogout={handleLogout}
      />

      <main className="pt-24 pb-8">
        {currentView === 'dashboard' && (
          <StudentDashboard
            studentProfile={studentProfile}
            skillProgress={skillProgress}
            onStartQuiz={handleStartQuiz}
          />
        )}

        {currentView === 'skills' && (
          <SkillExplorer
            skillProgress={skillProgress}
            onStartQuiz={handleStartQuiz}
          />
        )}

        {currentView === 'quiz' && (
          <QuizInterface
            studentId={auth.userId}
            selectedSkill={selectedSkill}
            onComplete={handleQuizComplete}
            onExit={() => setCurrentView('skills')}
          />
        )}

        {currentView === 'progress' && (
          <ProgressDashboard
            studentProfile={studentProfile}
            skillProgress={skillProgress}
          />
        )}
      </main>
    </div>
  )
}
