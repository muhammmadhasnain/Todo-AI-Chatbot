from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class ConversationBase(SQLModel):
    """Base model for Conversation with common fields"""
    user_id: str = Field(nullable=False, description="User ID who owns this conversation")


class Conversation(ConversationBase, table=True):
    """
    Conversation model representing a chat session in the system.
    This follows the exact specifications from the constitution:
    - user_id: User ID who owns this conversation
    - id: Primary key
    - created_at: Timestamp when conversation was created
    - updated_at: Timestamp when conversation was last updated
    """
    __tablename__ = "conversations"

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when conversation was created")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when conversation was last updated")


class ConversationCreate(ConversationBase):
    """Model for creating a new conversation"""
    pass


class ConversationRead(ConversationBase):
    """Model for reading conversation data"""
    id: int
    created_at: datetime
    updated_at: datetime


class ConversationUpdate(SQLModel):
    """Model for updating conversation information"""
    pass