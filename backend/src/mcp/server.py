"""
MCP Server for the Todo AI Chatbot Backend
Implements MCP-first architecture with the 5 required tools
"""

from mcp.server.fastmcp import FastMCP
from typing import Dict, Any, List
from ..services.auth import SessionVerificationResponse
from ..services.data import data_service
from ..db.session import get_session
from .tools import create_authenticated_mcp_tools, MCPSessionContext
from sqlmodel import Session
from fastapi import HTTPException
import os


class TodoMCPServer:
    """
    MCP Server implementation for the Todo AI Chatbot Backend
    Registers all 5 required tools as specified in the constitution:
    - add_task
    - list_tasks
    - complete_task
    - delete_task
    - update_task
    """

    def __init__(self):
        self.mcp = FastMCP("todo-ai-chatbot-mcp")
        # Register tools using decorators
        self.tools = {}  # Keep track of tools for the startup event
        self._register_mcp_tools()

    def _register_mcp_tools(self):
        """Register all 5 required MCP tools with proper contracts."""

        @self.mcp.tool(
            description="Create new task; Requires user_id (string), title (string), optional description; Returns task_id, status, title"
        )
        async def add_task(user_id: str, title: str, description: str = None) -> Dict[str, Any]:
            """Add a new task for the authenticated user."""
            # This is a placeholder - in a real implementation, we would need to get the session context
            # For now, we'll create a mock implementation
            # In a real implementation, this would need access to the authenticated session
            return {
                "task_id": 1,
                "status": "created",
                "title": title
            }

        @self.mcp.tool(
            description="Retrieve tasks; Requires user_id (string), optional status filter ('all', 'pending', 'completed'); Returns array of task objects"
        )
        async def list_tasks(user_id: str, status: str = "all") -> List[Dict[str, Any]]:
            """List tasks for the authenticated user."""
            # Placeholder implementation
            return [
                {
                    "id": 1,
                    "user_id": user_id,
                    "title": "Sample task",
                    "description": "Sample description",
                    "completed": False,
                    "created_at": "2023-01-01T00:00:00",
                    "updated_at": "2023-01-01T00:00:00"
                }
            ]

        @self.mcp.tool(
            description="Mark task as complete; Requires user_id (string), task_id (integer); Returns task_id, status, title"
        )
        async def complete_task(user_id: str, task_id: int) -> Dict[str, Any]:
            """Mark a task as complete for the authenticated user."""
            # Placeholder implementation
            return {
                "task_id": task_id,
                "status": "completed",
                "title": f"Task {task_id}"
            }

        @self.mcp.tool(
            description="Remove task; Requires user_id (string), task_id (integer); Returns task_id, status, title"
        )
        async def delete_task(user_id: str, task_id: int) -> Dict[str, Any]:
            """Delete a task for the authenticated user."""
            # Placeholder implementation
            return {
                "task_id": task_id,
                "status": "deleted",
                "title": f"Task {task_id}"
            }

        @self.mcp.tool(
            description="Modify task; Requires user_id (string), task_id (integer), optional title/description; Returns task_id, status, title"
        )
        async def update_task(user_id: str, task_id: int, title: str = None, description: str = None) -> Dict[str, Any]:
            """Update a task for the authenticated user."""
            # Placeholder implementation
            return {
                "task_id": task_id,
                "status": "updated",
                "title": title or f"Task {task_id}"
            }

    def get_mcp_tools_instance(self, user_session: SessionVerificationResponse, db_session: Session):
        """Get an instance of MCP tools with authenticated user context."""
        return create_authenticated_mcp_tools(user_session, db_session)

    async def run_server(self):
        """Run the MCP server."""
        await self.mcp.run_stdio_async()


# Global MCP server instance
mcp_server = TodoMCPServer()