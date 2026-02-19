"""Authentication dependencies for FastAPI"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials

from auth.security import verify_access_token
from database import User, SessionLocal, get_db
from sqlalchemy.orm import Session

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from JWT token.
    Raises 401 if token is invalid or user not found.
    """
    token = credentials.credentials
    user_id = verify_access_token(token)
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    
    return user

async def get_optional_user(
    credentials: Optional[HTTPAuthCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Get the current user if authenticated, otherwise return None.
    """
    if not credentials:
        return None
    
    token = credentials.credentials
    user_id = verify_access_token(token)
    
    if not user_id:
        return None
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if user and user.is_active:
        return user
    
    return None
