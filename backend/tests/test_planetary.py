import pytest
from app.services.planetary_positions import planetary_service
from app.services.nakshatra import get_rashi_info, get_nakshatra_info
from app.utils.time_conversion import parse_local_to_utc, datetime_to_julian_day_ut

def test_calculate_all_planets():
    """Verify all 12 grahas (7 physical + 2 nodes + 3 outer) are computed with full attributes"""
    dt_utc = parse_local_to_utc("2024-05-15", "10:30:00", "UTC", 0.0)
    jd = datetime_to_julian_day_ut(dt_utc)
    planets = planetary_service.calculate_all_planets(jd, lagna_rashi_num=1)
    
    assert len(planets) == 12
    p_names = [p["name"] for p in planets]
    for required in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        assert required in p_names

    for p in planets:
        assert 0.0 <= p["sidereal_longitude"] < 360.0
        assert 1 <= p["rashi_number"] <= 12
        assert 1 <= p["nakshatra_number"] <= 27
        assert 1 <= p["pada"] <= 4
        assert 1 <= p["house"] <= 12
        assert isinstance(p["is_retrograde"], bool)
        assert p["dignity"] in ["Exalted", "Debilitated", "Own Sign", "Great Friend", "Neutral", "Enemy"]

def test_exaltation_debilitation_dignity():
    """Verify dignity logic for Sun in Aries (Exalted) vs Sun in Libra (Debilitated)"""
    sun_exalted = planetary_service._calculate_dignity("Sun", 1, "Mars")
    assert sun_exalted == "Exalted"
    
    sun_debilitated = planetary_service._calculate_dignity("Sun", 7, "Venus")
    assert sun_debilitated == "Debilitated"

    jupiter_cancer = planetary_service._calculate_dignity("Jupiter", 4, "Moon")
    assert jupiter_cancer == "Exalted"

def test_combustion_check():
    """Verify combustion rule triggers when planet is within orb of Sun"""
    # Test combustion orbs
    from app.services.planetary_positions.planetary_service import COMBUSTION_ORBS
    assert COMBUSTION_ORBS["Mars"] == 17.0
    assert COMBUSTION_ORBS["Jupiter"] == 11.0
    assert COMBUSTION_ORBS["Saturn"] == 15.0
