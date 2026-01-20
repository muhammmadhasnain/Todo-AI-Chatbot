# MCP SDK Skill

This skill provides guidance and tools for creating Model Context Protocol (MCP) servers and tools using the Official Python MCP SDK.

## Contents

- `SKILL.md` - Main skill documentation with usage instructions
- `scripts/` - Example Python scripts for MCP development
  - `example_server.py` - Complete example of an MCP server with various tools
  - `example_client.py` - Example client to connect to MCP servers
  - `setup_mcp_env.py` - Setup script for MCP development environment
- `references/` - Detailed reference documentation
  - `mcp_sdk_reference.md` - Complete MCP SDK reference
  - `advanced_patterns.md` - Advanced usage patterns and examples
- `package_skill.py` - Script to package the skill

## Usage

This skill can be used when you need to:
1. Create new MCP servers with tools, resources, or prompts
2. Define MCP tools for LLM integration
3. Create MCP resources for data access
4. Build MCP clients to interact with servers
5. Implement authentication and security for MCP servers
6. Handle complex data types (images, files) in MCP tools

## About MCP

The Model Context Protocol (MCP) enables LLMs to access external tools and resources through a standardized protocol. The Python SDK provides:
- `FastMCP`: High-level server framework for quick development
- `@mcp.tool()`: Decorator to define executable tools
- `@mcp.resource()`: Decorator to define accessible resources
- `@mcp.prompt()`: Decorator to define reusable prompts
- Client libraries for connecting to MCP servers