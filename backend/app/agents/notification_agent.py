from datetime import datetime


class NotificationAgent:
    """
    Responsible for sending notifications to patients and doctors.
    Currently prints messages to console (can later integrate SMS/Email).
    """

    @staticmethod
    def send_appointment_confirmation(appointment):

        print(
            f"[NOTIFICATION] Appointment Confirmed\n"
            f"Patient ID: {appointment.patient_id}\n"
            f"Doctor ID: {appointment.doctor_id}\n"
            f"Date: {appointment.appointment_date}\n"
        )

    @staticmethod
    def send_appointment_cancellation(appointment):

        print(
            f"[NOTIFICATION] Appointment Cancelled\n"
            f"Patient ID: {appointment.patient_id}\n"
            f"Doctor ID: {appointment.doctor_id}\n"
            f"Date: {appointment.appointment_date}\n"
        )

    @staticmethod
    def send_reminder(appointment):

        print(
            f"[REMINDER] Upcoming Appointment\n"
            f"Patient ID: {appointment.patient_id}\n"
            f"Doctor ID: {appointment.doctor_id}\n"
            f"Date: {appointment.appointment_date}\n"
        )