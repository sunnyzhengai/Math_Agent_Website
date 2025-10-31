# Component Usage Guide

## Question Component

The `Question` component is the core of the learning interface. It displays a math problem with multiple choice answers, tracks time, and handles submission.

### Basic Usage

```typescript
'use client'

import { useState } from 'react'
import Question from '@/components/Question'
import { api } from '@/lib/api'
import { Item } from '@/types/api'

export default function StudentAppPage() {
  const [item, setItem] = useState<Item | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const userId = 'julia_001' // From auth context

  // Load first question on mount
  useEffect(() => {
    loadNextItem()
  }, [])

  const loadNextItem = async () => {
    try {
      setIsLoading(true)
      const response = await api.nextItem(userId, 'Quadratics')
      setItem(response.item)
      setError(null)
    } catch (err) {
      setError(api.getErrorMessage(err))
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubmit = async (choiceId: string) => {
    try {
      setIsLoading(true)
      const result = await api.grade(userId, item!.item_id, choiceId)
      
      // Show feedback
      console.log('Correct:', result.correct)
      console.log('Mastery:', result.p_mastery_after)
      console.log('Tags:', result.tags)
      
      // Load next item after 2 seconds
      setTimeout(() => {
        loadNextItem()
      }, 2000)
    } catch (err) {
      setError(api.getErrorMessage(err))
    } finally {
      setIsLoading(false)
    }
  }

  if (error) return <div className="text-red-600">Error: {error}</div>
  if (!item) return <div>Loading...</div>

  return (
    <Question
      item={item}
      onSubmit={handleSubmit}
      isLoading={isLoading}
      timeLimit={300}
    />
  )
}
```

### Component Props

```typescript
interface QuestionProps {
  item: Item                           // Question data from API
  onSubmit: (choiceId: string) => Promise<void>  // Submit handler
  isLoading?: boolean                 // Show loading state
  timeLimit?: number                  // Time in seconds (default: 300)
}
```

### Item Structure (from API)

```typescript
{
  item_id: 'item_123',
  skill_id: 'quad.vertex.form',
  difficulty: 'easy',
  stem: 'Convert x² + 2x + 1 to vertex form',
  choices: [
    { id: 'c1', text: '(x + 1)²', tags_on_select: ['correct'] },
    { id: 'c2', text: '(x - 1)²', tags_on_select: ['sign_error'] },
    // ... 2 more
  ],
  explanation: 'When x² + 2x + 1 = (x + 1)²...',
  hints: ['Complete the square...']
}
```

## Sub-Components

### ChoiceButton

```typescript
import ChoiceButton from '@/components/ChoiceButton'

<ChoiceButton
  choice={{ id: 'c1', text: 'Answer A', tags_on_select: ['correct'] }}
  selected={false}
  disabled={false}
  onChange={() => console.log('Selected!')}
/>
```

### Timer

```typescript
import Timer from '@/components/Timer'

<Timer 
  seconds={45}  // Show "0:45"
  warning={true}  // Red color if < 60 seconds
/>
```

## Full Page Example

```typescript
'use client'

import { useEffect, useState } from 'react'
import { useAppStore } from '@/lib/store'  // Coming soon
import Question from '@/components/Question'
import { api } from '@/lib/api'
import { Item, GradeResponse } from '@/types/api'

export default function AppPage() {
  const userId = 'julia_001'
  const [item, setItem] = useState<Item | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [feedback, setFeedback] = useState<GradeResponse | null>(null)
  const [showingFeedback, setShowingFeedback] = useState(false)

  useEffect(() => {
    getNextQuestion()
  }, [])

  const getNextQuestion = async () => {
    try {
      setIsLoading(true)
      setShowingFeedback(false)
      setFeedback(null)
      
      const response = await api.nextItem(userId, 'Quadratics')
      setItem(response.item)
    } catch (error) {
      console.error(api.getErrorMessage(error))
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubmit = async (choiceId: string) => {
    if (!item) return
    
    try {
      setIsLoading(true)
      const result = await api.grade(
        userId,
        item.item_id,
        choiceId,
        5000,  // Time spent in ms
        0.8    // Confidence (0-1)
      )
      
      setFeedback(result)
      setShowingFeedback(true)
      
      // Auto-load next question after 3 seconds
      setTimeout(() => {
        getNextQuestion()
      }, 3000)
    } catch (error) {
      console.error(api.getErrorMessage(error))
    } finally {
      setIsLoading(false)
    }
  }

  if (!item) return <div className="p-8">Loading first question...</div>

  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <div className="max-w-4xl mx-auto">
        {/* Mastery Progress */}
        <div className="mb-8">
          <div className="bg-white rounded-lg p-4 shadow">
            <p className="text-sm text-gray-600 mb-2">Your Mastery</p>
            <div className="w-full bg-gray-200 rounded-full h-3">
              <div
                className="bg-blue-600 h-3 rounded-full transition-all"
                style={{ width: '60%' }}
              ></div>
            </div>
          </div>
        </div>

        {/* Question Component */}
        {!showingFeedback && (
          <Question
            item={item}
            onSubmit={handleSubmit}
            isLoading={isLoading}
            timeLimit={300}
          />
        )}

        {/* Feedback */}
        {showingFeedback && feedback && (
          <div
            className={`text-center p-8 rounded-lg ${
              feedback.correct
                ? 'bg-green-50 border border-green-200'
                : 'bg-red-50 border border-red-200'
            }`}
          >
            <h2 className={`text-2xl font-bold mb-2 ${
              feedback.correct ? 'text-green-700' : 'text-red-700'
            }`}>
              {feedback.correct ? '✓ Correct!' : '✗ Not quite...'}
            </h2>
            <p className={feedback.correct ? 'text-green-600' : 'text-red-600'}>
              Mastery: {(feedback.p_mastery_after * 100).toFixed(0)}%
            </p>
            {feedback.tags && feedback.tags.length > 0 && (
              <p className="text-sm text-gray-600 mt-2">
                Tags: {feedback.tags.join(', ')}
              </p>
            )}
            <p className="text-sm text-gray-600 mt-4">
              Loading next question...
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
```

## Integration Checklist

- [x] Question component with timer
- [x] ChoiceButton with selection
- [x] Timer with warning state
- [x] API client integration
- [ ] Feedback display component (next)
- [ ] ProgressBar component (next)
- [ ] Mini-lesson drawer (next)
- [ ] Auth wrapper (next)

## Next Steps

After integrating this into a page:
1. Build `FeedbackCard` for displaying results
2. Build `ProgressBar` for mastery visualization
3. Create full `/app/app/page.tsx` student page
4. Add state management with Zustand
5. Wire up Supabase auth
