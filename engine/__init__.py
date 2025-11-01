"""
Math Agent Engine — Core item generation and validation.

Public API:
- generate_item: Generate a math question item
- validate_item: Validate item structure
"""

from .templates import generate_item
from .validators import validate_item

__all__ = ["generate_item", "validate_item"]
