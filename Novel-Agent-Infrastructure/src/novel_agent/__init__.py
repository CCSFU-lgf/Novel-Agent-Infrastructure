"""
Novel Agent Infrastructure - Open-source infrastructure for AI fiction creation

This package provides the core infrastructure for building AI-powered fiction
creation systems with support for multiple platforms, long-form story memory,
and agent-native workflows.

Example:
    >>> from novel_agent import NovelAgent
    >>> agent = NovelAgent()
    >>> agent.create_story("My Story", platform="royalroad")
"""

__version__ = "0.1.0"
__author__ = "Novel Agent Team"
__email__ = "team@novel-agent.dev"

from novel_agent.core.platform import Platform, PlatformType
from novel_agent.core.memory import MemoryEngine
from novel_agent.core.agent import Agent, AgentConfig
from novel_agent.core.story import Story, StoryConfig

__all__ = [
    "Platform",
    "PlatformType",
    "MemoryEngine",
    "Agent",
    "AgentConfig",
    "Story",
    "StoryConfig",
]
