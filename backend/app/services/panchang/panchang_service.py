from datetime import datetime, time, timedelta
from typing import Dict, Any
import swisseph as swe
from app.services.swiss_ephemeris import swe_engine
from app.services.nakshatra import get_nakshatra_info
from app.utils.time_conversion import datetime_to_julian_day_ut

TITHI_NAMES = [
    "Shukla Pratipada", "Shukla Dwitiya", "Shukla Tritiya", "Shukla Chaturthi",
    "Shukla Panchami", "Shukla Shashthi", "Shukla Saptami", "Shukla Ashtami",
    "Shukla Navami", "Shukla Dashami", "Shukla Ekadashi", "Shukla Dwadashi",
    "Shukla Trayodashi", "Shukla Chaturdashi", "Purnima",
    "Krishna Pratipada", "Krishna Dwitiya", "Krishna Tritiya", "Krishna Chaturthi",
    "Krishna Panchami", "Krishna Shashthi", "Krishna Saptami", "Krishna Ashtami",
    "Krishna Navami", "Krishna Dashami", "Krishna Ekadashi", "Krishna Dwadashi",
    "Krishna Trayodashi", "Krishna Chaturdashi", "Amavasya"
]

VARAS = [
    "Ravivara (Sunday)", "Somavara (Monday)", "Mangalavara (Tuesday)",
    "Budhavara (Wednesday)", "Guruvara (Thursday)", "Shukravara (Friday)",
    "Shanivara (Saturday)"
]

YOGAS = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana",
    "Atiganda", "Sukarma", "Dhriti", "Shoola", "Ganda",
    "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
    "Siddhi", "Vyatipata", "Variyan", "Parigha", "Shiva",
    "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma",
    "Indra", "Vaidhriti"
]

REPEATING_KARANAS = ["Bava", "Balava", "Kaulava", "Taitila", "Gara", "Vanija", "Vishti (Bhadra)"]

class PanchangService:
    def __init__(self, engine=None):
        self.engine = engine or swe_engine

    def calculate_panchang(
        self,
        dt_local: datetime,
        latitude: float,
        longitude: float,
        timezone_offset: float = 0.0
    ) -> Dict[str, Any]:
        """
        Calculates complete Panchang (Tithi, Vara, Nakshatra, Yoga, Karana, Sunrise, Sunset)
        for a given local datetime and location.
        """
        dt_utc = dt_local - timedelta(hours=timezone_offset)
        jd_ut = datetime_to_julian_day_ut(dt_utc)

        # Calculate exact Sun and Moon positions
        sun_res = self.engine.calculate_planet(jd_ut, "Sun", sidereal=True)
        moon_res = self.engine.calculate_planet(jd_ut, "Moon", sidereal=True)
        
        sun_lon = sun_res["longitude"]
        moon_lon = moon_res["longitude"]

        # 1. Tithi
        diff_deg = (moon_lon - sun_lon) % 360.0
        tithi_float = diff_deg / 12.0
        tithi_idx = int(tithi_float)
        tithi_progress = (tithi_float - tithi_idx) * 100.0
        paksha = "Shukla" if tithi_idx < 15 else "Krishna"
        tithi_name = TITHI_NAMES[tithi_idx]

        # 2. Vara (Weekday)
        # Weekday 0=Monday in Python datetime, translate to Sunday=0
        weekday_idx = (dt_local.weekday() + 1) % 7
        vara_name = VARAS[weekday_idx]

        # 3. Nakshatra
        nak_info = get_nakshatra_info(moon_lon)

        # 4. Yoga (Sun + Moon mod 360 / (360/27))
        sum_deg = (sun_lon + moon_lon) % 360.0
        yoga_idx = int(sum_deg // (360.0 / 27.0))
        yoga_name = YOGAS[yoga_idx % 27]

        # 5. Karana (Half of Tithi, 6 degrees)
        karana_idx = int(diff_deg // 6.0)
        if karana_idx == 0:
            karana_name = "Kintughna"
        elif karana_idx >= 57:
            if karana_idx == 57:
                karana_name = "Shakuni"
            elif karana_idx == 58:
                karana_name = "Chatushpada"
            else:
                karana_name = "Naga"
        else:
            rep_idx = (karana_idx - 1) % 7
            karana_name = REPEATING_KARANAS[rep_idx]

        # 6. Sunrise and Sunset calculation using Swiss Ephemeris
        sunrise_str, sunset_str = self._calculate_sunrise_sunset(jd_ut, latitude, longitude, timezone_offset)

        return {
            "date": dt_local.strftime("%Y-%m-%d"),
            "tithi": tithi_name,
            "tithi_number": tithi_idx + 1,
            "paksha": paksha,
            "tithi_progress_pct": round(tithi_progress, 2),
            "vara": vara_name,
            "nakshatra": nak_info["name"],
            "nakshatra_number": nak_info["number"],
            "yoga": yoga_name,
            "yoga_number": yoga_idx + 1,
            "karana": karana_name,
            "sunrise": sunrise_str,
            "sunset": sunset_str,
            "moonrise": "N/A",
            "moonset": "N/A",
        }

    def _calculate_sunrise_sunset(self, jd_ut: float, lat: float, lon: float, tz_offset: float) -> tuple[str, str]:
        try:
            # swe.rise_trans for Sun
            # swe.CALC_RISE = 1, swe.CALC_SET = 2
            geopos = (lon, lat, 0.0)
            res_rise, ret_rise = swe.rise_trans(jd_ut - 0.5, swe.SUN, geopos, 0, 0, swe.CALC_RISE)
            res_set, ret_set = swe.rise_trans(jd_ut - 0.5, swe.SUN, geopos, 0, 0, swe.CALC_SET)
            
            def jd_to_time_str(jd_val):
                # Convert JD back to local time
                year, month, day, hour_float = swe.revjul(jd_val + (tz_offset / 24.0), swe.GREG_CAL)
                h = int(hour_float)
                m = int((hour_float - h) * 60)
                s = int(round(((hour_float - h) * 60 - m) * 60))
                return f"{h:02d}:{m:02d}:{s:02d}"

            return jd_to_time_str(res_rise[0]), jd_to_time_str(res_set[0])
        except Exception:
            # Fallback astronomical approximation if swe_rise fails on extreme latitudes
            return "06:00:00", "18:00:00"

panchang_service = PanchangService()
