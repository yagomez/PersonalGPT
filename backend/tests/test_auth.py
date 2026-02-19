"""JWT authentication tests"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4

from app.main import app
from database import Base, get_db, User
from auth.security import hash_password

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    """Reset database before each test"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

def test_register_success():
    """Test successful user registration"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "password": "SecurePassword123!"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["email"] == "test@example.com"
    assert data["user"]["username"] == "testuser"
    assert "access_token" in data
    assert "refresh_token" in data

def test_register_duplicate_email():
    """Test registration with duplicate email"""
    # First registration
    client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser1",
            "password": "Password123!"
        }
    )
    
    # Duplicate email
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser2",
            "password": "Password123!"
        }
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_login_success():
    """Test successful login"""
    # Register first
    client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "Password123!"
        }
    )
    
    # Login
    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "Password123!"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

def test_login_invalid_password():
    """Test login with wrong password"""
    # Register first
    client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "CorrectPassword123!"
        }
    )
    
    # Wrong password
    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "WrongPassword123!"
        }
    )
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]

def test_refresh_token():
    """Test token refresh"""
    # Register
    register_response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "Password123!"
        }
    )
    refresh_token = register_response.json()["refresh_token"]
    
    # Refresh
    response = client.post(
        "/api/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

def test_get_current_user():
    """Test getting current user info"""
    # Register
    register_response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "Password123!"
        }
    )
    access_token = register_response.json()["access_token"]
    
    # Get current user
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"

def test_unauthorized_without_token():
    """Test that protected endpoints require authentication"""
    response = client.get("/api/auth/me")
    assert response.status_code == 403
