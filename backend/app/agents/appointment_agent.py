from sqlalchemy.orm import Session
from app.models.appointment import Appointment


class AppointmentAgent:

    @staticmethod
    def check_doctor_availability(db: Session, doctor_id: int, appointment_date):

        existing = db.query(Appointment).filter(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_date == appointment_date
        ).first()

        if existing:
            return False

        return True