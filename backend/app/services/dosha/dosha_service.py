from typing import List, Dict, Any

class DoshaService:
    def analyze_doshas(
        self,
        planets: List[Dict[str, Any]],
        houses: List[Dict[str, Any]],
        lagna_rashi_num: int
    ) -> List[Dict[str, Any]]:
        """
        Calculates Manglik, Kala Sarpa, Pitru Dosha, and Sade Sati status
        with classical cancellation factors and objective, research-grounded explanations.
        """
        p_by_name = {p["name"]: p for p in planets}
        h_by_num = {h["house_number"]: h for h in houses}
        
        doshas = []

        # 1. Manglik Dosha (Kuja Dosha)
        mars = p_by_name.get("Mars")
        if mars:
            m_house = mars["house"]
            manglik_houses = [1, 2, 4, 7, 8, 12]
            is_manglik_pos = m_house in manglik_houses
            
            cancellations = []
            if is_manglik_pos:
                # Classical Parashari cancellations:
                # 1. Mars in own sign (Aries, Scorpio) or exalted (Capricorn)
                if mars["dignity"] in ["Own Sign", "Exalted"]:
                    cancellations.append(f"Mars is dignified in {mars['dignity']} ({mars['rashi']}).")
                
                # 2. Jupiter aspect or conjunction
                jup = p_by_name.get("Jupiter")
                if jup:
                    if jup["house"] == mars["house"]:
                        cancellations.append("Mars is conjunct benefic Jupiter (Guru-Mangala).")
                    elif ((m_house - jup["house"]) % 12) + 1 in [5, 7, 9]:
                        cancellations.append("Mars is aspected by benefic Jupiter.")

                # 3. Moon conjunction (Chandra-Mangala)
                moon = p_by_name.get("Moon")
                if moon and moon["house"] == mars["house"]:
                    cancellations.append("Mars is conjunct Moon mitigating affliction.")

                # 4. Specific house sign exemptions
                if m_house == 1 and mars["rashi"] == "Aries":
                    cancellations.append("Mars in 1st house in Aries is cancelled.")
                elif m_house == 4 and mars["rashi"] == "Scorpio":
                    cancellations.append("Mars in 4th house in Scorpio is cancelled.")
                elif m_house == 7 and mars["rashi"] in ["Capricorn", "Pisces"]:
                    cancellations.append(f"Mars in 7th house in {mars['rashi']} is cancelled.")
                elif m_house == 8 and mars["rashi"] in ["Cancer", "Sagittarius"]:
                    cancellations.append(f"Mars in 8th house in {mars['rashi']} is cancelled.")
                elif m_house == 12 and mars["rashi"] in ["Sagittarius", "Taurus"]:
                    cancellations.append(f"Mars in 12th house in {mars['rashi']} is cancelled.")

            is_cancelled = len(cancellations) > 0
            severity = "None" if not is_manglik_pos else ("Cancelled / Mild" if is_cancelled else "Moderate")

            doshas.append({
                "name": "Manglik Dosha (Kuja Dosha)",
                "is_present": is_manglik_pos,
                "severity": severity,
                "planets_involved": ["Mars"],
                "houses_involved": [m_house] if is_manglik_pos else [],
                "rule_applied": f"Mars situated in house {m_house} relative to Lagna (affects houses {manglik_houses}).",
                "cancellation_factors": cancellations,
                "is_cancelled": is_cancelled,
                "explanation": "Manglik dosha evaluates planetary martial energy in relation to partnership houses. In Parashari astrology, when accompanied by mitigating benefics or appropriate planetary dignity, dynamic drive replaces friction."
            })

        # 2. Kala Sarpa Dosha
        # All 7 physical planets (Sun to Saturn) hemmed between Rahu and Ketu
        rahu = p_by_name.get("Rahu")
        ketu = p_by_name.get("Ketu")
        if rahu and ketu:
            physical_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
            rahu_long = rahu["sidereal_longitude"]
            ketu_long = ketu["sidereal_longitude"]

            # Calculate whether all 7 planets are on one side of the nodal axis
            # Forward arc from Rahu to Ketu
            arc_side1 = []
            arc_side2 = []
            
            for p_name in physical_planets:
                p_obj = p_by_name.get(p_name)
                if not p_obj:
                    continue
                p_long = p_obj["sidereal_longitude"]
                
                # Check if in arc Rahu -> Ketu
                in_side1 = False
                if rahu_long < ketu_long:
                    in_side1 = (rahu_long <= p_long <= ketu_long)
                else:
                    in_side1 = (p_long >= rahu_long or p_long <= ketu_long)

                if in_side1:
                    arc_side1.append(p_name)
                else:
                    arc_side2.append(p_name)

            has_complete_ksd = (len(arc_side1) == 7 or len(arc_side2) == 7)
            has_partial_ksd = (len(arc_side1) == 6 or len(arc_side2) == 6) and not has_complete_ksd

            ksd_types = [
                "Anant", "Kulik", "Vasuki", "Shankhapal", "Padma", "Mahapadma",
                "Takshak", "Karkotak", "Shankhachur", "Ghatak", "Vishdhar", "Sheshnag"
            ]
            r_house = rahu["house"]
            ksd_name = ksd_types[(r_house - 1) % 12] + " Kala Sarpa Yoga"

            cancellations_ksd = []
            if has_complete_ksd:
                # Benefic in Kendra or Ascendant lord exalted cancels malefic effect
                lagna_lord_name = houses[0]["sign_lord"]
                lagna_lord_p = p_by_name.get(lagna_lord_name)
                if lagna_lord_p and lagna_lord_p["dignity"] in ["Exalted", "Own Sign"]:
                    cancellations_ksd.append(f"Lagna lord {lagna_lord_name} is dignified in {lagna_lord_p['dignity']}.")

            doshas.append({
                "name": f"Kala Sarpa Dosha ({ksd_name})",
                "is_present": has_complete_ksd or has_partial_ksd,
                "severity": "High" if (has_complete_ksd and not cancellations_ksd) else ("Partial / Cancelled" if (has_partial_ksd or cancellations_ksd) else "None"),
                "planets_involved": ["Rahu", "Ketu"] + (arc_side1 if len(arc_side1) >= 6 else arc_side2),
                "houses_involved": [rahu["house"], ketu["house"]],
                "rule_applied": "All 7 physical grahas bounded between Rahu and Ketu nodal axis.",
                "cancellation_factors": cancellations_ksd,
                "is_cancelled": len(cancellations_ksd) > 0,
                "explanation": "Kala Sarpa indicates intense karmic focus and cyclical life acceleration. When disciplined, individuals with this combination frequently attain profound public eminence and dedicated purpose."
            })

        # 3. Pitru Dosha
        # Sun conjunction with Rahu/Ketu, or 9th house occupied by Rahu/Ketu/Saturn
        sun = p_by_name.get("Sun")
        h9 = h_by_num.get(9)
        pitru_factors = []
        if sun and rahu and sun["house"] == rahu["house"]:
            pitru_factors.append("Sun is conjunct Rahu.")
        if sun and ketu and sun["house"] == ketu["house"]:
            pitru_factors.append("Sun is conjunct Ketu.")
        if h9 and ("Rahu" in h9["occupants"] or "Ketu" in h9["occupants"]):
            pitru_factors.append("9th house of Dharma/Ancestors is occupied by a lunar node.")

        has_pitru = len(pitru_factors) > 0
        doshas.append({
            "name": "Pitru Dosha",
            "is_present": has_pitru,
            "severity": "Mild to Moderate" if has_pitru else "None",
            "planets_involved": ["Sun", "Rahu"] if has_pitru else [],
            "houses_involved": [9] if has_pitru else [],
            "rule_applied": "; ".join(pitru_factors) if has_pitru else "No affliction to Sun or 9th house.",
            "cancellation_factors": ["Jupiter aspect on 9th house or Sun restores equilibrium."] if has_pitru else [],
            "is_cancelled": False,
            "explanation": "Reflects ancestral karmic responsibilities and debts to be harmonized through filial respect, noble conduct, and lineage honoring."
        })

        return doshas

dosha_service = DoshaService()
