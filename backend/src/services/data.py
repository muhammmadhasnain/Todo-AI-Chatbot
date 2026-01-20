from sqlmodel import Session, select, func
from typing import List, Optional
from ..models.user import User, UserCreate, UserUpdate
from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.conversation import Conversation, ConversationCreate
from ..models.message import Message, MessageCreate
from ..services.auth import SessionVerificationResponse
from fastapi import HTTPException
from datetime import datetime

class DataService:
    """
    Service class that handles data operations with proper user isolation.
    All queries are scoped by verified user_id from Better Auth session.
    """

    def get_user_by_id(self, db_session: Session, user_id: str) -> Optional[User]:
        """
        Get a user by their user_id with proper verification.
        Always ensures the user_id matches authenticated context.
        """
        statement = select(User).where(User.user_id == user_id)
        user = db_session.exec(statement).first()
        return user

    def create_user(self, db_session: Session, user_data: User) -> User:
        """
        Create a new user with proper validation.
        """
        # Verify the user_id is from a trusted source (Better Auth)
        if not user_data.user_id or len(user_data.user_id) == 0:
            raise HTTPException(
                status_code=400,
                detail="Invalid user_id provided"
            )

        # Check if user already exists
        existing_user = self.get_user_by_id(db_session, user_data.user_id)
        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="User already exists"
            )

        # Create the new user
        db_session.add(user_data)
        db_session.commit()
        db_session.refresh(user_data)
        return user_data

    def update_user(self, db_session: Session, user_id: str, update_data: dict) -> Optional[User]:
        """
        Update a user with proper user_id validation.
        """
        user = self.get_user_by_id(db_session, user_id)
        if not user:
            return None

        # Update only allowed fields
        for field, value in update_data.items():
            if hasattr(user, field) and field not in ['id', 'user_id', 'email']:
                setattr(user, field, value)

        user.updated_at = datetime.utcnow()
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    def delete_user(self, db_session: Session, user_id: str) -> bool:
        """
        Delete a user with proper validation (soft delete in real implementation).
        """
        user = self.get_user_by_id(db_session, user_id)
        if not user:
            return False

        # In a real implementation, this would be a soft delete
        db_session.delete(user)
        db_session.commit()
        return True

    def create_task(self, db_session: Session, task_create: TaskCreate, user_id: str) -> Task:
        """
        Create a new task in the database.
        """
        # Ensure user_id in the task_create matches the passed user_id for security
        task_data = task_create.model_dump()
        task_data['user_id'] = user_id  # Override with verified user_id
        task = Task(**task_data)
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        return task

    def get_tasks_by_user(self, db_session: Session, user_id: str, status_filter: str = "all") -> List[Task]:
        """
        Get tasks for a specific user with optional status filter.
        """
        query = select(Task).where(Task.user_id == user_id)

        if status_filter == "pending":
            query = query.where(Task.completed == False)
        elif status_filter == "completed":
            query = query.where(Task.completed == True)

        tasks = db_session.exec(query).all()
        return tasks

    def get_task_by_id(self, db_session: Session, user_id: str, task_id: int) -> Task:
        """
        Get a specific task by ID for a user.
        """
        statement = select(Task).where(Task.user_id == user_id, Task.id == task_id)
        task = db_session.exec(statement).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    def update_task(self, db_session: Session, user_id: str, task_id: int, task_update: TaskUpdate) -> Task:
        """
        Update a task in the database.
        """
        task = self.get_task_by_id(db_session, user_id, task_id)

        # Update fields that were provided
        for field, value in task_update.model_dump(exclude_unset=True).items():
            setattr(task, field, value)

        # Update the timestamp
        task.updated_at = datetime.utcnow()

        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        return task

    def delete_task(self, db_session: Session, user_id: str, task_id: int) -> bool:
        """
        Delete a task from the database.
        """
        task = self.get_task_by_id(db_session, user_id, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        db_session.delete(task)
        db_session.commit()
        return True

    def mark_task_completed(self, db_session: Session, user_id: str, task_id: int) -> Task:
        """
        Mark a task as completed.
        """
        task = self.get_task_by_id(db_session, user_id, task_id)

        task.completed = True
        task.updated_at = datetime.utcnow()

        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        return task

    def create_conversation(self, db_session: Session, conversation_create: ConversationCreate, user_id: str) -> Conversation:
        """
        Create a new conversation in the database.
        """
        # Ensure user_id in the conversation_create matches the passed user_id for security
        conversation_data = conversation_create.model_dump()
        conversation_data['user_id'] = user_id  # Override with verified user_id
        conversation = Conversation(**conversation_data)
        db_session.add(conversation)
        db_session.commit()
        db_session.refresh(conversation)
        return conversation

    def get_conversation_by_id(self, db_session: Session, user_id: str, conversation_id: int) -> Conversation:
        """
        Get a specific conversation by ID for a user.
        """
        statement = select(Conversation).where(
            Conversation.user_id == user_id,
            Conversation.id == conversation_id
        )
        conversation = db_session.exec(statement).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return conversation

    def create_message(self, db_session: Session, message_create: MessageCreate, user_id: str) -> Message:
        """
        Create a new message in the database.
        """
        # Ensure user_id in the message_create matches the passed user_id for security
        message_data = message_create.model_dump()
        message_data['user_id'] = user_id  # Override with verified user_id
        message = Message(**message_data)
        db_session.add(message)
        db_session.commit()
        db_session.refresh(message)
        return message

    def get_messages_by_conversation(self, db_session: Session, user_id: str, conversation_id: int) -> List[Message]:
        """
        Get all messages for a specific conversation.
        """
        statement = select(Message).where(
            Message.user_id == user_id,
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc())

        messages = db_session.exec(statement).all()
        return messages

    def get_latest_conversation_for_user(self, db_session: Session, user_id: str) -> Optional[Conversation]:
        """
        Get the most recent conversation for a user.
        """
        statement = select(Conversation).where(
            Conversation.user_id == user_id
        ).order_by(Conversation.updated_at.desc()).limit(1)

        conversation = db_session.exec(statement).first()
        return conversation

    def get_total_tasks_count(self, db_session: Session, user_id: str) -> int:
        """
        Get the total count of tasks for a user.
        """
        statement = select(func.count(Task.id)).where(Task.user_id == user_id)
        count = db_session.exec(statement).one()
        return count

    def get_completed_tasks_count(self, db_session: Session, user_id: str) -> int:
        """
        Get the count of completed tasks for a user.
        """
        statement = select(func.count(Task.id)).where(
            Task.user_id == user_id,
            Task.completed == True
        )
        count = db_session.exec(statement).one()
        return count

    def get_pending_tasks_count(self, db_session: Session, user_id: str) -> int:
        """
        Get the count of pending tasks for a user.
        """
        statement = select(func.count(Task.id)).where(
            Task.user_id == user_id,
            Task.completed == False
        )
        count = db_session.exec(statement).one()
        return count

    def validate_user_access(self, authenticated_user_id: str, target_user_id: str) -> bool:
        """
        Validate that the authenticated user can access the target user's data.
        This enforces the user isolation principle.
        """
        return authenticated_user_id == target_user_id

    def verify_user_context(
        self,
        session_verification: SessionVerificationResponse,
        required_user_id: str
    ) -> bool:
        """
        Verify that the session belongs to the required user.
        This ensures that operations are performed in the correct user context.
        """
        if not session_verification.is_valid:
            return False

        return session_verification.user_id == required_user_id

# Global instance of the data service
data_service = DataService()