from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class TaskBase(SQLModel):
    """Base model for Task with common fields"""
    user_id: str = Field(nullable=False, description="User ID who owns this task")
    title: str = Field(nullable=False, description="Task title")
    description: Optional[str] = Field(default=None, description="Task description")
    completed: bool = Field(default=False, description="Whether task is completed")


class Task(TaskBase, table=True):
    """
    Task model representing a todo item in the system.
    This follows the exact specifications from the constitution:
    - user_id: User ID who owns this task
    - id: Primary key
    - title: Task title
    - description: Task description
    - completed: Whether task is completed
    - created_at: Timestamp when task was created
    - updated_at: Timestamp when task was last updated
    """
    __tablename__ = "tasks"

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when task was created")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when task was last updated")


class TaskCreate(TaskBase):
    """Model for creating a new task"""
    pass


class TaskRead(TaskBase):
    """Model for reading task data"""
    id: int
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    """Model for updating task information"""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None