from datetime import datetime
import pytest
from app.services.panchang import panchang_service

def test_daily_panchang_calculation():
    """Verify Panchang engine returns valid astronomical Tithi, Vara, Yoga, and Karana"""
    dt_local = datetime(2024, 4, 8, 12, 0, 0)
    panchang = panchang_service.calculate_panchang(
        dt_local=dt_local,
        latitude=28.6139,
        longitude=77.2090,
        timezone_offset=5.5
    )
    
    assert "tithi" in panchang
    assert 1 <= panchang["tithi_number"] <= 30
    assert panchang["paksha"] in ["Shukla", "Krishna"]
    assert "vara" in panchang
    assert "nakshatra" in panchang
    assert "yoga" in panchang
    assert "karana" in panchang
    assert "sunrise" in panchang
    assert "sunset" in panchang
