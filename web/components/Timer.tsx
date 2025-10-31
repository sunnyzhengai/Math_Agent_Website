'use client'

interface TimerProps {
  seconds: number
  warning?: boolean
}

/**
 * Timer Component
 * 
 * Displays remaining time in MM:SS format.
 * Changes color based on warning state.
 */
export default function Timer({ seconds, warning = false }: TimerProps) {
  const minutes = Math.floor(seconds / 60)
  const secs = seconds % 60
  const displaySeconds = secs.toString().padStart(2, '0')

  return (
    <div className={`font-mono text-lg font-semibold ${warning ? 'text-red-600' : 'text-gray-600'}`}>
      {minutes}:{displaySeconds}
    </div>
  )
}
