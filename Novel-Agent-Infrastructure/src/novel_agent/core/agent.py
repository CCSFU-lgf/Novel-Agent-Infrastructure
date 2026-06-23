"""
Agent system for Novel Agent Infrastructure.

This module provides the agent framework for multi-agent fiction creation
workflows.

Agent Types:
- Planner: High-level story planning
- Character: Character development and consistency
- WorldBuilder: World-building and setting management
- Outline: Chapter and scene outlining
- Writer: Actual prose generation
- Editor: Quality control and consistency checking
- Publishing: Platform-specific publishing

Example:
    >>> from novel_agent.core.agent import Agent, AgentConfig
    >>> config = AgentConfig(agent_type="writer", model="gpt-4")
    >>> agent = Agent.create(config)
    >>> agent.execute(task="Write chapter 1", context={...})
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Dict, Any, List, Callable, Awaitable
from pydantic import BaseModel, Field
from datetime import datetime


class AgentType(str, Enum):
    """Types of agents."""

    PLANNER = "planner"
    CHARACTER = "character"
    WORLDBUILDER = "worldbuilder"
    OUTLINE = "outline"
    WRITER = "writer"
    EDITOR = "editor"
    PUBLISHER = "publisher"


class AgentStatus(str, Enum):
    """Agent status."""

    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    ERROR = "error"
    COMPLETED = "completed"


class AgentConfig(BaseModel):
    """Agent configuration."""

    agent_type: AgentType
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 4096
    system_prompt: Optional[str] = None
    tools: List[str] = Field(default_factory=list)
    memory_enabled: bool = True
    collaboration_enabled: bool = True
    max_iterations: int = 10
    timeout: int = 300  # seconds


class AgentMessage(BaseModel):
    """Message between agents."""

    id: str
    sender: str
    receiver: str
    content: str
    message_type: str = "task"  # task, response, feedback, query
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AgentTask(BaseModel):
    """Task for an agent."""

    id: str
    task_type: str
    description: str
    context: Dict[str, Any] = Field(default_factory=dict)
    priority: int = 1  # 1-10
    deadline: Optional[datetime] = None
    dependencies: List[str] = Field(default_factory=list)  # task IDs


class AgentResult(BaseModel):
    """Result from an agent."""

    task_id: str
    agent_id: str
    status: AgentStatus
    output: Any
    reasoning: Optional[str] = None
    confidence: float = 1.0
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)


class Agent(ABC):
    """Abstract base class for agents."""

    def __init__(self, config: AgentConfig):
        """Initialize agent.

        Args:
            config: Agent configuration
        """
        self.config = config
        self.agent_id = f"{config.agent_type.value}_{id(self)}"
        self.status = AgentStatus.IDLE
        self.memory: List[Dict[str, Any]] = []
        self.message_queue: List[AgentMessage] = []

    @abstractmethod
    async def execute(self, task: AgentTask) -> AgentResult:
        """Execute a task.

        Args:
            task: Task to execute

        Returns:
            AgentResult with output
        """
        pass

    @abstractmethod
    async def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Process a message from another agent.

        Args:
            message: Message to process

        Returns:
            Optional response message
        """
        pass

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Get agent capabilities.

        Returns:
            List of capability descriptions
        """
        pass

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent.

        Returns:
            System prompt string
        """
        pass

    def send_message(self, receiver: str, content: str, message_type: str = "task") -> AgentMessage:
        """Send a message to another agent.

        Args:
            receiver: Receiver agent ID
            content: Message content
            message_type: Type of message

        Returns:
            Created message
        """
        message = AgentMessage(
            id=f"msg_{id(self)}_{len(self.message_queue)}",
            sender=self.agent_id,
            receiver=receiver,
            content=content,
            message_type=message_type,
        )
        self.message_queue.append(message)
        return message

    def receive_message(self, message: AgentMessage) -> None:
        """Receive a message from another agent.

        Args:
            message: Message to receive
        """
        self.message_queue.append(message)

    def update_status(self, status: AgentStatus) -> None:
        """Update agent status.

        Args:
            status: New status
        """
        self.status = status

    def add_to_memory(self, entry: Dict[str, Any]) -> None:
        """Add an entry to agent memory.

        Args:
            entry: Memory entry
        """
        self.memory.append(entry)

    def get_memory(self, query: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get agent memory.

        Args:
            query: Optional query to filter memory

        Returns:
            List of memory entries
        """
        if query is None:
            return self.memory
        # Simple keyword search - can be enhanced with vector search
        return [m for m in self.memory if query.lower() in str(m).lower()]

    def clear_memory(self) -> None:
        """Clear agent memory."""
        self.memory.clear()

    @classmethod
    def create(cls, config: AgentConfig) -> "Agent":
        """Create an agent instance.

        Args:
            config: Agent configuration

        Returns:
            Agent instance

        Raises:
            ValueError: If agent type is not supported
        """
        from novel_agent.agents import get_agent_class

        agent_class = get_agent_class(config.agent_type)
        return agent_class(config)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.agent_id} status={self.status}>"
