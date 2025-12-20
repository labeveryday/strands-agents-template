# Examples

This directory contains example agents demonstrating different use cases.

## MCP Documentation Agent

`mcp_docs_agent.py` - An agent with MCP server integration for accessing AgentCore and Strands documentation.

```bash
python examples/mcp_docs_agent.py
```

This agent can:
- Search and fetch AWS AgentCore documentation
- Search and fetch Strands Agents framework documentation
- Answer questions about building and deploying agents

---

## Gemini Image Generation

`gemini_image_example.py` - Generate and edit images using Gemini 3 Pro Image Preview.

```bash
# Generate an image
python examples/gemini_image_example.py --prompt "A serene mountain landscape at sunset"

# Edit an existing image
python examples/gemini_image_example.py --edit path/to/image.png --edit-prompt "Make it more vibrant"

# Interactive mode with session tracking
python examples/gemini_image_example.py --interactive

# Without hub tracking
python examples/gemini_image_example.py --no-hub --prompt "A cute robot"
```

**Features:**
- Text-to-image generation with `generate_image` tool
- Image editing with `edit_image` tool
- Hub integration for session tracking and metrics
- Interactive agent mode

**Requirements:** `GOOGLE_API_KEY` environment variable

---

## Gemini Video Generation

`gemini_video_example.py` - Generate videos using Veo 3.1 (text-to-video and image-to-video).

```bash
# Generate video from text (takes 1-5 minutes)
python examples/gemini_video_example.py --prompt "A drone shot over a coastal city at golden hour"

# Generate video from image
python examples/gemini_video_example.py --image path/to/image.png --prompt "Animate this scene"

# Specify duration (4 or 6 seconds)
python examples/gemini_video_example.py --duration 6 --prompt "Ocean waves crashing"

# Interactive mode
python examples/gemini_video_example.py --interactive
```

**Features:**
- Text-to-video generation with `generate_video` tool
- Image-to-video animation with `generate_video_from_image` tool
- Duration options: 4 or 6 seconds
- Async polling for long-running operations
- Hub integration for session tracking and metrics

**Requirements:** `GOOGLE_API_KEY` environment variable

---

## Gemini Music Generation

`gemini_music_example.py` - Generate music using Lyria RealTime via WebSocket streaming.

```bash
# Generate music from text
python examples/gemini_music_example.py --prompt "Upbeat electronic dance track with synth leads"

# Specify duration (5-120 seconds)
python examples/gemini_music_example.py --duration 30 --prompt "Calm ambient meditation music"

# Weighted prompts for blending styles
python examples/gemini_music_example.py --weighted --prompts "jazz:0.7" "electronic:0.3"

# Interactive mode
python examples/gemini_music_example.py --interactive
```

**Features:**
- Text-to-music generation with `generate_music` tool
- Weighted prompt blending with `generate_music_weighted` tool
- Real-time WebSocket streaming
- Stereo 48kHz WAV output
- Hub integration for session tracking and metrics

**Requirements:** `GOOGLE_API_KEY` environment variable (uses v1alpha API for Lyria)

---

## Deploying to AWS Bedrock AgentCore

Deploy your Strands agent to [AWS Bedrock AgentCore](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore.html) for serverless, production deployment.

### Step 1: Create AgentCore Entry Point

AgentCore requires a specific entry point pattern using `BedrockAgentCoreApp`:

```python
# agentcore_agent.py
from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent
from strands.models.bedrock import BedrockModel

app = BedrockAgentCoreApp()

# Create your agent
model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="us-east-1",
)

agent = Agent(
    model=model,
    system_prompt="You are a helpful assistant...",
)

@app.entrypoint
def invoke(payload, context):
    """AgentCore entry point - receives requests and returns responses."""
    user_message = payload.get("prompt", "Hello!")
    result = agent(user_message)
    return {"result": str(result)}

if __name__ == "__main__":
    app.run()
```

### Step 2: Create Requirements File

```txt
# requirements.txt for AgentCore
bedrock-agentcore
strands-agents>=0.1.0
strands-agents-tools
boto3>=1.34.0
```

### Step 3: Deploy with AgentCore CLI

```bash
# Install AgentCore CLI
pip install bedrock-agentcore-starter-toolkit

# Configure your agent
agentcore configure --entrypoint agentcore_agent.py --non-interactive

# Deploy to AWS
agentcore launch

# Test your deployed agent
agentcore invoke '{"prompt": "Hello world!"}'

# Check status
agentcore status
```

### Key Requirements

- **Entry point**: Use `@app.entrypoint` decorator on your invoke function
- **App wrapper**: Initialize `BedrockAgentCoreApp()` and call `app.run()`
- **Dependencies**: Include `bedrock-agentcore` in requirements.txt
- **Bedrock models**: Use `BedrockModel` for model access within AgentCore

### MCP Tools on AgentCore

For MCP server tools on AgentCore:

1. Use the [AgentCore Gateway](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore-gateway.html) to expose MCP servers
2. Configure IAM permissions for cross-service access
3. Update tool endpoints to use Gateway URLs

See the [AgentCore documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore.html) for detailed setup.
