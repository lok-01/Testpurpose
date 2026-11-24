# TESTING GUIDE & QA PROTOCOL

## AstroRize Vedic Research Lab

This guide describes how to run automated unit, integration, and verification tests for the calculation engines.

---

### 1. Test Environment Setup
The backend runs on Python 3.11 with `pytest`.
```powershell
cd astrorize-vedic-research-lab/backend
& "C:\Users\balok\AppData\Local\Programs\Python\Python311\python.exe" -m pytest -v
```

---

### 2. Verification Philosophy
- A test does **NOT** pass simply because code completes without throwing an exception.
- Tests verify output against independently known ephemeris and classical Vedic reference positions within specific angular tolerances:
  - **Planetary Longitude**: Tolerance $\le 0.001^\circ$ (approx 3.6 arcseconds) for Swiss Ephemeris.
  - **Lagna (Ascendant)**: Tolerance $\le 0.01^\circ$.
  - **Ayanamsa**: Tolerance $\le 0.0001^\circ$.
  - **Nakshatra & Pada**: Exact integer matching.
  - **Dasha Dates**: Date calculation accuracy within 1 day across 120-year cycle.
  - **Ashtakoota Score**: Exact point match against traditional matching tables.

---

### 3. Automated Test Suite Modules
- `test_ephemeris.py`: Validates Swiss Ephemeris library, Julian day, Delta T, Lahiri ayanamsa.
- `test_planetary.py`: Validates geocentric sidereal planetary positions, retrograde speed, dignities.
- `test_houses.py`: Validates Lagna and Whole Sign house cusps.
- `test_divisional.py`: Validates D9 Navamsha and higher Vargas D2-D60.
- `test_nakshatra.py`: Validates 27 Nakshatras and 108 Pada boundaries.
- `test_dasha.py`: Validates Vimshottari Mahadasha balance and subperiods.
- `test_panchang.py`: Validates Tithi, Vara, Yoga, and Karana.
- `test_yogas_doshas.py`: Validates rule triggers and cancellations.
- `test_matching.py`: Ashtakoota compatibility scoring.
- `test_transits.py`: Real-time planetary transits.
- `test_api.py`: FastAPI endpoints and data contracts.
