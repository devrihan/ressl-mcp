# MCP File Search Server

This project is a simple server built using `FastMCP` that exposes a tool for searching within files.

The server provides one remote tool:
* `search_in_file(keyword: str, filepath: str)`: This function searches the specified file on the server for a given keyword (case-insensitively) and returns a list of all matching lines, prefixed with their line number.

For security, the server will only search for files within its own working directory.

## How to Run

1.  Make sure any dependencies (like the `mcp` library) are installed.
2.  Start the server from your terminal:
    ```bash
    python server.py
    ```
3.  The server will print a startup message and run, listening for requests via `stdio`.

## Example

The repository includes a `sample.txt` file. If a client calls the `search_in_file` tool with `keyword="MCP"` and `filepath="sample.txt"`, the server will find two matches and return the following list:

```json
[
  "L1: This is a sample file for the MCP server task.",
  "L2: MCP stands for Model Context Protocol."
]
