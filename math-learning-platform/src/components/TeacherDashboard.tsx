'use client'

import { useState } from 'react'
import { StudentProfile, SkillProgress, SkillId } from '@/types/learning'
import {
  AcademicCapIcon,
  ChartBarIcon,
  UserGroupIcon,
  ClockIcon,
  TrophyIcon,
  FireIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline'

interface TeacherDashboardProps {
  students: StudentProfile[]
  classProgress: Record<string, SkillProgress[]>
}

export default function TeacherDashboard({ students, classProgress }: TeacherDashboardProps) {
  const [selectedStudent, setSelectedStudent] = useState<StudentProfile | null>(null)
  const [viewMode, setViewMode] = useState<'overview' | 'students' | 'skills'>('overview')

  // Calculate class-wide metrics
  const totalQuestions = students.reduce((sum, s) => sum + s.total_questions, 0)
  const totalCorrect = students.reduce((sum, s) => sum + s.total_correct, 0)
  const classAccuracy = totalQuestions > 0 ? (totalCorrect / totalQuestions) * 100 : 0
  const avgQuestionsPerStudent = students.length > 0 ? totalQuestions / students.length : 0
  const activeStudents = students.filter(s => {
    const lastLogin = new Date(s.last_login)
    const daysSince = (Date.now() - lastLogin.getTime()) / (1000 * 60 * 60 * 24)
    return daysSince < 7
  }).length

  // Identify struggling students (low accuracy or low engagement)
  const strugglingStudents = students.filter(s =>
    s.overall_accuracy < 50 || s.total_questions < 10
  )

  // Calculate skill mastery distribution across class
  const skillMasteryMap = new Map<SkillId, { total: number; proficient: number }>()
  Object.entries(classProgress).forEach(([_, skills]) => {
    skills.forEach(skill => {
      const current = skillMasteryMap.get(skill.skill_id) || { total: 0, proficient: 0 }
      current.total++
      if (['proficient', 'advanced', 'expert'].includes(skill.mastery_level)) {
        current.proficient++
      }
      skillMasteryMap.set(skill.skill_id, current)
    })
  })

  const skillNames: Record<SkillId, string> = {
    'quad.graph.vertex': 'Vertex from Graph',
    'quad.standard.vertex': 'Vertex from Standard Form',
    'quad.roots.factored': 'Roots from Factored Form',
    'quad.solve.by_factoring': 'Solve by Factoring',
    'quad.solve.by_formula': 'Quadratic Formula',
    'quad.discriminant.analysis': 'Discriminant Analysis',
    'quad.intercepts': 'Finding Intercepts',
    'quad.complete.square': 'Complete the Square',
    'quad.axis.symmetry': 'Axis of Symmetry'
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Teacher Dashboard</h1>
        <p className="text-gray-600">Monitor student progress and identify learning gaps</p>
      </div>

      {/* View Mode Tabs */}
      <div className="mb-8 border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {[
            { id: 'overview', label: 'Class Overview', icon: ChartBarIcon },
            { id: 'students', label: 'Students', icon: UserGroupIcon },
            { id: 'skills', label: 'Skills Analysis', icon: AcademicCapIcon }
          ].map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              onClick={() => setViewMode(id as any)}
              className={`flex items-center py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                viewMode === id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <Icon className="w-5 h-5 mr-2" />
              {label}
            </button>
          ))}
        </nav>
      </div>

      {/* Overview Tab */}
      {viewMode === 'overview' && (
        <>
          {/* Key Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
              <div className="flex items-center justify-between mb-4">
                <UserGroupIcon className="w-10 h-10 text-blue-500" />
                <span className="text-3xl font-bold text-gray-900">{students.length}</span>
              </div>
              <p className="text-gray-600 font-medium">Total Students</p>
              <p className="text-sm text-gray-500 mt-1">{activeStudents} active this week</p>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
              <div className="flex items-center justify-between mb-4">
                <CheckCircleIcon className="w-10 h-10 text-green-500" />
                <span className="text-3xl font-bold text-gray-900">{classAccuracy.toFixed(0)}%</span>
              </div>
              <p className="text-gray-600 font-medium">Class Accuracy</p>
              <p className="text-sm text-gray-500 mt-1">{totalCorrect}/{totalQuestions} correct</p>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
              <div className="flex items-center justify-between mb-4">
                <AcademicCapIcon className="w-10 h-10 text-purple-500" />
                <span className="text-3xl font-bold text-gray-900">{avgQuestionsPerStudent.toFixed(0)}</span>
              </div>
              <p className="text-gray-600 font-medium">Avg Questions/Student</p>
              <p className="text-sm text-gray-500 mt-1">Total: {totalQuestions}</p>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
              <div className="flex items-center justify-between mb-4">
                <ExclamationTriangleIcon className="w-10 h-10 text-orange-500" />
                <span className="text-3xl font-bold text-gray-900">{strugglingStudents.length}</span>
              </div>
              <p className="text-gray-600 font-medium">Need Attention</p>
              <p className="text-sm text-gray-500 mt-1">Low performance</p>
            </div>
          </div>

          {/* Struggling Students Alert */}
          {strugglingStudents.length > 0 && (
            <div className="bg-orange-50 border border-orange-200 rounded-xl p-6 mb-8">
              <div className="flex items-start">
                <ExclamationTriangleIcon className="w-6 h-6 text-orange-600 mr-3 flex-shrink-0 mt-1" />
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-orange-900 mb-2">
                    Students Needing Support
                  </h3>
                  <p className="text-orange-800 text-sm mb-4">
                    The following students have low accuracy (&lt;50%) or minimal engagement (&lt;10 questions):
                  </p>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                    {strugglingStudents.map(student => (
                      <div key={student.id} className="bg-white rounded-lg p-3 border border-orange-200">
                        <p className="font-medium text-gray-900">{student.name}</p>
                        <p className="text-sm text-gray-600">
                          {student.overall_accuracy.toFixed(0)}% accuracy • {student.total_questions} questions
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Top Performers */}
          <div className="bg-white rounded-xl shadow-sm p-6 mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
              <TrophyIcon className="w-6 h-6 mr-2 text-yellow-500" />
              Top Performers
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {students
                .sort((a, b) => b.skills_mastered - a.skills_mastered || b.total_questions - a.total_questions)
                .slice(0, 3)
                .map((student, index) => (
                  <div key={student.id} className="bg-gradient-to-br from-yellow-50 to-orange-50 rounded-lg p-4 border border-yellow-200">
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-2xl font-bold text-yellow-600">#{index + 1}</span>
                      <TrophyIcon className="w-8 h-8 text-yellow-500" />
                    </div>
                    <p className="font-semibold text-gray-900 mb-1">{student.name}</p>
                    <div className="space-y-1 text-sm text-gray-600">
                      <p>{student.skills_mastered} skills mastered</p>
                      <p>{student.total_questions} questions completed</p>
                      <p>{student.overall_accuracy.toFixed(0)}% accuracy</p>
                    </div>
                  </div>
                ))}
            </div>
          </div>
        </>
      )}

      {/* Students Tab */}
      {viewMode === 'students' && (
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">All Students</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead>
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Student
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Questions
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Accuracy
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Skills Mastered
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Streak
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Last Active
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {students
                  .sort((a, b) => b.total_questions - a.total_questions)
                  .map(student => {
                    const lastLogin = new Date(student.last_login)
                    const daysSince = Math.floor((Date.now() - lastLogin.getTime()) / (1000 * 60 * 60 * 24))
                    const isRecent = daysSince < 7

                    return (
                      <tr key={student.id} className="hover:bg-gray-50 cursor-pointer" onClick={() => setSelectedStudent(student)}>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <div className="flex-shrink-0 h-10 w-10">
                              <div className="h-10 w-10 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white font-semibold">
                                {student.name.split(' ').map(n => n[0]).join('')}
                              </div>
                            </div>
                            <div className="ml-4">
                              <div className="text-sm font-medium text-gray-900">{student.name}</div>
                              <div className="text-sm text-gray-500">{student.grade_level || '9th Grade'}</div>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {student.total_questions}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                            student.overall_accuracy >= 70 ? 'bg-green-100 text-green-800' :
                            student.overall_accuracy >= 50 ? 'bg-yellow-100 text-yellow-800' :
                            'bg-red-100 text-red-800'
                          }`}>
                            {student.overall_accuracy.toFixed(0)}%
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {student.skills_mastered}/9
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center text-sm text-gray-900">
                            <FireIcon className="w-4 h-4 mr-1 text-orange-500" />
                            {student.current_streak}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`text-sm ${isRecent ? 'text-green-600 font-medium' : 'text-gray-500'}`}>
                            {daysSince === 0 ? 'Today' : daysSince === 1 ? 'Yesterday' : `${daysSince}d ago`}
                          </span>
                        </td>
                      </tr>
                    )
                  })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Skills Analysis Tab */}
      {viewMode === 'skills' && (
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Class-Wide Skill Mastery</h2>
          <div className="space-y-6">
            {Array.from(skillMasteryMap.entries())
              .sort((a, b) => (a[1].proficient / a[1].total) - (b[1].proficient / b[1].total))
              .map(([skillId, data]) => {
                const proficiencyRate = (data.proficient / data.total) * 100
                const isStruggling = proficiencyRate < 50

                return (
                  <div key={skillId} className={`p-4 rounded-lg border-2 ${
                    isStruggling ? 'bg-red-50 border-red-200' : 'bg-gray-50 border-gray-200'
                  }`}>
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex-1">
                        <h3 className="font-semibold text-gray-900">{skillNames[skillId]}</h3>
                        <p className="text-sm text-gray-600 mt-1">
                          {data.proficient} of {data.total} students proficient or higher
                        </p>
                      </div>
                      <div className="text-right">
                        <div className={`text-2xl font-bold ${
                          isStruggling ? 'text-red-600' : proficiencyRate >= 70 ? 'text-green-600' : 'text-yellow-600'
                        }`}>
                          {proficiencyRate.toFixed(0)}%
                        </div>
                        {isStruggling && (
                          <span className="text-xs text-red-600 font-medium">Needs attention</span>
                        )}
                      </div>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                      <div
                        className={`h-3 rounded-full transition-all duration-500 ${
                          isStruggling ? 'bg-red-500' : proficiencyRate >= 70 ? 'bg-green-500' : 'bg-yellow-500'
                        }`}
                        style={{ width: `${proficiencyRate}%` }}
                      />
                    </div>
                  </div>
                )
              })}
          </div>
        </div>
      )}

      {/* Student Detail Modal */}
      {selectedStudent && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50" onClick={() => setSelectedStudent(null)}>
          <div className="bg-white rounded-xl shadow-xl max-w-2xl w-full p-8" onClick={e => e.stopPropagation()}>
            <div className="flex items-start justify-between mb-6">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">{selectedStudent.name}</h2>
                <p className="text-gray-600">{selectedStudent.grade_level || '9th Grade'}</p>
              </div>
              <button
                onClick={() => setSelectedStudent(null)}
                className="text-gray-400 hover:text-gray-600 text-2xl font-bold"
              >
                ×
              </button>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">{selectedStudent.total_questions}</div>
                <div className="text-sm text-gray-600">Questions</div>
              </div>
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <div className="text-2xl font-bold text-green-600">{selectedStudent.overall_accuracy.toFixed(0)}%</div>
                <div className="text-sm text-gray-600">Accuracy</div>
              </div>
              <div className="text-center p-4 bg-purple-50 rounded-lg">
                <div className="text-2xl font-bold text-purple-600">{selectedStudent.skills_mastered}</div>
                <div className="text-sm text-gray-600">Skills</div>
              </div>
              <div className="text-center p-4 bg-orange-50 rounded-lg">
                <div className="text-2xl font-bold text-orange-600">{selectedStudent.current_streak}</div>
                <div className="text-sm text-gray-600">Streak</div>
              </div>
            </div>

            {classProgress[selectedStudent.id] && (
              <div>
                <h3 className="font-semibold text-gray-900 mb-4">Skill Progress</h3>
                <div className="space-y-3 max-h-80 overflow-y-auto">
                  {classProgress[selectedStudent.id].map(skill => (
                    <div key={skill.skill_id} className="p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-medium text-gray-900 text-sm">
                          {skillNames[skill.skill_id]}
                        </span>
                        <span className="text-xs px-2 py-1 rounded-full bg-blue-100 text-blue-800 font-medium capitalize">
                          {skill.mastery_level}
                        </span>
                      </div>
                      <div className="flex items-center justify-between text-xs text-gray-600">
                        <span>{skill.questions_correct}/{skill.questions_attempted} correct</span>
                        <span>{skill.progress_percentage}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <button
              onClick={() => setSelectedStudent(null)}
              className="w-full mt-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
