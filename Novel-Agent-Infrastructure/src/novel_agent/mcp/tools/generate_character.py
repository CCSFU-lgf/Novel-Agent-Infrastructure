"""
MCP Tool: Generate Character

This tool generates character profiles.
"""

from typing import Optional, Dict, Any, List

from novel_agent.mcp.tools.base import BaseTool, ToolResult


class GenerateCharacterTool(BaseTool):
    """Tool for generating character profiles."""

    async def execute(
        self,
        name: str,
        role: str = "protagonist",
        genre: str = "fantasy",
        traits: Optional[List[str]] = None,
    ) -> ToolResult:
        """Generate a character profile.

        Args:
            name: Character name
            role: Character role
            genre: Story genre
            traits: Optional character traits

        Returns:
            ToolResult with character profile
        """
        try:
            # Generate character profile
            profile = self._generate_profile(name, role, genre, traits or [])

            return self._success(
                data=profile,
                metadata={
                    "genre": genre,
                    "role": role,
                },
            )
        except Exception as e:
            return self._error(f"Character generation failed: {str(e)}")

    def _generate_profile(
        self,
        name: str,
        role: str,
        genre: str,
        traits: List[str],
    ) -> Dict[str, Any]:
        """Generate character profile.

        Args:
            name: Character name
            role: Character role
            genre: Story genre
            traits: Character traits

        Returns:
            Character profile
        """
        # Base profile
        profile = {
            "name": name,
            "role": role,
            "genre": genre,
            "personality": self._generate_personality(role, traits),
            "appearance": self._generate_appearance(role, genre),
            "background": self._generate_background(role, genre),
            "goals": self._generate_goals(role, genre),
            "relationships": self._generate_relationships(role),
            "abilities": self._generate_abilities(role, genre),
            "weaknesses": self._generate_weaknesses(role),
        }

        return profile

    def _generate_personality(self, role: str, traits: List[str]) -> List[str]:
        """Generate personality traits.

        Args:
            role: Character role
            traits: Requested traits

        Returns:
            Personality traits
        """
        base_traits = {
            "protagonist": ["determined", "compassionate", "curious"],
            "antagonist": ["ambitious", "cunning", "ruthless"],
            "supporting": ["loyal", "reliable", "wise"],
        }

        personality = base_traits.get(role, ["neutral"])
        personality.extend(traits[:3])  # Add up to 3 custom traits

        return personality

    def _generate_appearance(self, role: str, genre: str) -> str:
        """Generate appearance description.

        Args:
            role: Character role
            genre: Story genre

        Returns:
            Appearance description
        """
        appearances = {
            "protagonist": "A young person with determined eyes and a distinctive presence that draws attention.",
            "antagonist": "A figure with sharp features and an aura of authority that commands respect or fear.",
            "supporting": "An approachable person with kind eyes and a warm smile.",
        }

        return appearances.get(role, "An ordinary person with no distinctive features.")

    def _generate_background(self, role: str, genre: str) -> str:
        """Generate background story.

        Args:
            role: Character role
            genre: Story genre

        Returns:
            Background story
        """
        backgrounds = {
            "protagonist": "Born in humble circumstances, they discovered an extraordinary ability or destiny that would change their life forever.",
            "antagonist": "Once a promising individual, they were corrupted by power or tragedy, leading them down a dark path.",
            "supporting": "A loyal companion who has been by the protagonist's side through thick and thin.",
        }

        return backgrounds.get(role, "A mysterious past that remains largely unknown.")

    def _generate_goals(self, role: str, genre: str) -> List[str]:
        """Generate character goals.

        Args:
            role: Character role
            genre: Story genre

        Returns:
            Character goals
        """
        goals = {
            "protagonist": ["Protect loved ones", "Achieve their destiny", "Grow stronger"],
            "antagonist": ["Gain ultimate power", "Exact revenge", "Reshape the world"],
            "supporting": ["Support the protagonist", "Find their own purpose", "Maintain balance"],
        }

        return goals.get(role, ["Survive", "Find meaning"])

    def _generate_relationships(self, role: str) -> Dict[str, str]:
        """Generate relationship templates.

        Args:
            role: Character role

        Returns:
            Relationship templates
        """
        relationships = {
            "protagonist": {
                "mentor": "Guides and teaches",
                "rival": "Competes with",
                "love_interest": "Romantic connection",
            },
            "antagonist": {
                "protagonist": "Opposes",
                "subordinate": "Commands",
                "nemesis": "Bitter enemy",
            },
            "supporting": {
                "protagonist": "Supports and protects",
                "other_allies": "Works alongside",
            },
        }

        return relationships.get(role, {})

    def _generate_abilities(self, role: str, genre: str) -> List[str]:
        """Generate character abilities.

        Args:
            role: Character role
            genre: Story genre

        Returns:
            Character abilities
        """
        abilities = {
            "protagonist": ["Hidden potential", "Quick learner", "Natural talent"],
            "antagonist": ["Powerful magic", "Strategic mind", "Intimidation"],
            "supporting": ["Specialized skill", "Knowledge", "Support abilities"],
        }

        return abilities.get(role, ["Basic skills"])

    def _generate_weaknesses(self, role: str) -> List[str]:
        """Generate character weaknesses.

        Args:
            role: Character role

        Returns:
            Character weaknesses
        """
        weaknesses = {
            "protagonist": ["Inexperience", "Impulsive", "Too trusting"],
            "antagonist": ["Arrogance", "Obsession", "Blind spots"],
            "supporting": ["Loyalty can be exploited", "Self-doubt", "Limited power"],
        }

        return weaknesses.get(role, ["Unknown weaknesses"])


# Create singleton instance
generate_character = GenerateCharacterTool()
