import pytest
from app.services.divisional_charts import divisional_service, VARGA_CONFIGS

def test_all_16_vargas_supported():
    """Verify all 16 required Vargas exist in VARGA_CONFIGS"""
    required_vargas = [
        "D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12",
        "D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60"
    ]
    for v in required_vargas:
        assert v in VARGA_CONFIGS

def test_d9_navamsha_mapping():
    """Verify classical Navamsha formula for fire, earth, air, and water signs"""
    # 0° Aries (Fire) -> 1st Navamsha should be Aries (1)
    assert divisional_service.calculate_varga_sign(0.5, "D9") == 1
    # 29° Aries (Fire) -> 9th Navamsha (26°40' - 30°) should be Sagittarius (9)
    assert divisional_service.calculate_varga_sign(29.0, "D9") == 9
    
    # 0° Taurus (Earth) -> 1st Navamsha should start at Capricorn (10)
    assert divisional_service.calculate_varga_sign(30.5, "D9") == 10
    
    # 0° Gemini (Air) -> 1st Navamsha should start at Libra (7)
    assert divisional_service.calculate_varga_sign(60.5, "D9") == 7
    
    # 0° Cancer (Water) -> 1st Navamsha should start at Cancer (4)
    assert divisional_service.calculate_varga_sign(90.5, "D9") == 4

def test_d30_trimshamsha_mapping():
    """Verify BPHS unequal division degree rulers for Trimshamsha"""
    # Odd sign: Aries 0-5° is Mars (Aries / 1)
    assert divisional_service.calculate_varga_sign(2.0, "D30") == 1
    # Odd sign: Aries 5-10° is Saturn (Aquarius / 11)
    assert divisional_service.calculate_varga_sign(7.0, "D30") == 11
    # Odd sign: Aries 10-18° is Jupiter (Sagittarius / 9)
    assert divisional_service.calculate_varga_sign(14.0, "D30") == 9
    # Odd sign: Aries 18-25° is Mercury (Gemini / 3)
    assert divisional_service.calculate_varga_sign(21.0, "D30") == 3
    # Odd sign: Aries 25-30° is Venus (Libra / 7)
    assert divisional_service.calculate_varga_sign(27.0, "D30") == 7

def test_generate_divisional_chart():
    """Verify full divisional chart generation structure"""
    mock_planets = [
        {"name": "Sun", "sidereal_longitude": 248.5},
        {"name": "Moon", "sidereal_longitude": 328.0},
    ]
    d9_chart = divisional_service.generate_divisional_chart("D9", lagna_longitude=65.0, planets=mock_planets)
    assert d9_chart["varga_key"] == "D9"
    assert "lagna_rashi" in d9_chart
    assert len(d9_chart["planets"]) == 2
    assert 1 <= d9_chart["planets"][0]["house"] <= 12
