from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from datetime import datetime
from app.services.firestore_service import db

router = APIRouter()

@router.post("/send")
async def send_message(request: Request):
    """Send a message between users."""
    body = await request.json()
    sender_id = body.get("sender_id")
    receiver_id = body.get("receiver_id")
    message = body.get("message")
    message_type = body.get("type", "direct")

    if not sender_id or not receiver_id or not message:
        return JSONResponse(status_code=400, content={"error": "Sender, receiver, and message required"})

    msg_data = {
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "message": message,
        "type": message_type,
        "timestamp": datetime.now().isoformat(),
        "read": False
    }

    if db:
        db.collection('messages').add(msg_data)

    return {"status": "sent", "timestamp": msg_data["timestamp"]}

@router.get("/history")
async def get_history(user_id: str, other_user_id: str, limit: int = 50):
    """Get chat history between two users."""
    if not user_id or not other_user_id:
        return JSONResponse(status_code=400, content={"error": "Both user IDs required"})

    if db:
        messages = db.collection('messages').where('sender_id', 'in', [user_id, other_user_id]).where('receiver_id', 'in', [user_id, other_user_id]).order_by('timestamp', direction='DESCENDING').limit(limit).get()
        return [m.to_dict() for m in messages]
    
    return []
