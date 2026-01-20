# MCP SDK Advanced Patterns

## Multi-Server Applications

For applications requiring multiple MCP servers, you can mount them in a single FastAPI application:

```python
import contextlib
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp import Context


# Define separate servers
echo_mcp = FastMCP(name="EchoServer", stateless_http=True)
math_mcp = FastMCP(name="MathServer", stateless_http=True)


@echo_mcp.tool(description="Echo a message")
def echo(message: str) -> str:
    return f"Echo: {message}"


@math_mcp.tool(description="Add two numbers")
def add(n1: int, n2: int) -> int:
    return n1 + n2


@math_mcp.tool(description="Calculate factorial")
def factorial(n: int) -> int:
    if n <= 1:
        return 1
    return n * factorial(n - 1)


# Create combined lifespan
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(echo_mcp.session_manager.run())
        await stack.enter_async_context(math_mcp.session_manager.run())
        yield


# Create FastAPI app and mount servers
app = FastAPI(lifespan=lifespan)
app.mount("/echo", echo_mcp.streamable_http_app())
app.mount("/math", math_mcp.streamable_http_app())
```

## Authentication and Authorization

Implement authentication for your MCP servers:

```python
from mcp.server.fastmcp import FastMCP
from typing import Optional
import os


mcp = FastMCP("Secure Server")


def verify_auth(token: Optional[str]) -> bool:
    """Verify authentication token"""
    expected_token = os.getenv("MCP_AUTH_TOKEN")
    return token == expected_token


@mcp.tool(description="Secure API call")
def secure_api_call(auth_token: str, data: str) -> str:
    """API call that requires authentication"""
    if not verify_auth(auth_token):
        raise ValueError("Invalid authentication token")

    # Process authenticated request
    return f"Processed secure data: {data}"
```

## Database Integration

Example of integrating with SQLite:

```python
import sqlite3
from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any


mcp = FastMCP("Database Explorer")


def get_db_connection():
    """Get database connection"""
    return sqlite3.connect("example.db")


@mcp.resource("db-schema://main")
def get_schema() -> str:
    """Get database schema"""
    conn = get_db_connection()
    try:
        schema = conn.execute("""
            SELECT name, sql
            FROM sqlite_master
            WHERE type='table'
        """).fetchall()
        return "\n".join(f"{name}: {sql}" for name, sql in schema)
    finally:
        conn.close()


@mcp.tool(description="Execute a SELECT query")
def execute_select_query(query: str) -> List[Dict[str, Any]]:
    """Execute a SELECT query safely"""
    if not query.strip().upper().startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed")

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query)

        # Get column names
        columns = [description[0] for description in cursor.description]

        # Get results
        rows = cursor.fetchall()

        # Convert to list of dictionaries
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        conn.close()
```

## File System Operations

Safe file system operations with MCP:

```python
from mcp.server.fastmcp import FastMCP, Context
import os
from pathlib import Path
from typing import List


mcp = FastMCP("File System")


def safe_path_join(base_path: str, relative_path: str) -> str:
    """Safely join paths to prevent directory traversal"""
    base = Path(base_path).resolve()
    target = (base / relative_path).resolve()

    if not target.is_relative_to(base):
        raise ValueError("Path traversal detected")

    return str(target)


@mcp.tool(description="List files in a directory")
def list_files(directory: str, ctx: Context) -> List[str]:
    """List files in a directory safely"""
    safe_dir = safe_path_join("./safe_dir", directory)

    if not os.path.exists(safe_dir):
        return []

    if not os.path.isdir(safe_dir):
        return [os.path.basename(safe_dir)]

    files = []
    for item in os.listdir(safe_dir):
        item_path = os.path.join(safe_dir, item)
        if os.path.isfile(item_path):
            files.append(item)

    return files


@mcp.tool(description="Read a file")
def read_file(filename: str, ctx: Context) -> str:
    """Read a file safely"""
    safe_path = safe_path_join("./safe_dir", filename)

    if not os.path.exists(safe_path):
        raise FileNotFoundError(f"File does not exist: {filename}")

    if not os.path.isfile(safe_path):
        raise ValueError(f"Path is not a file: {filename}")

    with open(safe_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if len(content) > 10000:  # Limit file size
            return content[:10000] + "\n... (truncated)"
        return content
```

