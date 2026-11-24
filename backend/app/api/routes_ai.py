from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.birth_profile import BirthProfile
from app.services.ai_chat import ai_chat_service
from app.services.swiss_ephemeris import swe_engine
from app.services.planetary_positions import planetary_service
from app.services.birth_chart import house_service
from app.services.yoga import yoga_service
from app.services.dosha import dosha_service
from app.services.dasha import dasha_service
from app.utils.time_conversion import parse_local_to_utc, datetime_to_julian_day_ut
from datetime import datetime

router = APIRouter(prefix="/ai", tags=["AI Astrology Chat"])

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    profile_id: int
    message: str
    conversation_history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    response: str
    source: str
    model: str
    provider: str
    grounded_context: str

@router.post("/chat", response_model=ChatResponse)
def chat_with_astrologer(request: ChatRequest, db: Session = Depends(get_db)):
    profile = db.query(BirthProfile).filter(BirthProfile.id == request.profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Birth profile not found")

    # Retrieve real calculated chart data
    dt_utc = parse_local_to_utc(
        profile.date_of_birth,
        profile.time_of_birth,
        profile.timezone_str,
        profile.timezone_offset
    )
    jd_ut = datetime_to_julian_day_ut(dt_utc)
    
    sidereal_asc, cusps, mc, armc = swe_engine.calculate_houses(jd_ut, profile.latitude, profile.longitude)
    lagna_rashi_num = int(sidereal_asc // 30.0) + 1
    planets = planetary_service.calculate_all_planets(jd_ut, lagna_rashi_num)
    lagna_summary, houses = house_service.calculate_houses_and_lagna(
        jd_ut, profile.latitude, profile.longitude, planets
    )
    yogas = yoga_service.analyze_yogas(planets, houses)
    doshas = dosha_service.analyze_doshas(planets, houses, lagna_rashi_num)
    
    moon_p = next(p for p in planets if p["name"] == "Moon")
    birth_dt = datetime.strptime(f"{profile.date_of_birth} {profile.time_of_birth}", "%Y-%m-%d %H:%M:%S")
    dashas = dasha_service.calculate_dasha_timeline(birth_dt, moon_p["sidereal_longitude"])

    chart_data = {
        "chart_summary": lagna_summary,
        "planets": planets,
        "houses": houses,
        "yogas": yogas,
        "doshas": doshas,
        "dashas": dashas,
    }

    history_dicts = [{"role": m.role, "content": m.content} for m in request.conversation_history]
    
    return ai_chat_service.generate_chat_response(
        user_message=request.message,
        conversation_history=history_dicts,
        chart_data=chart_data
    )
