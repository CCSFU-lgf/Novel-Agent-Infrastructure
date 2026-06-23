"""
MCP Tool: Validate Title

This tool validates story titles for different platforms.
"""

from typing import Optional, Dict, Any

from novel_agent.mcp.tools.base import BaseTool, ToolResult
from novel_agent.core.platform import Platform, PlatformType


class ValidateTitleTool(BaseTool):
    """Tool for validating story titles."""

    async def execute(
        self,
        title: str,
        platform: str = "royalroad",
        language: str = "en",
    ) -> ToolResult:
        """Validate a story title.

        Args:
            title: The title to validate
            platform: Target platform
            language: Language code

        Returns:
            ToolResult with validation details
        """
        try:
            # Get platform adapter
            platform_type = PlatformType(platform)
            platform_adapter = Platform.create(platform_type)

            # Validate title
            result = platform_adapter.validate_title(title)

            return self._success(
                data={
                    "is_valid": result.is_valid,
                    "title": result.title,
                    "suggestions": result.suggestions,
                    "message": result.message,
                    "platform": platform,
                },
                metadata={
                    "platform": platform,
                    "language": language,
                },
            )
        except Exception as e:
            return self._error(f"Validation failed: {str(e)}")


# Create singleton instance
validate_title = ValidateTitleTool()
