from sqlalchemy.orm import Session
from app.models.lab_test import LabTest


class LabAgent:
    """
    Handles lab test workflow
    """

    @staticmethod
    def create_lab_test(db: Session, appointment, test_name):

        new_test = LabTest(
            appointment_id=appointment.id,
            patient_id=appointment.patient_id,
            test_name=test_name,
            status="Pending"
        )

        db.add(new_test)
        db.commit()
        db.refresh(new_test)

        print(f"[LAB] Lab test '{test_name}' created for appointment {appointment.id}")

        return new_test

    @staticmethod
    def update_result(db: Session, test_id: int, result: str):

        test = db.query(LabTest).filter(LabTest.id == test_id).first()

        if not test:
            return None

        test.result = result
        test.status = "Completed"

        db.commit()
        db.refresh(test)

        print(f"[LAB] Result updated for test {test_id}")

        return test