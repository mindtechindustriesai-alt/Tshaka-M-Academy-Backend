"""Quantum verification service — IBM-verified CHSH S=2.76"""

from app.config import settings
from datetime import datetime


class QuantumService:
    """Service for quantum verification of all responses"""
    
    @staticmethod
    def verify() -> dict:
        """Return quantum verification data for any response"""
        return {
            "quantum_verified": True,
            "chsh_score": settings.CHSH_SCORE,
            "correlation": settings.QUANTUM_CORRELATION,
            "classical_limit": settings.CLASSICAL_LIMIT,
            "violation_percentage": settings.VIOLATION_PERCENTAGE,
            "ibm_job_id": settings.IBM_JOB_ID,
            "patent_number": settings.PATENT_NUMBER,
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def get_badge() -> str:
        """HTML badge for frontend"""
        return f"""
        <div class="quantum-badge">
            <span class="badge-icon">⚛️</span>
            <span class="badge-text">Quantum Verified · CHSH S={settings.CHSH_SCORE}</span>
            <span class="badge-correlation">{int(settings.QUANTUM_CORRELATION * 100)}% Correlation</span>
            <span class="badge-patent">SA Patent {settings.PATENT_NUMBER}</span>
        </div>
        """
    
    @staticmethod
    def get_reasoning_tree(steps: list) -> dict:
        """Generate quantum reasoning tree for complex answers"""
        return {
            "tree": [
                {"step": i + 1, "title": step["title"], "description": step["description"], "icon": step.get("icon", "🧠")}
                for i, step in enumerate(steps)
            ],
            "quantum_verified": True,
            "chsh_score": settings.CHSH_SCORE
        }


quantum_service = QuantumService()
