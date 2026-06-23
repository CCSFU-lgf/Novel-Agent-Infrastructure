"""
Utility functions for Novel Agent Infrastructure.

This module provides common utility functions used throughout the system.
"""

from novel_agent.utils.text import (
    count_words,
    truncate_text,
    clean_text,
    extract_keywords,
)
from novel_agent.utils.validation import (
    validate_title,
    validate_genre,
    validate_platform,
)

__all__ = [
    "count_words",
    "truncate_text",
    "clean_text",
    "extract_keywords",
    "validate_title",
    "validate_genre",
    "validate_platform",
]
