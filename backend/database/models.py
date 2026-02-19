"""Database models for PersonalGPT"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Float, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid

from database.connection import Base

class User(Base):
    """User account model"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    user_settings = relationship("UserSettings", back_populates="user", uselist=False, cascade="all, delete-orphan")
    api_keys = relationship("APIKey", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"

class UserSettings(Base):
    """User preferences and configuration"""
    __tablename__ = "user_settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True, index=True)
    
    # LLM Preferences
    preferred_model = Column(String(100), default="gpt-4", nullable=False)
    temperature = Column(Float, default=0.7, nullable=False)
    max_tokens = Column(Integer, default=2000, nullable=False)
    
    # Settings
    theme = Column(String(20), default="light", nullable=False)  # light, dark
    language = Column(String(10), default="en", nullable=False)
    timezone = Column(String(50), default="UTC", nullable=False)
    email_notifications = Column(Boolean, default=True)
    
    # Advanced
    custom_instructions = Column(Text, nullable=True)
    search_history_enabled = Column(Boolean, default=True)
    data_retention_days = Column(Integer, default=90)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="user_settings")

    def __repr__(self):
        return f"<UserSettings {self.user_id}>"

class Conversation(Base):
    """Conversation/Chat thread"""
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=True)  # Auto-generated from first message if null
    summary = Column(Text, nullable=True)
    
    # Context
    system_prompt = Column(Text, nullable=True)
    model_used = Column(String(100), default="gpt-4")
    temperature = Column(Float, default=0.7)
    
    # Status
    is_archived = Column(Boolean, default=False, index=True)
    is_pinned = Column(Boolean, default=False)
    
    # Metadata
    message_count = Column(Integer, default=0)
    token_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Conversation {self.id} - {self.title}>"

class Message(Base):
    """Individual message in a conversation"""
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False, index=True)
    
    # Content
    role = Column(String(20), nullable=False)  # "user", "assistant", "system"
    content = Column(Text, nullable=False)
    
    # Metadata
    token_count = Column(Integer, default=0)
    model_response = Column(Boolean, default=False)  # Whether this is an AI response
    
    # Embeddings (for semantic search)
    # Note: actual embeddings stored in Chroma, but keeping reference
    embedding_id = Column(String(255), nullable=True, index=True)
    
    # Feedback
    is_liked = Column(Boolean, nullable=True)  # None = not rated, True = liked, False = disliked
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")

    def __repr__(self):
        return f"<Message {self.id} - {self.role}>"

class APIKey(Base):
    """User API keys for extension/external access"""
    __tablename__ = "api_keys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    name = Column(String(255), nullable=False)
    key_hash = Column(String(255), nullable=False, unique=True)
    
    # Permissions (stored as JSON)
    permissions = Column(JSONB, default=dict, nullable=False)  # e.g., {"read": True, "write": True}
    
    # Rate limiting
    rate_limit_requests = Column(Integer, default=100)  # requests per minute
    rate_limit_window = Column(Integer, default=60)  # seconds
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    last_used_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)  # None = never expires

    # Relationships
    user = relationship("User", back_populates="api_keys")

    def __repr__(self):
        return f"<APIKey {self.name}>"

class ConversationMetadata(Base):
    """Extended metadata and tags for conversations"""
    __tablename__ = "conversation_metadata"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False, unique=True, index=True)
    
    # Tags for organization
    tags = Column(JSON, default=list, nullable=False)  # e.g., ["important", "project-x"]
    
    # Custom metadata
    custom_data = Column(JSONB, default=dict, nullable=False)
    
    # Analytics
    session_duration_seconds = Column(Integer, nullable=True)
    user_satisfaction_score = Column(Float, nullable=True)  # 1-5 scale
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<ConversationMetadata {self.conversation_id}>"

class SessionLog(Base):
    """Session tracking for analytics"""
    __tablename__ = "session_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    session_token = Column(String(255), unique=True, nullable=False)
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    user_agent = Column(String(500), nullable=True)
    
    started_at = Column(DateTime, default=datetime.utcnow, index=True)
    ended_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SessionLog {self.user_id} - {self.started_at}>"
