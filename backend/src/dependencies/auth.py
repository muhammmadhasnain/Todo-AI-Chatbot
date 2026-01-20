import logging
from fastapi import HTTPException, Depends, Request
from typing import Optional
from ..services.auth import session_verification_service, SessionVerificationResponse

logger = logging.getLogger(__name__)

async def get_current_user(request: Request) -> SessionVerificationResponse:
    """
    FastAPI dependency to get the current authenticated user by verifying the session cookies
    via Better Auth API. This ensures all protected endpoints verify sessions before processing.
    """
    # Extract all cookies from the request for debugging
    logger.debug(f"All incoming cookies: {list(request.cookies.keys())}")

    # Extract cookies from the request
    cookies = {}
    for key, value in request.cookies.items():
        if key.startswith('authjs.'):  # NextAuth.js cookie prefix
            cookies[key] = value
        elif key.startswith('better-auth.'):  # Better Auth cookie prefix
            cookies[key] = value

    # If no Better Auth cookies found, try specific Better Auth cookie names
    if not cookies:
        # Better Auth typically uses these specific cookie names
        session_token = request.cookies.get('better-auth.session_token')  # Main session token
        if session_token:
            cookies['better-auth.session_token'] = session_token

        # Also check for other possible Better Auth cookies
        csrf_token = request.cookies.get('better-auth.csrf_token')
        if csrf_token:
            cookies['better-auth.csrf_token'] = csrf_token

    logger.debug(f"Extracted Better Auth cookies: {list(cookies.keys())}")

    if not cookies:
        raise HTTPException(
            status_code=401,
            detail="No session cookies found"
        )

    # Verify the session via Better Auth API using cookies
    session_data = await session_verification_service.verify_session_with_cookies(cookies)

    if not session_data.is_valid:
        # Check if the failure is due to Better Auth service being unavailable vs actual invalid session
        if not cookies:  # No cookies were provided at all
            raise HTTPException(
                status_code=401,
                detail="No session cookies found. User is not authenticated."
            )
        else:  # Cookies were provided but session verification failed
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired session. Please log in again."
            )

    return session_data

async def get_current_user_with_user_id_check(request: Request) -> SessionVerificationResponse:
    """
    FastAPI dependency to verify the session and check if the authenticated user_id
    matches the user_id in the path parameter. This ensures proper user data isolation.
    """
    # Extract user_id from the path
    user_id_from_path = request.path_params.get("user_id")

    # First, get the current authenticated user
    current_user = await get_current_user(request)

    # Check if the authenticated user_id matches the user_id in the path
    if current_user.user_id != user_id_from_path:
        raise HTTPException(
            status_code=403,
            detail="User ID in path does not match authenticated user"
        )

    return current_user