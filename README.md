# Blog Generator

A lightweight, agent-based blog generation scaffold.

## Project Structure

```
blog-gen/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── content_writer.py
│   ├── editor_agent.py
│   └── seo_optimizer_agent.py
├── core/
│   ├── __init__.py
│   ├── memory_manager.py
│   ├── message.py
│   └── orchestrator.py
├── frontend/
│   └── app.py
├── tests/
│   ├── __init__.py
│   ├── __initi__.oy
│   └── test_orchestrator.py
├── utils/
│   ├── __init__.py
│   └── logger.py
├── .env.template
├── config.py
├── main.py
└── requirements.txt
```

## Setup

1. Create a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy env template:

```bash
cp .env.template .env
```

4. Run CLI:

```bash
python main.py --topic "How to Start a Blog"
```

5. Run tests:

```bash
pytest -q
```

## Notes

- This is an MVP scaffold with placeholder agent logic.
- Replace agent internals with your preferred LLM/provider integration.
