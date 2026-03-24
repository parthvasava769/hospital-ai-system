from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.appointment import Appointment
from app.agents.notification_agent import NotificationAgent
from app.agents.billing_agent import BillingAgent
from app.services.event_bus import EventBus
from app.services.events import Events



class WorkflowOrchestrator:
    """
    Central brain of the hospital workflow automation system.
    Responsible for coordinating agents and managing scheduling logic.
    """

    SLOT_DURATION_MINUTES = 30

    # ------------------------------------
    # Generate time slots
    # ------------------------------------
    @staticmethod
    def generate_time_slots(start_time: datetime, end_time: datetime):

        slots = []
        current = start_time

        while current < end_time:
            slot_end = current + timedelta(minutes=WorkflowOrchestrator.SLOT_DURATION_MINUTES)

            slots.append({
                "start": current,
                "end": slot_end
            })

            current = slot_end

        return slots

    # ------------------------------------
    # Check if slot is free
    # ------------------------------------
    @staticmethod
    def is_slot_available(db: Session, doctor_id: int, slot_start: datetime):

        existing = db.query(Appointment).filter(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_date == slot_start
        ).first()

        return existing is None

    # ------------------------------------
    # Get available slots
    # ------------------------------------
    @staticmethod
    def get_available_slots(db: Session, doctor_id: int, start_time: datetime, end_time: datetime):

        slots = WorkflowOrchestrator.generate_time_slots(start_time, end_time)

        available_slots = []

        for slot in slots:
            if WorkflowOrchestrator.is_slot_available(db, doctor_id, slot["start"]):
                available_slots.append(slot)

        return available_slots

    # ------------------------------------
    # Appointment created workflow
    # ------------------------------------
    @staticmethod
    def appointment_created(appointment):

        print(f"[EVENT] Appointment created: {appointment.id}")

        EventBus.publish(Events.APPOINTMENT_CREATED, appointment)


    @staticmethod
    def appointment_cancelled(appointment):

        print(f"[EVENT] Appointment cancelled: {appointment.id}")

        EventBus.publish(Events.APPOINTMENT_CANCELLED, appointment)


    @staticmethod
    def lab_result_updated(test):

        print(f"[EVENT] Lab result updated: {test.id}")

        EventBus.publish(Events.LAB_RESULT_UPDATED, test)