"""
Story Memory Engine for Novel Agent Infrastructure.

This module provides long-term memory capabilities for fiction creation,
enabling consistent storytelling across hundreds of chapters.

Key Features:
- Character tracking and relationship management
- World-building consistency
- Plot thread tracking
- Foreshadowing and callback management
- Vector-based semantic retrieval

Example:
    >>> from novel_agent.core.memory import MemoryEngine
    >>> engine = MemoryEngine()
    >>> engine.add_character("Alice", {"age": 25, "role": "protagonist"})
    >>> engine.get_character("Alice")
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Dict, Any, List, Set
from pydantic import BaseModel, Field
from datetime import datetime


class EntityType(str, Enum):
    """Types of entities stored in memory."""

    CHARACTER = "character"
    LOCATION = "location"
    ITEM = "item"
    EVENT = "event"
    ORGANIZATION = "organization"
    RELATIONSHIP = "relationship"
    PLOT_THREAD = "plot_thread"
    FORESHADOWING = "foreshadowing"


class Entity(BaseModel):
    """Base entity in memory."""

    id: str
    name: str
    entity_type: EntityType
    description: Optional[str] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    chapter_introduced: Optional[int] = None
    tags: List[str] = Field(default_factory=list)


class Character(Entity):
    """Character entity."""

    entity_type: EntityType = EntityType.CHARACTER
    age: Optional[int] = None
    gender: Optional[str] = None
    role: Optional[str] = None  # protagonist, antagonist, supporting, etc.
    personality: List[str] = Field(default_factory=list)
    appearance: Optional[str] = None
    background: Optional[str] = None
    goals: List[str] = Field(default_factory=list)
    relationships: Dict[str, str] = Field(default_factory=dict)  # character_id -> relationship_type


class Location(Entity):
    """Location entity."""

    entity_type: EntityType = EntityType.LOCATION
    location_type: Optional[str] = None  # city, building, realm, etc.
    coordinates: Optional[Dict[str, float]] = None
    inhabitants: List[str] = Field(default_factory=list)  # character_ids
    connected_locations: List[str] = Field(default_factory=list)


class PlotThread(Entity):
    """Plot thread tracking."""

    entity_type: EntityType = EntityType.PLOT_THREAD
    status: str = "active"  # active, resolved, abandoned
    importance: int = 1  # 1-10
    chapters_involved: List[int] = Field(default_factory=list)
    related_characters: List[str] = Field(default_factory=list)
    resolution: Optional[str] = None


class Foreshadowing(Entity):
    """Foreshadowing element."""

    entity_type: EntityType = EntityType.FORESHADOWING
    planted_chapter: int
    expected_payoff_chapter: Optional[int] = None
    actual_payoff_chapter: Optional[int] = None
    subtlety_level: int = 5  # 1-10
    status: str = "planted"  # planted, hinted, payoff


class MemoryQuery(BaseModel):
    """Query for memory retrieval."""

    query: str
    entity_type: Optional[EntityType] = None
    chapter_range: Optional[tuple[int, int]] = None
    tags: List[str] = Field(default_factory=list)
    limit: int = 10
    similarity_threshold: float = 0.7


class MemoryResult(BaseModel):
    """Result from memory query."""

    entity: Entity
    similarity: float
    relevance_reason: Optional[str] = None
    context: Dict[str, Any] = Field(default_factory=dict)


class MemoryEngine(ABC):
    """Abstract base class for memory engines."""

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the memory engine.

        Args:
            config: Configuration for the memory engine
        """
        pass

    @abstractmethod
    def add_entity(self, entity: Entity) -> str:
        """Add an entity to memory.

        Args:
            entity: Entity to add

        Returns:
            Entity ID
        """
        pass

    @abstractmethod
    def update_entity(self, entity_id: str, updates: Dict[str, Any]) -> bool:
        """Update an entity in memory.

        Args:
            entity_id: ID of entity to update
            updates: Fields to update

        Returns:
            True if successful
        """
        pass

    @abstractmethod
    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """Get an entity by ID.

        Args:
            entity_id: ID of entity to retrieve

        Returns:
            Entity if found, None otherwise
        """
        pass

    @abstractmethod
    def delete_entity(self, entity_id: str) -> bool:
        """Delete an entity from memory.

        Args:
            entity_id: ID of entity to delete

        Returns:
            True if successful
        """
        pass

    @abstractmethod
    def query(self, query: MemoryQuery) -> List[MemoryResult]:
        """Query memory for relevant entities.

        Args:
            query: Memory query

        Returns:
            List of relevant entities
        """
        pass

    @abstractmethod
    def get_characters(self, chapter: Optional[int] = None) -> List[Character]:
        """Get all characters, optionally filtered by chapter.

        Args:
            chapter: Optional chapter number to filter by

        Returns:
            List of characters
        """
        pass

    @abstractmethod
    def get_locations(self, chapter: Optional[int] = None) -> List[Location]:
        """Get all locations, optionally filtered by chapter.

        Args:
            chapter: Optional chapter number to filter by

        Returns:
            List of locations
        """
        pass

    @abstractmethod
    def get_plot_threads(self, status: Optional[str] = None) -> List[PlotThread]:
        """Get plot threads, optionally filtered by status.

        Args:
            status: Optional status to filter by

        Returns:
            List of plot threads
        """
        pass

    @abstractmethod
    def get_foreshadowing(self, status: Optional[str] = None) -> List[Foreshadowing]:
        """Get foreshadowing elements, optionally filtered by status.

        Args:
            status: Optional status to filter by

        Returns:
            List of foreshadowing elements
        """
        pass

    @abstractmethod
    def add_relationship(self, char1_id: str, char2_id: str, relationship_type: str) -> bool:
        """Add a relationship between two characters.

        Args:
            char1_id: First character ID
            char2_id: Second character ID
            relationship_type: Type of relationship

        Returns:
            True if successful
        """
        pass

    @abstractmethod
    def get_relationships(self, character_id: str) -> Dict[str, str]:
        """Get all relationships for a character.

        Args:
            character_id: Character ID

        Returns:
            Dict mapping character_id to relationship_type
        """
        pass

    @abstractmethod
    def track_chapter(self, chapter_number: int, entities_mentioned: List[str]) -> None:
        """Track entities mentioned in a chapter.

        Args:
            chapter_number: Chapter number
            entities_mentioned: List of entity IDs mentioned
        """
        pass

    @abstractmethod
    def get_chapter_summary(self, chapter_number: int) -> Dict[str, Any]:
        """Get summary of entities in a chapter.

        Args:
            chapter_number: Chapter number

        Returns:
            Summary of entities
        """
        pass

    @abstractmethod
    def export_memory(self, format: str = "json") -> str:
        """Export memory to a file.

        Args:
            format: Export format (json, yaml, etc.)

        Returns:
            Exported data as string
        """
        pass

    @abstractmethod
    def import_memory(self, data: str, format: str = "json") -> bool:
        """Import memory from a file.

        Args:
            data: Data to import
            format: Import format (json, yaml, etc.)

        Returns:
            True if successful
        """
        pass

    @classmethod
    def create(cls, engine_type: str = "vector", config: Optional[Dict[str, Any]] = None) -> "MemoryEngine":
        """Create a memory engine instance.

        Args:
            engine_type: Type of memory engine (vector, graph, etc.)
            config: Engine configuration

        Returns:
            MemoryEngine instance
        """
        from novel_agent.memory import get_memory_engine_class

        engine_class = get_memory_engine_class(engine_type)
        engine = engine_class()
        engine.initialize(config or {})
        return engine
