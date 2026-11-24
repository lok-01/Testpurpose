import pytest
from app.services.birth_chart import house_service
from app.services.planetary_positions import planetary_service
from app.utils.time_conversion import parse_local_to_utc, datetime_to_julian_day_ut

def test_whole_sign_houses_and_lagna():
    """Verify Lagna and 12 Bhavas calculation in Whole Sign system"""
    dt_utc = parse_local_to_utc("1990-08-15", "06:00:00", "UTC", 0.0)
    jd = datetime_to_julian_day_ut(dt_utc)
    
    planets = planetary_service.calculate_all_planets(jd, lagna_rashi_num=5)
    lagna_sum, houses = house_service.calculate_houses_and_lagna(
        jd, latitude=28.6139, longitude=77.2090, planets=planets, house_system="WHOLE_SIGN"
    )

    assert "lagna_rashi" in lagna_sum
    assert 1 <= lagna_sum["lagna_rashi_number"] <= 12
    assert len(houses) == 12
    
    # Check consecutive sign progression in whole sign
    lagna_num = lagna_sum["lagna_rashi_number"]
    for i, h in enumerate(houses):
        assert h["house_number"] == i + 1
        expected_sign = ((lagna_num - 1 + i) % 12) + 1
        assert h["sign_number"] == expected_sign
        assert isinstance(h["occupants"], list)
        assert isinstance(h["aspecting_planets"], list)

def test_planetary_aspects():
    """Verify classical Vedic special aspects (Mars 4/8, Jupiter 5/9, Saturn 3/10)"""
    mock_planets = [
        {"name": "Mars", "house": 1},
        {"name": "Jupiter", "house": 1},
        {"name": "Saturn", "house": 1},
        {"name": "Sun", "house": 1},
    ]
    # Check aspects cast on 4th house
    aspects_on_4 = house_service._calculate_aspects_on_house(4, mock_planets)
    assert "Mars" in aspects_on_4
    assert "Sun" not in aspects_on_4

    # Check aspects cast on 5th house
    aspects_on_5 = house_service._calculate_aspects_on_house(5, mock_planets)
    assert "Jupiter" in aspects_on_5

    # Check aspects cast on 3rd house
    aspects_on_3 = house_service._calculate_aspects_on_house(3, mock_planets)
    assert "Saturn" in aspects_on_3

    # Check 7th aspect cast by Sun
    aspects_on_7 = house_service._calculate_aspects_on_house(7, mock_planets)
    assert "Sun" in aspects_on_7
