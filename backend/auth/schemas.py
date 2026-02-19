"""Authentication schemas for request/response validation"""

from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    """User creation schema"""
    password: str

class UserResponse(UserBase):
    """User response schema (without sensitive data)"""
    id: UUID
    avatar_url: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    """Login response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse

class RefreshTokenRequest(BaseModel):
    """Refresh token request schema"""
    refresh_token: str

class RefreshTokenResponse(BaseModel):
    """Refresh token response schema"""
    access_token: str
    token_type: str = "bearer"

class RegisterRequest(UserCreate):
    """Registration request schema"""
    pass

class RegisterResponse(BaseModel):
    """Registration response schema"""
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class CurrentUser(UserResponse):
    """Current authenticated user schema"""
    pass

class UserSettingsResponse(BaseModel):
    """User settings schema"""
    id: UUID
    user_id: UUID
    preferred_model: str
    temperature: float
    max_tokens: int
    theme: str
    language: str
    timezone: str
    email_notifications: bool
    custom_instructions: Optional[str] = None
    search_history_enabled: bool
    data_retention_days: int

    class Config:
        from_attributes = True

class UserSettingsUpdate(BaseModel):
    """User settings update schema"""
    preferred_model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    theme: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[str] = None
    email_notifications: Optional[bool] = None
    custom_instructions: Optional[str] = None
    search_history_enabled: Optional[bool] = None
    data_retention_days: Optional[int] = None
