"""
Setup script for MCP development environment
"""

import os
import subprocess
import sys


def install_mcp_sdk():
    """
    Install the MCP SDK with CLI tools
    """
    print("Installing MCP SDK...")

    try:
        # Using pip as fallback, but recommend uv
        result = subprocess.run([sys.executable, "-m", "pip", "install", "mcp[cli]"],
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ MCP SDK installed successfully")
        else:
            print(f"✗ Error installing MCP SDK: {result.stderr}")
    except Exception as e:
        print(f"✗ Error running pip install: {e}")


def create_mcp_project(project_name):
    """
    Create a new MCP project structure
    """
    print(f"Creating MCP project: {project_name}")

    # Create project directory
    os.makedirs(project_name, exist_ok=True)

    # Create server.py
    server_content = '''from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("{}")

@mcp.tool()
def hello(name: str) -> str:
    """A simple greeting tool"""
    return f"Hello, {{}}!".format(name)

if __name__ == "__main__":
    # This will be run with uv when you use `uv run server.py`
    pass
'''.format(project_name)

    with open(os.path.join(project_name, "server.py"), "w") as f:
        f.write(server_content)

    # Create pyproject.toml
    pyproject_content = f'''[project]
name = "{project_name}"
version = "0.1.0"
description = "An MCP server for {project_name}"
dependencies = [
    "mcp[cli]>=1.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
'''

    with open(os.path.join(project_name, "pyproject.toml"), "w") as f:
        f.write(pyproject_content)

    # Create README.md
    readme_content = f'''# {project_name}

An MCP (Model Context Protocol) server for {project_name}.

## Setup

```bash
uv sync
```

## Run

```bash
# Development mode
mcp dev server.py

# Or install in Claude Desktop
mcp install server.py
```

## Usage

This server provides tools for interacting with {project_name}.
'''

    with open(os.path.join(project_name, "README.md"), "w") as f:
        f.write(readme_content)

    print(f"✓ Created project structure in {project_name}/")


def show_setup_instructions():
    """
    Show instructions for setting up MCP development
    """
    instructions = """
MCP Development Setup Instructions
==================================

1. Install uv package manager (recommended):
   ```bash
   pip install uv
   # or with homebrew on macOS: brew install uv
   # or with winget on Windows: winget install astral-sh.uv
   ```

2. Create a new project:
   ```bash
   python setup_mcp_env.py create my-mcp-server
   ```

3. Navigate to your project:
   ```bash
   cd my-mcp-server
   ```

4. Install dependencies:
   ```bash
   uv sync
   ```

5. Run in development mode:
   ```bash
   mcp dev server.py
   ```

6. Or install in Claude Desktop:
   ```bash
   mcp install server.py
   ```

Alternative: Install MCP SDK directly:
```bash
pip install "mcp[cli]"
```

For development with additional dependencies:
```bash
mcp dev server.py --with pandas --with numpy
```

For installation with environment variables:
```bash
mcp install server.py -v API_KEY=your_key
```
"""
    print(instructions)


def main():
    """
    Main function to handle setup commands
    """
    if len(sys.argv) < 2:
        show_setup_instructions()
        return

    command = sys.argv[1]

    if command == "install":
        install_mcp_sdk()
    elif command == "create" and len(sys.argv) > 2:
        create_mcp_project(sys.argv[2])
    elif command == "help":
        show_setup_instructions()
    else:
        print("Usage:")
        print("  python setup_mcp_env.py install    # Install MCP SDK")
        print("  python setup_mcp_env.py create <project_name>  # Create new project")
        print("  python setup_mcp_env.py help       # Show instructions")


if __name__ == "__main__":
    main()