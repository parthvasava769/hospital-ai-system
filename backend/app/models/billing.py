from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from datetime import datetime

from app.database import Base


class Billing(Base):
    __tablename__ = "billings"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(Integer, ForeignKey("users.id"))
    appointment_id = Column(Integer, ForeignKey("appointments.id"))

    amount = Column(Float, nullable=False)
    status = Column(String(50), default="Pending")

    created_at = Column(DateTime, default=datetime.utcnow)