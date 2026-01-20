"""
Example MCP Server with Tools, Resources, and Prompts
"""

from mcp.server.fastmcp import FastMCP
import httpx
import sqlite3
from typing import List
from mcp.server.fastmcp import Context, Image
from PIL import Image as PILImage


# Create an MCP server instance
mcp = FastMCP("Example Server")


# Example 1: Simple arithmetic tool
@mcp.tool(description="Add two numbers together")
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.tool(description="Multiply two numbers")
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b


# Example 2: Async tool for fetching data from web
@mcp.tool(description="Fetch content from a URL")
async def fetch_url_content(url: str) -> str:
    """Fetch content from a URL"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            return f"Status: {response.status_code}\nContent: {response.text[:500]}..."
        except Exception as e:
            return f"Error fetching URL: {str(e)}"


# Example 3: Resource that provides database schema
@mcp.resource("db-schema://{database_name}")
def get_database_schema(database_name: str) -> str:
    """Provide the database schema as a resource"""
    # In a real implementation, this would connect to the actual database
    if database_name == "users":
        return """
        Table: users
        - id (INTEGER, PRIMARY KEY)
        - name (TEXT)
        - email (TEXT)
        - created_at (TIMESTAMP)

        Table: orders
        - id (INTEGER, PRIMARY KEY)
        - user_id (INTEGER, FOREIGN KEY)
        - amount (REAL)
        - status (TEXT)
        """
    return f"Schema for database: {database_name}"


# Example 4: Tool that processes files with progress tracking
@mcp.tool(description="Process multiple files with progress reporting")
async def process_files_with_context(files: List[str], ctx: Context) -> str:
    """Process multiple files with progress tracking using context"""
    results = []
    for i, file_path in enumerate(files):
        ctx.info(f"Processing file {i+1} of {len(files)}: {file_path}")
        await ctx.report_progress(i, len(files))

        # Simulate file processing
        result = f"Processed: {file_path}"
        results.append(result)

    return f"Processed {len(files)} files successfully: {results}"


# Example 5: Tool that works with images
@mcp.tool(description="Create a thumbnail from an image file")
def create_thumbnail_from_image(image_path: str, size: int = 100) -> Image:
    """Create a thumbnail from an image file"""
    try:
        img = PILImage.open(image_path)
        img.thumbnail((size, size))
        # Return as MCP Image object
        return Image(data=img.tobytes(), format="png")
    except Exception as e:
        raise ValueError(f"Could not create thumbnail: {str(e)}")


# Example 6: Prompt template for code review
@mcp.prompt(description="Review code for best practices and potential issues")
def code_review_prompt(code: str) -> str:
    """Create a prompt for code review"""
    return f"""
Please review the following code for:
1. Best practices adherence
2. Potential bugs or issues
3. Performance considerations
4. Security vulnerabilities

Code to review:
{code}
"""


# Example 7: Prompt template with multiple message types
@mcp.prompt(description="Debug an error with interactive conversation")
def debug_error_prompt(error: str) -> list:
    """Create a multi-message prompt for debugging"""
    from mcp.server.fastmcp.prompts import base

    return [
        base.UserMessage(f"I'm encountering this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help you debug this. Can you provide more context about what you were trying to do?"),
        base.UserMessage("Please also share any relevant code or steps that led to this error.")
    ]


# Example 8: Tool for database operations (simulated)
@mcp.tool(description="Execute a SQL query on the database")
def execute_sql_query(query: str) -> str:
    """Execute a SQL query (simulated)"""
    # This is a simulation - in real usage, connect to your actual database
    if "SELECT" in query.upper():
        return f"Query executed successfully. Sample result for: {query[:50]}..."
    elif "INSERT" in query.upper() or "UPDATE" in query.upper() or "DELETE" in query.upper():
        return f"Data modification query executed: {query[:50]}..."
    else:
        return f"Query processed: {query[:50]}..."


if __name__ == "__main__":
    # This would be run with uv or similar to start the server
    print("MCP Server defined. Run with: uv run example_server.py")