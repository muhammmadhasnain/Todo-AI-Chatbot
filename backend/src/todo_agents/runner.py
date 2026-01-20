


# """
# Agent Runner for the Todo AI Chatbot.
# """

# import logging
# from typing import Dict, Any, Optional
# from sqlmodel import Session

# from .agent import TodoAgentService
# from agents import set_tracing_disabled

# logger = logging.getLogger(__name__)
# set_tracing_disabled(True)


# class AgentRunner:

#     def __init__(self, db_session: Session, user_id: str | None = None):
#         self.db_session = db_session
#         self.user_id = user_id
#         self.agent_service = (
#             TodoAgentService(db_session, user_id) if user_id else None
#         )

#     # -------------------------
#     # ASYNC
#     # -------------------------
#     async def run_agent(
#         self,
#         user_id: str,
#         message: str,
#         conversation_id: Optional[int] = None
#     ) -> Dict[str, Any]:

#         if not self.agent_service or self.agent_service.user_id != user_id:
#             self.agent_service = TodoAgentService(self.db_session, user_id)

#         try:
#             result = await self.agent_service.process_request(
#                 message=message,
#                 conversation_id=conversation_id,
#                 db_session=self.db_session
#             )

#             return {
#                 "response": result.response,
#                 "tool_calls": result.tool_calls,
#                 "success": True,
#                 "error": None
#             }

#         except Exception as e:
#             logger.error("Agent failed", exc_info=True)
#             return {
#                 "response": "❌ AI failed to process request.",
#                 "tool_calls": [],
#                 "success": False,
#                 "error": str(e)
#             }

#     # -------------------------
#     # SYNC
#     # -------------------------
#     def run_agent_sync(
#         self,
#         user_id: str,
#         message: str,
#         conversation_id: Optional[int] = None
#     ) -> Dict[str, Any]:

#         if not self.agent_service or self.agent_service.user_id != user_id:
#             self.agent_service = TodoAgentService(self.db_session, user_id)

#         try:
#             result = self.agent_service.run_sync(
#                 message=message,
#                 conversation_id=conversation_id,
#                 db_session=self.db_session
#             )

#             return {
#                 "response": result.response,
#                 "tool_calls": result.tool_calls,
#                 "success": True,
#                 "error": None
#             }

#         except Exception as e:
#             logger.error("Agent sync failed", exc_info=True)
#             return {
#                 "response": "❌ AI failed to process request.",
#                 "tool_calls": [],
#                 "success": False,
#                 "error": str(e)
#             }




"""
Agent Runner for the Todo AI Chatbot.
"""

import logging
from typing import Dict, Any, Optional
from sqlmodel import Session

from .agent import TodoAgentService
from agents import set_tracing_disabled

logger = logging.getLogger(__name__)
set_tracing_disabled(True)


class AgentRunner:

    def __init__(self, db_session: Session, user_id: str | None = None):
        self.db_session = db_session
        self.user_id = user_id
        self.agent_service = (
            TodoAgentService(db_session, user_id) if user_id else None
        )

    # -------------------------
    # ASYNC
    # -------------------------
    async def run_agent(
        self,
        user_id: str,
        message: str,
        conversation_id: Optional[int] = None
    ) -> Dict[str, Any]:

        if not self.agent_service or self.agent_service.user_id != user_id:
            self.agent_service = TodoAgentService(self.db_session, user_id)

        try:
            result = await self.agent_service.process_request(
                message=message,
                conversation_id=conversation_id,
                db_session=self.db_session
            )

            return {
                "response": result.response,
                "success": True,
                "error": None
            }

        except Exception as e:
            logger.error("Agent failed", exc_info=True)
            return {
                "response": "❌ AI failed to process request.",
                "success": False,
                "error": str(e)
            }

    # -------------------------
    # SYNC
    # -------------------------
    def run_agent_sync(
        self,
        user_id: str,
        message: str,
        conversation_id: Optional[int] = None
    ) -> Dict[str, Any]:

        if not self.agent_service or self.agent_service.user_id != user_id:
            self.agent_service = TodoAgentService(self.db_session, user_id)

        try:
            result = self.agent_service.run_sync(
                message=message,
                conversation_id=conversation_id,
                db_session=self.db_session
            )

            return {
                "response": result.response,
                "success": True,
                "error": None
            }

        except Exception as e:
            logger.error("Agent sync failed", exc_info=True)
            return {
                "response": "❌ AI failed to process request.",
                "success": False,
                "error": str(e)
            }
