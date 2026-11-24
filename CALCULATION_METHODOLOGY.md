# CALCULATION METHODOLOGY & MATHEMATICAL SPECIFICATION

## AstroRize Vedic Research Lab

This document defines the exact mathematical foundations, algorithms, and astronomical formulas implemented in the AstroRize Vedic Research Lab.

---

### 1. Ephemeris & Time Standard
- **Engine**: Swiss Ephemeris (`sweph`), version 2.10.03+.
- **Time Representation**:
  - Input: Local Civil Time (Year, Month, Day, Hour, Minute, Second).
  - Offset Determination: Explicit timezone offset handling (`pytz` with historical IANA database resolution).
  - Universal Time (UT): `UT = LocalTime - TimezoneOffset`.
  - Julian Day (UT): Calculated via `swe_julday(year, month, day, hour_float, swe.GREG_CAL)`.
  - Delta T: Dynamically computed by Swiss Ephemeris for Ephemeris Time (ET/TDT).

---

### 2. Sidereal Zodiac & Ayanamsa
- **Sidereal Mode**: Set via `swe_set_sid_mode(sid_mode, t0, ayan_t0)`.
- **Default Ayanamsa**: Lahiri (Chitrapaksha), `swe.SIDM_LAHIRI`.
- **Alternative Supported Ayanamsas**:
  - Raman (`swe.SIDM_RAMAN`)
  - Krishnamurti (KP) (`swe.SIDM_KRISHNAMURTI`)
  - Fagan-Bradley (`swe.SIDM_FAGAN_BRADLEY`)
  - Yukteshwar (`swe.SIDM_YUKTESHWAR`)
  - True Chitra (`swe.SIDM_TRUE_CITRA`)
- **Ayanamsa Calculation**:
  \[
  \text{Ayanamsa}(JD) = \text{swe\_get\_ayanamsa\_ut}(JD)
  \]
  \[
  \lambda_{\text{sidereal}} = (\lambda_{\text{tropical}} - \text{Ayanamsa}) \pmod{360^\circ}
  \]

---

### 3. Planetary Coordinates & Node Handling
- **Coordinate System**: Geocentric ecliptic longitudes and latitudes.
- **Flag configuration**: `swe.FLG_SIDEREAL | swe.FLG_SWIEPH | swe.FLG_SPEED`.
- **Lunar Nodes**:
  - True Node (`swe.TRUE_NODE`): Rahu is the true North Node; Ketu is opposite by exactly $180^\circ$:
    \[
    \lambda_{\text{Ketu}} = (\lambda_{\text{Rahu}} + 180^\circ) \pmod{360^\circ}
    \]
  - Mean Node (`swe.MEAN_NODE`): Available through engine settings.
- **Dignity & Relationships**:
  - Exaltation / Debilitation points based on Brihat Parashara Hora Shastra (BPHS).
  - Own sign, Moolatrikona, and Mitra/Shatru/Sama fivefold (Pancha-da) relationships.

---

### 4. Ascendant (Lagna) and House Calculations
- **Ascendant Calculation**: `swe_houses_ex(JD, lat, lon, b'W')` where 'W' is Whole Sign (or configurable 'P' for Placidus, 'E' for Equal).
- **Vedic Lagna**:
  - Tropical Ascendant is corrected by the active Ayanamsa:
  \[
  \text{Lagna}_{\text{sidereal}} = (\text{Lagna}_{\text{tropical}} - \text{Ayanamsa}) \pmod{360^\circ}
  \]
- **Whole Sign Houses (Parashari)**:
  - House 1 begins at $0^\circ$ of the Lagna Rashi.
  - House $N$ spans the entire sign $((\text{Lagna Rashi Index} + N - 1) \pmod{12})$.

---

### 5. Divisional Charts (Vargas D1 to D60)
Strict classical Parashari algorithms implemented:
- **D1 (Rashi)**: $\lfloor \lambda / 30^\circ \rfloor$
- **D2 (Hora)**: Sun/Moon halves based on Odd/Even signs.
- **D3 (Drekkana)**: 1st decan same sign, 2nd decan 5th sign, 3rd decan 9th sign.
- **D4 (Chaturthamsha)**: 1st, 4th, 7th, 10th signs.
- **D7 (Saptamsha)**: From same sign for odd; from 7th sign for even.
- **D9 (Navamsha)**:
  - Fire signs (Aries, Leo, Sag) start from Aries.
  - Earth signs (Taurus, Virgo, Cap) start from Capricorn.
  - Air signs (Gemini, Libra, Aqu) start from Libra.
  - Water signs (Cancer, Scorpio, Pis) start from Cancer.
- **D10 (Dashamsha)**: From same sign for odd; from 9th sign for even.
- **D12 (Dwadashamsha)**: Starts from the sign itself.
- **D16 (Shodashamsha)**: From Aries for movable, Leo for fixed, Sagittarius for dual.
- **D20 (Vimshamsha)**: From Aries for movable, Sagittarius for fixed, Leo for dual.
- **D24 (Chaturvimshamsha)**: From Leo for odd signs, Cancer for even signs.
- **D27 (Saptavimshamsha)**: From Aries for fire, Cancer for earth, Libra for air, Capricorn for water.
- **D30 (Trimshamsha)**: Unequal degree ruler mapping (Mars, Saturn, Jupiter, Mercury, Venus).
- **D40 (Khavedamsha)**: From Aries for odd signs, Libra for even signs.
- **D45 (Akshavedamsha)**: From Aries for movable, Leo for fixed, Sagittarius for dual.
- **D60 (Shashtiamsha)**: 60 divisions of $0.5^\circ$ with sign progression from the sign itself.

---

### 6. Vimshottari Dasha Engine
- Cycle of 120 solar years ruled by 9 grahas in classical sequence:
  Ketu (7), Venus (20), Sun (6), Moon (10), Mars (7), Rahu (18), Jupiter (16), Saturn (19), Mercury (17).
- Starting balance determined by exact Moon position in birth Nakshatra:
  \[
  \text{Fraction Elapsed} = \frac{\lambda_{\text{Moon}} \pmod{13^\circ 20'}}{13^\circ 20'}
  \]
  \[
  \text{Balance Remaining} = (1 - \text{Fraction Elapsed}) \times \text{Mahadasha Span}
  \]
- Antardasha and Pratyantardasha proportional subdivision:
  \[
  \text{Duration}_{sub} = \text{Duration}_{parent} \times \frac{\text{Years}_{sub}}{120}
  \]

---

### 7. Panchang Algorithms
- **Tithi**: $(\lambda_{\text{Moon}} - \lambda_{\text{Sun}}) \pmod{360^\circ} / 12^\circ$.
- **Vara**: Day of the week beginning from local sunrise.
- **Nakshatra**: $\lambda_{\text{Moon}} / (360^\circ / 27) = \lambda_{\text{Moon}} / 13^\circ 20'$.
- **Yoga**: $(\lambda_{\text{Sun}} + \lambda_{\text{Moon}}) \pmod{360^\circ} / 13^\circ 20'$.
- **Karana**: Half-tithi ($6^\circ$), 60 per lunar month (4 fixed, 7 repeating).
- **Sunrise/Sunset**: `swe_rise_trans()` with atmospheric refraction.
