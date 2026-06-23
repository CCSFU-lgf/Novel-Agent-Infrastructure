"""
Text utility functions for Novel Agent Infrastructure.

This module provides text processing utilities.
"""

import re
from typing import List, Optional


def count_words(text: str) -> int:
    """Count words in text.

    Args:
        text: Text to count words in

    Returns:
        Number of words
    """
    # Handle both English and Chinese text
    # For Chinese, count characters
    chinese_chars = len(re.findall(r'[一-鿿]', text))

    # For English, count space-separated words
    english_words = len(re.findall(r'[a-zA-Z]+', text))

    # Chinese characters are roughly equivalent to words
    return chinese_chars + english_words


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def clean_text(text: str) -> str:
    """Clean text by removing extra whitespace and special characters.

    Args:
        text: Text to clean

    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)

    # Remove control characters
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)

    return text.strip()


def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """Extract keywords from text.

    Args:
        text: Text to extract keywords from
        max_keywords: Maximum number of keywords

    Returns:
        List of keywords
    """
    # Simple keyword extraction based on word frequency
    # For production, use NLP libraries like spaCy or NLTK

    # Convert to lowercase
    text_lower = text.lower()

    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
        'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these',
        'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him',
        'her', 'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their',
    }

    # Extract words
    words = re.findall(r'[a-zA-Z]+', text_lower)

    # Filter stop words and short words
    keywords = [w for w in words if w not in stop_words and len(w) > 2]

    # Count frequency
    word_freq = {}
    for word in keywords:
        word_freq[word] = word_freq.get(word, 0) + 1

    # Sort by frequency
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

    return [word for word, freq in sorted_words[:max_keywords]]


def has_chinese(text: str) -> bool:
    """Check if text contains Chinese characters.

    Args:
        text: Text to check

    Returns:
        True if text contains Chinese characters
    """
    return bool(re.search(r'[一-鿿]', text))


def is_chinese(text: str) -> bool:
    """Check if text is primarily Chinese.

    Args:
        text: Text to check

    Returns:
        True if text is primarily Chinese
    """
    chinese_chars = len(re.findall(r'[一-鿿]', text))
    total_chars = len(text)

    if total_chars == 0:
        return False

    return chinese_chars / total_chars > 0.5
