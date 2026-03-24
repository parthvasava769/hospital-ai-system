from sqlalchemy import Column, Integer, Time, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class DoctorSchedule(Base):
    __tablename__ = "doctor_schedules"

    id = Column(Integer, primary_key=True, index=True)

    doctor_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # 0 = Monday, 6 = Sunday
    day_of_week = Column(Integer, nullable=False)

    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    slot_duration = Column(Integer, default=30)

    doctor = relationship("User")

    def __repr__(self):
        return (
            f"<DoctorSchedule doctor_id={self.doctor_id}, "
            f"day={self.day_of_week}, "
            f"start={self.start_time}, "
            f"end={self.end_time}>"
        )