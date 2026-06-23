"""
Unit tests for MCP tools.
"""

import pytest
import asyncio
from novel_agent.mcp.tools.validate_title import validate_title
from novel_agent.mcp.tools.classify_story import classify_story
from novel_agent.mcp.tools.generate_character import generate_character


class TestValidateTitleTool:
    """Test validate_title tool."""

    def test_valid_title(self):
        """Test valid title validation."""
        result = asyncio.run(validate_title.execute(
            title="The Last Guardian",
            platform="royalroad",
        ))
        assert result.success is True
        assert result.data["is_valid"] is True

    def test_invalid_title_too_short(self):
        """Test invalid title (too short)."""
        result = asyncio.run(validate_title.execute(
            title="A",
            platform="royalroad",
        ))
        assert result.success is True
        assert result.data["is_valid"] is False


class TestClassifyStoryTool:
    """Test classify_story tool."""

    def test_classify_fantasy(self):
        """Test classifying fantasy story."""
        result = asyncio.run(classify_story.execute(
            title="The Dragon's Quest",
            description="A young wizard must save the kingdom from an ancient dragon",
            platform="royalroad",
        ))
        assert result.success is True
        assert "suggested_genres" in result.data

    def test_classify_romance(self):
        """Test classifying romance story."""
        result = asyncio.run(classify_story.execute(
            title="Love in Paris",
            description="A heartwarming romance story about finding love",
            platform="wattpad",
        ))
        assert result.success is True
        assert "suggested_genres" in result.data


class TestGenerateCharacterTool:
    """Test generate_character tool."""

    def test_generate_protagonist(self):
        """Test generating protagonist."""
        result = asyncio.run(generate_character.execute(
            name="Alice",
            role="protagonist",
            genre="fantasy",
        ))
        assert result.success is True
        assert result.data["name"] == "Alice"
        assert result.data["role"] == "protagonist"

    def test_generate_antagonist(self):
        """Test generating antagonist."""
        result = asyncio.run(generate_character.execute(
            name="Dark Lord",
            role="antagonist",
            genre="fantasy",
        ))
        assert result.success is True
        assert result.data["role"] == "antagonist"
