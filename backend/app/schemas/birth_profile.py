from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class BirthProfileBase(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Srinivasa Ramanujan"})
    gender: Optional[str] = Field("Male", json_schema_extra={"example": "Male"})
    date_of_birth: str = Field(..., json_schema_extra={"example": "1887-12-22"})
    time_of_birth: str = Field(..., json_schema_extra={"example": "17:20:00"})
    birthplace: str = Field(..., json_schema_extra={"example": "Erode, Tamil Nadu, India"})
    country: Optional[str] = "India"
    state: Optional[str] = "Tamil Nadu"
    city: Optional[str] = "Erode"
    latitude: float = Field(..., json_schema_extra={"example": 11.3410})
    longitude: float = Field(..., json_schema_extra={"example": 77.7172})
    timezone_str: str = Field("Asia/Kolkata", json_schema_extra={"example": "Asia/Kolkata"})
    timezone_offset: float = Field(5.5, json_schema_extra={"example": 5.5})
    accuracy_notes: Optional[str] = None

class BirthProfileCreate(BirthProfileBase):
    pass

class BirthProfileUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None
    time_of_birth: Optional[str] = None
    birthplace: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone_str: Optional[str] = None
    timezone_offset: Optional[float] = None
    accuracy_notes: Optional[str] = None

class BirthProfileResponse(BirthProfileBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
