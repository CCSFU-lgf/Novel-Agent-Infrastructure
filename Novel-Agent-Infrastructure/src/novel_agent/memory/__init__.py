"""
Memory engine implementations for Novel Agent Infrastructure.

This module provides different memory engine implementations:
- Vector: Vector-based semantic search
- Graph: Graph-based relationship tracking
- Hybrid: Combined approach
"""

from typing import Dict, Type
from novel_agent.core.memory import MemoryEngine

# Registry of memory engines
_engine_registry: Dict[str, Type[MemoryEngine]] = {}


def register_memory_engine(engine_type: str, engine_class: Type[MemoryEngine]) -> None:
    """Register a memory engine.

    Args:
        engine_type: Type of engine
        engine_class: Engine class
    """
    _engine_registry[engine_type] = engine_class


def get_memory_engine_class(engine_type: str) -> Type[MemoryEngine]:
    """Get memory engine class.

    Args:
        engine_type: Type of engine

    Returns:
        Engine class

    Raises:
        ValueError: If engine type is not registered
    """
    if engine_type not in _engine_registry:
        _load_engine(engine_type)

    if engine_type not in _engine_registry:
        raise ValueError(f"Unsupported memory engine: {engine_type}")

    return _engine_registry[engine_type]


def _load_engine(engine_type: str) -> None:
    """Lazy load a memory engine.

    Args:
        engine_type: Type of engine to load
    """
    if engine_type == "vector":
        from novel_agent.memory.vector import VectorMemoryEngine
        register_memory_engine(engine_type, VectorMemoryEngine)
    elif engine_type == "graph":
        from novel_agent.memory.graph import GraphMemoryEngine
        register_memory_engine(engine_type, GraphMemoryEngine)


__all__ = [
    "register_memory_engine",
    "get_memory_engine_class",
]
