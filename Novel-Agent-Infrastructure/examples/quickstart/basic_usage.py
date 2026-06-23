"""
Basic usage example for Novel Agent Infrastructure.

This example demonstrates how to use the core features of the library.
"""

import asyncio
from novel_agent import Platform, PlatformType
from novel_agent.core.memory import MemoryEngine, Entity, EntityType


async def main():
    """Main example function."""
    print("🚀 Novel Agent Infrastructure - Basic Usage Example")
    print("=" * 50)

    # 1. Platform Usage
    print("\n📚 Platform Usage:")
    platform = Platform.create(PlatformType.ROYALROAD)

    # Validate title
    title = "The Last Guardian"
    result = platform.validate_title(title)
    print(f"Title '{title}' valid: {result.is_valid}")

    # Get genres
    genres = platform.get_genres()
    print(f"Available genres: {len(genres)}")
    for genre in genres[:3]:
        print(f"  - {genre.name}")

    # Get tags
    tags = platform.get_tags()
    print(f"Available tags: {len(tags)}")

    # Market analysis
    analysis = platform.analyze_market("fantasy", ["magic", "system"])
    print(f"Market analysis: {analysis['competition_level']} competition")

    # 2. Memory Engine Usage
    print("\n🧠 Memory Engine Usage:")
    memory = MemoryEngine.create("vector")

    # Add character
    character = Entity(
        id="char_1",
        name="Alice",
        entity_type=EntityType.CHARACTER,
        description="A brave young warrior",
        attributes={"age": 25, "role": "protagonist"},
    )
    memory.add_entity(character)
    print(f"Added character: {character.name}")

    # Add location
    location = Entity(
        id="loc_1",
        name="Crystal Castle",
        entity_type=EntityType.LOCATION,
        description="A magnificent castle made of crystal",
    )
    memory.add_entity(location)
    print(f"Added location: {location.name}")

    # Query memory
    from novel_agent.core.memory import MemoryQuery
    query = MemoryQuery(query="warrior", entity_type=EntityType.CHARACTER)
    results = memory.query(query)
    print(f"Query results: {len(results)}")

    # 3. MCP Tools Usage
    print("\n🔧 MCP Tools Usage:")
    from novel_agent.mcp.tools.validate_title import validate_title
    from novel_agent.mcp.tools.classify_story import classify_story

    # Validate title
    result = await validate_title.execute(
        title="The Dragon's Quest",
        platform="royalroad",
    )
    print(f"Title validation: {result.success}")

    # Classify story
    result = await classify_story.execute(
        title="The Dragon's Quest",
        description="A young wizard must save the kingdom",
        platform="royalroad",
    )
    print(f"Story classification: {result.success}")

    print("\n✅ Example completed!")


if __name__ == "__main__":
    asyncio.run(main())
