from pydantic import BaseModel


class BillingCreate(BaseModel):

    patient_id: int
    appointment_id: int
    amount: float


class BillingResponse(BaseModel):

    id: int
    patient_id: int
    appointment_id: int
    amount: float
    status: str

    class Config:
        from_attributes = True