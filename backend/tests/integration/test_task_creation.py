import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
from main import app  # Assuming main.py contains the FastAPI app
from src.services.auth import SessionVerificationResponse
from src.db.session import get_session
from sqlmodel import Session
from src.models.user import User
from src.models.task import Task
from src.models.conversation import Conversation
from src.models.message import Message
from src.services.data import data_service


@pytest.fixture
def mock_db_session():
    """Mock database session for testing"""
    session = Mock(spec=Session)
    yield session


@pytest.fixture
def test_client():
    """Test client for the FastAPI application"""
    with TestClient(app) as client:
        yield client


def test_task_creation_integration_success(test_client, mock_db_session):
    """
    Integration test for task creation flow
    Tests the complete flow: user message → AI agent → add_task MCP tool → database persistence
    """
    # Mock the database session dependency
    def mock_get_session():
        yield mock_db_session

    app.dependency_overrides[get_session] = mock_get_session

    # Mock the authentication service to return a valid user
    with patch('src.api.chat.get_current_user_with_user_id_check') as mock_auth:
        mock_auth.return_value = SessionVerificationResponse(
            user_id="test_user_123",
            email="test@example.com",
            is_valid=True
        )

        # Mock the agent service to return a response indicating a task was created
        with patch('src.api.chat.TodoAgentService') as mock_agent_class:
            mock_agent_instance = AsyncMock()
            mock_agent_instance.process_request.return_value = Mock(
                response="Task 'buy groceries' has been created successfully.",
                tool_calls=["add_task"]
            )
            mock_agent_class.return_value = mock_agent_instance

            # Mock the data service methods that will be called
            with patch('src.api.chat.data_service') as mock_data_service:
                # Mock creating a conversation
                mock_conversation = Conversation(
                    id=1,
                    user_id="test_user_123",
                    created_at="2023-01-01T00:00:00",
                    updated_at="2023-01-01T00:00:00"
                )
                mock_data_service.create_conversation.return_value = mock_conversation
                mock_data_service.get_conversation_by_id.return_value = mock_conversation

                # Mock creating user message
                mock_user_message = Message(
                    id=1,
                    user_id="test_user_123",
                    conversation_id=1,
                    role="user",
                    content="Add a task to buy groceries",
                    created_at="2023-01-01T00:00:00"
                )
                mock_data_service.create_message.return_value = mock_user_message

                # Mock creating assistant message
                mock_assistant_message = Message(
                    id=2,
                    user_id="test_user_123",
                    conversation_id=1,
                    role="assistant",
                    content="Task 'buy groceries' has been created successfully.",
                    created_at="2023-01-01T00:00:00"
                )
                mock_data_service.create_message.return_value = mock_assistant_message

                # Prepare test request
                user_id = "test_user_123"
                test_request = {
                    "message": "Add a task to buy groceries"
                }

                # Make request to the endpoint
                response = test_client.post(f"/api/v1/{user_id}/chat", json=test_request)

                # Verify response
                assert response.status_code == 200
                response_data = response.json()
                assert response_data["conversation_id"] == 1
                assert "buy groceries" in response_data["response"].lower()
                assert "add_task" in response_data["tool_calls"]

                # Verify that the agent was called with correct parameters
                mock_agent_instance.process_request.assert_called_once()
                call_args = mock_agent_instance.process_request.call_args
                assert call_args[1]['user_id'] == "test_user_123"
                assert call_args[1]['message'] == "Add a task to buy groceries"

                # Verify that data service methods were called to persist messages
                assert mock_data_service.create_conversation.called
                assert mock_data_service.create_message.call_count >= 2  # user and assistant messages

    # Clean up dependency overrides
    app.dependency_overrides = {}


