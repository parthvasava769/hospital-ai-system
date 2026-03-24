from pydantic import BaseModel


class LabTestCreate(BaseModel):

    appointment_id: int
    patient_id: int
    test_name: str
    result: str

class LabTestResponse(BaseModel):

    id: int
    appointment_id: int
    patient_id: int
    test_name: str
    status: str
    result: str | None = None

    class Config:
        from_attributes = True