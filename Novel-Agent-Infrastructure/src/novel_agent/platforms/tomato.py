"""
Tomato Novel (番茄小说) platform adapter.

This module provides integration with Tomato Novel, a popular Chinese
fiction platform owned by ByteDance.

Features:
- Title validation with Chinese-specific rules
- Genre and tag support for Chinese web novels
- Market analysis for Chinese fiction trends
- Chapter publishing and management
"""

from typing import Optional, Dict, Any, List

from novel_agent.core.platform import (
    PlatformType,
    TitleValidationResult,
    Genre,
    Tag,
    Chapter,
    StoryMetadata,
)
from novel_agent.platforms.base import BasePlatform


# Tomato Novel specific genres
TOMATO_GENRES = [
    Genre(id="urban", name="都市", name_en="Urban", name_zh="都市"),
    Genre(id="fantasy", name="玄幻", name_en="Fantasy", name_zh="玄幻"),
    Genre(id="xianxia", name="仙侠", name_en="Xianxia", name_zh="仙侠"),
    Genre(id="scifi", name="科幻", name_en="Sci-Fi", name_zh="科幻"),
    Genre(id="mystery", name="悬疑", name_en="Mystery", name_zh="悬疑"),
    Genre(id="romance", name="言情", name_en="Romance", name_zh="言情"),
    Genre(id="history", name="历史", name_en="Historical", name_zh="历史"),
    Genre(id="military", name="军事", name_en="Military", name_zh="军事"),
    Genre(id="game", name="游戏", name_en="Game", name_zh="游戏"),
    Genre(id="sports", name="体育", name_en="Sports", name_zh="体育"),
    Genre(id="horror", name="恐怖", name_en="Horror", name_zh="恐怖"),
    Genre(id="short_story", name="短篇", name_en="Short Story", name_zh="短篇"),
]

# Tomato Novel specific tags
TOMATO_TAGS = [
    Tag(id="system", name="系统", name_en="System", name_zh="系统", category="theme"),
    Tag(id="rebirth", name="重生", name_en="Rebirth", name_zh="重生", category="theme"),
    Tag(id="transmigration", name="穿越", name_en="Transmigration", name_zh="穿越", category="theme"),
    Tag(id="face_slapping", name="打脸", name_en="Face Slapping", name_zh="打脸", category="theme"),
    Tag(id="strong_male", name="强势男主", name_en="Strong Male Lead", name_zh="强势男主", category="character"),
    Tag(id="strong_female", name="强势女主", name_en="Strong Female Lead", name_zh="强势女主", category="character"),
    Tag(id="genius", name="天才", name_en="Genius", name_zh="天才", category="character"),
    Tag(id="cultivation", name="修炼", name_en="Cultivation", name_zh="修炼", category="theme"),
    Tag(id="martial_arts", name="武侠", name_en="Martial Arts", name_zh="武侠", category="theme"),
    Tag(id="harem", name="后宫", name_en="Harem", name_zh="后宫", category="theme"),
    Tag(id="no_harem", name="无后宫", name_en="No Harem", name_zh="无后宫", category="theme"),
    Tag(id="comedy", name="轻松", name_en="Comedy", name_zh="轻松", category="tone"),
    Tag(id="dark", name="暗黑", name_en="Dark", name_zh="暗黑", category="tone"),
]


