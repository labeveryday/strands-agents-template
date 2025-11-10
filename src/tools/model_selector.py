"""
Model selector tool for Strands agents.

Provides model information to help agents choose the best model for a task.
"""

from typing import Literal, Optional
from strands import tool


# Model registry with capabilities and costs
MODELS = {
    "claude-sonnet-4-20250514": {
        "provider": "anthropic",
        "name": "Claude Sonnet 4.5",
        "capabilities": ["chat", "reasoning", "code", "analysis", "long-context"],
        "context_window": 200000,
        "cost_input": 3.00,  # per 1M tokens
        "cost_output": 15.00,
        "speed": "medium",
        "quality": "highest",
        "use_cases": ["complex reasoning", "code generation", "deep analysis", "creative writing"]
    },
    "claude-3-5-sonnet-20241022": {
        "provider": "anthropic",
        "name": "Claude 3.5 Sonnet",
        "capabilities": ["chat", "reasoning", "code", "analysis"],
        "context_window": 200000,
        "cost_input": 3.00,
        "cost_output": 15.00,
        "speed": "medium",
        "quality": "high",
        "use_cases": ["general tasks", "coding", "analysis"]
    },
    "claude-3-haiku-20240307": {
        "provider": "anthropic",
        "name": "Claude 3 Haiku",
        "capabilities": ["chat", "simple-tasks"],
        "context_window": 200000,
        "cost_input": 0.25,
        "cost_output": 1.25,
        "speed": "fast",
        "quality": "good",
        "use_cases": ["simple tasks", "classification", "quick responses"]
    },
    "gpt-4o": {
        "provider": "openai",
        "name": "GPT-4o",
        "capabilities": ["chat", "vision", "reasoning", "code", "multimodal"],
        "context_window": 128000,
        "cost_input": 2.50,
        "cost_output": 10.00,
        "speed": "medium",
        "quality": "high",
        "use_cases": ["multimodal tasks", "vision", "general reasoning"]
    },
    "gpt-4o-mini": {
        "provider": "openai",
        "name": "GPT-4o Mini",
        "capabilities": ["chat", "vision", "code", "multimodal"],
        "context_window": 128000,
        "cost_input": 0.15,
        "cost_output": 0.60,
        "speed": "fast",
        "quality": "good",
        "use_cases": ["cheap tasks", "quick responses", "simple vision"]
    },
    "gpt-4-turbo": {
        "provider": "openai",
        "name": "GPT-4 Turbo",
        "capabilities": ["chat", "vision", "code", "reasoning"],
        "context_window": 128000,
        "cost_input": 10.00,
        "cost_output": 30.00,
        "speed": "medium",
        "quality": "high",
        "use_cases": ["complex tasks", "high quality output"]
    },
    "o1": {
        "provider": "openai",
        "name": "O1",
        "capabilities": ["reasoning", "math", "science", "code"],
        "context_window": 128000,
        "cost_input": 15.00,
        "cost_output": 60.00,
        "speed": "slow",
        "quality": "highest",
        "use_cases": ["complex reasoning", "math", "science", "research"]
    },
    "o1-mini": {
        "provider": "openai",
        "name": "O1 Mini",
        "capabilities": ["reasoning", "math", "code"],
        "context_window": 128000,
        "cost_input": 3.00,
        "cost_output": 12.00,
        "speed": "medium",
        "quality": "high",
        "use_cases": ["reasoning", "cheaper than o1"]
    },
}


@tool
def get_available_models(
    provider: Optional[Literal["anthropic", "openai"]] = None,
    capability: Optional[str] = None,
    max_cost_input: Optional[float] = None,
    min_quality: Optional[Literal["good", "high", "highest"]] = None
) -> str:
    """
    Get information about available AI models with optional filtering.

    Use this tool to choose the best model for a specific task based on
    requirements like cost, quality, speed, or capabilities.

    Args:
        provider: Filter by provider (anthropic or openai)
        capability: Filter by capability (chat, reasoning, code, vision, etc.)
        max_cost_input: Maximum input cost per 1M tokens
        min_quality: Minimum quality level (good, high, highest)

    Returns:
        JSON string with model information

    Example:
        To find a cheap model for simple tasks:
        get_available_models(max_cost_input=1.0, min_quality="good")

        To find models with vision capability:
        get_available_models(capability="vision")

        To find best reasoning model:
        get_available_models(capability="reasoning", min_quality="highest")
    """
    import json

    quality_levels = {"good": 1, "high": 2, "highest": 3}

    filtered = {}
    for model_id, info in MODELS.items():
        # Apply filters
        if provider and info["provider"] != provider:
            continue
        if capability and capability not in info["capabilities"]:
            continue
        if max_cost_input and info["cost_input"] > max_cost_input:
            continue
        if min_quality and quality_levels[info["quality"]] < quality_levels[min_quality]:
            continue

        filtered[model_id] = info

    result = {
        "count": len(filtered),
        "models": filtered
    }

    return json.dumps(result, indent=2)


