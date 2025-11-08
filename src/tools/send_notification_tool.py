from strands import tool


# ============================================================================
# PATTERN 2: Tool with Multiple Parameters
# ============================================================================

@tool
def send_notification(
    channel: str,
    message: str,
    urgency: str = "normal"
) -> str:
    """Send a notification to a communication channel.
    
    Args:
        channel: Target channel ('email', 'slack', 'sms')
        message: Notification message to send
        urgency: Priority level ('low', 'normal', 'high')
    
    Returns:
        Confirmation message
    """
    valid_channels = ["email", "slack", "sms"]
    if channel not in valid_channels:
        return f"Error: Invalid channel. Use: {', '.join(valid_channels)}"
    
    return f"✓ Sent {urgency} priority message to {channel}: {message}"