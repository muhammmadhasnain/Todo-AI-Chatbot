from sqlmodel import Session, select
from typing import List, Optional
from ..models.conversation import Conversation, ConversationCreate
from ..models.message import Message, MessageCreate
from ..services.data import data_service
from fastapi import HTTPException


class ConversationService:
    """
    Service class specifically for conversation-related operations.
    This provides a dedicated service for conversation management as specified in the task requirements.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_conversation(self, user_id: str) -> Conversation:
        """
        Create a new conversation for the specified user.
        """
        conversation_create = ConversationCreate(user_id=user_id)
        conversation = data_service.create_conversation(self.db_session, conversation_create)
        return conversation

    def get_conversation_by_id(self, user_id: str, conversation_id: int) -> Conversation:
        """
        Get a specific conversation by its ID for the specified user.
        """
        conversation = data_service.get_conversation_by_id(self.db_session, user_id, conversation_id)
        return conversation

    def get_latest_conversation_for_user(self, user_id: str) -> Optional[Conversation]:
        """
        Get the most recent conversation for a user.
        """
        conversation = data_service.get_latest_conversation_for_user(self.db_session, user_id)
        return conversation

    def create_message(self, user_id: str, conversation_id: int, role: str, content: str) -> Message:
        """
        Create a new message in the specified conversation.
        """
        message_create = MessageCreate(
            user_id=user_id,
            conversation_id=conversation_id,
            role=role,
            content=content
        )
        message = data_service.create_message(self.db_session, message_create, user_id)
        return message

    def get_messages_for_conversation(self, user_id: str, conversation_id: int) -> List[Message]:
        """
        Get all messages for a specific conversation.
        """
        messages = data_service.get_messages_by_conversation(self.db_session, user_id, conversation_id)
        return messages

    def get_user_conversations(self, user_id: str) -> List[Conversation]:
        """
        Get all conversations for a specific user.
        """
        # Currently, we don't have a direct method in data_service for this
        # We'll need to query conversations by user_id
        # For now, this would use the same data_service method used in the API
        statement = select(Conversation).where(Conversation.user_id == user_id)
        conversations = self.db_session.exec(statement).all()
        return conversations