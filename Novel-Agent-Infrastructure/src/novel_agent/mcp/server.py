"""
MCP Server implementation for Novel Agent Infrastructure.

This module provides the main MCP server that exposes novel creation
tools to MCP-compatible clients.

Example:
    >>> from novel_agent.mcp import MCPServer
    >>> server = MCPServer()
    >>> server.run()
"""

import asyncio
from typing import Optional, Dict, Any, List
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

from novel_agent.core.config import Config
from novel_agent.core.memory import MemoryEngine
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


class MCPServer:
    """MCP Server for Novel Agent Infrastructure."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize MCP server.

        Args:
            config: Optional configuration
        """
        self.config = config or Config.from_env()
        self.memory = MemoryEngine.create(
            self.config.memory.engine_type,
            {
                "vector_db": self.config.memory.vector_db,
                "embedding_model": self.config.memory.embedding_model,
                "persist_directory": self.config.memory.persist_directory,
            },
        )
        self.server = Server("novel-agent-infrastructure")
        self._register_tools()

    def _register_tools(self) -> None:
        """Register all MCP tools."""

        @self.server.tool()
        async def validate_title(
            title: str,
            platform: str = "royalroad",
            language: str = "en",
        ) -> List[TextContent]:
            """Validate a story title for a specific platform.

            Args:
                title: The title to validate
                platform: Target platform (tomato, qidian, qimao, royalroad, wattpad, ao3, scribblehub)
                language: Language code (en, zh, etc.)

            Returns:
                Validation result
            """
            result = await validate_title.execute(
                title=title,
                platform=platform,
                language=language,
            )
            return [TextContent(type="text", text=str(result))]

        @self.server.tool()
        async def classify_story(
            title: str,
            description: str,
            platform: str = "royalroad",
        ) -> List[TextContent]:
            """Classify a story by genre and tags.

            Args:
                title: Story title
                description: Story description
                platform: Target platform

            Returns:
                Classification result
            """
            result = await classify_story.execute(
                title=title,
                description=description,
                platform=platform,
            )
            return [TextContent(type="text", text=str(result))]

        @self.server.tool()
        async def generate_character(
            name: str,
            role: str = "protagonist",
            genre: str = "fantasy",
            traits: Optional[List[str]] = None,
        ) -> List[TextContent]:
            """Generate a character profile.

            Args:
                name: Character name
                role: Character role (protagonist, antagonist, supporting)
                genre: Story genre
                traits: Optional character traits

            Returns:
                Character profile
            """
            result = await generate_character.execute(
                name=name,
                role=role,
                genre=genre,
                traits=traits or [],
            )
            return [TextContent(type="text", text=str(result))]

        @self.server.tool()
        async def generate_world(
            genre: str,
            setting: str = "medieval",
            magic_system: bool = True,
            technology_level: str = "pre-industrial",
        ) -> List[TextContent]:
            """Generate world-building elements.

            Args:
                genre: Story genre
                setting: World setting type
                magic_system: Whether to include magic system
                technology_level: Technology level of the world

            Returns:
                World-building elements
            """
            result = await generate_world.execute(
                genre=genre,
                setting=setting,
                magic_system=magic_system,
                technology_level=technology_level,
            )
            return [TextContent(type="text", text=str(result))]

        @self.server.tool()
        async def generate_outline(
            title: str,
            genre: str,
            target_chapters: int = 100,
            target_word_count: int = 200000,
        ) -> List[TextContent]:
            """Generate a story outline.

            Args:
                title: Story title
                genre: Story genre
                target_chapters: Target number of chapters
                target_word_count: Target word count

            Returns:
                Story outline
            """
            result = await generate_outline.execute(
                title=title,
                genre=genre,
                target_chapters=target_chapters,
                target_word_count=target_word_count,
            )
            return [TextContent(type="text", text=str(result))]

        @self.server.tool()
        async def generate_chapter_plan(
            chapter_number: int,
            previous_summary: str,
            plot_threads: List[str],
            characters: List[str],
        ) -> List[TextContent]:
            """Generate a chapter plan.

            Args:
                chapter_number: Chapter number
                previous_summary: Summary of previous chapter
                plot_threads: Active plot threads
                characters: Characters to include

            Returns:
                Chapter plan
            """
            result = await generate_chapter_plan.execute(
                chapter_number=chapter_number,
                previous_summary=previous_summary,
                plot_threads=plot_threads,
                characters=characters,
            )
            return [TextContent(type="text", text=str(result))]

        @self.server.tool()
        async def market_analysis(
            genre: str,
            tags: List[str],
            platform: str = "royalroad",
        ) -> List[TextContent]:
            """Analyze market for a story concept.

            Args:
                genre: Story genre
                tags: Story tags
                platform: Target platform

            Returns:
                Market analysis
            """
            result = await market_analysis.execute(
                genre=genre,
                tags=tags,
                platform=platform,
            )
            return [TextContent(type="text", text=str(result))]

        @self.server.tool()
        async def trend_analysis(
            platform: str = "royalroad",
            timeframe: str = "month",
        ) -> List[TextContent]:
            """Analyze fiction trends.

            Args:
                platform: Target platform
                timeframe: Analysis timeframe (week, month, year)

            Returns:
                Trend analysis
            """
            result = await trend_analysis.execute(
                platform=platform,
                timeframe=timeframe,
            )
            return [TextContent(type="text", text=str(result))]

        @self.server.tool()
        async def story_memory(
            action: str,
            entity_type: Optional[str] = None,
            entity_id: Optional[str] = None,
            data: Optional[Dict[str, Any]] = None,
        ) -> List[TextContent]:
            """Manage story memory.

            Args:
                action: Action to perform (add, get, update, delete, query)
                entity_type: Type of entity (character, location, plot_thread)
                entity_id: Entity ID
                data: Entity data

            Returns:
                Operation result
            """
            result = await story_memory.execute(
                action=action,
                entity_type=entity_type,
                entity_id=entity_id,
                data=data,
                memory_engine=self.memory,
            )
            return [TextContent(type="text", text=str(result))]

        @self.server.tool()
        async def publishing_assistant(
            story_id: str,
            platform: str,
            chapter_number: int,
            content: str,
            title: Optional[str] = None,
        ) -> List[TextContent]:
            """Assist with publishing a chapter.

            Args:
                story_id: Story ID
                platform: Target platform
                chapter_number: Chapter number
                content: Chapter content
                title: Optional chapter title

            Returns:
                Publishing result
            """
            result = await publishing_assistant.execute(
                story_id=story_id,
                platform=platform,
                chapter_number=chapter_number,
                content=content,
                title=title,
            )
            return [TextContent(type="text", text=str(result))]

    async def run(self) -> None:
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options(),
            )

    def run_sync(self) -> None:
        """Run the MCP server synchronously."""
        asyncio.run(self.run())


def create_server(config: Optional[Config] = None) -> MCPServer:
    """Create an MCP server instance.

    Args:
        config: Optional configuration

    Returns:
        MCPServer instance
    """
    return MCPServer(config)


if __name__ == "__main__":
    server = create_server()
    server.run_sync()
