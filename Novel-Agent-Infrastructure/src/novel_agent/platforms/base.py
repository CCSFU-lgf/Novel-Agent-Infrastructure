"""
Base platform adapter with common functionality.

This module provides a base class with shared logic for all platform adapters.
"""

from typing import Optional, Dict, Any, List
from abc import abstractmethod

from novel_agent.core.platform import (
    Platform,
    PlatformType,
    TitleValidationResult,
    Genre,
    Tag,
    Chapter,
    StoryMetadata,
)


class BasePlatform(Platform):
    """Base class for platform adapters with common functionality."""

    def _initialize(self) -> None:
        """Initialize base platform resources."""
        self.api_key = self.config.get("api_key")
        self.base_url = self.config.get("base_url")
        self.timeout = self.config.get("timeout", 30)
        self._genres_cache: Optional[List[Genre]] = None
        self._tags_cache: Dict[str, List[Tag]] = {}

    def validate_title(self, title: str) -> TitleValidationResult:
        """Validate title with common rules.

        Args:
            title: Title to validate

        Returns:
            TitleValidationResult
        """
        errors = []
        suggestions = []

        # Common validation rules
        if len(title) < 2:
            errors.append("Title too short (minimum 2 characters)")
        if len(title) > 200:
            errors.append("Title too long (maximum 200 characters)")

        # Platform-specific validation
        platform_result = self._validate_title_platform(title)
        if platform_result and not platform_result.is_valid:
            errors.extend(platform_result.suggestions or [])

        is_valid = len(errors) == 0
        message = "; ".join(errors) if errors else "Title is valid"

        return TitleValidationResult(
            is_valid=is_valid,
            title=title,
            suggestions=suggestions,
            message=message,
        )

    @abstractmethod
    def _validate_title_platform(self, title: str) -> Optional[TitleValidationResult]:
        """Platform-specific title validation.

        Args:
            title: Title to validate

        Returns:
            TitleValidationResult if platform has specific rules, None otherwise
        """
        pass

    def get_genres(self, language: str = "en") -> List[Genre]:
        """Get genres with caching.

        Args:
            language: Language code

        Returns:
            List of genres
        """
        if self._genres_cache is None:
            self._genres_cache = self._fetch_genres(language)
        return self._genres_cache

    @abstractmethod
    def _fetch_genres(self, language: str) -> List[Genre]:
        """Fetch genres from platform.

        Args:
            language: Language code

        Returns:
            List of genres
        """
        pass

    def get_tags(self, genre: Optional[str] = None) -> List[Tag]:
        """Get tags with caching.

        Args:
            genre: Optional genre filter

        Returns:
            List of tags
        """
        cache_key = genre or "__all__"
        if cache_key not in self._tags_cache:
            self._tags_cache[cache_key] = self._fetch_tags(genre)
        return self._tags_cache[cache_key]

    @abstractmethod
    def _fetch_tags(self, genre: Optional[str]) -> List[Tag]:
        """Fetch tags from platform.

        Args:
            genre: Optional genre filter

        Returns:
            List of tags
        """
        pass

    def analyze_market(self, genre: str, tags: List[str]) -> Dict[str, Any]:
        """Analyze market with common structure.

        Args:
            genre: Genre to analyze
            tags: Tags to analyze

        Returns:
            Market analysis data
        """
        # Get platform-specific analysis
        platform_analysis = self._analyze_market_platform(genre, tags)

        # Enhance with common analysis
        return {
            "genre": genre,
            "tags": tags,
            "platform": self._get_platform_name(),
            "competition_level": platform_analysis.get("competition_level", "medium"),
            "reader_demand": platform_analysis.get("reader_demand", "medium"),
            "monetization_potential": platform_analysis.get("monetization_potential", "medium"),
            "recommended_tags": platform_analysis.get("recommended_tags", []),
            "similar_stories": platform_analysis.get("similar_stories", []),
            "market_size": platform_analysis.get("market_size", "unknown"),
            "growth_trend": platform_analysis.get("growth_trend", "stable"),
        }

    @abstractmethod
    def _analyze_market_platform(self, genre: str, tags: List[str]) -> Dict[str, Any]:
        """Platform-specific market analysis.

        Args:
            genre: Genre to analyze
            tags: Tags to analyze

        Returns:
            Platform-specific market analysis
        """
        pass

    @abstractmethod
    def _get_platform_name(self) -> str:
        """Get platform name.

        Returns:
            Platform name
        """
        pass

    def get_trending(self, limit: int = 10) -> List[StoryMetadata]:
        """Get trending stories with limit.

        Args:
            limit: Maximum number of stories

        Returns:
            List of trending stories
        """
        return self._fetch_trending(limit)

    @abstractmethod
    def _fetch_trending(self, limit: int) -> List[StoryMetadata]:
        """Fetch trending stories from platform.

        Args:
            limit: Maximum number of stories

        Returns:
            List of trending stories
        """
        pass

    def publish_chapter(self, story_id: str, chapter: Chapter) -> bool:
        """Publish chapter with validation.

        Args:
            story_id: Story ID
            chapter: Chapter to publish

        Returns:
            True if successful
        """
        # Validate chapter
        if not chapter.content:
            return False

        if chapter.word_count < 100:
            # Most platforms require minimum word count
            pass

        return self._publish_chapter_platform(story_id, chapter)

    @abstractmethod
    def _publish_chapter_platform(self, story_id: str, chapter: Chapter) -> bool:
        """Platform-specific chapter publishing.

        Args:
            story_id: Story ID
            chapter: Chapter to publish

        Returns:
            True if successful
        """
        pass

    def get_story_metadata(self, story_id: str) -> StoryMetadata:
        """Get story metadata.

        Args:
            story_id: Story ID

        Returns:
            Story metadata
        """
        return self._fetch_story_metadata(story_id)

    @abstractmethod
    def _fetch_story_metadata(self, story_id: str) -> StoryMetadata:
        """Fetch story metadata from platform.

        Args:
            story_id: Story ID

        Returns:
            Story metadata
        """
        pass

    def get_chapters(self, story_id: str, limit: int = 100) -> List[Chapter]:
        """Get chapters with limit.

        Args:
            story_id: Story ID
            limit: Maximum chapters

        Returns:
            List of chapters
        """
        return self._fetch_chapters(story_id, limit)

    @abstractmethod
    def _fetch_chapters(self, story_id: str, limit: int) -> List[Chapter]:
        """Fetch chapters from platform.

        Args:
            story_id: Story ID
            limit: Maximum chapters

        Returns:
            List of chapters
        """
        pass
