# Novel Agent Infrastructure

<div align="center">

**Open-source infrastructure for AI fiction creation**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-compatible-brightgreen.svg)](https://modelcontextprotocol.io/)

[English](README.md) | [中文](README_CN.md)

</div>

## 🚀 Overview

Novel Agent Infrastructure is a production-grade, open-source framework for building AI-powered fiction creation systems. It provides:

- **Multi-Platform Support**: Integrate with 7+ fiction platforms (Chinese & International)
- **Story Memory Engine**: Long-term memory for consistent storytelling across 1000+ chapters
- **Agent-Native Workflows**: Multi-agent system for collaborative fiction creation
- **MCP Integration**: First-class support for Model Context Protocol
- **Extensible Architecture**: Plugin-based design for easy customization

## ✨ Key Features

### 🌍 Multi-Platform Support

| Platform | Language | Type |
|----------|----------|------|
| 🍅 Tomato Novel (番茄小说) | Chinese | Free |
| 📚 Qidian (起点中文网) | Chinese | Premium |
| 🐱 Qimao (七猫) | Chinese | Free |
| ⚔️ Royal Road | English | Web Novel |
| 📖 Wattpad | Multi-language | Social |
| 📚 AO3 | English | Fanfiction |
| ✍️ ScribbleHub | English | Light Novel |

### 🧠 Story Memory Engine

- **Character Tracking**: Maintain consistent character traits, relationships, and development
- **World-Building**: Track locations, organizations, and world rules
- **Plot Management**: Monitor plot threads, foreshadowing, and callbacks
- **Vector Search**: Semantic search for relevant story elements
- **Chapter Tracking**: Know exactly what happened in each chapter

### 🤖 Multi-Agent System

| Agent | Responsibility |
|-------|---------------|
| 🎯 Planner | High-level story planning and structure |
| 👤 Character | Character development and consistency |
| 🌍 WorldBuilder | World-building and setting management |
| 📋 Outline | Chapter and scene outlining |
| ✍️ Writer | Prose generation and storytelling |
| ✏️ Editor | Quality control and consistency checking |
| 📤 Publishing | Platform-specific publishing |

### 🔌 MCP Integration

First-class support for Model Context Protocol, enabling integration with:
- Claude Code
- GitHub Copilot
- Cursor
- Any MCP-compatible client

## 📦 Installation

```bash
# Install from PyPI
pip install novel-agent-infrastructure

# Install with development dependencies
pip install novel-agent-infrastructure[dev]

# Install with documentation dependencies
pip install novel-agent-infrastructure[docs]
```

## 🚀 Quick Start

### Basic Usage

```python
from novel_agent import NovelAgent, Platform, PlatformType

# Create a platform adapter
platform = Platform.create(PlatformType.ROYALROAD)

# Validate a title
result = platform.validate_title("The Last Guardian")
print(f"Valid: {result.is_valid}")

# Get available genres
genres = platform.get_genres()
for genre in genres:
    print(f"- {genre.name}")
```

### MCP Server

```bash
# Start the MCP server
novel-agent serve

# Or with custom configuration
novel-agent serve --host 0.0.0.0 --port 8000
```

### Agent System

```python
from novel_agent.core.agent import Agent, AgentConfig, AgentType

# Create a writer agent
config = AgentConfig(
    agent_type=AgentType.WRITER,
    model="gpt-4",
    temperature=0.7,
)
agent = Agent.create(config)

# Execute a task
result = await agent.execute(task)
print(result.output)
```

## 📚 Documentation

- [Architecture Guide](docs/architecture/README.md)
- [API Reference](docs/api/README.md)
- [MCP Integration](docs/mcp/README.md)
- [Platform Guides](docs/guides/platforms.md)
- [Agent System](docs/guides/agents.md)

## 🏗️ Project Structure

```
novel-agent-infrastructure/
├── src/
│   └── novel_agent/
│       ├── core/              # Core abstractions
│       ├── mcp/               # MCP server & tools
│       ├── platforms/         # Platform adapters
│       ├── agents/            # Agent system
│       ├── memory/            # Memory engines
│       ├── cli/               # CLI interface
│       └── utils/             # Utility functions
├── tests/                     # Test suite
├── docs/                      # Documentation
├── examples/                  # Example code
├── benchmarks/                # Performance benchmarks
└── datasets/                  # Training datasets
```

## 🔧 Development

```bash
# Clone the repository
git clone https://github.com/novel-agent/novel-agent-infrastructure.git
cd novel-agent-infrastructure

# Install in development mode
make install-dev

# Run tests
make test

# Run linter
make lint

# Format code
make format

# Type check
make type-check
```

## 📊 MCP Tools

| Tool | Description |
|------|-------------|
| `validate_title` | Validate story titles for different platforms |
| `classify_story` | Classify stories by genre and tags |
| `generate_character` | Generate character profiles |
| `generate_world` | Generate world-building elements |
| `generate_outline` | Generate story outlines |
| `generate_chapter_plan` | Generate chapter plans |
| `market_analysis` | Analyze market trends |
| `trend_analysis` | Analyze fiction trends |
| `story_memory` | Manage story memory |
| `publishing_assistant` | Assist with publishing |

## 🎯 Use Cases

### For Authors
- Get AI assistance for story planning and writing
- Maintain consistency across long novels
- Optimize titles and tags for different platforms
- Track character development and plot threads

### For Developers
- Build AI-powered writing tools
- Integrate with fiction platforms
- Create custom agents for specific tasks
- Extend with new platforms and features

### For MCP Users
- Use novel creation tools in Claude Code
- Integrate with GitHub Copilot
- Build custom MCP workflows
- Create automated writing assistants

## 🌟 Why Novel Agent Infrastructure?

### Unique Advantages

1. **Chinese Web Novel Expertise**: Deep understanding of Chinese fiction platforms and conventions
2. **Platform-Specific Optimization**: Tailored support for each platform's requirements
3. **Long-Form Story Memory**: Memory engine designed for 1000+ chapter novels
4. **Agent-Native Workflows**: Built for multi-agent collaboration from the ground up

### Production Ready

- Comprehensive test suite
- Type annotations throughout
- Extensive documentation
- CI/CD pipeline

## 🗺️ Roadmap

### v0.1 (Current)
- Core platform adapters
- Basic memory engine
- MCP server with 10 tools
- CLI interface

### v0.2
- Enhanced memory engine with vector search
- Improved agent system
- More platform features

### v0.3
- Web UI
- VS Code extension
- Advanced analytics

### v0.5
- Enterprise features
- Custom model support
- Advanced workflows

### v1.0
- Full production release
- Complete documentation
- Community ecosystem

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest features
- 📖 Improve documentation
- 🧪 Add tests
- 🔧 Fix issues
- 🌍 Add platform support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io/) for the MCP specification
- [ChromaDB](https://www.trychroma.com/) for vector storage
- [Pydantic](https://docs.pydantic.dev/) for data validation
- [Typer](https://typer.tiangolo.com/) for CLI interface

## 📞 Contact

- **GitHub**: CCSFU-lgf
- **Email**: lgf15568701008@gmail.com
- **Discord**: 

---

<div align="center">

**Built with ❤️ for the fiction writing community**

</div>
