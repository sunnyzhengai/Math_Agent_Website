'use client'

import { useEffect, useRef } from 'react'
import katex from 'katex'
import 'katex/dist/katex.min.css'
import { convertToLatex } from '@/lib/math-formatter'

interface MathTextProps {
  children: string
  className?: string
  displayMode?: boolean  // true for block display, false for inline
}

/**
 * Renders mathematical notation using KaTeX
 *
 * Automatically converts plain text notation to LaTeX:
 * - x^2 → x² (superscripts)
 * - 3/2 → proper fractions
 * - y = x^2 + 3x - 5 → properly formatted equation
 */
export default function MathText({ children, className = '', displayMode = false }: MathTextProps) {
  const containerRef = useRef<HTMLSpanElement>(null)

  useEffect(() => {
    if (!containerRef.current) return

    try {
      // Convert plain text math to LaTeX
      const latex = convertToLatex(children)

      // Render with KaTeX
      katex.render(latex, containerRef.current, {
        displayMode,  // Block vs inline rendering
        throwOnError: false,  // Don't crash on invalid LaTeX
        output: 'html',
        trust: false,  // Security: don't allow arbitrary commands
        strict: false,  // Be lenient with syntax
      })
    } catch (error) {
      // If KaTeX rendering fails, show the original text
      console.warn('KaTeX rendering error:', error)
      if (containerRef.current) {
        containerRef.current.textContent = children
      }
    }
  }, [children, displayMode])

  return <span ref={containerRef} className={className} />
}
