'use client'

import { SkillProgress, SkillId } from '@/types/learning'
import { 
  LockClosedIcon,
  PlayIcon,
  TrophyIcon,
  ChartBarIcon,
  ClockIcon
} from '@heroicons/react/24/outline'

interface SkillExplorerProps {
  skillProgress: SkillProgress[]
  onStartQuiz: (skillId: SkillId) => void
}

interface SkillDefinition {
  name: string
  description: string
  prerequisites: string[]
  estimated_time: number
}

const skillDefinitions: Record<SkillId, SkillDefinition> = {
  'quad.graph.vertex': {
    name: 'Vertex from Graph',
    description: 'Find the vertex of a parabola from its graph',
    prerequisites: [],
    estimated_time: 15
  },
  'quad.standard.vertex': {
    name: 'Vertex from Standard Form',
    description: 'Find the vertex from standard form ax² + bx + c',
    prerequisites: ['quad.graph.vertex'],
    estimated_time: 20
  },
  'quad.roots.factored': {
    name: 'Roots from Factored Form',
    description: 'Find roots when quadratic is in factored form',
    prerequisites: [],
    estimated_time: 18
  },
  'quad.solve.by_factoring': {
    name: 'Solve by Factoring',
    description: 'Factor quadratics and solve for roots',
    prerequisites: ['quad.roots.factored'],
    estimated_time: 25
  },
  'quad.solve.by_formula': {
    name: 'Quadratic Formula',
    description: 'Use the quadratic formula to solve equations',
    prerequisites: ['quad.discriminant.analysis'],
    estimated_time: 30
  },
  'quad.discriminant.analysis': {
    name: 'Discriminant Analysis',
    description: 'Analyze the nature of roots using discriminant',
    prerequisites: ['quad.standard.vertex'],
    estimated_time: 22
  },
  'quad.intercepts': {
    name: 'Finding Intercepts',
    description: 'Find x and y intercepts of quadratic functions',
    prerequisites: ['quad.graph.vertex'],
    estimated_time: 20
  },
  'quad.complete.square': {
    name: 'Complete the Square',
    description: 'Convert to vertex form by completing the square',
    prerequisites: ['quad.standard.vertex'],
    estimated_time: 28
  },
  'quad.axis.symmetry': {
    name: 'Axis of Symmetry',
    description: 'Find the axis of symmetry of parabolas',
    prerequisites: ['quad.graph.vertex'],
    estimated_time: 15
  },
  // Julia's Current Curriculum (Immediate Priority)
  'quad.complete.square.solve': {
    name: 'Solving by Completing the Square',
    description: 'Solve quadratic equations by completing the square method',
    prerequisites: ['quad.complete.square'],
    estimated_time: 30
  },
  'quad.solve.square_root_property': {
    name: 'Square Root Property',
    description: 'Solve equations like (x-h)² = k using square roots',
    prerequisites: [],
    estimated_time: 20
  },
  'quad.factoring.review': {
    name: 'Factoring Quadratics',
    description: 'Factor trinomials, difference of squares, and GCF',
    prerequisites: [],
    estimated_time: 25
  },
  'quad.solve.factoring': {
    name: 'Solving by Factoring',
    description: 'Solve equations by factoring and zero product property',
    prerequisites: ['quad.factoring.review'],
    estimated_time: 25
  },
  'quad.solutions.graphical': {
    name: 'Number of Solutions from Graph',
    description: 'Determine 0, 1, or 2 real solutions from parabola graphs',
    prerequisites: [],
    estimated_time: 15
  },
  // Phase 1: New Algebra 1 Skills (PAUSED - not yet implemented in backend)
  'quad.transformations': {
    name: 'Quadratic Transformations',
    description: 'Identify shifts, stretches, and reflections of parabolas',
    prerequisites: ['quad.graph.vertex'],
    estimated_time: 25
  },
  'quad.form.conversions': {
    name: 'Converting Quadratic Forms',
    description: 'Convert between standard, vertex, and factored forms',
    prerequisites: ['quad.complete.square', 'quad.solve.by_factoring'],
    estimated_time: 30
  },
  'quad.solve.inequalities': {
    name: 'Quadratic Inequalities',
    description: 'Solve inequalities and express solutions in interval notation',
    prerequisites: ['quad.solve.by_factoring', 'quad.roots.factored'],
    estimated_time: 28
  },
  'quad.applications.maxmin': {
    name: 'Optimization with Quadratics',
    description: 'Solve real-world max/min problems using quadratic functions',
    prerequisites: ['quad.graph.vertex', 'quad.standard.vertex'],
    estimated_time: 30
  },
  'quad.domain.range': {
    name: 'Domain and Range',
    description: 'Determine domain and range of quadratic functions',
    prerequisites: ['quad.graph.vertex'],
    estimated_time: 20
  },
  'quad.solutions.count': {
    name: 'Counting Solutions/Roots',
    description: 'Determine number of real solutions using discriminant',
    prerequisites: ['quad.discriminant.analysis'],
    estimated_time: 22
  }
}

