from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.birth_profile import BirthProfile
from app.schemas.calculation import (
    DivisionalChartResponse,
    DashaResponse,
    PanchangResponse,
    YogaDetailSchema,
    DoshaDetailSchema,
    AshtakootaMatchingResponse,
)
from app.services.swiss_ephemeris import swe_engine
from app.services.planetary_positions import planetary_service
from app.services.birth_chart import house_service
from app.services.divisional_charts import divisional_service, VARGA_CONFIGS
from app.services.divisional_charts.parashari_varga_engine import parashari_varga_engine
from app.services.dasha import dasha_service
from app.services.panchang import panchang_service
from app.services.yoga import yoga_service
from app.services.dosha import dosha_service
from app.services.kundli_matching import matching_service
from app.services.transit import transit_service
from app.utils.time_conversion import parse_local_to_utc, datetime_to_julian_day_ut

router = APIRouter(prefix="/calculations", tags=["Vedic Calculations"])

def _get_profile_chart_context(
    profile_id: int,
    db: Session,
    ayanamsa: Optional[str] = None,
    node_type: Optional[str] = None,
):
    profile = db.query(BirthProfile).filter(BirthProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Birth profile not found")

    if ayanamsa:
        swe_engine._configure_sidereal(ayanamsa)
    if node_type:
        swe_engine.node_type = node_type.upper()

    dt_utc = parse_local_to_utc(
        profile.date_of_birth,
        profile.time_of_birth,
        profile.timezone_str,
        profile.timezone_offset
    )
    jd_ut = datetime_to_julian_day_ut(dt_utc)
    
    sidereal_asc, cusps, mc, armc = swe_engine.calculate_houses(jd_ut, profile.latitude, profile.longitude)
    lagna_rashi_num = int(sidereal_asc // 30.0) + 1
    planets = planetary_service.calculate_all_planets(
        jd_ut,
        lagna_rashi_num,
        node_type=(node_type.upper() if node_type else swe_engine.node_type),
    )
    lagna_summary, houses = house_service.calculate_houses_and_lagna(
        jd_ut, profile.latitude, profile.longitude, planets
    )
    return profile, dt_utc, jd_ut, sidereal_asc, lagna_rashi_num, planets, houses, lagna_summary

# 1. Divisional Charts (D1 to D60)
@router.get("/divisional/{profile_id}/{varga_key}")
def get_divisional_chart(profile_id: int, varga_key: str, db: Session = Depends(get_db)):
    v_upper = varga_key.upper()
    if v_upper not in VARGA_CONFIGS:
        raise HTTPException(status_code=400, detail=f"Invalid varga: {varga_key}. Supported: {list(VARGA_CONFIGS.keys())}")
    
    _, _, _, sidereal_asc, _, planets, _, _ = _get_profile_chart_context(profile_id, db)
    return divisional_service.generate_divisional_chart(v_upper, sidereal_asc, planets)

# 1b. Full Parashari Varga Worksheet (D1 to D60: Placements, Upagrahas, Vimshopaka, Shadbala, Ashtakavarga, Varnada, Tithi)
@router.get("/varga-full/{profile_id}/{varga_key}")
def get_full_varga_worksheet(
    profile_id: int,
    varga_key: str,
    ayanamsa: Optional[str] = Query("LAHIRI"),
    node_type: Optional[str] = Query("TRUE_NODE"),
    db: Session = Depends(get_db),
):
    v_upper = varga_key.upper()
    if v_upper not in VARGA_CONFIGS:
        raise HTTPException(status_code=400, detail=f"Invalid varga: {varga_key}. Supported: {list(VARGA_CONFIGS.keys())}")

    profile, _, _, sidereal_asc, _, planets, _, _ = _get_profile_chart_context(
        profile_id, db, ayanamsa=ayanamsa, node_type=node_type
    )
    dt_local = datetime.strptime(f"{profile.date_of_birth} {profile.time_of_birth}", "%Y-%m-%d %H:%M:%S")
    return parashari_varga_engine.get_full_varga_worksheet(
        varga_key=v_upper,
        lagna_longitude=sidereal_asc,
        planets=planets,
        dt_local=dt_local,
        latitude=profile.latitude,
        longitude=profile.longitude,
        timezone_offset=profile.timezone_offset,
    )

# 2. Vimshottari Dasha
@router.get("/dasha/{profile_id}", response_model=DashaResponse)
def get_vimshottari_dasha(
    profile_id: int,
    target_date: Optional[str] = Query(None, description="Optional target date YYYY-MM-DD to check current dasha"),
    db: Session = Depends(get_db)
):
    profile, dt_utc, _, _, _, planets, _, _ = _get_profile_chart_context(profile_id, db)
    moon = next(p for p in planets if p["name"] == "Moon")
    
    tgt_dt = datetime.strptime(target_date, "%Y-%m-%d") if target_date else datetime.utcnow()
    birth_dt = datetime.strptime(f"{profile.date_of_birth} {profile.time_of_birth}", "%Y-%m-%d %H:%M:%S")

    return dasha_service.calculate_dasha_timeline(
        birth_datetime=birth_dt,
        moon_sidereal_longitude=moon["sidereal_longitude"],
        target_date=tgt_dt
    )

# 3. Panchang
@router.get("/panchang", response_model=PanchangResponse)
def get_daily_panchang(
    date: str = Query(..., description="Date YYYY-MM-DD"),
    time_str: str = Query("06:00:00", description="Time HH:MM:SS"),
    latitude: float = Query(28.6139, description="Latitude (default: New Delhi)"),
    longitude: float = Query(77.2090, description="Longitude (default: New Delhi)"),
    timezone_offset: float = Query(5.5, description="Timezone offset in hours")
):
    dt_local = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %H:%M:%S")
    return panchang_service.calculate_panchang(dt_local, latitude, longitude, timezone_offset)

# 4. Yogas
@router.get("/yogas/{profile_id}", response_model=List[YogaDetailSchema])
def get_yogas(profile_id: int, db: Session = Depends(get_db)):
    _, _, _, _, _, planets, houses, _ = _get_profile_chart_context(profile_id, db)
    return yoga_service.analyze_yogas(planets, houses)

# 5. Doshas
@router.get("/doshas/{profile_id}", response_model=List[DoshaDetailSchema])
def get_doshas(profile_id: int, db: Session = Depends(get_db)):
    _, _, _, _, lagna_rashi_num, planets, houses, _ = _get_profile_chart_context(profile_id, db)
    return dosha_service.analyze_doshas(planets, houses, lagna_rashi_num)

# 6. Kundli Matching (Ashtakoota 36 points)
@router.get("/matching", response_model=AshtakootaMatchingResponse)
def match_two_profiles(
    boy_profile_id: int = Query(..., description="ID of Boy's profile"),
    girl_profile_id: int = Query(..., description="ID of Girl's profile"),
    db: Session = Depends(get_db)
):
    _, _, _, _, b_lagna, b_planets, b_houses, _ = _get_profile_chart_context(boy_profile_id, db)
    _, _, _, _, g_lagna, g_planets, g_houses, _ = _get_profile_chart_context(girl_profile_id, db)

    b_moon = next(p for p in b_planets if p["name"] == "Moon")
    g_moon = next(p for p in g_planets if p["name"] == "Moon")

    b_doshas = dosha_service.analyze_doshas(b_planets, b_houses, b_lagna)
    g_doshas = dosha_service.analyze_doshas(g_planets, g_houses, g_lagna)

    b_manglik = any(d["name"].startswith("Manglik") and d["is_present"] and not d["is_cancelled"] for d in b_doshas)
    g_manglik = any(d["name"].startswith("Manglik") and d["is_present"] and not d["is_cancelled"] for d in g_doshas)

    return matching_service.match_charts(
        boy_moon_long=b_moon["sidereal_longitude"],
        girl_moon_long=g_moon["sidereal_longitude"],
        boy_is_manglik=b_manglik,
        girl_is_manglik=g_manglik
    )

# 7. Planetary Transits
@router.get("/transits")
def get_transits(
    profile_id: Optional[int] = Query(None, description="Optional profile ID to compute houses from natal Moon & Lagna"),
    transit_date: Optional[str] = Query(None, description="Date YYYY-MM-DD (defaults to now)"),
    db: Session = Depends(get_db)
):
    tgt_dt = datetime.strptime(transit_date, "%Y-%m-%d") if transit_date else datetime.utcnow()
    
    natal_lagna = 1
    natal_moon = 1
    if profile_id:
        _, _, _, _, natal_lagna, planets, _, _ = _get_profile_chart_context(profile_id, db)
        moon_obj = next(p for p in planets if p["name"] == "Moon")
        natal_moon = moon_obj["rashi_number"]

    return transit_service.calculate_transits(tgt_dt, natal_lagna, natal_moon)
