"""
Graph-based memory engine for Novel Agent Infrastructure.

This module provides graph-based relationship tracking for story memory.
"""

from typing import Optional, Dict, Any, List
from collections import defaultdict

from novel_agent.core.memory import (
    MemoryEngine,
    Entity,
    EntityType,
    Character,
    Location,
    PlotThread,
    Foreshadowing,
    MemoryQuery,
    MemoryResult,
)


class GraphMemoryEngine(MemoryEngine):
    """Graph-based memory engine for relationship tracking."""

    def __init__(self):
        """Initialize graph memory engine."""
        self.entities: Dict[str, Entity] = {}
        self.relationships: Dict[str, Dict[str, str]] = defaultdict(dict)
        self.chapters: Dict[int, List[str]] = defaultdict(list)

    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the graph memory engine.

        Args:
            config: Configuration
        """
        self.config = config

    def add_entity(self, entity: Entity) -> str:
        """Add an entity to memory.

        Args:
            entity: Entity to add

        Returns:
            Entity ID
        """
        self.entities[entity.id] = entity
        return entity.id

    def update_entity(self, entity_id: str, updates: Dict[str, Any]) -> bool:
        """Update an entity in memory.

        Args:
            entity_id: ID of entity to update
            updates: Fields to update

        Returns:
            True if successful
        """
        if entity_id not in self.entities:
            return False

        entity = self.entities[entity_id]
        for key, value in updates.items():
            if hasattr(entity, key):
                setattr(entity, key, value)

        return True

    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """Get an entity by ID.

        Args:
            entity_id: ID of entity to retrieve

        Returns:
            Entity if found, None otherwise
        """
        return self.entities.get(entity_id)

    def delete_entity(self, entity_id: str) -> bool:
        """Delete an entity from memory.

        Args:
            entity_id: ID of entity to delete

        Returns:
            True if successful
        """
        if entity_id in self.entities:
            del self.entities[entity_id]

            # Remove relationships
            if entity_id in self.relationships:
                del self.relationships[entity_id]

            # Remove from other entities' relationships
            for other_id in self.relationships:
                if entity_id in self.relationships[other_id]:
                    del self.relationships[other_id][entity_id]

            return True
        return False

    def query(self, query: MemoryQuery) -> List[MemoryResult]:
        """Query memory for relevant entities.

        Args:
            query: Memory query

        Returns:
            List of relevant entities
        """
        results = []
        query_lower = query.query.lower()

        for entity in self.entities.values():
            # Check entity type filter
            if query.entity_type and entity.entity_type != query.entity_type:
                continue

            # Check chapter range filter
            if query.chapter_range:
                chapter = entity.chapter_introduced or 0
                if not (query.chapter_range[0] <= chapter <= query.chapter_range[1]):
                    continue

            # Check tags filter
            if query.tags and not any(tag in entity.tags for tag in query.tags):
                continue

            # Simple text matching
            if query_lower in entity.name.lower() or (entity.description and query_lower in entity.description.lower()):
                results.append(MemoryResult(
                    entity=entity,
                    similarity=1.0,
                ))

        return results[:query.limit]

    def get_characters(self, chapter: Optional[int] = None) -> List[Character]:
        """Get all characters."""
        characters = []
        for entity in self.entities.values():
            if entity.entity_type == EntityType.CHARACTER:
                if chapter is None or entity.chapter_introduced == chapter:
                    characters.append(entity)
        return characters

    def get_locations(self, chapter: Optional[int] = None) -> List[Location]:
        """Get all locations."""
        locations = []
        for entity in self.entities.values():
            if entity.entity_type == EntityType.LOCATION:
                if chapter is None or entity.chapter_introduced == chapter:
                    locations.append(entity)
        return locations

    def get_plot_threads(self, status: Optional[str] = None) -> List[PlotThread]:
        """Get plot threads."""
        threads = []
        for entity in self.entities.values():
            if entity.entity_type == EntityType.PLOT_THREAD:
                if status is None or entity.attributes.get("status") == status:
                    threads.append(entity)
        return threads

    def get_foreshadowing(self, status: Optional[str] = None) -> List[Foreshadowing]:
        """Get foreshadowing elements."""
        elements = []
        for entity in self.entities.values():
            if entity.entity_type == EntityType.FORESHADOWING:
                if status is None or entity.attributes.get("status") == status:
                    elements.append(entity)
        return elements

    def add_relationship(self, char1_id: str, char2_id: str, relationship_type: str) -> bool:
        """Add a relationship between two characters.

        Args:
            char1_id: First character ID
            char2_id: Second character ID
            relationship_type: Type of relationship

        Returns:
            True if successful
        """
        if char1_id in self.entities and char2_id in self.entities:
            self.relationships[char1_id][char2_id] = relationship_type
            self.relationships[char2_id][char1_id] = relationship_type
            return True
        return False

    def get_relationships(self, character_id: str) -> Dict[str, str]:
        """Get all relationships for a character.

        Args:
            character_id: Character ID

        Returns:
            Dict mapping character_id to relationship_type
        """
        return dict(self.relationships.get(character_id, {}))

    def track_chapter(self, chapter_number: int, entities_mentioned: List[str]) -> None:
        """Track entities mentioned in a chapter.

        Args:
            chapter_number: Chapter number
            entities_mentioned: List of entity IDs mentioned
        """
        self.chapters[chapter_number].extend(entities_mentioned)

        # Update entity chapter tracking
        for entity_id in entities_mentioned:
            if entity_id in self.entities:
                entity = self.entities[entity_id]
                if not hasattr(entity, "chapters_mentioned"):
                    entity.chapters_mentioned = []
                if chapter_number not in entity.chapters_mentioned:
                    entity.chapters_mentioned.append(chapter_number)

    def get_chapter_summary(self, chapter_number: int) -> Dict[str, Any]:
        """Get summary of entities in a chapter.

        Args:
            chapter_number: Chapter number

        Returns:
            Summary of entities
        """
        mentioned = self.chapters.get(chapter_number, [])

        return {
            "chapter": chapter_number,
            "entities_mentioned": mentioned,
            "count": len(mentioned),
        }

    def export_memory(self, format: str = "json") -> str:
        """Export memory to a file.

        Args:
            format: Export format

        Returns:
            Exported data as string
        """
        import json

        data = {
            "entities": {k: v.model_dump() for k, v in self.entities.items()},
            "relationships": {k: dict(v) for k, v in self.relationships.items()},
            "chapters": {k: v for k, v in self.chapters.items()},
        }

        if format == "json":
            return json.dumps(data, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def import_memory(self, data: str, format: str = "json") -> bool:
        """Import memory from a file.

        Args:
            data: Data to import
            format: Import format

        Returns:
            True if successful
        """
        import json

        if format == "json":
            parsed = json.loads(data)

            # Import entities
            entities_data = parsed.get("entities", {})
            for entity_id, entity_data in entities_data.items():
                entity_type = entity_data.get("entity_type")
                if entity_type == "character":
                    entity = Character(**entity_data)
                elif entity_type == "location":
                    entity = Location(**entity_data)
                else:
                    entity = Entity(**entity_data)
                self.entities[entity_id] = entity

            # Import relationships
            relationships_data = parsed.get("relationships", {})
            for char_id, rels in relationships_data.items():
                self.relationships[char_id] = rels

            # Import chapters
            chapters_data = parsed.get("chapters", {})
            for chapter_num, entities in chapters_data.items():
                self.chapters[int(chapter_num)] = entities

            return True
        else:
            raise ValueError(f"Unsupported format: {format}")

    def get_connected_entities(self, entity_id: str, depth: int = 1) -> List[Entity]:
        """Get entities connected to a given entity.

        Args:
            entity_id: Starting entity ID
            depth: How many levels of connections to traverse

        Returns:
            List of connected entities
        """
        visited = set()
        result = []

        def traverse(current_id: str, current_depth: int):
            if current_depth > depth or current_id in visited:
                return

            visited.add(current_id)
            if current_id in self.entities:
                result.append(self.entities[current_id])

            # Get direct connections
            for related_id in self.relationships.get(current_id, {}):
                traverse(related_id, current_depth + 1)

        traverse(entity_id, 0)
        return result

    def find_path(self, start_id: str, end_id: str) -> Optional[List[str]]:
        """Find path between two entities.

        Args:
            start_id: Starting entity ID
            end_id: Ending entity ID

        Returns:
            Path as list of entity IDs, or None if no path exists
        """
        if start_id not in self.entities or end_id not in self.entities:
            return None

        visited = set()
        queue = [[start_id]]

        while queue:
            path = queue.pop(0)
            current = path[-1]

            if current == end_id:
                return path

            if current in visited:
                continue

            visited.add(current)

            for related_id in self.relationships.get(current, {}):
                if related_id not in visited:
                    queue.append(path + [related_id])

        return None
