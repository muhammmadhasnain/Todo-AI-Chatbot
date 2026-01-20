---
name: mcp-sdk
description: Create and manage Model Context Protocol (MCP) servers and tools using the Official Python MCP SDK. Use when building MCP servers, defining MCP tools, resources, and prompts, or creating MCP clients. Provides patterns, examples, and best practices for MCP development.
---

# MCP SDK Skill

This skill provides guidance and tools for creating Model Context Protocol (MCP) servers and tools using the Official Python MCP SDK.

## When to Use This Skill

Use this skill when you need to:
1. Create new MCP servers with tools, resources, or prompts
2. Define MCP tools for LLM integration
3. Create MCP resources for data access
4. Build MCP clients to interact with servers
5. Implement authentication and security for MCP servers
6. Handle complex data types (images, files) in MCP tools

## Core Concepts

MCP enables LLMs to access external tools and resources through a standardized protocol. The Python SDK provides:
- `FastMCP`: High-level server framework for quick development
- `@mcp.tool()`: Decorator to define executable tools
- `@mcp.resource()`: Decorator to define accessible resources
- `@mcp.prompt()`: Decorator to define reusable prompts
- Client libraries for connecting to MCP servers

## Creating an MCP Server

Use the `FastMCP` class to create servers quickly:

```python
# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("My Server Name")

# Add an addition tool
@mcp.tool(description="Add two numbers together")
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Add a dynamic resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

# Add a prompt template
@mcp.prompt(description="Review code for best practices")
def review_code(code: str) -> str:
    return f"Please review this code for best practices:\\n\\n{code}"
```

## Advanced Server Patterns

### Using Context for Progress and Logging

```python
from mcp.server.fastmcp import FastMCP, Context

mcp = FastMCP("My App")

@mcp.tool()
async def long_task(files: list[str], ctx: Context) -> str:
    """Process multiple files with progress tracking"""
    for i, file in enumerate(files):
        ctx.info(f"Processing {file}")
        await ctx.report_progress(i, len(files))
        data, mime_type = await ctx.read_resource(f"file://{file}")
    return "Processing complete"
```

### Working with Images

```python
from mcp.server.fastmcp import FastMCP, Image
from PIL import Image as PILImage

mcp = FastMCP("Image Processor")

@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image"""
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")
```

## Client Implementation

Connect to MCP servers using client libraries:

```python
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

async def main():
    async with stdio_client(
        StdioServerParameters(command="uv", args=["run", "mcp-simple-tool"])
    ) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print(tools)

            # Call a tool
            result = await session.call_tool("add", {"a": 5, "b": 3})
            print(result)

asyncio.run(main())
```

## Transport Options

MCP servers support multiple transport mechanisms:
- **Stdio**: Default for local processes
- **SSE (Server-Sent Events)**: For HTTP-based communication
- **Streamable HTTP**: For web server integration

Start with different transports:
```bash
# Stdio (default)
uv run server.py

# SSE transport
uv run server.py --transport sse --port 8000

# Streamable HTTP
uv run server.py --transport streamable-http --port 3000
```

## Installation and Development

Install the MCP SDK:
```bash
pip install "mcp[cli]"
# or with uv
uv add "mcp[cli]"
```

For development:
```bash
mcp dev server.py
mcp dev server.py --with pandas --with numpy  # Add dependencies
mcp install server.py  # Install in Claude Desktop
mcp install server.py --name "My Server"  # Custom name
mcp install server.py -v API_KEY=abc123  # Environment variables
```

## Best Practices

1. **Type Hints**: Always use proper type hints for function parameters and return values
2. **Descriptions**: Provide clear descriptions for tools, resources, and prompts
3. **Error Handling**: Implement proper error handling in your tools
4. **Security**: Validate inputs and sanitize outputs when appropriate
5. **State Management**: Use stateless_http=True for HTTP-based servers when possible
6. **Resource URIs**: Use descriptive URI patterns for resources

## Reference Documentation

For detailed information about MCP concepts and advanced features, see the references directory.