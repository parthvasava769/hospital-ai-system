from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User

router = APIRouter()

# -------------------------
# Temporary role simulation
# -------------------------

CURRENT_TEST_ROLE = "patient"


# -------------------------
# Register User
# -------------------------
@router.post("/register")
def register_user(
    name: str,
    email: str,
    password: str,
    role: str,
    phone: str,
    db: Session = Depends(get_db)
):

    # Check duplicate email
    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        name=name,
        email=email,
        password=password,
        role=role,
        phone=phone
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


# -------------------------
# Login User (Simple)
# -------------------------
@router.post("/login")
def login(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.email == email).first()

    if not user or user.password != password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "message": "Login successful",
        "user_id": user.id,
        "role": user.role
    }


# -------------------------
# Switch Role (Testing)
# -------------------------
@router.post("/switch-role")
def switch_role(role: str):

    global CURRENT_TEST_ROLE

    CURRENT_TEST_ROLE = role

    return {"message": f"Current role switched to {role}"}