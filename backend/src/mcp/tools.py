from typing import Dict, Any, List
from ..services.auth import SessionVerificationResponse
from ..services.data import data_service
from sqlmodel import Session
from ..models.user import User
from ..models.task import Task, TaskCreate, TaskUpdate
from fastapi import HTTPException
import json

class MCPSessionContext:
    """
    Context class that holds the authenticated user information for MCP tool calls.
    This ensures that all MCP tools operate within the verified user context.
    """

    def __init__(self, user_session: SessionVerificationResponse, db_session: Session):
        self.user_session = user_session
        self.db_session = db_session

    def validate_user_access(self, target_user_id: str) -> bool:
        """
        Validate that the authenticated user can access resources for target_user_id.
        """
        return self.user_session.user_id == target_user_id

    def get_user_data(self) -> Dict[str, Any]:
        """
        Get the authenticated user's data based on their session.
        """
        user = data_service.get_user_by_id(self.db_session, self.user_session.user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return {
            "user_id": user.user_id,
            "email": user.email,
            "name": user.name,
            "email_verified": user.email_verified
        }


class MCPTools:
    """
    MCP tools that operate within the authenticated user context.
    Each tool validates that operations are performed by the correct user.
    Additionally, these tools are designed to be called only by the AI agent.
    """

    def __init__(self, session_context: MCPSessionContext):
        self.session_context = session_context

    async def add_task(self, user_id: str, title: str, description: str = None) -> Dict[str, Any]:
        """
        Add a new task for the authenticated user.
        Implements the constitution-specified contract:
        - Requires: user_id (string), title (string), optional description
        - Returns: task_id, status, title
        """
        # Validate that the operation is performed by the correct user
        if not self.session_context.validate_user_access(user_id):
            raise HTTPException(
                status_code=403,
                detail="Unauthorized: Cannot add task for another user"
            )

        # Create the task using the data service
        task_create = TaskCreate(
            user_id=user_id,  # Pass user_id to the model
            title=title,
            description=description,
            completed=False
        )

        task = data_service.create_task(self.session_context.db_session, task_create, user_id)

        return {
            "task_id": task.id,
            "status": "created",
            "title": task.title
        }

    async def list_tasks(self, user_id: str, status: str) -> List[Dict[str, Any]]:
        """
        List tasks for the authenticated user.
        Implements the constitution-specified contract:
        - Requires: user_id (string), optional status filter ("all", "pending", "completed")
        - Returns: array of task objects
        """
        # Validate that the operation is performed by the correct user
        if not self.session_context.validate_user_access(user_id):
            raise HTTPException(
                status_code=403,
                detail="Unauthorized: Cannot list tasks for another user"
            )

        # Get tasks using the data service with status filter
        tasks = data_service.get_tasks_by_user(self.session_context.db_session, user_id, status_filter=status)

        # Convert to dictionary format
        task_list = []
        for task in tasks:
            task_dict = {
                "id": task.id,
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
            task_list.append(task_dict)

        return task_list

    async def complete_task(self, user_id: str, task_id: int) -> Dict[str, Any]:
        """
        Mark a task as complete for the authenticated user.
        Implements the constitution-specified contract:
        - Requires: user_id (string), task_id (integer)
        - Returns: task_id, status, title
        """
        # Validate that the operation is performed by the correct user
        if not self.session_context.validate_user_access(user_id):
            raise HTTPException(
                status_code=403,
                detail="Unauthorized: Cannot complete task for another user"
            )

        # Mark task as completed using the data service
        task = data_service.mark_task_completed(self.session_context.db_session, user_id, task_id)

        return {
            "task_id": task.id,
            "status": "completed",
            "title": task.title
        }

    async def delete_task(self, user_id: str, task_id: int) -> Dict[str, Any]:
        """
        Delete a task for the authenticated user.
        Implements the constitution-specified contract:
        - Requires: user_id (string), task_id (integer)
        - Returns: task_id, status, title
        """
        # Validate that the operation is performed by the correct user
        if not self.session_context.validate_user_access(user_id):
            raise HTTPException(
                status_code=403,
                detail="Unauthorized: Cannot delete task for another user"
            )

        # Get the task before deletion to return its details
        task = data_service.get_task_by_id(self.session_context.db_session, user_id, task_id)

        # Delete the task using the data service
        success = data_service.delete_task(self.session_context.db_session, user_id, task_id)

        if not success:
            raise HTTPException(
                status_code=500,
                detail="Failed to delete task"
            )

        return {
            "task_id": task.id,
            "status": "deleted",
            "title": task.title
        }

    async def update_task(self, user_id: str, task_id: int, title: str = None, description: str = None) -> Dict[str, Any]:
        """
        Update a task for the authenticated user.
        Implements the constitution-specified contract:
        - Requires: user_id (string), task_id (integer), optional title/description
        - Returns: task_id, status, title
        """
        # Validate that the operation is performed by the correct user
        if not self.session_context.validate_user_access(user_id):
            raise HTTPException(
                status_code=403,
                detail="Unauthorized: Cannot update task for another user"
            )

        # Create update object with provided fields
        task_update_data = {}
        if title is not None:
            task_update_data['title'] = title
        if description is not None:
            task_update_data['description'] = description

        task_update = TaskUpdate(**task_update_data)

        # Update the task using the data service
        task = data_service.update_task(self.session_context.db_session, user_id, task_id, task_update)

        return {
            "task_id": task.id,
            "status": "updated",
            "title": task.title
        }

# Global function to create MCP tools with authenticated user context
def create_authenticated_mcp_tools(user_session: SessionVerificationResponse, db_session: Session) -> MCPTools:
    """
    Create MCP tools instance with authenticated user context.
    This ensures all MCP tool operations are properly scoped by user_id from verified sessions.
    """
    session_context = MCPSessionContext(user_session, db_session)
    return MCPTools(session_context)