#!/usr/bin/env python3
"""
Test script for generating quadratic equation practice problems.

Usage:
    python3 test_quadratics_completing_the_square.py <template_number>

Where template_number is between 1 and 24.

Example:
    python3 test_quadratics_completing_the_square.py 9
"""

import sys
import os

# Add the code directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

import quadratics_completing_the_square as qe


def display_question(equation, choices):
    """
    Display the equation and multiple choice options in a formatted way.

    Args:
        equation: The equation string to display
        choices: List of 4 choice strings [A, B, C, D]
    """
    print()
    print("=" * 60)
    print("Solve by completing the square:")
    print()
    print(f"  {equation}")
    print()
    print("Multiple Choice Options:")
    print(f"  A) {choices[0]}")
    print(f"  B) {choices[1]}")
    print(f"  C) {choices[2]}")
    print(f"  D) {choices[3]}")
    print("=" * 60)
    print()


def main():
    """
    Main function to run the test script.
    Accepts template number as command line argument.
    """
    # Check if template number was provided
    if len(sys.argv) != 2:
        print("Usage: python3 test_quadratics_completing_the_square.py <template_number>")
        print("Example: python3 test_quadratics_completing_the_square.py 9")
        print()
        print("Template numbers range from 1 to 24")
        sys.exit(1)

    # Parse template number
    try:
        template_num = int(sys.argv[1])
    except ValueError:
        print(f"Error: '{sys.argv[1]}' is not a valid number")
        print("Template number must be an integer between 1 and 24")
        sys.exit(1)

    # Validate template number range
    if template_num < 1 or template_num > 24:
        print(f"Error: Template number {template_num} is out of range")
        print("Template number must be between 1 and 24")
        sys.exit(1)

    # Get the corresponding template function
    template_function_name = f"template_{template_num}"
    template_function = getattr(qe, template_function_name)

    # Generate the question
    equation, correct_letter, choices = template_function()

    # Display the question
    display_question(equation, choices)

    # Show correct answer (for debugging/verification)
    print(f"[Debug] Correct answer: {correct_letter}")
    print()


if __name__ == "__main__":
    main()