@tool
def get_model_recommendation(
    task_description: str,
    priority: Literal["cost", "quality", "speed", "balanced"] = "balanced"
) -> str:
    """
    Get a model recommendation based on task description and priority.

    The tool analyzes the task and suggests the best model to use.

    Args:
        task_description: Description of the task (e.g., "analyze code", "quick chat", "complex reasoning")
        priority: What to optimize for (cost, quality, speed, balanced)

    Returns:
        JSON with recommended model and reasoning

    Example:
        get_model_recommendation("write complex code with detailed explanations", priority="quality")
        get_model_recommendation("simple classification task", priority="cost")
    """
    import json

    task_lower = task_description.lower()

    # Analyze task requirements
    needs_vision = any(word in task_lower for word in ["image", "vision", "picture", "visual"])
    needs_reasoning = any(word in task_lower for word in ["complex", "reasoning", "math", "science", "research"])
    needs_code = any(word in task_lower for word in ["code", "programming", "debug", "implement"])
    is_simple = any(word in task_lower for word in ["simple", "quick", "basic", "classification"])

    # Default recommendation
    recommended = "claude-sonnet-4-20250514"
    reasoning = "Balanced model for general tasks"

    # Cost-optimized
    if priority == "cost":
        if is_simple:
            recommended = "claude-3-haiku-20240307"
            reasoning = "Cheapest model, good for simple tasks"
        else:
            recommended = "gpt-4o-mini"
            reasoning = "Good balance of cost and capability"

    # Quality-optimized
    elif priority == "quality":
        if needs_reasoning:
            recommended = "o1"
            reasoning = "Best reasoning model available"
        elif needs_code:
            recommended = "claude-sonnet-4-20250514"
            reasoning = "Excellent code generation and reasoning"
        else:
            recommended = "claude-sonnet-4-20250514"
            reasoning = "Highest quality general-purpose model"

    # Speed-optimized
    elif priority == "speed":
        if needs_vision:
            recommended = "gpt-4o-mini"
            reasoning = "Fast multimodal model"
        else:
            recommended = "claude-3-haiku-20240307"
            reasoning = "Fastest model available"

    # Balanced
    else:
        if needs_reasoning and not is_simple:
            recommended = "o1-mini"
            reasoning = "Good reasoning at reasonable cost"
        elif needs_vision:
            recommended = "gpt-4o"
            reasoning = "Best multimodal model"
        elif needs_code:
            recommended = "claude-sonnet-4-20250514"
            reasoning = "Excellent for code tasks"
        elif is_simple:
            recommended = "gpt-4o-mini"
            reasoning = "Cheap and fast for simple tasks"
        else:
            recommended = "claude-sonnet-4-20250514"
            reasoning = "Best general-purpose model"

    result = {
        "recommended_model": recommended,
        "model_info": MODELS[recommended],
        "reasoning": reasoning,
        "task_analysis": {
            "needs_vision": needs_vision,
            "needs_reasoning": needs_reasoning,
            "needs_code": needs_code,
            "is_simple": is_simple
        }
    }

    return json.dumps(result, indent=2)


@tool
def compare_models(model_ids: list[str]) -> str:
    """
    Compare multiple models side-by-side.

    Args:
        model_ids: List of model IDs to compare

    Returns:
        JSON with comparison data

    Example:
        compare_models(["claude-sonnet-4-20250514", "gpt-4o", "o1-mini"])
    """
    import json

    comparison = {}
    for model_id in model_ids:
        if model_id in MODELS:
            comparison[model_id] = MODELS[model_id]
        else:
            comparison[model_id] = {"error": "Model not found"}

    return json.dumps(comparison, indent=2)
