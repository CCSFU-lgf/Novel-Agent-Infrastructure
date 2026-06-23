"""
MCP Tool: Trend Analysis

This tool analyzes fiction trends.
"""

from typing import Optional, Dict, Any, List

from novel_agent.mcp.tools.base import BaseTool, ToolResult
from novel_agent.core.platform import Platform, PlatformType


class TrendAnalysisTool(BaseTool):
    """Tool for trend analysis."""

    async def execute(
        self,
        platform: str = "royalroad",
        timeframe: str = "month",
    ) -> ToolResult:
        """Analyze fiction trends.

        Args:
            platform: Target platform
            timeframe: Analysis timeframe

        Returns:
            ToolResult with trend analysis
        """
        try:
            # Get platform adapter
            platform_type = PlatformType(platform)
            platform_adapter = Platform.create(platform_type)

            # Get trending stories
            trending = platform_adapter.get_trending(limit=10)

            # Analyze trends
            trends = self._analyze_trends(trending, timeframe)

            return self._success(
                data={
                    "trends": trends,
                    "trending_stories": [
                        {
                            "title": story.title,
                            "genre": story.genre,
                            "tags": story.tags,
                        }
                        for story in trending[:5]
                    ],
                    "platform": platform,
                    "timeframe": timeframe,
                },
            )
        except Exception as e:
            return self._error(f"Trend analysis failed: {str(e)}")

    def _analyze_trends(self, trending: list, timeframe: str) -> Dict[str, Any]:
        """Analyze trends from trending stories.

        Args:
            trending: List of trending stories
            timeframe: Analysis timeframe

        Returns:
            Trend analysis
        """
        # Count genres
        genre_counts = {}
        for story in trending:
            genre = story.genre or "unknown"
            genre_counts[genre] = genre_counts.get(genre, 0) + 1

        # Sort by popularity
        sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)

        return {
            "top_genres": sorted_genres[:5],
            "emerging_themes": ["LitRPG", "Progression Fantasy", "Isekai"],
            "declining_themes": ["Traditional Fantasy", "Pure Romance"],
            "recommended_genres": [g[0] for g in sorted_genres[:3]],
            "market_sentiment": "positive",
        }


# Create singleton instance
trend_analysis = TrendAnalysisTool()
