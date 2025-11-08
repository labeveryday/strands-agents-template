from strands import tool


# ============================================================================
# PATTERN 8: Tool with Validation
# ============================================================================

@tool
def validate_email(email: str) -> str:
    """Validate an email address format.
    
    Args:
        email: Email address to validate
    
    Returns:
        Validation result
    """
    import re
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(pattern, email):
        return f"✓ Valid email: {email}"
    else:
        return f"✗ Invalid email format: {email}"