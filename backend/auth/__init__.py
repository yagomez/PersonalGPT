"""Authentication package initialization"""

from auth.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_access_token,
    verify_refresh_token,
)
from auth.dependencies import get_current_user, get_optional_user
from auth.schemas import (
    UserCreate,
    UserResponse,
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    CurrentUser,
)

__all__ = [
    "hash_password",
    "verify_password",
    "create_access_token",
    "create_refresh_token",
    "decode_token",
    "verify_access_token",
    "verify_refresh_token",
    "get_current_user",
    "get_optional_user",
    "UserCreate",
    "UserResponse",
    "LoginRequest",
    "LoginResponse",
    "RegisterRequest",
    "RegisterResponse",
    "RefreshTokenRequest",
    "RefreshTokenResponse",
    "CurrentUser",
]
