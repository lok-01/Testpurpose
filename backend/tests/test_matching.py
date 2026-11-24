import pytest
from app.services.kundli_matching import matching_service

def test_ashtakoota_matching_score_range():
    """Verify Ashtakoota total score is calculated between 0 and 36 points"""
    # Test identical Moon positions
    match_same = matching_service.match_charts(
        boy_moon_long=45.0,  # Taurus (Rohini)
        girl_moon_long=45.0, # Taurus (Rohini)
        boy_is_manglik=False,
        girl_is_manglik=False
    )
    assert 0.0 <= match_same["total_score"] <= 36.0
    assert "varna" in match_same
    assert "vashya" in match_same
    assert "tara" in match_same
    assert "yoni" in match_same
    assert "graha_maitri" in match_same
    assert "gana" in match_same
    assert "bhakoot" in match_same
    assert "nadi" in match_same
    assert "recommendation" in match_same
