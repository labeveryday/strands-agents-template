from strands import tool


@tool
def get_available_models() -> str:
    """Get all available AI models with their specifications for model selection.

    Returns:
        Complete list of available models with context, pricing, reasoning capabilities, and optimal use cases
    """

    return """
# ANTHROPIC MODELS

## claude-haiku-4-5-20251001
- Context: 200k
- Max Output: 64k tokens
- Cost: $1/M input, $5/M output
- Reasoning: Yes
- Best for: Quick tasks, high volume, cost-sensitive, real-time responses

## claude-sonnet-4-5-20250929
- Context: 200k (1M beta)
- Max Output: 64k tokens
- Cost: $3/M input, $15/M output
- Reasoning: Yes
- Best for: Complex reasoning, analysis, writing, balanced performance

## claude-sonnet-4-20250514
- Context: 200k (1M beta)
- Max Output: 64k tokens
- Cost: $3/M input, $15/M output
- Reasoning: Yes
- Best for: Complex tasks, stable production, extended context

## claude-3-7-sonnet-20250219
- Context: 200k
- Max Output: 64k tokens
- Cost: $3/M input, $15/M output
- Reasoning: Yes
- Best for: General purpose, reliable performance

## claude-3-5-haiku-20241022
- Context: 200k
- Max Output: 8k tokens
- Cost: $0.80/M input, $4/M output
- Reasoning: No
- Best for: Simple tasks, minimal cost, no reasoning needed


# OPENAI MODELS

## gpt-5-2025-08-07
- Context: 400k
- Max Output: 128k tokens
- Cost: $1.25/M input, $10/M output
- Reasoning: Yes
- Best for: Complex reasoning, large context, balanced cost/performance

## gpt-4.1-2025-04-14
- Context: 1M
- Max Output: 32k tokens
- Cost: $2/M input, $8/M output
- Reasoning: No
- Best for: Massive context, document processing, no reasoning needed

## o4-mini-2025-04-16
- Context: 200k
- Max Output: 100k tokens
- Cost: $1.10/M input, $4.40/M output
- Reasoning: Yes
- Best for: Reasoning on budget, large outputs, cost-effective

## gpt-5-mini-2025-08-07
- Context: 400k
- Max Output: 128k tokens
- Cost: $0.25/M input, $2/M output
- Reasoning: Yes
- Best for: High volume, budget-friendly, fast reasoning

## gpt-5-nano-2025-08-07
- Context: 400k
- Max Output: 128k tokens
- Cost: $0.05/M input, $0.40/M output
- Reasoning: Yes
- Best for: Ultra-low cost, simple reasoning, massive scale

## gpt-4o-2024-11-20
- Context: 128k
- Max Output: 16k tokens
- Cost: $2.50/M input, $1.25/M output
- Reasoning: No
- Best for: Legacy compatibility, standard tasks

## gpt-5-pro-2025-10-06
- Context: 400k
- Max Output: 272k tokens
- Cost: $1.25/M input, $120/M output
- Reasoning: Yes (slower)
- Best for: Deep reasoning, research, when cost doesn't matter

## o4-mini-deep-research-2025-06-26
- Context: 200k
- Max Output: 100k tokens
- Cost: $2/M input, $8/M output
- Reasoning: Yes
- Best for: Research, deep analysis, thorough investigation


# WRITER MODELS

## palmyra-x5
- Context: 1M
- Max Output: 32k tokens
- Cost: $0.60/M input, $6.00/M output
- Reasoning: No
- Best for: Massive context, content generation, cost-effective

## palmyra-x4
- Context: 128k
- Max Output: 32k tokens
- Cost: $2.50/M input, $10/M output
- Reasoning: No
- Best for: Writer ecosystem, standard content tasks

## palmyra-fin
- Context: 128k
- Max Output: 32k tokens
- Cost: $5/M input, $12/M output
- Reasoning: No
- Best for: Financial content, domain-specific writing

## palmyra-med
- Context: 32k
- Max Output: 8k tokens
- Cost: $5/M input, $12/M output
- Reasoning: No
- Best for: Medical content, healthcare writing

## palmyra-creative
- Context: 128k
- Max Output: 32k tokens
- Cost: $5/M input, $12/M output
- Reasoning: No
- Best for: Creative writing, storytelling, marketing


# OLLAMA MODELS (Local)

## qwen3:4b
- Context: 260k
- Max Output: 128k tokens
- Cost: Free (local)
- Reasoning: No
- Best for: Local/private, no API costs, offline use

## llama3.1:latest
- Context: 131k
- Max Output: 128k tokens
- Cost: Free (local)
- Reasoning: No
- Best for: Local/private, open source, offline use

## gemma3n:e4b
- Context: 32k
- Max Output: 8k tokens
- Cost: Free (local)
- Reasoning: No
- Note: Does not support tools
- Best for: Simple local tasks without tool use

## nomic-embed-text:latest
- Context: 2k
- Max Output: N/A (embedding model)
- Cost: Free (local)
- Type: Embedding model
- Best for: Text embeddings, semantic search, RAG applications
"""
