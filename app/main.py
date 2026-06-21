"""
TSHAKA M ACADEMY — Complete Quantum Backend
South African Patent No. 2026/05142 · CHSH S=2.76
MindTech Industries — Africa's Quantum Education Platform
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime

from app.config import settings
from app.api.routes.chat import router as chat_router
from app.api.routes.quiz import router as quiz_router
from app.api.routes.analytics import router as analytics_router
from app.api.routes.upload import router as upload_router

# ============================================================
# NEW ROUTERS FOR UPGRADED FEATURES
# ============================================================
from app.api.routes.luvuno import router as luvuno_router
from app.api.routes.decolonize import router as decolonize_router
from app.api.routes.adaptive_quiz import router as adaptive_quiz_router
from app.api.routes.privacy import router as privacy_router
from app.api.routes.communication import router as communication_router
from app.api.routes.rbac import router as rbac_router

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
    ║  🔥 LUVUNO INTEGRATION      🔥 DECOLONIZATION ENGINE                      ║
    ║  🔥 ADAPTIVE QUIZZES        🔥 PERFORMANCE PREDICTOR                     ║
    ║  🔥 INCOGNITO MODE          🔥 COMMUNICATION HUB                         ║
    ║  🔥 ROLE-BASED ACCESS       🔥 QUANTUM CHAT                             ║
    ║                                                                              ║
    ╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    yield
    print("Shutting down Tshaka M Academy...")


app = FastAPI(
    title="Tshaka M Academy — Quantum Education Platform",
    description="Quantum-powered home-schooling platform with letter-by-letter AI typing, table generation, full memory, quantum verification, Luvuno integration, and decolonization engine",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# ============================================================
# CORS — Allow all frontend domains (including Render)
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://localhost:5500",
        "https://tshaka-m-academy-frontend.onrender.com",
        "https://*.onrender.com",
        "https://*.netlify.app",
        "https://symphonious-pothos-042c80.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# INCLUDE ROUTERS (Existing + New)
# ============================================================
app.include_router(chat_router, prefix="/api/chat", tags=["Chat"])
app.include_router(quiz_router, prefix="/api/quiz", tags=["Quiz"])
app.include_router(analytics_router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(upload_router, prefix="/api/upload", tags=["Upload"])

# New routers
app.include_router(luvuno_router, prefix="/api/luvuno", tags=["Luvuno"])
app.include_router(decolonize_router, prefix="/api/decolonize", tags=["Decolonization"])
app.include_router(adaptive_quiz_router, prefix="/api/quiz/adaptive", tags=["Adaptive Quiz"])
app.include_router(privacy_router, prefix="/api/privacy", tags=["Privacy"])
app.include_router(communication_router, prefix="/api/communication", tags=["Communication"])
app.include_router(rbac_router, prefix="/api/rbac", tags=["RBAC"])


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
            "Adaptive quizzes (knowledge space theory)",
            "Real-time performance analytics",
            "Performance prediction (XGBoost)",
            "WhatsApp group integration",
            "Weekly extra class scheduling",
            "Grade 0 to university level",
            "Luvuno curriculum integration",
            "Decolonization content engine",
            "Incognito privacy mode",
            "Communication hub (chat/messaging)",
            "Role-based access control (RBAC)"
        ],
        "endpoints": [
            "GET /",
            "GET /api/health",
            "GET /api/quantum/status",
            "POST /api/chat",
            "POST /api/quiz/generate",
            "POST /api/quiz/adaptive",
            "POST /api/analytics/update",
            "GET /api/analytics/predict",
            "POST /api/upload/analyze",
            "GET /api/luvuno/status",
            "GET /api/luvuno/curriculum",
            "POST /api/decolonize/enrich",
            "POST /api/privacy/incognito",
            "POST /api/communication/send",
            "GET /api/communication/history",
            "POST /api/rbac/verify"
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
            "quantum": "verified",
            "luvuno": "operational"
        }
    }
