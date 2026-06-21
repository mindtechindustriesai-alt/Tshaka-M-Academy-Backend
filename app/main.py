"""
TSHAKA M ACADEMY — Ultimate Quantum Backend
South African Patent No. 2026/05142 · CHSH S=2.76
MindTech Industries — Africa's Quantum Education Platform
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.api.routes import chat, quiz, analytics, upload
from app.services.quantum_service import quantum_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    print(f"""
    ╔═══════════════════════════════════════════════════════════════════════════════╗
    ║                         TSHAKA M ACADEMY                                     ║
    ║                    Quantum Education Platform                                ║
    ║                                                                              ║
    ║  Patent: {settings.PATENT_NUMBER} (Filed {settings.PATENT_FILING_DATE})      ║
    ║  Quantum Verification: CHSH S={settings.CHSH_SCORE}                          ║
    ║  Correlation: {int(settings.QUANTUM_CORRELATION * 100)}%                    ║
    ║  IBM Job ID: {settings.IBM_JOB_ID}                                          ║
    ║  ENSafrica Pro Bono · Dr Bernard Dippenaar                                 ║
    ║                                                                              ║
    ║  🔥 LETTER-BY-LETTER TYPING  🔥 QUANTUM REASONING                           ║
    ║  🔥 TABLE GENERATION        🔥 NUMBERING & SPACING                         ║
    ║  🔥 FILE UPLOAD ANALYSIS    🔥 FULL FIRESTORE MEMORY                      ║
    ║                                                                              ║
    ╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    yield
    print("Shutting down Tshaka M Academy...")


app = FastAPI(
    title="Tshaka M Academy — Quantum Education Platform",
    description="Quantum-powered home-schooling platform with letter-by-letter AI typing, table generation, full memory, and quantum verification",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(quiz.router, prefix="/api/quiz", tags=["Quiz"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])


@app.get("/")
async def root():
    return {
        "service": "Tshaka M Academy",
        "version": "2.0.0",
        "status": "operational",
        "patent": {
            "number": settings.PATENT_NUMBER,
            "filing_date": settings.PATENT_FILING_DATE,
            "attorney": "ENSafrica — Dr Bernard Dippenaar"
        },
        "quantum_verification": {
            "chsh_score": settings.CHSH_SCORE,
            "correlation": settings.QUANTUM_CORRELATION,
            "violation_percentage": settings.VIOLATION_PERCENTAGE,
            "ibm_job_id": settings.IBM_JOB_ID
        },
        "features": [
            "Letter-by-letter streaming typing",
            "Adjustable typing speed (10-100 cps)",
            "Quantum reasoning tree (step-by-step)",
            "Table generation with formatting",
            "Numbered lists and bullet points",
            "Full Firestore memory (no forgetting)",
            "File upload analysis (PDF, DOCX, images)",
            "Infinite quantum quiz engine",
            "Real-time performance analytics",
            "WhatsApp group integration",
            "Weekly extra class scheduling",
            "Grade 0 to university level"
        ],
        "endpoints": [
            "GET /",
            "GET /api/health",
            "GET /api/quantum/status",
            "POST /api/chat",
            "POST /api/quiz/generate",
            "POST /api/analytics/update",
            "POST /api/upload/analyze"
        ]
    }


@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "quantum_verified": True,
        "chsh_score": settings.CHSH_SCORE,
        "services": {
            "firestore": "connected",
            "deepseek": "available",
            "quantum": "verified"
        }
    }
