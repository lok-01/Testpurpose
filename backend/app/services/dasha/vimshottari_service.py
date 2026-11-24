from datetime import datetime, timedelta
from typing import List, Dict, Any
from app.services.nakshatra import get_nakshatra_info

DASHA_LORDS = [
    {"planet": "Ketu", "years": 7.0},
    {"planet": "Venus", "years": 20.0},
    {"planet": "Sun", "years": 6.0},
    {"planet": "Moon", "years": 10.0},
    {"planet": "Mars", "years": 7.0},
    {"planet": "Rahu", "years": 18.0},
    {"planet": "Jupiter", "years": 16.0},
    {"planet": "Saturn", "years": 19.0},
    {"planet": "Mercury", "years": 17.0},
]

YEAR_DAYS = 365.2425  # Tropical/standard solar year length

PLANET_ABBR = {
    "Ketu": "Ke",
    "Venus": "Ve",
    "Sun": "Su",
    "Moon": "Mo",
    "Mars": "Ma",
    "Rahu": "Ra",
    "Jupiter": "Ju",
    "Saturn": "Sa",
    "Mercury": "Me",
}

def format_years_to_ymd(years_val: float) -> str:
    total_days = max(0.0, years_val) * YEAR_DAYS
    y = int(total_days // YEAR_DAYS)
    rem = total_days % YEAR_DAYS
    m = int(rem // 30.437)
    d = int(round(rem % 30.437))
    return f"{y}y {m}m {d}d"

class VimshottariDashaService:
    def calculate_dasha_timeline(
        self,
        birth_datetime: datetime,
        moon_sidereal_longitude: float,
        target_date: datetime = None
    ) -> Dict[str, Any]:
        """
        Calculates complete Vimshottari Dasha system (Mahadasha, Antardasha, Pratyantardasha)
        and identifies current running period.
        """
        now = target_date or datetime.utcnow()
        nak_info = get_nakshatra_info(moon_sidereal_longitude)
        nak_name = nak_info["name"]
        starting_lord = nak_info["lord"]
        
        # Elapsed fraction inside birth nakshatra
        deg_in_nak = nak_info["degree_in_nakshatra"]
        total_span = nak_info["total_span"]
        elapsed_fraction = deg_in_nak / total_span
        balance_fraction = 1.0 - elapsed_fraction

        # Locate starting planet index in 9-lord cycle
        start_idx = next(i for i, d in enumerate(DASHA_LORDS) if d["planet"] == starting_lord)
        start_years = DASHA_LORDS[start_idx]["years"]
        balance_years = balance_fraction * start_years

        timeline = []
        current_cursor = birth_datetime
        
        current_md = ""
        current_ad = ""
        current_pd = ""

        # First Mahadasha (balance period)
        first_span_days = balance_years * YEAR_DAYS
        first_end = current_cursor + timedelta(days=first_span_days)
        
        # Generate 120-year cycle of 9 Mahadashas
        for i in range(9):
            idx = (start_idx + i) % 9
            d_info = DASHA_LORDS[idx]
            planet = d_info["planet"]
            full_years = d_info["years"]
            
            if i == 0:
                duration_years = balance_years
                md_start = current_cursor
                md_end = first_end
            else:
                duration_years = full_years
                md_start = current_cursor
                md_end = md_start + timedelta(days=duration_years * YEAR_DAYS)

            is_md_current = (md_start <= now <= md_end)
            if is_md_current:
                current_md = planet

            # Generate Antardashas for this Mahadasha
            antardashas = self._calculate_antardashas(
                md_planet_idx=idx,
                md_duration_years=duration_years,
                md_start=md_start,
                is_balance_first_md=(i == 0),
                elapsed_fraction=elapsed_fraction if i == 0 else 0.0,
                now=now
            )

            # If current MD, find current AD and PD
            if is_md_current:
                for ad in antardashas:
                    if ad["is_current"]:
                        current_ad = ad["planet"]
                        for pd in (ad.get("sub_periods") or []):
                            if pd["is_current"]:
                                current_pd = pd["planet"]
                                break
                        break

            abbr = PLANET_ABBR.get(planet, planet[:2])
            timeline.append({
                "planet": planet,
                "abbr": abbr,
                "start_date": md_start.strftime("%Y-%m-%d"),
                "end_date": md_end.strftime("%Y-%m-%d"),
                "start_year": md_start.year,
                "end_year": md_end.year,
                "duration_years": round(duration_years, 3),
                "parashara_display": f"{abbr}: {md_end.year}",
                "is_current": is_md_current,
                "sub_periods": antardashas,
            })

            current_cursor = md_end

        balance_ymd = format_years_to_ymd(balance_years)
        return {
            "birth_nakshatra": nak_name,
            "birth_nakshatra_lord": starting_lord,
            "birth_nakshatra_pada": nak_info.get("pada", 1),
            "moon_longitude": moon_sidereal_longitude,
            "starting_mahadasha_lord": starting_lord,
            "balance_years": round(balance_years, 3),
            "balance_ymd": balance_ymd,
            "formatted_balance": f"{starting_lord} – {round(balance_years, 2)} years ({balance_ymd})",
            "current_mahadasha": current_md,
            "current_antardasha": current_ad,
            "current_pratyantardasha": current_pd,
            "dashas": timeline,
        }

    def _calculate_antardashas(
        self,
        md_planet_idx: int,
        md_duration_years: float,
        md_start: datetime,
        is_balance_first_md: bool,
        elapsed_fraction: float,
        now: datetime
    ) -> List[Dict[str, Any]]:
        antardashas = []
        md_planet_years = DASHA_LORDS[md_planet_idx]["years"]
        cursor = md_start

        # Subdivisions start with the Mahadasha lord itself
        for j in range(9):
            ad_idx = (md_planet_idx + j) % 9
            ad_info = DASHA_LORDS[ad_idx]
            ad_planet = ad_info["planet"]
            ad_years = ad_info["years"]
            
            # Theoretical full AD duration
            full_ad_duration_years = (md_planet_years * ad_years) / 120.0
            
            # Handle starting MD balance adjustment if needed
            ad_span_years = (full_ad_duration_years * (1.0 - elapsed_fraction)) if is_balance_first_md else full_ad_duration_years
            ad_start = cursor
            ad_end = ad_start + timedelta(days=ad_span_years * YEAR_DAYS)
            is_ad_current = (ad_start <= now <= ad_end)

            # Generate Pratyantardashas (sub-sub periods)
            pratyantardashas = self._calculate_pratyantardashas(
                ad_idx=ad_idx,
                ad_duration_years=ad_span_years,
                ad_start=ad_start,
                now=now
            )

            ad_abbr = PLANET_ABBR.get(ad_planet, ad_planet[:2])
            md_abbr = PLANET_ABBR.get(DASHA_LORDS[md_planet_idx]["planet"], "")
            pair_abbr = f"{md_abbr}-{ad_abbr}"

            antardashas.append({
                "planet": ad_planet,
                "abbr": ad_abbr,
                "pair_abbr": pair_abbr,
                "start_date": ad_start.strftime("%Y-%m-%d"),
                "end_date": ad_end.strftime("%Y-%m-%d"),
                "start_year": ad_start.year,
                "end_year": ad_end.year,
                "duration_years": round(ad_span_years, 3),
                "parashara_display": f"{pair_abbr}: {ad_end.strftime('%Y-%m')}",
                "is_current": is_ad_current,
                "sub_periods": pratyantardashas,
            })
            cursor = ad_end

        return antardashas

    def _calculate_pratyantardashas(
        self,
        ad_idx: int,
        ad_duration_years: float,
        ad_start: datetime,
        now: datetime
    ) -> List[Dict[str, Any]]:
        pratyantardashas = []
        cursor = ad_start

        for k in range(9):
            pd_idx = (ad_idx + k) % 9
            pd_info = DASHA_LORDS[pd_idx]
            pd_planet = pd_info["planet"]
            pd_years = pd_info["years"]

            pd_duration_years = (ad_duration_years * pd_years) / 120.0
            pd_start = cursor
            pd_end = pd_start + timedelta(days=pd_duration_years * YEAR_DAYS)
            is_pd_current = (pd_start <= now <= pd_end)

            pratyantardashas.append({
                "planet": pd_planet,
                "start_date": pd_start.strftime("%Y-%m-%d"),
                "end_date": pd_end.strftime("%Y-%m-%d"),
                "duration_years": round(pd_duration_years, 3),
                "is_current": is_pd_current,
            })
            cursor = pd_end

        return pratyantardashas

dasha_service = VimshottariDashaService()
