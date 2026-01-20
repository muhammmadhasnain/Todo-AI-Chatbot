from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class UserBase(SQLModel):
    """Base model for User with common fields"""
    email: str = Field(unique=True, nullable=False, description="User's email address")
    name: Optional[str] = Field(default=None, description="User's display name")


class User(UserBase, table=True):
    """
    User model representing an authenticated user in the system.
    This follows the exact specifications from the constitution:
    - id: Unique identifier for the user (from Better Auth system)
    - user_id: User ID from Better Auth system
    - email: User's email address
    - name: User's display name
    - created_at: Timestamp of user creation
    - updated_at: Timestamp of last update
    """
    __tablename__ = "user_profiles"

    # Primary key - using auto-generated ID for internal use
    id: int = Field(default=None, primary_key=True, description="Internal unique identifier for the user")

    # Better Auth user ID - this is what we use for identification
    user_id: str = Field(unique=True, nullable=False, description="User ID from Better Auth system")

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of user creation")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of last update")

    # Additional fields that might come from Better Auth
    avatar_url: Optional[str] = Field(default=None, description="User's avatar URL")
    email_verified: bool = Field(default=False, description="Whether the user's email is verified")
    last_login_at: Optional[datetime] = Field(default=None, description="Timestamp of last login")


class UserCreate(SQLModel):
    """Model for creating a new user"""
    user_id: str
    email: str
    name: Optional[str] = None


class UserRead(SQLModel):
    """Model for reading user data (without sensitive information)"""
    id: int
    user_id: str
    email: str
    name: Optional[str]
    created_at: datetime
    updated_at: datetime


class UserUpdate(SQLModel):
    """Model for updating user information"""
    name: Optional[str] = None