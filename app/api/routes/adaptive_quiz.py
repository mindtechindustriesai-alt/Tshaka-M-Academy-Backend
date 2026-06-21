from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from datetime import datetime
from app.services.firestore_service import db

router = APIRouter()

@router.post("/")
async def adaptive_quiz(request: Request):
    """Generate an adaptive quiz based on student performance."""
    body = await request.json()
    student_id = body.get("student_id")
    subject = body.get("subject")
    topic = body.get("topic")

    if not student_id or not subject:
        return JSONResponse(status_code=400, content={"error": "Student ID and subject required"})

    # Get student performance from Firestore
    student_level = "beginner"
    if db:
        performance = db.collection('student_performance').where('student_id', '==', student_id).where('subject', '==', subject).order_by('timestamp', direction='DESCENDING').limit(10).get()
        if performance:
            scores = [p.to_dict().get('score', 0) for p in performance]
            avg_score = sum(scores) / len(scores) if scores else 0
            if avg_score >= 80:
                student_level = "advanced"
            elif avg_score >= 50:
                student_level = "intermediate"

    quiz = {
        "student_id": student_id,
        "subject": subject,
        "topic": topic or "General",
        "level": student_level,
        "questions": generate_questions(subject, topic, student_level),
        "timestamp": datetime.now().isoformat()
    }

    if db:
        db.collection('adaptive_quizzes').add(quiz)

    return quiz

def generate_questions(subject, topic, level):
    """Generate questions based on subject, topic, and level."""
    # Placeholder - in production, this would pull from Luvuno or a question bank
    return [
        {
            "question": f"Sample {subject} question for {level} level",
            "options": ["A", "B", "C", "D"],
            "correct": "A",
            "explanation": "This is a placeholder explanation."
        }
    ]
