from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ..dependencies.auth import get_current_user_with_user_id_check
from ..services.auth import SessionVerificationResponse
from sqlmodel import Session
from ..db.session import get_session
from ..models.user import User, UserUpdate
from ..services.data import data_service

router = APIRouter()

# Request and Response models
class UserResponse(BaseModel):
    id: int
    user_id: str
    email: str
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    email_verified: bool = False
    created_at: str
    updated_at: str
    last_login_at: Optional[str] = None

class UserProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    avatar_url: Optional[str] = None

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_profile(
    user_id: str,
    current_user: SessionVerificationResponse = Depends(get_current_user_with_user_id_check),
    db_session: Session = Depends(get_session)
):
    """
    Get user profile information (requires authenticated session and user_id validation).
    This endpoint ensures users can only access their own profile information.
    If the user doesn't exist in the app database yet, it creates a profile based on the authenticated session.
    """
    # Get user using the data service
    user = data_service.get_user_by_id(db_session, user_id)

    if not user:
        # User doesn't exist in app database, create from Better Auth session data
        from ..models.user import User as UserModel
        from datetime import datetime

        # Create user based on the authenticated session data
        new_user = UserModel(
            user_id=user_id,
            email = current_user.email or "",
            name = current_user.name or "",

            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        try:
            user = data_service.create_user(db_session, new_user)
        except Exception as e:
            # If creation fails (e.g., due to duplicate), try to get the user again
            user = data_service.get_user_by_id(db_session, user_id)
            if not user:
                raise HTTPException(
                    status_code=404,
                    detail="User not found and could not be created"
                )

    return UserResponse(
        id=user.id,
        user_id=user.user_id,
        email=user.email,
        name=user.name,
        avatar_url=getattr(user, 'avatar_url', None),
        email_verified=getattr(user, 'email_verified', False),
        created_at=user.created_at.isoformat(),
        updated_at=user.updated_at.isoformat(),
        last_login_at=getattr(user, 'last_login_at', None).isoformat() if getattr(user, 'last_login_at', None) else None
    )

@router.put("/{user_id}", response_model=UserResponse)
async def update_user_profile(
    user_id: str,
    profile_update: UserProfileUpdateRequest,
    current_user: SessionVerificationResponse = Depends(get_current_user_with_user_id_check),
    db_session: Session = Depends(get_session)
):
    """
    Update user profile information (requires authenticated session and user_id validation).
    This endpoint ensures users can only update their own profile information.
    """
    # Validate that the user_id in the path matches the authenticated user
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized: Cannot update profile for another user"
        )

    # Prepare update data
    update_data = {}
    if profile_update.name is not None:
        update_data['name'] = profile_update.name
    if profile_update.avatar_url is not None:
        update_data['avatar_url'] = profile_update.avatar_url

    # Update user using the data service
    updated_user = data_service.update_user(db_session, user_id, update_data)

    if not updated_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return UserResponse(
        id=updated_user.id,
        user_id=updated_user.user_id,
        email=updated_user.email,
        name=updated_user.name,
        avatar_url=updated_user.avatar_url,
        email_verified=updated_user.email_verified,
        created_at=updated_user.created_at.isoformat(),
        updated_at=updated_user.updated_at.isoformat(),
        last_login_at=updated_user.last_login_at.isoformat() if updated_user.last_login_at else None
    )

@router.delete("/{user_id}")
async def delete_user_account(
    user_id: str,
    current_user: SessionVerificationResponse = Depends(get_current_user_with_user_id_check),
    db_session: Session = Depends(get_session)
):
    """
    Delete user account (requires authenticated session and user_id validation).
    This endpoint ensures users can only delete their own account.
    NOTE: This is a sensitive operation that would require additional verification in production.
    """
    # Delete user using the data service
    success = data_service.delete_user(db_session, user_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {"message": f"User account {user_id} marked for deletion"}