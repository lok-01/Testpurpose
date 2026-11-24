from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.birth_profile import BirthProfile, CalculationRecord
from app.schemas.calculation import BirthChartResponse
from app.services.swiss_ephemeris import swe_engine
from app.services.planetary_positions import planetary_service
from app.services.birth_chart import house_service
from app.utils.time_conversion import parse_local_to_utc, datetime_to_julian_day_ut

router = APIRouter(prefix="/chart", tags=["Birth Chart (Kundli)"])

@router.get("/calculate/{profile_id}", response_model=BirthChartResponse)
def calculate_birth_chart(
    profile_id: int,
    ayanamsa: Optional[str] = Query("LAHIRI", description="Ayanamsa: LAHIRI, RAMAN, KP, TRUE_CITRA"),
    node_type: Optional[str] = Query("TRUE_NODE", description="TRUE_NODE or MEAN_NODE"),
    house_system: Optional[str] = Query("WHOLE_SIGN", description="WHOLE_SIGN or PLACIDUS"),
    db: Session = Depends(get_db)
):
    profile = db.query(BirthProfile).filter(BirthProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Birth profile not found")

    # Time handling with historical timezone resolution
    dt_utc = parse_local_to_utc(
        profile.date_of_birth,
        profile.time_of_birth,
        profile.timezone_str,
        profile.timezone_offset
    )
    jd_ut = datetime_to_julian_day_ut(dt_utc)

    # Configure Ayanamsa
    swe_engine._configure_sidereal(ayanamsa)
    swe_engine.node_type = node_type

    # Ascendant and Houses
    hsys_code = "W" if house_system == "WHOLE_SIGN" else "P"
    sidereal_asc, cusps, mc, armc = swe_engine.calculate_houses(
        jd_ut, profile.latitude, profile.longitude, hsys=hsys_code
    )
    lagna_rashi_num = int(sidereal_asc // 30.0) + 1

    # Real Swiss Ephemeris Planetary Calculations
    planets = planetary_service.calculate_all_planets(jd_ut, lagna_rashi_num, node_type=node_type)

    # Detailed Houses with Occupants and Aspects
    lagna_summary, houses = house_service.calculate_houses_and_lagna(
        jd_ut, profile.latitude, profile.longitude, planets, house_system=house_system
    )

    result = {
        "chart_summary": lagna_summary,
        "planets": planets,
        "houses": houses,
    }

    # Record calculation history
    calc_record = CalculationRecord(
        profile_id=profile.id,
        calculation_type="D1_BIRTH_CHART",
        engine_version=swe_engine.get_version(),
        ayanamsa_used=ayanamsa,
        input_params={"ayanamsa": ayanamsa, "node_type": node_type, "house_system": house_system},
        result_data=result,
    )
    db.add(calc_record)
    db.commit()

    return result
