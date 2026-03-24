from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.billing import Billing
from app.schemas.billing import BillingResponse

router = APIRouter()


@router.get("/", response_model=list[BillingResponse])
def get_all_bills(db: Session = Depends(get_db)):

    bills = db.query(Billing).all()
    return bills


@router.get("/{bill_id}", response_model=BillingResponse)
def get_bill(bill_id: int, db: Session = Depends(get_db)):

    bill = db.query(Billing).filter(Billing.id == bill_id).first()

    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    return bill


@router.put("/{bill_id}/pay")
def pay_bill(bill_id: int, db: Session = Depends(get_db)):

    bill = db.query(Billing).filter(Billing.id == bill_id).first()

    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    bill.status = "Paid"

    db.commit()

    return {"message": "Bill paid successfully"}