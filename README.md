# Strands Agents Template

**A production-ready template for building AI agents with [Strands Agents](https://strandsagents.com/latest/).**

Created by [Du'An Lightfoot](https://duanlightfoot.com) | [@labeveryday](https://github.com/labeveryday)

---

## Features

- ✅ **Multi-Model Support** - Anthropic, OpenAI, Writer, and Ollama (local) with easy switching
- ✅ **Pre-Built Tool Patterns** - 9 example tools covering sync/async, error handling, APIs, and more
- ✅ **Session Management** - Built-in conversation history and persistence
- ✅ **Auto-Tool Loading** - Tools automatically discovered from `src/tools/` directory
- ✅ **Custom Hooks** - Extensible logging and monitoring system
- ✅ **Model Recommendations** - Built-in tool to help select the right model for your use case

## Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/labeveryday/strands-agents-template.git
cd strands-agents-template
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
cp .env.example .env
```

Edit `.env` and add your API key (you only need ONE):

```bash
# Choose one provider
ANTHROPIC_API_KEY=your_key_here
# OR
OPENAI_API_KEY=your_key_here
# OR
WRITER_API_KEY=your_key_here
```

### 3. Run the Demo Agent

```bash
python src/agent.py
```

Try these commands:
- `What's the weather in Seattle?`
- `Search GitHub for strands agents`
- `What model should I use for fast customer support?`
- Type `tools` to see all available tools
- Type `exit` to quit

## Project Structure

```
.
├── src/
│   ├── agent.py              # Main agent implementation
│   ├── models/
│   │   └── models.py         # Model configurations (Anthropic, OpenAI, Writer, Ollama)
│   └── tools/                # Agent tools (auto-loaded)
│       ├── __init__.py       # Tool exports
│       ├── get_weather_tool.py
│       ├── search_github_tool.py
│       ├── recommend_model_tool.py
│       └── ...               # 8+ example tools
├── sessions/                 # Conversation history (auto-created)
├── .env                      # API keys (you create this)
└── requirements.txt          # Dependencies
```

## Switching Models

Edit `src/agent.py` line 34:

```python
# Current (Anthropic Claude Haiku)
from models import anthropic_model
MODEL = anthropic_model()

# Switch to OpenAI
from models import openai_model
MODEL = openai_model(model_id="gpt-5-mini-2025-08-07")

# Switch to local Ollama
from models import ollama_model
MODEL = ollama_model(model_id="qwen3:4b")
```

See `src/models/models.py` for all available models and configurations.

## Adding Your Own Tools

### Step 1: Create Tool File

Create `src/tools/my_tool.py`:

```python
from strands import tool

@tool
def my_tool(param: str) -> str:
    """Description of what your tool does.

    Args:
        param: Parameter description

    Returns:
        Result description
    """
    return f"Result: {param}"
```

### Step 2: Export Tool

Add to `src/tools/__init__.py`:

```python
from .my_tool import my_tool

__all__ = [
    # ... existing tools
    "my_tool",
]
```

### Step 3: Done!

The tool auto-loads when you run `python src/agent.py`. No changes needed to `agent.py`.

## Tool Patterns Included

| Tool | Pattern | Use Case |
|------|---------|----------|
| `get_weather` | Simple sync | Basic function calls |
| `send_notification` | Parameterized | Multiple parameters with defaults |
| `divide_numbers` | Error handling | Safe execution with try/catch |
| `fetch_api_data` | Async | Concurrent execution for I/O |
| `get_user_preferences` | Stateful | Maintaining state across calls |
| `search_github` | External API | HTTP requests with error handling |
| `count_lines_in_file` | File operations | Reading/processing files |
| `validate_email` | Validation | Input validation with regex |
| `get_available_models` | Data provider | Returning structured information |

## Configuration Options

### Agent Configuration (`src/agent.py`)

```python
agent = Agent(
    model=MODEL,                          # Your chosen model
    tools=[shell, current_time, editor],  # Built-in Strands tools
    session_manager=session_manager,      # Persist conversations
    conversation_manager=conversation_manager,  # Manage context window
    hooks=[LoggingHook()],                # Custom logging/monitoring
    name="Demo Agent",                    # Agent identifier
    load_tools_from_directory=True        # Auto-load from src/tools/
)
```

### Conversation Manager

```python
# Controls context window size
SlidingWindowConversationManager(
    window_size=20,              # Keep last 20 messages
    should_truncate_results=True # Truncate long tool outputs
)
```

### Session Manager

```python
# Persists conversation history to disk
FileSessionManager(
    session_id=SESSION_ID,       # Daily rotation (YYYYMMDD)
    storage_dir="./sessions"     # Storage location
)
```

## Model Selection Guide

Ask your agent for recommendations:

```
> What model should I use for complex reasoning tasks?
> Which model is most cost-effective for high volume?
> Recommend a model for analyzing long documents
```

Or check `src/models/models.py` for detailed model specifications including:
- Context windows
- Token limits
- Pricing
- Reasoning capabilities
- Best use cases

## Advanced: Custom Hooks

Add custom behavior by creating [hooks](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/agents/hooks/):

```python
from strands.hooks import HookProvider, HookRegistry
from strands.experimental.hooks import BeforeToolInvocationEvent

class MyHook(HookProvider):
    def register_hooks(self, registry: HookRegistry) -> None:
        registry.add_callback(BeforeToolInvocationEvent, self.on_tool_call)

    def on_tool_call(self, event: BeforeToolInvocationEvent) -> None:
        print(f"Calling tool: {event.tool_use['name']}")

# Add to agent
agent = Agent(..., hooks=[MyHook()])
```

## Tips

- **Sessions accumulate** - Clean up old files in `./sessions/` periodically
- **Context limits** - Adjust `window_size` in conversation manager for longer/shorter context
- **Extended thinking** - Anthropic models support extended thinking mode (see `models.py`)
- **Local models** - Ollama models run locally with zero API costs (requires Ollama installed)
- **Tool discovery** - Tools MUST be exported in `__init__.py` to be auto-loaded

## Requirements

- Python 3.10+
- Virtual environment (recommended)
- API key for at least one provider (Anthropic, OpenAI, Writer) OR Ollama for local models

## Contributing

This is a personal template, but feel free to:
- Fork for your own use
- Submit issues if you find bugs
- Share improvements

## License

MIT License - Use freely, build amazing things.

## About

Built by **Du'An Lightfoot** ([@labeveryday](https://github.com/labeveryday))
- Website: [duanlightfoot.com](https://duanlightfoot.com)
- YouTube: [LabEveryday](https://youtube.com/@labeveryday)
- Focus: Building AI agents, teaching others, creating in public

---

**Ready to build? Run `python src/agent.py` and start creating.**
