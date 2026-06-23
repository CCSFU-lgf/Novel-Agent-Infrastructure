"""
Story management for Novel Agent Infrastructure.

This module provides story creation, management, and persistence.

Example:
    >>> from novel_agent.core.story import Story, StoryConfig
    >>> config = StoryConfig(title="My Novel", genre="fantasy")
    >>> story = Story.create(config)
    >>> story.add_chapter("Chapter 1", "Once upon a time...")
"""

from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime

from novel_agent.core.platform import PlatformType, Genre, Tag
from novel_agent.core.memory import MemoryEngine


class StoryStatus(str, Enum):
    """Story status."""

    PLANNING = "planning"
    OUTLINING = "outlining"
    WRITING = "writing"
    EDITING = "editing"
    PUBLISHING = "publishing"
    COMPLETED = "completed"
    HIATUS = "hiatus"
    ABANDONED = "abandoned"


class StoryConfig(BaseModel):
    """Story configuration."""

    title: str
    title_zh: Optional[str] = None
    genre: str
    subgenre: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    target_word_count: Optional[int] = None
    target_chapters: Optional[int] = None
    platform: PlatformType = PlatformType.ROYALROAD
    language: str = "en"
    author: Optional[str] = None
    description: Optional[str] = None


class Chapter(BaseModel):
    """Chapter in a story."""

    id: str
    number: int
    title: str
    content: str
    word_count: int
    status: str = "draft"  # draft, revised, final
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Character(BaseModel):
    """Character in a story."""

    id: str
    name: str
    role: str  # protagonist, antagonist, supporting, minor
    description: Optional[str] = None
    personality: List[str] = Field(default_factory=list)
    appearance: Optional[str] = None
    background: Optional[str] = None
    goals: List[str] = Field(default_factory=list)
    relationships: Dict[str, str] = Field(default_factory=dict)
    chapter_introduced: int = 1


class WorldElement(BaseModel):
    """World-building element."""

    id: str
    name: str
    element_type: str  # location, organization, item, magic_system, etc.
    description: str
    attributes: Dict[str, Any] = Field(default_factory=dict)
    chapter_introduced: int = 1
    related_elements: List[str] = Field(default_factory=list)


class PlotThread(BaseModel):
    """Plot thread in a story."""

    id: str
    name: str
    description: str
    status: str = "active"  # active, resolved, abandoned
    importance: int = 1  # 1-10
    chapters_involved: List[int] = Field(default_factory=list)
    related_characters: List[str] = Field(default_factory=list)
    resolution: Optional[str] = None


