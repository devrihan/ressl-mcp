import os
from mcp.server.fastmcp import FastMCP
from typing import List

# 1. Initialize the MCP server
mcp = FastMCP("file-search-server")

@mcp.tool()
def search_in_file(keyword: str, filepath: str) -> List[str]:
    """
    Searches for a keyword in a specified file and returns all matching lines.
    
    Args:
        keyword (str): The word to search for (case-insensitive).
        filepath (str): The path to the file (e.g., 'sample.txt').
    """
    
    print(f"[Server] Received request: search for '{keyword}' in '{filepath}'")
    
    safe_base_dir = os.path.abspath(os.getcwd())
    target_file_abs = os.path.abspath(filepath)
    
    if not target_file_abs.startswith(safe_base_dir):
        print(f"[Server] ERROR: Path '{filepath}' is outside the allowed directory.")
        raise ValueError("Error: File path is not in the allowed directory.")
    

    try:
        matching_lines = []
        with open(target_file_abs, 'r') as f:
            for line_number, line in enumerate(f, 1):
                if keyword.lower() in line.lower():
                    matching_lines.append(f"L{line_number}: {line.strip()}")
        
        if not matching_lines:
            print("[Server] Found 0 matches.")
            return ["No matches found for that keyword."]

        print(f"[Server] Found {len(matching_lines)} matches.")
        return matching_lines

    except FileNotFoundError:
        print(f"[Server] ERROR: File not found at '{filepath}'")
        raise FileNotFoundError(f"Error: The file '{filepath}' was not found.")
    except Exception as e:
        print(f"[Server] ERROR: {e}")
        raise e

if __name__ == "__main__":
    print("Starting file search MCP server...")
    print(f"Ready to search for files in: {os.path.abspath(os.getcwd())}")

    mcp.run(transport="stdio")