export default function SkillExplorer({ skillProgress, onStartQuiz }: SkillExplorerProps) {
  const getMasteryColor = (level: string) => {
    const colors = {
      beginner: 'border-gray-300 bg-gray-50 text-gray-700',
      developing: 'border-yellow-300 bg-yellow-50 text-yellow-800',
      proficient: 'border-blue-300 bg-blue-50 text-blue-800',
      advanced: 'border-green-300 bg-green-50 text-green-800',
      expert: 'border-purple-300 bg-purple-50 text-purple-800'
    }
    return colors[level as keyof typeof colors] || colors.beginner
  }

  const getMasteryIcon = (level: string) => {
    switch (level) {
      case 'expert':
      case 'advanced':
        return <TrophyIcon className="icon-sm" />
      case 'proficient':
        return <ChartBarIcon className="icon-sm" />
      default:
        return <PlayIcon className="icon-sm" />
    }
  }

  const isSkillUnlocked = (skillId: SkillId) => {
    const skillDef = skillDefinitions[skillId]
    if (!skillDef.prerequisites.length) return true
    
    return skillDef.prerequisites.every(prereq => {
      const prereqProgress = skillProgress.find(p => p.skill_id === prereq)
      return prereqProgress && ['proficient', 'advanced', 'expert'].includes(prereqProgress.mastery_level)
    })
  }

  const formatTime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    return hours > 0 ? `${hours}h ${minutes}m` : `${minutes}m`
  }

  // Sort skills by prerequisite order (topological sort)
  const skillOrder: SkillId[] = [
    // Julia's Current Curriculum - Foundational
    'quad.factoring.review',         // JULIA: Foundational factoring (no prereqs)
    'quad.solve.square_root_property', // JULIA: Square root method (no prereqs)
    'quad.solutions.graphical',       // JULIA: Count solutions from graph (no prereqs)

    // Original foundational skills
    'quad.graph.vertex',      // Foundational: graphing
    'quad.roots.factored',     // Foundational: roots
    'quad.standard.vertex',    // Level 1: builds on graphing
    'quad.intercepts',         // Level 1: builds on graphing
    'quad.axis.symmetry',      // Level 1: builds on graphing
    'quad.solve.by_factoring', // Level 1: builds on roots

    // Julia's Current Curriculum - Intermediate
    'quad.solve.factoring',         // JULIA: Solving by factoring (needs factoring review)

    // Original intermediate skills
    'quad.discriminant.analysis', // Level 2: builds on standard form
    'quad.complete.square',    // Level 2: builds on standard form

    // Julia's Current Curriculum - Advanced
    'quad.complete.square.solve',   // JULIA: Solving by completing square (needs complete square)

    // Original advanced skills
    'quad.solve.by_formula',    // Level 3: builds on discriminant

    // Phase 1: New Algebra 1 Skills (PAUSED - will show as locked until backend templates added)
    'quad.transformations',        // Transformations: shifts, stretches, reflections
    'quad.domain.range',           // Domain and range analysis
    'quad.solutions.count',        // Number of solutions (discriminant)
    'quad.form.conversions',       // Converting between forms
    'quad.solve.inequalities',     // Quadratic inequalities
    'quad.applications.maxmin'     // Real-world optimization
  ]

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Quadratic Skills</h1>
        <p className="text-lg text-gray-600 mb-6">Master these skills to become a quadratic expert</p>

        {/* Adaptive Quiz Button */}
        <button
          onClick={() => onStartQuiz(undefined as any)}
          className="inline-flex items-center space-x-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-4 rounded-xl font-semibold hover:from-blue-600 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
        >
          <PlayIcon className="icon-md" />
          <span>Start Adaptive Quiz</span>
        </button>
        <p className="text-sm text-gray-500 mt-2">Practice across all unlocked skills with adaptive difficulty</p>
      </div>

      <div className="mt-12 mb-6">
        <h2 className="text-xl font-semibold text-gray-900">Practice Individual Skills</h2>
        <p className="text-gray-600">Or focus on specific skills below</p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {skillOrder.map(skillId => {
          const definition = skillDefinitions[skillId]
          const progress = skillProgress.find(p => p.skill_id === skillId)
          const isUnlocked = isSkillUnlocked(skillId)
          
          return (
            <div
              key={skillId}
              className={`skill-card ${!isUnlocked ? 'locked' : ''}`}
            >
              {/* Skill header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900 mb-1">
                    {definition.name}
                  </h3>
                  <p className="text-sm text-gray-600">
                    {definition.description}
                  </p>
                </div>
                {!isUnlocked && (
                  <LockClosedIcon className="icon-sm text-gray-400 flex-shrink-0 ml-2" />
                )}
              </div>

              {/* Prerequisites */}
              {definition.prerequisites.length > 0 && (
                <div className="mb-4">
                  <p className="text-xs text-gray-500 mb-1">Prerequisites:</p>
                  <div className="flex flex-wrap gap-1">
                    {definition.prerequisites.map(prereq => {
                      const prereqDef = skillDefinitions[prereq as SkillId]
                      const prereqProgress = skillProgress.find(p => p.skill_id === prereq)
                      const isPrereqMet = prereqProgress && ['proficient', 'advanced', 'expert'].includes(prereqProgress.mastery_level)
                      
                      return (
                        <span
                          key={prereq}
                          className={`px-2 py-1 rounded text-xs ${
                            isPrereqMet 
                              ? 'bg-green-100 text-green-700' 
                              : 'bg-gray-100 text-gray-600'
                          }`}
                        >
                          {prereqDef.name}
                        </span>
                      )
                    })}
                  </div>
                </div>
              )}

              {/* Progress section */}
              {progress && isUnlocked ? (
                <div className="mb-6 space-y-3">
                  {/* Mastery level */}
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Mastery Level</span>
                    <div className={`flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium border ${getMasteryColor(progress.mastery_level)}`}>
                      {getMasteryIcon(progress.mastery_level)}
                      <span className="capitalize">{progress.mastery_level}</span>
                    </div>
                  </div>

                  {/* Progress bar */}
                  <div>
                    <div className="flex justify-between text-sm text-gray-600 mb-1">
                      <span>Progress</span>
                      <span>{progress.progress_percentage}%</span>
                    </div>
                    <div className="progress-bar">
                      <div 
                        className="progress-fill" 
                        style={{ width: `${progress.progress_percentage}%` }}
                      />
                    </div>
                  </div>

                  {/* Stats */}
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-600">Accuracy</span>
                      <div className="font-semibold">
                        {progress.questions_attempted > 0 
                          ? Math.round((progress.questions_correct / progress.questions_attempted) * 100)
                          : 0}%
                      </div>
                    </div>
                    <div>
                      <span className="text-gray-600">Time Spent</span>
                      <div className="font-semibold">
                        {formatTime(progress.total_time_spent)}
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-600">Questions</span>
                      <div className="font-semibold">
                        {progress.questions_correct}/{progress.questions_attempted}
                      </div>
                    </div>
                    <div>
                      <span className="text-gray-600">Best Streak</span>
                      <div className="font-semibold">
                        {progress.best_streak}
                      </div>
                    </div>
                  </div>
                </div>
              ) : isUnlocked ? (
                <div className="mb-6 text-center py-4">
                  <PlayIcon className="icon-lg text-gray-400 mx-auto mb-2" />
                  <p className="text-sm text-gray-600">Start practicing to see your progress</p>
                </div>
              ) : (
                <div className="mb-6 text-center py-4">
                  <LockClosedIcon className="icon-lg text-gray-400 mx-auto mb-2" />
                  <p className="text-sm text-gray-600">Complete prerequisites to unlock</p>
                </div>
              )}

              {/* Estimated time */}
              <div className="flex items-center justify-center text-xs text-gray-500 mb-4">
                <ClockIcon className="icon-sm mr-1" />
                <span>~{definition.estimated_time} minutes</span>
              </div>

              {/* Action button */}
              <button
                onClick={() => onStartQuiz(skillId as SkillId)}
                disabled={!isUnlocked}
                className={`w-full py-3 rounded-lg font-semibold transition-colors duration-200 ${
                  isUnlocked
                    ? 'btn-primary'
                    : 'bg-gray-100 text-gray-400 cursor-not-allowed'
                }`}
              >
                {isUnlocked ? 'Practice Skill' : 'Locked'}
              </button>
            </div>
          )
        })}
      </div>

      {/* Learning path info */}
      <div className="mt-12 bg-blue-50 border border-blue-200 rounded-xl p-6">
        <h2 className="text-lg font-semibold text-blue-900 mb-2">
          🗺️ Your Learning Path
        </h2>
        <p className="text-blue-800 text-sm mb-4">
          Skills build on each other! Complete earlier skills to unlock advanced topics. 
          Your adaptive quiz will automatically choose the best questions based on your progress.
        </p>
        <div className="flex flex-wrap gap-2">
          <span className="px-3 py-1 bg-white text-blue-700 rounded-full text-xs font-medium border">
            Start with vertex and graphing
          </span>
          <span className="px-3 py-1 bg-white text-blue-700 rounded-full text-xs font-medium border">
            Progress to solving techniques
          </span>
          <span className="px-3 py-1 bg-white text-blue-700 rounded-full text-xs font-medium border">
            Master advanced analysis
          </span>
        </div>
      </div>
    </div>
  )
}