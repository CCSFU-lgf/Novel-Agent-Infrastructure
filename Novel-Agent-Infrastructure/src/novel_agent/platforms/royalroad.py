"""
Royal Road platform adapter.

This module provides integration with Royal Road, a popular English-language
fiction platform specializing in LitRPG, Progression Fantasy, and web novels.

Features:
- English-language title validation
- Western fiction genre support
- Market analysis for English web fiction
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


# Royal Road specific genres
ROYALROAD_GENRES = [
    Genre(id="litrpg", name="LitRPG", name_en="LitRPG"),
    Genre(id="progression_fantasy", name="Progression Fantasy", name_en="Progression Fantasy"),
    Genre(id="epic_fantasy", name="Epic Fantasy", name_en="Epic Fantasy"),
    Genre(id="urban_fantasy", name="Urban Fantasy", name_en="Urban Fantasy"),
    Genre(id="sci_fi", name="Sci-Fi", name_en="Sci-Fi"),
    Genre(id="romance", name="Romance", name_en="Romance"),
    Genre(id="mystery", name="Mystery", name_en="Mystery"),
    Genre(id="horror", name="Horror", name_en="Horror"),
    Genre(id="thriller", name="Thriller", name_en="Thriller"),
    Genre(id="comedy", name="Comedy", name_en="Comedy"),
    Genre(id="slice_of_life", name="Slice of Life", name_en="Slice of Life"),
    Genre(id="action", name="Action", name_en="Action"),
    Genre(id="adventure", name="Adventure", name_en="Adventure"),
    Genre(id="isekai", name="Isekai", name_en="Isekai"),
    Genre(id="wuxia", name="Wuxia", name_en="Wuxia"),
    Genre(id="xianxia", name="Xianxia", name_en="Xianxia"),
]

# Royal Road specific tags
ROYALROAD_TAGS = [
    Tag(id="male_lead", name="Male Lead", name_en="Male Lead", category="character"),
    Tag(id="female_lead", name="Female Lead", name_en="Female Lead", category="character"),
    Tag(id="strong_lead", name="Strong Lead", name_en="Strong Lead", category="character"),
    Tag(id="weak_to_strong", name="Weak to Strong", name_en="Weak to Strong", category="progression"),
    Tag(id="op_lead", name="OP Lead", name_en="OP Lead", category="character"),
    Tag(id="magic", name="Magic", name_en="Magic", category="system"),
    Tag(id="system", name="System", name_en="System", category="system"),
    Tag(id="stats", name="Stats", name_en="Stats", category="system"),
    Tag(id="leveling", name="Leveling", name_en="Leveling", category="system"),
    Tag(id="skills", name="Skills", name_en="Skills", category="system"),
    Tag(id="crafting", name="Crafting", name_en="Crafting", category="activity"),
    Tag(id="kingdom_building", name="Kingdom Building", name_en="Kingdom Building", category="theme"),
    Tag(id="tower_climbing", name="Tower Climbing", name_en="Tower Climbing", category="theme"),
    Tag(id="dungeon", name="Dungeon", name_en="Dungeon", category="theme"),
    Tag(id="academy", name="Academy", name_en="Academy", category="setting"),
    Tag(id="vr", name="VR", name_en="VR", category="setting"),
    Tag(id="post_apocalyptic", name="Post Apocalyptic", name_en="Post Apocalyptic", category="setting"),
    Tag(id="time_loop", name="Time Loop", name_en="Time Loop", category="theme"),
    Tag(id="reincarnation", name="Reincarnation", name_en="Reincarnation", category="theme"),
    Tag(id="transmigration", name="Transmigration", name_en="Transmigration", category="theme"),
    Tag(id="slow_burn", name="Slow Burn", name_en="Slow Burn", category="pacing"),
    Tag(id="fast_paced", name="Fast Paced", name_en="Fast Paced", category="pacing"),
]


class RoyalRoadPlatform(BasePlatform):
    """Royal Road platform adapter."""

    def _initialize(self) -> None:
        """Initialize Royal Road platform."""
        super()._initialize()
        self.platform_type = PlatformType.ROYALROAD
        self.base_url = self.config.get("base_url", "https://www.royalroad.com")

    def _validate_title_platform(self, title: str) -> Optional[TitleValidationResult]:
        """Validate title for Royal Road.

        Args:
            title: Title to validate

        Returns:
            TitleValidationResult if validation fails, None otherwise
        """
        errors = []
        suggestions = []

        # Royal Road prefers English titles
        has_non_ascii = any(ord(char) > 127 for char in title)
        if has_non_ascii:
            suggestions.append("Consider using English characters for better discoverability")

        # Check for common patterns
        if title.isupper():
            suggestions.append("Consider using title case instead of all caps")

        if errors:
            return TitleValidationResult(
                is_valid=False,
                title=title,
                suggestions=errors,
            )

        return None

    def _fetch_genres(self, language: str) -> List[Genre]:
        """Fetch Royal Road genres.

        Args:
            language: Language code

        Returns:
            List of genres
        """
        return ROYALROAD_GENRES

    def _fetch_tags(self, genre: Optional[str]) -> List[Tag]:
        """Fetch Royal Road tags.

        Args:
            genre: Optional genre filter

        Returns:
            List of tags
        """
        if genre:
            return [tag for tag in ROYALROAD_TAGS if self._is_tag_relevant(tag, genre)]
        return ROYALROAD_TAGS

    def _is_tag_relevant(self, tag: Tag, genre: str) -> bool:
        """Check if tag is relevant to genre.

        Args:
            tag: Tag to check
            genre: Genre to check against

        Returns:
            True if relevant
        """
        genre_tag_mapping = {
            "litrpg": ["system", "stats", "leveling", "skills", "male_lead", "weak_to_strong"],
            "progression_fantasy": ["magic", "leveling", "skills", "weak_to_strong", "strong_lead"],
            "epic_fantasy": ["magic", "male_lead", "female_lead", "kingdom_building"],
            "isekai": ["transmigration", "reincarnation", "system", "op_lead"],
            "xianxia": ["cultivation", "magic", "weak_to_strong", "male_lead"],
        }
        relevant_tags = genre_tag_mapping.get(genre, [])
        return tag.id in relevant_tags

    def _analyze_market_platform(self, genre: str, tags: List[str]) -> Dict[str, Any]:
        """Analyze Royal Road market.

        Args:
            genre: Genre to analyze
            tags: Tags to analyze

        Returns:
            Market analysis
        """
        competition_levels = {
            "litrpg": "high",
            "progression_fantasy": "high",
            "epic_fantasy": "medium",
            "isekai": "medium",
            "sci_fi": "low",
            "mystery": "low",
        }

        return {
            "competition_level": competition_levels.get(genre, "medium"),
            "reader_demand": "high" if genre in ["litrpg", "progression_fantasy"] else "medium",
            "monetization_potential": "medium",
            "recommended_tags": ["system", "leveling", "weak_to_strong"],
            "similar_stories": [],
            "market_size": "medium",
            "growth_trend": "growing",
        }

    def _get_platform_name(self) -> str:
        """Get platform name.

        Returns:
            Platform name
        """
        return "Royal Road"

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
        """Publish chapter to Royal Road.

        Args:
            story_id: Story ID
            chapter: Chapter to publish

        Returns:
            True if successful
        """
        # Placeholder implementation
        return True

    def _fetch_story_metadata(self, story_id: str) -> StoryMetadata:
        """Fetch story metadata.

        Args:
            story_id: Story ID

        Returns:
            Story metadata
        """
        return StoryMetadata(
            id=story_id,
            title="Sample Story",
            author="Sample Author",
            platform=PlatformType.ROYALROAD,
        )

    def _fetch_chapters(self, story_id: str, limit: int) -> List[Chapter]:
        """Fetch chapters.

        Args:
            story_id: Story ID
            limit: Maximum chapters

        Returns:
            List of chapters
        """
        return []