## Async Operations with Progress Tracking

Long-running operations with progress reporting:

```python
from mcp.server.fastmcp import FastMCP, Context
import asyncio
from typing import List


mcp = FastMCP("Async Operations")


@mcp.tool(description="Process multiple files with progress tracking")
async def process_files_async(filenames: List[str], ctx: Context) -> str:
    """Process multiple files with progress tracking"""
    results = []

    for i, filename in enumerate(filenames):
        # Report progress
        progress_percentage = int((i / len(filenames)) * 100)
        await ctx.report_progress(i, len(filenames))
        ctx.info(f"Processing file {i+1} of {len(filenames)}: {filename}")

        # Simulate async processing
        await asyncio.sleep(0.1)  # Simulate work

        # Process the file (in a real implementation)
        result = f"Processed: {filename}"
        results.append(result)

    return f"Successfully processed {len(filenames)} files"
```

## Custom Content Types

Working with custom content types:

```python
from mcp.server.fastmcp import FastMCP, Image
from PIL import Image as PILImage
import base64
from typing import Union


mcp = FastMCP("Content Processor")


@mcp.tool(description="Convert image to different format")
def convert_image_format(image_path: str, target_format: str) -> Image:
    """Convert an image to a different format"""
    try:
        img = PILImage.open(image_path)

        # Convert based on target format
        if target_format.upper() == "JPEG":
            if img.mode in ("RGBA", "LA", "P"):
                img = img.convert("RGB")
            target_format = "jpeg"
        elif target_format.upper() == "PNG":
            target_format = "png"
        elif target_format.upper() == "WEBP":
            target_format = "webp"
        else:
            raise ValueError(f"Unsupported format: {target_format}")

        # Return as MCP Image object
        return Image(data=img.tobytes(), format=target_format)
    except Exception as e:
        raise ValueError(f"Could not convert image: {str(e)}")


@mcp.tool(description="Generate data visualization")
def generate_chart(data: dict, chart_type: str = "bar") -> Image:
    """Generate a simple chart as an image"""
    # In a real implementation, you would use matplotlib, plotly, etc.
    # This is a placeholder for the concept

    # Create a simple placeholder image
    img = PILImage.new('RGB', (200, 100), color='white')

    return Image(data=img.tobytes(), format="png")
```

## Error Handling and Validation

Comprehensive error handling:

```python
from mcp.server.fastmcp import FastMCP
from typing import Union
import re


mcp = FastMCP("Validated Operations")


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


@mcp.tool(description="Process user data with validation")
def process_user_data(name: str, email: str, age: int) -> str:
    """Process user data with validation"""
    errors = []

    if not name or len(name.strip()) < 2:
        errors.append("Name must be at least 2 characters")

    if not validate_email(email):
        errors.append("Invalid email format")

    if age < 0 or age > 150:
        errors.append("Age must be between 0 and 150")

    if errors:
        raise ValueError("Validation errors: " + "; ".join(errors))

    return f"User processed: {name} ({email}), age {age}"
```

## Configuration and Settings

Managing server configuration:

```python
from mcp.server.fastmcp import FastMCP
import os


# Create server with configuration
mcp = FastMCP("Configurable Server")

# Server settings can be configured via environment variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.example.com")
TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))


@mcp.tool(description="API call with configurable settings")
def api_call(endpoint: str, data: str) -> str:
    """Make an API call using configured settings"""
    # In a real implementation, this would make an actual API call
    # using the configured base URL and timeout

    full_url = f"{API_BASE_URL}/{endpoint}"
    return f"Would call API: {full_url} with data: {data[:50]}... (configurable timeout: {TIMEOUT}s)"
```