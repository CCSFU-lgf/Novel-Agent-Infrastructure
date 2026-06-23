"""
Vector-based memory engine for Novel Agent Infrastructure.

This module provides vector-based semantic search for story memory.
"""

from typing import Optional, Dict, Any, List
from pathlib import Path

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


class VectorMemoryEngine(MemoryEngine):
    """Vector-based memory engine using ChromaDB."""

    def __init__(self):
        """Initialize vector memory engine."""
        self.client = None
        self.collection = None
        self.entities: Dict[str, Entity] = {}
        self.config: Dict[str, Any] = {}

    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the vector memory engine.

        Args:
            config: Configuration including vector_db, embedding_model, etc.
        """
        self.config = config
        persist_directory = config.get("persist_directory", "./data/memory")

        try:
            import chromadb
            from chromadb.config import Settings

            # Create persist directory
            Path(persist_directory).mkdir(parents=True, exist_ok=True)

            # Initialize ChromaDB
            self.client = chromadb.Client(Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=persist_directory,
                anonymized_telemetry=False,
            ))

            # Get or create collection
            collection_name = config.get("collection_name", "novel_memory")
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"},
            )
        except ImportError:
            # Fallback to in-memory storage
            self.client = None
            self.collection = None

    def add_entity(self, entity: Entity) -> str:
        """Add an entity to memory.

        Args:
            entity: Entity to add

        Returns:
            Entity ID
        """
        self.entities[entity.id] = entity

        if self.collection:
            # Add to vector store
            doc = f"{entity.name} {entity.description or ''} {' '.join(entity.tags)}"
            self.collection.add(
                ids=[entity.id],
                documents=[doc],
                metadatas=[{
                    "entity_type": entity.entity_type.value,
                    "name": entity.name,
                }],
            )

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

            if self.collection:
                try:
                    self.collection.delete(ids=[entity_id])
                except Exception:
                    pass

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

        if self.collection and query.query:
            # Vector search
            query_results = self.collection.query(
                query_texts=[query.query],
                n_results=query.limit,
            )

            for i, doc_id in enumerate(query_results["ids"][0]):
                entity = self.entities.get(doc_id)
                if entity:
                    similarity = 1.0 - query_results["distances"][0][i]
                    if similarity >= query.similarity_threshold:
                        results.append(MemoryResult(
                            entity=entity,
                            similarity=similarity,
                        ))
        else:
            # Fallback to simple search
            query_lower = query.query.lower()
            for entity in self.entities.values():
                if query_lower in entity.name.lower() or (entity.description and query_lower in entity.description.lower()):
                    if query.entity_type is None or entity.entity_type == query.entity_type:
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
        """Add a relationship between two characters."""
        if char1_id in self.entities and char2_id in self.entities:
            char1 = self.entities[char1_id]
            char2 = self.entities[char2_id]

            if not hasattr(char1, "relationships"):
                char1.relationships = {}
            if not hasattr(char2, "relationships"):
                char2.relationships = {}

            char1.relationships[char2_id] = relationship_type
            char2.relationships[char1_id] = relationship_type

            return True
        return False

    def get_relationships(self, character_id: str) -> Dict[str, str]:
        """Get all relationships for a character."""
        if character_id in self.entities:
            entity = self.entities[character_id]
            if hasattr(entity, "relationships"):
                return entity.relationships
        return {}

    def track_chapter(self, chapter_number: int, entities_mentioned: List[str]) -> None:
        """Track entities mentioned in a chapter."""
        # Update chapter tracking in entities
        for entity_id in entities_mentioned:
            if entity_id in self.entities:
                entity = self.entities[entity_id]
                if not hasattr(entity, "chapters_mentioned"):
                    entity.chapters_mentioned = []
                entity.chapters_mentioned.append(chapter_number)

    def get_chapter_summary(self, chapter_number: int) -> Dict[str, Any]:
        """Get summary of entities in a chapter."""
        mentioned = []
        for entity in self.entities.values():
            if hasattr(entity, "chapters_mentioned") and chapter_number in entity.chapters_mentioned:
                mentioned.append(entity.id)

        return {
            "chapter": chapter_number,
            "entities_mentioned": mentioned,
            "count": len(mentioned),
        }

    def export_memory(self, format: str = "json") -> str:
        """Export memory to a file."""
        import json

        data = {
            "entities": {k: v.model_dump() for k, v in self.entities.items()},
        }

        if format == "json":
            return json.dumps(data, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def import_memory(self, data: str, format: str = "json") -> bool:
        """Import memory from a file."""
        import json

        if format == "json":
            parsed = json.loads(data)
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

            return True
        else:
            raise ValueError(f"Unsupported format: {format}")
