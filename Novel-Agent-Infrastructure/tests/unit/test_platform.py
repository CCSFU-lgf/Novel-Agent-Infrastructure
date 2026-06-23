"""
Unit tests for platform adapters.
"""

import pytest
from novel_agent.core.platform import Platform, PlatformType, TitleValidationResult


class TestPlatform:
    """Test platform adapters."""

    def test_platform_creation(self):
        """Test platform adapter creation."""
        platform = Platform.create(PlatformType.ROYALROAD)
        assert platform is not None

    def test_validate_title_valid(self):
        """Test title validation with valid title."""
        platform = Platform.create(PlatformType.ROYALROAD)
        result = platform.validate_title("The Last Guardian")
        assert result.is_valid is True

    def test_validate_title_too_short(self):
        """Test title validation with too short title."""
        platform = Platform.create(PlatformType.ROYALROAD)
        result = platform.validate_title("A")
        assert result.is_valid is False

    def test_get_genres(self):
        """Test getting genres."""
        platform = Platform.create(PlatformType.ROYALROAD)
        genres = platform.get_genres()
        assert len(genres) > 0

    def test_get_tags(self):
        """Test getting tags."""
        platform = Platform.create(PlatformType.ROYALROAD)
        tags = platform.get_tags()
        assert len(tags) > 0

    def test_analyze_market(self):
        """Test market analysis."""
        platform = Platform.create(PlatformType.ROYALROAD)
        analysis = platform.analyze_market("fantasy", ["magic", "system"])
        assert "genre" in analysis
        assert "platform" in analysis


class TestPlatformTypes:
    """Test platform types."""

    def test_chinese_platforms(self):
        """Test Chinese platform types."""
        assert PlatformType.TOMATO.value == "tomato"
        assert PlatformType.QIDIAN.value == "qidian"
        assert PlatformType.QIMAO.value == "qimao"

    def test_international_platforms(self):
        """Test international platform types."""
        assert PlatformType.ROYALROAD.value == "royalroad"
        assert PlatformType.WATTPAD.value == "wattpad"
        assert PlatformType.AO3.value == "ao3"
        assert PlatformType.SCRIBBLEHUB.value == "scribblehub"
