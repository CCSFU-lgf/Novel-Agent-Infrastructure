# Architecture Guide

This document describes the architecture of Novel Agent Infrastructure.

## Overview

Novel Agent Infrastructure is designed as a modular, extensible system for AI-powered fiction creation. The architecture follows these principles:

1. **Separation of Concerns**: Each module has a clear responsibility
2. **Plugin Architecture**: Easy to extend with new platforms and features
3. **MCP-First Design**: Built for Model Context Protocol from the ground up
4. **Memory-Centric**: Long-term memory is a core feature, not an afterthought

## Core Components

### 1. Core Module (`src/novel_agent/core/`)

The core module provides the fundamental abstractions:

- **Platform**: Abstract interface for platform adapters
- **MemoryEngine**: Abstract interface for memory storage
- **Agent**: Abstract interface for agents
- **Story**: Story management and persistence
- **Config**: Configuration management

### 2. Platform Adapters (`src/novel_agent/platforms/`)

Platform adapters provide integration with fiction publishing platforms:

```
platforms/
├── base.py          # Base platform with common logic
├── tomato.py        # 番茄小说 adapter
├── qidian.py        # 起点中文网 adapter
├── qimao.py         # 七猫 adapter
├── royalroad.py     # Royal Road adapter
├── wattpad.py       # Wattpad adapter
├── ao3.py           # AO3 adapter
└── scribblehub.py   # ScribbleHub adapter
```

Each adapter implements:
- Title validation
- Genre and tag support
- Market analysis
- Chapter publishing

### 3. MCP Server (`src/novel_agent/mcp/`)

The MCP server provides tools for MCP-compatible clients:

```
mcp/
├── server.py        # MCP server implementation
└── tools/           # Individual tool implementations
    ├── validate_title.py
    ├── classify_story.py
    ├── generate_character.py
    ├── generate_world.py
    ├── generate_outline.py
    ├── generate_chapter_plan.py
    ├── market_analysis.py
    ├── trend_analysis.py
    ├── story_memory.py
    └── publishing_assistant.py
```

### 4. Agent System (`src/novel_agent/agents/`)

The agent system provides multi-agent collaboration:

```
agents/
├── planner.py       # Story planning agent
├── character.py     # Character development agent
├── worldbuilder.py  # World-building agent
├── outline.py       # Outlining agent
├── writer.py        # Writing agent
├── editor.py        # Editing agent
└── publisher.py     # Publishing agent
```

### 5. Memory Engine (`src/novel_agent/memory/`)

The memory engine provides long-term story memory:

```
memory/
├── vector.py        # Vector-based semantic search
└── graph.py         # Graph-based relationship tracking
```

## Data Flow

### Story Creation Flow

```
User Request
    ↓
MCP Tool
    ↓
Platform Adapter
    ↓
Memory Engine
    ↓
Agent System
    ↓
Output
```

### Memory Flow

```
Chapter Content
    ↓
Entity Extraction
    ↓
Vector Embedding
    ↓
Storage
    ↓
Retrieval
```

## Design Patterns

### 1. Strategy Pattern

Platform adapters use the Strategy pattern to provide different implementations for different platforms while maintaining a common interface.

### 2. Factory Pattern

The `Platform.create()` and `Agent.create()` methods use the Factory pattern to create instances based on configuration.

### 3. Observer Pattern

The agent system uses the Observer pattern for communication between agents.

### 4. Repository Pattern

The memory engine uses the Repository pattern to abstract storage details.

## Extension Points

### Adding a New Platform

1. Create a new file in `src/novel_agent/platforms/`
2. Implement the `Platform` interface
3. Register in `__init__.py`

### Adding a New MCP Tool

1. Create a new file in `src/novel_agent/mcp/tools/`
2. Implement the `BaseTool` interface
3. Register in `server.py`

### Adding a New Agent

1. Create a new file in `src/novel_agent/agents/`
2. Implement the `Agent` interface
3. Register in `__init__.py`

## Dependencies

- **Pydantic**: Data validation and serialization
- **MCP**: Model Context Protocol implementation
- **ChromaDB**: Vector storage for memory engine
- **httpx**: HTTP client for platform APIs
- **Typer**: CLI interface
- **Rich**: Terminal formatting

## Performance Considerations

- **Caching**: Platform adapters cache genres and tags
- **Lazy Loading**: Components are loaded on demand
- **Async Support**: Core operations support async/await
- **Vector Search**: Efficient semantic search for memory

## Security Considerations

- **API Keys**: Stored in environment variables
- **Input Validation**: All inputs are validated
- **Rate Limiting**: Platform adapters respect rate limits
- **Error Handling**: Comprehensive error handling throughout
