from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..services.auth import session_verification_service, SessionVerificationResponse
from typing import Callable, Optional
import os

class AuthenticationMiddleware:
    """
    Authentication middleware that verifies session tokens using Better Auth API.
    This ensures all requests are properly authenticated before reaching the endpoints.
    """

    def __init__(self):
        self.security = HTTPBearer(auto_error=True)

    async def verify_token(self, credentials: HTTPAuthorizationCredentials) -> SessionVerificationResponse:
        """
        Verify the provided bearer token using Better Auth API.
        """
        if not credentials:
            raise HTTPException(
                status_code=401,
                detail="No credentials provided"
            )

        # Verify the session token using the service
        verification_result = await session_verification_service.verify_session(credentials.credentials)

        if not verification_result.is_valid:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired session token"
            )

        return verification_result

    async def verify_user_access(self, request: Request, call_next) -> Request:
        """
        Verify that the authenticated user can access the requested resource.
        This checks that the user_id in the path matches the authenticated user.
        """
        # Extract user_id from path parameters
        user_id_from_path = request.path_params.get("user_id")

        # Get the authenticated user from request state (set by dependency)
        authenticated_user = request.state.user if hasattr(request.state, 'user') else None

        if user_id_from_path and authenticated_user:
            # Validate that the authenticated user matches the requested user_id
            if authenticated_user.user_id != user_id_from_path:
                raise HTTPException(
                    status_code=403,
                    detail="Access denied: Cannot access another user's resources"
                )

        response = await call_next(request)
        return response

# Global instance of the middleware
auth_middleware = AuthenticationMiddleware()