class TomatoPlatform(BasePlatform):
    """Tomato Novel platform adapter."""

    def _initialize(self) -> None:
        """Initialize Tomato Novel platform."""
        super()._initialize()
        self.platform_type = PlatformType.TOMATO
        self.base_url = self.config.get("base_url", "https://fanqienovel.com")

    def _validate_title_platform(self, title: str) -> Optional[TitleValidationResult]:
        """Validate title for Tomato Novel.

        Args:
            title: Title to validate

        Returns:
            TitleValidationResult if validation fails, None otherwise
        """
        errors = []
        suggestions = []

        # Check for Chinese characters (preferred)
        has_chinese = any('一' <= char <= '鿿' for char in title)
        if not has_chinese:
            suggestions.append("Consider adding Chinese characters for better discoverability")

        # Check for sensitive words
        sensitive_words = ["政治", "色情", "暴力", "赌博"]
        for word in sensitive_words:
            if word in title:
                errors.append(f"Title contains sensitive word: {word}")

        # Check length (Chinese platforms prefer shorter titles)
        if len(title) > 30:
            suggestions.append("Title may be too long for optimal display")

        if errors:
            return TitleValidationResult(
                is_valid=False,
                title=title,
                suggestions=errors,
            )

        return None  # No issues

    def _fetch_genres(self, language: str) -> List[Genre]:
        """Fetch Tomato Novel genres.

        Args:
            language: Language code

        Returns:
            List of genres
        """
        return TOMATO_GENRES

    def _fetch_tags(self, genre: Optional[str]) -> List[Tag]:
        """Fetch Tomato Novel tags.

        Args:
            genre: Optional genre filter

        Returns:
            List of tags
        """
        if genre:
            # Filter tags by genre relevance
            return [tag for tag in TOMATO_TAGS if self._is_tag_relevant(tag, genre)]
        return TOMATO_TAGS

    def _is_tag_relevant(self, tag: Tag, genre: str) -> bool:
        """Check if tag is relevant to genre.

        Args:
            tag: Tag to check
            genre: Genre to check against

        Returns:
            True if relevant
        """
        # Simplified relevance logic
        genre_tag_mapping = {
            "fantasy": ["system", "cultivation", "genius", "strong_male"],
            "romance": ["strong_female", "rebirth", "transmigration"],
            "urban": ["system", "rebirth", "strong_male"],
            "xianxia": ["cultivation", "martial_arts", "genius"],
        }
        relevant_tags = genre_tag_mapping.get(genre, [])
        return tag.id in relevant_tags

    def _analyze_market_platform(self, genre: str, tags: List[str]) -> Dict[str, Any]:
        """Analyze Tomato Novel market.

        Args:
            genre: Genre to analyze
            tags: Tags to analyze

        Returns:
            Market analysis
        """
        # Simplified market analysis
        competition_levels = {
            "fantasy": "high",
            "romance": "high",
            "urban": "medium",
            "xianxia": "medium",
            "scifi": "low",
            "mystery": "low",
        }

        return {
            "competition_level": competition_levels.get(genre, "medium"),
            "reader_demand": "high" if genre in ["fantasy", "romance"] else "medium",
            "monetization_potential": "high",
            "recommended_tags": ["system", "rebirth", "strong_male"],
            "similar_stories": [],
            "market_size": "large",
            "growth_trend": "stable",
        }

    def _get_platform_name(self) -> str:
        """Get platform name.

        Returns:
            Platform name
        """
        return "Tomato Novel (番茄小说)"

    def _fetch_trending(self, limit: int) -> List[StoryMetadata]:
        """Fetch trending stories.

        Args:
            limit: Maximum stories

        Returns:
            List of trending stories
        """
        # Placeholder implementation
        return []

    def _publish_chapter_platform(self, story_id: str, chapter: Chapter) -> bool:
        """Publish chapter to Tomato Novel.

        Args:
            story_id: Story ID
            chapter: Chapter to publish

        Returns:
            True if successful
        """
        # Placeholder implementation
        # In real implementation, this would use Tomato Novel's API
        return True

    def _fetch_story_metadata(self, story_id: str) -> StoryMetadata:
        """Fetch story metadata.

        Args:
            story_id: Story ID

        Returns:
            Story metadata
        """
        # Placeholder implementation
        return StoryMetadata(
            id=story_id,
            title="Sample Story",
            author="Sample Author",
            platform=PlatformType.TOMATO,
        )

    def _fetch_chapters(self, story_id: str, limit: int) -> List[Chapter]:
        """Fetch chapters.

        Args:
            story_id: Story ID
            limit: Maximum chapters

        Returns:
            List of chapters
        """
        # Placeholder implementation
        return []
