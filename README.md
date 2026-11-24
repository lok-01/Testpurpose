# AstroRize Vedic Research Lab

A complete, high-precision Parashari Vedic Astrology Calculation Engine and Research Platform powered by **Swiss Ephemeris** with an integrated, chart-grounded **AI Astrology Chatbot**.

Developed as an independent local research and calculation verification laboratory before considering production integration into AstroRize.

---

## Key Features

1. **Mandatory Astronomical Core: Swiss Ephemeris (`sweph` 2.10.03+)**
   - High-precision planetary calculations using C calculation libraries and `pyswisseph` bindings.
   - Geocentric sidereal coordinates with customizable Ayanamsa (Lahiri Chitrapaksha by default, Raman, KP, True Chitra, Fagan-Bradley, Yukteshwar).
   - True Node calculation for Rahu and Ketu, with Mean Node option.
   - Zero approximations or dummy mock values.

2. **Complete Vedic Calculation Modules**
   - **D1 Rashi Chart & Whole Sign Bhava Cusps**: Lagna calculation, planetary dignities (Exalted, Debilitated, Own Sign, Moolatrikona), combustions, and classical planetary aspects.
   - **North & South Indian Kundli**: Interactive SVG rendering with clickable houses and planets.
   - **All 16 Classical Parashari Vargas (D1 to D60)**: D1 (Rashi), D2 (Hora), D3 (Drekkana), D4 (Chaturthamsha), D7 (Saptamsha), D9 (Navamsha), D10 (Dashamsha), D12 (Dwadashamsha), D16 (Shodashamsha), D20 (Vimshamsha), D24 (Chaturvimshamsha), D27 (Saptavimshamsha), D30 (Trimshamsha), D40 (Khavedamsha), D45 (Akshavedamsha), D60 (Shashtiamsha).
   - **27 Nakshatras & 108 Padas**: Boundary math, ruling planets, deities, and gunas.
   - **Vimshottari Dasha Engine**: 120-year cycle with Mahadasha, Antardasha, and Pratyantardasha derived from exact Moon position at birth.
   - **Astronomical Daily Panchang**: Tithi progress %, Vara, Nakshatra, Yoga, Karana, and Swiss Ephemeris sunrise/sunset times.
   - **Parashari Yoga Engine**: Gaja Kesari, Budhaditya, Chandra Mangala, Pancha Mahapurusha (Ruchaka, Bhadra, Hamsa, Malavya, Sasa), Dharma Karmadhipati, Neecha Bhanga Raja Yoga, and Vipareeta Raja Yoga (Harsha, Sarala, Vimala) with exact cancellation checks.
   - **Dosha Analysis Engine**: Manglik (Kuja) Dosha, Kala Sarpa Dosha (12 types), Pitru Dosha, and Saturn Sade Sati transit status with objective explanations.
   - **Ashtakoota 36-Point Kundli Matching**: Varna, Vashya, Tara, Yoni, Graha Maitri, Gana, Bhakoot, and Nadi with Dosha cancellation logic.
   - **Gochara Real-Time Transits**: Transits for any date relative to natal Moon and Lagna.
   - **Grounded Vedic AI Chatbot**: Integrates Ollama local LLM with fallback to deterministic Parashari rule engine. Grounds all answers directly in computed chart placements.
   - **Mandatory Calculation Verification Module**: Automated QA engine testing against independently verified reference datasets within configured angular tolerances.

---

## Architecture & Technology Stack

- **Backend**: Python 3.11, FastAPI, SQLAlchemy ORM, SQLite database, Pydantic V2, Swiss Ephemeris (`pyswisseph 2.10.3.2`).
- **Frontend**: React 18, TypeScript, Tailwind CSS, Vite, Lucide Icons.
- **Local AI**: Ollama HTTP integration (`llama3.2` or any local model) with built-in rule-based fallback.

---

## Directory Structure

```text
├── backend/
│   ├── app/
│   │   ├── api/                     # REST API routers
│   │   ├── models/                  # SQLite models
│   │   ├── schemas/                 # Pydantic schemas
│   │   ├── services/
│   │   │   ├── swiss_ephemeris/     # Core Swiss Ephemeris service
│   │   │   ├── birth_chart/         # Lagna & House calculations
│   │   │   ├── planetary_positions/ # Planetary engine & dignities
│   │   │   ├── divisional_charts/   # Vargas D1 through D60
│   │   │   ├── nakshatra/           # 27 Nakshatras & 108 Padas
│   │   │   ├── dasha/               # Vimshottari Dasha system
│   │   │   ├── panchang/            # Astronomical Panchang
│   │   │   ├── yoga/                # Parashari Yogas
│   │   │   ├── dosha/               # Doshas & cancellations
│   │   │   ├── kundli_matching/     # Ashtakoota 36-pt matching
│   │   │   ├── transit/             # Gochara transits
│   │   │   ├── ai_chat/             # Grounded AI Chatbot
│   │   │   └── verification/        # QA Verification engine
│   │   ├── utils/                   # Timezone & degree conversion
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   ├── tests/                       # Automated pytest suite (26 tests)
│   └── requirements.txt
├── frontend/                        # React + TypeScript + Tailwind UI
│   ├── src/
│   │   ├── charts/                  # North & South Indian Kundli
│   │   ├── services/api.ts          # API client
│   │   ├── types/index.ts           # Frontend contracts
│   │   ├── App.tsx                  # 17-section research interface
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── LICENSES.md                      # Swiss Ephemeris GPL & OSS licensing
├── CALCULATION_METHODOLOGY.md       # Mathematical & astrological specs
├── TESTING_GUIDE.md                 # QA and automated testing protocol
├── DEVELOPMENT_PROGRESS.md          # Implementation progress tracking
└── README.md
```

---

## Local Installation & Execution

### 1. Backend Setup (FastAPI & Swiss Ephemeris)
```powershell
cd astrorize-vedic-research-lab/backend

# Run tests to verify astronomical engine
& "C:\Users\balok\AppData\Local\Programs\Python\Python311\python.exe" -m pytest -v

# Start FastAPI backend server on port 8000
& "C:\Users\balok\AppData\Local\Programs\Python\Python311\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 2. Frontend Setup (React & Vite)
```powershell
cd astrorize-vedic-research-lab/frontend

# Install dependencies
npm install

# Start development server on port 3000
npm run dev
```

Open your browser at `http://localhost:3000` to access the lab dashboard.
API documentation is available at `http://127.0.0.1:8000/docs`.
