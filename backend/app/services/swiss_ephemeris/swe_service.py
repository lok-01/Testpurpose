import os
from typing import Dict, Tuple, Any
import swisseph as swe
from app.config import settings

class SwissEphemerisService:
    AYANAMSA_MAP = {
        "LAHIRI": swe.SIDM_LAHIRI,
        "RAMAN": swe.SIDM_RAMAN,
        "KRISHNAMURTI": swe.SIDM_KRISHNAMURTI,
        "KP": swe.SIDM_KRISHNAMURTI,
        "FAGAN_BRADLEY": swe.SIDM_FAGAN_BRADLEY,
        "YUKTESHWAR": swe.SIDM_YUKTESHWAR,
        "TRUE_CITRA": swe.SIDM_TRUE_CITRA,
        "TRUE_CHITRA": swe.SIDM_TRUE_CITRA,
    }

    PLANET_MAP = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mars": swe.MARS,
        "Mercury": swe.MERCURY,
        "Jupiter": swe.JUPITER,
        "Venus": swe.VENUS,
        "Saturn": swe.SATURN,
        "Rahu": swe.TRUE_NODE,  # Configurable between TRUE_NODE and MEAN_NODE
        "Uranus": swe.URANUS,
        "Neptune": swe.NEPTUNE,
        "Pluto": swe.PLUTO,
    }

    def __init__(self, ephe_path: str = None):
        self.ephe_path = ephe_path or settings.SWE_EPHE_PATH
        if os.path.exists(self.ephe_path):
            swe.set_ephe_path(self.ephe_path)
        else:
            swe.set_ephe_path("")  # Uses internal Moshier ephemeris if files not found
        
        self.active_ayanamsa = settings.DEFAULT_AYANAMSA
        self.node_type = settings.DEFAULT_NODE_CALC
        self._configure_sidereal()

    def _configure_sidereal(self, ayanamsa_name: str = None):
        if ayanamsa_name:
            self.active_ayanamsa = ayanamsa_name.upper()
        ayan_id = self.AYANAMSA_MAP.get(self.active_ayanamsa, swe.SIDM_LAHIRI)
        swe.set_sid_mode(ayan_id)

    def get_version(self) -> str:
        return str(swe.version)

    def get_ayanamsa_ut(self, jd_ut: float, ayanamsa_name: str = None) -> float:
        self._configure_sidereal(ayanamsa_name)
        return float(swe.get_ayanamsa_ut(jd_ut))

    def calculate_planet(self, jd_ut: float, planet_name: str, sidereal: bool = True, node_type: str = None) -> Dict[str, Any]:
        """
        Calculates exact astronomical position of a planet using Swiss Ephemeris.
        Returns longitude, latitude, distance, speed in longitude, speed in latitude, speed in distance.
        """
        self._configure_sidereal()
        
        # Determine planet identifier
        if planet_name == "Ketu":
            # Ketu is exactly 180 degrees from Rahu
            rahu_res = self.calculate_planet(jd_ut, "Rahu", sidereal=sidereal, node_type=node_type)
            ketu_long = (rahu_res["longitude"] + 180.0) % 360.0
            return {
                "name": "Ketu",
                "id": -1,
                "longitude": ketu_long,
                "latitude": -rahu_res["latitude"],
                "distance": rahu_res["distance"],
                "speed_longitude": rahu_res["speed_longitude"],
                "is_retrograde": True,  # Nodes are normally retrograde
            }

        node_choice = node_type or self.node_type
        if planet_name == "Rahu":
            p_id = swe.TRUE_NODE if node_choice == "TRUE_NODE" else swe.MEAN_NODE
        else:
            p_id = self.PLANET_MAP.get(planet_name)
            if p_id is None:
                raise ValueError(f"Unknown planet: {planet_name}")

        flag = swe.FLG_SWIEPH | swe.FLG_SPEED
        if sidereal:
            flag |= swe.FLG_SIDEREAL

        res, ret_flag = swe.calc_ut(jd_ut, p_id, flag)
        return {
            "name": planet_name,
            "id": p_id,
            "longitude": float(res[0]),
            "latitude": float(res[1]),
            "distance": float(res[2]),
            "speed_longitude": float(res[3]),
            "is_retrograde": res[3] < 0.0,
        }

    def calculate_houses(self, jd_ut: float, lat: float, lon: float, hsys: str = "W") -> Tuple[float, list, float, float]:
        """
        Calculates Lagna (Ascendant), MC, and house cusps.
        hsys: 'W' for Whole Sign, 'P' for Placidus, 'E' for Equal.
        Returns: (sidereal_ascendant, cusps, mc, armc)
        """
        self._configure_sidereal()
        ayanamsa = self.get_ayanamsa_ut(jd_ut)
        
        # swe.houses returns tropical cusps and ascmc (Asc, MC, ARMC, Vertex, etc.)
        cusps, ascmc = swe.houses(jd_ut, lat, lon, hsys.encode('ascii'))
        tropical_asc = ascmc[0]
        tropical_mc = ascmc[1]
        
        # Sidereal conversion
        sidereal_asc = (tropical_asc - ayanamsa) % 360.0
        sidereal_mc = (tropical_mc - ayanamsa) % 360.0
        
        # Correct cusps if not whole-sign
        sidereal_cusps = [(c - ayanamsa) % 360.0 for c in cusps]
        
        return sidereal_asc, sidereal_cusps, sidereal_mc, ascmc[2]

swe_engine = SwissEphemerisService()
