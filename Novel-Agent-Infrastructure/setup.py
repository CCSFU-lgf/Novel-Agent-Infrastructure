"""Setup script for novel-agent-infrastructure."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="novel-agent-infrastructure",
    version="0.1.0",
    author="Novel Agent Team",
    author_email="team@novel-agent.dev",
    description="Open-source infrastructure for AI fiction creation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/novel-agent/novel-agent-infrastructure",
    project_urls={
        "Bug Tracker": "https://github.com/novel-agent/novel-agent-infrastructure/issues",
        "Documentation": "https://novel-agent.github.io/novel-agent-infrastructure",
        "Source Code": "https://github.com/novel-agent/novel-agent-infrastructure",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: General",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=[
        "pydantic>=2.0.0",
        "httpx>=0.25.0",
        "mcp>=1.0.0",
        "rich>=13.0.0",
        "typer>=0.9.0",
        "chromadb>=0.4.0",
        "sentence-transformers>=2.2.0",
        "openai>=1.0.0",
        "anthropic>=0.18.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-asyncio>=0.21.0",
            "mypy>=1.5.0",
            "ruff>=0.1.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "pre-commit>=3.3.0",
        ],
        "docs": [
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.0.0",
            "mkdocstrings[python]>=0.23.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "novel-agent=novel_agent.cli:app",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
