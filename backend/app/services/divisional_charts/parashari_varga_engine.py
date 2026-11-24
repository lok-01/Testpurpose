"""
Parashari Varga Details, Upagrahas, Functional Benefic/Malefic, and Vimshopaka Bala Engine.
All astronomical positions derived from Swiss Ephemeris longitudes and Sunrise/Sunset.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import swisseph as swe

from app.services.nakshatra import RASHIS, get_nakshatra_info
from app.services.divisional_charts.divisional_service import DivisionalChartService, VARGA_CONFIGS
from app.services.divisional_charts.parashari_strength_service import parashari_strength_service
from app.services.panchang.panchang_service import panchang_service
from app.services.planetary_positions.planetary_service import (
    EXALTATION_SIGNS,
    DEBILITATION_SIGNS,
    OWN_SIGNS,
    NATURAL_FRIENDS,
)
from app.utils.time_conversion import datetime_to_julian_day_ut

SIGN_ABBR_2 = [
    "Ar", "Ta", "Ge", "Cn", "Le", "Vi",
    "Li", "Sc", "Sg", "Cp", "Aq", "Pi"
]

# Natural benefic/malefic status (B, M, N)
NATURAL_NATURE = {
    "Sun": "M",
    "Moon": "B",
    "Mars": "M",
    "Mercury": "N",
    "Jupiter": "B",
    "Venus": "B",
    "Saturn": "M",
    "Rahu": "M",
    "Ketu": "M",
}

# Standard Parashari Vimshopaka Varga Weights (Sum = 20.0)
VIMSHOPAKA_WEIGHTS = {
    "Shad": {
        "D1": 6.0, "D2": 2.0, "D3": 4.0, "D9": 5.0, "D12": 2.0, "D30": 1.0
    },
    "Sapta": {
        "D1": 5.0, "D2": 2.0, "D3": 3.0, "D7": 2.5, "D9": 4.5, "D12": 2.0, "D30": 1.0
    },
    "Dasha": {
        "D1": 3.0, "D2": 1.5, "D3": 1.5, "D7": 1.5, "D9": 1.5, "D10": 1.5,
        "D12": 1.5, "D16": 1.5, "D30": 1.5, "D60": 5.0
    },
    "Shodasha": {
        "D1": 3.5, "D2": 1.0, "D3": 1.0, "D4": 0.5, "D7": 0.5, "D9": 3.0,
        "D10": 0.5, "D12": 0.5, "D16": 2.0, "D20": 0.5, "D24": 0.5, "D27": 0.5,
        "D30": 1.0, "D40": 0.5, "D45": 0.5, "D60": 4.0
    }
}

# Weekday Upagraha part indices (1-based among 8 parts of day; night shifts by +4 mod 7)
# Order of lords starting from Sunday (0): Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn
# Part numbers (1..8) for Gulika(Saturn), Kaala(Sun), Mrityu(Mars), ArthaPrahara(Mercury), YamaGhantaka(Jupiter)
# Standard Parashari daytime sequence starting from weekday lord:
# Weekday 0=Sun, 1=Mon, 2=Tue, 3=Wed, 4=Thu, 5=Fri, 6=Sat
WEEKDAY_DAY_ORDER = [
    ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", None],      # Sun
    ["Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Sun", None],      # Mon
    ["Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Sun", "Moon", None],      # Tue
    ["Mercury", "Jupiter", "Venus", "Saturn", "Sun", "Moon", "Mars", None],      # Wed
    ["Jupiter", "Venus", "Saturn", "Sun", "Moon", "Mars", "Mercury", None],      # Thu
    ["Venus", "Saturn", "Sun", "Moon", "Mars", "Mercury", "Jupiter", None],      # Fri
    ["Saturn", "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", None],      # Sat
]

WEEKDAY_NIGHT_ORDER = [
    ["Jupiter", "Venus", "Saturn", "Sun", "Moon", "Mars", "Mercury", None],      # Sun night (starts 5th from Sun)
    ["Venus", "Saturn", "Sun", "Moon", "Mars", "Mercury", "Jupiter", None],      # Mon night
    ["Saturn", "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", None],      # Tue night
    ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", None],      # Wed night
    ["Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Sun", None],      # Thu night
    ["Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Sun", "Moon", None],      # Fri night
    ["Mercury", "Jupiter", "Venus", "Saturn", "Sun", "Moon", "Mars", None],      # Sat night
]


def format_dms_clean(deg_in_sign: float) -> str:
    d = int(deg_in_sign)
    m_float = (deg_in_sign - d) * 60.0
    m = int(m_float)
    s = int(round((m_float - m) * 60.0))
    if s == 60:
        s = 0
        m += 1
    if m == 60:
        m = 0
        d += 1
    return f"{d}° {m:02d}' {s:02d}\""


def get_dignity_in_sign(planet_name: str, sign_1based: int) -> str:
    if EXALTATION_SIGNS.get(planet_name) == sign_1based:
        return "Exalted"
    if DEBILITATION_SIGNS.get(planet_name) == sign_1based:
        return "Debilitated"
    if sign_1based in OWN_SIGNS.get(planet_name, []):
        return "Own"

    sign_lord = RASHIS[sign_1based - 1]["lord"]
    rel = NATURAL_FRIENDS.get(planet_name, {})
    if sign_lord in rel.get("friends", []):
        return "Friend"
    if sign_lord in rel.get("enemies", []):
        return "Enemy"
    return "Neutral"


def get_functional_nature(planet_name: str, lagna_sign: int) -> str:
    """
    Determines Functional Benefic (B), Malefic (M), or Neutral (N) for the given Lagna sign (1-12).
    """
    if planet_name in ("Rahu", "Ketu"):
        return "M" if planet_name == "Ketu" else "B"

    # Find which houses (1..12) this planet rules from Lagna
    ruled_houses = []
    for h in range(1, 13):
        sign_h = ((lagna_sign - 1 + (h - 1)) % 12) + 1
        if RASHIS[sign_h - 1]["lord"] == planet_name:
            ruled_houses.append(h)

    if not ruled_houses:
        return "N"

    # Trikona lords (1, 5, 9) are always functional benefics
    if any(h in (1, 5, 9) for h in ruled_houses):
        return "B"
    # Dusthana lords (6, 8, 12) without trikona lordship lean functional malefic
    if all(h in (3, 6, 8, 11, 12) for h in ruled_houses):
        return "M"
    # Kendra (4, 7, 10) ruled by natural malefic -> B/N; by natural benefic -> N/M (Kendradhipati)
    if any(h in (4, 7, 10) for h in ruled_houses):
        return "N"
    return "N"


class ParashariVargaEngine:
    def __init__(self):
        self.div_service = DivisionalChartService()

    def calculate_upagrahas(
        self,
        sun_sidereal: float,
        dt_local: datetime,
        latitude: float,
        longitude: float,
        timezone_offset: float,
        varga_key: str,
        varga_lagna_sign: int,
    ) -> List[Dict[str, Any]]:
        """
        Calculates the 11 classical Upagrahas & Aprakasha Grahas:
        Gulika, Mandi, Kaala, Mrityu, Artha Prahara, Yama Ghantaka,
        Dhooma, Indra Chapa, Parivesha, Upaketu, Vyatipata.
        """
        results = []

        # 1. Time-based Upagrahas (using Sunrise & Sunset)
        jd_noon = datetime_to_julian_day_ut(dt_local - timedelta(hours=timezone_offset))
        p_info = panchang_service.calculate_panchang(dt_local, latitude, longitude, timezone_offset)

        # Parse sunrise & sunset HH:MM:SS
        try:
            sr_t = datetime.strptime(p_info["sunrise"], "%H:%M:%S").time()
            ss_t = datetime.strptime(p_info["sunset"], "%H:%M:%S").time()
            sr_dt = datetime.combine(dt_local.date(), sr_t)
            ss_dt = datetime.combine(dt_local.date(), ss_t)
        except Exception:
            sr_dt = datetime.combine(dt_local.date(), datetime.strptime("06:00:00", "%H:%M:%S").time())
            ss_dt = datetime.combine(dt_local.date(), datetime.strptime("18:00:00", "%H:%M:%S").time())

        is_day = sr_dt <= dt_local < ss_dt
        if is_day:
            span_start = sr_dt
            span_end = ss_dt
        elif dt_local >= ss_dt:
            span_start = ss_dt
            span_end = sr_dt + timedelta(days=1)
        else:
            # Before sunrise -> previous night
            span_start = ss_dt - timedelta(days=1)
            span_end = sr_dt

        part_duration = (span_end - span_start) / 8.0
        # Weekday index: Python Monday=0..Sunday=6 -> convert to Sunday=0..Saturday=6
        wd_idx = (span_start.weekday() + 1) % 7
        order = WEEKDAY_DAY_ORDER[wd_idx] if is_day else WEEKDAY_NIGHT_ORDER[wd_idx]

        # Mapping of Upagraha -> governing planet in the 8-part sequence
        time_upagraha_lords = [
            ("Gulika", "Saturn", 0.0),      # Start of Saturn part
            ("Mandi", "Saturn", 0.5),       # Midpoint of Saturn part
            ("Kaala", "Sun", 0.0),
            ("Mrityu", "Mars", 0.0),
            ("Artha Prahara", "Mercury", 0.0),
            ("Yama Ghantaka", "Jupiter", 0.0),
        ]

        swe.set_sid_mode(swe.SIDM_LAHIRI)

        for u_name, gov_planet, offset_frac in time_upagraha_lords:
            try:
                part_idx = order.index(gov_planet)
            except ValueError:
                part_idx = 0
            u_local_dt = span_start + part_duration * (part_idx + offset_frac)
            u_utc_dt = u_local_dt - timedelta(hours=timezone_offset)
            u_jd = datetime_to_julian_day_ut(u_utc_dt)
            ayan = float(swe.get_ayanamsa_ut(u_jd))
            _, ascmc = swe.houses(u_jd, latitude, longitude, b"W")
            u_lon = (ascmc[0] - ayan) % 360.0

            v_sign = self.div_service.calculate_varga_sign(u_lon, varga_key)
            deg_in_sign = u_lon % 30.0
            house = ((v_sign - varga_lagna_sign) % 12) + 1
            results.append({
                "body": u_name,
                "sign": RASHIS[v_sign - 1]["name"],
                "degrees": format_dms_clean(deg_in_sign),
                "house": house,
                "sidereal_longitude": round(u_lon, 4),
            })

        # 2. Sun-based Aprakasha Grahas
        dhooma = (sun_sidereal + 133.3333333333) % 360.0
        vyatipata = (360.0 - dhooma) % 360.0
        parivesha = (vyatipata + 180.0) % 360.0
        indra_chapa = (360.0 - parivesha) % 360.0
        upaketu = (indra_chapa + 16.6666666667) % 360.0

        sun_upagrahas = [
            ("Dhooma", dhooma),
            ("Indra Chapa", indra_chapa),
            ("Parivesha", parivesha),
            ("Upaketu", upaketu),
            ("Vyatipata", vyatipata),
        ]

        for u_name, u_lon in sun_upagrahas:
            v_sign = self.div_service.calculate_varga_sign(u_lon, varga_key)
            deg_in_sign = u_lon % 30.0
            house = ((v_sign - varga_lagna_sign) % 12) + 1
            results.append({
                "body": u_name,
                "sign": RASHIS[v_sign - 1]["name"],
                "degrees": format_dms_clean(deg_in_sign),
                "house": house,
                "sidereal_longitude": round(u_lon, 4),
            })

        return results

    def calculate_vimshopaka_bala(self, planets: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Calculates Vimshopaka Bala (out of 20.00) for Shad, Sapta, Dasha, and Shodasha varga groups.
        """
        dignity_points = {
            "Exalted": 20.0,
            "Own": 20.0,
            "Friend": 15.0,
            "Neutral": 10.0,
            "Enemy": 5.0,
            "Debilitated": 3.0,
        }

        vedic_9 = [p for p in planets if p["name"] in (
            "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"
        )]

        output: Dict[str, List[Dict[str, Any]]] = {}
        for group_name, weights in VIMSHOPAKA_WEIGHTS.items():
            rows = []
            for p in vedic_9:
                total_score = 0.0
                strong_count = 0
                for v_key, w in weights.items():
                    v_sign = self.div_service.calculate_varga_sign(p["sidereal_longitude"], v_key)
                    dig = get_dignity_in_sign(p["name"], v_sign)
                    pts = dignity_points.get(dig, 10.0)
                    total_score += (pts / 20.0) * w
                    if dig in ("Exalted", "Own", "Friend"):
                        strong_count += 1

                pct = (total_score / 20.0) * 100.0
                if pct >= 75.0:
                    band = "Pūrna"
                elif pct >= 62.5:
                    band = "Atimadhya"
                elif pct >= 50.0:
                    band = "Madhya"
                else:
                    band = "Svalpa"

                # Classical Vaisheshikamsa designation when strong in 2+ vargas
                designation = "—"
                if strong_count >= 10:
                    designation = f"{strong_count}-Devaloka"
                elif strong_count >= 7:
                    designation = f"{strong_count}-Simhasana"
                elif strong_count >= 5:
                    designation = f"{strong_count}-Uttama"
                elif strong_count >= 2:
                    designation = f"{strong_count}-Kimsuka"

                rows.append({
                    "body": p["name"],
                    "score": round(total_score, 2),
                    "pct": round(pct, 2),
                    "band": band,
                    "designation": designation,
                })
            output[group_name] = rows

        return output

    def get_full_varga_worksheet(
        self,
        varga_key: str,
        lagna_longitude: float,
        planets: List[Dict[str, Any]],
        dt_local: datetime,
        latitude: float,
        longitude: float,
        timezone_offset: float,
    ) -> Dict[str, Any]:
        cfg = VARGA_CONFIGS.get(varga_key, VARGA_CONFIGS["D1"])
        division = cfg["division"]
        varga_lagna_sign = self.div_service.calculate_varga_sign(lagna_longitude, varga_key)
        lagna_rashi_data = RASHIS[varga_lagna_sign - 1]

        vedic_9 = [p for p in planets if p["name"] in (
            "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"
        )]

        placements = []
        houses_dict = {h: [] for h in range(1, 13)}

        for p in vedic_9:
            sid_lon = p["sidereal_longitude"]
            deg_in_sign = sid_lon % 30.0
            v_sign = self.div_service.calculate_varga_sign(sid_lon, varga_key)
            house = ((v_sign - varga_lagna_sign) % 12) + 1
            amsha = int((deg_in_sign / (30.0 / division))) + 1 if division > 1 else 1
            if amsha > division:
                amsha = division

            # In D1 use exact deg_in_sign; in higher Vargas show projected varga degree (deg_in_sign * division) % 30
            display_deg = deg_in_sign if division == 1 else ((deg_in_sign * division) % 30.0)
            dignity = get_dignity_in_sign(p["name"], v_sign)
            nat = NATURAL_NATURE.get(p["name"], "N")
            func = get_functional_nature(p["name"], varga_lagna_sign)

            placements.append({
                "body": p["name"],
                "is_retrograde": p["is_retrograde"],
                "house": house,
                "sign_abbr": SIGN_ABBR_2[v_sign - 1],
                "sign": RASHIS[v_sign - 1]["name"],
                "sign_number": v_sign,
                "deg": format_dms_clean(display_deg),
                "nakshatra": f"{p['nakshatra']} {p['pada']}",
                "amsha": amsha,
                "dignity": dignity,
                "nat": nat,
                "func": func,
                "is_combust": p.get("is_combust", False),
            })
            houses_dict[house].append(p["name"])

        sun_lon = next(p["sidereal_longitude"] for p in vedic_9 if p["name"] == "Sun")
        upagrahas = self.calculate_upagrahas(
            sun_sidereal=sun_lon,
            dt_local=dt_local,
            latitude=latitude,
            longitude=longitude,
            timezone_offset=timezone_offset,
            varga_key=varga_key,
            varga_lagna_sign=varga_lagna_sign,
        )

        vimshopaka = self.calculate_vimshopaka_bala(planets)
        moon_lon = next(p["sidereal_longitude"] for p in vedic_9 if p["name"] == "Moon")
        ashtakavarga = parashari_strength_service.calculate_ashtakavarga(varga_lagna_sign, placements)
        shadbala = parashari_strength_service.calculate_shadbala(
            planets=planets,
            lagna_longitude=lagna_longitude,
            dt_local=dt_local,
            latitude=latitude,
            longitude=longitude,
            timezone_offset=timezone_offset,
        )
        varnada = parashari_strength_service.calculate_varnada(
            lagna_longitude=lagna_longitude,
            sun_longitude=sun_lon,
            dt_local=dt_local,
            latitude=latitude,
            longitude=longitude,
            timezone_offset=timezone_offset,
        )
        special_tithis = parashari_strength_service.calculate_special_tithis(sun_lon, moon_lon)

        return {
            "varga_key": varga_key,
            "varga_name": cfg["name"],
            "varga_division": division,
            "description": cfg["description"],
            "lagna_rashi": lagna_rashi_data["name"],
            "lagna_sign_abbr": SIGN_ABBR_2[varga_lagna_sign - 1],
            "lagna_rashi_number": varga_lagna_sign,
            "lagna_deg": format_dms_clean((lagna_longitude % 30.0) if division == 1 else ((lagna_longitude % 30.0) * division) % 30.0),
            "placements": placements,
            "houses": houses_dict,
            "upagrahas": upagrahas,
            "vimshopaka": vimshopaka,
            "shadbala": shadbala,
            "ashtakavarga": ashtakavarga,
            "varnada": varnada,
            "special_tithis": special_tithis,
        }


parashari_varga_engine = ParashariVargaEngine()
