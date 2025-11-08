from strands import tool


# ============================================================================
# PATTERN 7: Tool with File Operations
# ============================================================================

@tool
def count_lines_in_file(filepath: str) -> str:
    """Count lines in a text file.
    
    Args:
        filepath: Path to the file
    
    Returns:
        Number of lines in the file
    """
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
        return f"File '{filepath}' contains {len(lines)} lines"
    except FileNotFoundError:
        return f"Error: File '{filepath}' not found"
    except Exception as e:
        return f"Error reading file: {str(e)}"