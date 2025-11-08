/**
 * Telemetry client for logging student interactions.
 * 
 * This enables the data flywheel - we learn from real student behavior
 * to continuously improve question quality.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface TelemetryEvent {
  event_type: 'question_presented' | 'question_answered' | 'session_summary';
  timestamp: string;
  session_id: string;
  user_id?: string;
  question_id?: string;
  skill_id?: string;
  difficulty?: string;
  generation_method?: string;
  parameters?: Record<string, any>;
  question_stem?: string;
  correct_answer?: string;
  choices?: string[];
  distractor_types?: (string | null)[];
  student_answer?: string;
  is_correct?: boolean;
  distractor_type_chosen?: string;
  time_to_answer_ms?: number;
  attempt_number?: number;
  // Session summary fields
  total_questions?: number;
  correct_count?: number;
  accuracy?: number;
  total_time_ms?: number;
  avg_time_per_question_ms?: number;
  skills_practiced?: string[];
  difficulty_distribution?: Record<string, number>;
}

/**
 * Log a telemetry event.
 * Fails gracefully - telemetry errors don't break the user experience.
 */
export async function logTelemetryEvent(event: TelemetryEvent): Promise<void> {
  try {
    const response = await fetch(`${API_BASE_URL}/telemetry/log`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(event),
    });

    if (!response.ok) {
      console.warn('Telemetry logging failed:', response.status);
    }
  } catch (error) {
    // Fail silently - don't break user experience for telemetry
    console.warn('Telemetry error:', error);
  }
}

/**
 * Log when a question is presented to the student.
 */
export function logQuestionPresented(params: {
  sessionId: string;
  questionId: string;
  skillId: string;
  difficulty: string;
  generationMethod: string;
  parameters?: Record<string, any>;
  questionStem: string;
  correctAnswer: string;
  choices: string[];
  distractorTypes?: (string | null)[];
  userId?: string;
}): void {
  logTelemetryEvent({
    event_type: 'question_presented',
    timestamp: new Date().toISOString(),
    session_id: params.sessionId,
    user_id: params.userId,
    question_id: params.questionId,
    skill_id: params.skillId,
    difficulty: params.difficulty,
    generation_method: params.generationMethod,
    parameters: params.parameters,
    question_stem: params.questionStem,
    correct_answer: params.correctAnswer,
    choices: params.choices,
    distractor_types: params.distractorTypes,
  });
}

/**
 * Log when a student answers a question.
 */
export function logQuestionAnswered(params: {
  sessionId: string;
  questionId: string;
  skillId: string;
  difficulty: string;
  studentAnswer: string;
  correctAnswer: string;
  isCorrect: boolean;
  distractorTypeChosen?: string;
  timeToAnswerMs: number;
  attemptNumber?: number;
  userId?: string;
}): void {
  logTelemetryEvent({
    event_type: 'question_answered',
    timestamp: new Date().toISOString(),
    session_id: params.sessionId,
    user_id: params.userId,
    question_id: params.questionId,
    skill_id: params.skillId,
    difficulty: params.difficulty,
    student_answer: params.studentAnswer,
    correct_answer: params.correctAnswer,
    is_correct: params.isCorrect,
    distractor_type_chosen: params.distractorTypeChosen,
    time_to_answer_ms: params.timeToAnswerMs,
    attempt_number: params.attemptNumber || 1,
  });
}

/**
 * Log session summary when practice session completes.
 */
export function logSessionSummary(params: {
  sessionId: string;
  totalQuestions: number;
  correctCount: number;
  accuracy: number;
  totalTimeMs: number;
  avgTimePerQuestionMs: number;
  skillsPracticed: string[];
  difficultyDistribution: Record<string, number>;
  userId?: string;
}): void {
  logTelemetryEvent({
    event_type: 'session_summary',
    timestamp: new Date().toISOString(),
    session_id: params.sessionId,
    user_id: params.userId,
    total_questions: params.totalQuestions,
    correct_count: params.correctCount,
    accuracy: params.accuracy,
    total_time_ms: params.totalTimeMs,
    avg_time_per_question_ms: params.avgTimePerQuestionMs,
    skills_practiced: params.skillsPracticed,
    difficulty_distribution: params.difficultyDistribution,
  });
}

/**
 * Generate a unique session ID.
 */
export function generateSessionId(): string {
  const timestamp = Date.now();
  const random = Math.random().toString(36).substring(2, 9);
  return `session_${timestamp}_${random}`;
}

/**
 * Generate a unique question ID.
 */
export function generateQuestionId(): string {
  const timestamp = Date.now();
  const random = Math.random().toString(36).substring(2, 9);
  return `q_${timestamp}_${random}`;
}
