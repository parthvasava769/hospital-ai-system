from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.appointment import Appointment

router = APIRouter()

# -----------------------
# GET ALL USERS
# -----------------------
@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


# -----------------------
# DELETE USER
# -----------------------
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted"}


# -----------------------
# GET ALL APPOINTMENTS
# -----------------------
@router.get("/appointments")
def get_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()