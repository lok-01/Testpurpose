from datetime import datetime
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.verification import VerificationCase
from app.services.swiss_ephemeris import swe_engine
from app.services.planetary_positions import planetary_service
from app.services.birth_chart import house_service
from app.utils.time_conversion import parse_local_to_utc, datetime_to_julian_day_ut

# Standard reference cases (Ramanujan, Indira Gandhi, Standard Ephemeris benchmarks)
DEFAULT_VERIFICATION_BENCHMARKS = [
    {
        "test_name": "Srinivasa Ramanujan Ephemeris Baseline",
        "reference_source": "BV Raman Classical Dataset & Swiss Ephemeris Standard",
        "profile_details": {
            "name": "Srinivasa Ramanujan",
            "date": "1887-12-22",
            "time": "17:20:00",
            "latitude": 11.3410,
            "longitude": 77.7172,
            "timezone_str": "Asia/Kolkata",
            "timezone_offset": 5.5,
            "ayanamsa": "LAHIRI",
        },
        "expected_values": {
            "Sun_longitude": 248.5,        # Approx Sagittarius 8°
            "Moon_longitude": 328.0,       # Approx Pisces 8° (Uttara Bhadrapada)
            "Jupiter_longitude": 204.0,    # Approx Libra 24°
            "Saturn_longitude": 105.0,     # Approx Cancer 15°
        },
        "tolerance": 0.5,  # degrees
        "notes": "Historical benchmark verifying sidereal planetary positions against classical records."
    },
    {
        "test_name": "Modern J2000 Benchmark Baseline",
        "reference_source": "Astrodienst AG Official Ephemeris Reference",
        "profile_details": {
            "name": "J2000 Standard Epoch",
            "date": "2000-01-01",
            "time": "12:00:00",
            "latitude": 0.0,
            "longitude": 0.0,
            "timezone_str": "UTC",
            "timezone_offset": 0.0,
            "ayanamsa": "LAHIRI",
        },
        "expected_values": {
            "Sun_longitude": 256.36,       # Approx Sidereal Sagittarius 16°21'
            "Moon_longitude": 213.56,      # Approx Sidereal Scorpio 3°34'
        },
        "tolerance": 0.05,
        "notes": "Precision test verifying Julian Day 2451545.0 and Lahiri ayanamsa."
    }
]

class VerificationService:
    def __init__(self, engine=None):
        self.engine = engine or swe_engine

    def run_case_verification(self, case: VerificationCase, db: Session = None) -> Dict[str, Any]:
        """
        Executes a verification test by calculating real values and strictly measuring differences
        against expected values within tolerance.
        """
        p_info = case.profile_details
        dt_utc = parse_local_to_utc(
            p_info["date"],
            p_info["time"],
            p_info.get("timezone_str", "UTC"),
            p_info.get("timezone_offset", 0.0)
        )
        jd_ut = datetime_to_julian_day_ut(dt_utc)
        
        # Configure Ayanamsa
        ayan_name = p_info.get("ayanamsa", "LAHIRI")
        self.engine._configure_sidereal(ayan_name)
        
        # Calculate real planetary positions
        # Using Ascendant calculated with whole sign
        asc_long, cusps, mc, armc = self.engine.calculate_houses(jd_ut, p_info["latitude"], p_info["longitude"])
        lagna_rashi_num = int(asc_long // 30.0) + 1
        planets = planetary_service.calculate_all_planets(jd_ut, lagna_rashi_num)
        
        p_dict = {p["name"]: p for p in planets}

        actual_values = {}
        differences = {}
        all_passed = True
        max_diff = 0.0

        for key, exp_val in case.expected_values.items():
            if "_longitude" in key:
                p_name = key.split("_")[0]
                if p_name in p_dict:
                    act_val = p_dict[p_name]["sidereal_longitude"]
                    actual_values[key] = round(act_val, 4)
                    
                    diff = abs(act_val - exp_val)
                    if diff > 180.0:
                        diff = 360.0 - diff
                    differences[key] = round(diff, 4)
                    if diff > max_diff:
                        max_diff = diff
                    if diff > case.tolerance:
                        all_passed = False

        status = "PASSED" if all_passed else "FAILED"
        case.actual_values = actual_values
        case.differences = differences
        case.status = status
        case.executed_at = datetime.utcnow()

        if db:
            db.commit()
            db.refresh(case)

        return {
            "case_id": case.id,
            "test_name": case.test_name,
            "status": status,
            "max_difference": round(max_diff, 4),
            "tolerance": case.tolerance,
            "expected_values": case.expected_values,
            "actual_values": actual_values,
            "differences": differences,
        }

    def seed_default_benchmarks(self, db: Session):
        """
        Seeds standard astronomical test benchmarks if none exist.
        """
        existing = db.query(VerificationCase).count()
        if existing == 0:
            for b in DEFAULT_VERIFICATION_BENCHMARKS:
                vc = VerificationCase(
                    test_name=b["test_name"],
                    reference_source=b["reference_source"],
                    profile_details=b["profile_details"],
                    expected_values=b["expected_values"],
                    tolerance=b["tolerance"],
                    notes=b["notes"],
                    status="PENDING",
                )
                db.add(vc)
            db.commit()

verification_service = VerificationService()
