# Novel Agent Infrastructure

<div align="center">

**AI小说创作的开源基础设施**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-compatible-brightgreen.svg)](https://modelcontextprotocol.io/)

[English](README.md) | [中文](README_CN.md)

</div>

## 🚀 概述

Novel Agent Infrastructure 是一个生产级的开源框架，用于构建AI驱动的小说创作系统。它提供：

- **多平台支持**：集成7+小说平台（中国 & 国际）
- **故事记忆引擎**：支持1000+章节的长期记忆
- **Agent原生工作流**：多Agent协作创作系统
- **MCP集成**：Model Context Protocol 一等支持
- **可扩展架构**：基于插件的设计，易于定制

## ✨ 核心特性

### 🌍 多平台支持

| 平台 | 语言 | 类型 |
|------|------|------|
| 🍅 番茄小说 | 中文 | 免费 |
| 📚 起点中文网 | 中文 | 付费 |
| 🐱 七猫 | 中文 | 免费 |
| ⚔️ Royal Road | 英文 | 网络小说 |
| 📖 Wattpad | 多语言 | 社交 |
| 📚 AO3 | 英文 | 同人小说 |
| ✍️ ScribbleHub | 英文 | 轻小说 |

### 🧠 故事记忆引擎

- **角色追踪**：维护一致的角色特征、关系和发展
- **世界观构建**：追踪地点、组织和世界规则
- **情节管理**：监控情节线、伏笔和回调
- **向量搜索**：语义搜索相关故事元素
- **章节追踪**：精确知道每章发生了什么

### 🤖 多Agent系统

| Agent | 职责 |
|-------|------|
| 🎯 规划师 | 高层故事规划和结构 |
| 👤 角色师 | 角色发展和一致性 |
| 🌍 世界观构建师 | 世界观和设定管理 |
| 📋 大纲师 | 章节和场景大纲 |
| ✍️ 写手 | 散文生成和故事讲述 |
| ✏️ 编辑师 | 质量控制和一致性检查 |
| 📤 发布师 | 平台特定发布 |

### 🔌 MCP集成

对Model Context Protocol的一等支持，可集成：
- Claude Code
- GitHub Copilot
- Cursor
- 任何MCP兼容客户端

## 📦 安装

```bash
# 从PyPI安装
pip install novel-agent-infrastructure

# 安装开发依赖
pip install novel-agent-infrastructure[dev]

# 安装文档依赖
pip install novel-agent-infrastructure[docs]
```

## 🚀 快速开始

### 基本用法

```python
from novel_agent import NovelAgent, Platform, PlatformType

# 创建平台适配器
platform = Platform.create(PlatformType.ROYALROAD)

# 验证标题
result = platform.validate_title("最后的守护者")
print(f"有效: {result.is_valid}")

# 获取可用类型
genres = platform.get_genres()
for genre in genres:
    print(f"- {genre.name}")
```

### MCP服务器

```bash
# 启动MCP服务器
novel-agent serve

# 或自定义配置
novel-agent serve --host 0.0.0.0 --port 8000
```

### Agent系统

```python
from novel_agent.core.agent import Agent, AgentConfig, AgentType

# 创建写手Agent
config = AgentConfig(
    agent_type=AgentType.WRITER,
    model="gpt-4",
    temperature=0.7,
)
agent = Agent.create(config)

# 执行任务
result = await agent.execute(task)
print(result.output)
```

## 📚 文档

- [架构指南](docs/architecture/README.md)
- [API参考](docs/api/README.md)
- [MCP集成](docs/mcp/README.md)
- [平台指南](docs/guides/platforms.md)
- [Agent系统](docs/guides/agents.md)

## 🏗️ 项目结构

```
novel-agent-infrastructure/
├── src/
│   └── novel_agent/
│       ├── core/              # 核心抽象
│       ├── mcp/               # MCP服务器和工具
│       ├── platforms/         # 平台适配器
│       ├── agents/            # Agent系统
│       ├── memory/            # 记忆引擎
│       ├── cli/               # CLI接口
│       └── utils/             # 工具函数
├── tests/                     # 测试套件
├── docs/                      # 文档
├── examples/                  # 示例代码
├── benchmarks/                # 性能基准
└── datasets/                  # 训练数据集
```

## 🔧 开发

```bash
# 克隆仓库
git clone https://github.com/novel-agent/novel-agent-infrastructure.git
cd novel-agent-infrastructure

# 以开发模式安装
make install-dev

# 运行测试
make test

# 运行代码检查
make lint

# 格式化代码
make format

# 类型检查
make type-check
```

## 📊 MCP工具

| 工具 | 描述 |
|------|------|
| `validate_title` | 验证不同平台的故事标题 |
| `classify_story` | 按类型和标签分类故事 |
| `generate_character` | 生成角色档案 |
| `generate_world` | 生成世界观元素 |
| `generate_outline` | 生成故事大纲 |
| `generate_chapter_plan` | 生成章节计划 |
| `market_analysis` | 分析市场趋势 |
| `trend_analysis` | 分析小说趋势 |
| `story_memory` | 管理故事记忆 |
| `publishing_assistant` | 协助发布 |

## 🎯 使用场景

### 对于作者
- 获得AI辅助的故事规划和写作
- 在长篇小说中保持一致性
- 为不同平台优化标题和标签
- 追踪角色发展和情节线

### 对于开发者
- 构建AI驱动的写作工具
- 集成小说平台
- 为特定任务创建自定义Agent
- 用新平台和功能扩展

### 对于MCP用户
- 在Claude Code中使用小说创作工具
- 集成GitHub Copilot
- 构建自定义MCP工作流
- 创建自动化写作助手

## 🌟 为什么选择Novel Agent Infrastructure？

### 独特优势

1. **中文网络小说专业知识**：深入理解中文小说平台和惯例
2. **平台特定优化**：为每个平台的需求量身定制
3. **长篇故事记忆**：专为1000+章节小说设计的记忆引擎
4. **Agent原生工作流**：从底层为多Agent协作而构建

### 生产就绪

- 全面的测试套件
- 全面的类型注解
- 详尽的文档
- CI/CD流水线

## 🗺️ 路线图

### v0.1（当前）
- 核心平台适配器
- 基础记忆引擎
- 10个工具的MCP服务器
- CLI接口

### v0.2
- 增强的向量搜索记忆引擎
- 改进的Agent系统
- 更多平台功能

### v0.3
- Web UI
- VS Code扩展
- 高级分析

### v0.5
- 企业功能
- 自定义模型支持
- 高级工作流

### v1.0
- 完整生产发布
- 完整文档
- 社区生态系统

## 🤝 贡献

我们欢迎贡献！请参阅我们的[贡献指南](CONTRIBUTING.md)了解详情。

### 贡献方式

- 🐛 报告bug
- 💡 建议功能
- 📖 改进文档
- 🧪 添加测试
- 🔧 修复问题
- 🌍 添加平台支持

## 📄 许可证

本项目采用MIT许可证 - 详见[LICENSE](LICENSE)文件。

## 🙏 致谢

- [Model Context Protocol](https://modelcontextprotocol.io/) 提供MCP规范
- [ChromaDB](https://www.trychroma.com/) 提供向量存储
- [Pydantic](https://docs.pydantic.dev/) 提供数据验证
- [Typer](https://typer.tiangolo.com/) 提供CLI接口

## 📞 联系方式

- **GitHub**: [novel-agent/novel-agent-infrastructure](https://github.com/novel-agent/novel-agent-infrastructure)
- **Email**: team@novel-agent.dev
- **Discord**: [加入我们的社区](https://discord.gg/novel-agent)

---

<div align="center">

**为小说写作社区用❤️打造**

</div>
