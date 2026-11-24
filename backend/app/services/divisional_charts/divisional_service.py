from typing import Dict, List, Any
from app.services.nakshatra import RASHIS

VARGA_CONFIGS = {
    "D1": {"name": "Rashi", "division": 1, "description": "Physical existence, primary life pattern"},
    "D2": {"name": "Hora", "division": 2, "description": "Wealth, family prosperity, resources"},
    "D3": {"name": "Drekkana", "division": 3, "description": "Siblings, courage, vitality, initiatives"},
    "D4": {"name": "Chaturthamsha", "division": 4, "description": "Fixed assets, home, conveyances, fortune"},
    "D7": {"name": "Saptamsha", "division": 7, "description": "Children, progeny, creative lineage"},
    "D9": {"name": "Navamsha", "division": 9, "description": "Dharma, marriage, inner potential, soul purpose"},
    "D10": {"name": "Dashamsha", "division": 10, "description": "Career, profession, social status, achievements"},
    "D12": {"name": "Dwadashamsha", "division": 12, "description": "Parents, lineage, ancestral karma"},
    "D16": {"name": "Shodashamsha", "division": 16, "description": "Vehicles, comforts, happiness, luxuries"},
    "D20": {"name": "Vimshamsha", "division": 20, "description": "Spiritual progress, devotion, upasana"},
    "D24": {"name": "Chaturvimshamsha", "division": 24, "description": "Higher knowledge, education, learning"},
    "D27": {"name": "Saptavimshamsha", "division": 27, "description": "Subconscious strength, weaknesses, resilience"},
    "D30": {"name": "Trimshamsha", "division": 30, "description": "Misfortunes, evils, moral vulnerabilities"},
    "D40": {"name": "Khavedamsha", "division": 40, "description": "Auspicious & inauspicious karmic fruits"},
    "D45": {"name": "Akshavedamsha", "division": 45, "description": "General well-being, character, ethics"},
    "D60": {"name": "Shashtiamsha", "division": 60, "description": "Past life karma, all matters confirmation"},
}

