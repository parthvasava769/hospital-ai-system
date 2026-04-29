from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from datetime import datetime

from app.database import Base


class Billing(Base):
    __tablename__ = "billing"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer)
    appointment_id = Column(Integer)
    amount = Column(Float)
    status = Column(String, default="pending")