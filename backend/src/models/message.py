from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class MessageBase(SQLModel):
    """Base model for Message with common fields"""
    user_id: str = Field(nullable=False, description="User ID who sent this message")
    conversation_id: int = Field(nullable=False, description="Conversation ID this message belongs to")
    role: str = Field(nullable=False, description="Role of the message sender (user/assistant)")
    content: str = Field(nullable=False, description="Message content")


class Message(MessageBase, table=True):
    """
    Message model representing an individual message in a conversation.
    This follows the exact specifications from the constitution:
    - user_id: User ID who sent this message
    - id: Primary key
    - conversation_id: Conversation ID this message belongs to
    - role: Role of the message sender (user/assistant)
    - content: Message content
    - created_at: Timestamp when message was created
    """
    __tablename__ = "messages"

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when message was created")


class MessageCreate(MessageBase):
    """Model for creating a new message"""
    pass


class MessageRead(MessageBase):
    """Model for reading message data"""
    id: int
    created_at: datetime


class MessageUpdate(SQLModel):
    """Model for updating message information"""
    content: Optional[str] = None