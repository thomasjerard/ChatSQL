from mcp.server.fastmcp import FastMCP
from mcp_server import tools  # Ensure tools are registered

app = FastMCP(name="chatSQL MCP Server")

if __name__ == "__main__":
    app.run_stdio()