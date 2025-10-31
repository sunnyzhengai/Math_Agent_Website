'use client'

import { Choice } from '@/types/api'

interface ChoiceButtonProps {
  choice: Choice
  selected: boolean
  disabled?: boolean
  onChange?: () => void
  [key: string]: any // Allow aria-* and other props
}

/**
 * ChoiceButton Component
 * 
 * Displays a single answer choice as a selectable button.
 * Shows:
 * - Choice text
 * - Selection state (border, background)
 * - Hover effects
 * - Disabled state
 */
export default function ChoiceButton({
  choice,
  selected,
  disabled = false,
  onChange,
  ...props
}: ChoiceButtonProps) {
  return (
    <button
      onClick={onChange}
      disabled={disabled}
      className={`w-full p-4 text-left rounded-lg border-2 transition-all ${
        selected
          ? 'border-blue-600 bg-blue-50'
          : 'border-gray-200 bg-white hover:border-gray-300'
      } ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
      type="button"
      {...props}
    >
      {/* Choice Letter / Icon */}
      <div className="flex items-start gap-3">
        <div
          className={`flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center text-sm font-semibold ${
            selected
              ? 'border-blue-600 bg-blue-600 text-white'
              : 'border-gray-300 bg-white text-gray-600'
          }`}
        >
          {selected ? '✓' : ''}
        </div>

        {/* Choice Text */}
        <p className={`text-lg ${selected ? 'font-semibold text-gray-900' : 'text-gray-700'}`}>
          {choice.text}
        </p>
      </div>
    </button>
  )
}