class Outline(BaseModel):
    """Story outline."""

    id: str
    chapters: List[Dict[str, Any]] = Field(default_factory=list)
    major_plot_points: List[str] = Field(default_factory=list)
    character_arcs: Dict[str, List[str]] = Field(default_factory=dict)
    world_building_notes: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Story:
    """Main story class."""

    def __init__(self, config: StoryConfig, memory_engine: Optional[MemoryEngine] = None):
        """Initialize story.

        Args:
            config: Story configuration
            memory_engine: Optional memory engine for persistence
        """
        self.config = config
        self.memory = memory_engine or MemoryEngine.create("vector")
        self.chapters: List[Chapter] = []
        self.characters: Dict[str, Character] = {}
        self.world_elements: Dict[str, WorldElement] = {}
        self.plot_threads: Dict[str, PlotThread] = {}
        self.outline: Optional[Outline] = None
        self.status = StoryStatus.PLANNING
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def add_chapter(self, title: str, content: str, notes: Optional[str] = None) -> Chapter:
        """Add a chapter to the story.

        Args:
            title: Chapter title
            content: Chapter content
            notes: Optional notes

        Returns:
            Created chapter
        """
        chapter = Chapter(
            id=f"ch_{len(self.chapters) + 1}",
            number=len(self.chapters) + 1,
            title=title,
            content=content,
            word_count=len(content.split()),
            notes=notes,
        )
        self.chapters.append(chapter)
        self.updated_at = datetime.now()

        # Track in memory
        self.memory.track_chapter(chapter.number, [])

        return chapter

    def add_character(self, name: str, role: str, **kwargs) -> Character:
        """Add a character to the story.

        Args:
            name: Character name
            role: Character role
            **kwargs: Additional character attributes

        Returns:
            Created character
        """
        character = Character(
            id=f"char_{len(self.characters) + 1}",
            name=name,
            role=role,
            chapter_introduced=len(self.chapters) + 1,
            **kwargs,
        )
        self.characters[character.id] = character

        # Add to memory
        self.memory.add_entity(character)

        return character

    def add_world_element(self, name: str, element_type: str, description: str, **kwargs) -> WorldElement:
        """Add a world-building element.

        Args:
            name: Element name
            element_type: Type of element
            description: Element description
            **kwargs: Additional attributes

        Returns:
            Created world element
        """
        element = WorldElement(
            id=f"world_{len(self.world_elements) + 1}",
            name=name,
            element_type=element_type,
            description=description,
            chapter_introduced=len(self.chapters) + 1,
            **kwargs,
        )
        self.world_elements[element.id] = element

        # Add to memory
        self.memory.add_entity(element)

        return element

    def add_plot_thread(self, name: str, description: str, importance: int = 1) -> PlotThread:
        """Add a plot thread.

        Args:
            name: Plot thread name
            description: Plot thread description
            importance: Importance level (1-10)

        Returns:
            Created plot thread
        """
        thread = PlotThread(
            id=f"plot_{len(self.plot_threads) + 1}",
            name=name,
            description=description,
            importance=importance,
        )
        self.plot_threads[thread.id] = thread

        # Add to memory
        self.memory.add_entity(thread)

        return thread

    def set_outline(self, outline: Outline) -> None:
        """Set the story outline.

        Args:
            outline: Story outline
        """
        self.outline = outline
        self.status = StoryStatus.OUTLINING

    def get_word_count(self) -> int:
        """Get total word count.

        Returns:
            Total word count
        """
        return sum(chapter.word_count for chapter in self.chapters)

    def get_chapter_count(self) -> int:
        """Get total chapter count.

        Returns:
            Total chapter count
        """
        return len(self.chapters)

    def get_character(self, name: str) -> Optional[Character]:
        """Get a character by name.

        Args:
            name: Character name

        Returns:
            Character if found, None otherwise
        """
        for character in self.characters.values():
            if character.name.lower() == name.lower():
                return character
        return None

    def get_characters_by_role(self, role: str) -> List[Character]:
        """Get characters by role.

        Args:
            role: Character role

        Returns:
            List of characters with that role
        """
        return [c for c in self.characters.values() if c.role == role]

    def get_active_plot_threads(self) -> List[PlotThread]:
        """Get active plot threads.

        Returns:
            List of active plot threads
        """
        return [t for t in self.plot_threads.values() if t.status == "active"]

    def get_summary(self) -> Dict[str, Any]:
        """Get story summary.

        Returns:
            Story summary
        """
        return {
            "title": self.config.title,
            "genre": self.config.genre,
            "status": self.status.value,
            "chapter_count": self.get_chapter_count(),
            "word_count": self.get_word_count(),
            "character_count": len(self.characters),
            "world_element_count": len(self.world_elements),
            "active_plot_threads": len(self.get_active_plot_threads()),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def export(self, format: str = "json") -> str:
        """Export story data.

        Args:
            format: Export format

        Returns:
            Exported data
        """
        import json

        data = {
            "config": self.config.model_dump(),
            "chapters": [ch.model_dump() for ch in self.chapters],
            "characters": {k: v.model_dump() for k, v in self.characters.items()},
            "world_elements": {k: v.model_dump() for k, v in self.world_elements.items()},
            "plot_threads": {k: v.model_dump() for k, v in self.plot_threads.items()},
            "outline": self.outline.model_dump() if self.outline else None,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

        if format == "json":
            return json.dumps(data, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")

    @classmethod
    def create(cls, config: StoryConfig) -> "Story":
        """Create a new story.

        Args:
            config: Story configuration

        Returns:
            New story instance
        """
        return cls(config)

    def __repr__(self) -> str:
        return f"<Story title='{self.config.title}' chapters={len(self.chapters)}>"
