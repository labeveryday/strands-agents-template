# Strands Agents Template

**A production-ready template for building AI agents with [Strands Agents](https://strandsagents.com/latest/).**

Created by [Du'An Lightfoot](https://duanlightfoot.com) | [@labeveryday](https://github.com/labeveryday)

---

## Features

- ✅ **Multi-Model Support** - Anthropic, OpenAI, Writer, and Ollama (local) with easy switching
- ✅ **Model Selection Tools** - Smart model recommendations based on task requirements and constraints
- ✅ **MCP Server Integration** - Built-in AgentCore and Strands documentation servers
- ✅ **Session Management** - Built-in conversation history and persistence
- ✅ **Auto-Tool Loading** - Tools automatically discovered from `src/tools/` directory
- ✅ **Custom Hooks** - Extensible logging and monitoring system
- ✅ **Shell, Editor & Time Tools** - Built-in Strands tools for system interaction

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
- `What model should I use for complex reasoning tasks?`
- `Compare Claude Sonnet 4.5, GPT-4o, and O1-mini`
- `Show me available models under $1 per million tokens`
- `What's in the Strands documentation about hooks?`
- Type `tools` to see all available tools
- Type `exit` to quit

## Project Structure

```
.
├── src/
│   ├── agent.py              # Main agent with MCP server integration
│   ├── models/
│   │   └── models.py         # Model configurations (Anthropic, OpenAI, Writer, Ollama)
│   └── tools/                # Agent tools (auto-loaded)
│       ├── __init__.py       # Tool exports
│       └── model_selector.py # Model selection and comparison tools
├── sessions/                 # Conversation history (auto-created)
├── .env                      # API keys (you create this)
├── CLAUDE.md                 # Project documentation for Claude Code
└── requirements.txt          # Dependencies
```

## Switching Models

Edit `src/agent.py` line 37:

```python
# Current (Anthropic Claude Sonnet 4.5)
from models import anthropic_model
MODEL = anthropic_model(model_id="claude-sonnet-4-5-20250929")

# Switch to OpenAI
from models import openai_model
MODEL = openai_model(model_id="gpt-4o")

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

## Built-in Tools

### Model Selection Tools (`src/tools/model_selector.py`)

| Tool | Purpose | Example Use |
|------|---------|-------------|
| `get_available_models` | Filter models by provider, capability, cost, or quality | Find models under $2/M tokens with reasoning capability |
| `get_model_recommendation` | Get model suggestions based on task description | "What model for complex code generation?" |
| `compare_models` | Compare multiple models side-by-side | Compare Claude Sonnet 4.5, GPT-4o, and O1 |

### Strands Built-in Tools

- `shell` - Execute shell commands
- `editor` - Edit files with AI assistance
- `current_time` - Get current date/time

### MCP Server Tools

- **AgentCore MCP** - Search and fetch AWS AgentCore documentation
- **Strands MCP** - Search and fetch Strands Agents documentation

## Configuration Options

### Agent Configuration (`src/agent.py`)

```python
# MCP Clients for documentation access
agentcore_mcp_client = MCPClient(...)  # AWS AgentCore docs
strands_mcp_client = MCPClient(...)    # Strands Agents docs

agent = Agent(
    model=MODEL,                          # Your chosen model
    tools=[shell, current_time, editor] + mcp_tools,  # Built-in + MCP tools
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
> Show me available models with vision capability
> Compare Claude Sonnet 4.5 and GPT-4o
```

The model selector tool analyzes your task requirements and suggests the best model based on:
- **Cost** - Optimize for lowest price per million tokens
- **Quality** - Prioritize output quality and capabilities
- **Speed** - Choose fastest response times
- **Balanced** - Best overall value

Check `src/models/models.py` for detailed specifications including context windows, token limits, pricing, and capabilities.

## MCP Server Integration

The template includes two MCP (Model Context Protocol) servers for documentation access:

### AgentCore MCP Server
Access AWS AgentCore documentation directly in your agent:
```
> How do I use event handlers in AgentCore?
> Search AgentCore docs for session management
```

### Strands MCP Server
Query Strands Agents framework documentation:
```
> What are hooks in Strands?
> How do I create async tools?
```

These servers auto-approve read-only documentation queries for seamless integration.

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
