"""
MCP Tool: Market Analysis

This tool analyzes market trends for fiction.
"""

from typing import Optional, Dict, Any, List

from novel_agent.mcp.tools.base import BaseTool, ToolResult
from novel_agent.core.platform import Platform, PlatformType


class MarketAnalysisTool(BaseTool):
    """Tool for market analysis."""

    async def execute(
        self,
        genre: str,
        tags: List[str],
        platform: str = "royalroad",
    ) -> ToolResult:
        """Analyze market for a story concept.

        Args:
            genre: Story genre
            tags: Story tags
            platform: Target platform

        Returns:
            ToolResult with market analysis
        """
        try:
            # Get platform adapter
            platform_type = PlatformType(platform)
            platform_adapter = Platform.create(platform_type)

            # Get market analysis
            analysis = platform_adapter.analyze_market(genre, tags)

            # Enhance with recommendations
            recommendations = self._generate_recommendations(analysis)

            return self._success(
                data={
                    "analysis": analysis,
                    "recommendations": recommendations,
                    "platform": platform,
                },
            )
        except Exception as e:
            return self._error(f"Market analysis failed: {str(e)}")

    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on analysis.

        Args:
            analysis: Market analysis

        Returns:
            Recommendations
        """
        recommendations = []

        competition = analysis.get("competition_level", "medium")
        demand = analysis.get("reader_demand", "medium")

        if competition == "high" and demand == "high":
            recommendations.append("High competition but high demand - focus on unique angle")
        elif competition == "low" and demand == "high":
            recommendations.append("Great opportunity - low competition with high demand")
        elif competition == "high" and demand == "low":
            recommendations.append("Consider pivoting to a different genre or subgenre")

        if analysis.get("growth_trend") == "growing":
            recommendations.append("Market is growing - good time to enter")

        recommendations.extend([
            "Research top-performing stories in this genre",
            "Focus on consistent release schedule",
            "Engage with the community",
        ])

        return recommendations


# Create singleton instance
market_analysis = MarketAnalysisTool()
