import logging
import sys
from datetime import datetime
from typing import Any, Dict, Optional
from fastapi import HTTPException
import traceback


class LoggingService:
    """
    Service class that provides structured logging for the application.
    This implements the error handling and logging infrastructure required by the constitution.
    """

    def __init__(self):
        # Configure root logger
        self.logger = logging.getLogger("todo_agent_backend")
        self.logger.setLevel(logging.INFO)

        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)

        # Create file handler
        file_handler = logging.FileHandler("app.log")
        file_handler.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add handlers to logger
        if not self.logger.handlers:
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)

    def log_info(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log an informational message."""
        if extra:
            message = f"{message} | Extra: {extra}"
        self.logger.info(message)

    def log_warning(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log a warning message."""
        if extra:
            message = f"{message} | Extra: {extra}"
        self.logger.warning(message)

    def log_error(self, message: str, extra: Optional[Dict[str, Any]] = None, exc_info: bool = False):
        """Log an error message with optional exception info."""
        if extra:
            message = f"{message} | Extra: {extra}"
        self.logger.error(message, exc_info=exc_info)

    def log_exception(self, message: str, exc: Exception, extra: Optional[Dict[str, Any]] = None):
        """Log an exception with traceback."""
        if extra:
            message = f"{message} | Extra: {extra}"
        self.logger.error(f"{message} | Exception: {str(exc)} | Traceback: {traceback.format_exc()}")

    def log_api_call(self, endpoint: str, method: str, user_id: Optional[str] = None,
                     status_code: Optional[int] = None, response_time: Optional[float] = None):
        """Log API call details."""
        extra = {
            "endpoint": endpoint,
            "method": method,
            "user_id": user_id,
            "status_code": status_code,
            "response_time_ms": response_time
        }
        self.log_info(f"API call to {endpoint}", extra=extra)

    def log_mcp_tool_call(self, tool_name: str, user_id: str,
                          parameters: Optional[Dict[str, Any]] = None,
                          result: Optional[Dict[str, Any]] = None):
        """Log MCP tool calls for observability."""
        extra = {
            "tool_name": tool_name,
            "user_id": user_id,
            "parameters": parameters,
            "result": result
        }
        self.log_info(f"MCP tool call: {tool_name}", extra=extra)

    def log_agent_interaction(self, user_id: str, message: str,
                             response: Optional[str] = None,
                             tools_used: Optional[list] = None):
        """Log agent interactions for monitoring and debugging."""
        extra = {
            "user_id": user_id,
            "message": message,
            "response": response,
            "tools_used": tools_used
        }
        self.log_info("Agent interaction", extra=extra)


# Global instance of the logging service
logging_service = LoggingService()