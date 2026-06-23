"""
Configuration management for Novel Agent Infrastructure.

This module provides configuration management for the entire system.

Example:
    >>> from novel_agent.core.config import Config
    >>> config = Config.from_file("config.yaml")
    >>> config.llm.model
    'gpt-4'
"""

import os
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from pathlib import Path
import yaml
import json


class LLMConfig(BaseModel):
    """LLM configuration."""

    provider: str = "openai"  # openai, anthropic, local
    model: str = "gpt-4"
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 4096
    timeout: int = 60


class MemoryConfig(BaseModel):
    """Memory engine configuration."""

    engine_type: str = "vector"  # vector, graph, hybrid
    vector_db: str = "chroma"  # chroma, qdrant, pinecone
    embedding_model: str = "all-MiniLM-L6-v2"
    collection_name: str = "novel_memory"
    persist_directory: str = "./data/memory"
    similarity_threshold: float = 0.7


class PlatformConfig(BaseModel):
    """Platform configuration."""

    default_platform: str = "royalroad"
    api_keys: Dict[str, str] = Field(default_factory=dict)
    rate_limits: Dict[str, int] = Field(default_factory=dict)
    proxy: Optional[str] = None


class AgentConfig(BaseModel):
    """Agent system configuration."""

    default_model: str = "gpt-4"
    max_iterations: int = 10
    timeout: int = 300
    enable_collaboration: bool = True
    enable_memory: bool = True


class ServerConfig(BaseModel):
    """MCP server configuration."""

    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    cors_origins: List[str] = Field(default_factory=lambda: ["*"])


class Config(BaseModel):
    """Main configuration."""

    llm: LLMConfig = Field(default_factory=LLMConfig)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    platform: PlatformConfig = Field(default_factory=PlatformConfig)
    agent: AgentConfig = Field(default_factory=AgentConfig)
    server: ServerConfig = Field(default_factory=ServerConfig)

    # Project settings
    project_name: str = "Novel Agent Infrastructure"
    version: str = "0.1.0"
    debug: bool = False
    log_level: str = "INFO"

    # Paths
    data_dir: str = "./data"
    output_dir: str = "./output"
    temp_dir: str = "./temp"

    @classmethod
    def from_file(cls, path: str) -> "Config":
        """Load config from file.

        Args:
            path: Path to config file (yaml or json)

        Returns:
            Config instance
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            if path.suffix in (".yaml", ".yml"):
                data = yaml.safe_load(f)
            elif path.suffix == ".json":
                data = json.load(f)
            else:
                raise ValueError(f"Unsupported config format: {path.suffix}")

        return cls(**data)

    @classmethod
    def from_env(cls) -> "Config":
        """Load config from environment variables.

        Returns:
            Config instance
        """
        config = cls()

        # LLM
        if os.getenv("OPENAI_API_KEY"):
            config.llm.api_key = os.getenv("OPENAI_API_KEY")
        if os.getenv("ANTHROPIC_API_KEY"):
            config.llm.provider = "anthropic"
            config.llm.api_key = os.getenv("ANTHROPIC_API_KEY")
        if os.getenv("LLM_MODEL"):
            config.llm.model = os.getenv("LLM_MODEL")

        # Memory
        if os.getenv("VECTOR_DB"):
            config.memory.vector_db = os.getenv("VECTOR_DB")
        if os.getenv("MEMORY_DIR"):
            config.memory.persist_directory = os.getenv("MEMORY_DIR")

        # Server
        if os.getenv("SERVER_HOST"):
            config.server.host = os.getenv("SERVER_HOST")
        if os.getenv("SERVER_PORT"):
            config.server.port = int(os.getenv("SERVER_PORT"))

        # Debug
        if os.getenv("DEBUG"):
            config.debug = os.getenv("DEBUG").lower() in ("true", "1", "yes")

        return config

    def to_file(self, path: str) -> None:
        """Save config to file.

        Args:
            path: Path to save config
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            if path.suffix in (".yaml", ".yml"):
                yaml.dump(self.model_dump(), f, default_flow_style=False)
            elif path.suffix == "json":
                json.dump(self.model_dump(), f, indent=2)
            else:
                raise ValueError(f"Unsupported config format: {path.suffix}")

    def get_llm_client(self) -> Any:
        """Get LLM client based on configuration.

        Returns:
            LLM client instance
        """
        if self.llm.provider == "openai":
            from openai import OpenAI
            return OpenAI(api_key=self.llm.api_key, base_url=self.llm.api_base)
        elif self.llm.provider == "anthropic":
            from anthropic import Anthropic
            return Anthropic(api_key=self.llm.api_key)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.llm.provider}")

    def create_directories(self) -> None:
        """Create necessary directories."""
        for dir_path in [self.data_dir, self.output_dir, self.temp_dir]:
            Path(dir_path).mkdir(parents=True, exist_ok=True)

    def validate(self) -> List[str]:
        """Validate configuration.

        Returns:
            List of validation errors
        """
        errors = []

        if not self.llm.api_key and self.llm.provider in ("openai", "anthropic"):
            errors.append(f"API key required for {self.llm.provider}")

        if self.memory.engine_type == "vector" and self.memory.vector_db not in ("chroma", "qdrant", "pinecone"):
            errors.append(f"Unsupported vector DB: {self.memory.vector_db}")

        if self.server.port < 1 or self.server.port > 65535:
            errors.append(f"Invalid port: {self.server.port}")

        return errors
