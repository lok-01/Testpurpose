from datetime import datetime
import pytz
import swisseph as swe

def parse_local_to_utc(date_str: str, time_str: str, timezone_str: str = "UTC", fallback_offset: float = 0.0) -> datetime:
    """
    Parses a local date (YYYY-MM-DD) and time (HH:MM:SS) string with timezone handling.
    Accurately resolves historical timezone offsets including DST transitions via pytz.
    """
    dt_naive = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
    
    try:
        tz = pytz.timezone(timezone_str)
        # localize handles historical daylight saving transitions
        dt_local = tz.localize(dt_naive, is_dst=None)
        dt_utc = dt_local.astimezone(pytz.utc)
        return dt_utc
    except Exception:
        # Fallback using explicit manual offset in hours if timezone string is unknown
        from datetime import timedelta
        return dt_naive - timedelta(hours=fallback_offset)

def datetime_to_julian_day_ut(dt_utc: datetime) -> float:
    """
    Converts a UTC datetime to Swiss Ephemeris Julian Day in Universal Time (UT).
    """
    hour_float = dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0 + dt_utc.microsecond / 3600000000.0
    jd = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, hour_float, swe.GREG_CAL)
    return jd

def degree_to_dms(deg: float) -> str:
    """
    Formats a decimal degree into DD° MM' SS" string.
    """
    deg_norm = deg % 360.0
    d = int(deg_norm)
    rem_m = (deg_norm - d) * 60.0
    m = int(rem_m)
    s = int(round((rem_m - m) * 60.0))
    if s >= 60:
        s = 0
        m += 1
    if m >= 60:
        m = 0
        d += 1
    return f"{d}° {m:02d}' {s:02d}\""
