from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.verification import VerificationCase
from app.schemas.verification import (
    VerificationCaseCreate,
    VerificationCaseResponse,
    VerificationRunResult,
)
from app.services.verification import verification_service

router = APIRouter(prefix="/verification", tags=["Calculation Verification & QA"])

@router.get("/cases", response_model=List[VerificationCaseResponse])
def list_verification_cases(db: Session = Depends(get_db)):
    return db.query(VerificationCase).order_by(VerificationCase.id.asc()).all()

@router.post("/cases", response_model=VerificationCaseResponse)
def create_verification_case(case_in: VerificationCaseCreate, db: Session = Depends(get_db)):
    vc = VerificationCase(**case_in.model_dump())
    db.add(vc)
    db.commit()
    db.refresh(vc)
    return vc

@router.post("/run/{case_id}", response_model=VerificationRunResult)
def run_case(case_id: int, db: Session = Depends(get_db)):
    case = db.query(VerificationCase).filter(VerificationCase.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Verification case not found")
    return verification_service.run_case_verification(case, db=db)

@router.post("/run-all")
def run_all_cases(db: Session = Depends(get_db)):
    cases = db.query(VerificationCase).all()
    results = []
    for c in cases:
        res = verification_service.run_case_verification(c, db=db)
        results.append(res)
    return {
        "total_cases_executed": len(cases),
        "passed": sum(1 for r in results if r["status"] == "PASSED"),
        "failed": sum(1 for r in results if r["status"] == "FAILED"),
        "details": results,
    }

@router.post("/seed-benchmarks")
def seed_benchmarks(db: Session = Depends(get_db)):
    verification_service.seed_default_benchmarks(db)
    return {"message": "Verification benchmark cases successfully seeded."}

@router.get("/stats")
def get_verification_stats(db: Session = Depends(get_db)):
    total = db.query(VerificationCase).count()
    passed = db.query(VerificationCase).filter(VerificationCase.status == "PASSED").count()
    failed = db.query(VerificationCase).filter(VerificationCase.status == "FAILED").count()
    pending = db.query(VerificationCase).filter(VerificationCase.status == "PENDING").count()
    return {
        "total_test_cases": total,
        "passed": passed,
        "failed": failed,
        "pending": pending,
        "pass_rate_pct": round((passed / total * 100.0) if total > 0 else 0.0, 1),
    }
