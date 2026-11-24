from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class VerificationCaseCreate(BaseModel):
    test_name: str
    reference_source: str
    profile_details: Dict[str, Any]
    expected_values: Dict[str, Any]
    tolerance: float = 0.01
    notes: Optional[str] = None

class VerificationCaseResponse(BaseModel):
    id: int
    test_name: str
    reference_source: str
    profile_details: Dict[str, Any]
    expected_values: Dict[str, Any]
    actual_values: Optional[Dict[str, Any]] = None
    differences: Optional[Dict[str, Any]] = None
    tolerance: float
    status: str
    notes: Optional[str] = None
    executed_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class VerificationRunResult(BaseModel):
    case_id: int
    test_name: str
    status: str
    max_difference: float
    tolerance: float
    details: Dict[str, Any]
