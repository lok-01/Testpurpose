from typing import List, Optional
from datetime import datetime
import requests
import pytz
from timezonefinder import TimezoneFinder
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.birth_profile import BirthProfile
from app.schemas.birth_profile import BirthProfileCreate, BirthProfileUpdate, BirthProfileResponse
from app.services.location.cities_database import search_offline_cities

router = APIRouter(prefix="/profiles", tags=["Birth Profiles"])

tf = TimezoneFinder()

@router.get("/search-location")
def search_location(query: str = Query(..., min_length=2), date_str: Optional[str] = "2000-01-01"):
    """
    Public geocoding & astronomical timezone resolution.
    Searches built-in high-precision city database with online OpenStreetMap/Photon fallback.
    Automatically resolves exact Latitude, Longitude, City, State, Country,
    and historical IANA Timezone with UTC offset.
    """
    q_clean = query.strip()
    
    # 1. Fast offline astronomical city database (100% offline & instantaneous)
    offline_matches = search_offline_cities(q_clean, limit=8)
    if offline_matches:
        return offline_matches

    headers = {"User-Agent": "AstroRizeVedicLab/1.0 (research; contact: lab@astrorize.local)"}
    
    # 2. Try OpenStreetMap Nominatim
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={requests.utils.quote(q_clean)}&format=json&addressdetails=1&limit=6"
        resp = requests.get(url, headers=headers, timeout=4.0)
        if resp.status_code == 200:
            items = resp.json()
            if items:
                results = []
                for item in items:
                    lat = float(item["lat"])
                    lon = float(item["lon"])
                    addr = item.get("address", {})
                    city = addr.get("city") or addr.get("town") or addr.get("village") or addr.get("municipality") or item.get("display_name", "").split(",")[0]
                    state = addr.get("state") or addr.get("region") or addr.get("county") or ""
                    country = addr.get("country") or ""
                    
                    tz_name = tf.timezone_at(lng=lon, lat=lat) or "UTC"
                    try:
                        tz = pytz.timezone(tz_name)
                        dt_ref = datetime.strptime(date_str, "%Y-%m-%d")
                        offset_h = tz.utcoffset(dt_ref).total_seconds() / 3600.0
                    except Exception:
                        offset_h = 0.0

                    results.append({
                        "display_name": item["display_name"],
                        "city": city,
                        "state": state,
                        "country": country,
                        "latitude": round(lat, 5),
                        "longitude": round(lon, 5),
                        "timezone_str": tz_name,
                        "timezone_offset": round(offset_h, 2),
                    })
                return results
    except Exception:
        pass

    # 2. Fallback to Photon geocoding (OpenStreetMap based, high availability)
    try:
        p_url = f"https://photon.komoot.io/api/?q={requests.utils.quote(q_clean)}&limit=6"
        resp = requests.get(p_url, timeout=4.0)
        if resp.status_code == 200:
            features = resp.json().get("features", [])
            results = []
            for feat in features:
                coords = feat.get("geometry", {}).get("coordinates", [0, 0])
                lon, lat = float(coords[0]), float(coords[1])
                props = feat.get("properties", {})
                city = props.get("city") or props.get("name") or ""
                state = props.get("state") or ""
                country = props.get("country") or ""
                disp = f"{city}, {state}, {country}".strip(", ")
                
                tz_name = tf.timezone_at(lng=lon, lat=lat) or "UTC"
                try:
                    tz = pytz.timezone(tz_name)
                    dt_ref = datetime.strptime(date_str, "%Y-%m-%d")
                    offset_h = tz.utcoffset(dt_ref).total_seconds() / 3600.0
                except Exception:
                    offset_h = 0.0

                results.append({
                    "display_name": disp,
                    "city": city,
                    "state": state,
                    "country": country,
                    "latitude": round(lat, 5),
                    "longitude": round(lon, 5),
                    "timezone_str": tz_name,
                    "timezone_offset": round(offset_h, 2),
                })
            return results
    except Exception:
        pass

    return []

@router.get("/", response_model=List[BirthProfileResponse])
def list_profiles(db: Session = Depends(get_db)):
    return db.query(BirthProfile).order_by(BirthProfile.created_at.desc()).all()

@router.post("/", response_model=BirthProfileResponse)
def create_profile(profile: BirthProfileCreate, db: Session = Depends(get_db)):
    db_profile = BirthProfile(**profile.model_dump())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.get("/{profile_id}", response_model=BirthProfileResponse)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(BirthProfile).filter(BirthProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Birth profile not found")
    return profile

@router.put("/{profile_id}", response_model=BirthProfileResponse)
def update_profile(profile_id: int, updates: BirthProfileUpdate, db: Session = Depends(get_db)):
    profile = db.query(BirthProfile).filter(BirthProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Birth profile not found")
    
    update_data = updates.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)
    
    db.commit()
    db.refresh(profile)
    return profile

@router.delete("/{profile_id}")
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(BirthProfile).filter(BirthProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Birth profile not found")
    db.delete(profile)
    db.commit()
    return {"message": f"Profile {profile_id} successfully deleted"}
