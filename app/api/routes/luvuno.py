from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
import os
from datetime import datetime

router = APIRouter()
LUVUNO_PROXY_URL = os.getenv("LUVUNO_PROXY_URL", "https://luvuno-backend-proxy.onrender.com")

@router.get("/status")
async def luvuno_status():
    """Check if the Luvuno proxy is operational."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{LUVUNO_PROXY_URL}/health")
            if response.status_code == 200:
                return {"status": "operational", "detail": response.json()}
            return {"status": "unavailable", "detail": f"Status code: {response.status_code}"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@router.get("/curriculum")
async def fetch_curriculum(grade: str, subject: str, topic: str = None):
    """Fetch curriculum content from Luvuno proxy."""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{LUVUNO_PROXY_URL}/api/curriculum",
                params={"grade": grade, "subject": subject, "topic": topic}
            )
            if response.status_code == 200:
                return {"source": "luvuno", "data": response.json()}
            return {"error": f"Luvuno returned {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}
