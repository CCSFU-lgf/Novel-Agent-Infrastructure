"""
Agent workflow example for Novel Agent Infrastructure.

This example demonstrates how to use the multi-agent system.
"""

import asyncio
from novel_agent.core.agent import Agent, AgentConfig, AgentType, AgentTask


async def main():
    """Main workflow example."""
    print("🚀 Agent Workflow Example")
    print("=" * 50)

    # 1. Create agents
    print("\n🤖 Creating Agents...")

    planner_config = AgentConfig(
        agent_type=AgentType.PLANNER,
        model="gpt-4",
        temperature=0.7,
    )
    planner = Agent.create(planner_config)
    print(f"Created: {planner.agent_id}")

    character_config = AgentConfig(
        agent_type=AgentType.CHARACTER,
        model="gpt-4",
        temperature=0.7,
    )
    character_agent = Agent.create(character_config)
    print(f"Created: {character_agent.agent_id}")

    writer_config = AgentConfig(
        agent_type=AgentType.WRITER,
        model="gpt-4",
        temperature=0.8,
    )
    writer = Agent.create(writer_config)
    print(f"Created: {writer.agent_id}")

    # 2. Execute tasks
    print("\n📋 Executing Tasks...")

    # Planner task
    planner_task = AgentTask(
        id="task_1",
        task_type="create_concept",
        description="Create a fantasy story concept",
        context={
            "genre": "fantasy",
            "themes": ["growth", "destiny"],
        },
    )
    planner_result = await planner.execute(planner_task)
    print(f"Planner result: {planner_result.status}")

    # Character task
    character_task = AgentTask(
        id="task_2",
        task_type="create_character",
        description="Create the protagonist",
        context={
            "name": "Elena",
            "role": "protagonist",
        },
    )
    character_result = await character_agent.execute(character_task)
    print(f"Character result: {character_result.status}")

    # Writer task
    writer_task = AgentTask(
        id="task_3",
        task_type="write_chapter",
        description="Write chapter 1",
        context={
            "chapter_number": 1,
            "outline": "Introduce the protagonist",
            "characters": ["Elena"],
        },
    )
    writer_result = await writer.execute(writer_task)
    print(f"Writer result: {writer_result.status}")

    # 3. Agent capabilities
    print("\n🎯 Agent Capabilities:")
    print(f"Planner: {planner.get_capabilities()}")
    print(f"Character: {character_agent.get_capabilities()}")
    print(f"Writer: {writer.get_capabilities()}")

    print("\n✅ Workflow example completed!")


if __name__ == "__main__":
    asyncio.run(main())
