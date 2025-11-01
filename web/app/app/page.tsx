'use client'

import { useEffect, useState } from 'react'
import Question from '@/components/Question'
import { api } from '@/lib/api'
import { Item, GradeResponse, NextItemResponse } from '@/types/api'

interface PageState {
  item: Item | null
  isLoading: boolean
  error: string | null
  feedback: GradeResponse | null
  showingFeedback: boolean
  masteryPercent: number
  attemptCount: number
}

/**
 * Student App Page
 * 
 * Main learning interface where Julia answers questions.
 * Flow:
 * 1. Load first question on mount
 * 2. Display Question component
 * 3. Handle submission → show feedback
 * 4. Auto-load next question after 3 seconds
 * 5. Update mastery display
 */
export default function AppPage() {
  const userId = 'julia_001' // TODO: Get from auth context
  const [state, setState] = useState<PageState>({
    item: null,
    isLoading: true,
    error: null,
    feedback: null,
    showingFeedback: false,
    masteryPercent: 50,
    attemptCount: 0,
  })

  // Load first question on mount
  useEffect(() => {
    loadNextQuestion()
  }, [])

  /**
   * Load next question from backend
   */
  const loadNextQuestion = async () => {
    try {
      setState((prev) => ({
        ...prev,
        isLoading: true,
        error: null,
        feedback: null,
        showingFeedback: false,
      }))

      const response: NextItemResponse = await api.nextItem(userId, 'Quadratics')
      
      setState((prev) => ({
        ...prev,
        item: response.item,
        isLoading: false,
        masteryPercent: Math.round(response.learner_mastery_before * 100),
      }))
    } catch (error) {
      const errorMsg = api.getErrorMessage(error)
      setState((prev) => ({
        ...prev,
        error: errorMsg,
        isLoading: false,
      }))
    }
  }

  /**
   * Handle answer submission
   */
  const handleSubmit = async (choiceId: string) => {
    if (!state.item) return

    try {
      setState((prev) => ({ ...prev, isLoading: true }))

      // Grade the response
      const result: GradeResponse = await api.grade(
        userId,
        state.item.item_id,
        choiceId,
        5000, // 5 seconds (would be calculated in real app)
        0.75  // Confidence (could come from slider)
      )

      // Update state with feedback
      setState((prev) => ({
        ...prev,
        feedback: result,
        showingFeedback: true,
        isLoading: false,
        masteryPercent: Math.round(result.p_mastery_after * 100),
        attemptCount: prev.attemptCount + 1,
      }))

      // Auto-load next question after 3 seconds
      setTimeout(() => {
        loadNextQuestion()
      }, 3000)
    } catch (error) {
      const errorMsg = api.getErrorMessage(error)
      setState((prev) => ({
        ...prev,
        error: errorMsg,
        isLoading: false,
      }))
    }
  }

  // Render loading state
  if (state.isLoading && !state.item) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your next question...</p>
        </div>
      </div>
    )
  }

  // Render error state
  if (state.error && !state.item) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-md">
          <h2 className="text-2xl font-bold text-red-600 mb-4">Error</h2>
          <p className="text-gray-700 mb-6">{state.error}</p>
          <button
            onClick={loadNextQuestion}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700"
          >
            Try Again
          </button>
        </div>
      </div>
    )
  }

  // Render main learning interface
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 py-8">
      <div className="max-w-4xl mx-auto">
        {/* Header with progress */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-3xl font-bold text-gray-900">Quadratics</h1>
            <div className="text-right">
              <p className="text-sm text-gray-600">Your Mastery</p>
              <p className="text-3xl font-bold text-blue-600">
                {state.masteryPercent}%
              </p>
            </div>
          </div>

          {/* Mastery Progress Bar */}
          <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
            <div
              className="bg-gradient-to-r from-blue-500 to-indigo-600 h-full transition-all duration-500"
              style={{ width: `${state.masteryPercent}%` }}
            ></div>
          </div>

          {/* Stats */}
          <div className="mt-4 flex gap-4 text-sm">
            <span className="text-gray-600">
              Questions answered: <strong>{state.attemptCount}</strong>
            </span>
          </div>
        </div>

        {/* Main Content */}
        {!state.showingFeedback && state.item ? (
          <Question
            item={state.item}
            onSubmit={handleSubmit}
            isLoading={state.isLoading}
            timeLimit={300}
          />
        ) : null}

        {/* Feedback Card */}
        {state.showingFeedback && state.feedback ? (
          <div
            className={`rounded-lg shadow-lg p-8 text-center transition-all ${
              state.feedback.correct
                ? 'bg-gradient-to-br from-green-50 to-emerald-50 border-l-4 border-green-500'
                : 'bg-gradient-to-br from-orange-50 to-red-50 border-l-4 border-orange-500'
            }`}
          >
            {/* Result Icon */}
            <div className="mb-4">
              {state.feedback.correct ? (
                <div className="text-6xl">✨</div>
              ) : (
                <div className="text-6xl">🤔</div>
              )}
            </div>

            {/* Result Text */}
            <h2
              className={`text-4xl font-bold mb-2 ${
                state.feedback.correct ? 'text-green-700' : 'text-orange-700'
              }`}
            >
              {state.feedback.correct ? 'Correct!' : 'Not quite...'}
            </h2>

            {/* Mastery Update */}
            <p className="text-2xl font-semibold mb-4">
              <span
                className={
                  state.feedback.correct ? 'text-green-600' : 'text-orange-600'
                }
              >
                Mastery: {Math.round(state.feedback.p_mastery_after * 100)}%
              </span>
            </p>

            {/* Tags */}
            {state.feedback.tags && state.feedback.tags.length > 0 && (
              <div className="mb-4">
                <p className="text-sm text-gray-600 mb-2">Detected:</p>
                <div className="flex flex-wrap gap-2 justify-center">
                  {state.feedback.tags.map((tag) => (
                    <span
                      key={tag}
                      className="px-3 py-1 bg-gray-200 text-gray-700 rounded-full text-sm font-medium"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Resource Link */}
            {state.feedback.suggested_resource_url && (
              <div className="mb-4">
                <a
                  href={state.feedback.suggested_resource_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-block px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  📚 Learn More
                </a>
              </div>
            )}

            {/* Loading Next */}
            <p className="text-sm text-gray-600 mt-6">
              {state.isLoading
                ? 'Loading next question...'
                : 'Getting your next question...'}
            </p>
          </div>
        ) : null}

        {/* Error in feedback */}
        {state.error && state.showingFeedback && (
          <div className="bg-red-50 border-l-4 border-red-500 rounded-lg p-6 text-red-700">
            <p className="font-semibold mb-2">Error submitting answer:</p>
            <p>{state.error}</p>
            <button
              onClick={loadNextQuestion}
              className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
            >
              Try Next Question
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
