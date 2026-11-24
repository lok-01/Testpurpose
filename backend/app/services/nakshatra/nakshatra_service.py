from typing import Dict, Any

NAKSHATRAS = [
    {"name": "Ashwini", "lord": "Ketu", "deity": "Ashwini Kumaras", "symbol": "Horse's head", "element": "Earth", "guna": "Sattva"},
    {"name": "Bharani", "lord": "Venus", "deity": "Yama", "symbol": "Yoni", "element": "Earth", "guna": "Rajas"},
    {"name": "Krittika", "lord": "Sun", "deity": "Agni", "symbol": "Razor/Flame", "element": "Fire", "guna": "Rajas"},
    {"name": "Rohini", "lord": "Moon", "deity": "Brahma", "symbol": "Chariot/Cart", "element": "Earth", "guna": "Rajas"},
    {"name": "Mrigashira", "lord": "Mars", "deity": "Soma", "symbol": "Deer's head", "element": "Earth", "guna": "Tamas"},
    {"name": "Ardra", "lord": "Rahu", "deity": "Rudra", "symbol": "Teardrop", "element": "Water", "guna": "Tamas"},
    {"name": "Punarvasu", "lord": "Jupiter", "deity": "Aditi", "symbol": "Bow and Quiver", "element": "Water", "guna": "Sattva"},
    {"name": "Pushya", "lord": "Saturn", "deity": "Brihaspati", "symbol": "Cow's udder/Lotus", "element": "Water", "guna": "Tamas"},
    {"name": "Ashlesha", "lord": "Mercury", "deity": "Nagas", "symbol": "Coiled Serpent", "element": "Water", "guna": "Sattva"},
    {"name": "Magha", "lord": "Ketu", "deity": "Pitris", "symbol": "Royal Throne", "element": "Water", "guna": "Tamas"},
    {"name": "Purva Phalguni", "lord": "Venus", "deity": "Bhaga", "symbol": "Front legs of bed", "element": "Water", "guna": "Rajas"},
    {"name": "Uttara Phalguni", "lord": "Sun", "deity": "Aryaman", "symbol": "Back legs of bed", "element": "Fire", "guna": "Rajas"},
    {"name": "Hasta", "lord": "Moon", "deity": "Savitr", "symbol": "Hand/Fist", "element": "Fire", "guna": "Rajas"},
    {"name": "Chitra", "lord": "Mars", "deity": "Tvashtar", "symbol": "Bright Jewel", "element": "Fire", "guna": "Tamas"},
    {"name": "Swati", "lord": "Rahu", "deity": "Vayu", "symbol": "Young shoot/Coral", "element": "Fire", "guna": "Tamas"},
    {"name": "Vishakha", "lord": "Jupiter", "deity": "Indragni", "symbol": "Triumphal Arch", "element": "Fire", "guna": "Sattva"},
    {"name": "Anuradha", "lord": "Saturn", "deity": "Mitra", "symbol": "Lotus/Staff", "element": "Fire", "guna": "Tamas"},
    {"name": "Jyeshtha", "lord": "Mercury", "deity": "Indra", "symbol": "Circular Amulet", "element": "Air", "guna": "Sattva"},
    {"name": "Mula", "lord": "Ketu", "deity": "Nirriti", "symbol": "Tied bunch of roots", "element": "Air", "guna": "Tamas"},
    {"name": "Purva Ashadha", "lord": "Venus", "deity": "Apas", "symbol": "Winnowing fan", "element": "Air", "guna": "Rajas"},
    {"name": "Uttara Ashadha", "lord": "Sun", "deity": "Vishwadevas", "symbol": "Elephant tusk", "element": "Air", "guna": "Sattva"},
    {"name": "Shravana", "lord": "Moon", "deity": "Vishnu", "symbol": "Ear/Three footprints", "element": "Air", "guna": "Rajas"},
    {"name": "Dhanishta", "lord": "Mars", "deity": "Eight Vasus", "symbol": "Drum (Mridanga)", "element": "Ether", "guna": "Tamas"},
    {"name": "Shatabhisha", "lord": "Rahu", "deity": "Varuna", "symbol": "Empty circle/100 healers", "element": "Ether", "guna": "Tamas"},
    {"name": "Purva Bhadrapada", "lord": "Jupiter", "deity": "Aja Ekapada", "symbol": "Two-faced man/Sword", "element": "Ether", "guna": "Sattva"},
    {"name": "Uttara Bhadrapada", "lord": "Saturn", "deity": "Ahirbudhnya", "symbol": "Snake of the deep", "element": "Ether", "guna": "Tamas"},
    {"name": "Revati", "lord": "Mercury", "deity": "Pushan", "symbol": "Fish/Drum", "element": "Ether", "guna": "Sattva"},
]

