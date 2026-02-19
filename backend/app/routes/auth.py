"""Updated authentication routes with full implementation"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4

from database import User, UserSettings, get_db
from auth.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
)
from auth.schemas import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    UserResponse,
    CurrentUser,
    UserSettingsResponse,
    UserSettingsUpdate,
)
from auth.dependencies import get_current_user

router = APIRouter()

@router.post("/register", response_model=RegisterResponse)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user"""
    
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == request.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    existing_username = db.query(User).filter(User.username == request.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    user_id = uuid4()
    user = User(
        id=user_id,
        email=request.email,
        username=request.username,
        full_name=request.full_name,
        password_hash=hash_password(request.password),
    )
    db.add(user)
    db.flush()  # Ensure user is created before creating settings
    
    # Create default user settings
    user_settings = UserSettings(
        user_id=user_id,
    )
    db.add(user_settings)
    db.commit()
    db.refresh(user)
    
    # Generate tokens
    access_token = create_access_token(str(user_id))
    refresh_token = create_refresh_token(str(user_id))
    
    return RegisterResponse(
        user=UserResponse.from_orm(user),
        access_token=access_token,
        refresh_token=refresh_token,
    )

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """User login"""
    
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    
    # Generate tokens
    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.from_orm(user),
    )

@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Refresh access token using refresh token"""
    
    # Verify refresh token
    user_id = verify_refresh_token(request.refresh_token)
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
    
    # Verify user still exists and is active
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    
    # Generate new access token
    new_access_token = create_access_token(str(user.id))
    
    return RefreshTokenResponse(
        access_token=new_access_token,
    )

@router.get("/me", response_model=CurrentUser)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return CurrentUser.from_orm(current_user)

@router.get("/settings", response_model=UserSettingsResponse)
async def get_user_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user settings"""
    settings = db.query(UserSettings).filter(
        UserSettings.user_id == current_user.id
    ).first()
    
    if not settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User settings not found",
        )
    
    return UserSettingsResponse.from_orm(settings)

@router.put("/settings", response_model=UserSettingsResponse)
async def update_user_settings(
    request: UserSettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user settings"""
    settings = db.query(UserSettings).filter(
        UserSettings.user_id == current_user.id
    ).first()
    
    if not settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User settings not found",
        )
    
    # Update only provided fields
    update_data = request.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(settings, field, value)
    
    db.commit()
    db.refresh(settings)
    
    return UserSettingsResponse.from_orm(settings)

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Logout user (client should discard tokens)"""
    return {"message": "Successfully logged out"}
