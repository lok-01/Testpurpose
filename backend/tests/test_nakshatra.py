import pytest
from app.services.nakshatra import get_nakshatra_info, get_rashi_info, NAKSHATRAS

def test_27_nakshatras_definitions():
    """Verify all 27 classical Nakshatras exist with lords and deities"""
    assert len(NAKSHATRAS) == 27
    assert NAKSHATRAS[0]["name"] == "Ashwini"
    assert NAKSHATRAS[0]["lord"] == "Ketu"
    assert NAKSHATRAS[26]["name"] == "Revati"
    assert NAKSHATRAS[26]["lord"] == "Mercury"

def test_nakshatra_and_pada_spans():
    """Verify exact degree boundaries for Nakshatras and Padas (13°20' and 3°20')"""
    # 0.0° Aries is Ashwini Pada 1
    nak0 = get_nakshatra_info(0.5)
    assert nak0["name"] == "Ashwini"
    assert nak0["pada"] == 1
    assert nak0["lord"] == "Ketu"

    # 4.0° Aries is Ashwini Pada 2 (3°20' to 6°40')
    nak_pada2 = get_nakshatra_info(4.0)
    assert nak_pada2["name"] == "Ashwini"
    assert nak_pada2["pada"] == 2

    # 13.5° Aries is Bharani Pada 1 (13°20' to 16°40')
    nak_bharani = get_nakshatra_info(13.5)
    assert nak_bharani["name"] == "Bharani"
    assert nak_bharani["pada"] == 1
    assert nak_bharani["lord"] == "Venus"

def test_rashi_spans():
    """Verify exact 30° bounds for Rashis"""
    r_aries = get_rashi_info(15.0)
    assert r_aries["name"] == "Aries"
    assert r_aries["number"] == 1

    r_pisces = get_rashi_info(345.0)
    assert r_pisces["name"] == "Pisces"
    assert r_pisces["number"] == 12
