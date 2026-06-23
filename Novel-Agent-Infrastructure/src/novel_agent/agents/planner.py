"""
Planner Agent for Novel Agent Infrastructure.

This agent handles high-level story planning.
"""

from typing import Optional, Dict, Any, List

from novel_agent.core.agent import Agent, AgentConfig, AgentTask, AgentResult, AgentMessage, AgentStatus


class PlannerAgent(Agent):
    """Agent for high-level story planning."""

    def __init__(self, config: AgentConfig):
        """Initialize planner agent."""
        super().__init__(config)
        self.capabilities = [
            "Create story concepts",
            "Develop plot outlines",
            "Plan character arcs",
            "Structure story acts",
            "Define themes and motifs",
        ]

    async def execute(self, task: AgentTask) -> AgentResult:
        """Execute a planning task.

        Args:
            task: Task to execute

        Returns:
            AgentResult with planning output
        """
        self.update_status(AgentStatus.WORKING)

        try:
            task_type = task.task_type

            if task_type == "create_concept":
                result = await self._create_concept(task.context)
            elif task_type == "develop_outline":
                result = await self._develop_outline(task.context)
            elif task_type == "plan_character_arcs":
                result = await self._plan_character_arcs(task.context)
            elif task_type == "structure_acts":
                result = await self._structure_acts(task.context)
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

    async def _create_concept(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create a story concept.

        Args:
            context: Context with genre, themes, etc.

        Returns:
            Story concept
        """
        genre = context.get("genre", "fantasy")
        themes = context.get("themes", [])

        return {
            "title_suggestions": [
                "The Last Guardian",
                "Echoes of Destiny",
                "Shadows of the Forgotten",
            ],
            "premise": "A young protagonist discovers they have a unique ability...",
            "hook": "What if the chosen one refused their destiny?",
            "themes": themes or ["growth", "sacrifice", "identity"],
            "target_audience": "Young Adult",
            "comparable_works": [],
        }

    async def _develop_outline(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Develop a story outline.

        Args:
            context: Context with concept details

        Returns:
            Story outline
        """
        chapters = context.get("target_chapters", 100)

        return {
            "total_chapters": chapters,
            "acts": [
                {"name": "Act 1: Setup", "chapters": f"1-{chapters//3}", "purpose": "Introduce world and characters"},
                {"name": "Act 2: Confrontation", "chapters": f"{chapters//3+1}-{2*chapters//3}", "purpose": "Develop conflicts"},
                {"name": "Act 3: Resolution", "chapters": f"{2*chapters//3+1}-{chapters}", "purpose": "Resolve story"},
            ],
            "major_turning_points": [
                {"chapter": chapters//10, "event": "Inciting incident"},
                {"chapter": chapters//2, "event": "Midpoint reversal"},
                {"chapter": 3*chapters//4, "event": "Dark moment"},
            ],
        }

    async def _plan_character_arcs(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Plan character arcs.

        Args:
            context: Context with character details

        Returns:
            Character arc plans
        """
        characters = context.get("characters", [])

        arcs = {}
        for char in characters[:5]:  # Limit to 5 characters
            arcs[char] = {
                "start": "Initial state",
                "growth": "Key development moments",
                "end": "Final transformation",
            }

        return {"character_arcs": arcs}

    async def _structure_acts(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Structure story acts.

        Args:
            context: Context with outline details

        Returns:
            Act structure
        """
        return {
            "structure": "three_act",
            "pacing": "progressive",
            "tension_curve": "rising",
        }

    async def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Process a message from another agent.

        Args:
            message: Message to process

        Returns:
            Optional response
        """
        # Handle messages from other agents
        if message.message_type == "query":
            return self.send_message(
                message.sender,
                "Planning information available",
                "response",
            )
        return None

    def get_capabilities(self) -> List[str]:
        """Get agent capabilities."""
        return self.capabilities

    def get_system_prompt(self) -> str:
        """Get system prompt."""
        return """You are a story planning expert. Your role is to:
1. Create compelling story concepts
2. Develop detailed outlines
3. Plan character arcs
4. Structure acts and pacing

Focus on creating engaging, marketable stories that resonate with readers."""
