from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.models import user, appointment
from app.routes.appointments import router as appointments_router
from app.models import doctor_schedule
from app.routes.doctor_schedule import router as schedule_router
from app.models import billing
from app.routes.billing import router as billing_router
from app.models import lab_test
from app.routes.lab_tests import router as lab_router
from app.routes.ai_assistance import router as ai_router
from app.services.agent_registry import register_agents
from app.routes import auth
from app.routes.users import router as users_router

app = FastAPI(
    title="Multi-Agent Hospital Workflow Automation System",
    description="Backend API for automating hospital operational workflows using AI agents",
    version="1.0.0"
)
register_agents()

# Enable CORS (important for frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Health Check Endpoint
# -------------------------
@app.get("/health")
def health_check():
    return {
        "status": "OK",
        "message": "Hospital Workflow Automation API is running"
    }

# -------------------------
# Include Routers
# -------------------------
app.include_router(appointments_router, prefix="/appointments", tags=["Appointments"])
app.include_router(schedule_router, prefix="/doctor-schedules", tags=["Doctor Schedules"])
app.include_router(lab_router, prefix="/lab-tests", tags=["Lab Tests"])
app.include_router(ai_router, prefix="/ai-assistance", tags=["AI Assistance"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(billing_router, prefix="/billing", tags=["Billing"])
app.include_router(users_router, prefix="/users", tags=["Users"])

# -------------------------
# Create Database Tables
# -------------------------
user.Base.metadata.create_all(bind=engine)
appointment.Base.metadata.create_all(bind=engine)
doctor_schedule.Base.metadata.create_all(bind=engine)
billing.Base.metadata.create_all(bind=engine)
lab_test.Base.metadata.create_all(bind=engine)