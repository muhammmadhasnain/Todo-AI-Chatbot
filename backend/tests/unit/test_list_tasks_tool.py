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
async def test_list_tasks_success(mcp_tools, mock_db_session, mock_user_session):
    """
    Unit test for list_tasks MCP tool - successful case
    Tests the contract: requires user_id, optional status; returns array of task objects
    """
    # Create mock tasks
    mock_task1 = Mock(spec=Task)
    mock_task1.id = 1
    mock_task1.user_id = mock_user_session.user_id
    mock_task1.title = "Buy groceries"
    mock_task1.description = "Milk, bread, eggs"
    mock_task1.completed = False
    mock_task1.created_at = datetime.now()
    mock_task1.updated_at = datetime.now()

    mock_task2 = Mock(spec=Task)
    mock_task2.id = 2
    mock_task2.user_id = mock_user_session.user_id
    mock_task2.title = "Finish report"
    mock_task2.description = "Complete the quarterly report"
    mock_task2.completed = True
    mock_task2.created_at = datetime.now()
    mock_task2.updated_at = datetime.now()

    mock_tasks = [mock_task1, mock_task2]

    # Mock the data service call
    with patch('src.mcp.tools.data_service') as mock_data_service:
        mock_data_service.get_tasks_by_user.return_value = mock_tasks

        # Call the list_tasks method
        result = await mcp_tools.list_tasks(
            user_id=mock_user_session.user_id,
            status="all"
        )

        # Verify the result matches the contract
        assert isinstance(result, list)
        assert len(result) == 2

        # Verify the first task structure
        first_task = result[0]
        assert "id" in first_task
        assert "user_id" in first_task
        assert "title" in first_task
        assert "description" in first_task
        assert "completed" in first_task
        assert "created_at" in first_task
        assert "updated_at" in first_task

        # Verify values
        assert first_task["id"] == 1
        assert first_task["title"] == "Buy groceries"
        assert first_task["completed"] == False

        # Verify the second task
        second_task = result[1]
        assert second_task["id"] == 2
        assert second_task["title"] == "Finish report"
        assert second_task["completed"] == True

        # Verify the data service was called with correct parameters
        mock_data_service.get_tasks_by_user.assert_called_once_with(
            mock_db_session, mock_user_session.user_id, status_filter="all"
        )


@pytest.mark.asyncio
async def test_list_tasks_without_status_param(mcp_tools, mock_db_session, mock_user_session):
    """
    Unit test for list_tasks MCP tool - without status parameter (defaults to "all")
    """
    # Create mock tasks
    mock_task = Mock(spec=Task)
    mock_task.id = 1
    mock_task.user_id = mock_user_session.user_id
    mock_task.title = "Default test task"
    mock_task.completed = False
    mock_task.created_at = datetime.now()
    mock_task.updated_at = datetime.now()

    mock_tasks = [mock_task]

    # Mock the data service call
    with patch('src.mcp.tools.data_service') as mock_data_service:
        mock_data_service.get_tasks_by_user.return_value = mock_tasks

        # Call the list_tasks method without status parameter (should default to "all")
        result = await mcp_tools.list_tasks(user_id=mock_user_session.user_id)

        # Verify the result
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["title"] == "Default test task"

        # Verify the data service was called with default "all" status
        mock_data_service.get_tasks_by_user.assert_called_once_with(
            mock_db_session, mock_user_session.user_id, status_filter="all"
        )


@pytest.mark.asyncio
async def test_list_tasks_with_status_filter_pending(mcp_tools, mock_db_session, mock_user_session):
    """
    Unit test for list_tasks MCP tool - with "pending" status filter
    """
    # Create mock tasks (only pending tasks)
    mock_task1 = Mock(spec=Task)
    mock_task1.id = 1
    mock_task1.user_id = mock_user_session.user_id
    mock_task1.title = "Pending task 1"
    mock_task1.completed = False
    mock_task1.created_at = datetime.now()
    mock_task1.updated_at = datetime.now()

    mock_task2 = Mock(spec=Task)
    mock_task2.id = 2
    mock_task2.user_id = mock_user_session.user_id
    mock_task2.title = "Pending task 2"
    mock_task2.completed = False
    mock_task2.created_at = datetime.now()
    mock_task2.updated_at = datetime.now()

    mock_tasks = [mock_task1, mock_task2]

    # Mock the data service call
    with patch('src.mcp.tools.data_service') as mock_data_service:
        mock_data_service.get_tasks_by_user.return_value = mock_tasks

        # Call the list_tasks method with "pending" status
        result = await mcp_tools.list_tasks(
            user_id=mock_user_session.user_id,
            status="pending"
        )

        # Verify the result
        assert isinstance(result, list)
        assert len(result) == 2
        for task in result:
            assert task["completed"] == False

        # Verify the data service was called with correct status
        mock_data_service.get_tasks_by_user.assert_called_once_with(
            mock_db_session, mock_user_session.user_id, status_filter="pending"
        )


