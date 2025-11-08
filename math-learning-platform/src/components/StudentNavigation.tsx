'use client'

import { StudentProfile } from '@/types/learning'
import { 
  HomeIcon, 
  BookOpenIcon, 
  ChartBarIcon,
  UserCircleIcon,
  FireIcon 
} from '@heroicons/react/24/outline'

type ViewMode = 'dashboard' | 'skills' | 'quiz' | 'progress'

interface StudentNavigationProps {
  currentView: ViewMode
  onViewChange: (view: ViewMode) => void
  studentProfile: StudentProfile | null
  onLogout?: () => void
}

export default function StudentNavigation({
  currentView,
  onViewChange,
  studentProfile,
  onLogout
}: StudentNavigationProps) {
  const navItems = [
    { id: 'dashboard' as ViewMode, label: 'Dashboard', icon: HomeIcon },
    { id: 'skills' as ViewMode, label: 'Skills', icon: BookOpenIcon },
    { id: 'progress' as ViewMode, label: 'Progress', icon: ChartBarIcon },
  ]

  return (
    <nav className="fixed top-0 left-0 right-0 bg-white border-b border-gray-200 shadow-sm z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo and title */}
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">Q</span>
            </div>
            <h1 className="text-xl font-bold text-gray-900">Quadratic Mastery</h1>
          </div>

          {/* Navigation links */}
          <div className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon
              return (
                <button
                  key={item.id}
                  onClick={() => onViewChange(item.id)}
                  className={`
                    px-4 py-2 rounded-lg flex items-center space-x-2 transition-all duration-200
                    ${currentView === item.id 
                      ? 'bg-blue-50 text-blue-700 font-medium' 
                      : 'text-gray-600 hover:text-blue-600 hover:bg-gray-50'
                    }
                  `}
                >
                  <Icon className="icon-md" />
                  <span>{item.label}</span>
                </button>
              )
            })}
          </div>

          {/* Student info */}
          <div className="flex items-center space-x-4">
            {studentProfile && (
              <>
                {/* Streak indicator */}
                <div className="hidden sm:flex items-center space-x-1 bg-orange-50 text-orange-700 px-3 py-1 rounded-full">
                  <FireIcon className="icon-sm" />
                  <span className="text-sm font-medium">{studentProfile.current_streak}</span>
                </div>

                {/* Accuracy */}
                <div className="hidden sm:flex items-center space-x-1 bg-green-50 text-green-700 px-3 py-1 rounded-full">
                  <span className="text-sm font-medium">
                    {Math.round(studentProfile.overall_accuracy)}%
                  </span>
                </div>

                {/* Student avatar */}
                <div className="flex items-center space-x-2">
                  <UserCircleIcon className="icon-lg text-gray-400" />
                  <span className="hidden sm:block text-sm font-medium text-gray-700">
                    {studentProfile.name}
                  </span>
                </div>
              </>
            )}

            {/* Logout button */}
            {onLogout && (
              <button
                onClick={onLogout}
                className="text-sm text-gray-600 hover:text-gray-900 font-medium transition-colors"
              >
                Logout
              </button>
            )}
          </div>
        </div>

        {/* Mobile navigation */}
        <div className="md:hidden flex space-x-1 pb-2">
          {navItems.map((item) => {
            const Icon = item.icon
            return (
              <button
                key={item.id}
                onClick={() => onViewChange(item.id)}
                className={`
                  flex-1 px-3 py-2 rounded-lg flex flex-col items-center space-y-1 transition-all duration-200
                  ${currentView === item.id 
                    ? 'bg-blue-50 text-blue-700 font-medium' 
                    : 'text-gray-600 hover:text-blue-600 hover:bg-gray-50'
                  }
                `}
              >
                <Icon className="icon-md" />
                <span className="text-xs">{item.label}</span>
              </button>
            )
          })}
        </div>
      </div>
    </nav>
  )
}