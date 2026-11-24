from typing import List, Dict, Any
from app.services.swiss_ephemeris import swe_engine
from app.services.nakshatra import get_nakshatra_info, get_rashi_info
from app.utils.time_conversion import degree_to_dms

PLANET_ORDER = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu", "Uranus", "Neptune", "Pluto"]

# 2-letter sign abbreviations used in Parashara's Light and Jagannatha Hora
SIGN_ABBR = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]

# Combustion orb thresholds in degrees from Sun
COMBUSTION_ORBS = {
    "Moon": 12.0,
    "Mars": 17.0,
    "Mercury": 14.0,       # 12.0 if retrograde
    "Jupiter": 11.0,
    "Venus": 10.0,         # 8.0 if retrograde
    "Saturn": 15.0,
}

# Exaltation and Debilitation Rashis (1-indexed: 1=Aries, 2=Taurus...)
EXALTATION_SIGNS = {
    "Sun": 1,        # Aries
    "Moon": 2,       # Taurus
    "Mars": 10,      # Capricorn
    "Mercury": 6,    # Virgo
    "Jupiter": 4,    # Cancer
    "Venus": 12,     # Pisces
    "Saturn": 7,     # Libra
    "Rahu": 2,       # Taurus
    "Ketu": 8,       # Scorpio
}

DEBILITATION_SIGNS = {
    "Sun": 7,        # Libra
    "Moon": 8,       # Scorpio
    "Mars": 4,       # Cancer
    "Mercury": 12,   # Pisces
    "Jupiter": 10,   # Capricorn
    "Venus": 6,      # Virgo
    "Saturn": 1,     # Aries
    "Rahu": 8,       # Scorpio
    "Ketu": 2,       # Taurus
}

OWN_SIGNS = {
    "Sun": [5],            # Leo
    "Moon": [4],           # Cancer
    "Mars": [1, 8],        # Aries, Scorpio
    "Mercury": [3, 6],     # Gemini, Virgo
    "Jupiter": [9, 12],    # Sagittarius, Pisces
    "Venus": [2, 7],       # Taurus, Libra
    "Saturn": [10, 11],    # Capricorn, Aquarius
}

# Natural friendships (Mitra, Shatru, Sama)
NATURAL_FRIENDS = {
    "Sun": {"friends": ["Moon", "Mars", "Jupiter"], "enemies": ["Venus", "Saturn"], "neutral": ["Mercury"]},
    "Moon": {"friends": ["Sun", "Mercury"], "enemies": [], "neutral": ["Mars", "Jupiter", "Venus", "Saturn"]},
    "Mars": {"friends": ["Sun", "Moon", "Jupiter"], "enemies": ["Mercury"], "neutral": ["Venus", "Saturn"]},
    "Mercury": {"friends": ["Sun", "Venus"], "enemies": ["Moon"], "neutral": ["Mars", "Jupiter", "Saturn"]},
    "Jupiter": {"friends": ["Sun", "Moon", "Mars"], "enemies": ["Mercury", "Venus"], "neutral": ["Saturn"]},
    "Venus": {"friends": ["Mercury", "Saturn"], "enemies": ["Sun", "Moon"], "neutral": ["Mars", "Jupiter"]},
    "Saturn": {"friends": ["Mercury", "Venus"], "enemies": ["Sun", "Moon", "Mars"], "neutral": ["Jupiter"]},
}