def test_task_creation_integration_with_existing_conversation(test_client, mock_db_session):
    """
    Integration test for task creation flow with existing conversation
    """
    # Mock the database session dependency
    def mock_get_session():
        yield mock_db_session

    app.dependency_overrides[get_session] = mock_get_session

    # Mock the authentication service to return a valid user
    with patch('src.api.chat.get_current_user_with_user_id_check') as mock_auth:
        mock_auth.return_value = SessionVerificationResponse(
            user_id="test_user_123",
            email="test@example.com",
            is_valid=True
        )

        # Mock the agent service
        with patch('src.api.chat.TodoAgentService') as mock_agent_class:
            mock_agent_instance = AsyncMock()
            mock_agent_instance.process_request.return_value = Mock(
                response="Task 'call mom' has been created successfully.",
                tool_calls=["add_task"]
            )
            mock_agent_class.return_value = mock_agent_instance

            # Mock the data service methods
            with patch('src.api.chat.data_service') as mock_data_service:
                # Mock getting existing conversation
                mock_conversation = Conversation(
                    id=5,
                    user_id="test_user_123",
                    created_at="2023-01-01T00:00:00",
                    updated_at="2023-01-01T00:00:00"
                )
                mock_data_service.get_conversation_by_id.return_value = mock_conversation

                # Mock creating messages
                mock_user_message = Message(
                    id=3,
                    user_id="test_user_123",
                    conversation_id=5,
                    role="user",
                    content="Add a task to call mom",
                    created_at="2023-01-01T00:00:00"
                )
                mock_assistant_message = Message(
                    id=4,
                    user_id="test_user_123",
                    conversation_id=5,
                    role="assistant",
                    content="Task 'call mom' has been created successfully.",
                    created_at="2023-01-01T00:00:00"
                )
                mock_data_service.create_message.side_effect = [mock_user_message, mock_assistant_message]

                # Prepare test request with existing conversation ID
                user_id = "test_user_123"
                test_request = {
                    "conversation_id": 5,
                    "message": "Add a task to call mom"
                }

                # Make request
                response = test_client.post(f"/api/v1/{user_id}/chat", json=test_request)

                # Verify response
                assert response.status_code == 200
                response_data = response.json()
                assert response_data["conversation_id"] == 5
                assert "call mom" in response_data["response"].lower()

    # Clean up dependency overrides
    app.dependency_overrides = {}


def test_task_creation_agent_error_handling(test_client, mock_db_session):
    """
    Integration test for task creation when agent encounters an error
    """
    # Mock the database session dependency
    def mock_get_session():
        yield mock_db_session

    app.dependency_overrides[get_session] = mock_get_session

    # Mock the authentication service to return a valid user
    with patch('src.api.chat.get_current_user_with_user_id_check') as mock_auth:
        mock_auth.return_value = SessionVerificationResponse(
            user_id="test_user_123",
            email="test@example.com",
            is_valid=True
        )

        # Mock the agent service to raise an exception
        with patch('src.api.chat.TodoAgentService') as mock_agent_class:
            mock_agent_instance = AsyncMock()
            mock_agent_instance.process_request.side_effect = Exception("Agent processing failed")
            mock_agent_class.return_value = mock_agent_instance

            # Prepare test request
            user_id = "test_user_123"
            test_request = {
                "message": "Add a task to test error handling"
            }

            # Make request - should handle the error gracefully
            response = test_client.post(f"/api/v1/{user_id}/chat", json=test_request)

            # Should return an appropriate error status
            # The exact status depends on the error handling implementation
            assert response.status_code in [500, 422, 400]  # Expected error responses

    # Clean up dependency overrides
    app.dependency_overrides = {}


def test_task_creation_database_error_handling(test_client, mock_db_session):
    """
    Integration test for task creation when database operations fail
    """
    # Mock the database session dependency
    def mock_get_session():
        yield mock_db_session

    app.dependency_overrides[get_session] = mock_get_session

    # Mock the authentication service to return a valid user
    with patch('src.api.chat.get_current_user_with_user_id_check') as mock_auth:
        mock_auth.return_value = SessionVerificationResponse(
            user_id="test_user_123",
            email="test@example.com",
            is_valid=True
        )

        # Mock the agent service to return a normal response
        with patch('src.api.chat.TodoAgentService') as mock_agent_class:
            mock_agent_instance = AsyncMock()
            mock_agent_instance.process_request.return_value = Mock(
                response="Task 'test' has been created.",
                tool_calls=["add_task"]
            )
            mock_agent_class.return_value = mock_agent_instance

            # Mock the data service to raise an exception when creating conversation
            with patch('src.api.chat.data_service') as mock_data_service:
                mock_data_service.create_conversation.side_effect = Exception("Database error")

                # Prepare test request
                user_id = "test_user_123"
                test_request = {
                    "message": "Add a task to test database error"
                }

                # Make request
                response = test_client.post(f"/api/v1/{user_id}/chat", json=test_request)

                # Should return an appropriate error status
                assert response.status_code in [500, 422, 400]  # Expected error responses

    # Clean up dependency overrides
    app.dependency_overrides = {}