"""
Classical Parashari Strength & Special Points Service:
- Ashtakavarga (Bhinna Ashtakavarga for Lagna + 7 Grahas, Sarvashtakavarga SAV = 337)
- Shadbala (Sthana, Dig, Kala, Chesta, Naisargika, Drik, Total Virupas, Rupas, %, Min)
- Varnada Lagna (Varnada Lagna + V2..V12)
- Special House Tithis (Janma..Vyaya with % Left, Lord, Deity)
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any
import math
import swisseph as swe

from app.services.nakshatra import RASHIS
from app.services.panchang.panchang_service import panchang_service
from app.services.planetary_positions.planetary_service import (
    EXALTATION_SIGNS,
    DEBILITATION_SIGNS,
    OWN_SIGNS,
    NATURAL_FRIENDS,
)
from app.utils.time_conversion import datetime_to_julian_day_ut

SEVEN_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

# Canonical BPHS Ashtakavarga Bindu Matrices (1-based houses from each contributor)
# Total bindus: Sun=48, Moon=49, Mars=39, Mercury=54, Jupiter=56, Venus=52, Saturn=39, Lagna=49
ASHTAKAVARGA_RULES = {
    "Sun": {
        "Sun": [1, 2, 4, 7, 8, 9, 10, 11],
        "Moon": [3, 6, 10, 11],
        "Mars": [1, 2, 4, 7, 8, 9, 10, 11],
        "Mercury": [3, 5, 6, 9, 10, 11, 12],
        "Jupiter": [5, 6, 9, 11],
        "Venus": [6, 7, 12],
        "Saturn": [1, 2, 4, 7, 8, 9, 10, 11],
        "Lagna": [3, 4, 6, 10, 11, 12],
    },
    "Moon": {
        "Sun": [3, 6, 7, 8, 10, 11],
        "Moon": [1, 3, 6, 7, 10, 11],
        "Mars": [2, 3, 5, 6, 9, 10, 11],
        "Mercury": [1, 3, 4, 5, 7, 8, 10, 11],
        "Jupiter": [1, 4, 7, 8, 10, 11, 12],
        "Venus": [3, 4, 5, 7, 9, 10, 11],
        "Saturn": [3, 5, 6, 11],
        "Lagna": [3, 6, 10, 11],
    },
    "Mars": {
        "Sun": [3, 5, 6, 10, 11],
        "Moon": [3, 6, 11],
        "Mars": [1, 2, 4, 7, 8, 10, 11],
        "Mercury": [3, 5, 6, 11],
        "Jupiter": [6, 10, 11, 12],
        "Venus": [6, 8, 11, 12],
        "Saturn": [1, 4, 7, 8, 9, 10, 11],
        "Lagna": [1, 3, 6, 10, 11],
    },
    "Mercury": {
        "Sun": [5, 6, 9, 11, 12],
        "Moon": [2, 4, 6, 8, 10, 11],
        "Mars": [1, 2, 4, 7, 8, 9, 10, 11],
        "Mercury": [1, 3, 5, 6, 9, 10, 11, 12],
        "Jupiter": [6, 8, 11, 12],
        "Venus": [1, 2, 3, 4, 5, 8, 9, 11],
        "Saturn": [1, 2, 4, 7, 8, 9, 10, 11],
        "Lagna": [1, 2, 4, 6, 8, 10, 11],
    },
    "Jupiter": {
        "Sun": [1, 2, 3, 4, 7, 8, 9, 10, 11],
        "Moon": [2, 5, 7, 9, 11],
        "Mars": [1, 2, 4, 7, 8, 10, 11],
        "Mercury": [1, 2, 4, 5, 6, 9, 10, 11],
        "Jupiter": [1, 2, 3, 4, 7, 8, 10, 11],
        "Venus": [2, 5, 6, 9, 10, 11],
        "Saturn": [3, 5, 6, 12],
        "Lagna": [1, 2, 4, 5, 6, 7, 9, 10, 11],
    },
    "Venus": {
        "Sun": [8, 11, 12],
        "Moon": [1, 2, 3, 4, 5, 8, 9, 11, 12],
        "Mars": [3, 5, 6, 9, 11, 12],
        "Mercury": [3, 5, 6, 9, 11],
        "Jupiter": [5, 8, 9, 10, 11],
        "Venus": [1, 2, 3, 4, 5, 8, 9, 10, 11],
        "Saturn": [3, 4, 5, 8, 9, 10, 11],
        "Lagna": [1, 2, 3, 4, 5, 8, 9, 11],
    },
    "Saturn": {
        "Sun": [1, 2, 4, 7, 8, 10, 11],
        "Moon": [3, 6, 11],
        "Mars": [3, 5, 6, 10, 11, 12],
        "Mercury": [6, 8, 9, 10, 11, 12],
        "Jupiter": [5, 6, 11, 12],
        "Venus": [6, 11, 12],
        "Saturn": [3, 5, 6, 11],
        "Lagna": [1, 3, 4, 6, 10, 11],
    },
    "Lagna": {
        "Sun": [3, 4, 6, 10, 11, 12],
        "Moon": [3, 6, 10, 11, 12],
        "Mars": [1, 3, 6, 10, 11],
        "Mercury": [1, 2, 4, 6, 8, 10, 11],
        "Jupiter": [1, 2, 4, 5, 6, 7, 9, 10, 11],
        "Venus": [1, 2, 3, 4, 5, 8, 9],
        "Saturn": [1, 3, 4, 6, 10, 11],
        "Lagna": [3, 6, 10, 11],
    },
}

SHADBALA_MIN_VIRUPAS = {
    "Sun": 300.0,
    "Moon": 360.0,
    "Mars": 300.0,
    "Mercury": 420.0,
    "Jupiter": 390.0,
    "Venus": 330.0,
    "Saturn": 300.0,
}

NAISARGIKA_BALA = {
    "Sun": 60.00,
    "Moon": 51.43,
    "Venus": 42.86,
    "Jupiter": 34.29,
    "Mercury": 25.71,
    "Mars": 17.14,
    "Saturn": 8.57,
}

EXALTATION_DEEP_DEG = {
    "Sun": 10.0,       # Aries 10
    "Moon": 33.0,      # Taurus 3
    "Mars": 298.0,     # Capricorn 28
    "Mercury": 165.0,  # Virgo 15
    "Jupiter": 95.0,   # Cancer 5
    "Venus": 357.0,    # Pisces 27
    "Saturn": 200.0,   # Libra 20
}

DIGBALA_ZERO_HOUSE = {
    "Sun": 4,       # Strongest in 10th -> 0 in 4th
    "Mars": 4,      # Strongest in 10th -> 0 in 4th
    "Jupiter": 7,   # Strongest in 1st -> 0 in 7th
    "Mercury": 7,   # Strongest in 1st -> 0 in 7th
    "Moon": 10,     # Strongest in 4th -> 0 in 10th
    "Venus": 10,    # Strongest in 4th -> 0 in 10th
    "Saturn": 1,    # Strongest in 7th -> 0 in 1st
}

TITHI_NAMES_15 = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dasami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi",
]

TITHI_HOUSE_LABELS = [
    "Janma", "Dhana", "Bhratri", "Matri", "Putra", "Satru",
    "Kalatra", "Mrityu", "Bhagya", "Karma", "Laabha", "Vyaya",
]

TITHI_LORDS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu"]

NITYA_DEITIES = [
    "Kameswari", "Bhagamalini", "Nitya Klinna", "Bherunda", "Vahni Vaasini",
    "Maha Vajreswari", "Sivaduti", "Tvarita", "Kula Sundari", "Nitya",
    "Nilapataka", "Vijaya", "Sarva Mangala", "Jwaalaa Maalini", "Chitra",
]


def _get_tithi_name(tithi_num: int) -> str:
    if tithi_num == 15:
        return "Pournimasya"
    if tithi_num == 30:
        return "Amavasya"
    if tithi_num < 15:
        return f"Sukla {TITHI_NAMES_15[tithi_num - 1]}"
    return f"Krishna {TITHI_NAMES_15[tithi_num - 16]}"


class ParashariStrengthService:
    def calculate_ashtakavarga(self, varga_lagna_sign: int, varga_planets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates Bhinna Ashtakavarga (Lagna + 7 planets) and Sarvashtakavarga (SAV)
        for the selected Varga chart.
        """
        pos_map: Dict[str, int] = {"Lagna": varga_lagna_sign}
        for p in varga_planets:
            name = p.get("body") or p.get("name")
            if name in SEVEN_PLANETS:
                pos_map[name] = p["sign_number"]

        bav_rows = []
        sav = [0] * 12

        for target in ["Lagna"] + SEVEN_PLANETS:
            rules = ASHTAKAVARGA_RULES[target]
            counts = [0] * 12
            for contributor, offsets in rules.items():
                c_sign = pos_map.get(contributor, 1)
                for off in offsets:
                    sign_idx = (c_sign - 1 + (off - 1)) % 12
                    counts[sign_idx] += 1
                    if target != "Lagna":
                        sav[sign_idx] += 1
            bav_rows.append({
                "body": target,
                "signs": counts,
                "total": sum(counts),
            })

        return {
            "rows": bav_rows,
            "sav": sav,
            "sav_total": sum(sav),
        }

    def calculate_shadbala(
        self,
        planets: List[Dict[str, Any]],
        lagna_longitude: float,
        dt_local: datetime,
        latitude: float,
        longitude: float,
        timezone_offset: float,
    ) -> List[Dict[str, Any]]:
        """
        Calculates classical Parashari Shadbala (Sthana, Dig, Kala, Chesta, Naisargika, Drik)
        in Virupas and Rupas for Sun through Saturn.
        """
        p_map = {p["name"]: p for p in planets if p["name"] in SEVEN_PLANETS}
        sun = p_map["Sun"]
        moon = p_map["Moon"]
        lagna_sign = int(lagna_longitude // 30.0) + 1

        # Day/night fraction for Kala Bala
        panch = panchang_service.calculate_panchang(dt_local, latitude, longitude, timezone_offset)
        try:
            sr_t = datetime.strptime(panch["sunrise"], "%H:%M:%S").time()
            ss_t = datetime.strptime(panch["sunset"], "%H:%M:%S").time()
            sr_dt = datetime.combine(dt_local.date(), sr_t)
            ss_dt = datetime.combine(dt_local.date(), ss_t)
        except Exception:
            sr_dt = datetime.combine(dt_local.date(), datetime.strptime("06:00:00", "%H:%M:%S").time())
            ss_dt = datetime.combine(dt_local.date(), datetime.strptime("18:00:00", "%H:%M:%S").time())

        is_day = sr_dt <= dt_local < ss_dt
        noon_dt = sr_dt + (ss_dt - sr_dt) / 2
        midnight_dt = ss_dt + ((sr_dt + timedelta(days=1)) - ss_dt) / 2
        if is_day:
            dist_from_midnight = abs((dt_local - (midnight_dt - timedelta(days=1))).total_seconds()) / 3600.0
            nathonnatha_day = min(60.0, (dist_from_midnight / 12.0) * 60.0)
        else:
            dist_from_midnight = abs((dt_local - midnight_dt).total_seconds()) / 3600.0
            nathonnatha_day = max(0.0, 60.0 - (dist_from_midnight / 12.0) * 60.0)

        # Paksha Bala (Moon-Sun angular elongation 0..180 -> 0..60)
        elong = abs(((moon["sidereal_longitude"] - sun["sidereal_longitude"]) % 360.0))
        if elong > 180.0:
            elong = 360.0 - elong
        benefic_paksha = (elong / 180.0) * 60.0
        malefic_paksha = 60.0 - benefic_paksha

        # Weekday lord
        wd_lords = ["Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Sun"]
        dina_lord = wd_lords[dt_local.weekday()]

        rows = []
        for name in SEVEN_PLANETS:
            p = p_map[name]
            lon = p["sidereal_longitude"]
            sign = p["rashi_number"]
            deg_in_sign = lon % 30.0
            house = ((sign - lagna_sign) % 12) + 1

            # 1. STHANA BALA
            # Uchcha Bala (max 60 at exaltation, 0 at debilitation)
            debil_deg = (EXALTATION_DEEP_DEG[name] + 180.0) % 360.0
            arc_from_debil = abs(lon - debil_deg)
            if arc_from_debil > 180.0:
                arc_from_debil = 360.0 - arc_from_debil
            uchcha_bala = (arc_from_debil / 180.0) * 60.0

            # Saptavargaja approximation via D1 + D9 dignity + Kendradi + Drekkana
            dig_map = {"Exalted": 30.0, "Moolatrikona": 22.5, "Own": 20.0, "Friend": 15.0, "Neutral": 10.0, "Enemy": 5.0, "Debilitated": 2.0}
            saptavargaja = dig_map.get(p["dignity"], 10.0) * 4.5
            kendradi = 60.0 if house in (1, 4, 7, 10) else (30.0 if house in (2, 5, 8, 11) else 15.0)
            ojha = 15.0 if ((sign % 2 == 1 and name in ("Sun", "Mars", "Jupiter", "Mercury", "Saturn")) or (sign % 2 == 0 and name in ("Moon", "Venus"))) else 0.0
            sthana = uchcha_bala + saptavargaja + kendradi + ojha

            # 2. DIG BALA (0..60)
            zero_cusp = (((lagna_sign - 1 + (DIGBALA_ZERO_HOUSE[name] - 1)) % 12) * 30.0) + 15.0
            arc_dig = abs(lon - zero_cusp)
            if arc_dig > 180.0:
                arc_dig = 360.0 - arc_dig
            dig_bala = (arc_dig / 180.0) * 60.0

            # 3. KALA BALA
            is_benefic = name in ("Moon", "Jupiter", "Venus", "Mercury")
            nath = 60.0 if name == "Mercury" else (nathonnatha_day if name in ("Sun", "Jupiter", "Venus") else (60.0 - nathonnatha_day))
            paksha = benefic_paksha * (2.0 if name == "Moon" else 1.0) if is_benefic else malefic_paksha
            tribhaga = 60.0 if ((is_day and name in ("Mercury", "Sun", "Saturn")) or (not is_day and name in ("Moon", "Venus", "Mars")) or name == "Jupiter") else 0.0
            dina = 45.0 if name == dina_lord else 0.0
            # Ayana Bala (from tropical declination approximation)
            trop_rad = math.radians(p["tropical_longitude"])
            decl = math.degrees(math.asin(math.sin(math.radians(23.44)) * math.sin(trop_rad)))
            if name in ("Sun", "Mars", "Jupiter", "Venus"):
                ayana = 30.0 + (decl / 23.44) * 30.0
            elif name in ("Moon", "Saturn"):
                ayana = 30.0 - (decl / 23.44) * 30.0
            else:
                ayana = 30.0 + abs(decl / 23.44) * 15.0
            kala = nath + paksha + tribhaga * 0.5 + dina + ayana

            # 4. CHESTA BALA
            if name == "Sun":
                chesta = ayana
            elif name == "Moon":
                chesta = paksha * 0.5
            elif p["is_retrograde"]:
                chesta = 60.0
            else:
                mean_speeds = {"Mars": 0.524, "Mercury": 1.38, "Jupiter": 0.083, "Venus": 1.2, "Saturn": 0.033}
                ratio = min(1.0, abs(p["speed"]) / max(0.01, mean_speeds.get(name, 1.0)))
                chesta = 15.0 + (1.0 - ratio) * 35.0

            # 5. NAISARGIKA BALA
            naisargika = NAISARGIKA_BALA[name]

            # 6. DRIK BALA (Benefic aspects add, malefic aspects subtract)
            drik = 0.0
            for other_name, other_p in p_map.items():
                if other_name == name:
                    continue
                diff = (lon - other_p["sidereal_longitude"]) % 360.0
                # Aspect value 0..60 simplified by Parashari Drishti angles
                asp = 0.0
                if 150.0 <= diff <= 210.0:
                    asp = 60.0 * (1.0 - abs(diff - 180.0) / 30.0)
                elif other_name == "Mars" and (90.0 <= diff <= 120.0 or 210.0 <= diff <= 240.0):
                    asp = 45.0
                elif other_name == "Jupiter" and (120.0 <= diff <= 150.0 or 240.0 <= diff <= 270.0):
                    asp = 45.0
                elif other_name == "Saturn" and (60.0 <= diff <= 90.0 or 270.0 <= diff <= 300.0):
                    asp = 45.0

                if other_name in ("Jupiter", "Venus", "Mercury"):
                    drik += asp * 0.25
                elif other_name == "Moon":
                    drik += (asp * 0.25) if elong > 90.0 else (-asp * 0.25)
                else:
                    drik -= asp * 0.25

            total = sthana + dig_bala + kala + chesta + naisargika + drik
            rupa = total / 60.0
            min_req = SHADBALA_MIN_VIRUPAS[name]
            pct = (total / min_req) * 100.0

            rows.append({
                "body": name,
                "sthana": round(sthana, 2),
                "dig": round(dig_bala, 2),
                "kala": round(kala, 2),
                "chesta": round(chesta, 2),
                "naisargika": round(naisargika, 2),
                "drik": round(drik, 2),
                "total": round(total, 2),
                "rupa": round(rupa, 2),
                "pct": round(pct, 2),
                "meets_min": total >= min_req,
            })

        return rows

    def calculate_varnada(
        self,
        lagna_longitude: float,
        sun_longitude: float,
        dt_local: datetime,
        latitude: float,
        longitude: float,
        timezone_offset: float,
    ) -> List[Dict[str, Any]]:
        """
        Calculates Varnada Lagna and Varnadas V2 through V12 (Whole Sign).
        """
        panch = panchang_service.calculate_panchang(dt_local, latitude, longitude, timezone_offset)
        try:
            sr_t = datetime.strptime(panch["sunrise"], "%H:%M:%S").time()
            sr_dt = datetime.combine(dt_local.date(), sr_t)
        except Exception:
            sr_dt = datetime.combine(dt_local.date(), datetime.strptime("06:00:00", "%H:%M:%S").time())

        hours_since_sr = ((dt_local - sr_dt).total_seconds() / 3600.0) % 24.0
        # Hora Lagna moves 30° (1 sign) per hour from Sun's position at Sunrise
        hl_lon = (sun_longitude + hours_since_sr * 30.0) % 360.0
        hl_sign = int(hl_lon // 30.0) + 1
        lagna_sign = int(lagna_longitude // 30.0) + 1

        def count_for_sign(s: int) -> int:
            return s if (s % 2 == 1) else (13 - s)

        c_hl = count_for_sign(hl_sign)
        rows = []
        for h in range(1, 13):
            h_sign = ((lagna_sign - 1 + (h - 1)) % 12) + 1
            c_h = count_for_sign(h_sign)
            same_parity = (h_sign % 2) == (hl_sign % 2)
            if same_parity:
                res_count = ((c_h + c_hl - 1) % 12) + 1
            else:
                diff = abs(c_h - c_hl)
                res_count = diff if diff > 0 else 12

            if h_sign % 2 == 1:
                v_sign = res_count
            else:
                v_sign = 13 - res_count

            v_house = ((v_sign - lagna_sign) % 12) + 1
            rows.append({
                "varnada": "Varnada Lagna" if h == 1 else f"V{h}",
                "sign": RASHIS[v_sign - 1]["name"],
                "house": v_house,
            })
        return rows

    def calculate_special_tithis(self, sun_longitude: float, moon_longitude: float) -> List[Dict[str, Any]]:
        """
        Calculates the 12 Special House Tithis (Janma through Vyaya) from Moon-Sun elongation.
        """
        base_elong = (moon_longitude - sun_longitude) % 360.0
        rows = []
        for idx, label in enumerate(TITHI_HOUSE_LABELS, start=1):
            angle = (base_elong * idx) % 360.0
            tithi_float = angle / 12.0  # 0..30
            tithi_num = int(tithi_float) + 1
            if tithi_num > 30:
                tithi_num = 30
            pct_elapsed = tithi_float - int(tithi_float)
            pct_left = int(round((1.0 - pct_elapsed) * 100))
            if pct_left == 0:
                pct_left = 100

            lord = TITHI_LORDS[(tithi_num - 1) % 8]
            deity_idx = (tithi_num - 1) % 15
            deity = NITYA_DEITIES[deity_idx]

            rows.append({
                "tithi": label,
                "name": _get_tithi_name(tithi_num),
                "pct_left": f"{pct_left}%",
                "lord": lord,
                "deity": deity,
            })
        return rows


parashari_strength_service = ParashariStrengthService()
