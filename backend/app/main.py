from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base, SessionLocal
from app.api import (
    profile_router,
    chart_router,
    calculations_router,
    ai_router,
    verification_router,
    settings_router,
)
from app.services.verification import verification_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database tables
    Base.metadata.create_all(bind=engine)
    # Seed default verification test cases if empty
    db = SessionLocal()
    try:
        verification_service.seed_default_benchmarks(db)
    finally:
        db.close()
    yield

app = FastAPI(
    title="AstroRize Vedic Research Lab API",
    description="Astronomical calculation engine powered by Swiss Ephemeris with Parashari Vedic Astrology Algorithms & Grounded AI Chatbot.",
    version="1.0.0",
    lifespan=lifespan,
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers under /api
app.include_router(profile_router, prefix="/api")
app.include_router(chart_router, prefix="/api")
app.include_router(calculations_router, prefix="/api")
app.include_router(ai_router, prefix="/api")
app.include_router(verification_router, prefix="/api")
app.include_router(settings_router, prefix="/api")

@app.get("/")
def root():
    return {
        "app": settings.APP_NAME,
        "engine": "Swiss Ephemeris",
        "status": "Operational",
        "docs_url": "/docs",
    }
