import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.mcp.tools import MCPSessionContext, MCPTools
from src.services.auth import SessionVerificationResponse
from src.models.task import Task
from fastapi import HTTPException
from datetime import datetime


@pytest.fixture
def mock_db_session():
    """Mock database session for testing"""
    session = Mock()
    yield session


@pytest.fixture
def mock_user_session():
    """Mock user session for testing"""
    user_session = SessionVerificationResponse(
        user_id="test_user_123",
        email="test@example.com",
        is_valid=True
    )
    yield user_session


@pytest.fixture
def mcp_tools(mock_user_session, mock_db_session):
    """Create MCP tools instance for testing"""
    session_context = MCPSessionContext(mock_user_session, mock_db_session)
    tools = MCPTools(session_context)
    yield tools


@pytest.mark.asyncio
async def test_add_task_success(mcp_tools, mock_db_session, mock_user_session):
    """
    Unit test for add_task MCP tool - successful case
    Tests the contract: requires user_id, title, optional description; returns task_id, status, title
    """
    # Mock the data service to return a task
    mock_task = Mock(spec=Task)
    mock_task.id = 42
    mock_task.title = "Buy groceries"
    mock_task.description = "Milk, bread, eggs"
    mock_task.completed = False
    mock_task.created_at = datetime.now()
    mock_task.updated_at = datetime.now()
    mock_task.user_id = mock_user_session.user_id

    # Mock the data service call
    with patch('src.mcp.tools.data_service') as mock_data_service:
        mock_data_service.create_task.return_value = mock_task

        # Call the add_task method
        result = await mcp_tools.add_task(
            user_id=mock_user_session.user_id,
            title="Buy groceries",
            description="Milk, bread, eggs"
        )

        # Verify the result matches the contract
        assert result["task_id"] == 42
        assert result["status"] == "created"
        assert result["title"] == "Buy groceries"

        # Verify the data service was called with correct parameters
        mock_data_service.create_task.assert_called_once()
        call_args = mock_data_service.create_task.call_args
        # Verify the arguments passed to create_task
        assert call_args[0][2] == mock_user_session.user_id  # user_id parameter


@pytest.mark.asyncio
async def test_add_task_without_description(mcp_tools, mock_db_session, mock_user_session):
    """
    Unit test for add_task MCP tool - without optional description
    """
    # Mock the data service to return a task
    mock_task = Mock(spec=Task)
    mock_task.id = 123
    mock_task.title = "Complete project"
    mock_task.description = None
    mock_task.completed = False
    mock_task.created_at = datetime.now()
    mock_task.updated_at = datetime.now()
    mock_task.user_id = mock_user_session.user_id

    # Mock the data service call
    with patch('src.mcp.tools.data_service') as mock_data_service:
        mock_data_service.create_task.return_value = mock_task

        # Call the add_task method without description
        result = await mcp_tools.add_task(
            user_id=mock_user_session.user_id,
            title="Complete project"
        )

        # Verify the result
        assert result["task_id"] == 123
        assert result["status"] == "created"
        assert result["title"] == "Complete project"


@pytest.mark.asyncio
async def test_add_task_unauthorized_user(mcp_tools, mock_db_session, mock_user_session):
    """
    Unit test for add_task MCP tool - unauthorized user access
    Tests that users cannot add tasks for other users
    """
    # Try to add a task for a different user_id
    different_user_id = "another_user_456"

    # Call the add_task method with different user_id
    with pytest.raises(HTTPException) as exc_info:
        await mcp_tools.add_task(
            user_id=different_user_id,
            title="Should fail"
        )

    # Verify the exception
    assert exc_info.value.status_code == 403
    assert "Cannot add task for another user" in exc_info.value.detail


@pytest.mark.asyncio
async def test_add_task_data_service_error(mcp_tools, mock_db_session, mock_user_session):
    """
    Unit test for add_task MCP tool - data service error
    """
    # Mock the data service to raise an exception
    with patch('src.mcp.tools.data_service') as mock_data_service:
        mock_data_service.create_task.side_effect = Exception("Database error")

        # Call the add_task method - should handle the error appropriately
        with pytest.raises(Exception):
            await mcp_tools.add_task(
                user_id=mock_user_session.user_id,
                title="Task with error"
            )


@pytest.mark.asyncio
async def test_add_task_empty_title_error(mcp_tools, mock_db_session, mock_user_session):
    """
    Unit test for add_task MCP tool - empty title validation
    """
    # Mock the data service to return a task
    mock_task = Mock(spec=Task)
    mock_task.id = 456
    mock_task.title = ""  # Empty title
    mock_task.completed = False
    mock_task.created_at = datetime.now()
    mock_task.updated_at = datetime.now()
    mock_task.user_id = mock_user_session.user_id

    # Mock the data service call
    with patch('src.mcp.tools.data_service') as mock_data_service:
        mock_data_service.create_task.return_value = mock_task

        # Call the add_task method with empty title
        result = await mcp_tools.add_task(
            user_id=mock_user_session.user_id,
            title=""
        )

        # Result should still have the empty title, validation should be handled by data service
        assert result["title"] == ""


@pytest.mark.asyncio
async def test_add_task_special_characters(mcp_tools, mock_db_session, mock_user_session):
    """
    Unit test for add_task MCP tool - special characters in title/description
    """
    # Mock the data service to return a task
    mock_task = Mock(spec=Task)
    mock_task.id = 789
    mock_task.title = "Buy groceries & stuff!"
    mock_task.description = "Test with: special; characters? Yes!"
    mock_task.completed = False
    mock_task.created_at = datetime.now()
    mock_task.updated_at = datetime.now()
    mock_task.user_id = mock_user_session.user_id

    # Mock the data service call
    with patch('src.mcp.tools.data_service') as mock_data_service:
        mock_data_service.create_task.return_value = mock_task

        # Call the add_task method with special characters
        result = await mcp_tools.add_task(
            user_id=mock_user_session.user_id,
            title="Buy groceries & stuff!",
            description="Test with: special; characters? Yes!"
        )

        # Verify the result
        assert result["task_id"] == 789
        assert result["status"] == "created"
        assert result["title"] == "Buy groceries & stuff!"


@pytest.mark.asyncio
async def test_add_task_long_title_and_description(mcp_tools, mock_db_session, mock_user_session):
    """
    Unit test for add_task MCP tool - long title and description
    """
    long_title = "A" * 200  # 200 character title
    long_description = "B" * 1000  # 1000 character description

    # Mock the data service to return a task
    mock_task = Mock(spec=Task)
    mock_task.id = 999
    mock_task.title = long_title
    mock_task.description = long_description
    mock_task.completed = False
    mock_task.created_at = datetime.now()
    mock_task.updated_at = datetime.now()
    mock_task.user_id = mock_user_session.user_id

    # Mock the data service call
    with patch('src.mcp.tools.data_service') as mock_data_service:
        mock_data_service.create_task.return_value = mock_task

        # Call the add_task method with long text
        result = await mcp_tools.add_task(
            user_id=mock_user_session.user_id,
            title=long_title,
            description=long_description
        )

        # Verify the result
        assert result["task_id"] == 999
        assert result["status"] == "created"
        assert result["title"] == long_title


