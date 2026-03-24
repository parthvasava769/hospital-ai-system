from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import joinedload

from app.database import get_db
from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentCreate, AppointmentResponse
from app.agents.appointment_agent import AppointmentAgent
from app.services.orchestrator import WorkflowOrchestrator
from app.auth.role_checker import RoleChecker       # Admin only
from app.agents.reminder_agent import ReminderAgent

router = APIRouter()
allow_patient = RoleChecker(["patient"])
allow_doctor = RoleChecker(["doctor"])


# -----------------------------------------
# Create Appointment
# -----------------------------------------
@router.post("/", response_model=AppointmentResponse, dependencies=[Depends(allow_patient)])
def create_appointment(
    appointment: AppointmentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    # Check if doctor is available
    if not AppointmentAgent.check_doctor_availability(
        db,
        appointment.doctor_id,
        appointment.appointment_date
    ):
        raise HTTPException(
            status_code=400,
            detail="Doctor already has an appointment at this time"
        )

    new_appointment = Appointment(
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        appointment_date=appointment.appointment_date,
        reason=appointment.reason
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    # Trigger orchestrator workflow safely
    try:
        WorkflowOrchestrator.appointment_created(db, new_appointment)
    except Exception as e:
        print("Orchestrator Error:", e)

    # Trigger reminder safely
    try:
        background_tasks.add_task(
            ReminderAgent.send_reminder,
            new_appointment
        )
    except Exception as e:
        print("Reminder Error:", e)

    return new_appointment


# -----------------------------------------
# Get All Appointments
# -----------------------------------------
@router.get("/", response_model=list[AppointmentResponse])
def get_appointments(db: Session = Depends(get_db)):

    appointments = db.query(Appointment).all()
    return appointments


# -----------------------------------------
# Get Appointment by ID
# -----------------------------------------
@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):

    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return appointment


# -----------------------------------------
# Delete Appointment
# -----------------------------------------
@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):

    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    db.delete(appointment)
    db.commit()

    WorkflowOrchestrator.appointment_cancelled(appointment)

    return {"message": "Appointment deleted successfully"}


# -----------------------------------------
# Get Available Time Slots
# -----------------------------------------
@router.get("/available-slots")
def get_available_slots(
    doctor_id: int,
    start_time: datetime,
    end_time: datetime,
    db: Session = Depends(get_db)
):
    """
    Returns available appointment slots for a doctor
    """

    slots = WorkflowOrchestrator.get_available_slots(
        db,
        doctor_id,
        start_time,
        end_time
    )

    return {"available_slots": slots}


@router.get("/doctor/{doctor_id}", dependencies=[Depends(allow_doctor)])
def get_doctor_appointments(doctor_id: int, db: Session = Depends(get_db)):

    appointments = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id
    ).all()

    return appointments


class StatusUpdate(BaseModel):
    status: str


@router.put("/{appointment_id}/status")
def update_status(
    appointment_id: int,
    data: StatusUpdate,
    db: Session = Depends(get_db)
):

    print("STATUS UPDATE CALLED")

    appt = db.query(Appointment)\
        .options(joinedload(Appointment.patient))\
        .filter(Appointment.id == appointment_id)\
        .first()

    if not appt:
        return {"message": "Appointment not found"}

    appt.status = data.status
    db.commit()
    db.refresh(appt)
    print("Sending email now...")
    # 🔔 Send email
    try:
        ReminderAgent.send_reminder(appt)
    except Exception as e:
        print("Email Error:", e)

    return {"message": f"Appointment {data.status}"}

@router.get("/patient/{patient_id}")
def get_patient_appointments(patient_id: int, db: Session = Depends(get_db)):
    return db.query(Appointment).filter(
        Appointment.patient_id == patient_id
    ).all()