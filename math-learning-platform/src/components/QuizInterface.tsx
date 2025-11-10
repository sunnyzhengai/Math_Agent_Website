'use client'

import { useState, useEffect } from 'react'
import { Question, QuestionResult, StudentResponse, SkillId } from '@/types/learning'
import { learningApi } from '@/lib/learning-api'
import {
  XMarkIcon,
  ClockIcon,
  CheckCircleIcon,
  XCircleIcon,
  LightBulbIcon,
  ArrowRightIcon
} from '@heroicons/react/24/outline'
import {
  generateSessionId,
  generateQuestionId,
  logQuestionPresented,
  logQuestionAnswered,
  logSessionSummary
} from '@/lib/telemetry'
import MathText from './MathText'
import SmartMathText from './SmartMathText'

interface QuizInterfaceProps {
  studentId: string
  selectedSkill?: SkillId | null
  onComplete: () => void
  onExit: () => void
}

type QuizState = 'loading' | 'question' | 'feedback' | 'error'

export default function QuizInterface({
  studentId,
  selectedSkill,
  onComplete,
  onExit
}: QuizInterfaceProps) {
  const [state, setState] = useState<QuizState>('loading')
  const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null)
  const [selectedChoice, setSelectedChoice] = useState<string | null>(null)
  const [questionResult, setQuestionResult] = useState<QuestionResult | null>(null)
  const [startTime, setStartTime] = useState<number>(Date.now())
  const [questionsAnswered, setQuestionsAnswered] = useState(0)
  const [questionsCorrect, setQuestionsCorrect] = useState(0)

  // Telemetry tracking
  const [sessionId] = useState(() => generateSessionId())
  const [sessionStartTime] = useState(() => Date.now())
  const [currentQuestionId, setCurrentQuestionId] = useState<string | null>(null)
  const [skillsPracticed, setSkillsPracticed] = useState<Set<string>>(new Set())
  const [difficultyCount, setDifficultyCount] = useState<Record<string, number>>({})

  useEffect(() => {
    loadNextQuestion()
  }, [])

  const loadNextQuestion = async () => {
    try {
      setState('loading')
      const question = await learningApi.getNextQuestion(studentId, selectedSkill || undefined)
      setCurrentQuestion(question)
      setSelectedChoice(null)
      setQuestionResult(null)
      setStartTime(Date.now())
      setState('question')

      // Generate question ID and log presentation
      const questionId = generateQuestionId()
      setCurrentQuestionId(questionId)

      // Track skills and difficulties
      setSkillsPracticed(prev => new Set(prev).add(question.skill_id))
      setDifficultyCount(prev => ({
        ...prev,
        [question.difficulty]: (prev[question.difficulty] || 0) + 1
      }))

      // Log telemetry: question presented
      logQuestionPresented({
        sessionId,
        questionId,
        skillId: question.skill_id,
        difficulty: question.difficulty,
        generationMethod: 'parameterized', // Using infinite variations with difficulty-aware distractors
        questionStem: question.stem,
        correctAnswer: question.choices.find(c => c.id === question.solution_choice_id)?.text || '',
        choices: question.choices.map(c => c.text),
        userId: studentId,
      })
    } catch (error) {
      console.error('Error loading question:', error)
      setState('error')
    }
  }

  const handleChoiceSelect = (choiceId: string) => {
    if (state === 'question') {
      setSelectedChoice(choiceId)
    }
  }

  const handleSubmitAnswer = async () => {
    if (!currentQuestion || !selectedChoice || !currentQuestionId) return

    try {
      const timeTaken = Date.now() - startTime
      const response: StudentResponse = {
        question_id: currentQuestion.item_id,
        selected_choice: selectedChoice,
        time_taken: timeTaken
      }

      const result = await learningApi.submitAnswer(studentId, currentQuestion, response)
      setQuestionResult(result)
      setQuestionsAnswered(prev => prev + 1)
      if (result.correct) {
        setQuestionsCorrect(prev => prev + 1)
      }
      setState('feedback')

      // Log telemetry: question answered
      const selectedChoiceText = currentQuestion.choices.find(c => c.choice_id === selectedChoice)?.text || ''
      const correctAnswerText = currentQuestion.choices.find(c => c.choice_id === currentQuestion.solution_choice_id)?.text || ''

      logQuestionAnswered({
        sessionId,
        questionId: currentQuestionId,
        skillId: currentQuestion.skill_id,
        difficulty: currentQuestion.difficulty,
        studentAnswer: selectedChoiceText,
        correctAnswer: correctAnswerText,
        isCorrect: result.correct,
        timeToAnswerMs: timeTaken,
        userId: studentId,
      })

      // Check if we've exhausted all templates - if so, auto-complete quiz after feedback
      if (currentQuestion.pool_exhausted) {
        console.log('Pool exhausted - all templates have been seen')
      }
    } catch (error) {
      console.error('Error submitting answer:', error)
      setState('error')
    }
  }

  const handleNextQuestion = () => {
    loadNextQuestion()
  }

  const handleFinishQuiz = () => {
    // Log session summary before exiting
    const sessionDuration = Date.now() - sessionStartTime
    const avgTimePerQuestion = questionsAnswered > 0 ? sessionDuration / questionsAnswered : 0

    logSessionSummary({
      sessionId,
      totalQuestions: questionsAnswered,
      correctCount: questionsCorrect,
      accuracy: questionsAnswered > 0 ? questionsCorrect / questionsAnswered : 0,
      totalTimeMs: sessionDuration,
      avgTimePerQuestionMs: avgTimePerQuestion,
      skillsPracticed: Array.from(skillsPracticed),
      difficultyDistribution: difficultyCount,
      userId: studentId,
    })

    onComplete()
  }

  const formatTime = (ms: number) => {
    const seconds = Math.floor(ms / 1000)
    return `${seconds}s`
  }

  const renderExplanation = (explanation: string, isCorrect: boolean) => {
    // Parse and render markdown-style explanation
    const lines = explanation.split('\n')
    const elements: JSX.Element[] = []

    let currentSection: string[] = []
    let inCodeBlock = false

    const flushSection = () => {
      if (currentSection.length > 0) {
        const text = currentSection.join('\n')
        elements.push(
          <div key={elements.length} className="mb-2">
            {parseInlineFormatting(text, isCorrect)}
          </div>
        )
        currentSection = []
      }
    }

    lines.forEach((line, index) => {
      // Check for bold headers (lines starting with **)
      if (line.trim().startsWith('**') && line.trim().endsWith('**')) {
        flushSection()
        const headerText = line.replace(/\*\*/g, '').trim()
        const isMainHeader = headerText.includes('Step') || headerText.includes('solution') || headerText.includes('mistake')
        elements.push(
          <div key={elements.length} className={`font-semibold mt-3 mb-1 ${isMainHeader ? 'text-base' : 'text-sm'}`}>
            {headerText}
          </div>
        )
      }
      // Check for bullet points
      else if (line.trim().startsWith('•') || line.trim().startsWith('-')) {
        flushSection()
        const bulletText = line.replace(/^[•-]\s*/, '')
        elements.push(
          <div key={elements.length} className="ml-4 mb-1 flex items-start">
            <span className="mr-2">•</span>
            <span>{parseInlineFormatting(bulletText, isCorrect)}</span>
          </div>
        )
      }
      // Check for checkmarks and X marks
      else if (line.trim().startsWith('✓') || line.trim().startsWith('✗')) {
        flushSection()
        const isCheck = line.trim().startsWith('✓')
        elements.push(
          <div key={elements.length} className={`flex items-start mt-2 p-2 rounded ${isCheck ? 'bg-green-100' : 'bg-red-100'}`}>
            <span className="mr-2">{isCheck ? '✓' : '✗'}</span>
            <span className="font-medium">{parseInlineFormatting(line.substring(2), isCorrect)}</span>
          </div>
        )
      }
      // Regular text
      else if (line.trim()) {
        currentSection.push(line)
      }
      // Empty line - flush current section
      else {
        flushSection()
      }
    })

    flushSection()

    return <div>{elements}</div>
  }

  const parseInlineFormatting = (text: string, isCorrect: boolean) => {
    // Parse **bold** text
    const parts = text.split(/(\*\*[^*]+\*\*)/)
    return parts.map((part, index) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        const boldText = part.replace(/\*\*/g, '')
        return <strong key={index} className="font-semibold">{boldText}</strong>
      }
      return <span key={index}>{part}</span>
    })
  }

  if (state === 'loading') {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your next question...</p>
        </div>
      </div>
    )
  }

  if (state === 'error') {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center max-w-md">
          <XCircleIcon className="w-16 h-16 text-red-500 mx-auto mb-4" style={{width: '48px !important', height: '48px !important'}} />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Oops! Something went wrong</h2>
          <p className="text-gray-600 mb-6">We couldn't load your question. Let's try again.</p>
          <div className="space-x-4">
            <button
              onClick={loadNextQuestion}
              className="btn-primary"
            >
              Try Again
            </button>
            <button
              onClick={onExit}
              className="btn-secondary"
            >
              Exit Quiz
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (!currentQuestion) {
    return null
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-4 py-4">
        <div className="container mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <h1 className="text-lg font-semibold text-gray-900">
              {selectedSkill ? `${selectedSkill.replace(/\./g, ' ').replace('quad ', '').replace(/\b\w/g, l => l.toUpperCase())}` : 'Adaptive Quiz'}
            </h1>
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-500">
                Question {questionsAnswered + 1}
              </span>
              {currentQuestion.templates_remaining !== undefined && currentQuestion.templates_remaining >= 0 && (
                <span className="text-xs text-gray-400">
                  • {currentQuestion.templates_remaining + 1} in {currentQuestion.difficulty}
                </span>
              )}
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <div className="text-sm text-gray-600">
              {questionsCorrect}/{questionsAnswered} correct
            </div>
            {currentQuestion.pool_exhausted && (
              <div className="text-xs text-green-600 bg-green-50 px-3 py-1 rounded-full font-medium">
                ✓ Difficulty complete!
              </div>
            )}
            <button
              onClick={onExit}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <XMarkIcon className="icon-md" />
            </button>
          </div>
        </div>
      </div>

      {/* Question Content */}
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="question-card">
          {/* Question header */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-2">
              <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium capitalize">
                {currentQuestion.difficulty}
              </span>
              <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">
                {currentQuestion.skill_id.replace(/\./g, ' ').replace('quad ', '')}
              </span>
            </div>
            {state === 'question' && (
              <div className="flex items-center space-x-1 text-gray-500">
                <ClockIcon className="icon-sm" />
                <span className="text-sm">
                  {formatTime(Date.now() - startTime)}
                </span>
              </div>
            )}
          </div>

          {/* Question stem */}
          <div className="math-problem mb-8 text-lg">
            <SmartMathText>{currentQuestion.stem}</SmartMathText>
          </div>

          {/* Answer choices */}
          <div className="space-y-3 mb-8">
            {currentQuestion.choices.map((choice) => {
              let buttonClass = 'choice-button'
              
              if (state === 'feedback' && questionResult) {
                if (choice.id === questionResult.solution_choice_id) {
                  buttonClass += ' correct'
                } else if (choice.id === selectedChoice && !questionResult.correct) {
                  buttonClass += ' incorrect'
                }
              } else if (choice.id === selectedChoice) {
                buttonClass += ' selected'
              }

              return (
                <button
                  key={choice.id}
                  onClick={() => handleChoiceSelect(choice.id)}
                  disabled={state !== 'question'}
                  className={buttonClass}
                >
                  <div className="flex items-center space-x-3">
                    <span className="w-8 h-8 rounded-full border-2 border-current flex items-center justify-center font-semibold">
                      {choice.id}
                    </span>
                    <span className="math-choice flex-1">
                      <MathText>{choice.text}</MathText>
                    </span>
                  </div>
                </button>
              )
            })}
          </div>

          {/* Feedback section */}
          {state === 'feedback' && questionResult && (
            <div className={`p-6 rounded-lg mb-6 ${questionResult.correct ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
              <div className="flex items-start space-x-3">
                {questionResult.correct ? (
                  <CheckCircleIcon className="icon-md text-green-600 flex-shrink-0 mt-1" />
                ) : (
                  <XCircleIcon className="icon-md text-red-600 flex-shrink-0 mt-1" />
                )}
                <div className="flex-1">
                  <h3 className={`font-semibold mb-3 text-lg ${questionResult.correct ? 'text-green-800' : 'text-red-800'}`}>
                    {questionResult.correct ? 'Excellent work!' : 'Let\'s work through this together'}
                  </h3>
                  <div className={`prose prose-sm max-w-none ${questionResult.correct ? 'text-green-900' : 'text-red-900'}`}>
                    {renderExplanation(questionResult.explanation, questionResult.correct)}
                  </div>
                  <p className="text-xs text-gray-600 mt-3 pt-3 border-t border-gray-200">
                    Time taken: {formatTime(questionResult.time_taken)}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Action buttons */}
          <div className="flex justify-between">
            {state === 'question' ? (
              <>
                <button
                  onClick={onExit}
                  className="btn-secondary"
                >
                  Exit Quiz
                </button>
                <button
                  onClick={handleSubmitAnswer}
                  disabled={!selectedChoice}
                  className={`btn-primary ${!selectedChoice ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                  Submit Answer
                </button>
              </>
            ) : (
              <>
                {currentQuestion.pool_exhausted ? (
                  // Pool exhausted - show only "Complete Quiz" button
                  <button
                    onClick={handleFinishQuiz}
                    className="btn-primary w-full inline-flex items-center justify-center space-x-2"
                  >
                    <CheckCircleIcon className="w-5 h-5" />
                    <span>Complete Quiz - All Questions Answered!</span>
                  </button>
                ) : (
                  // Still have questions - show both buttons
                  <>
                    <button
                      onClick={handleFinishQuiz}
                      className="btn-secondary"
                    >
                      Finish Quiz
                    </button>
                    <button
                      onClick={handleNextQuestion}
                      className="btn-primary inline-flex items-center space-x-2"
                    >
                      <span>Next Question</span>
                      <ArrowRightIcon className="w-4 h-4" />
                    </button>
                  </>
                )}
              </>
            )}
          </div>
        </div>

        {/* Helpful tips */}
        {state === 'question' && (
          <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-start space-x-2">
              <LightBulbIcon className="icon-sm text-blue-600 flex-shrink-0 mt-0.5" />
              <div className="text-sm text-blue-800">
                <p className="font-medium mb-1">Tip:</p>
                <p>Take your time to read the question carefully. Look for key information and consider what mathematical concept is being tested.</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}