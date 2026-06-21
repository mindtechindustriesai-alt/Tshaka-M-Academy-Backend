"""Application configuration"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings"""
    
    # Server
    ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
    PORT = int(os.getenv("PORT", 8000))
    HOST = os.getenv("HOST", "0.0.0.0")
    
    # API Keys
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    
    # CORS
    CORS_ORIGINS = [
        "http://localhost:8000",
        "http://localhost:5500",
        "https://*.onrender.com",
        "https://*.netlify.app",
        "https://tshaka-m-academy.netlify.app"
    ]
    
    # Firebase
    FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "mindflow-ai-education")
    FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY", "AIzaSyD5OB59lG6bAsmQ7A97zXP_MfQ5AM3BYaw")
    
    # Quantum Constants (IBM Verified)
    CHSH_SCORE = float(os.getenv("CHSH_SCORE", 2.76))
    QUANTUM_CORRELATION = float(os.getenv("QUANTUM_CORRELATION", 0.984))
    CLASSICAL_LIMIT = 2.0
    QUANTUM_LIMIT = 2.828
    VIOLATION_PERCENTAGE = int(os.getenv("VIOLATION_PERCENTAGE", 38))
    IBM_JOB_ID = os.getenv("IBM_JOB_ID", "d55p3jgnsj9s73b32lj0")
    
    # Patent
    PATENT_NUMBER = os.getenv("PATENT_NUMBER", "2026/05142")
    PATENT_FILING_DATE = os.getenv("PATENT_FILING_DATE", "2026-05-12")
    
    # Typing defaults
    DEFAULT_TYPING_SPEED = int(os.getenv("DEFAULT_TYPING_SPEED", 35))
    MIN_TYPING_SPEED = 10
    MAX_TYPING_SPEED = 100
    
    # Language Support
    SUPPORTED_LANGUAGES = ["english", "zulu", "xhosa", "shona"]
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", 200))
    RATE_LIMIT_PERIOD = int(os.getenv("RATE_LIMIT_PERIOD", 60))
    
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"


settings = Settings()
