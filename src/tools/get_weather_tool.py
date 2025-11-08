from strands import tool

# ============================================================================
# PATTERN 1: Simple Synchronous Tool
# ============================================================================

@tool
def get_weather(city: str) -> str:
    """Get weather information for a city.
    
    Args:
        city: Name of the city
    
    Returns:
        Weather description
    """
    # In production, call a real weather API
    weather_data = {
        "Seattle": "Cloudy, 55°F",
        "San Francisco": "Foggy, 62°F",
        "Miami": "Sunny, 85°F",
        "New York": "Rainy, 48°F"
    }
    return weather_data.get(city, f"Weather data not available for {city}")