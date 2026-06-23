"""
Unit tests for memory engine.
"""

import pytest
from novel_agent.core.memory import (
    MemoryEngine,
    Entity,
    EntityType,
    MemoryQuery,
)


class TestMemoryEngine:
    """Test memory engine."""

    def test_memory_creation(self):
        """Test memory engine creation."""
        engine = MemoryEngine.create("vector")
        assert engine is not None

    def test_add_entity(self):
        """Test adding entity to memory."""
        engine = MemoryEngine.create("vector")
        entity = Entity(
            id="test_1",
            name="Test Entity",
            entity_type=EntityType.CHARACTER,
            description="A test character",
        )
        entity_id = engine.add_entity(entity)
        assert entity_id == "test_1"

    def test_get_entity(self):
        """Test getting entity from memory."""
        engine = MemoryEngine.create("vector")
        entity = Entity(
            id="test_2",
            name="Test Entity 2",
            entity_type=EntityType.LOCATION,
        )
        engine.add_entity(entity)

        retrieved = engine.get_entity("test_2")
        assert retrieved is not None
        assert retrieved.name == "Test Entity 2"

    def test_delete_entity(self):
        """Test deleting entity from memory."""
        engine = MemoryEngine.create("vector")
        entity = Entity(
            id="test_3",
            name="Test Entity 3",
            entity_type=EntityType.ITEM,
        )
        engine.add_entity(entity)

        success = engine.delete_entity("test_3")
        assert success is True

        retrieved = engine.get_entity("test_3")
        assert retrieved is None

    def test_query_memory(self):
        """Test querying memory."""
        engine = MemoryEngine.create("vector")
        entity = Entity(
            id="test_4",
            name="Alice",
            entity_type=EntityType.CHARACTER,
            description="A brave warrior",
        )
        engine.add_entity(entity)

        query = MemoryQuery(query="Alice", entity_type=EntityType.CHARACTER)
        results = engine.query(query)
        assert len(results) > 0


class TestEntityTypes:
    """Test entity types."""

    def test_entity_types(self):
        """Test entity type values."""
        assert EntityType.CHARACTER.value == "character"
        assert EntityType.LOCATION.value == "location"
        assert EntityType.ITEM.value == "item"
        assert EntityType.EVENT.value == "event"