@pytest.mark.asyncio
async def test_list_tasks_with_status_filter_completed(mcp_tools, mock_db_session, mock_user_session):
    """
    Unit test for list_tasks MCP tool - with "completed" status filter
    """
    # Create mock tasks (only completed tasks)
    mock_task = Mock(spec=Task)
    mock_task.id = 1
    mock_task.user_id = mock_user_session.user_id
    mock_task.title = "Completed task"
    mock_task.completed = True
    mock_task.created_at = datetime.now()
    mock_task.updated_at = datetime.now()

    mock_tasks = [mock_task]

    # Mock the data service call
    with patch('src.mcp.tools.data_service') as mock_data_service:
        mock_data_service.get_tasks_by_user.return_value = mock_tasks

        # Call the list_tasks method with "completed" status
        result = await mcp_tools.list_tasks(
            user_id=mock_user_session.user_id,
            status="completed"
        )

        # Verify the result
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["completed"] == True
        assert result[0]["title"] == "Completed task"

        # Verify the data service was called with correct status
        mock_data_service.get_tasks_by_user.assert_called_once_with(
            mock_db_session, mock_user_session.user_id, status_filter="completed"
        )


@pytest.mark.asyncio
async def test_list_tasks_unauthorized_user(mcp_tools, mock_db_session, mock_user_session):
    """
    Unit test for list_tasks MCP tool - unauthorized user access
    Tests that users cannot list tasks for other users
    """
    # Try to list tasks for a different user_id
    different_user_id = "another_user_456"

    # Call the list_tasks method with different user_id
    with pytest.raises(HTTPException) as exc_info:
        await mcp_tools.list_tasks(user_id=different_user_id, status="all")

    # Verify the exception
    assert exc_info.value.status_code == 403
    assert "Cannot list tasks for another user" in exc_info.value.detail


@pytest.mark.asyncio
async def test_list_tasks_empty_result(mcp_tools, mock_db_session, mock_user_session):
    """
    Unit test for list_tasks MCP tool - empty result
    """
    # Mock the data service to return empty list
    with patch('src.mcp.tools.data_service') as mock_data_service:
        mock_data_service.get_tasks_by_user.return_value = []

        # Call the list_tasks method
        result = await mcp_tools.list_tasks(user_id=mock_user_session.user_id)

        # Verify the result is an empty list
        assert isinstance(result, list)
        assert len(result) == 0

        # Verify the data service was called
        mock_data_service.get_tasks_by_user.assert_called_once()


@pytest.mark.asyncio
async def test_list_tasks_data_service_error(mcp_tools, mock_db_session, mock_user_session):
    """
    Unit test for list_tasks MCP tool - data service error
    """
    # Mock the data service to raise an exception
    with patch('src.mcp.tools.data_service') as mock_data_service:
        mock_data_service.get_tasks_by_user.side_effect = Exception("Database error")

        # Call the list_tasks method - should handle the error appropriately
        with pytest.raises(Exception):
            await mcp_tools.list_tasks(user_id=mock_user_session.user_id)


@pytest.mark.asyncio
async def test_list_tasks_single_task(mcp_tools, mock_db_session, mock_user_session):
    """
    Unit test for list_tasks MCP tool - single task result
    """
    # Create mock task
    mock_task = Mock(spec=Task)
    mock_task.id = 100
    mock_task.user_id = mock_user_session.user_id
    mock_task.title = "Single task"
    mock_task.description = "This is a single task"
    mock_task.completed = False
    mock_task.created_at = datetime.now()
    mock_task.updated_at = datetime.now()

    mock_tasks = [mock_task]

    # Mock the data service call
    with patch('src.mcp.tools.data_service') as mock_data_service:
        mock_data_service.get_tasks_by_user.return_value = mock_tasks

        # Call the list_tasks method
        result = await mcp_tools.list_tasks(
            user_id=mock_user_session.user_id,
            status="all"
        )

        # Verify the result
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["id"] == 100
        assert result[0]["title"] == "Single task"
        assert result[0]["description"] == "This is a single task"
        assert result[0]["completed"] == False