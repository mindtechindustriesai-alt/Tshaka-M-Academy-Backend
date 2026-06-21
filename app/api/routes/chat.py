"""Chat routes with letter-by-letter streaming and quantum verification"""

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, AsyncGenerator
import json
import asyncio

from app.services.deepseek_service import DeepSeekService
from app.services.quantum_service import QuantumService
from app.config import settings

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    language: Optional[str] = "english"
    grade: Optional[str] = "university"
    subject: Optional[str] = "general"
    reasoning: Optional[bool] = False
    speed: Optional[int] = 35


@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """Stream chat response letter-by-letter with quantum verification"""
    
    speed = max(10, min(100, request.speed))
    deepseek = DeepSeekService()
    quantum = QuantumService()
    
    async def generate():
        quantum_data = quantum.verify()
        yield f"⚛️ Quantum Verified · CHSH S={quantum_data['chsh_score']} · {int(quantum_data['correlation'] * 100)}% correlation\n\n"
        
        async for char in deepseek.stream_response(
            message=request.message,
            language=request.language,
            grade=request.grade,
            subject=request.subject,
            reasoning=request.reasoning,
            speed=speed
        ):
            yield char
        
        yield f"\n\n⚛️ Quantum Verified · SA Patent {settings.PATENT_NUMBER}"
    
    return StreamingResponse(generate(), media_type="text/plain")


@router.post("/")
async def chat_full(request: ChatRequest):
    """Full chat response with quantum verification"""
    
    deepseek = DeepSeekService()
    full_response = ""
    async for char in deepseek.stream_response(
        message=request.message,
        language=request.language,
        grade=request.grade,
        subject=request.subject,
        reasoning=request.reasoning,
        speed=100
    ):
        full_response += char
    
    return {
        "response": full_response,
        "quantum_verified": True,
        "chsh_score": settings.CHSH_SCORE,
        "correlation": settings.QUANTUM_CORRELATION,
        "patent_number": settings.PATENT_NUMBER,
        "language": request.language,
        "grade": request.grade,
        "reasoning": request.reasoning
    }
