from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class LabTest(Base):
    __tablename__ = "lab_tests"

    id = Column(Integer, primary_key=True, index=True)

    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    patient_id = Column(Integer, ForeignKey("users.id"))

    test_name = Column(String(100), nullable=False)
    status = Column(String(50), default="Pending")

    result = Column(String(500), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    appointment = relationship("Appointment")
    patient = relationship("User")

    def __repr__(self):
        return f"<LabTest appointment_id={self.appointment_id} test={self.test_name}>"