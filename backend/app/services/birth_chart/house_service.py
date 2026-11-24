from typing import List, Dict, Any, Tuple
from app.services.swiss_ephemeris import swe_engine
from app.services.nakshatra import get_rashi_info, get_nakshatra_info, RASHIS
from app.utils.time_conversion import degree_to_dms

class HouseService:
    def __init__(self, engine=None):
        self.engine = engine or swe_engine

    def calculate_houses_and_lagna(
        self,
        jd_ut: float,
        latitude: float,
        longitude: float,
        planets: List[Dict[str, Any]],
        house_system: str = "WHOLE_SIGN"
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Calculates Ascendant (Lagna) and 12 Bhavas/Houses with occupants and aspects.
        """
        hsys_code = "W" if house_system == "WHOLE_SIGN" else "P"
        sidereal_asc, cusps, mc, armc = self.engine.calculate_houses(jd_ut, latitude, longitude, hsys=hsys_code)
        
        asc_rashi = get_rashi_info(sidereal_asc)
        asc_nak = get_nakshatra_info(sidereal_asc)
        
        SIGN_ABBR = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]
        s_abbr = SIGN_ABBR[asc_rashi["number"] - 1]
        deg_norm = asc_rashi["degree_in_rashi"]
        d = int(deg_norm)
        m = int((deg_norm - d) * 60)
        s = int(round(((deg_norm - d) * 60 - m) * 60))
        if s >= 60:
            s = 0
            m += 1
        if m >= 60:
            m = 0
            d += 1
        parashara_asc_dms = f"{d:02d}° {s_abbr} {m:02d}' {s:02d}\""

        lagna_summary = {
            "lagna_longitude": sidereal_asc,
            "lagna_rashi": asc_rashi["name"],
            "lagna_rashi_number": asc_rashi["number"],
            "lagna_degree": asc_rashi["degree_in_rashi"],
            "lagna_dms": degree_to_dms(asc_rashi["degree_in_rashi"]),
            "lagna_parashara_dms": parashara_asc_dms,
            "lagna_lord": asc_rashi["lord"],
            "lagna_nakshatra": asc_nak["name"],
            "lagna_pada": asc_nak["pada"],
            "ayanamsa_value": self.engine.get_ayanamsa_ut(jd_ut),
            "ayanamsa_name": self.engine.active_ayanamsa,
            "engine_name": "Swiss Ephemeris",
            "engine_version": self.engine.get_version(),
        }

        # Build 12 houses
        houses = []
        for h_num in range(1, 13):
            # In Whole Sign, house N sign is (Lagna Sign - 1 + N - 1) % 12
            sign_idx = (asc_rashi["number"] - 1 + h_num - 1) % 12
            sign_data = RASHIS[sign_idx]
            
            start_deg = sign_idx * 30.0
            cusp_deg = (start_deg + 15.0) if house_system == "WHOLE_SIGN" else cusps[h_num - 1]
            
            # Find planets occupying this house
            occupants = [p["name"] for p in planets if p["house"] == h_num]
            
            # Find planets casting an aspect on this house
            aspects = self._calculate_aspects_on_house(h_num, planets)

            houses.append({
                "house_number": h_num,
                "sign": sign_data["name"],
                "sign_number": sign_idx + 1,
                "sign_lord": sign_data["lord"],
                "start_degree": start_deg,
                "cusp_degree": cusp_deg,
                "occupants": occupants,
                "aspecting_planets": aspects,
            })

        return lagna_summary, houses

    def _calculate_aspects_on_house(self, target_house: int, planets: List[Dict[str, Any]]) -> List[str]:
        aspecting = []
        for p in planets:
            p_house = p["house"]
            p_name = p["name"]
            
            # House distance (1-12)
            dist = ((target_house - p_house) % 12) + 1
            
            # Standard 7th aspect for all planets
            if dist == 7:
                aspecting.append(p_name)
            elif p_name == "Mars" and dist in [4, 8]:
                aspecting.append(p_name)
            elif p_name == "Jupiter" and dist in [5, 9]:
                aspecting.append(p_name)
            elif p_name == "Saturn" and dist in [3, 10]:
                aspecting.append(p_name)
            elif p_name in ["Rahu", "Ketu"] and dist in [5, 9]:
                aspecting.append(p_name)

        return aspecting

house_service = HouseService()
