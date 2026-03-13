# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an agent-based blog generation scaffold. It uses a multi-agent pipeline to generate blog content: ContentWriterAgent creates a draft, EditorAgent refines it, and SeoOptimizerAgent adds SEO keywords.

- User procudes blog topic
- 3 agents sequentialy improve the blog post
- Content wrtier -> editor -> seo optimizer
- each agent receives prevoius agent's ouitput
- final output: polished blog post

## Commands

```bash
# Run CLI with a topic
python main.py --topic "Your Topic"

# Run the Streamlit web UI
streamlit run frontend/app.py

# Run tests
pytest -q
```

## Architecture

The project follows an agent pipeline architecture:

- **Orchestrator** (`core/orchestrator.py`): Coordinates the pipeline by invoking agents sequentially and managing MemoryManager
- **Agents** (`agents/`): All inherit from `BaseAgent` (abstract class with `run(text) -> str` method)
  - `ContentWriterAgent`: Generates initial draft content
  - `EditorAgent`: Polishes/revises the draft
  - `SeoOptimizerAgent`: Adds SEO keywords section
- **MemoryManager** (`core/memory_manager.py`): Stores Message objects for conversation history
- **Message** (`core/message.py`): Dataclass with role, content, and timestamp
- **Settings** (`config.py`): Frozen dataclass loaded from environment variables

## Configuration

Environment variables in `.env`:
- `APP_NAME`, `APP_ENV`, `LOG_LEVEL`, `DEFAULT_TOPIC`

Copy `.env.template` to `.env` and configure as needed.

## requirements
1. type hints throughout
2. comprehensive docstrings
3. proper async/await
4. logging at key points
5. error handling
6. both cli and streamlit ui
7. working test suite
8. production ready code
9. clear separation of concerns
10. use langchain
11. use openrouter api key in .env
12. use a free model from openrouter