"""
Validation utility functions for Novel Agent Infrastructure.

This module provides validation utilities.
"""

from typing import Optional, List, Tuple


def validate_title(title: str, min_length: int = 2, max_length: int = 200) -> Tuple[bool, Optional[str]]:
    """Validate a story title.

    Args:
        title: Title to validate
        min_length: Minimum title length
        max_length: Maximum title length

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not title or not title.strip():
        return False, "Title cannot be empty"

    title = title.strip()

    if len(title) < min_length:
        return False, f"Title too short (minimum {min_length} characters)"

    if len(title) > max_length:
        return False, f"Title too long (maximum {max_length} characters)"

    return True, None


def validate_genre(genre: str, valid_genres: Optional[List[str]] = None) -> Tuple[bool, Optional[str]]:
    """Validate a story genre.

    Args:
        genre: Genre to validate
        valid_genres: Optional list of valid genres

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not genre or not genre.strip():
        return False, "Genre cannot be empty"

    genre = genre.strip().lower()

    if valid_genres and genre not in valid_genres:
        return False, f"Invalid genre: {genre}. Valid genres: {', '.join(valid_genres)}"

    return True, None


def validate_platform(platform: str) -> Tuple[bool, Optional[str]]:
    """Validate a platform name.

    Args:
        platform: Platform to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    valid_platforms = [
        "tomato",
        "qidian",
        "qimao",
        "royalroad",
        "wattpad",
        "ao3",
        "scribblehub",
    ]

    if not platform or not platform.strip():
        return False, "Platform cannot be empty"

    platform = platform.strip().lower()

    if platform not in valid_platforms:
        return False, f"Invalid platform: {platform}. Valid platforms: {', '.join(valid_platforms)}"

    return True, None


def validate_chapter_number(chapter_number: int) -> Tuple[bool, Optional[str]]:
    """Validate a chapter number.

    Args:
        chapter_number: Chapter number to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if chapter_number < 1:
        return False, "Chapter number must be positive"

    return True, None


def validate_word_count(word_count: int, min_words: int = 100, max_words: int = 10000) -> Tuple[bool, Optional[str]]:
    """Validate word count.

    Args:
        word_count: Word count to validate
        min_words: Minimum word count
        max_words: Maximum word count

    Returns:
        Tuple of (is_valid, error_message)
    """
    if word_count < min_words:
        return False, f"Word count too low (minimum {min_words} words)"

    if word_count > max_words:
        return False, f"Word count too high (maximum {max_words} words)"

    return True, None
