from sqlmodel import Session
from typing import List
from ..models.task import Task, TaskCreate, TaskUpdate
from ..services.data import data_service
from fastapi import HTTPException


class TaskService:
    """
    Service class specifically for task-related operations.
    This provides a dedicated service for task management as specified in the task requirements.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_task(self, user_id: str, title: str, description: str = None) -> Task:
        """
        Create a new task for the specified user.
        """
        task_create = TaskCreate(
            title=title,
            description=description,
            completed=False
        )

        task = data_service.create_task(self.db_session, task_create, user_id)
        return task

    def get_tasks_for_user(self, user_id: str, status_filter: str = "all") -> List[Task]:
        """
        Get all tasks for a specific user with optional status filter.
        """
        tasks = data_service.get_tasks_by_user(self.db_session, user_id, status_filter)
        return tasks

    def get_task_by_id(self, user_id: str, task_id: int) -> Task:
        """
        Get a specific task by its ID for the specified user.
        """
        task = data_service.get_task_by_id(self.db_session, user_id, task_id)
        return task

    def update_task(self, user_id: str, task_id: int, title: str = None, description: str = None, completed: bool = None) -> Task:
        """
        Update a specific task for the specified user.
        """
        # Prepare update data
        update_data = {}
        if title is not None:
            update_data['title'] = title
        if description is not None:
            update_data['description'] = description
        if completed is not None:
            update_data['completed'] = completed

        task_update = TaskUpdate(**update_data)
        task = data_service.update_task(self.db_session, user_id, task_id, task_update)
        return task

    def delete_task(self, user_id: str, task_id: int) -> bool:
        """
        Delete a specific task for the specified user.
        """
        success = data_service.delete_task(self.db_session, user_id, task_id)
        return success

    def mark_task_completed(self, user_id: str, task_id: int) -> Task:
        """
        Mark a specific task as completed for the specified user.
        """
        task = data_service.mark_task_completed(self.db_session, user_id, task_id)
        return task

    def get_task_statistics(self, user_id: str) -> dict:
        """
        Get statistics about tasks for the specified user.
        """
        total_count = data_service.get_total_tasks_count(self.db_session, user_id)
        completed_count = data_service.get_completed_tasks_count(self.db_session, user_id)
        pending_count = data_service.get_pending_tasks_count(self.db_session, user_id)

        return {
            "total": total_count,
            "completed": completed_count,
            "pending": pending_count
        }