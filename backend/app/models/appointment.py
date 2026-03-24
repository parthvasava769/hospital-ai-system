from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    appointment_date = Column(DateTime, nullable=False)

    status = Column(String(50), default="Pending")
    reason = Column(String(255), nullable=True)
    notes = Column(String(500), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = relationship("User", foreign_keys=[patient_id])
    doctor = relationship("User", foreign_keys=[doctor_id])

    def __repr__(self):
        return (
            f"<Appointment(id={self.id}, "
            f"patient_id={self.patient_id}, "
            f"doctor_id={self.doctor_id}, "
            f"date={self.appointment_date}, "
            f"status={self.status})>"
        )