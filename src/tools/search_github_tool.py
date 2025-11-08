from strands import tool


# ============================================================================
# PATTERN 6: Tool with External API
# ============================================================================

@tool
def search_github(query: str, max_results: int = 5) -> str:
    """Search GitHub repositories.
    
    Args:
        query: Search query
        max_results: Maximum number of results (default: 5)
    
    Returns:
        Search results
    """
    try:
        import requests
        
        url = "https://api.github.com/search/repositories"
        params = {"q": query, "per_page": max_results, "sort": "stars"}
        headers = {"Accept": "application/vnd.github.v3+json"}
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        repos = data.get("items", [])
        
        if not repos:
            return f"No repositories found for: {query}"
        
        results = []
        for repo in repos[:max_results]:
            results.append(
                f"• {repo['full_name']} - ⭐ {repo['stargazers_count']}\n"
                f"  {repo['description']}\n"
                f"  {repo['html_url']}"
            )
        
        return "\n\n".join(results)
        
    except Exception as e:
        return f"Error searching GitHub: {str(e)}"