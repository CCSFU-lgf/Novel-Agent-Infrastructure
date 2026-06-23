"""
MCP Tools for Novel Agent Infrastructure.

This module provides all MCP tools for novel creation and management.
"""

from novel_agent.mcp.tools.validate_title import validate_title
from novel_agent.mcp.tools.classify_story import classify_story
from novel_agent.mcp.tools.generate_character import generate_character
from novel_agent.mcp.tools.generate_world import generate_world
from novel_agent.mcp.tools.generate_outline import generate_outline
from novel_agent.mcp.tools.generate_chapter_plan import generate_chapter_plan
from novel_agent.mcp.tools.market_analysis import market_analysis
from novel_agent.mcp.tools.trend_analysis import trend_analysis
from novel_agent.mcp.tools.story_memory import story_memory
from novel_agent.mcp.tools.publishing_assistant import publishing_assistant

__all__ = [
    "validate_title",
    "classify_story",
    "generate_character",
    "generate_world",
    "generate_outline",
    "generate_chapter_plan",
    "market_analysis",
    "trend_analysis",
    "story_memory",
    "publishing_assistant",
]
