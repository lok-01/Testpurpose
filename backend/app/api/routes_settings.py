import os
from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import settings
from app.models.birth_profile import BirthProfile, CalculationRecord
from app.models.verification import VerificationCase
from app.services.swiss_ephemeris import swe_engine

router = APIRouter(prefix="/settings", tags=["Engine Settings & Dashboard"])

@router.get("/status")
def get_engine_status():
    ephe_exists = os.path.exists(settings.SWE_EPHE_PATH)
    return {
        "engine_name": "Swiss Ephemeris",
        "engine_version": swe_engine.get_version(),
        "active_ayanamsa": swe_engine.active_ayanamsa,
        "supported_ayanamsas": list(swe_engine.AYANAMSA_MAP.keys()),
        "node_type": swe_engine.node_type,
        "default_house_system": settings.DEFAULT_HOUSE_SYSTEM,
        "ephemeris_path": settings.SWE_EPHE_PATH,
        "ephemeris_files_available": ephe_exists,
        "llm_provider": settings.LLM_PROVIDER,
        "ollama_url": settings.OLLAMA_BASE_URL,
        "ollama_model": settings.OLLAMA_MODEL,
        "rule_based_fallback_active": settings.AI_FALLBACK_RULE_BASED,
    }

@router.post("/update")
def update_engine_settings(
    ayanamsa: str = None,
    node_type: str = None,
    house_system: str = None,
):
    if ayanamsa:
        swe_engine._configure_sidereal(ayanamsa)
    if node_type:
        swe_engine.node_type = node_type
    if house_system:
        settings.DEFAULT_HOUSE_SYSTEM = house_system

    return {
        "message": "Engine settings updated successfully",
        "active_ayanamsa": swe_engine.active_ayanamsa,
        "node_type": swe_engine.node_type,
        "house_system": settings.DEFAULT_HOUSE_SYSTEM,
    }

@router.get("/dashboard-summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    total_profiles = db.query(BirthProfile).count()
    total_calcs = db.query(CalculationRecord).count()
    total_tests = db.query(VerificationCase).count()
    passed_tests = db.query(VerificationCase).filter(VerificationCase.status == "PASSED").count()
    failed_tests = db.query(VerificationCase).filter(VerificationCase.status == "FAILED").count()
    
    recent_profiles = db.query(BirthProfile).order_by(BirthProfile.created_at.desc()).limit(5).all()
    recent_calcs = db.query(CalculationRecord).order_by(CalculationRecord.created_at.desc()).limit(5).all()

    return {
        "engine_name": "Swiss Ephemeris",
        "engine_version": swe_engine.get_version(),
        "active_ayanamsa": swe_engine.active_ayanamsa,
        "ephemeris_available": os.path.exists(settings.SWE_EPHE_PATH),
        "total_birth_charts": total_profiles,
        "total_calculations_run": total_calcs,
        "total_test_cases": total_tests,
        "passed_test_cases": passed_tests,
        "failed_test_cases": failed_tests,
        "recent_profiles": [
            {"id": p.id, "name": p.name, "dob": p.date_of_birth, "tob": p.time_of_birth, "city": p.city}
            for p in recent_profiles
        ],
        "recent_calculations": [
            {"id": c.id, "profile_id": c.profile_id, "type": c.calculation_type, "ayanamsa": c.ayanamsa_used, "date": c.created_at.strftime("%Y-%m-%d %H:%M:%S")}
            for c in recent_calcs
        ],
    }
