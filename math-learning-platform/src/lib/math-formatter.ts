/**
 * Converts plain text math notation to LaTeX for rendering with KaTeX
 *
 * Handles:
 * - x^2 → x² (superscripts)
 * - 3/2 → \frac{3}{2} (fractions)
 * - sqrt(...) → \sqrt{...}
 * - (x - 3)(x + 2) → proper formatting
 */

export function convertToLatex(text: string): string {
  let latex = text

  // Preserve spaces by using \text{} for regular text parts
  // Split into text and math components
  const parts: string[] = []
  let currentText = ''
  let inMath = false

  // First, protect spaces around words and punctuation
  latex = latex.replace(/([a-zA-Z]+)\s+([a-zA-Z]+)/g, (match, word1, word2) => {
    return `${word1}\\text{ }${word2}`
  })

  // Protect colon spacing
  latex = latex.replace(/:\s+/g, ':\\text{ }')

  // Protect spacing around equals signs in text context
  latex = latex.replace(/([a-zA-Z])\s*=\s*/g, '$1 = ')

  // Convert fractions: 3/2 → \frac{3}{2}
  // Handle various fraction formats including negative numbers and decimals
  latex = latex.replace(/(-?\d+\.?\d*)\/(-?\d+\.?\d*)/g, '\\frac{$1}{$2}')

  // Convert superscripts: x^2 → x^{2}, x^2.5 → x^{2.5}
  // Also handle parentheses in exponents: (x + 1)^2 → (x + 1)^{2}
  latex = latex.replace(/(\w|\))\^(\d+\.?\d*)/g, '$1^{$2}')

  // Convert sqrt(x) → \sqrt{x}
  latex = latex.replace(/sqrt\(([^)]+)\)/g, '\\sqrt{$1}')

  // Convert common symbols
  latex = latex.replace(/±/g, '\\pm')
  latex = latex.replace(/≤/g, '\\leq')
  latex = latex.replace(/≥/g, '\\geq')
  latex = latex.replace(/≠/g, '\\neq')
  latex = latex.replace(/×/g, '\\times')
  latex = latex.replace(/÷/g, '\\div')

  return latex
}

/**
 * Formats text containing math expressions by wrapping them in LaTeX delimiters
 *
 * Detects math expressions and wraps them appropriately for KaTeX rendering
 */
export function formatMathText(text: string): string {
  // If the text contains equation markers (y =, x =, etc.), treat entire text as math
  if (/[xy]\s*=|=\s*[0-9-]/.test(text)) {
    return convertToLatex(text)
  }

  // Otherwise, just convert inline math patterns
  return convertToLatex(text)
}

/**
 * Parses text and identifies inline math vs regular text
 * Returns array of segments with type information
 */
export function parseMathSegments(text: string): Array<{type: 'math' | 'text', content: string}> {
  const segments: Array<{type: 'math' | 'text', content: string}> = []

  // Split by common math delimiters while preserving them
  // Match patterns like: "y = x^2 + 3", "x = 3/2", equations, etc.
  const mathPattern = /([xy]\s*=\s*[^,;.!?]+|=\s*[0-9-][^,;.!?]*|\([^)]*\^[^)]*\)|[0-9]+\/[0-9]+|\w+\^[0-9]+)/g

  let lastIndex = 0
  let match: RegExpExecArray | null

  while ((match = mathPattern.exec(text)) !== null) {
    // Add text before the match
    if (match.index > lastIndex) {
      segments.push({
        type: 'text',
        content: text.substring(lastIndex, match.index)
      })
    }

    // Add the math match
    segments.push({
      type: 'math',
      content: match[0]
    })

    lastIndex = match.index + match[0].length
  }

  // Add remaining text
  if (lastIndex < text.length) {
    segments.push({
      type: 'text',
      content: text.substring(lastIndex)
    })
  }

  // If no math was found, return entire text as math if it looks like an equation
  if (segments.length === 0 || (segments.length === 1 && segments[0].type === 'text')) {
    if (/[xy]|[0-9]+\/[0-9]+|\^/.test(text)) {
      return [{type: 'math', content: text}]
    }
  }

  return segments.length > 0 ? segments : [{type: 'text', content: text}]
}