RASHIS = [
    {"name": "Aries", "sanskrit": "Mesha", "lord": "Mars", "element": "Fire"},
    {"name": "Taurus", "sanskrit": "Vrishabha", "lord": "Venus", "element": "Earth"},
    {"name": "Gemini", "sanskrit": "Mithuna", "lord": "Mercury", "element": "Air"},
    {"name": "Cancer", "sanskrit": "Karka", "lord": "Moon", "element": "Water"},
    {"name": "Leo", "sanskrit": "Simha", "lord": "Sun", "element": "Fire"},
    {"name": "Virgo", "sanskrit": "Kanya", "lord": "Mercury", "element": "Earth"},
    {"name": "Libra", "sanskrit": "Tula", "lord": "Venus", "element": "Air"},
    {"name": "Scorpio", "sanskrit": "Vrishchika", "lord": "Mars", "element": "Water"},
    {"name": "Sagittarius", "sanskrit": "Dhanu", "lord": "Jupiter", "element": "Fire"},
    {"name": "Capricorn", "sanskrit": "Makara", "lord": "Saturn", "element": "Earth"},
    {"name": "Aquarius", "sanskrit": "Kumbha", "lord": "Saturn", "element": "Air"},
    {"name": "Pisces", "sanskrit": "Meena", "lord": "Jupiter", "element": "Water"},
]

def get_nakshatra_info(sidereal_longitude: float) -> Dict[str, Any]:
    """
    Calculates Nakshatra number (1-27), Pada (1-4), Lord, Deity, and characteristics.
    """
    lon = sidereal_longitude % 360.0
    nak_span = 360.0 / 27.0  # 13.33333333 degrees = 13° 20'
    pada_span = nak_span / 4.0  # 3.33333333 degrees = 3° 20'
    
    nak_idx = int(lon // nak_span)
    nak_deg_rem = lon - (nak_idx * nak_span)
    pada = int(nak_deg_rem // pada_span) + 1
    
    nak_data = NAKSHATRAS[nak_idx]
    
    return {
        "number": nak_idx + 1,
        "name": nak_data["name"],
        "lord": nak_data["lord"],
        "pada": pada,
        "deity": nak_data["deity"],
        "symbol": nak_data["symbol"],
        "element": nak_data["element"],
        "guna": nak_data["guna"],
        "degree_in_nakshatra": nak_deg_rem,
        "pada_span": pada_span,
        "total_span": nak_span,
    }

def get_rashi_info(sidereal_longitude: float) -> Dict[str, Any]:
    """
    Calculates Rashi number (1-12), sign name, Sanskrit name, and lord.
    """
    lon = sidereal_longitude % 360.0
    rashi_idx = int(lon // 30.0)
    deg_in_rashi = lon - (rashi_idx * 30.0)
    rashi_data = RASHIS[rashi_idx]
    
    return {
        "number": rashi_idx + 1,
        "name": rashi_data["name"],
        "sanskrit": rashi_data["sanskrit"],
        "lord": rashi_data["lord"],
        "element": rashi_data["element"],
        "degree_in_rashi": deg_in_rashi,
    }
