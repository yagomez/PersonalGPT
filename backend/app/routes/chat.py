"""Chat routes"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    conversation_id: str = None

class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    timestamp: str

@router.post("/message", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """Send a message and get AI response"""
    # TODO: Implement message handling with LangChain
    return {
        "message": "AI response placeholder",
        "conversation_id": request.conversation_id or "new",
        "timestamp": "2026-02-19T00:00:00Z"
    }

@router.get("/stream")
async def stream_message(conversation_id: str, message: str):
    """Stream AI response (Server-Sent Events)"""
    # TODO: Implement SSE streaming with LangChain
    return {"status": "streaming"}
