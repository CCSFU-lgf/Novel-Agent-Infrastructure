"""
MCP Tool: Classify Story

This tool classifies stories by genre and tags.
"""

from typing import Optional, Dict, Any, List

from novel_agent.mcp.tools.base import BaseTool, ToolResult
from novel_agent.core.platform import Platform, PlatformType


class ClassifyStoryTool(BaseTool):
    """Tool for classifying stories."""

    async def execute(
        self,
        title: str,
        description: str,
        platform: str = "royalroad",
    ) -> ToolResult:
        """Classify a story.

        Args:
            title: Story title
            description: Story description
            platform: Target platform

        Returns:
            ToolResult with classification
        """
        try:
            # Get platform adapter
            platform_type = PlatformType(platform)
            platform_adapter = Platform.create(platform_type)

            # Get available genres and tags
            genres = platform_adapter.get_genres()
            tags = platform_adapter.get_tags()

            # Simple classification based on keywords
            suggested_genres = self._suggest_genres(title, description, genres)
            suggested_tags = self._suggest_tags(title, description, tags)

            return self._success(
                data={
                    "title": title,
                    "suggested_genres": suggested_genres,
                    "suggested_tags": suggested_tags,
                    "available_genres": [{"id": g.id, "name": g.name} for g in genres[:10]],
                    "available_tags": [{"id": t.id, "name": t.name} for t in tags[:20]],
                    "platform": platform,
                },
                metadata={
                    "platform": platform,
                },
            )
        except Exception as e:
            return self._error(f"Classification failed: {str(e)}")

    def _suggest_genres(self, title: str, description: str, genres: list) -> List[Dict[str, Any]]:
        """Suggest genres based on title and description.

        Args:
            title: Story title
            description: Story description
            genres: Available genres

        Returns:
            Suggested genres
        """
        text = f"{title} {description}".lower()
        suggestions = []

        # Keyword-based genre detection
        genre_keywords = {
            "fantasy": ["magic", "wizard", "dragon", "kingdom", "quest", "sword"],
            "romance": ["love", "heart", "relationship", "passion", "kiss"],
            "scifi": ["space", "future", "technology", "robot", "alien", "galaxy"],
            "mystery": ["murder", "detective", "clue", "secret", "investigate"],
            "horror": ["ghost", "monster", "dark", "fear", "nightmare", "haunted"],
            "litrpg": ["level", "stat", "skill", "system", "game", "rpg"],
            "xianxia": ["cultivation", "immortal", "sect", "spirit", "qi"],
        }

        for genre in genres:
            keywords = genre_keywords.get(genre.id, [])
            if any(keyword in text for keyword in keywords):
                suggestions.append({
                    "id": genre.id,
                    "name": genre.name,
                    "confidence": 0.7,
                })

        # Return top 3 suggestions
        return suggestions[:3]

    def _suggest_tags(self, title: str, description: str, tags: list) -> List[Dict[str, Any]]:
        """Suggest tags based on title and description.

        Args:
            title: Story title
            description: Story description
            tags: Available tags

        Returns:
            Suggested tags
        """
        text = f"{title} {description}".lower()
        suggestions = []

        # Keyword-based tag detection
        tag_keywords = {
            "male_lead": ["he", "him", "man", "boy", "male"],
            "female_lead": ["she", "her", "woman", "girl", "female"],
            "system": ["system", "game", "stats", "level"],
            "rebirth": ["rebirth", "reborn", "second chance"],
            "transmigration": ["transmigration", "isekai", "another world"],
            "magic": ["magic", "spell", "enchant", "arcane"],
            "cultivation": ["cultivation", "qi", "spirit", "immortal"],
        }

        for tag in tags:
            keywords = tag_keywords.get(tag.id, [])
            if any(keyword in text for keyword in keywords):
                suggestions.append({
                    "id": tag.id,
                    "name": tag.name,
                    "confidence": 0.6,
                })

        return suggestions[:5]


# Create singleton instance
classify_story = ClassifyStoryTool()
