"""FastAPI Application Main Entry Point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.routes import auth, chat, conversations
from database.connection import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    # Create database tables if they don't exist
    Base.metadata.create_all(bind=engine)
    print("Database tables initialized")
    print(f"Starting PersonalGPT API ({settings.ENVIRONMENT})")
    yield
    # Shutdown
    print("Shutting down PersonalGPT API")

app = FastAPI(
    title="PersonalGPT API",
    description="Full-stack personalized AI assistant",
    version="0.1.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(conversations.router, prefix="/api/conversations", tags=["Conversations"])

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "version": "0.1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
