"""
MCP Tool: Story Memory

This tool manages story memory.
"""

from typing import Optional, Dict, Any, List

from novel_agent.mcp.tools.base import BaseTool, ToolResult
from novel_agent.core.memory import MemoryEngine, Entity, EntityType


class StoryMemoryTool(BaseTool):
    """Tool for managing story memory."""

    async def execute(
        self,
        action: str,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
        memory_engine: Optional[MemoryEngine] = None,
    ) -> ToolResult:
        """Manage story memory.

        Args:
            action: Action to perform
            entity_type: Type of entity
            entity_id: Entity ID
            data: Entity data
            memory_engine: Memory engine instance

        Returns:
            ToolResult with operation result
        """
        if not memory_engine:
            return self._error("Memory engine not initialized")

        try:
            if action == "add":
                return await self._add_entity(memory_engine, entity_type, data)
            elif action == "get":
                return await self._get_entity(memory_engine, entity_id)
            elif action == "update":
                return await self._update_entity(memory_engine, entity_id, data)
            elif action == "delete":
                return await self._delete_entity(memory_engine, entity_id)
            elif action == "query":
                return await self._query_memory(memory_engine, data)
            else:
                return self._error(f"Unknown action: {action}")
        except Exception as e:
            return self._error(f"Memory operation failed: {str(e)}")

    async def _add_entity(
        self,
        engine: MemoryEngine,
        entity_type: Optional[str],
        data: Optional[Dict[str, Any]],
    ) -> ToolResult:
        """Add an entity to memory.

        Args:
            engine: Memory engine
            entity_type: Entity type
            data: Entity data

        Returns:
            ToolResult
        """
        if not entity_type or not data:
            return self._error("Entity type and data required for add action")

        try:
            etype = EntityType(entity_type)
            entity = Entity(
                id=data.get("id", "auto"),
                name=data.get("name", "Unknown"),
                entity_type=etype,
                description=data.get("description"),
                attributes=data.get("attributes", {}),
            )
            entity_id = engine.add_entity(entity)

            return self._success(
                data={"entity_id": entity_id, "message": "Entity added successfully"},
            )
        except Exception as e:
            return self._error(f"Failed to add entity: {str(e)}")

    async def _get_entity(
        self,
        engine: MemoryEngine,
        entity_id: Optional[str],
    ) -> ToolResult:
        """Get an entity from memory.

        Args:
            engine: Memory engine
            entity_id: Entity ID

        Returns:
            ToolResult
        """
        if not entity_id:
            return self._error("Entity ID required for get action")

        entity = engine.get_entity(entity_id)
        if entity:
            return self._success(data=entity.model_dump())
        else:
            return self._error(f"Entity not found: {entity_id}")

    async def _update_entity(
        self,
        engine: MemoryEngine,
        entity_id: Optional[str],
        data: Optional[Dict[str, Any]],
    ) -> ToolResult:
        """Update an entity in memory.

        Args:
            engine: Memory engine
            entity_id: Entity ID
            data: Update data

        Returns:
            ToolResult
        """
        if not entity_id or not data:
            return self._error("Entity ID and data required for update action")

        success = engine.update_entity(entity_id, data)
        if success:
            return self._success(data={"message": "Entity updated successfully"})
        else:
            return self._error(f"Failed to update entity: {entity_id}")

    async def _delete_entity(
        self,
        engine: MemoryEngine,
        entity_id: Optional[str],
    ) -> ToolResult:
        """Delete an entity from memory.

        Args:
            engine: Memory engine
            entity_id: Entity ID

        Returns:
            ToolResult
        """
        if not entity_id:
            return self._error("Entity ID required for delete action")

        success = engine.delete_entity(entity_id)
        if success:
            return self._success(data={"message": "Entity deleted successfully"})
        else:
            return self._error(f"Failed to delete entity: {entity_id}")

    async def _query_memory(
        self,
        engine: MemoryEngine,
        data: Optional[Dict[str, Any]],
    ) -> ToolResult:
        """Query memory for entities.

        Args:
            engine: Memory engine
            data: Query parameters

        Returns:
            ToolResult
        """
        if not data:
            return self._error("Query data required for query action")

        from novel_agent.core.memory import MemoryQuery

        query = MemoryQuery(
            query=data.get("query", ""),
            entity_type=data.get("entity_type"),
            limit=data.get("limit", 10),
        )

        results = engine.query(query)

        return self._success(
            data={
                "results": [r.model_dump() for r in results],
                "count": len(results),
            },
        )


# Create singleton instance
story_memory = StoryMemoryTool()
