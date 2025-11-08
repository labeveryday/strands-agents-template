import asyncio
from strands import tool


# ============================================================================
# PATTERN 4: Async Tool (for concurrent execution)
# ============================================================================

@tool
async def fetch_api_data(endpoint: str) -> str:
    """Fetch data from an API asynchronously.
    
    Async tools are invoked concurrently by Strands for better performance.
    
    Args:
        endpoint: API endpoint to call
    
    Returns:
        API response data
    """
    # Simulate API call
    await asyncio.sleep(1)
    return f"Data from {endpoint}: [API Response]"