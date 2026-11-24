from datetime import datetime
import pytest
from app.services.dasha import dasha_service, DASHA_LORDS

def test_vimshottari_total_years_120():
    """Verify sum of all 9 Mahadasha durations is exactly 120 years"""
    total = sum(d["years"] for d in DASHA_LORDS)
    assert abs(total - 120.0) < 1e-5

def test_dasha_calculation_balance():
    """Verify Mahadasha balance calculation at birth"""
    # Ashwini (0 - 13°20', ruled by Ketu with 7 years total)
    # If Moon is at exactly half of Ashwini (6°40' = 6.666667°), balance should be exactly 3.5 years of Ketu
    birth_dt = datetime(2000, 1, 1, 12, 0, 0)
    moon_mid_ashwini = 360.0 / 27.0 / 2.0  # 6.6666667 degrees
    dasha_res = dasha_service.calculate_dasha_timeline(birth_dt, moon_mid_ashwini)
    
    assert dasha_res["starting_mahadasha_lord"] == "Ketu"
    assert abs(dasha_res["balance_years"] - 3.5) < 0.05
    assert len(dasha_res["dashas"]) == 9
    
    # Check that second Mahadasha is Venus with full 20 years
    venus_md = dasha_res["dashas"][1]
    assert venus_md["planet"] == "Venus"
    assert abs(venus_md["duration_years"] - 20.0) < 1e-3
    assert len(venus_md["sub_periods"]) == 9
