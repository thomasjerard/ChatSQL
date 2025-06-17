# mcp_server/tools.py
import sys
import os

# Add the project root to sys.path so 'db.connector' can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastmcp import FastMCP
from db.connector import run_query
from pydantic import Field

# Initialize FastMCP server with a name
mcp = FastMCP("Employee_Database_Tool_Server")

@mcp.tool()
def ask(query: str = Field(..., description="The SQL query to execute against the employees database.")) -> list:
    """
    Executes a SQL query against the employees database.
    Returns a list of row dictionaries or an error dictionary.
    """
    try:
        print(f"Executing SQL query: {query}")
        result = run_query(query)
        print(f"Query result: {result}")
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
        return [{"error": str(e)}]

# Allow this module to expose FastMCP objects when imported elsewhere
__all__ = ["mcp", "ask"]

# Run the server if executed directly
if __name__ == "__main__":
    print("Starting Employee Database Tool Server...")
    # --- CRITICAL CHANGE HERE: Remove transport="stdio" ---
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8002) # This will default to HTTP transport (usually 127.0.0.1:8000)