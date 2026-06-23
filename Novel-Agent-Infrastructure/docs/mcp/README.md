# MCP Integration Guide

This document describes how to integrate Novel Agent Infrastructure with MCP-compatible clients.

## Overview

Model Context Protocol (MCP) is a protocol for integrating AI models with external tools. Novel Agent Infrastructure provides a full MCP server implementation with 10 tools for fiction creation.

## Supported Clients

- **Claude Code**: Full support
- **GitHub Copilot**: Full support
- **Cursor**: Full support
- **Any MCP Client**: Compatible with any MCP implementation

## MCP Tools

### 1. validate_title

Validates story titles for different platforms.

**Input Schema:**
```json
{
  "title": "string",
  "platform": "string",
  "language": "string"
}
```

**Example:**
```json
{
  "title": "The Last Guardian",
  "platform": "royalroad",
  "language": "en"
}
```

### 2. classify_story

Classifies stories by genre and tags.

**Input Schema:**
```json
{
  "title": "string",
  "description": "string",
  "platform": "string"
}
```

### 3. generate_character

Generates character profiles.

**Input Schema:**
```json
{
  "name": "string",
  "role": "string",
  "genre": "string",
  "traits": ["string"]
}
```

### 4. generate_world

Generates world-building elements.

**Input Schema:**
```json
{
  "genre": "string",
  "setting": "string",
  "magic_system": "boolean",
  "technology_level": "string"
}
```

### 5. generate_outline

Generates story outlines.

**Input Schema:**
```json
{
  "title": "string",
  "genre": "string",
  "target_chapters": "number",
  "target_word_count": "number"
}
```

### 6. generate_chapter_plan

Generates chapter plans.

**Input Schema:**
```json
{
  "chapter_number": "number",
  "previous_summary": "string",
  "plot_threads": ["string"],
  "characters": ["string"]
}
```

### 7. market_analysis

Analyzes market trends.

**Input Schema:**
```json
{
  "genre": "string",
  "tags": ["string"],
  "platform": "string"
}
```

### 8. trend_analysis

Analyzes fiction trends.

**Input Schema:**
```json
{
  "platform": "string",
  "timeframe": "string"
}
```

### 9. story_memory

Manages story memory.

**Input Schema:**
```json
{
  "action": "string",
  "entity_type": "string",
  "entity_id": "string",
  "data": "object"
}
```

### 10. publishing_assistant

Assists with publishing.

**Input Schema:**
```json
{
  "story_id": "string",
  "platform": "string",
  "chapter_number": "number",
  "content": "string",
  "title": "string"
}
```

## Setup

### Claude Code

Add to your Claude Code configuration:

```json
{
  "mcpServers": {
    "novel-agent": {
      "command": "novel-agent",
      "args": ["serve"]
    }
  }
}
```

### GitHub Copilot

Add to your Copilot configuration:

```yaml
mcp:
  servers:
    novel-agent:
      command: novel-agent
      args:
        - serve
```

### Cursor

Add to your Cursor settings:

```json
{
  "mcp.servers": {
    "novel-agent": {
      "command": "novel-agent",
      "args": ["serve"]
    }
  }
}
```

## Usage Examples

### In Claude Code

```
> Use the validate_title tool to check if "The Dragon's Quest" is a good title for Royal Road
```

### In GitHub Copilot

```python
# Ask Copilot to generate a character profile using MCP
# Copilot will use the generate_character tool
```

### In Cursor

```
@novel-agent generate_character name="Elena" role="protagonist" genre="fantasy"
```

## Custom Integration

### Python Client

```python
from mcp import Client

async with Client("novel-agent") as client:
    result = await client.call_tool(
        "validate_title",
        {"title": "My Story", "platform": "royalroad"}
    )
    print(result)
```

### JavaScript Client

```javascript
import { Client } from '@modelcontextprotocol/sdk';

const client = new Client('novel-agent');
await client.connect();

const result = await client.callTool('validate_title', {
  title: 'My Story',
  platform: 'royalroad',
});
console.log(result);
```

## Troubleshooting

### Server won't start

- Check that `novel-agent` is installed
- Verify Python version (3.10+ required)
- Check for port conflicts

### Tools not available

- Verify MCP server is running
- Check client configuration
- Review server logs for errors

### Performance issues

- Enable caching in configuration
- Reduce concurrent requests
- Check network connectivity
