"""
MCP Tool: Publishing Assistant

This tool assists with publishing chapters.
"""

from typing import Optional, Dict, Any, List

from novel_agent.mcp.tools.base import BaseTool, ToolResult
from novel_agent.core.platform import Platform, PlatformType, Chapter


class PublishingAssistantTool(BaseTool):
    """Tool for publishing assistance."""

    async def execute(
        self,
        story_id: str,
        platform: str,
        chapter_number: int,
        content: str,
        title: Optional[str] = None,
    ) -> ToolResult:
        """Assist with publishing a chapter.

        Args:
            story_id: Story ID
            platform: Target platform
            chapter_number: Chapter number
            content: Chapter content
            title: Optional chapter title

        Returns:
            ToolResult with publishing result
        """
        try:
            # Get platform adapter
            platform_type = PlatformType(platform)
            platform_adapter = Platform.create(platform_type)

            # Create chapter object
            chapter = Chapter(
                id=f"ch_{chapter_number}",
                title=title or f"Chapter {chapter_number}",
                content=content,
                word_count=len(content.split()),
                chapter_number=chapter_number,
            )

            # Validate chapter
            validation = self._validate_chapter(chapter, platform)

            if not validation["is_valid"]:
                return self._success(
                    data={
                        "status": "validation_failed",
                        "validation": validation,
                    },
                )

            # Publish chapter
            success = platform_adapter.publish_chapter(story_id, chapter)

            if success:
                return self._success(
                    data={
                        "status": "published",
                        "chapter_number": chapter_number,
                        "word_count": chapter.word_count,
                        "platform": platform,
                        "validation": validation,
                    },
                )
            else:
                return self._error("Failed to publish chapter")

        except Exception as e:
            return self._error(f"Publishing failed: {str(e)}")

    def _validate_chapter(self, chapter: Chapter, platform: str) -> Dict[str, Any]:
        """Validate chapter for publishing.

        Args:
            chapter: Chapter to validate
            platform: Target platform

        Returns:
            Validation result
        """
        issues = []
        warnings = []

        # Word count checks
        if chapter.word_count < 100:
            issues.append("Chapter too short (minimum 100 words)")
        elif chapter.word_count < 500:
            warnings.append("Chapter may be too short for optimal engagement")

        if chapter.word_count > 10000:
            warnings.append("Chapter may be too long for web fiction")

        # Content checks
        if not chapter.content.strip():
            issues.append("Chapter content is empty")

        # Title checks
        if not chapter.title:
            warnings.append("No chapter title provided")

        return {
            "is_valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "word_count": chapter.word_count,
        }


# Create singleton instance
publishing_assistant = PublishingAssistantTool()
