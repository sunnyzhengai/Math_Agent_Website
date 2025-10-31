'use client'

import { useState, useEffect } from 'react'
import { Item } from '@/types/api'
import ChoiceButton from './ChoiceButton'
import Timer from './Timer'

interface QuestionProps {
  item: Item
  onSubmit: (choiceId: string) => Promise<void>
  isLoading?: boolean
  timeLimit?: number // seconds
}

/**
 * Question Component
 * 
 * Displays a math question with multiple choice options.
 * Features:
 * - Responsive layout
 * - Choice selection tracking
 * - Timer countdown
 * - Submit with loading state
 * - Accessibility (ARIA labels)
 */
export default function Question({
  item,
  onSubmit,
  isLoading = false,
  timeLimit = 300, // 5 minutes default
}: QuestionProps) {
  const [selectedChoice, setSelectedChoice] = useState<string | null>(null)
  const [timeRemaining, setTimeRemaining] = useState(timeLimit)
  const [hasSubmitted, setHasSubmitted] = useState(false)

  // Timer countdown
  useEffect(() => {
    if (hasSubmitted) return

    const interval = setInterval(() => {
      setTimeRemaining((prev) => {
        if (prev <= 1) {
          // Auto-submit on timeout
          handleSubmit()
          return 0
        }
        return prev - 1
      })
    }, 1000)

    return () => clearInterval(interval)
  }, [hasSubmitted])

  const handleSubmit = async () => {
    if (!selectedChoice || isLoading) return

    setHasSubmitted(true)
    try {
      await onSubmit(selectedChoice)
    } catch (error) {
      // Error handled by parent component
      setHasSubmitted(false)
    }
  }

  const isTimeWarning = timeRemaining < 60
  const isTimeExpired = timeRemaining <= 0

  return (
    <div className="w-full max-w-2xl mx-auto">
      {/* Header with timer */}
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Question</h1>
        <div
          className={`text-lg font-semibold ${
            isTimeWarning ? 'text-red-600' : 'text-gray-600'
          }`}
          aria-label={`Time remaining: ${timeRemaining} seconds`}
        >
          <Timer seconds={timeRemaining} warning={isTimeWarning} />
        </div>
      </div>

      {/* Question Card */}
      <div className="bg-white rounded-lg shadow-md p-8 mb-8">
        {/* Question Stem */}
        <div className="mb-8">
          <p className="text-xl text-gray-800 leading-relaxed font-medium">
            {item.stem}
          </p>
          {item.hints && item.hints.length > 0 && (
            <div className="mt-4 p-3 bg-blue-50 border-l-4 border-blue-500 rounded">
              <p className="text-sm text-blue-800">
                <strong>Hint:</strong> {item.hints[0]}
              </p>
            </div>
          )}
        </div>

        {/* Choices */}
        <fieldset className="mb-8">
          <legend className="sr-only">Answer options</legend>
          <div className="space-y-3">
            {item.choices.map((choice) => (
              <ChoiceButton
                key={choice.id}
                choice={choice}
                selected={selectedChoice === choice.id}
                disabled={isLoading || hasSubmitted}
                onChange={() => !isLoading && setSelectedChoice(choice.id)}
                aria-checked={selectedChoice === choice.id}
              />
            ))}
          </div>
        </fieldset>

        {/* Confidence Slider (optional) */}
        <div className="mb-8">
          <label
            htmlFor="confidence"
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            How confident are you? ({Math.round((item.confidence_target || 0.7) * 100)}%)
          </label>
          <input
            id="confidence"
            type="range"
            min="0"
            max="100"
            defaultValue={Math.round((item.confidence_target || 0.7) * 100)}
            disabled={isLoading || hasSubmitted}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer disabled:opacity-50"
          />
        </div>

        {/* Submit Button */}
        <button
          onClick={handleSubmit}
          disabled={!selectedChoice || isLoading || hasSubmitted || isTimeExpired}
          className={`w-full py-3 px-4 rounded-lg font-semibold text-white transition-all ${
            !selectedChoice || isLoading || hasSubmitted || isTimeExpired
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700 active:scale-95'
          }`}
          aria-busy={isLoading}
          aria-disabled={!selectedChoice || isLoading}
        >
          {isLoading && (
            <>
              <span className="inline-block animate-spin mr-2">⏳</span>
              Checking answer...
            </>
          )}
          {!isLoading && hasSubmitted && 'Answer submitted!'}
          {!isLoading && !hasSubmitted && 'Submit Answer'}
        </button>

        {isTimeExpired && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded text-red-700 text-sm">
            Time's up! Your answer has been auto-submitted.
          </div>
        )}
      </div>

      {/* Explanation (shown after submission) */}
      {hasSubmitted && item.explanation && (
        <div className="bg-green-50 border-l-4 border-green-500 rounded-lg p-6">
          <h3 className="font-semibold text-green-900 mb-2">Explanation:</h3>
          <p className="text-green-800 leading-relaxed">{item.explanation}</p>
        </div>
      )}
    </div>
  )
}
