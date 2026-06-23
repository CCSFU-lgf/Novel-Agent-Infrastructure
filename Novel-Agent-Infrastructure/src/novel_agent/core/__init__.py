"""
Core module for Novel Agent Infrastructure.

This module provides the core abstractions and interfaces for:
- Platform adapters
- Memory engines
- Agent system
- Story management
"""

from novel_agent.core.platform import Platform, PlatformType
from novel_agent.core.memory import MemoryEngine
from novel_agent.core.agent import Agent, AgentConfig
from novel_agent.core.story import Story, StoryConfig
from novel_agent.core.config import Config

__all__ = [
    "Platform",
    "PlatformType",
    "MemoryEngine",
    "Agent",
    "AgentConfig",
    "Story",
    "StoryConfig",
    "Config",
]
