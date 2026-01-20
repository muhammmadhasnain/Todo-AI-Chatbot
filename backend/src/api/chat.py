import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from ..dependencies.auth import get_current_user_with_user_id_check, get_current_user
from ..services.auth import SessionVerificationResponse
from ..middleware.rate_limit import rate_limit_by_user
from ..mcp.tools import MCPSessionContext
from sqlmodel import Session
from ..config import settings
from ..db.session import get_session
from ..todo_agents.agent import TodoAgentService
from ..models.conversation import ConversationCreate
from ..models.message import MessageCreate
from ..services.data import data_service

logger = logging.getLogger(__name__)

router = APIRouter()

# Request models
class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str

# Response models
class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[str] = []

@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    current_user: SessionVerificationResponse = Depends(get_current_user_with_user_id_check),
    db_session: Session = Depends(get_session)
):
    """
    Protected chat endpoint that verifies session via Better Auth API and processes user requests.
    This endpoint requires a valid session and ensures the user_id in the path matches the
    authenticated user.
    """
    # Verify that the current user matches the user_id in the path
    # This is handled by the get_current_user_with_user_id_check dependency

    # Apply rate limiting based on authenticated user_id
    await rate_limit_by_user(current_user.user_id)

    # Initialize Agent service with the new OpenAI Agent SDK, passing the authenticated user_id
    agent_service = TodoAgentService(db_session, user_id)

    # Get or create conversation
    conversation = None
    if request.conversation_id:
        # Try to get existing conversation
        try:
            conversation = data_service.get_conversation_by_id(db_session, user_id, request.conversation_id)
        except HTTPException:
            # If conversation doesn't exist, create a new one
            conversation_create = ConversationCreate(user_id=user_id)
            conversation = data_service.create_conversation(db_session, conversation_create, user_id)
    else:
        # Create a new conversation
        conversation_create = ConversationCreate(user_id=user_id)
        conversation = data_service.create_conversation(db_session, conversation_create, user_id)

    # Create user message in database
    message_create = MessageCreate(
        user_id=user_id,
        conversation_id=conversation.id,
        role="user",
        content=request.message
    )
    user_message = data_service.create_message(db_session, message_create, user_id)

    # Process the request with the new OpenAI Agent SDK
    try:
        agent_response = await agent_service.process_request(
            message=request.message,
            conversation_id=conversation.id,
            db_session=db_session  # Pass the database session for history loading
        )
    except Exception as e:
        # Log the error for debugging
        logger.error(f"Error processing agent request: {str(e)}")
        # Return a user-friendly error response
        raise HTTPException(
            status_code=500,
            detail="Sorry, I encountered an error processing your request. Please try again."
        )

    # Create assistant message in database
    assistant_message_create = MessageCreate(
        user_id=user_id,
        conversation_id=conversation.id,
        role="assistant",
        content=agent_response.response
    )
    assistant_message = data_service.create_message(db_session, assistant_message_create, user_id)

    response = ChatResponse(
        conversation_id=conversation.id,
        response=agent_response.response,
    
    )

    return response

# Additional chat-related endpoints can be added here
@router.get("/{user_id}/conversations")
async def get_user_conversations(
    user_id: str,
    current_user: SessionVerificationResponse = Depends(get_current_user_with_user_id_check),
    db_session: Session = Depends(get_session)
):
    """
    Get user's conversations (requires authentication and user_id validation)
    """
    from sqlmodel import select
    from ..models.conversation import Conversation

    statement = select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())
    conversations = db_session.exec(statement).all()

    return {
        "conversations": [
            {
                "id": conv.id,
                "user_id": conv.user_id,
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat()
            }
            for conv in conversations
        ]
    }

@router.get("/{user_id}/conversation/{conversation_id}")
async def get_conversation(
    user_id: str,
    conversation_id: int,
    current_user: SessionVerificationResponse = Depends(get_current_user_with_user_id_check),
    db_session: Session = Depends(get_session)
):
    """
    Get a specific conversation with its messages (requires authentication and user_id validation)
    """
    # Get the conversation
    conversation = data_service.get_conversation_by_id(db_session, user_id, conversation_id)

    # Get all messages for this conversation
    messages = data_service.get_messages_by_conversation(db_session, user_id, conversation_id)

    # Convert backend Message objects to frontend format
    formatted_messages = []
    for msg in messages:
        formatted_messages.append({
            "id": str(msg.id),
            "content": msg.content,
            "role": msg.role,
            "timestamp": msg.created_at.isoformat(),
            "status": "sent"  # Default status for historical messages
        })

    return {
        "conversation_id": conversation.id,
        "messages": formatted_messages
    }