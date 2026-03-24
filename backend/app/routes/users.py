from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User

router = APIRouter()

@router.get("/")
def get_users(role: str = None, db: Session = Depends(get_db)):

    query = db.query(User)

    if role:
        query = query.filter(User.role == role)

    return query.all()