from typing import Dict, Any
from app.services.nakshatra import get_nakshatra_info, get_rashi_info, NAKSHATRAS, RASHIS

# Nakshatra Yoni Mapping (14 animal classifications)
NAKSHATRA_YONI = [
    "Horse", "Elephant", "Sheep", "Serpent", "Serpent", "Dog", "Cat", "Sheep", "Cat",
    "Rat", "Rat", "Cow", "Buffalo", "Tiger", "Buffalo", "Tiger", "Deer", "Deer",
    "Dog", "Monkey", "Mongoose", "Monkey", "Lion", "Horse", "Lion", "Cow", "Elephant"
]

# Nakshatra Gana Mapping (Deva, Manushya, Rakshasa)
# 0: Deva, 1: Manushya, 2: Rakshasa
NAKSHATRA_GANA = [
    "Deva", "Manushya", "Rakshasa", "Manushya", "Deva", "Manushya", "Deva", "Deva", "Rakshasa",
    "Rakshasa", "Manushya", "Manushya", "Deva", "Rakshasa", "Deva", "Rakshasa", "Deva", "Rakshasa",
    "Rakshasa", "Manushya", "Manushya", "Deva", "Rakshasa", "Rakshasa", "Manushya", "Manushya", "Deva"
]

# Nakshatra Nadi Mapping (0: Adi/Vata, 1: Madhya/Pitta, 2: Antya/Kapha)
# Pattern alternates 1, 2, 3, 3, 2, 1...
NAKSHATRA_NADI = [
    "Adi", "Madhya", "Antya", "Antya", "Madhya", "Adi", "Adi", "Madhya", "Antya",
    "Antya", "Madhya", "Adi", "Adi", "Madhya", "Antya", "Antya", "Madhya", "Adi",
    "Adi", "Madhya", "Antya", "Antya", "Madhya", "Adi", "Adi", "Madhya", "Antya"
]

# Varna hierarchy based on Moon sign (1-12)
# Brahmin (4, 8, 12) = 4; Kshatriya (1, 5, 9) = 3; Vaishya (2, 6, 10) = 2; Shudra (3, 7, 11) = 1
VARNA_RANKS = {
    4: 4, 8: 4, 12: 4,  # Water = Brahmin
    1: 3, 5: 3, 9: 3,   # Fire = Kshatriya
    2: 2, 6: 2, 10: 2,  # Earth = Vaishya
    3: 1, 7: 1, 11: 1,  # Air = Shudra
}

