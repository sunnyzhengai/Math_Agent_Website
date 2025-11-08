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

type ViewMode = 'dashboard' | 'skills' | 'quiz' | 'progress'

interface AuthState {
  isAuthenticated: boolean
  studentId: string
  studentName: string
}

export default function HomePage() {
  const [auth, setAuth] = useState<AuthState>({ isAuthenticated: false, studentId: '', studentName: '' })
  const [currentView, setCurrentView] = useState<ViewMode>('dashboard')
  const [studentProfile, setStudentProfile] = useState<StudentProfile | null>(null)
  const [skillProgress, setSkillProgress] = useState<SkillProgress[]>([])
  const [selectedSkill, setSelectedSkill] = useState<SkillId | null>(null)
  const [loading, setLoading] = useState(true)

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

  // Load student data when authenticated
  useEffect(() => {
    if (auth.isAuthenticated) {
      loadStudentData()
    }
  }, [auth.isAuthenticated])

  const handleLogin = (studentId: string, studentName: string) => {
    const authData = { studentId, studentName }
    localStorage.setItem('quadratic_mastery_auth', JSON.stringify(authData))
    setAuth({ ...authData, isAuthenticated: true })
  }

  const handleLogout = () => {
    localStorage.removeItem('quadratic_mastery_auth')
    setAuth({ isAuthenticated: false, studentId: '', studentName: '' })
    setCurrentView('dashboard')
  }

  const loadStudentData = async () => {
    try {
      setLoading(true)
      const [profile, progress] = await Promise.all([
        learningApi.getStudentProfile(auth.studentId),
        learningApi.getSkillProgress(auth.studentId)
      ])
      setStudentProfile(profile)
      setSkillProgress(progress)
    } catch (error) {
      console.error('Error loading student data:', error)
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
    setCurrentView('dashboard')
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
          <p className="text-gray-600">Loading your learning journey...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <StudentNavigation
        currentView={currentView}
        onViewChange={setCurrentView}
        studentProfile={studentProfile}
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
            studentId={auth.studentId}
            selectedSkill={selectedSkill}
            onComplete={handleQuizComplete}
            onExit={() => setCurrentView('dashboard')}
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