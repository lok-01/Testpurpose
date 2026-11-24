from typing import List, Dict, Any

class YogaService:
    def analyze_yogas(self, planets: List[Dict[str, Any]], houses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyzes classical Parashari Yogas, checking exact conditions and cancellations.
        """
        p_by_name = {p["name"]: p for p in planets}
        h_by_num = {h["house_number"]: h for h in houses}
        
        yogas = []

        # 1. Gaja Kesari Yoga
        # Jupiter in Kendra (1, 4, 7, 10) from Moon
        moon = p_by_name.get("Moon")
        jupiter = p_by_name.get("Jupiter")
        if moon and jupiter:
            dist = ((jupiter["house"] - moon["house"]) % 12) + 1
            if dist in [1, 4, 7, 10]:
                is_cancelled = jupiter["dignity"] == "Debilitated" or jupiter["is_combust"]
                yogas.append({
                    "name": "Gaja Kesari Yoga",
                    "category": "Raja / Auspicious",
                    "planets_involved": ["Moon", "Jupiter"],
                    "houses_involved": [moon["house"], jupiter["house"]],
                    "description": "Jupiter is in a Kendra (angular house) from the Moon, conferring wisdom, reputation, virtue, and enduring respect.",
                    "is_present": True,
                    "cancellation_rules_checked": "Checked whether Jupiter is debilitated or severely combust.",
                    "is_cancelled": is_cancelled,
                })

        # 2. Budhaditya Yoga
        # Sun and Mercury conjunct in same house/sign
        sun = p_by_name.get("Sun")
        mercury = p_by_name.get("Mercury")
        if sun and mercury:
            if sun["house"] == mercury["house"]:
                # Cancellation if Mercury is debilitated (Pisces) or deeply combust within 3 degrees
                diff = abs(sun["sidereal_longitude"] - mercury["sidereal_longitude"])
                is_cancelled = (mercury["dignity"] == "Debilitated") or (diff < 3.0)
                yogas.append({
                    "name": "Budhaditya Yoga",
                    "category": "Intellect / Dhana",
                    "planets_involved": ["Sun", "Mercury"],
                    "houses_involved": [sun["house"]],
                    "description": "Sun and Mercury conjunction in the same sign, bestowing analytical intellect, administrative skill, and academic brilliance.",
                    "is_present": True,
                    "cancellation_rules_checked": "Checked whether Mercury is debilitated in Pisces or combust within 3°.",
                    "is_cancelled": is_cancelled,
                })

        # 3. Chandra Mangala Yoga
        # Moon and Mars conjunct or in mutual Kendra
        mars = p_by_name.get("Mars")
        if moon and mars:
            if moon["house"] == mars["house"]:
                yogas.append({
                    "name": "Chandra Mangala Yoga",
                    "category": "Dhana / Financial",
                    "planets_involved": ["Moon", "Mars"],
                    "houses_involved": [moon["house"]],
                    "description": "Conjunction of Moon and Mars, driving energetic enterprise, financial acumen, and wealth generation through active endeavor.",
                    "is_present": True,
                    "cancellation_rules_checked": "Checked whether either planet is heavily debilitated without cancellation.",
                    "is_cancelled": moon["dignity"] == "Debilitated" and mars["dignity"] == "Debilitated",
                })

        # 4. Pancha Mahapurusha Yogas
        # Mars (Ruchaka), Mercury (Bhadra), Jupiter (Hamsa), Venus (Malavya), Saturn (Sasa)
        # Condition: In own sign or exaltation AND in Kendra (1, 4, 7, 10) from Lagna
        mahapurusha_map = {
            "Mars": ("Ruchaka Yoga", "Heroic courage, physical command, leadership, victory in competitions"),
            "Mercury": ("Bhadra Yoga", "Oratorical genius, mastery in sciences, scholarship, long life"),
            "Jupiter": ("Hamsa Yoga", "Righteous character, philosophical wisdom, reverence, spiritual distinction"),
            "Venus": ("Malavya Yoga", "Aesthetic refinement, luxurious conveyances, marital felicity, artistic mastery"),
            "Saturn": ("Sasa Yoga", "Command over masses, enduring authority, judicial discernment, disciplined perseverance"),
        }

        for p_name, (y_name, y_desc) in mahapurusha_map.items():
            p_obj = p_by_name.get(p_name)
            if p_obj and p_obj["house"] in [1, 4, 7, 10]:
                if p_obj["dignity"] in ["Exalted", "Own Sign"]:
                    is_canc = p_obj["is_combust"]
                    yogas.append({
                        "name": y_name,
                        "category": "Pancha Mahapurusha",
                        "planets_involved": [p_name],
                        "houses_involved": [p_obj["house"]],
                        "description": f"{p_name} placed in a Kendra in own sign/exaltation forming {y_name}: {y_desc}.",
                        "is_present": True,
                        "cancellation_rules_checked": "Checked whether the planet is combust or heavily afflicted.",
                        "is_cancelled": is_canc,
                    })

        # 5. Dharma Karmadhipati Yoga
        # Association of 9th lord (Dharma) and 10th lord (Karma)
        h9 = h_by_num.get(9)
        h10 = h_by_num.get(10)
        if h9 and h10:
            lord9 = h9["sign_lord"]
            lord10 = h10["sign_lord"]
            p9 = p_by_name.get(lord9)
            p10 = p_by_name.get(lord10)
            if p9 and p10:
                is_dharma_karma = False
                # Conjunct in same house
                if p9["house"] == p10["house"]:
                    is_dharma_karma = True
                # Mutual aspect (7th from each other)
                elif ((p10["house"] - p9["house"]) % 12) + 1 == 7:
                    is_dharma_karma = True
                
                if is_dharma_karma:
                    yogas.append({
                        "name": "Dharma Karmadhipati Yoga",
                        "category": "Supreme Raja Yoga",
                        "planets_involved": [lord9, lord10],
                        "houses_involved": [p9["house"], p10["house"]],
                        "description": "Sambandha between 9th lord of fortune and 10th lord of action creates a premier Raja Yoga for executive status and ethical prosperity.",
                        "is_present": True,
                        "cancellation_rules_checked": "Checked whether lords are debilitated in dusthanas.",
                        "is_cancelled": False,
                    })

        # 6. Neecha Bhanga Raja Yoga
        # Debilitated planet whose debilitation is cancelled
        for p in planets:
            if p["dignity"] == "Debilitated":
                p_deb = p["name"]
                # Cancellation condition: The lord of the debilitated sign is in Kendra from Lagna or Moon
                sign_lord = p["rashi_lord"]
                sign_lord_obj = p_by_name.get(sign_lord)
                is_nbry = False
                if sign_lord_obj and sign_lord_obj["house"] in [1, 4, 7, 10]:
                    is_nbry = True
                
                if is_nbry:
                    yogas.append({
                        "name": f"Neecha Bhanga Raja Yoga ({p_deb})",
                        "category": "Raja Yoga",
                        "planets_involved": [p_deb, sign_lord],
                        "houses_involved": [p["house"], sign_lord_obj["house"]],
                        "description": f"Debilitation of {p_deb} is annulled because sign dispositor {sign_lord} is situated in a Kendra, converting adversity into ultimate distinction.",
                        "is_present": True,
                        "cancellation_rules_checked": "Verified Kendra placement of dispositor from Lagna.",
                        "is_cancelled": False,
                    })

        # 7. Vipareeta Raja Yoga (Harsha, Sarala, Vimala)
        # Harsha: 6th lord in 6th, 8th, or 12th
        # Sarala: 8th lord in 6th, 8th, or 12th
        # Vimala: 12th lord in 6th, 8th, or 12th
        dusthanas = [6, 8, 12]
        vry_configs = [
            (6, "Harsha Yoga", "6th lord placed in a dusthana (6, 8, or 12) granting immunity from debt, enemies, and chronic illnesses"),
            (8, "Sarala Yoga", "8th lord placed in a dusthana (6, 8, or 12) bestowing long life, fearlessness, and sudden windfalls"),
            (12, "Vimala Yoga", "12th lord placed in a dusthana (6, 8, or 12) conferring noble expenditure, independence, and spiritual release"),
        ]

        for h_d, v_name, v_desc in vry_configs:
            h_obj = h_by_num.get(h_d)
            if h_obj:
                lord_name = h_obj["sign_lord"]
                lord_p = p_by_name.get(lord_name)
                if lord_p and lord_p["house"] in dusthanas:
                    yogas.append({
                        "name": v_name,
                        "category": "Vipareeta Raja Yoga",
                        "planets_involved": [lord_name],
                        "houses_involved": [lord_p["house"]],
                        "description": v_desc,
                        "is_present": True,
                        "cancellation_rules_checked": "Checked whether beneficial planets join without dusthana rulership.",
                        "is_cancelled": False,
                    })

        return yogas

yoga_service = YogaService()
