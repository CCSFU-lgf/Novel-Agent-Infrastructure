"""
MCP Server example for Novel Agent Infrastructure.

This example demonstrates how to start and use the MCP server.
"""

from novel_agent.mcp import MCPServer
from novel_agent.core.config import Config


def main():
    """Start MCP server."""
    print("🚀 Starting MCP Server...")
    print("=" * 50)

    # Create configuration
    config = Config()
    config.server.host = "0.0.0.0"
    config.server.port = 8000

    # Create and start server
    server = MCPServer(config)

    print(f"Server starting on {config.server.host}:{config.server.port}")
    print("\nAvailable MCP Tools:")
    print("  - validate_title")
    print("  - classify_story")
    print("  - generate_character")
    print("  - generate_world")
    print("  - generate_outline")
    print("  - generate_chapter_plan")
    print("  - market_analysis")
    print("  - trend_analysis")
    print("  - story_memory")
    print("  - publishing_assistant")

    print("\nPress Ctrl+C to stop the server")

    try:
        server.run_sync()
    except KeyboardInterrupt:
        print("\n✅ Server stopped")


if __name__ == "__main__":
    main()
