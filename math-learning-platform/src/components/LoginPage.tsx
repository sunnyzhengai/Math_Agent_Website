'use client'

import { useState } from 'react'
import { BookOpenIcon, ChartBarIcon, AcademicCapIcon } from '@heroicons/react/24/outline'

interface LoginPageProps {
  onLogin: (userId: string, userName: string, role: 'student' | 'teacher') => void
}

export default function LoginPage({ onLogin }: LoginPageProps) {
  const [userName, setUserName] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [loginMode, setLoginMode] = useState<'student' | 'teacher'>('student')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!userName.trim()) return

    setIsLoading(true)

    // Clear any existing session first
    localStorage.removeItem('quadratic_mastery_auth')

    // Simulate a brief loading state for better UX
    setTimeout(() => {
      // Generate ID from name (in production, this would be handled by backend)
      const userId = `${loginMode}_${userName.toLowerCase().replace(/\s+/g, '_')}`
      onLogin(userId, userName.trim(), loginMode)
      setIsLoading(false)
    }, 500)
  }

  const handleDemoLogin = () => {
    if (loginMode === 'student') {
      onLogin('student_001', 'Julia Student', 'student')
    } else {
      onLogin('teacher_001', 'Ms. Rodriguez', 'teacher')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        {/* Logo and Title */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl mb-4">
            <AcademicCapIcon className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Quadratic Mastery</h1>
          <p className="text-lg text-gray-600">Master quadratics through adaptive practice</p>
        </div>

        {/* Login Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-6">
          {/* Role Selection */}
          <div className="flex mb-6 bg-gray-100 p-1 rounded-lg">
            <button
              onClick={() => setLoginMode('student')}
              className={`flex-1 py-2 px-4 rounded-md font-medium transition-colors ${
                loginMode === 'student'
                  ? 'bg-white text-blue-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Student
            </button>
            <button
              onClick={() => setLoginMode('teacher')}
              className={`flex-1 py-2 px-4 rounded-md font-medium transition-colors ${
                loginMode === 'teacher'
                  ? 'bg-white text-purple-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Teacher
            </button>
          </div>

          <h2 className="text-2xl font-semibold text-gray-900 mb-2">
            {loginMode === 'student' ? 'Welcome!' : 'Teacher Login'}
          </h2>
          <p className="text-gray-600 mb-6">
            {loginMode === 'student' ? 'Enter your name to start learning (new users automatically created)' : 'Access your teacher dashboard'}
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="userName" className="block text-sm font-medium text-gray-700 mb-2">
                Your Name
              </label>
              <input
                type="text"
                id="userName"
                value={userName}
                onChange={(e) => setUserName(e.target.value)}
                placeholder="Enter your name"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                autoFocus
              />
            </div>

            <button
              type="submit"
              disabled={!userName.trim() || isLoading}
              className={`w-full py-3 rounded-lg font-semibold transition-all ${
                userName.trim() && !isLoading
                  ? `bg-gradient-to-r ${
                      loginMode === 'student'
                        ? 'from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700'
                        : 'from-purple-500 to-pink-600 hover:from-purple-600 hover:to-pink-700'
                    } text-white shadow-lg hover:shadow-xl`
                  : 'bg-gray-100 text-gray-400 cursor-not-allowed'
              }`}
            >
              {isLoading ? (
                <div className="flex items-center justify-center space-x-2">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  <span>Logging in...</span>
                </div>
              ) : (
                loginMode === 'student' ? 'Start Learning' : 'Access Dashboard'
              )}
            </button>
          </form>

          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-200"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-4 bg-white text-gray-500">or</span>
            </div>
          </div>

          <button
            onClick={handleDemoLogin}
            className="w-full py-3 border-2 border-gray-200 rounded-lg font-semibold text-gray-700 hover:border-blue-500 hover:text-blue-600 hover:bg-blue-50 transition-all"
          >
            Continue as Demo User
          </button>
        </div>

        {/* Features */}
        <div className="grid grid-cols-3 gap-4 text-center">
          <div className="bg-white/80 backdrop-blur rounded-lg p-4">
            <BookOpenIcon className="w-8 h-8 text-blue-500 mx-auto mb-2" />
            <p className="text-sm font-medium text-gray-700">9 Skills</p>
          </div>
          <div className="bg-white/80 backdrop-blur rounded-lg p-4">
            <ChartBarIcon className="w-8 h-8 text-purple-500 mx-auto mb-2" />
            <p className="text-sm font-medium text-gray-700">Track Progress</p>
          </div>
          <div className="bg-white/80 backdrop-blur rounded-lg p-4">
            <AcademicCapIcon className="w-8 h-8 text-pink-500 mx-auto mb-2" />
            <p className="text-sm font-medium text-gray-700">Adaptive</p>
          </div>
        </div>

        {/* Footer */}
        <p className="text-center text-sm text-gray-500 mt-8">
          Practice makes perfect. Start your journey today!
        </p>
      </div>
    </div>
  )
}
