



# """
# OpenAI Agent SDK implementation for the Todo AI Chatbot.
# """

# import asyncio
# from typing import Dict, Any, List
# from pydantic import BaseModel
# from agents import Agent, Runner, function_tool
# from sqlmodel import Session

# from ..mcp.tools import MCPTools, MCPSessionContext
# from ..services.auth import SessionVerificationResponse
# from .llm_config import model, config
# from .todo_agent_prompt import get_todo_agent_prompt


# # -----------------------------
# # Response Model
# # -----------------------------
# class TodoAgentResponse(BaseModel):
#     response: str
#     tool_calls: List[str] = []


# # -----------------------------
# # Todo Agent Service
# # -----------------------------
# class TodoAgentService:

#     def __init__(self, db_session: Session, user_id: str):
#         self.db_session = db_session
#         self.user_id = user_id
#         self.tool_results: List[Dict[str, Any]] = []
#         self._initialize_agent()

#     # -----------------------------
#     # MCP Tools Factory
#     # -----------------------------
#     def create_mcp_tools_for_user(self) -> MCPTools:
#         user_session = SessionVerificationResponse(
#             user_id=self.user_id,
#             email="temp@example.com",
#             is_verified=True,
#             is_valid=True
#         )
#         session_context = MCPSessionContext(user_session, self.db_session)
#         return MCPTools(session_context)

#     # -----------------------------
#     # Agent Init
#     # -----------------------------
#     def _initialize_agent(self):

#         mcp_tools = self.create_mcp_tools_for_user()
#         agent_self = self

#         @function_tool
#         async def add_task(title: str, description: str = None):
#             result = await mcp_tools.add_task(self.user_id, title, description)
#             agent_self.tool_results.append({"tool": "add_task", "result": result})
#             return result

#         @function_tool
#         async def list_tasks(status: str = "all"):
#             result = await mcp_tools.list_tasks(self.user_id, status)
#             agent_self.tool_results.append({"tool": "list_tasks", "result": result})
#             return result

#         @function_tool
#         async def complete_task(task_id: int):
#             result = await mcp_tools.complete_task(self.user_id, task_id)
#             agent_self.tool_results.append({"tool": "complete_task", "result": result})
#             return result

#         @function_tool
#         async def delete_task(task_id: int):
#             result = await mcp_tools.delete_task(self.user_id, task_id)
#             agent_self.tool_results.append({"tool": "delete_task", "result": result})
#             return result

#         @function_tool
#         async def update_task(task_id: int, title: str = None, description: str = None):
#             result = await mcp_tools.update_task(self.user_id, task_id, title, description)
#             agent_self.tool_results.append({"tool": "update_task", "result": result})
#             return result

#         self.agent = Agent(
#             name="Todo AI Assistant",
#             instructions=get_todo_agent_prompt(),
#             model=model,
#             tools=[
#                 add_task,
#                 list_tasks,
#                 complete_task,
#                 delete_task,
#                 update_task
#             ],
#         )

#     # -----------------------------
#     # Tool Result → User Response
#     # -----------------------------
#     def _generate_response_from_tool_results(self, final_output: str) -> str:
#         tool_results = list(self.tool_results)
#         self.tool_results.clear()

#         responses = []

#         if final_output and final_output.strip():
#             responses.append(final_output)

#         for tr in tool_results:
#             tool = tr["tool"]
#             data = tr["result"]

#             if tool == "add_task":
#                 responses.append(f"✅ Task added: {data.get('title')} (ID {data.get('task_id')})")
#             elif tool == "list_tasks":
#                 responses.append(f"📋 {len(data)} task(s) found")
#             elif tool == "complete_task":
#                 responses.append(f"✅ Task completed (ID {data.get('task_id')})")
#             elif tool == "delete_task":
#                 responses.append(f"🗑️ Task deleted (ID {data.get('task_id')})")
#             elif tool == "update_task":
#                 responses.append(f"✏️ Task updated (ID {data.get('task_id')})")

#         return "\n".join(responses) if responses else "✅ Done."

#     # -----------------------------
#     # ASYNC RUN
#     # -----------------------------
#     async def process_request(
#         self,
#         message: str,
#         conversation_id: int = None,
#         db_session: Session = None
#     ) -> TodoAgentResponse:

#         self.tool_results.clear()

#         try:
#             result = await Runner.run(
#                 self.agent,
#                 input=message,
#                 run_config=config
#             )

#             response_text = self._generate_response_from_tool_results(
#                 result.final_output or ""
#             )

#             return TodoAgentResponse(
#                 response=response_text,
#                 tool_calls=[]
#             )

#         except Exception as e:
#             error = str(e)

#             # 🔥 QUOTA SAFE HANDLING
#             if "429" in error or "RESOURCE_EXHAUSTED" in error:
#                 return TodoAgentResponse(
#                     response="⚠️ AI quota limit reached. Please wait 40 seconds and try again.",
#                     tool_calls=[]
#                 )

