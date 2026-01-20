from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.security import HTTPBearer
from typing import Optional
from pydantic import BaseModel
from ..dependencies.auth import get_current_user

# Create API router
router = APIRouter()

# Security scheme for token verification
security = HTTPBearer()

# Pydantic models for request/response
class SessionResponse(BaseModel):
    user: Optional[dict] = None
    session: Optional[dict] = None

class SignUpRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None

class SignUpResponse(BaseModel):
    user: dict
    session: dict

@router.get("/get-session", response_model=SessionResponse)
async def get_session(request: Request):
    """
    Get current user session by verifying the token via Better Auth API
    """
    # Use the dependency to verify the session via Better Auth API
    session_data = await get_current_user(request)

    # Return user and session info
    return SessionResponse(
        user={
            "id": session_data.user_id,
            "email": session_data.email,
            "name": session_data.name  # optional
        },
        session={
            "is_valid": session_data.is_valid,
            "expires_at": session_data.expires_at
        }
    )

@router.post("/sign-up/email", response_model=SignUpResponse)
async def signup_email(signup_data: SignUpRequest):
    """
    Sign up with email and password - redirects to Better Auth
    """
    # This endpoint should not be used directly. Better Auth handles registration on the frontend.
    # Return an error to guide the frontend to use Better Auth properly
    raise HTTPException(
        status_code=400,
        detail="Email registration should be handled through Better Auth frontend. Call authClient.signUp.email() from the frontend."
    )

@router.post("/sign-up/social")
async def signup_social():
    """
    Sign up with social provider - redirects to Better Auth
    """
    # This endpoint should not be used directly. Better Auth handles social registration on the frontend.
    raise HTTPException(
        status_code=400,
        detail="Social registration should be handled through Better Auth frontend. Call authClient.signUp.social() from the frontend."
    )

