#!/usr/bin/env python3
"""
Test script for solving equations with square roots templates

Usage: python3 tests/test_solving_with_square_roots.py <template_number>
"""

import sys
import os

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

try:
    import solving_with_square_roots as swr
except ImportError:
    print("Error: Could not import solving_with_square_roots.py")
    print("Make sure the file exists in the code/ directory")
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 tests/test_solving_with_square_roots.py <template_number>")
        print("Example: python3 tests/test_solving_with_square_roots.py 1")
        sys.exit(1)

    try:
        template_num = int(sys.argv[1])
        if template_num < 1 or template_num > 8:
            print("Error: Template number must be between 1 and 8")
            sys.exit(1)
    except ValueError:
        print("Error: Template number must be an integer")
        sys.exit(1)

    # Get the template function
    template_func = getattr(swr, f'template_{template_num}')

    # Generate question
    equation, correct_letter, choices = template_func()

    # Display formatted output
    print("=" * 60)
    print("Solve the equation:")
    print()
    print(f"  {equation}")
    print()
    print("Multiple Choice Options:")
    for i, choice in enumerate(choices):
        letter = chr(65 + i)  # A, B, C, D
        print(f"  {letter}) {choice}")
    print("=" * 60)
    print()
    print(f"[Debug] Correct answer: {correct_letter}")


if __name__ == "__main__":
    main()
