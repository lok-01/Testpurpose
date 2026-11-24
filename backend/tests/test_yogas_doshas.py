import pytest
from app.services.yoga import yoga_service
from app.services.dosha import dosha_service

def test_gaja_kesari_yoga_detection():
    """Verify Gaja Kesari Yoga triggered when Jupiter in Kendra from Moon"""
    mock_planets = [
        {"name": "Moon", "house": 1, "sidereal_longitude": 30.0, "dignity": "Own Sign", "is_combust": False},
        {"name": "Jupiter", "house": 4, "sidereal_longitude": 120.0, "dignity": "Exalted", "is_combust": False},
    ]
    mock_houses = [{"house_number": i, "sign_lord": "Jupiter"} for i in range(1, 13)]
    
    yogas = yoga_service.analyze_yogas(mock_planets, mock_houses)
    gk = next((y for y in yogas if y["name"] == "Gaja Kesari Yoga"), None)
    assert gk is not None
    assert gk["is_present"] is True
    assert gk["is_cancelled"] is False

def test_manglik_dosha_and_cancellation():
    """Verify Manglik Dosha detects Mars in 7th house and evaluates cancellations"""
    # Mars in 7th house in Capricorn (Exalted -> cancelled)
    mock_planets = [
        {"name": "Mars", "house": 7, "sidereal_longitude": 280.0, "rashi": "Capricorn", "dignity": "Exalted", "is_combust": False},
        {"name": "Sun", "house": 1, "sidereal_longitude": 10.0, "rashi": "Aries", "dignity": "Exalted", "is_combust": False},
    ]
    mock_houses = [{"house_number": i, "sign_lord": "Mars", "occupants": []} for i in range(1, 13)]
    
    doshas = dosha_service.analyze_doshas(mock_planets, mock_houses, lagna_rashi_num=1)
    manglik = next((d for d in doshas if "Manglik" in d["name"]), None)
    assert manglik is not None
    assert manglik["is_present"] is True
    assert manglik["is_cancelled"] is True  # Dignified in Exaltation
