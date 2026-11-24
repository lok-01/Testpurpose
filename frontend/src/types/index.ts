export interface BirthProfile {
  id: number;
  name: string;
  gender?: string;
  date_of_birth: string;
  time_of_birth: string;
  birthplace: string;
  country?: string;
  state?: string;
  city?: string;
  latitude: number;
  longitude: number;
  timezone_str: string;
  timezone_offset: number;
  accuracy_notes?: string;
  created_at: string;
}

export interface PlanetPosition {
  name: string;
  id: number;
  tropical_longitude: number;
  sidereal_longitude: number;
  latitude: number;
  speed: number;
  is_retrograde: boolean;
  rashi: string;
  rashi_number: number;
  rashi_lord: string;
  degree_in_rashi: number;
  dms: string;
  parashara_dms?: string;
  chara_karaka?: string;
  nakshatra: string;
  nakshatra_number: number;
  pada: number;
  nakshatra_lord: string;
  house: number;
  is_combust: boolean;
  dignity: string;
}

export interface HouseCusp {
  house_number: number;
  sign: string;
  sign_number: number;
  sign_lord: string;
  start_degree: number;
  cusp_degree: number;
  occupants: string[];
  aspecting_planets: string[];
}

export interface ChartSummary {
  lagna_longitude: number;
  lagna_rashi: string;
  lagna_rashi_number: number;
  lagna_degree: number;
  lagna_dms: string;
  lagna_parashara_dms?: string;
  lagna_lord: string;
  lagna_nakshatra: string;
  lagna_pada: number;
  ayanamsa_value: number;
  ayanamsa_name: string;
  engine_name: string;
  engine_version: string;
}

export interface BirthChartData {
  chart_summary: ChartSummary;
  planets: PlanetPosition[];
  houses: HouseCusp[];
}

export interface VimshottariDashaLevel {
  planet: string;
  abbr?: string;
  start_date: string;
  end_date: string;
  start_year?: number;
  end_year?: number;
  duration_years: number;
  parashara_display?: string;
  pair_abbr?: string;
  is_current: boolean;
  sub_periods?: VimshottariDashaLevel[];
}

export interface DashaData {
  birth_nakshatra: string;
  birth_nakshatra_lord?: string;
  birth_nakshatra_pada?: number;
  moon_longitude: number;
  starting_mahadasha_lord: string;
  balance_years: number;
  balance_ymd?: string;
  formatted_balance?: string;
  current_mahadasha: string;
  current_antardasha: string;
  current_pratyantardasha: string;
  dashas: VimshottariDashaLevel[];
}

export interface PanchangData {
  date: string;
  tithi: string;
  tithi_number: number;
  paksha: string;
  tithi_progress_pct: number;
  vara: string;
  nakshatra: string;
  nakshatra_number: number;
  yoga: string;
  yoga_number: number;
  karana: string;
  sunrise: string;
  sunset: string;
  moonrise?: string;
  moonset?: string;
}

export interface YogaDetail {
  name: string;
  category: string;
  planets_involved: string[];
  houses_involved: number[];
  description: string;
  is_present: boolean;
  cancellation_rules_checked: string;
  is_cancelled: boolean;
}

export interface DoshaDetail {
  name: string;
  is_present: boolean;
  severity: string;
  planets_involved: string[];
  houses_involved: number[];
  rule_applied: string;
  cancellation_factors: string[];
  is_cancelled: boolean;
  explanation: string;
}

export interface AshtakootaMatchingData {
  varna: any;
  vashya: any;
  tara: any;
  yoni: any;
  graha_maitri: any;
  gana: any;
  bhakoot: any;
  nadi: any;
  total_score: number;
  max_score: number;
  recommendation: string;
  manglik_boy: boolean;
  manglik_girl: boolean;
  matching_summary: string;
}

export interface VerificationCase {
  id: number;
  test_name: string;
  reference_source: string;
  profile_details: any;
  expected_values: any;
  actual_values?: any;
  differences?: any;
  tolerance: number;
  status: string;
  notes?: string;
  executed_at?: string;
}

export interface DashboardSummary {
  engine_name: string;
  engine_version: string;
  active_ayanamsa: string;
  ephemeris_available: boolean;
  total_birth_charts: number;
  total_calculations_run: number;
  total_test_cases: number;
  passed_test_cases: number;
  failed_test_cases: number;
  recent_profiles: any[];
  recent_calculations: any[];
}
