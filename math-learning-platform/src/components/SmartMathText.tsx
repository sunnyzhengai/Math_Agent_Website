'use client'

import { useEffect, useRef } from 'react'
import katex from 'katex'
import 'katex/dist/katex.min.css'

interface SmartMathTextProps {
  children: string
  className?: string
}

/**
 * Intelligently renders text with math notation
 *
 * Separates regular text from math expressions so that:
 * - Regular text keeps normal spacing and formatting
 * - Only math expressions are rendered with KaTeX
 *
 * Example: "Solve by factoring: x^2 + 5x + 6 = 0"
 * - "Solve by factoring: " → regular text
 * - "x^2 + 5x + 6 = 0" → KaTeX math
 */
export default function SmartMathText({ children, className = '' }: SmartMathTextProps) {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!containerRef.current) return

    try {
      // Clear previous content
      containerRef.current.innerHTML = ''

      // Pattern to detect math expressions
      // Matches: equations (y = ..., x = ...), expressions with ^, fractions with /, etc.
      const mathPattern = /([xy]\s*=\s*[^.,;!?]+|=\s*[0-9-][^.,;!?]*|[\w()]+\^[\d.]+|[\d.]+\/[\d.]+|\([^)]*\^[^)]*\))/g

      let lastIndex = 0
      let match: RegExpExecArray | null
      const tempDiv = document.createElement('div')

      // Find all math expressions
      const matches: Array<{start: number, end: number, text: string}> = []
      while ((match = mathPattern.exec(children)) !== null) {
        matches.push({
          start: match.index,
          end: match.index + match[0].length,
          text: match[0]
        })
      }

      // If no math found, render as plain text
      if (matches.length === 0) {
        containerRef.current.textContent = children
        return
      }

      // Build the mixed content
      lastIndex = 0
      matches.forEach((match, index) => {
        // Add text before this math expression
        if (match.start > lastIndex) {
          const textBefore = children.substring(lastIndex, match.start)
          const textNode = document.createTextNode(textBefore)
          tempDiv.appendChild(textNode)
        }

        // Add the math expression rendered with KaTeX
        const mathSpan = document.createElement('span')
        mathSpan.style.display = 'inline'

        try {
          // Convert simple notation to LaTeX
          let latex = match.text
          // Convert x^2 to x^{2}
          latex = latex.replace(/(\w|\))\^([\d.]+)/g, '$1^{$2}')
          // Convert fractions
          latex = latex.replace(/([\d.]+)\/([\d.]+)/g, '\\frac{$1}{$2}')

          katex.render(latex, mathSpan, {
            displayMode: false,
            throwOnError: false,
            output: 'html',
            trust: false,
          })
        } catch (e) {
          // If KaTeX fails, just show the text
          mathSpan.textContent = match.text
        }

        tempDiv.appendChild(mathSpan)
        lastIndex = match.end
      })

      // Add any remaining text after the last math expression
      if (lastIndex < children.length) {
        const textAfter = children.substring(lastIndex)
        const textNode = document.createTextNode(textAfter)
        tempDiv.appendChild(textNode)
      }

      // Move all content to the container
      containerRef.current.appendChild(tempDiv)

    } catch (error) {
      console.warn('Smart math rendering error:', error)
      // Fallback to plain text
      if (containerRef.current) {
        containerRef.current.textContent = children
      }
    }
  }, [children])

  return <div ref={containerRef} className={`inline ${className}`} />
}
