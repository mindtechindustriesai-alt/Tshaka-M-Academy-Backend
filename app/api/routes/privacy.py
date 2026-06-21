from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from datetime import datetime
from app.services.firestore_service import db

router = APIRouter()

@router.post("/incognito")
async def enable_incognito(request: Request):
    """Enable incognito mode for a student."""
    body = await request.json()
    student_id = body.get("student_id")
    reason = body.get("reason", "privacy")

    if not student_id:
        return JSONResponse(status_code=400, content={"error": "Student ID required"})

    anonymous_id = f"anon_{student_id[:8]}_{int(datetime.now().timestamp())}"
    
    if db:
        db.collection('incognito_sessions').add({
            'student_id': student_id,
            'anonymous_id': anonymous_id,
            'reason': reason,
            'timestamp': datetime.now().isoformat(),
            'active': True
        })

    return {
        "anonymous_id": anonymous_id,
        "student_id": student_id,
        "active": True,
        "timestamp": datetime.now().isoformat()
    }