#             # Fallback safe response
#             return TodoAgentResponse(
#                 response="❌ Error occurred, but your action may have been completed.",
#                 tool_calls=[]
#             )

#     # -----------------------------
#     # SYNC RUN
#     # -----------------------------
#     def run_sync(
#         self,
#         message: str,
#         conversation_id: int = None,
#         db_session: Session = None
#     ) -> TodoAgentResponse:

#         self.tool_results.clear()

#         try:
#             result = Runner.run_sync(
#                 self.agent,
#                 input=message,
#                 run_config=config
#             )

#             response_text = self._generate_response_from_tool_results(
#                 result.final_output or ""
#             )

#             return TodoAgentResponse(response=response_text, tool_calls=[])

#         except Exception as e:
#             error = str(e)

#             if "429" in error or "RESOURCE_EXHAUSTED" in error:
#                 return TodoAgentResponse(
#                     response="⚠️ AI quota limit reached. Please wait and retry.",
#                     tool_calls=[]
#                 )

#             return TodoAgentResponse(
#                 response="❌ Error occurred while processing your request.",
#                 tool_calls=[]
#             )




"""
OpenAI Agent SDK implementation for the Todo AI Chatbot.
"""

from typing import Dict, Any
from pydantic import BaseModel
from agents import Agent, Runner, function_tool
from sqlmodel import Session

from ..mcp.tools import MCPTools, MCPSessionContext
from ..services.auth import SessionVerificationResponse
from .llm_config import model, config
from .todo_agent_prompt import get_todo_agent_prompt


# -----------------------------
# Response Model
# -----------------------------
class TodoAgentResponse(BaseModel):
    response: str


# -----------------------------
# Todo Agent Service
# -----------------------------
class TodoAgentService:

    def __init__(self, db_session: Session, user_id: str):
        self.db_session = db_session
        self.user_id = user_id
        self._initialize_agent()

    # -----------------------------
    # MCP Tools Factory
    # -----------------------------
    def create_mcp_tools_for_user(self) -> MCPTools:
        user_session = SessionVerificationResponse(
            user_id=self.user_id,
            email="temp@example.com",
            is_verified=True,
            is_valid=True
        )
        session_context = MCPSessionContext(user_session, self.db_session)
        return MCPTools(session_context)

    # -----------------------------
    # Agent Initialization
    # -----------------------------
    def _initialize_agent(self):

        mcp_tools = self.create_mcp_tools_for_user()

        @function_tool
        async def add_task(title: str, description: str = None):
            return await mcp_tools.add_task(self.user_id, title, description)

        @function_tool
        async def list_tasks(status: str = "all"):
            return await mcp_tools.list_tasks(self.user_id, status)

        @function_tool
        async def complete_task(task_id: int):
            return await mcp_tools.complete_task(self.user_id, task_id)

        @function_tool
        async def delete_task(task_id: int):
            return await mcp_tools.delete_task(self.user_id, task_id)

        @function_tool
        async def update_task(task_id: int, title: str = None, description: str = None):
            return await mcp_tools.update_task(
                self.user_id, task_id, title, description
            )

        self.agent = Agent(
            name="Todo AI Assistant",
            instructions=get_todo_agent_prompt(),
            model=model,
            tools=[
                add_task,
                list_tasks,
                complete_task,
                delete_task,
                update_task
            ],
        )

    # -----------------------------
    # ASYNC RUN
    # -----------------------------
    async def process_request(
        self,
        message: str,
        conversation_id: int = None,
        db_session: Session = None
    ) -> TodoAgentResponse:

        try:
            result = await Runner.run(
                self.agent,
                input=message,
                run_config=config
            )

            return TodoAgentResponse(
                response=result.final_output or "✅ Done."
            )

        except Exception as e:
            error = str(e)

            # Gemini quota handling
            if "429" in error or "RESOURCE_EXHAUSTED" in error:
                return TodoAgentResponse(
                    response="You have reached the AI usage limit. Kindly wait 40 seconds before retrying."
                )

            return TodoAgentResponse(
                response="An error has occurred; however, your action might have been completed successfully."
            )

    # -----------------------------
    # SYNC RUN
    # -----------------------------
    def run_sync(
        self,
        message: str,
        conversation_id: int = None,
        db_session: Session = None
    ) -> TodoAgentResponse:

        try:
            result = Runner.run_sync(
                self.agent,
                input=message,
                run_config=config
            )

            return TodoAgentResponse(
                response=result.final_output or "✅ Done."
            )

        except Exception as e:
            error = str(e)

            if "429" in error or "RESOURCE_EXHAUSTED" in error:
                return TodoAgentResponse(
                    response="⚠️ AI quota limit reached. Please retry shortly."
                )

            return TodoAgentResponse(
                response="❌ Error occurred while processing your request."
            )
