from datetime import datetime
from typing import List, Dict, Any
from app.services.swiss_ephemeris import swe_engine
from app.services.nakshatra import get_rashi_info, get_nakshatra_info
from app.utils.time_conversion import datetime_to_julian_day_ut, degree_to_dms

TRANSIT_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

# Favorable Gochara houses from natal Moon (BPHS / Phaladeepika)
FAVORABLE_TRANSIT_HOUSES = {
    "Sun": [3, 6, 10, 11],
    "Moon": [1, 3, 6, 7, 10, 11],
    "Mars": [3, 6, 11],
    "Mercury": [2, 4, 6, 8, 10, 11],
    "Jupiter": [2, 5, 7, 9, 11],
    "Venus": [1, 2, 3, 4, 5, 8, 9, 11, 12],
    "Saturn": [3, 6, 11],
    "Rahu": [3, 6, 10, 11],
    "Ketu": [3, 6, 9, 11],
}

class TransitService:
    def __init__(self, engine=None):
        self.engine = engine or swe_engine

    def calculate_transits(
        self,
        transit_datetime: datetime,
        natal_lagna_sign: int,
        natal_moon_sign: int
    ) -> Dict[str, Any]:
        """
        Calculates real-time planetary transits for any date using Swiss Ephemeris.
        Computes houses from Lagna and Moon, retrograde motion, and Gochara effects.
        """
        jd_ut = datetime_to_julian_day_ut(transit_datetime)
        ayanamsa = self.engine.get_ayanamsa_ut(jd_ut)

        transit_list = []
        for p_name in TRANSIT_PLANETS:
            p_calc = self.engine.calculate_planet(jd_ut, p_name, sidereal=True)
            lon = p_calc["longitude"]
            r_info = get_rashi_info(lon)
            nak_info = get_nakshatra_info(lon)

            # House from Natal Lagna
            house_from_lagna = ((r_info["number"] - natal_lagna_sign) % 12) + 1
            # House from Natal Moon
            house_from_moon = ((r_info["number"] - natal_moon_sign) % 12) + 1

            fav_houses = FAVORABLE_TRANSIT_HOUSES.get(p_name, [])
            is_favorable = house_from_moon in fav_houses

            transit_list.append({
                "planet": p_name,
                "sidereal_longitude": lon,
                "rashi": r_info["name"],
                "rashi_number": r_info["number"],
                "degree_in_rashi": r_info["degree_in_rashi"],
                "dms": degree_to_dms(r_info["degree_in_rashi"]),
                "nakshatra": nak_info["name"],
                "pada": nak_info["pada"],
                "is_retrograde": p_calc["is_retrograde"],
                "speed": p_calc["speed_longitude"],
                "house_from_lagna": house_from_lagna,
                "house_from_moon": house_from_moon,
                "is_favorable_gochara": is_favorable,
            })

        # Special Saturn Sade Sati check:
        # Saturn in 12th, 1st, or 2nd house from natal Moon
        saturn_t = next(p for p in transit_list if p["planet"] == "Saturn")
        sat_moon_dist = saturn_t["house_from_moon"]
        
        sade_sati_status = "Not in Sade Sati"
        if sat_moon_dist == 12:
            sade_sati_status = "Sade Sati Phase 1 (Rising Phase - 12th from Moon)"
        elif sat_moon_dist == 1:
            sade_sati_status = "Sade Sati Phase 2 (Peak Phase - over Moon)"
        elif sat_moon_dist == 2:
            sade_sati_status = "Sade Sati Phase 3 (Setting Phase - 2nd from Moon)"

        # Special Jupiter Transit
        jup_t = next(p for p in transit_list if p["planet"] == "Jupiter")
        jup_status = f"Jupiter transiting house {jup_t['house_from_moon']} from Moon ({'Favorable' if jup_t['is_favorable_gochara'] else 'Inauspicious/Transformative'})"

        return {
            "transit_date": transit_datetime.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "ayanamsa": ayanamsa,
            "engine_version": self.engine.get_version(),
            "sade_sati_status": sade_sati_status,
            "jupiter_transit_status": jup_status,
            "transits": transit_list,
        }

transit_service = TransitService()
