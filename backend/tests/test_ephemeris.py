import pytest
import swisseph as swe
from app.services.swiss_ephemeris import swe_engine
from app.utils.time_conversion import parse_local_to_utc, datetime_to_julian_day_ut, degree_to_dms

def test_swiss_ephemeris_version():
    """Verify Swiss Ephemeris is active and reports valid version (>= 2.10)"""
    ver = swe_engine.get_version()
    assert ver is not None
    assert "2.10" in ver

def test_julian_day_calculation():
    """Verify Julian Day calculation against known astronomical epoch (2000-01-01 12:00 UT = JD 2451545.0)"""
    dt_utc = parse_local_to_utc("2000-01-01", "12:00:00", "UTC", 0.0)
    jd = datetime_to_julian_day_ut(dt_utc)
    assert abs(jd - 2451545.0) < 1e-5

def test_lahiri_ayanamsa():
    """Verify Lahiri Ayanamsa for J2000 epoch (~23.85 degrees)"""
    dt_utc = parse_local_to_utc("2000-01-01", "12:00:00", "UTC", 0.0)
    jd = datetime_to_julian_day_ut(dt_utc)
    ayan = swe_engine.get_ayanamsa_ut(jd, "LAHIRI")
    assert 23.8 < ayan < 23.9

def test_sidereal_sun_calculation():
    """Verify Sidereal Sun computation does not crash and returns valid coordinates within [0, 360)"""
    dt_utc = parse_local_to_utc("2024-01-01", "12:00:00", "UTC", 0.0)
    jd = datetime_to_julian_day_ut(dt_utc)
    sun = swe_engine.calculate_planet(jd, "Sun", sidereal=True)
    assert "longitude" in sun
    assert 0.0 <= sun["longitude"] < 360.0
    assert sun["is_retrograde"] is False
    assert sun["name"] == "Sun"

def test_node_ketu_180_degrees_opposite():
    """Verify Ketu is mathematically opposite to Rahu by exactly 180 degrees"""
    dt_utc = parse_local_to_utc("2024-01-01", "12:00:00", "UTC", 0.0)
    jd = datetime_to_julian_day_ut(dt_utc)
    rahu = swe_engine.calculate_planet(jd, "Rahu", sidereal=True)
    ketu = swe_engine.calculate_planet(jd, "Ketu", sidereal=True)
    diff = abs(ketu["longitude"] - rahu["longitude"])
    assert abs(diff - 180.0) < 1e-4 or abs(diff - 180.0 - 360.0) < 1e-4
