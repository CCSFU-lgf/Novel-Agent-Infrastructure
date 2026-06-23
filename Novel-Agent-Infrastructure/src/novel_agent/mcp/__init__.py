"""
MCP (Model Context Protocol) server for Novel Agent Infrastructure.

This module provides MCP server implementation for integrating with
Claude Code, Codex, Cursor, and other MCP-compatible clients.

Available MCP Tools:
- validate_title: Validate story titles
- classify_story: Classify stories by genre
- generate_character: Generate character profiles
- generate_world: Generate world-building elements
- generate_outline: Generate story outlines
- generate_chapter_plan: Generate chapter plans
- market_analysis: Analyze market trends
- trend_analysis: Analyze fiction trends
- story_memory: Manage story memory
- publishing_assistant: Assist with publishing
"""

from novel_agent.mcp.server import MCPServer, create_server
from novel_agent.mcp.tools import (
    validate_title,
    classify_story,
    generate_character,
    generate_world,
    generate_outline,
    generate_chapter_plan,
    market_analysis,
    trend_analysis,
    story_memory,
    publishing_assistant,
)

__all__ = [
    "MCPServer",
    "create_server",
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
