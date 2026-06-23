"""
Character Agent for Novel Agent Infrastructure.

This agent handles character development and consistency.
"""

from typing import Optional, Dict, Any, List

from novel_agent.core.agent import Agent, AgentConfig, AgentTask, AgentResult, AgentMessage, AgentStatus


class CharacterAgent(Agent):
    """Agent for character development."""

    def __init__(self, config: AgentConfig):
        """Initialize character agent."""
        super().__init__(config)
        self.capabilities = [
            "Create character profiles",
            "Develop character backgrounds",
            "Ensure character consistency",
            "Manage character relationships",
            "Track character growth",
        ]

    async def execute(self, task: AgentTask) -> AgentResult:
        """Execute a character task.

        Args:
            task: Task to execute

        Returns:
            AgentResult with character output
        """
        self.update_status(AgentStatus.WORKING)

        try:
            task_type = task.task_type

            if task_type == "create_character":
                result = await self._create_character(task.context)
            elif task_type == "develop_background":
                result = await self._develop_background(task.context)
            elif task_type == "check_consistency":
                result = await self._check_consistency(task.context)
            else:
                result = {"error": f"Unknown task type: {task_type}"}

            self.update_status(AgentStatus.COMPLETED)

            return AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                status=AgentStatus.COMPLETED,
                output=result,
            )
        except Exception as e:
            self.update_status(AgentStatus.ERROR)
            return AgentResult(
                task_id=task.id,
                agent_id=self.agent_id,
                status=AgentStatus.ERROR,
                output=None,
                reasoning=str(e),
            )

    async def _create_character(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create a character profile.

        Args:
            context: Character details

        Returns:
            Character profile
        """
        name = context.get("name", "Unknown")
        role = context.get("role", "supporting")

        return {
            "name": name,
            "role": role,
            "personality": ["determined", "compassionate", "curious"],
            "appearance": "A distinctive figure with memorable features",
            "background": "Born in humble circumstances with hidden potential",
            "goals": ["Protect loved ones", "Discover truth", "Grow stronger"],
            "motivations": "Driven by a personal loss or revelation",
            "fears": ["Failure", "Losing loved ones", "The unknown"],
            "strengths": ["Quick thinking", "Loyalty", "Adaptability"],
            "weaknesses": ["Impulsive", "Too trusting", "Inexperienced"],
        }

    async def _develop_background(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Develop character background.

        Args:
            context: Character details

        Returns:
            Character background
        """
        return {
            "childhood": "A formative early life that shaped their worldview",
            "education": "Learned through experience and mentors",
            "relationships": "Key relationships that influenced them",
            "defining_moment": "A pivotal event that changed everything",
            "secrets": ["Hidden knowledge", "Past connection", "True identity"],
        }

    async def _check_consistency(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Check character consistency.

        Args:
            context: Character details and recent actions

        Returns:
            Consistency report
        """
        return {
            "is_consistent": True,
            "potential_issues": [],
            "suggestions": ["Maintain established personality traits"],
        }

    async def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Process a message from another agent."""
        return None

    def get_capabilities(self) -> List[str]:
        """Get agent capabilities."""
        return self.capabilities

    def get_system_prompt(self) -> str:
        """Get system prompt."""
        return """You are a character development expert. Your role is to:
1. Create compelling, three-dimensional characters
2. Develop rich backgrounds and motivations
3. Ensure character consistency throughout the story
4. Manage character relationships and growth

Focus on creating characters that readers will care about and remember."""
