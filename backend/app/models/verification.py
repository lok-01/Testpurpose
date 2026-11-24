from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, JSON
from app.database import Base

class VerificationCase(Base):
    __tablename__ = "verification_cases"

    id = Column(Integer, primary_key=True, index=True)
    test_name = Column(String(100), nullable=False)
    reference_source = Column(String(150), nullable=False)
    profile_details = Column(JSON, nullable=False)
    expected_values = Column(JSON, nullable=False)
    actual_values = Column(JSON, nullable=True)
    differences = Column(JSON, nullable=True)
    tolerance = Column(Float, default=0.01)
    status = Column(String(20), default="PENDING")  # PASSED, FAILED, PENDING
    notes = Column(Text, nullable=True)
    executed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
