from strands import Agent
from strands.models.bedrock import BedrockModel


model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="us-east-1",
    max_tokens=4096,
    temperature=1,
    additional_request_fields={
        "thinking": {
            "type": "enabled",
            "budget_tokens": 1024 
        }
    },
    additional_headers={
        "anthropic-beta": "extended-context-1m-2025-04-14"
    }
)

agent = Agent(model=model)
agent("What is an AI agent?")
