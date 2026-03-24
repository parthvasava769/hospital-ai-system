from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import dateparser
import re

from app.schemas.ai_assistance import SymptomRequest, AICommand, AIResponse
from app.models.appointment import Appointment
from app.models.user import User
from app.agents.command_agent import CommandAgent
from app.database import get_db
from app.agents.ai_assistance_agent import AIAssistanceAgent
from app.schemas.ai_assistance import AIMessageResponse

router = APIRouter()


# -----------------------------------------
# Symptom Analysis
# -----------------------------------------
@router.post("/analyze", response_model=AIResponse)
def analyze_symptoms(request: SymptomRequest):

    result = AIAssistanceAgent.analyze_symptoms(request.symptoms)

    conditions = ", ".join(result["possible_conditions"])
    tests = ", ".join(result["recommended_tests"])

    message = f"""
🧠 Possible Conditions: {conditions}

🧪 Recommended Tests: {tests}
"""

    return AIResponse(
    possible_conditions=result["possible_conditions"],
    recommended_tests=result["recommended_tests"]
)
# -----------------------------------------
# AI Command Handler
# -----------------------------------------
@router.post("/command", response_model=AIMessageResponse)
def handle_command(
    data: AICommand,
    user_id: int,
    db: Session = Depends(get_db)
):

    command = data.command.lower()
    intent = CommandAgent.parse_command(command)

    # =========================================
    # BOOK APPOINTMENT
    # =========================================
    if intent == "book_appointment":

        # ----------------------------
        # Doctor Detection
        # ----------------------------
        doctors = db.query(User).filter(User.role == "doctor").all()

        doctor_id = None
        doctor_name = None

        for d in doctors:
            if d.name.lower() in command:
                doctor_id = d.id
                doctor_name = d.name
                break

        # fallback doctor
        if not doctor_id and doctors:
            doctor_id = doctors[0].id
            doctor_name = doctors[0].name

        if not doctor_id:
            return AIMessageResponse(message="Doctor not found. Please mention the doctor's name.")

        # ----------------------------
        # Date-Time Extraction
        # ----------------------------
        try:
           # Extract date explicitly
            date_match = re.search(r"on ([a-z0-9\s]+?)(?: at| for|$)", command)

            if date_match:
                date_part = date_match.group(1)
            else:
                date_part = command

            print("EXTRACTED DATE:", date_part)

            # Parse date
            appointment_time = dateparser.parse(
                date_part,
                settings={
                    "PREFER_DATES_FROM": "future",
                    "RELATIVE_BASE": datetime.now()
                }
            )

            if not appointment_time:
                appointment_time = datetime.now() + timedelta(days=1)

            # ----------------------------
            # FORCE TIME EXTRACTION
            # ----------------------------
            time_match = re.search(r"at (\d{1,2})(?::(\d{2}))?\s*(am|pm)?", command)

            if time_match:
                hour = int(time_match.group(1))
                minute = int(time_match.group(2)) if time_match.group(2) else 0
                ampm = time_match.group(3)

                if ampm == "pm" and hour != 12:
                    hour += 12
                if ampm == "am" and hour == 12:
                    hour = 0

                appointment_time = appointment_time.replace(hour=hour, minute=minute)

            # ----------------------------
            # FIX WRONG YEAR BUG
            # ----------------------------
            current_year = datetime.now().year
            if appointment_time.year > current_year + 1:
                appointment_time = appointment_time.replace(year=current_year)

        except:
            appointment_time = datetime.now() + timedelta(days=1)
        # ----------------------------
        # Reason Extraction
        # ----------------------------
        reason = "General consultation"

        # If user explicitly writes "for ..."
        if "for" in command:
            reason = command.split("for", 1)[1].strip()

        else:
            # fallback symptom detection
            symptoms = ["fever", "cough", "headache", "pain", "cold", "vomiting"]
            for symptom in symptoms:
                if symptom in command:
                    reason = symptom
                    break

        # ----------------------------
        # Create Appointment
        # ----------------------------
        appointment = Appointment(
            patient_id=user_id,
            doctor_id=doctor_id,
            appointment_date=appointment_time,
            reason=reason
        )

        db.add(appointment)
        db.commit()
        db.refresh(appointment)

        return AIMessageResponse(
            message=f"Appointment booked with Dr {doctor_name} on {appointment_time.strftime('%d %B %Y at %H:%M')}"
        )

    # =========================================
    # DEFAULT RESPONSE
    # =========================================
    return AIMessageResponse(message="Command not understood. Please try again.")