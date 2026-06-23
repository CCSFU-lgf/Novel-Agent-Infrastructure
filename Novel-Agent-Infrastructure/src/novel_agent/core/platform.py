"""
Platform abstraction layer for Novel Agent Infrastructure.

This module provides a unified interface for interacting with different
fiction publishing platforms (Tomato Novel, Qidian, Royal Road, etc.).

Example:
    >>> from novel_agent.core.platform import Platform, PlatformType
    >>> platform = Platform.create(PlatformType.TOMATO)
    >>> platform.validate_title("My Story Title")
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class PlatformType(str, Enum):
    """Supported platform types."""

    # Chinese platforms
    TOMATO = "tomato"  # 番茄小说
    QIDIAN = "qidian"  # 起点中文网
    QIMAO = "qimao"    # 七猫

    # International platforms
    ROYALROAD = "royalroad"
    WATTPAD = "wattpad"
    AO3 = "ao3"        # Archive of Our Own
    SCRIBBLEHUB = "scribblehub"


class TitleValidationResult(BaseModel):
    """Result of title validation."""

    is_valid: bool
    title: str
    suggestions: List[str] = Field(default_factory=list)
    platform_specific: Dict[str, Any] = Field(default_factory=dict)
    message: Optional[str] = None


class Genre(BaseModel):
    """Genre representation."""

    id: str
    name: str
    name_en: str
    name_zh: Optional[str] = None
    description: Optional[str] = None
    subgenres: List["Genre"] = Field(default_factory=list)


class Tag(BaseModel):
    """Tag representation."""

    id: str
    name: str
    name_en: str
    name_zh: Optional[str] = None
    category: Optional[str] = None
    popularity: int = 0


class Chapter(BaseModel):
    """Chapter representation."""

    id: str
    title: str
    content: str
    word_count: int
    chapter_number: int
    published_at: Optional[str] = None
    platform_data: Dict[str, Any] = Field(default_factory=dict)


class StoryMetadata(BaseModel):
    """Story metadata from platform."""

    id: str
    title: str
    author: str
    description: Optional[str] = None
    genre: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    word_count: int = 0
    chapter_count: int = 0
    status: str = "ongoing"  # ongoing, completed, hiatus
    platform: PlatformType
    platform_data: Dict[str, Any] = Field(default_factory=dict)


class Platform(ABC):
    """Abstract base class for platform adapters."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize platform adapter.

        Args:
            config: Platform-specific configuration
        """
        self.config = config or {}
        self._initialize()

    @abstractmethod
    def _initialize(self) -> None:
        """Initialize platform-specific resources."""
        pass

    @abstractmethod
    def validate_title(self, title: str) -> TitleValidationResult:
        """Validate a story title for this platform.

        Args:
            title: The title to validate

        Returns:
            TitleValidationResult with validation details
        """
        pass

    @abstractmethod
    def get_genres(self, language: str = "en") -> List[Genre]:
        """Get available genres for this platform.

        Args:
            language: Language code (en, zh, etc.)

        Returns:
            List of available genres
        """
        pass

    @abstractmethod
    def get_tags(self, genre: Optional[str] = None) -> List[Tag]:
        """Get available tags for this platform.

        Args:
            genre: Optional genre to filter tags

        Returns:
            List of available tags
        """
        pass

    @abstractmethod
    def analyze_market(self, genre: str, tags: List[str]) -> Dict[str, Any]:
        """Analyze market for given genre and tags.

        Args:
            genre: Genre to analyze
            tags: Tags to analyze

        Returns:
            Market analysis data
        """
        pass

    @abstractmethod
    def get_trending(self, limit: int = 10) -> List[StoryMetadata]:
        """Get trending stories on this platform.

        Args:
            limit: Maximum number of stories to return

        Returns:
            List of trending story metadata
        """
        pass

    @abstractmethod
    def publish_chapter(self, story_id: str, chapter: Chapter) -> bool:
        """Publish a chapter to this platform.

        Args:
            story_id: Platform-specific story ID
            chapter: Chapter to publish

        Returns:
            True if successful
        """
        pass

    @abstractmethod
    def get_story_metadata(self, story_id: str) -> StoryMetadata:
        """Get story metadata from platform.

        Args:
            story_id: Platform-specific story ID

        Returns:
            Story metadata
        """
        pass

    @abstractmethod
    def get_chapters(self, story_id: str, limit: int = 100) -> List[Chapter]:
        """Get chapters from a story.

        Args:
            story_id: Platform-specific story ID
            limit: Maximum number of chapters to return

        Returns:
            List of chapters
        """
        pass

    @classmethod
    def create(cls, platform_type: PlatformType, config: Optional[Dict[str, Any]] = None) -> "Platform":
        """Create a platform adapter instance.

        Args:
            platform_type: Type of platform to create
            config: Platform-specific configuration

        Returns:
            Platform adapter instance

        Raises:
            ValueError: If platform type is not supported
        """
        from novel_agent.platforms import get_platform_class

        platform_class = get_platform_class(platform_type)
        return platform_class(config)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
