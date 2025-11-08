'use client'

import { StudentProfile, SkillProgress, SkillId } from '@/types/learning'
import { 
  TrophyIcon,
  ClockIcon,
  CheckCircleIcon,
  FireIcon,
  StarIcon,
  PlayIcon
} from '@heroicons/react/24/outline'

interface StudentDashboardProps {
  studentProfile: StudentProfile | null
  skillProgress: SkillProgress[]
  onStartQuiz: (skillId?: SkillId) => void
}

export default function StudentDashboard({ 
  studentProfile, 
  skillProgress, 
  onStartQuiz 
}: StudentDashboardProps) {
  if (!studentProfile) {
    return <div>Loading...</div>
  }

  const formatTime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    return hours > 0 ? `${hours}h ${minutes}m` : `${minutes}m`
  }

  const getMasteryColor = (level: string) => {
    const colors = {
      beginner: 'text-gray-600 bg-gray-100',
      developing: 'text-yellow-700 bg-yellow-100',
      proficient: 'text-blue-700 bg-blue-100',
      advanced: 'text-green-700 bg-green-100',
      expert: 'text-purple-700 bg-purple-100'
    }
    return colors[level as keyof typeof colors] || colors.beginner
  }

  const recentSkills = skillProgress
    .sort((a, b) => new Date(b.last_activity).getTime() - new Date(a.last_activity).getTime())
    .slice(0, 3)

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl">
      {/* Welcome header */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-3">
          Welcome back, {studentProfile.name}!
        </h1>
        <p className="text-lg text-gray-600">
          Ready to continue your math journey?
        </p>
      </div>

      {/* Quick stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-12">
        <div className="stat-card text-center">
          <div className="flex justify-center mb-3">
            <CheckCircleIcon className="icon-lg text-green-500" />
          </div>
          <div className="text-3xl font-bold text-gray-900 mb-1">{studentProfile.total_correct}</div>
          <div className="text-sm font-medium text-gray-600">Questions Solved</div>
        </div>

        <div className="stat-card text-center">
          <div className="flex justify-center mb-3">
            <TrophyIcon className="icon-lg text-yellow-500" />
          </div>
          <div className="text-3xl font-bold text-gray-900 mb-1">{studentProfile.skills_mastered}</div>
          <div className="text-sm font-medium text-gray-600">Skills Mastered</div>
        </div>

        <div className="stat-card text-center">
          <div className="flex justify-center mb-3">
            <FireIcon className="icon-lg text-orange-500" />
          </div>
          <div className="text-3xl font-bold text-gray-900 mb-1">{studentProfile.current_streak}</div>
          <div className="text-sm font-medium text-gray-600">Current Streak</div>
        </div>

        <div className="stat-card text-center">
          <div className="flex justify-center mb-3">
            <ClockIcon className="icon-lg text-blue-500" />
          </div>
          <div className="text-3xl font-bold text-gray-900 mb-1">
            {formatTime(studentProfile.total_time_spent)}
          </div>
          <div className="text-sm font-medium text-gray-600">Time Spent</div>
        </div>
      </div>

      {/* Quick start section */}
      <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl text-white p-8 text-center mb-12 shadow-lg">
        <h2 className="text-2xl font-bold mb-3">Continue Learning</h2>
        <p className="text-blue-100 mb-6">
          Let our adaptive system pick the best question for you
        </p>
        <button
          onClick={() => onStartQuiz()}
          className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors duration-200 inline-flex items-center space-x-2 shadow-md"
        >
          <PlayIcon className="icon-md" />
          <span>Start Adaptive Quiz</span>
        </button>
      </div>

      {/* Recent progress */}
      <div className="mb-12">
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-2xl font-bold text-gray-900">Recent Progress</h2>
          <button
            onClick={() => {/* Navigate to skills view */}}
            className="text-blue-600 hover:text-blue-700 font-medium"
          >
            View All Skills →
          </button>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {recentSkills.map((skill) => (
            <div key={skill.skill_id} className="skill-card">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold text-gray-900 capitalize">
                  {skill.skill_id.replace(/\./g, ' ').replace('quad ', '')}
                </h3>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getMasteryColor(skill.mastery_level)}`}>
                  {skill.mastery_level}
                </span>
              </div>

              <div className="mb-4">
                <div className="flex justify-between text-sm text-gray-600 mb-1">
                  <span>Progress</span>
                  <span>{skill.progress_percentage}%</span>
                </div>
                <div className="progress-bar">
                  <div 
                    className="progress-fill" 
                    style={{ width: `${skill.progress_percentage}%` }}
                  />
                </div>
              </div>

              <div className="flex justify-between text-sm text-gray-600 mb-4">
                <span>{skill.questions_correct}/{skill.questions_attempted} correct</span>
                <span>Streak: {skill.current_streak}</span>
              </div>

              <button
                onClick={() => onStartQuiz(skill.skill_id)}
                className="w-full btn-primary text-sm py-2"
              >
                Practice This Skill
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Achievements */}
      {studentProfile.badges_earned.length > 0 && (
        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-8">Recent Achievements</h2>
          <div className="flex flex-wrap gap-4">
            {studentProfile.badges_earned.slice(0, 5).map((badge, index) => (
              <div key={index} className="flex items-center space-x-2 bg-yellow-50 text-yellow-800 px-5 py-3 rounded-full border border-yellow-200 shadow-sm hover:shadow-md transition-shadow">
                <StarIcon className="w-5 h-5" />
                <span className="text-sm font-semibold capitalize">
                  {badge.replace(/_/g, ' ')}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}