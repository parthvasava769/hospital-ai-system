from pydantic import BaseModel
from datetime import time


class DoctorScheduleCreate(BaseModel):
    doctor_id: int
    day_of_week: int
    start_time: time
    end_time: time
    slot_duration: int = 30


class DoctorScheduleResponse(BaseModel):
    id: int
    doctor_id: int
    day_of_week: int
    start_time: time
    end_time: time
    slot_duration: int

    class Config:
        from_attributes = True