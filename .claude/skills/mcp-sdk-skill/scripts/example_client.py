"""
Example MCP Client for connecting to MCP servers
"""

import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.client.streamable_http import streamablehttp_client
from mcp.types import AnyUrl


async def connect_via_stdio():
    """
    Connect to an MCP server via stdio transport
    """
    print("Connecting via stdio transport...")

    server_params = StdioServerParameters(
        command="python",
        args=["example_server.py"],  # Replace with actual server path
        env={}  # Add environment variables if needed
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize connection
                result = await session.initialize()
                print(f"Connected to: {result.server_info.name if result.server_info else 'Unknown Server'}")

                # List available tools
                tools = await session.list_tools()
                print(f"Available tools: {len(tools.tools) if tools.tools else 0}")
                for tool in tools.tools if tools.tools else []:
                    print(f"  - {tool.name}: {tool.description}")

                # Example: Call the 'add' tool if it exists
                if tools.tools and any(t.name == "add" for t in tools.tools):
                    tool_result = await session.call_tool(
                        "add",
                        arguments={"a": 5, "b": 3}
                    )
                    print(f"Add result: {tool_result}")

                # List resources
                resources = await session.list_resources()
                print(f"Available resources: {len(resources.resources) if resources.resources else 0}")
                for resource in resources.resources if resources.resources else []:
                    print(f"  - {resource.uri}: {resource.name}")

    except Exception as e:
        print(f"Error connecting via stdio: {e}")


async def connect_via_streamable_http():
    """
    Connect to an MCP server via streamable HTTP transport
    """
    print("Connecting via streamable HTTP transport...")

    try:
        async with streamablehttp_client("http://localhost:3000/mcp") as (
            read, write, _
        ):
            async with ClientSession(read, write) as session:
                # Initialize connection
                result = await session.initialize()
                print(f"Connected to: {result.server_info.name if result.server_info else 'Unknown Server'}")

                # Call a tool
                tool_result = await session.call_tool(
                    "echo_tool",  # Replace with actual tool name
                    arguments={"message": "hello from client"}
                )
                print(f"Tool result: {tool_result}")

    except Exception as e:
        print(f"Error connecting via HTTP: {e}")


async def read_resource_example():
    """
    Example of reading a resource from an MCP server
    """
    print("Reading a resource...")

    server_params = StdioServerParameters(
        command="python",
        args=["example_server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Read a specific resource
            try:
                content = await session.read_resource(AnyUrl("greeting://World"))
                print(f"Resource content: {content}")
            except Exception as e:
                print(f"Error reading resource: {e}")


async def main():
    """
    Main function to demonstrate different client connection methods
    """
    print("MCP Client Examples")
    print("=" * 30)

    # Uncomment the connection method you want to try
    # await connect_via_stdio()
    # await connect_via_streamable_http()
    # await read_resource_example()

    print("\nNote: To run these examples, you need an active MCP server.")
    print("Start a server first with: uv run example_server.py")


if __name__ == "__main__":
    asyncio.run(main())