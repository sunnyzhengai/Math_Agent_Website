#!/usr/bin/env python3
"""
Test script for operations with radicals templates

Usage: python3 tests/test_operations_with_radicals.py <template_number>
"""

import sys
import os

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

try:
    import operations_with_radicals as opr
except ImportError:
    print("Error: Could not import operations_with_radicals.py")
    print("Make sure the file exists in the code/ directory")
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 tests/test_operations_with_radicals.py <template_number>")
        print("Example: python3 tests/test_operations_with_radicals.py 1")
        sys.exit(1)

    try:
        template_num = int(sys.argv[1])
        if template_num < 1 or template_num > 4:
            print("Error: Template number must be between 1 and 4")
            sys.exit(1)
    except ValueError:
        print("Error: Template number must be an integer")
        sys.exit(1)

    # Get the template function
    template_func = getattr(opr, f'template_{template_num}')

    # Generate question
    question, correct_letter, choices = template_func()

    # Display formatted output
    print("=" * 60)
    print("Simplify:")
    print()
    print(f"  {question}")
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
