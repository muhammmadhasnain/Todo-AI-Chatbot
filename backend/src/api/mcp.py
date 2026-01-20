from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Dict, Any
from ..dependencies.auth import get_current_user
from ..mcp.tools import create_authenticated_mcp_tools, MCPSessionContext
from sqlmodel import Session
from ..db.session import get_session
import json

router = APIRouter()

@router.post("/mcp")
async def mcp_endpoint(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    MCP endpoint that allows frontend to call MCP tools.
    Expects a JSON payload with 'tool' and 'parameters'.
    """
    try:
        # Parse the request body
        body = await request.json()
        tool_name = body.get("tool")
        parameters = body.get("parameters", {})

        if not tool_name:
            raise HTTPException(status_code=400, detail="Tool name is required")

        # Add user_id to parameters for authentication
        parameters["user_id"] = current_user["id"]

        # Create an MCPSessionContext with the current user and db session
        # We need to create a mock session verification response
        from ..services.auth import SessionVerificationResponse
        user_session = SessionVerificationResponse(
            user_id=current_user["id"],
            email=current_user["email"],
            is_authenticated=True
        )
        session_context = MCPSessionContext(user_session, db)

        # Create an MCPTools instance to handle the tools
        mcp_tools = create_authenticated_mcp_tools(user_session, db)

        # Map tool names to MCP tools methods
        tool_functions = {
            "add_task": mcp_tools.add_task,
            "list_tasks": mcp_tools.list_tasks,
            "complete_task": mcp_tools.complete_task,
            "delete_task": mcp_tools.delete_task,
            "update_task": mcp_tools.update_task,
            "get_history": get_history,  # Placeholder for history functionality
            "send_message": send_message  # Placeholder for send message functionality
        }

        if tool_name not in tool_functions:
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")

        # Call the appropriate tool function
        tool_function = tool_functions[tool_name]

        # Call the tool function with the parameters
        try:
            result = await tool_function(**parameters) if parameters else await tool_function()
            return {"result": result}
        except TypeError as e:
            # If there's a type error, it might be due to extra parameters
            # Try calling with only the required parameters
            # For now, return a more generic response
            raise HTTPException(status_code=400, detail=f"Invalid parameters for tool '{tool_name}': {str(e)}")

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in request body")
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing tool: {str(e)}")


async def get_history(user_id: str, session_id: str = None, limit: int = 50, offset: int = 0):
    """
    Placeholder function for getting chat history.
    In a real implementation, this would retrieve chat history from a database.
    """
    # This is a placeholder implementation
    return {
        "messages": [],
        "count": 0,
        "limit": limit,
        "offset": offset
    }


async def send_message(user_id: str, session_id: str, message: str, metadata: Dict[str, Any] = None):
    """
    Placeholder function for sending a message.
    In a real implementation, this would send the message to the AI service.
    """
    # This is a placeholder implementation
    # In a real implementation, this would call the AI service to process the message
    # and return the response

    # For now, just return a success response with a mock messageId
    return {
        "messageId": f"msg_{user_id}_{int(__import__('time').time())}",
        "status": "sent",
        "response": f"Echo: {message}"  # This would be replaced with actual AI response
    }