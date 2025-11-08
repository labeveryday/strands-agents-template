from strands import tool


# ============================================================================
# PATTERN 3: Tool with Error Handling
# ============================================================================

@tool
def divide_numbers(a: float, b: float) -> str:
    """Safely divide two numbers with error handling.
    
    Args:
        a: Numerator
        b: Denominator
    
    Returns:
        Result of division or error message
    """
    try:
        if b == 0:
            return "Error: Cannot divide by zero"
        result = a / b
        return f"{a} ÷ {b} = {result}"
    except Exception as e:
        return f"Error: {str(e)}"