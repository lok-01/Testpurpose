from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class CalculationSettingsSchema(BaseModel):
    ayanamsa: str = "LAHIRI"
    node_type: str = "TRUE_NODE"
    house_system: str = "WHOLE_SIGN"

class PlanetPositionSchema(BaseModel):
    name: str
    id: int
    tropical_longitude: float
    sidereal_longitude: float
    latitude: float
    speed: float
    is_retrograde: bool
    rashi: str
    rashi_number: int
    rashi_lord: str
    degree_in_rashi: float
    dms: str
    parashara_dms: Optional[str] = ""
    chara_karaka: Optional[str] = "-"
    nakshatra: str
    nakshatra_number: int
    pada: int
    nakshatra_lord: str
    house: int
    is_combust: bool
    dignity: str  # Exalted, Debilitated, Own, Moolatrikona, Friend, Neutral, Enemy

class HouseCuspSchema(BaseModel):
    house_number: int
    sign: str
    sign_number: int
    sign_lord: str
    start_degree: float
    cusp_degree: float
    occupants: List[str]
    aspecting_planets: List[str]

class ChartSummarySchema(BaseModel):
    lagna_longitude: float
    lagna_rashi: str
    lagna_rashi_number: int
    lagna_degree: float
    lagna_dms: str
    lagna_parashara_dms: Optional[str] = ""
    lagna_lord: str
    lagna_nakshatra: str
    lagna_pada: int
    ayanamsa_value: float
    ayanamsa_name: str
    engine_name: str = "Swiss Ephemeris"
    engine_version: str

class BirthChartResponse(BaseModel):
    chart_summary: ChartSummarySchema
    planets: List[PlanetPositionSchema]
    houses: List[HouseCuspSchema]

class DivisionalChartResponse(BaseModel):
    varga_name: str
    varga_division: int
    lagna_rashi: str
    lagna_rashi_number: int
    planets: List[Dict[str, Any]]
    houses: Dict[int, List[str]]

class VimshottariDashaLevel(BaseModel):
    planet: str
    abbr: Optional[str] = None
    start_date: str
    end_date: str
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    duration_years: float
    parashara_display: Optional[str] = None
    pair_abbr: Optional[str] = None
    is_current: bool = False
    sub_periods: Optional[List["VimshottariDashaLevel"]] = None

class DashaResponse(BaseModel):
    birth_nakshatra: str
    birth_nakshatra_lord: Optional[str] = None
    birth_nakshatra_pada: Optional[int] = None
    moon_longitude: float
    starting_mahadasha_lord: str
    balance_years: float
    balance_ymd: Optional[str] = None
    formatted_balance: Optional[str] = None
    current_mahadasha: str
    current_antardasha: str
    current_pratyantardasha: str
    dashas: List[VimshottariDashaLevel]

class PanchangResponse(BaseModel):
    date: str
    tithi: str
    tithi_number: int
    paksha: str
    tithi_progress_pct: float
    vara: str
    nakshatra: str
    nakshatra_number: int
    yoga: str
    yoga_number: int
    karana: str
    sunrise: str
    sunset: str
    moonrise: Optional[str] = None
    moonset: Optional[str] = None

class YogaDetailSchema(BaseModel):
    name: str
    category: str
    planets_involved: List[str]
    houses_involved: List[int]
    description: str
    is_present: bool
    cancellation_rules_checked: str
    is_cancelled: bool = False

class DoshaDetailSchema(BaseModel):
    name: str
    is_present: bool
    severity: str
    planets_involved: List[str]
    houses_involved: List[int]
    rule_applied: str
    cancellation_factors: List[str]
    is_cancelled: bool = False
    explanation: str

class AshtakootaMatchingResponse(BaseModel):
    varna: Dict[str, Any]
    vashya: Dict[str, Any]
    tara: Dict[str, Any]
    yoni: Dict[str, Any]
    graha_maitri: Dict[str, Any]
    gana: Dict[str, Any]
    bhakoot: Dict[str, Any]
    nadi: Dict[str, Any]
    total_score: float
    max_score: float = 36.0
    recommendation: str
    manglik_boy: bool
    manglik_girl: bool
    matching_summary: str
