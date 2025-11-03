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
    
    # Log in Terminal
    print(f"[Server] Received request: search for '{keyword}' in '{filepath}'")
    
    # Get the absolute path for the current working directory
    safe_base_dir = os.path.abspath(os.getcwd())
    # Get the absolute path for the file the user wants to access
    target_file_abs = os.path.abspath(filepath)
    
    # Check if the requested file path is 'inside' our project folder
    if not target_file_abs.startswith(safe_base_dir):
        print(f"[Server] ERROR: Path '{filepath}' is outside the allowed directory.")
        # Raise an error
        raise ValueError("Error: File path is not in the allowed directory.")
    

    try:
        matching_lines = []
        with open(target_file_abs, 'r') as f:
            # Enumerate to get line numbers
            for line_number, line in enumerate(f, 1):
                # Make the search case-insensitive
                if keyword.lower() in line.lower():
                    # Add the line number and text to our results
                    matching_lines.append(f"L{line_number}: {line.strip()}")
        
        if not matching_lines:
            print("[Server] Found 0 matches.")
            return ["No matches found for that keyword."]

        print(f"[Server] Found {len(matching_lines)} matches.")
        return matching_lines

    except FileNotFoundError:
        print(f"[Server] ERROR: File not found at '{filepath}'")
        # Raise an error that the MCP client will understand
        raise FileNotFoundError(f"Error: The file '{filepath}' was not found.")
    except Exception as e:
        print(f"[Server] ERROR: {e}")
        raise e

# 4. Run the server
if __name__ == "__main__":
    print("Starting file search MCP server...")
    print(f"Ready to search for files in: {os.path.abspath(os.getcwd())}")
    # 'stdio' (standard input/output) is the transport used
    # to connect to local tools like the MCP Inspector.
    mcp.run(transport="stdio")