class DivisionalChartService:
    def calculate_varga_sign(self, longitude: float, varga_key: str) -> int:
        """
        Calculates the mapped Rashi sign (1-12) for a given sidereal longitude according to classical Parashari rules.
        """
        lon = longitude % 360.0
        sign_1based = int(lon // 30.0) + 1
        deg_in_sign = lon % 30.0
        is_odd = (sign_1based % 2) != 0

        # Sign classifications
        # Movable (Chara): 1, 4, 7, 10
        # Fixed (Sthira): 2, 5, 8, 11
        # Dual (Dvisvabhava): 3, 6, 9, 12
        sign_mobility = "movable" if sign_1based in [1, 4, 7, 10] else ("fixed" if sign_1based in [2, 5, 8, 11] else "dual")
        
        # Triplicities (Elements)
        # Fire: 1, 5, 9; Earth: 2, 6, 10; Air: 3, 7, 11; Water: 4, 8, 12
        element = "fire" if sign_1based in [1, 5, 9] else ("earth" if sign_1based in [2, 6, 10] else ("air" if sign_1based in [3, 7, 11] else "water"))

        if varga_key == "D1":
            return sign_1based

        elif varga_key == "D2":  # Hora (15 deg each)
            part = int(deg_in_sign // 15.0)
            if is_odd:
                return 5 if part == 0 else 4  # Leo (Sun) then Cancer (Moon)
            else:
                return 4 if part == 0 else 5  # Cancer (Moon) then Leo (Sun)

        elif varga_key == "D3":  # Drekkana (10 deg each)
            part = int(deg_in_sign // 10.0)
            if part == 0:
                return sign_1based
            elif part == 1:
                return ((sign_1based - 1 + 4) % 12) + 1  # 5th from sign
            else:
                return ((sign_1based - 1 + 8) % 12) + 1  # 9th from sign

        elif varga_key == "D4":  # Chaturthamsha (7.5 deg each)
            part = int(deg_in_sign // 7.5)
            return ((sign_1based - 1 + (part * 3)) % 12) + 1

        elif varga_key == "D7":  # Saptamsha (30/7 deg each)
            part = int(deg_in_sign // (30.0 / 7.0))
            start_sign = sign_1based if is_odd else (((sign_1based - 1 + 6) % 12) + 1)
            return ((start_sign - 1 + part) % 12) + 1

        elif varga_key == "D9":  # Navamsha (3°20' = 3.3333333 deg each)
            part = int(deg_in_sign // (30.0 / 9.0))
            if element == "fire":
                start_sign = 1   # Aries
            elif element == "earth":
                start_sign = 10  # Capricorn
            elif element == "air":
                start_sign = 7   # Libra
            else:
                start_sign = 4   # Cancer
            return ((start_sign - 1 + part) % 12) + 1

        elif varga_key == "D10":  # Dashamsha (3 deg each)
            part = int(deg_in_sign // 3.0)
            start_sign = sign_1based if is_odd else (((sign_1based - 1 + 8) % 12) + 1)  # 9th from sign
            return ((start_sign - 1 + part) % 12) + 1

        elif varga_key == "D12":  # Dwadashamsha (2.5 deg each)
            part = int(deg_in_sign // 2.5)
            return ((sign_1based - 1 + part) % 12) + 1

        elif varga_key == "D16":  # Shodashamsha (30/16 deg each)
            part = int(deg_in_sign // (30.0 / 16.0))
            start_sign = 1 if sign_mobility == "movable" else (5 if sign_mobility == "fixed" else 9)
            return ((start_sign - 1 + part) % 12) + 1

        elif varga_key == "D20":  # Vimshamsha (1.5 deg each)
            part = int(deg_in_sign // 1.5)
            start_sign = 1 if sign_mobility == "movable" else (9 if sign_mobility == "fixed" else 5)
            return ((start_sign - 1 + part) % 12) + 1

        elif varga_key == "D24":  # Chaturvimshamsha (1.25 deg each)
            part = int(deg_in_sign // 1.25)
            start_sign = 5 if is_odd else 4  # Leo for odd, Cancer for even
            return ((start_sign - 1 + part) % 12) + 1

        elif varga_key == "D27":  # Saptavimshamsha (30/27 deg each)
            part = int(deg_in_sign // (30.0 / 27.0))
            start_sign = 1 if element == "fire" else (4 if element == "earth" else (7 if element == "air" else 10))
            return ((start_sign - 1 + part) % 12) + 1

        elif varga_key == "D30":  # Trimshamsha (classical unequal ruler degree mapping)
            if is_odd:
                if deg_in_sign < 5.0:
                    return 1   # Mars (Aries)
                elif deg_in_sign < 10.0:
                    return 11  # Saturn (Aquarius)
                elif deg_in_sign < 18.0:
                    return 9   # Jupiter (Sagittarius)
                elif deg_in_sign < 25.0:
                    return 3   # Mercury (Gemini)
                else:
                    return 7   # Venus (Libra)
            else:
                if deg_in_sign < 5.0:
                    return 2   # Venus (Taurus)
                elif deg_in_sign < 12.0:
                    return 6   # Mercury (Virgo)
                elif deg_in_sign < 20.0:
                    return 12  # Jupiter (Pisces)
                elif deg_in_sign < 25.0:
                    return 10  # Saturn (Capricorn)
                else:
                    return 8   # Mars (Scorpio)

        elif varga_key == "D40":  # Khavedamsha (30/40 deg = 0.75 deg each)
            part = int(deg_in_sign // 0.75)
            start_sign = 1 if is_odd else 7  # Aries for odd, Libra for even
            return ((start_sign - 1 + part) % 12) + 1

        elif varga_key == "D45":  # Akshavedamsha (30/45 deg = 0.6666667 deg each)
            part = int(deg_in_sign // (30.0 / 45.0))
            start_sign = 1 if sign_mobility == "movable" else (5 if sign_mobility == "fixed" else 9)
            return ((start_sign - 1 + part) % 12) + 1

        elif varga_key == "D60":  # Shashtiamsha (0.5 deg each)
            part = int(deg_in_sign // 0.5)
            return ((sign_1based - 1 + part) % 12) + 1

        return sign_1based

    def generate_divisional_chart(
        self,
        varga_key: str,
        lagna_longitude: float,
        planets: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        cfg = VARGA_CONFIGS.get(varga_key, VARGA_CONFIGS["D9"])
        varga_lagna_sign = self.calculate_varga_sign(lagna_longitude, varga_key)
        lagna_rashi_data = RASHIS[varga_lagna_sign - 1]

        varga_planets = []
        houses_dict = {h: [] for h in range(1, 13)}

        for p in planets:
            p_sign = self.calculate_varga_sign(p["sidereal_longitude"], varga_key)
            sign_data = RASHIS[p_sign - 1]
            # House in varga from varga lagna
            house = ((p_sign - varga_lagna_sign) % 12) + 1
            
            p_info = {
                "name": p["name"],
                "sign": sign_data["name"],
                "sign_number": p_sign,
                "sign_lord": sign_data["lord"],
                "house": house,
            }
            varga_planets.append(p_info)
            houses_dict[house].append(p["name"])

        return {
            "varga_name": cfg["name"],
            "varga_key": varga_key,
            "varga_division": cfg["division"],
            "description": cfg["description"],
            "lagna_rashi": lagna_rashi_data["name"],
            "lagna_rashi_number": varga_lagna_sign,
            "planets": varga_planets,
            "houses": houses_dict,
        }

divisional_service = DivisionalChartService()
