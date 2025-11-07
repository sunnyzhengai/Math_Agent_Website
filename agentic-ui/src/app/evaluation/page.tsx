'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { 
  ArrowLeftIcon,
  BeakerIcon,
  PlayIcon,
  CheckCircleIcon,
  XCircleIcon,
  ClockIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline'
import { AgentType, EvaluationResult, SkillId, Difficulty } from '@/types/agentic'
import { AGENT_DEFINITIONS, SKILL_DEFINITIONS, DIFFICULTY_DEFINITIONS } from '@/lib/skills'
import { api } from '@/lib/api'

export default function EvaluationPage() {
  const [selectedAgent, setSelectedAgent] = useState<AgentType>('rules')
  const [evaluationResults, setEvaluationResults] = useState<EvaluationResult[]>([])
  const [loading, setLoading] = useState(false)
  const [hasRun, setHasRun] = useState(false)

  const runEvaluation = async () => {
    setLoading(true)
    try {
      const results = await api.runAgentEvaluation(selectedAgent)
      setEvaluationResults(results)
      setHasRun(true)
    } catch (error) {
      console.error('Error running evaluation:', error)
    } finally {
      setLoading(false)
    }
  }

  // Calculate summary statistics
  const getStats = () => {
    if (evaluationResults.length === 0) return null

    const total = evaluationResults.length
    const correct = evaluationResults.filter(r => r.ok).length
    const accuracy = (correct / total) * 100

    // By skill
    const bySkill: Record<SkillId, { total: number; correct: number }> = {}
    evaluationResults.forEach(result => {
      if (!bySkill[result.skill_id]) {
        bySkill[result.skill_id] = { total: 0, correct: 0 }
      }
      bySkill[result.skill_id].total++
      if (result.ok) bySkill[result.skill_id].correct++
    })

    // By difficulty
    const byDifficulty: Record<Difficulty, { total: number; correct: number }> = {} as any
    evaluationResults.forEach(result => {
      if (!byDifficulty[result.difficulty]) {
        byDifficulty[result.difficulty] = { total: 0, correct: 0 }
      }
      byDifficulty[result.difficulty].total++
      if (result.ok) byDifficulty[result.difficulty].correct++
    })

    return {
      total,
      correct,
      accuracy,
      bySkill,
      byDifficulty
    }
  }

  const stats = getStats()

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between py-4">
            <div className="flex items-center space-x-4">
              <Link href="/" className="text-gray-500 hover:text-gray-700">
                <ArrowLeftIcon className="w-6 h-6" />
              </Link>
              <div className="flex items-center space-x-3">
                <BeakerIcon className="w-6 h-6 text-purple-600" />
                <h1 className="text-xl font-semibold text-gray-900">Evaluation Center</h1>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid lg:grid-cols-4 gap-8">
          {/* Controls */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-sm border p-6 sticky top-8">
              <h2 className="text-lg font-semibold text-gray-900 mb-6">Run Evaluation</h2>
              
              {/* Agent Selection */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  Select Agent to Test
                </label>
                <div className="space-y-2">
                  {Object.entries(AGENT_DEFINITIONS).map(([key, agent]) => (
                    <label key={key} className="flex items-center">
                      <input
                        type="radio"
                        name="agent"
                        value={key}
                        checked={selectedAgent === key}
                        onChange={(e) => setSelectedAgent(e.target.value as AgentType)}
                        className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
                      />
                      <div className="ml-3">
                        <div className="text-sm font-medium text-gray-900">{agent.name}</div>
                        <div className="text-xs text-gray-500">{agent.description}</div>
                      </div>
                    </label>
                  ))}
                </div>
              </div>

              {/* Evaluation Info */}
              <div className="mb-6 p-4 bg-blue-50 rounded-lg">
                <h3 className="text-sm font-medium text-blue-800 mb-2">Evaluation Dataset</h3>
                <div className="text-sm text-blue-700 space-y-1">
                  <div>• 36 seed evaluation cases</div>
                  <div>• 9 skills × 4 difficulties</div>
                  <div>• Deterministic & reproducible</div>
                  <div>• Comprehensive coverage</div>
                </div>
              </div>

              {/* Run Button */}
              <button
                onClick={runEvaluation}
                disabled={loading}
                className="w-full flex items-center justify-center px-4 py-3 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <ArrowPathIcon className="w-4 h-4 mr-2 animate-spin" />
                    Running...
                  </>
                ) : (
                  <>
                    <PlayIcon className="w-4 h-4 mr-2" />
                    Run Evaluation
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Results */}
          <div className="lg:col-span-3">
            {!hasRun ? (
              <div className="bg-white rounded-lg shadow-sm border p-12 text-center">
                <BeakerIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Ready to Evaluate</h3>
                <p className="text-gray-600 mb-6">
                  Select an agent and run the comprehensive evaluation to see performance 
                  across all 36 seed cases covering 9 quadratic skills.
                </p>
                <div className="grid grid-cols-3 gap-4 max-w-md mx-auto">
                  <div className="text-center">
                    <div className="text-xl font-bold text-blue-600">36</div>
                    <div className="text-xs text-gray-500">Test Cases</div>
                  </div>
                  <div className="text-center">
                    <div className="text-xl font-bold text-green-600">9</div>
                    <div className="text-xs text-gray-500">Skills</div>
                  </div>
                  <div className="text-center">
                    <div className="text-xl font-bold text-purple-600">4</div>
                    <div className="text-xs text-gray-500">Difficulties</div>
                  </div>
                </div>
              </div>
            ) : loading ? (
              <div className="bg-white rounded-lg shadow-sm border p-12 text-center">
                <ArrowPathIcon className="w-16 h-16 text-blue-600 mx-auto mb-4 animate-spin" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Running Evaluation</h3>
                <p className="text-gray-600">
                  Testing {AGENT_DEFINITIONS[selectedAgent].name} across all seed cases...
                </p>
              </div>
            ) : stats ? (
              <div className="space-y-6">
                {/* Summary Stats */}
                <div className="bg-white rounded-lg shadow-sm border p-6">
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {AGENT_DEFINITIONS[selectedAgent].name} Performance
                    </h3>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-blue-600">
                        {stats.accuracy.toFixed(1)}%
                      </div>
                      <div className="text-sm text-gray-500">
                        {stats.correct}/{stats.total} correct
                      </div>
                    </div>
                  </div>

                  {/* By Skill Performance */}
                  <div className="mb-6">
                    <h4 className="text-sm font-medium text-gray-700 mb-3">Performance by Skill</h4>
                    <div className="space-y-2">
                      {Object.entries(stats.bySkill).map(([skillId, skillStats]) => {
                        const accuracy = (skillStats.correct / skillStats.total) * 100
                        return (
                          <div key={skillId} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                            <span className="text-sm text-gray-700">
                              {SKILL_DEFINITIONS[skillId as SkillId]?.name || skillId}
                            </span>
                            <div className="flex items-center space-x-2">
                              <span className="text-sm text-gray-600">
                                {skillStats.correct}/{skillStats.total}
                              </span>
                              <span className={`text-sm font-medium ${
                                accuracy >= 75 ? 'text-green-600' : 
                                accuracy >= 50 ? 'text-yellow-600' : 'text-red-600'
                              }`}>
                                {accuracy.toFixed(0)}%
                              </span>
                            </div>
                          </div>
                        )
                      })}
                    </div>
                  </div>

                  {/* By Difficulty Performance */}
                  <div>
                    <h4 className="text-sm font-medium text-gray-700 mb-3">Performance by Difficulty</h4>
                    <div className="grid grid-cols-4 gap-2">
                      {Object.entries(stats.byDifficulty).map(([difficulty, diffStats]) => {
                        const accuracy = (diffStats.correct / diffStats.total) * 100
                        return (
                          <div key={difficulty} className="text-center p-3 bg-gray-50 rounded">
                            <div className={`text-xs font-medium mb-1 ${
                              DIFFICULTY_DEFINITIONS[difficulty as Difficulty].color
                            }`}>
                              {difficulty}
                            </div>
                            <div className="text-lg font-bold text-gray-900">
                              {accuracy.toFixed(0)}%
                            </div>
                            <div className="text-xs text-gray-500">
                              {diffStats.correct}/{diffStats.total}
                            </div>
                          </div>
                        )
                      })}
                    </div>
                  </div>
                </div>

                {/* Detailed Results */}
                <div className="bg-white rounded-lg shadow-sm border">
                  <div className="px-6 py-4 border-b">
                    <h3 className="text-lg font-semibold text-gray-900">Detailed Results</h3>
                    <p className="text-sm text-gray-600">Individual test case outcomes</p>
                  </div>
                  <div className="p-6">
                    <div className="space-y-2 max-h-96 overflow-y-auto">
                      {evaluationResults.map((result, index) => (
                        <div
                          key={result.id}
                          className={`flex items-center justify-between p-3 rounded-lg border ${
                            result.ok 
                              ? 'bg-green-50 border-green-200' 
                              : 'bg-red-50 border-red-200'
                          }`}
                        >
                          <div className="flex items-center space-x-3">
                            {result.ok ? (
                              <CheckCircleIcon className="w-5 h-5 text-green-600" />
                            ) : (
                              <XCircleIcon className="w-5 h-5 text-red-600" />
                            )}
                            <div>
                              <div className="text-sm font-medium text-gray-900">
                                {SKILL_DEFINITIONS[result.skill_id]?.name || result.skill_id}
                              </div>
                              <div className="text-xs text-gray-500">
                                {result.id} • {result.difficulty} • seed: {result.seed}
                              </div>
                            </div>
                          </div>
                          <div className="flex items-center space-x-4 text-sm">
                            <div className="text-gray-600">
                              Agent: <span className="font-mono">{result.picked || 'N/A'}</span>
                            </div>
                            <div className="text-gray-600">
                              Correct: <span className="font-mono">{result.solution}</span>
                            </div>
                            <div className="flex items-center text-gray-500">
                              <ClockIcon className="w-4 h-4 mr-1" />
                              {result.gen_ms.toFixed(1)}ms
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            ) : null}
          </div>
        </div>
      </div>
    </div>
  )
}