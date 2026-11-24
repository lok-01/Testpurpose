from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from app.database import Base

class BirthProfile(Base):
    __tablename__ = "birth_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    gender = Column(String(20), nullable=True)
    date_of_birth = Column(String(10), nullable=False)  # YYYY-MM-DD
    time_of_birth = Column(String(8), nullable=False)   # HH:MM:SS
    birthplace = Column(String(200), nullable=False)
    country = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timezone_str = Column(String(50), nullable=False, default="UTC")
    timezone_offset = Column(Float, nullable=False, default=0.0)
    accuracy_notes = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CalculationRecord(Base):
    __tablename__ = "calculation_records"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, nullable=True, index=True)
    calculation_type = Column(String(50), nullable=False)
    engine_version = Column(String(50), nullable=False)
    ayanamsa_used = Column(String(50), nullable=False)
    input_params = Column(JSON, nullable=True)
    result_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
