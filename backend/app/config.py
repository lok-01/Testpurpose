import os
from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = "AstroRize Vedic Research Lab"
    APP_ENV: str = "development"
    PORT: int = 8000
    HOST: str = "127.0.0.1"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./astrorize_lab.db")
    SWE_EPHE_PATH: str = os.getenv("SWE_EPHE_PATH", "./app/ephe")
    DEFAULT_AYANAMSA: str = "LAHIRI"
    DEFAULT_NODE_CALC: str = "TRUE_NODE"
    DEFAULT_HOUSE_SYSTEM: str = "WHOLE_SIGN"
    
    # AI / LLM Configuration
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2:latest")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "ollama")
    LLM_TEMPERATURE: float = 0.2
    LLM_CONTEXT_LENGTH: int = 4096
    AI_FALLBACK_RULE_BASED: bool = True

settings = Settings()
