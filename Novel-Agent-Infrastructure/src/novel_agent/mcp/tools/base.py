"""
Base MCP tool implementation.

This module provides the base class for all MCP tools.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from pydantic import BaseModel


class ToolResult(BaseModel):
    """Result from an MCP tool."""

    success: bool
    data: Any
    error: Optional[str] = None
    metadata: Dict[str, Any] = {}


class BaseTool(ABC):
    """Base class for MCP tools."""

    def __init__(self):
        """Initialize tool."""
        self.name = self.__class__.__name__

    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """Execute the tool.

        Args:
            **kwargs: Tool-specific arguments

        Returns:
            ToolResult with output
        """
        pass

    def _success(self, data: Any, metadata: Optional[Dict[str, Any]] = None) -> ToolResult:
        """Create a success result.

        Args:
            data: Result data
            metadata: Optional metadata

        Returns:
            ToolResult
        """
        return ToolResult(success=True, data=data, metadata=metadata or {})

    def _error(self, error: str, metadata: Optional[Dict[str, Any]] = None) -> ToolResult:
        """Create an error result.

        Args:
            error: Error message
            metadata: Optional metadata

        Returns:
            ToolResult
        """
        return ToolResult(success=False, data=None, error=error, metadata=metadata or {})
