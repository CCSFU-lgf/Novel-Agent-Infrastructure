# Platform Guide

This guide describes how to use the platform adapters in Novel Agent Infrastructure.

## Overview

Novel Agent Infrastructure supports 7 fiction publishing platforms:

| Platform | Language | Type | Best For |
|----------|----------|------|----------|
| Tomato Novel (番茄小说) | Chinese | Free | Chinese web novels |
| Qidian (起点中文网) | Chinese | Premium | Professional Chinese fiction |
| Qimao (七猫) | Chinese | Free | Mobile-first Chinese fiction |
| Royal Road | English | Web Novel | LitRPG, Progression Fantasy |
| Wattpad | Multi-language | Social | Young Adult, Romance |
| AO3 | English | Fanfiction | Fanfiction, Community |
| ScribbleHub | English | Light Novel | Light Novels, Asian Fiction |

## Basic Usage

### Creating a Platform Adapter

```python
from novel_agent import Platform, PlatformType

# Create a platform adapter
platform = Platform.create(PlatformType.ROYALROAD)
```

### Validating Titles

```python
result = platform.validate_title("The Last Guardian")
if result.is_valid:
    print(f"Title is valid: {result.title}")
else:
    print(f"Title invalid: {result.message}")
    for suggestion in result.suggestions:
        print(f"  - {suggestion}")
```

### Getting Genres

```python
genres = platform.get_genres()
for genre in genres:
    print(f"- {genre.name} ({genre.name_en})")
```

### Getting Tags

```python
tags = platform.get_tags()
for tag in tags:
    print(f"- {tag.name} ({tag.category})")
```

### Market Analysis

```python
analysis = platform.analyze_market(
    genre="fantasy",
    tags=["magic", "system"]
)

print(f"Competition: {analysis['competition_level']}")
print(f"Demand: {analysis['reader_demand']}")
print(f"Recommended tags: {analysis['recommended_tags']}")
```

## Platform-Specific Features

### Chinese Platforms (Tomato, Qidian, Qimao)

- Chinese character support
- Chinese genre categories
- Mobile optimization
- Free/Premium models

### International Platforms (Royal Road, Wattpad, AO3, ScribbleHub)

- English language support
- Western genre categories
- Community features
- Various monetization models

## Advanced Usage

### Custom Configuration

```python
config = {
    "api_key": "your-api-key",
    "base_url": "https://api.example.com",
    "timeout": 30,
}

platform = Platform.create(PlatformType.ROYALROAD, config)
```

### Multiple Platforms

```python
platforms = [
    Platform.create(PlatformType.ROYALROAD),
    Platform.create(PlatformType.WATTPAD),
    Platform.create(PlatformType.SCRIBBLEHUB),
]

for platform in platforms:
    analysis = platform.analyze_market("fantasy", ["magic"])
    print(f"{platform}: {analysis['competition_level']}")
```

## Error Handling

```python
from novel_agent.core.platform import Platform, PlatformType

try:
    platform = Platform.create(PlatformType.ROYALROAD)
    result = platform.validate_title("My Title")
except ValueError as e:
    print(f"Platform error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Best Practices

1. **Choose the right platform** for your target audience
2. **Validate titles** before publishing
3. **Use market analysis** to optimize your story
4. **Check platform guidelines** for specific requirements
5. **Test with multiple platforms** for cross-platform publishing
