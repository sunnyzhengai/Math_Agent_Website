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
    // All skills unlocked - students can practice any skill at any time
    return true
  }

  const formatTime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    return hours > 0 ? `${hours}h ${minutes}m` : `${minutes}m`
  }

  // Skills ordered from prerequisites → requirements (topological sort)
  const skillOrder: SkillId[] = [
    // ===== LEVEL 0: Foundational skills (no prerequisites) =====
    'quad.graph.vertex',              // Graphing basics
    'quad.roots.factored',            // Understanding roots
    'quad.factoring.review',          // Factoring basics
    'quad.solve.square_root_property', // Square root method
    'quad.solutions.graphical',       // Graphical analysis

    // ===== LEVEL 1: Build on one foundational skill =====
    'quad.standard.vertex',           // Needs: graph.vertex
    'quad.intercepts',                // Needs: graph.vertex
    'quad.axis.symmetry',             // Needs: graph.vertex
    'quad.transformations',           // Needs: graph.vertex
    'quad.domain.range',              // Needs: graph.vertex
    'quad.solve.by_factoring',        // Needs: roots.factored
    'quad.solve.factoring',           // Needs: factoring.review

    // ===== LEVEL 2: Build on Level 1 skills =====
    'quad.discriminant.analysis',     // Needs: standard.vertex
    'quad.complete.square',           // Needs: standard.vertex
    'quad.applications.maxmin',       // Needs: graph.vertex + standard.vertex
    'quad.solve.inequalities',        // Needs: solve.by_factoring + roots.factored

    // ===== LEVEL 3: Build on Level 2 skills =====
    'quad.solve.by_formula',          // Needs: discriminant.analysis
    'quad.complete.square.solve',     // Needs: complete.square
    'quad.solutions.count',           // Needs: discriminant.analysis
    'quad.form.conversions'           // Needs: complete.square + solve.by_factoring
  ]

  // Organize skills into clear categories
  const skillCategories = {
    juliasCurrent: {
      title: "Julia's Current Homework Skills",
      description: "Practice what you're learning in class right now",
      color: "purple",
      skills: [
        'quad.factoring.review',
        'quad.solve.square_root_property',
        'quad.solve.factoring',
        'quad.solutions.graphical',
        'quad.complete.square.solve'
      ] as SkillId[]
    },
    graphing: {
      title: "Graphing & Visualization",
      description: "Understanding parabolas and their properties",
      color: "blue",
      skills: [
        'quad.graph.vertex',
        'quad.intercepts',
        'quad.axis.symmetry',
        'quad.transformations',
        'quad.domain.range'
      ] as SkillId[]
    },
    solving: {
      title: "Solving Equations",
      description: "Different methods to find solutions",
      color: "green",
      skills: [
        'quad.roots.factored',
        'quad.solve.by_factoring',
        'quad.complete.square',
        'quad.solve.by_formula'
      ] as SkillId[]
    },
    analysis: {
      title: "Analysis & Properties",
      description: "Deeper understanding of quadratic behavior",
      color: "orange",
      skills: [
        'quad.standard.vertex',
        'quad.discriminant.analysis',
        'quad.solutions.count',
        'quad.form.conversions'
      ] as SkillId[]
    },
    advanced: {
      title: "Advanced Topics",
      description: "Applications and complex problems",
      color: "red",
      skills: [
        'quad.solve.inequalities',
        'quad.applications.maxmin'
      ] as SkillId[]
    }
  }

  const getCategoryColor = (color: string) => {
    const colors = {
      purple: 'border-purple-200 bg-purple-50',
      blue: 'border-blue-200 bg-blue-50',
      green: 'border-green-200 bg-green-50',
      orange: 'border-orange-200 bg-orange-50',
      red: 'border-red-200 bg-red-50'
    }
    return colors[color as keyof typeof colors] || colors.blue
  }

  const getCategoryTitleColor = (color: string) => {
    const colors = {
      purple: 'text-purple-900',
      blue: 'text-blue-900',
      green: 'text-green-900',
      orange: 'text-orange-900',
      red: 'text-red-900'
    }
    return colors[color as keyof typeof colors] || colors.blue
  }

  const renderSkillCard = (skillId: SkillId) => {
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
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="text-center mb-12">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Quadratic Skills Practice</h1>
        <p className="text-lg text-gray-600 mb-6">Choose a category to practice specific skills</p>

        {/* Adaptive Quiz Button */}
        <button
          onClick={() => onStartQuiz(undefined as any)}
          className="inline-flex items-center space-x-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-4 rounded-xl font-semibold hover:from-blue-600 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
        >
          <PlayIcon className="icon-md" />
          <span>Start Adaptive Quiz</span>
        </button>
        <p className="text-sm text-gray-500 mt-2">Mix of all skills with adaptive difficulty</p>
      </div>

      {/* Skill Categories */}
      <div className="space-y-12">
        {Object.entries(skillCategories).map(([key, category]) => (
          <div key={key}>
            {/* Category Header */}
            <div className={`border-2 rounded-xl p-6 mb-6 ${getCategoryColor(category.color)}`}>
              <h2 className={`text-2xl font-bold mb-2 ${getCategoryTitleColor(category.color)}`}>
                {category.title}
              </h2>
              <p className="text-gray-700">{category.description}</p>
              <div className="mt-3 text-sm text-gray-600">
                {category.skills.length} skill{category.skills.length !== 1 ? 's' : ''} available
              </div>
            </div>

            {/* Skills Grid */}
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {category.skills.map(skillId => renderSkillCard(skillId))}
            </div>
          </div>
        ))}
      </div>

      {/* Learning Tips */}
      <div className="mt-12 bg-gradient-to-r from-blue-50 to-purple-50 border-2 border-blue-200 rounded-xl p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          📚 How to Use This Practice Platform
        </h2>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-semibold text-gray-900 mb-2">Start with Julia's Current Skills</h3>
            <p className="text-gray-700 text-sm">
              Practice the skills you're learning in class right now for the best results on homework and tests.
            </p>
          </div>
          <div>
            <h3 className="font-semibold text-gray-900 mb-2">Explore by Category</h3>
            <p className="text-gray-700 text-sm">
              Each category groups related skills together. Pick the topic you want to work on and practice those skills.
            </p>
          </div>
          <div>
            <h3 className="font-semibold text-gray-900 mb-2">Check Prerequisites</h3>
            <p className="text-gray-700 text-sm">
              Some skills list prerequisites. While all skills are unlocked, mastering foundations helps with advanced topics.
            </p>
          </div>
          <div>
            <h3 className="font-semibold text-gray-900 mb-2">Use Adaptive Quizzes</h3>
            <p className="text-gray-700 text-sm">
              The adaptive quiz mixes skills and adjusts difficulty automatically for comprehensive practice.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}