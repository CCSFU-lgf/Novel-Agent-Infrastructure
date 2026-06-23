"""
CLI interface for Novel Agent Infrastructure.

This module provides the command-line interface for the novel agent system.
"""

import typer
from typing import Optional
from rich.console import Console
from rich.table import Table

from novel_agent import __version__

app = typer.Typer(
    name="novel-agent",
    help="Open-source infrastructure for AI fiction creation",
    no_args_is_help=True,
)

console = Console()


@app.command()
def version():
    """Show version information."""
    console.print(f"Novel Agent Infrastructure v{__version__}")


@app.command()
def init(
    name: str = typer.Argument(..., help="Project name"),
    platform: str = typer.Option("royalroad", help="Target platform"),
    genre: str = typer.Option("fantasy", help="Story genre"),
):
    """Initialize a new novel project."""
    console.print(f"[bold green]Initializing project: {name}[/bold green]")
    console.print(f"Platform: {platform}")
    console.print(f"Genre: {genre}")
    # TODO: Implement project initialization
    console.print("[yellow]Project initialization coming soon![/yellow]")


@app.command()
def validate(
    title: str = typer.Argument(..., help="Title to validate"),
    platform: str = typer.Option("royalroad", help="Target platform"),
):
    """Validate a story title."""
    from novel_agent.mcp.tools.validate_title import validate_title
    import asyncio

    result = asyncio.run(validate_title.execute(title=title, platform=platform))

    if result.success:
        data = result.data
        if data["is_valid"]:
            console.print(f"[bold green]✓ Title is valid: {data['title']}[/bold green]")
        else:
            console.print(f"[bold red]✗ Title validation failed[/bold red]")
            for suggestion in data.get("suggestions", []):
                console.print(f"  - {suggestion}")
    else:
        console.print(f"[bold red]Error: {result.error}[/bold red]")


@app.command()
def classify(
    title: str = typer.Argument(..., help="Story title"),
    description: str = typer.Argument(..., help="Story description"),
    platform: str = typer.Option("royalroad", help="Target platform"),
):
    """Classify a story by genre and tags."""
    from novel_agent.mcp.tools.classify_story import classify_story
    import asyncio

    result = asyncio.run(classify_story.execute(
        title=title,
        description=description,
        platform=platform,
    ))

    if result.success:
        data = result.data
        console.print(f"[bold]Classification for: {data['title']}[/bold]")

        if data.get("suggested_genres"):
            console.print("\n[bold blue]Suggested Genres:[/bold blue]")
            for genre in data["suggested_genres"]:
                console.print(f"  - {genre['name']} (confidence: {genre['confidence']:.0%})")

        if data.get("suggested_tags"):
            console.print("\n[bold blue]Suggested Tags:[/bold blue]")
            for tag in data["suggested_tags"]:
                console.print(f"  - {tag['name']}")
    else:
        console.print(f"[bold red]Error: {result.error}[/bold red]")


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", help="Server host"),
    port: int = typer.Option(8000, help="Server port"),
):
    """Start the MCP server."""
    from novel_agent.mcp import MCPServer
    from novel_agent.core.config import Config

    console.print(f"[bold green]Starting MCP server on {host}:{port}[/bold green]")

    config = Config()
    config.server.host = host
    config.server.port = port

    server = MCPServer(config)
    server.run_sync()


@app.command()
def benchmark():
    """Run benchmarks."""
    console.print("[bold yellow]Running benchmarks...[/bold yellow]")
    # TODO: Implement benchmarks
    console.print("[yellow]Benchmarks coming soon![/yellow]")


@app.command()
def examples():
    """Show example usage."""
    table = Table(title="Example Commands")
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="green")

    table.add_row("novel-agent init my-novel", "Initialize a new project")
    table.add_row("novel-agent validate 'My Title'", "Validate a title")
    table.add_row("novel-agent classify 'Title' 'Desc'", "Classify a story")
    table.add_row("novel-agent serve", "Start MCP server")

    console.print(table)


if __name__ == "__main__":
    app()
