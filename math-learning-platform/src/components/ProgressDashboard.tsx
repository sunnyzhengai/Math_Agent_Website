'use client'

import { StudentProfile, SkillProgress } from '@/types/learning'
import {
  ChartBarIcon,
  ClockIcon,
  FireIcon,
  TrophyIcon,
  AcademicCapIcon,
  CheckCircleIcon,
  ArrowTrendingUpIcon
} from '@heroicons/react/24/outline'

interface ProgressDashboardProps {
  studentProfile: StudentProfile | null
  skillProgress: SkillProgress[]
}

export default function ProgressDashboard({ studentProfile, skillProgress }: ProgressDashboardProps) {
  if (!studentProfile) {
    return (
      <div className="container mx-auto px-4 py-8">
        <p className="text-gray-600">Loading progress data...</p>
      </div>
    )
  }

  // Calculate skill mastery distribution
  const masteryDistribution = skillProgress.reduce((acc, skill) => {
    const level = skill.mastery_level || 'beginner'
    acc[level] = (acc[level] || 0) + 1
    return acc
  }, {} as Record<string, number>)

  // Calculate average accuracy per difficulty
  const totalAttempted = skillProgress.reduce((sum, skill) => sum + skill.questions_attempted, 0)
  const totalCorrect = skillProgress.reduce((sum, skill) => sum + skill.questions_correct, 0)
  const overallAccuracy = totalAttempted > 0 ? (totalCorrect / totalAttempted) * 100 : 0

  // Sort skills by progress
  const sortedSkills = [...skillProgress].sort((a, b) => b.progress_percentage - a.progress_percentage)

  // Calculate total time in hours
  const totalTimeHours = (studentProfile.total_time_spent / 3600).toFixed(1)

  const getMasteryColor = (level: string) => {
    const colors = {
      beginner: 'bg-gray-100 text-gray-700',
      developing: 'bg-yellow-100 text-yellow-800',
      proficient: 'bg-blue-100 text-blue-800',
      advanced: 'bg-green-100 text-green-800',
      expert: 'bg-purple-100 text-purple-800'
    }
    return colors[level as keyof typeof colors] || colors.beginner
  }

  const getMasteryLabel = (level: string) => {
    return level.charAt(0).toUpperCase() + level.slice(1)
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Your Progress</h1>
        <p className="text-gray-600">Track your learning journey and celebrate your achievements</p>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <AcademicCapIcon className="w-10 h-10 opacity-80" />
            <span className="text-3xl font-bold">{studentProfile.total_questions}</span>
          </div>
          <p className="text-blue-100">Questions Solved</p>
          <p className="text-xs text-blue-200 mt-1">{studentProfile.total_correct} correct</p>
        </div>

        <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-xl p-6 text-white shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <CheckCircleIcon className="w-10 h-10 opacity-80" />
            <span className="text-3xl font-bold">{overallAccuracy.toFixed(0)}%</span>
          </div>
          <p className="text-green-100">Overall Accuracy</p>
          <p className="text-xs text-green-200 mt-1">Across all skills</p>
        </div>

        <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl p-6 text-white shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <FireIcon className="w-10 h-10 opacity-80" />
            <span className="text-3xl font-bold">{studentProfile.current_streak}</span>
          </div>
          <p className="text-orange-100">Current Streak</p>
          <p className="text-xs text-orange-200 mt-1">Best: {studentProfile.best_streak} days</p>
        </div>

        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl p-6 text-white shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <ClockIcon className="w-10 h-10 opacity-80" />
            <span className="text-3xl font-bold">{totalTimeHours}h</span>
          </div>
          <p className="text-purple-100">Study Time</p>
          <p className="text-xs text-purple-200 mt-1">Total practice time</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Skill Progress List */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
              <ChartBarIcon className="w-6 h-6 mr-2 text-blue-500" />
              Skill Progress
            </h2>

            <div className="space-y-4">
              {sortedSkills.map((skill) => {
                const accuracy = skill.questions_attempted > 0
                  ? (skill.questions_correct / skill.questions_attempted) * 100
                  : 0

                return (
                  <div key={skill.skill_id} className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex-1">
                        <h3 className="font-semibold text-gray-900 mb-1">
                          {skill.skill_id.replace(/\./g, ' ').replace('quad ', '').replace(/\b\w/g, l => l.toUpperCase())}
                        </h3>
                        <div className="flex items-center space-x-3 text-sm text-gray-600">
                          <span>{skill.questions_attempted} questions</span>
                          <span>•</span>
                          <span>{accuracy.toFixed(0)}% accuracy</span>
                          <span>•</span>
                          <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${getMasteryColor(skill.mastery_level)}`}>
                            {getMasteryLabel(skill.mastery_level)}
                          </span>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-blue-600">{skill.progress_percentage}%</div>
                      </div>
                    </div>

                    {/* Progress Bar */}
                    <div className="w-full bg-gray-100 rounded-full h-2.5 overflow-hidden">
                      <div
                        className="bg-gradient-to-r from-blue-500 to-purple-600 h-2.5 rounded-full transition-all duration-500"
                        style={{ width: `${skill.progress_percentage}%` }}
                      />
                    </div>

                    {/* Additional Stats */}
                    <div className="mt-3 grid grid-cols-3 gap-4 text-sm">
                      <div>
                        <span className="text-gray-500">Correct:</span>
                        <span className="ml-2 font-semibold text-gray-900">{skill.questions_correct}/{skill.questions_attempted}</span>
                      </div>
                      <div>
                        <span className="text-gray-500">Streak:</span>
                        <span className="ml-2 font-semibold text-gray-900">{skill.current_streak} (best: {skill.best_streak})</span>
                      </div>
                      <div>
                        <span className="text-gray-500">Time:</span>
                        <span className="ml-2 font-semibold text-gray-900">{Math.round(skill.total_time_spent / 60)}min</span>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </div>

        {/* Mastery Distribution & Achievements */}
        <div className="space-y-6">
          {/* Mastery Distribution */}
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
              <TrophyIcon className="w-6 h-6 mr-2 text-yellow-500" />
              Mastery Levels
            </h2>

            <div className="space-y-3">
              {['expert', 'advanced', 'proficient', 'developing', 'beginner'].map(level => {
                const count = masteryDistribution[level] || 0
                const total = skillProgress.length
                const percentage = total > 0 ? (count / total) * 100 : 0

                return (
                  <div key={level}>
                    <div className="flex items-center justify-between mb-2">
                      <span className={`text-sm font-medium px-2 py-1 rounded ${getMasteryColor(level)}`}>
                        {getMasteryLabel(level)}
                      </span>
                      <span className="text-sm font-semibold text-gray-900">{count} skills</span>
                    </div>
                    <div className="w-full bg-gray-100 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${getMasteryColor(level).replace('bg-', 'bg-').replace('100', '500')}`}
                        style={{ width: `${percentage}%` }}
                      />
                    </div>
                  </div>
                )
              })}
            </div>
          </div>

          {/* Achievements */}
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
              <ArrowTrendingUpIcon className="w-6 h-6 mr-2 text-green-500" />
              Achievements
            </h2>

            <div className="space-y-3">
              {studentProfile.badges_earned?.map(badge => (
                <div key={badge} className="flex items-center space-x-3 p-3 bg-gradient-to-r from-yellow-50 to-orange-50 rounded-lg border border-yellow-200">
                  <TrophyIcon className="w-6 h-6 text-yellow-600 flex-shrink-0" />
                  <span className="text-sm font-medium text-gray-900">
                    {badge.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  </span>
                </div>
              ))}

              {(!studentProfile.badges_earned || studentProfile.badges_earned.length === 0) && (
                <p className="text-sm text-gray-500 text-center py-4">
                  Keep practicing to earn badges!
                </p>
              )}
            </div>
          </div>

          {/* Quick Stats */}
          <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl p-6 border border-blue-200">
            <h3 className="font-semibold text-gray-900 mb-4">Quick Stats</h3>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Skills Mastered:</span>
                <span className="font-semibold text-gray-900">{studentProfile.skills_mastered}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Grade Level:</span>
                <span className="font-semibold text-gray-900">{studentProfile.grade_level}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Member Since:</span>
                <span className="font-semibold text-gray-900">
                  {new Date(studentProfile.created_at).toLocaleDateString('en-US', { month: 'short', year: 'numeric' })}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
