# Examples

This directory contains example agents demonstrating different use cases.

## MCP Documentation Agent

`mcp_docs_agent.py` - An agent with MCP server integration for accessing AgentCore and Strands documentation.

```bash
cd examples
python mcp_docs_agent.py
```

This agent can:
- Search and fetch AWS AgentCore documentation
- Search and fetch Strands Agents framework documentation
- Answer questions about building and deploying agents

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
