from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.lab_test import LabTest
from app.schemas.lab_test import LabTestCreate, LabTestResponse
from app.agents.lab_agent import LabAgent
from app.auth.role_checker import RoleChecker

router = APIRouter()
allow_lab = RoleChecker(["lab_staff", "admin"])


@router.post("/", response_model=LabTestResponse)
def create_lab_test(test: LabTestCreate, db: Session = Depends(get_db)):

    new_test = LabTest(
        appointment_id=test.appointment_id,
        patient_id=test.patient_id,
        test_name=test.test_name,
        result=test.result
    )

    db.add(new_test)
    db.commit()
    db.refresh(new_test)

    return new_test


@router.get("/", response_model=list[LabTestResponse])
def get_lab_tests(db: Session = Depends(get_db)):

    return db.query(LabTest).all()


@router.put("/{test_id}/result", dependencies=[Depends(allow_lab)])
def update_result(test_id: int, result: str, db: Session = Depends(get_db)):

    updated = LabAgent.update_result(db, test_id, result)

    if not updated:
        raise HTTPException(status_code=404, detail="Lab test not found")

    return updated