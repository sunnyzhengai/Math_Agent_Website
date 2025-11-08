'use client'

import { useState, useEffect } from 'react'
import { StudentProfile, SkillProgress, SkillId } from '@/types/learning'
import { learningApi } from '@/lib/learning-api'
import StudentDashboard from '@/components/StudentDashboard'
import SkillExplorer from '@/components/SkillExplorer'
import QuizInterface from '@/components/QuizInterface'
import StudentNavigation from '@/components/StudentNavigation'

type ViewMode = 'dashboard' | 'skills' | 'quiz' | 'progress'

export default function HomePage() {
  const [currentView, setCurrentView] = useState<ViewMode>('dashboard')
  const [studentProfile, setStudentProfile] = useState<StudentProfile | null>(null)
  const [skillProgress, setSkillProgress] = useState<SkillProgress[]>([])
  const [selectedSkill, setSelectedSkill] = useState<SkillId | null>(null)
  const [loading, setLoading] = useState(true)

  // Mock student ID - in real app would come from auth
  const studentId = 'student_001'

  useEffect(() => {
    loadStudentData()
  }, [])

  const loadStudentData = async () => {
    try {
      setLoading(true)
      const [profile, progress] = await Promise.all([
        learningApi.getStudentProfile(studentId),
        learningApi.getSkillProgress(studentId)
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
            studentId={studentId}
            selectedSkill={selectedSkill}
            onComplete={handleQuizComplete}
            onExit={() => setCurrentView('dashboard')}
          />
        )}
        
        {currentView === 'progress' && (
          <div className="container mx-auto px-4 py-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-8">Your Progress</h1>
            <div className="bg-white rounded-xl p-6 shadow-sm">
              <p className="text-gray-600">Detailed progress analytics coming soon...</p>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}