import asyncio
from fastmcp import Client
from gemini.nl_to_sql import nl_to_sql
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import json
# from google.generativeai.types import TextContent
# from google.generativeai.types import TextContent
# import json

console = Console()

def print_table(results):
    if not results:
        console.print("[bold yellow]No results found[/bold yellow]")
        return

    # ✅ Handle response that looks like TextContent but without importing
    if isinstance(results, list) and hasattr(results[0], "text"):
        try:
            json_string = results[0].text
            results = json.loads(json_string)
        except Exception as e:
            console.print(f"[red]❌ Could not parse text response as JSON:[/red] {e}")
            return

    # ✅ Handle error results from DB
    if isinstance(results, list) and results and isinstance(results[0], dict) and "error" in results[0]:
        console.print(f"[red]Error from DB:[/red] {results[0]['error']}")
        return

    # ✅ Render table
    if isinstance(results, list) and len(results) > 0 and isinstance(results[0], dict):
        table = Table(show_header=True, header_style="bold blue")
        for col in results[0].keys():
            table.add_column(col)
        for row in results:
            table.add_row(*[str(val) for val in row.values()])
        console.print(table)
    else:
        console.print("[bold yellow]Unexpected result format.[/bold yellow]")

async def main():
    console.print("[bold green]💬 ChatSQL (Gemini + FastMCP)[/bold green] (Type 'exit' to quit)\n")

    # IMPORTANT: This is the standard HTTP address for FastMCP server
    mcp_server_address = "http://127.0.0.1:8002/mcp"

    try:
        # --------------------------------------------------------------------
        # THIS IS THE CRITICAL CONTEXT MANAGER BLOCK.
        # Everything that needs the 'client' object MUST be inside this block.
        # It ensures the client is connected when used and properly closed.
        # --------------------------------------------------------------------
        async with Client(mcp_server_address) as client:
            # ----------------------------------------------------------------
            # THIS 'while True' loop MUST BE INDENTED ONE LEVEL FURTHER
            # than the 'async with Client...' line.
            # All code that takes user input and calls the client should be here.
            # ----------------------------------------------------------------
            while True:
                user_input = input("🗨️  Ask (NL): ").strip()

                if user_input.lower() in ["exit", "quit"]:
                    console.print("[bold red]👋 Exiting ChatSQL...[/bold red]")
                    # Breaking out of this loop will automatically exit the 'async with' block.
                    break

                if not user_input:
                    console.print("[yellow]⚠️ Please enter a query.[/yellow]")
                    continue

                try:
                    # 1. Convert Natural Language to SQL
                    sql = nl_to_sql(user_input) # <--- COMMENT OUT THIS LINE
                    # sql = "SELECT id, name FROM employees LIMIT 3;" # <--- ADD THIS LINE FOR TESTING (Use a simple, valid SQL query)
                    console.print(Panel.fit(sql, title="Generated SQL", border_style="cyan"))
                    print(f"CLIENT DEBUG (before tool call): SQL variable value: '{sql}' (Type: {type(sql)})")

                    results = await client.call_tool("ask", {"query": sql})
                    console.print(Panel.fit(sql, title="Generated SQL", border_style="cyan"))

                    # 2. Call the 'ask' tool on the FastMCP server

                    # List the tools that were automatically generated
                    tools = await client.list_tools()
                    print("Generated Tools:")
                    for tool in tools:
                        print(f"- {tool.name}")

                    # This line is correctly inside the 'while True' loop, which is inside 'async with client'.
                    results = await client.call_tool("ask", {"query": sql})

                    # 3. Print the results from the database
                    print_table(results)
                    print("success")

                except Exception as e:
                    # Generic error handling for issues during NL->SQL or tool call
                    console.print(f"[red]❌ Error during processing:[/red] {e}")

    except Exception as conn_err:
        # This block catches errors specifically when trying to connect to the server initially.
        console.print(f"[red]❌ Cannot connect to FastMCP Server at {mcp_server_address}:[/red] {conn_err}")
        console.print("[bold yellow]Please ensure your FastMCP server is running in a separate terminal using './run_server.sh'.[/bold yellow]")

if __name__ == "__main__":
    # This runs the asynchronous main function.
    asyncio.run(main())