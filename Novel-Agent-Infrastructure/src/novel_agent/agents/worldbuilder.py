"""
WorldBuilder Agent for Novel Agent Infrastructure.

This agent handles world-building and setting management.
"""

from typing import Optional, Dict, Any, List

from novel_agent.core.agent import Agent, AgentConfig, AgentTask, AgentResult, AgentMessage, AgentStatus


class WorldBuilderAgent(Agent):
    """Agent for world-building."""

    def __init__(self, config: AgentConfig):
        """Initialize worldbuilder agent."""
        super().__init__(config)
        self.capabilities = [
            "Create world settings",
            "Design magic systems",
            "Build cultures and societies",
            "Develop geography",
            "Establish world rules",
        ]

    async def execute(self, task: AgentTask) -> AgentResult:
        """Execute a worldbuilding task."""
        self.update_status(AgentStatus.WORKING)

        try:
            result = {
                "setting": {"type": "fantasy", "atmosphere": "mysterious"},
                "magic_system": {"type": "elemental", "rules": ["Conservation", "Limits"]},
                "geography": {"continents": ["Main continent"], "features": ["Mountains", "Forests"]},
                "cultures": [{"name": "Kingdom", "values": ["Honor", "Tradition"]}],
            }

            self.update_status(AgentStatus.COMPLETED)
            return AgentResult(task_id=task.id, agent_id=self.agent_id, status=AgentStatus.COMPLETED, output=result)
        except Exception as e:
            self.update_status(AgentStatus.ERROR)
            return AgentResult(task_id=task.id, agent_id=self.agent_id, status=AgentStatus.ERROR, output=None, reasoning=str(e))

    async def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        return None

    def get_capabilities(self) -> List[str]:
        return self.capabilities

    def get_system_prompt(self) -> str:
        return "You are a world-building expert. Create immersive, consistent fictional worlds."