class KundliMatchingService:
    def match_charts(
        self,
        boy_moon_long: float,
        girl_moon_long: float,
        boy_is_manglik: bool = False,
        girl_is_manglik: bool = False
    ) -> Dict[str, Any]:
        boy_rashi = get_rashi_info(boy_moon_long)
        girl_rashi = get_rashi_info(girl_moon_long)
        boy_nak = get_nakshatra_info(boy_moon_long)
        girl_nak = get_nakshatra_info(girl_moon_long)

        # 1. Varna (1 Point)
        v_boy = VARNA_RANKS[boy_rashi["number"]]
        v_girl = VARNA_RANKS[girl_rashi["number"]]
        varna_score = 1.0 if v_boy >= v_girl else 0.0
        varna_detail = {
            "score": varna_score,
            "max": 1.0,
            "boy_varna": v_boy,
            "girl_varna": v_girl,
            "description": "Ego & spiritual temperament harmony based on Moon sign triplicities."
        }

        # 2. Vashya (2 Points)
        vashya_score = self._calc_vashya(boy_rashi["number"], girl_rashi["number"])
        vashya_detail = {
            "score": vashya_score,
            "max": 2.0,
            "description": "Mutual magnetic attraction, mutual amenability and control."
        }

        # 3. Tara (3 Points)
        tara_score = self._calc_tara(boy_nak["number"], girl_nak["number"])
        tara_detail = {
            "score": tara_score,
            "max": 3.0,
            "description": "Destiny, well-being, and longevity harmony between birth stars."
        }

        # 4. Yoni (4 Points)
        yoni_score = self._calc_yoni(boy_nak["number"], girl_nak["number"])
        yoni_detail = {
            "score": yoni_score,
            "max": 4.0,
            "boy_yoni": NAKSHATRA_YONI[boy_nak["number"] - 1],
            "girl_yoni": NAKSHATRA_YONI[girl_nak["number"] - 1],
            "description": "Biological and intimate temperament compatibility."
        }

        # 5. Graha Maitri (5 Points)
        maitri_score = self._calc_graha_maitri(boy_rashi["lord"], girl_rashi["lord"])
        maitri_detail = {
            "score": maitri_score,
            "max": 5.0,
            "boy_lord": boy_rashi["lord"],
            "girl_lord": girl_rashi["lord"],
            "description": "Mental, psychological, and intellectual friendship between Moon sign rulers."
        }

        # 6. Gana (6 Points)
        gana_score = self._calc_gana(boy_nak["number"], girl_nak["number"])
        gana_detail = {
            "score": gana_score,
            "max": 6.0,
            "boy_gana": NAKSHATRA_GANA[boy_nak["number"] - 1],
            "girl_gana": NAKSHATRA_GANA[girl_nak["number"] - 1],
            "description": "Behavioral disposition, temperament, and societal conduct."
        }

        # 7. Bhakoot (7 Points)
        bhakoot_score, bhakoot_notes = self._calc_bhakoot(
            boy_rashi["number"], girl_rashi["number"], boy_rashi["lord"], girl_rashi["lord"]
        )
        bhakoot_detail = {
            "score": bhakoot_score,
            "max": 7.0,
            "notes": bhakoot_notes,
            "description": "Family welfare, emotional bonding, and financial growth."
        }

        # 8. Nadi (8 Points)
        nadi_score, nadi_notes = self._calc_nadi(boy_nak["number"], girl_nak["number"])
        nadi_detail = {
            "score": nadi_score,
            "max": 8.0,
            "boy_nadi": NAKSHATRA_NADI[boy_nak["number"] - 1],
            "girl_nadi": NAKSHATRA_NADI[girl_nak["number"] - 1],
            "notes": nadi_notes,
            "description": "Physiological, genetic, and hereditary nerve constitution."
        }

        total_score = varna_score + vashya_score + tara_score + yoni_score + maitri_score + gana_score + bhakoot_score + nadi_score

        if total_score >= 28.0:
            recommendation = "Excellent Compatibility (Uttama)"
        elif total_score >= 18.0:
            recommendation = "Good Compatibility (Madhyama)"
        else:
            recommendation = "Low Compatibility (Adhama) - Classical remedies or deep chart analysis advised."

        # Manglik reconciliation
        manglik_compat = (boy_is_manglik == girl_is_manglik)
        summary = f"Total Ashtakoota Score: {total_score}/36. {recommendation}. "
        if boy_is_manglik and not girl_is_manglik:
            summary += "Boy has Manglik placement while Girl does not; check cancellations."
        elif girl_is_manglik and not boy_is_manglik:
            summary += "Girl has Manglik placement while Boy does not; check cancellations."
        else:
            summary += "Manglik energies are harmonized or mutually balanced."

        return {
            "varna": varna_detail,
            "vashya": vashya_detail,
            "tara": tara_detail,
            "yoni": yoni_detail,
            "graha_maitri": maitri_detail,
            "gana": gana_detail,
            "bhakoot": bhakoot_detail,
            "nadi": nadi_detail,
            "total_score": round(total_score, 1),
            "max_score": 36.0,
            "recommendation": recommendation,
            "manglik_boy": boy_is_manglik,
            "manglik_girl": girl_is_manglik,
            "matching_summary": summary,
        }

    def _calc_vashya(self, b_sign: int, g_sign: int) -> float:
        if b_sign == g_sign:
            return 2.0
        return 1.0

    def _calc_tara(self, b_nak: int, g_nak: int) -> float:
        # Distance girl to boy
        d1 = ((b_nak - g_nak) % 9) + 1
        d2 = ((g_nak - b_nak) % 9) + 1
        inauspicious = [3, 5, 7]
        b1 = d1 not in inauspicious
        b2 = d2 not in inauspicious
        if b1 and b2:
            return 3.0
        elif b1 or b2:
            return 1.5
        return 0.0

    def _calc_yoni(self, b_nak: int, g_nak: int) -> float:
        b_yoni = NAKSHATRA_YONI[b_nak - 1]
        g_yoni = NAKSHATRA_YONI[g_nak - 1]
        if b_yoni == g_yoni:
            return 4.0
        # Classic enemy pairs (Cow-Tiger, Elephant-Lion, Horse-Buffalo, Dog-Deer, Serpent-Mongoose, Monkey-Sheep, Cat-Rat)
        enemy_pairs = [
            {"Cow", "Tiger"}, {"Elephant", "Lion"}, {"Horse", "Buffalo"},
            {"Dog", "Deer"}, {"Serpent", "Mongoose"}, {"Monkey", "Sheep"}, {"Cat", "Rat"}
        ]
        pair = {b_yoni, g_yoni}
        if any(pair == ep for ep in enemy_pairs):
            return 0.0
        return 2.0

    def _calc_graha_maitri(self, lord1: str, lord2: str) -> float:
        if lord1 == lord2:
            return 5.0
        from app.services.planetary_positions.planetary_service import NATURAL_FRIENDS
        rel1 = NATURAL_FRIENDS.get(lord1, {})
        rel2 = NATURAL_FRIENDS.get(lord2, {})
        f1 = lord2 in rel1.get("friends", [])
        e1 = lord2 in rel1.get("enemies", [])
        f2 = lord1 in rel2.get("friends", [])
        e2 = lord1 in rel2.get("enemies", [])

        if f1 and f2:
            return 5.0
        elif (f1 and not e2) or (f2 and not e1):
            return 4.0
        elif not e1 and not e2:
            return 3.0
        elif (f1 and e2) or (f2 and e1):
            return 1.0
        return 0.0

    def _calc_gana(self, b_nak: int, g_nak: int) -> float:
        b_gana = NAKSHATRA_GANA[b_nak - 1]
        g_gana = NAKSHATRA_GANA[g_nak - 1]
        if b_gana == g_gana:
            return 6.0
        if (b_gana == "Deva" and g_gana == "Manushya") or (b_gana == "Manushya" and g_gana == "Deva"):
            return 5.0
        if (b_gana == "Deva" and g_gana == "Rakshasa") or (b_gana == "Rakshasa" and g_gana == "Deva"):
            return 1.0
        return 0.0

    def _calc_bhakoot(self, b_sign: int, g_sign: int, lord1: str, lord2: str) -> tuple[float, str]:
        diff = ((b_sign - g_sign) % 12) + 1
        # Inauspicious differences: 2/12 (Dwirdwadash), 6/8 (Shadashtak), 9/5 (Navapancham)
        if diff in [2, 12]:
            if lord1 == lord2:
                return 7.0, "Dwirdwadash cancelled due to identical lord."
            return 0.0, "Dwirdwadash (2/12) position."
        elif diff in [6, 8]:
            if lord1 == lord2:
                return 7.0, "Shadashtak cancelled due to identical lord."
            return 0.0, "Shadashtak (6/8) position."
        elif diff in [5, 9]:
            return 7.0, "Navapancham (5/9) favorable trine."
        return 7.0, "Auspicious Bhakoot."

    def _calc_nadi(self, b_nak: int, g_nak: int) -> tuple[float, str]:
        b_nadi = NAKSHATRA_NADI[b_nak - 1]
        g_nadi = NAKSHATRA_NADI[g_nak - 1]
        if b_nadi != g_nadi:
            return 8.0, "Different Nadis (No Nadi Dosha)."
        if b_nak == g_nak:
            return 8.0, "Same Nakshatra exception (Nadi Dosha cancelled)."
        return 0.0, f"Same Nadi ({b_nadi}) creates Nadi Dosha."

matching_service = KundliMatchingService()
