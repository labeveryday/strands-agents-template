from strands import tool, ToolContext


# ============================================================================
# PATTERN 5: Tool with Context (Access invocation state)
# ============================================================================

@tool(context=True)
def get_user_preferences(tool_context: ToolContext) -> str:
    """Get user preferences from invocation state.
    
    This tool has access to invocation_state passed to the agent.
    
    Returns:
        User preferences
    """
    user_id = tool_context.invocation_state.get("user_id", "unknown")
    preferences = tool_context.invocation_state.get("preferences", {})
    
    if not preferences:
        return f"No preferences found for user: {user_id}"
    
    prefs_list = [f"{k}: {v}" for k, v in preferences.items()]
    return f"User {user_id} preferences:\n" + "\n".join(prefs_list)