"""
Agent system for Novel Agent Infrastructure.

This module provides the multi-agent system for fiction creation.

Agent Types:
- Planner: High-level story planning
- Character: Character development
- WorldBuilder: World-building
- Outline: Chapter outlining
- Writer: Prose generation
- Editor: Quality control
- Publishing: Platform publishing
"""

from typing import Dict, Type
from novel_agent.core.agent import Agent, AgentType

# Registry of agents
_agent_registry: Dict[AgentType, Type[Agent]] = {}


def register_agent(agent_type: AgentType, agent_class: Type[Agent]) -> None:
    """Register an agent.

    Args:
        agent_type: Type of agent
        agent_class: Agent class
    """
    _agent_registry[agent_type] = agent_class


def get_agent_class(agent_type: AgentType) -> Type[Agent]:
    """Get agent class.

    Args:
        agent_type: Type of agent

    Returns:
        Agent class

    Raises:
        ValueError: If agent type is not registered
    """
    if agent_type not in _agent_registry:
        _load_agent(agent_type)

    if agent_type not in _agent_registry:
        raise ValueError(f"Unsupported agent type: {agent_type}")

    return _agent_registry[agent_type]


def _load_agent(agent_type: AgentType) -> None:
    """Lazy load an agent.

    Args:
        agent_type: Type of agent to load
    """
    if agent_type == AgentType.PLANNER:
        from novel_agent.agents.planner import PlannerAgent
        register_agent(agent_type, PlannerAgent)
    elif agent_type == AgentType.CHARACTER:
        from novel_agent.agents.character import CharacterAgent
        register_agent(agent_type, CharacterAgent)
    elif agent_type == AgentType.WORLDBUILDER:
        from novel_agent.agents.worldbuilder import WorldBuilderAgent
        register_agent(agent_type, WorldBuilderAgent)
    elif agent_type == AgentType.OUTLINE:
        from novel_agent.agents.outline import OutlineAgent
        register_agent(agent_type, OutlineAgent)
    elif agent_type == AgentType.WRITER:
        from novel_agent.agents.writer import WriterAgent
        register_agent(agent_type, WriterAgent)
    elif agent_type == AgentType.EDITOR:
        from novel_agent.agents.editor import EditorAgent
        register_agent(agent_type, EditorAgent)
    elif agent_type == AgentType.PUBLISHER:
        from novel_agent.agents.publisher import PublisherAgent
        register_agent(agent_type, PublisherAgent)


__all__ = [
    "register_agent",
    "get_agent_class",
]
