# Agent System Guide

This guide describes how to use the multi-agent system in Novel Agent Infrastructure.

## Overview

The agent system provides 7 specialized agents for fiction creation:

| Agent | Type | Responsibility |
|-------|------|---------------|
| 🎯 Planner | PLANNER | High-level story planning |
| 👤 Character | CHARACTER | Character development |
| 🌍 WorldBuilder | WORLDBUILDER | World-building |
| 📋 Outline | OUTLINE | Chapter outlining |
| ✍️ Writer | WRITER | Prose generation |
| ✏️ Editor | EDITOR | Quality control |
| 📤 Publisher | PUBLISHER | Platform publishing |

## Basic Usage

### Creating an Agent

```python
from novel_agent.core.agent import Agent, AgentConfig, AgentType

# Create configuration
config = AgentConfig(
    agent_type=AgentType.WRITER,
    model="gpt-4",
    temperature=0.7,
    max_tokens=4096,
)

# Create agent
agent = Agent.create(config)
```

### Executing Tasks

```python
from novel_agent.core.agent import AgentTask

# Create a task
task = AgentTask(
    id="task_1",
    task_type="write_chapter",
    description="Write chapter 1",
    context={
        "chapter_number": 1,
        "outline": "Introduce the protagonist",
        "characters": ["Elena"],
    },
)

# Execute task
result = await agent.execute(task)
print(f"Status: {result.status}")
print(f"Output: {result.output}")
```

### Agent Capabilities

```python
capabilities = agent.get_capabilities()
print(f"Agent capabilities: {capabilities}")
```

## Agent Types

### Planner Agent

Handles high-level story planning.

**Task Types:**
- `create_concept`: Create story concept
- `develop_outline`: Develop story outline
- `plan_character_arcs`: Plan character arcs
- `structure_acts`: Structure story acts

**Example:**
```python
task = AgentTask(
    id="plan_1",
    task_type="create_concept",
    description="Create fantasy story concept",
    context={"genre": "fantasy", "themes": ["growth", "destiny"]},
)
result = await planner.execute(task)
```

### Character Agent

Handles character development.

**Task Types:**
- `create_character`: Create character profile
- `develop_background`: Develop character background
- `check_consistency`: Check character consistency

**Example:**
```python
task = AgentTask(
    id="char_1",
    task_type="create_character",
    description="Create protagonist",
    context={"name": "Elena", "role": "protagonist"},
)
result = await character_agent.execute(task)
```

### WorldBuilder Agent

Handles world-building.

**Task Types:**
- `create_world`: Create world setting
- `design_magic_system`: Design magic system
- `build_cultures`: Build cultures and societies

**Example:**
```python
task = AgentTask(
    id="world_1",
    task_type="create_world",
    description="Create fantasy world",
    context={"genre": "fantasy", "setting": "medieval"},
)
result = await worldbuilder.execute(task)
```

### Outline Agent

Handles chapter outlining.

**Task Types:**
- `create_chapter_outline`: Create chapter outline
- `plan_scenes`: Plan scene sequences
- `track_plot_threads`: Track plot threads

**Example:**
```python
task = AgentTask(
    id="outline_1",
    task_type="create_chapter_outline",
    description="Create chapter 1 outline",
    context={"chapter_number": 1, "previous_summary": ""},
)
result = await outline_agent.execute(task)
```

### Writer Agent

Handles prose generation.

**Task Types:**
- `write_chapter`: Write a chapter
- `write_dialogue`: Write dialogue
- `write_description`: Write descriptions

**Example:**
```python
task = AgentTask(
    id="write_1",
    task_type="write_chapter",
    description="Write chapter 1",
    context={
        "chapter_number": 1,
        "outline": "Introduce Elena",
        "characters": ["Elena"],
    },
)
result = await writer.execute(task)
```

### Editor Agent

Handles quality control.

**Task Types:**
- `check_quality`: Check writing quality
- `verify_consistency`: Verify consistency
- `suggest_improvements`: Suggest improvements

**Example:**
```python
task = AgentTask(
    id="edit_1",
    task_type="check_quality",
    description="Check chapter 1 quality",
    context={"content": "Chapter content here..."},
)
result = await editor.execute(task)
```

### Publisher Agent

Handles platform publishing.

**Task Types:**
- `prepare_publish`: Prepare for publishing
- `optimize_title`: Optimize title for platform
- `schedule_publish`: Schedule publication

**Example:**
```python
task = AgentTask(
    id="pub_1",
    task_type="prepare_publish",
    description="Prepare chapter 1 for Royal Road",
    context={
        "platform": "royalroad",
        "chapter_number": 1,
        "content": "Chapter content...",
    },
)
result = await publisher.execute(task)
```

## Multi-Agent Workflows

### Sequential Workflow

```python
# 1. Planner creates concept
plan_result = await planner.execute(plan_task)

# 2. Character agent creates characters
char_result = await character_agent.execute(char_task)

# 3. WorldBuilder creates world
world_result = await worldbuilder.execute(world_task)

# 4. Outline agent creates outline
outline_result = await outline_agent.execute(outline_task)

# 5. Writer writes chapter
write_result = await writer.execute(write_task)

# 6. Editor reviews
edit_result = await editor.execute(edit_task)

# 7. Publisher publishes
pub_result = await publisher.execute(pub_task)
```

### Parallel Workflow

```python
import asyncio

# Run independent tasks in parallel
results = await asyncio.gather(
    character_agent.execute(char_task),
    worldbuilder.execute(world_task),
)

# Use results for dependent tasks
outline_result = await outline_agent.execute(outline_task)
```

## Error Handling

```python
from novel_agent.core.agent import AgentStatus

result = await agent.execute(task)

if result.status == AgentStatus.COMPLETED:
    print(f"Success: {result.output}")
elif result.status == AgentStatus.ERROR:
    print(f"Error: {result.reasoning}")
else:
    print(f"Status: {result.status}")
```

## Best Practices

1. **Choose the right agent** for each task
2. **Provide clear context** in task descriptions
3. **Use appropriate models** for different tasks
4. **Handle errors gracefully**
5. **Use parallel execution** when possible
6. **Monitor agent status** for long-running tasks
