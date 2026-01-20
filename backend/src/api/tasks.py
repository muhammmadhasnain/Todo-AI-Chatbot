from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ..dependencies.auth import get_current_user_with_user_id_check
from ..services.auth import SessionVerificationResponse
from sqlmodel import Session
from ..db.session import get_session
from ..models.task import Task, TaskCreate, TaskUpdate
from ..services.data import data_service

router = APIRouter()

# Request and Response models
class TaskCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: str
    updated_at: str

class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]

@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
async def get_user_tasks(
    user_id: str,
    status: str = "all",  # Query parameter for status filter
    current_user: SessionVerificationResponse = Depends(get_current_user_with_user_id_check),
    db_session: Session = Depends(get_session)
):
    """
    Get user's tasks (requires authenticated session and user_id validation).
    This endpoint ensures users can only access their own tasks.
    """
    # Get tasks using the data service with status filter
    tasks = data_service.get_tasks_by_user(db_session, user_id, status_filter=status)

    # Convert to response format
    task_responses = []
    for task in tasks:
        task_response = TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at.isoformat(),
            updated_at=task.updated_at.isoformat()
        )
        task_responses.append(task_response)

    return task_responses

@router.post("/{user_id}/tasks", response_model=TaskResponse)
async def create_task(
    user_id: str,
    task_request: TaskCreateRequest,
    current_user: SessionVerificationResponse = Depends(get_current_user_with_user_id_check),
    db_session: Session = Depends(get_session)
):
    """
    Create a new task (requires authenticated session and user_id validation).
    This endpoint ensures users can only create tasks for themselves.
    """
    # Validate that the user_id in the path matches the authenticated user
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized: Cannot create tasks for another user"
        )

    # Create task using the data service
    task_create = TaskCreate(
        user_id=user_id,
        title=task_request.title,
        description=task_request.description,
        completed=False
    )

    new_task = data_service.create_task(db_session, task_create, user_id)

    return TaskResponse(
        id=new_task.id,
        user_id=new_task.user_id,
        title=new_task.title,
        description=new_task.description,
        completed=new_task.completed,
        created_at=new_task.created_at.isoformat(),
        updated_at=new_task.updated_at.isoformat()
    )

@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: int,
    current_user: SessionVerificationResponse = Depends(get_current_user_with_user_id_check),
    db_session: Session = Depends(get_session)
):
    """
    Get a specific task (requires authenticated session and user_id validation).
    This endpoint ensures users can only access their own tasks.
    """
    # Get task using the data service
    task = data_service.get_task_by_id(db_session, user_id, task_id)

    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at.isoformat(),
        updated_at=task.updated_at.isoformat()
    )

@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: int,
    task_request: TaskUpdateRequest,
    current_user: SessionVerificationResponse = Depends(get_current_user_with_user_id_check),
    db_session: Session = Depends(get_session)
):
    """
    Update a task (requires authenticated session and user_id validation).
    This endpoint ensures users can only update their own tasks.
    """
    # Prepare update data
    update_data = {}
    if task_request.title is not None:
        update_data['title'] = task_request.title
    if task_request.description is not None:
        update_data['description'] = task_request.description
    if task_request.completed is not None:
        update_data['completed'] = task_request.completed

    task_update = TaskUpdate(**update_data)

    # Update task using the data service
    updated_task = data_service.update_task(db_session, user_id, task_id, task_update)

    return TaskResponse(
        id=updated_task.id,
        user_id=updated_task.user_id,
        title=updated_task.title,
        description=updated_task.description,
        completed=updated_task.completed,
        created_at=updated_task.created_at.isoformat(),
        updated_at=updated_task.updated_at.isoformat()
    )

@router.delete("/{user_id}/tasks/{task_id}")
async def delete_task(
    user_id: str,
    task_id: int,
    current_user: SessionVerificationResponse = Depends(get_current_user_with_user_id_check),
    db_session: Session = Depends(get_session)
):
    """
    Delete a task (requires authenticated session and user_id validation).
    This endpoint ensures users can only delete their own tasks.
    """
    # Delete task using the data service
    success = data_service.delete_task(db_session, user_id, task_id)

    if not success:
        raise HTTPException(
            status_code=500,
            detail="Failed to delete task"
        )

    return {"message": f"Task {task_id} deleted successfully"}