class PlanetaryPositionService:
    def __init__(self, engine=None):
        self.engine = engine or swe_engine

    def calculate_all_planets(self, jd_ut: float, lagna_rashi_num: int, node_type: str = "TRUE_NODE") -> List[Dict[str, Any]]:
        results = []
        sun_long = None

        # First calculate Sun to determine combustion of other planets
        sun_data = self.engine.calculate_planet(jd_ut, "Sun", sidereal=True)
        sun_long = sun_data["longitude"]

        for planet_name in PLANET_ORDER:
            p_calc = self.engine.calculate_planet(jd_ut, planet_name, sidereal=True, node_type=node_type)
            p_tropical = self.engine.calculate_planet(jd_ut, planet_name, sidereal=False, node_type=node_type)
            
            sid_long = p_calc["longitude"]
            rashi_info = get_rashi_info(sid_long)
            nak_info = get_nakshatra_info(sid_long)
            
            # House placement in Whole Sign system (1 to 12)
            house = ((rashi_info["number"] - lagna_rashi_num) % 12) + 1

            # Check combustion
            is_combust = False
            if planet_name in COMBUSTION_ORBS and sun_long is not None:
                diff = abs(sid_long - sun_long) % 360.0
                if diff > 180.0:
                    diff = 360.0 - diff
                orb = COMBUSTION_ORBS[planet_name]
                if p_calc["is_retrograde"] and planet_name in ["Mercury", "Venus"]:
                    orb -= 2.0
                is_combust = diff <= orb

            # Calculate dignity
            dignity = self._calculate_dignity(planet_name, rashi_info["number"], rashi_info["lord"])

            # Format Parashara's Light style: e.g. 16° Le 24' 12"
            s_abbr = SIGN_ABBR[rashi_info["number"] - 1]
            deg_norm = rashi_info["degree_in_rashi"]
            d = int(deg_norm)
            m = int((deg_norm - d) * 60)
            s = int(round(((deg_norm - d) * 60 - m) * 60))
            if s >= 60:
                s = 0
                m += 1
            if m >= 60:
                m = 0
                d += 1
            parashara_dms = f"{d:02d}° {s_abbr} {m:02d}' {s:02d}\""

            results.append({
                "name": planet_name,
                "id": p_calc["id"],
                "sidereal_longitude": sid_long,
                "tropical_longitude": p_tropical["longitude"],
                "latitude": p_calc["latitude"],
                "speed": p_calc["speed_longitude"],
                "is_retrograde": p_calc["is_retrograde"],
                "rashi": rashi_info["name"],
                "rashi_number": rashi_info["number"],
                "rashi_lord": rashi_info["lord"],
                "degree_in_rashi": rashi_info["degree_in_rashi"],
                "dms": degree_to_dms(rashi_info["degree_in_rashi"]),
                "parashara_dms": parashara_dms,
                "chara_karaka": "-",
                "nakshatra": nak_info["name"],
                "nakshatra_number": nak_info["number"],
                "pada": nak_info["pada"],
                "nakshatra_lord": nak_info["lord"],
                "house": house,
                "is_combust": is_combust,
                "dignity": dignity,
            })

        # Calculate 7 Jaimini Chara Karakas (AK, AmK, BK, MK, PK, GK, DK)
        # Prominently displayed in Parashara's Light for the 7 physical grahas
        chara_candidates = [p for p in results if p["name"] in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]]
        chara_candidates.sort(key=lambda x: x["degree_in_rashi"], reverse=True)
        
        karaka_titles = ["AK", "AmK", "BK", "MK", "PK", "GK", "DK"]
        for idx, p_candidate in enumerate(chara_candidates):
            for r in results:
                if r["name"] == p_candidate["name"]:
                    r["chara_karaka"] = karaka_titles[idx]

        return results

    def _calculate_dignity(self, planet: str, rashi_num: int, rashi_lord: str) -> str:
        if planet in EXALTATION_SIGNS and EXALTATION_SIGNS[planet] == rashi_num:
            return "Exalted"
        if planet in DEBILITATION_SIGNS and DEBILITATION_SIGNS[planet] == rashi_num:
            return "Debilitated"
        if planet in OWN_SIGNS and rashi_num in OWN_SIGNS[planet]:
            return "Own Sign"
        
        # Outer planets have no classical dignity
        if planet in ["Uranus", "Neptune", "Pluto"]:
            return "Neutral"
        if planet in ["Rahu", "Ketu"]:
            return "Neutral"

        # Determine friendship based on sign lord
        rel = NATURAL_FRIENDS.get(planet, {})
        if rashi_lord in rel.get("friends", []):
            return "Great Friend"
        elif rashi_lord in rel.get("enemies", []):
            return "Enemy"
        else:
            return "Neutral"

planetary_service = PlanetaryPositionService()
