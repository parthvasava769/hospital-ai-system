from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.doctor_schedule import DoctorSchedule
from app.schemas.doctor_schedule import (
    DoctorScheduleCreate,
    DoctorScheduleResponse
)

router = APIRouter()


@router.post("/", response_model=DoctorScheduleResponse)
def create_schedule(schedule: DoctorScheduleCreate, db: Session = Depends(get_db)):

    new_schedule = DoctorSchedule(
        doctor_id=schedule.doctor_id,
        day_of_week=schedule.day_of_week,
        start_time=schedule.start_time,
        end_time=schedule.end_time,
        slot_duration=schedule.slot_duration
    )

    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)

    return new_schedule


@router.get("/", response_model=list[DoctorScheduleResponse])
def get_schedules(db: Session = Depends(get_db)):

    return db.query(DoctorSchedule).all()