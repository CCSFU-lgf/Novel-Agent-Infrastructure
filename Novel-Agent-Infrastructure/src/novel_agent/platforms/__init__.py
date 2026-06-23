"""
Platform adapters for Novel Agent Infrastructure.

This module provides platform-specific adapters for different fiction
publishing platforms.

Supported Platforms:
- Chinese: Tomato Novel, Qidian, Qimao
- International: Royal Road, Wattpad, AO3, ScribbleHub
"""

from typing import Dict, Type
from novel_agent.core.platform import Platform, PlatformType

# Registry of platform adapters
_platform_registry: Dict[PlatformType, Type[Platform]] = {}


def register_platform(platform_type: PlatformType, platform_class: Type[Platform]) -> None:
    """Register a platform adapter.

    Args:
        platform_type: Type of platform
        platform_class: Platform adapter class
    """
    _platform_registry[platform_type] = platform_class


def get_platform_class(platform_type: PlatformType) -> Type[Platform]:
    """Get platform adapter class.

    Args:
        platform_type: Type of platform

    Returns:
        Platform adapter class

    Raises:
        ValueError: If platform type is not registered
    """
    if platform_type not in _platform_registry:
        # Lazy load platform adapters
        _load_platform(platform_type)

    if platform_type not in _platform_registry:
        raise ValueError(f"Unsupported platform: {platform_type}")

    return _platform_registry[platform_type]


def _load_platform(platform_type: PlatformType) -> None:
    """Lazy load a platform adapter.

    Args:
        platform_type: Type of platform to load
    """
    if platform_type == PlatformType.TOMATO:
        from novel_agent.platforms.tomato import TomatoPlatform
        register_platform(platform_type, TomatoPlatform)
    elif platform_type == PlatformType.QIDIAN:
        from novel_agent.platforms.qidian import QidianPlatform
        register_platform(platform_type, QidianPlatform)
    elif platform_type == PlatformType.QIMAO:
        from novel_agent.platforms.qimao import QimaoPlatform
        register_platform(platform_type, QimaoPlatform)
    elif platform_type == PlatformType.ROYALROAD:
        from novel_agent.platforms.royalroad import RoyalRoadPlatform
        register_platform(platform_type, RoyalRoadPlatform)
    elif platform_type == PlatformType.WATTPAD:
        from novel_agent.platforms.wattpad import WattpadPlatform
        register_platform(platform_type, WattpadPlatform)
    elif platform_type == PlatformType.AO3:
        from novel_agent.platforms.ao3 import AO3Platform
        register_platform(platform_type, AO3Platform)
    elif platform_type == PlatformType.SCRIBBLEHUB:
        from novel_agent.platforms.scribblehub import ScribbleHubPlatform
        register_platform(platform_type, ScribbleHubPlatform)


def list_platforms() -> list[PlatformType]:
    """List all available platforms.

    Returns:
        List of platform types
    """
    return list(PlatformType)


__all__ = [
    "register_platform",
    "get_platform_class",
    "list_platforms",
]
