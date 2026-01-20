# MCP SDK Reference Documentation

## Overview

The Model Context Protocol (MCP) SDK for Python enables developers to create servers that expose tools, resources, and prompts to LLMs. This reference provides detailed information about the SDK's capabilities and best practices.

## Core Components

### FastMCP Server

The `FastMCP` class is the primary interface for creating MCP servers:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Server Name", stateless_http=True)  # stateless_http=True for HTTP transports
```

Key parameters:
- `name`: Human-readable name for the server
- `stateless_http`: Whether the server is stateless for HTTP transports (default: False)

### Decorators

The SDK provides three main decorators for defining server capabilities:

#### @mcp.tool()
Defines executable functions that LLMs can call:

```python
@mcp.tool(description="Brief description of what the tool does")
def function_name(param1: type, param2: type) -> return_type:
    """Detailed docstring about the function"""
    # Implementation
    return result
```

#### @mcp.resource()
Defines resources that LLMs can read:

```python
@mcp.resource("pattern://{param_name}")
def function_name(param_name: type) -> str:
    """Returns resource content"""
    return content
```

URI patterns support:
- `resource://static` - Static resources
- `resource://{param}` - Dynamic resources with single parameter
- `resource://{param1}/{param2}` - Dynamic resources with multiple parameters

#### @mcp.prompt()
Defines prompt templates:

```python
@mcp.prompt(description="Brief description of the prompt's purpose")
def prompt_name(param: type) -> str:
    """Returns prompt text"""
    return prompt_text
```

## Context Object

The `Context` object provides access to MCP capabilities within tools:

```python
@mcp.tool()
async def tool_with_context(param: str, ctx: Context) -> str:
    # Logging
    ctx.info("Processing started")
    ctx.warning("Warning message")
    ctx.error("Error message")

    # Progress reporting
    await ctx.report_progress(current, total)

    # Reading resources
    content, mime_type = await ctx.read_resource("uri://path")

    return "result"
```

## Return Types

MCP tools can return various types:

### Basic Types
- `str`, `int`, `float`, `bool`
- `list`, `dict` with basic types

### Special Types
- `Image`: For image data
- `TextContent`: For structured text content
- `JsonContent`: For JSON content

```python
from mcp.server.fastmcp import Image

@mcp.tool()
def get_image() -> Image:
    # Create and return an image
    return Image(data=binary_data, format="png")
```

## Transport Mechanisms

MCP supports multiple transport protocols:

### Stdio (Default)
- Used for local processes
- Command: `uv run server.py`

### Server-Sent Events (SSE)
- HTTP-based communication
- Command: `uv run server.py --transport sse --port 8000`

### Streamable HTTP
- Modern HTTP-based communication
- Command: `uv run server.py --transport streamable-http --port 3000`

## Client Implementation

### Stdio Client
```python
from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        # Use session...
```

### HTTP Client
```python
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession

async with streamablehttp_client("http://server-url/mcp") as (read, write, _):
    async with ClientSession(read, write) as session:
        await session.initialize()
        # Use session...
```

## Common Operations

### List Available Tools
```python
tools = await session.list_tools()
for tool in tools.tools:
    print(f"{tool.name}: {tool.description}")
```

### Call a Tool
```python
result = await session.call_tool("tool_name", {"param": "value"})
```

### List Resources
```python
resources = await session.list_resources()
for resource in resources.resources:
    print(f"{resource.uri}: {resource.name}")
```

### Read a Resource
```python
content = await session.read_resource("uri://path")
```

## Security Considerations

1. **Input Validation**: Always validate and sanitize inputs to tools
2. **Resource Access**: Limit resource access to authorized paths
3. **Environment Variables**: Use environment variables for sensitive data
4. **Rate Limiting**: Implement rate limiting for expensive operations

## Best Practices

### Function Design
- Use type hints for all parameters and return values
- Provide clear, concise descriptions
- Handle errors gracefully
- Keep functions focused and single-purpose

### Resource Design
- Use descriptive URI patterns
- Implement proper error handling for missing resources
- Consider caching for expensive resource operations

### Error Handling
```python
@mcp.tool()
def robust_tool(param: str) -> str:
    try:
        # Tool implementation
        return result
    except ValueError as e:
        return f"Invalid input: {str(e)}"
    except Exception as e:
        return f"Error processing request: {str(e)}"
```

## Installation and Deployment

### Development
```bash
mcp dev server.py                    # Run in development mode
mcp dev server.py --with dep        # Add dependencies during development
```

### Production
```bash
mcp install server.py               # Install in Claude Desktop
mcp install server.py --name "Name" # Custom server name
mcp install server.py -v KEY=value  # Environment variables
```

## Troubleshooting

### Common Issues
- **Transport errors**: Ensure the correct transport protocol is specified
- **Type errors**: Verify all function parameters have proper type hints
- **Connection issues**: Check that the server is running and accessible
- **Permission errors**: Verify file paths and access permissions

### Debugging
- Use `--log-level DEBUG` for detailed logs
- Enable client-side logging for connection issues
- Check server initialization for missing dependencies