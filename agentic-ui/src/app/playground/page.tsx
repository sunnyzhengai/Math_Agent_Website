'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { 
  ArrowLeftIcon,
  BeakerIcon,
  CheckCircleIcon,
  XCircleIcon,
  ArrowPathIcon,
  PlayIcon
} from '@heroicons/react/24/outline'
import { AgentType, SkillId, Difficulty, MathItem } from '@/types/agentic'
import { SKILL_DEFINITIONS, AGENT_DEFINITIONS, DIFFICULTY_DEFINITIONS } from '@/lib/skills'
import { api } from '@/lib/api'

export default function PlaygroundPage() {
  const [selectedAgent, setSelectedAgent] = useState<AgentType>('rules')
  const [selectedSkill, setSelectedSkill] = useState<SkillId>('quad.graph.vertex')
  const [selectedDifficulty, setSelectedDifficulty] = useState<Difficulty>('easy')
  const [currentItem, setCurrentItem] = useState<MathItem | null>(null)
  const [loading, setLoading] = useState(false)
  const [agentResponse, setAgentResponse] = useState<string | null>(null)
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null)
  const [showSolution, setShowSolution] = useState(false)

  // Generate a new question
  const generateQuestion = async () => {
    setLoading(true)
    setAgentResponse(null)
    setIsCorrect(null)
    setShowSolution(false)
    
    try {
      const item = await api.generateItem(selectedSkill, selectedDifficulty)
      setCurrentItem(item)
    } catch (error) {
      console.error('Error generating item:', error)
    } finally {
      setLoading(false)
    }
  }

  // Test agent on current question
  const testAgent = async () => {
    if (!currentItem) return
    
    setLoading(true)
    try {
      const result = await api.testAgent(selectedAgent, currentItem)
      setAgentResponse(result.choice)
      setIsCorrect(result.correct)
      setShowSolution(true)
    } catch (error) {
      console.error('Error testing agent:', error)
    } finally {
      setLoading(false)
    }
  }

  // Generate initial question
  useEffect(() => {
    generateQuestion()
  }, [selectedSkill, selectedDifficulty])

  const agentInfo = AGENT_DEFINITIONS[selectedAgent]
  const skillInfo = SKILL_DEFINITIONS[selectedSkill]

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
                <BeakerIcon className="w-6 h-6 text-blue-600" />
                <h1 className="text-xl font-semibold text-gray-900">Agent Playground</h1>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Controls Panel */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-sm border p-6 sticky top-8">
              <h2 className="text-lg font-semibold text-gray-900 mb-6">Test Configuration</h2>
              
              {/* Agent Selection */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  Select Agent
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

              {/* Skill Selection */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  Select Skill
                </label>
                <select
                  value={selectedSkill}
                  onChange={(e) => setSelectedSkill(e.target.value as SkillId)}
                  className="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                >
                  {Object.entries(SKILL_DEFINITIONS).map(([key, skill]) => (
                    <option key={key} value={key}>
                      {skill.name}
                    </option>
                  ))}
                </select>
                <p className="mt-1 text-xs text-gray-500">
                  {skillInfo.description}
                </p>
              </div>

              {/* Difficulty Selection */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  Select Difficulty
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {Object.entries(DIFFICULTY_DEFINITIONS).map(([key, diff]) => (
                    <button
                      key={key}
                      onClick={() => setSelectedDifficulty(key as Difficulty)}
                      className={`px-3 py-2 text-sm font-medium rounded-md border transition-colors ${
                        selectedDifficulty === key
                          ? 'bg-blue-50 border-blue-200 text-blue-700'
                          : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
                      }`}
                    >
                      {diff.name}
                    </button>
                  ))}
                </div>
              </div>

              {/* Action Buttons */}
              <div className="space-y-3">
                <button
                  onClick={generateQuestion}
                  disabled={loading}
                  className="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                >
                  {loading ? (
                    <ArrowPathIcon className="w-4 h-4 mr-2 animate-spin" />
                  ) : (
                    <ArrowPathIcon className="w-4 h-4 mr-2" />
                  )}
                  New Question
                </button>
                
                <button
                  onClick={testAgent}
                  disabled={loading || !currentItem}
                  className="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
                >
                  <PlayIcon className="w-4 h-4 mr-2" />
                  Test Agent
                </button>
              </div>
            </div>
          </div>

          {/* Question Display */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-sm border p-6">
              {loading && !currentItem ? (
                <div className="flex items-center justify-center py-12">
                  <ArrowPathIcon className="w-8 h-8 animate-spin text-blue-600" />
                  <span className="ml-3 text-gray-600">Generating question...</span>
                </div>
              ) : currentItem ? (
                <div>
                  {/* Question Header */}
                  <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center space-x-3">
                      <h3 className="text-lg font-semibold text-gray-900">
                        {SKILL_DEFINITIONS[currentItem.skill_id].name}
                      </h3>
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        DIFFICULTY_DEFINITIONS[currentItem.difficulty].color
                      }`}>
                        {DIFFICULTY_DEFINITIONS[currentItem.difficulty].name}
                      </span>
                    </div>
                    <div className="text-sm text-gray-500">
                      ID: {currentItem.item_id.split(':')[2] || 'generated'}
                    </div>
                  </div>

                  {/* Question Stem */}
                  <div className="mb-6">
                    <div className="math-stem bg-gray-50 p-4 rounded-lg border">
                      {currentItem.stem}
                    </div>
                  </div>

                  {/* Answer Choices */}
                  <div className="mb-6">
                    <h4 className="text-sm font-medium text-gray-700 mb-3">Answer Choices:</h4>
                    <div className="space-y-2">
                      {currentItem.choices.map((choice) => (
                        <div
                          key={choice.id}
                          className={`p-3 rounded-lg border transition-colors ${
                            agentResponse === choice.id
                              ? isCorrect
                                ? 'bg-green-50 border-green-200'
                                : 'bg-red-50 border-red-200'
                              : showSolution && choice.id === currentItem.solution_choice_id
                              ? 'bg-blue-50 border-blue-200'
                              : 'bg-gray-50 border-gray-200'
                          }`}
                        >
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                              <span className="font-mono font-semibold text-gray-700">
                                {choice.id}.
                              </span>
                              <span className="math-choice">{choice.text}</span>
                            </div>
                            {agentResponse === choice.id && (
                              <div className="flex items-center space-x-2">
                                <span className="text-xs text-gray-600">Agent Choice</span>
                                {isCorrect ? (
                                  <CheckCircleIcon className="w-5 h-5 text-green-600" />
                                ) : (
                                  <XCircleIcon className="w-5 h-5 text-red-600" />
                                )}
                              </div>
                            )}
                            {showSolution && choice.id === currentItem.solution_choice_id && agentResponse !== choice.id && (
                              <div className="flex items-center space-x-2">
                                <span className="text-xs text-gray-600">Correct Answer</span>
                                <CheckCircleIcon className="w-5 h-5 text-blue-600" />
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Agent Response */}
                  {agentResponse && (
                    <div className="mb-6">
                      <div className={`p-4 rounded-lg border ${
                        isCorrect ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'
                      }`}>
                        <div className="flex items-center space-x-3">
                          <div className={`w-3 h-3 rounded-full ${agentInfo.color}`} />
                          <span className="font-medium text-gray-900">
                            {agentInfo.name} selected: {agentResponse}
                          </span>
                          {isCorrect ? (
                            <CheckCircleIcon className="w-5 h-5 text-green-600" />
                          ) : (
                            <XCircleIcon className="w-5 h-5 text-red-600" />
                          )}
                        </div>
                        <div className="mt-2 text-sm text-gray-600">
                          {isCorrect ? 'Correct! ' : 'Incorrect. '}
                          The correct answer is {currentItem.solution_choice_id}: {currentItem.solution_text}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-12 text-gray-500">
                  Select a skill and difficulty to generate a question
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}