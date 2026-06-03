# routers/doctors.py
# Doctor authentication and profile endpoints
# ============================================================
# Responsibilities:
# - Authenticate doctors using email and password
# - Generate secure JWT access tokens after login
# - Retrieve the currently logged-in doctor's profile
# - Restrict access to sensitive endpoints based on user roles
# - Provide doctor information for authorized users
# ============================================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorLogin, DoctorLoginResponse, DoctorResponse
from app.auth import get_current_doctor, require_role
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv
import os

# Load secret configuration values from the .env file.
# These values should never be hardcoded into source code.
load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)
# Secret key used to sign and verify JWT tokens.
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM  = os.getenv("ALGORITHM") # Encryption algorithm used for token generation.
EXPIRE_MIN = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # Number of minutes before an access token expires.


def create_doctor_token(data: dict):
    """Create a JWT token for a logged-in doctor"""
    payload = data.copy()
    expire  = datetime.utcnow() + timedelta(minutes=EXPIRE_MIN)
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# ── LOGIN ─────────────────────────────────────────────────
# POST /doctors/login
# Doctor sends email + password, gets back a token with their role
@router.post("/login", response_model=DoctorLoginResponse)
def login_doctor(credentials: DoctorLogin, db: Session = Depends(get_db)):

    # Find doctor by email
    doctor = db.query(Doctor).filter(
        Doctor.email == credentials.email
    ).first()

    # Verify doctor exists, is active, and password is correct
    if not doctor or not doctor.is_active:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not pwd_context.verify(credentials.password, doctor.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Create token — role is embedded inside it
    # This is what role-based access reads later
    token = create_doctor_token({
        "sub":         str(doctor.id),
        "role":        doctor.role,
        "name":        doctor.full_name,
        "hospital_id": str(doctor.hospital_id)
    })

    return {
        "access_token": token,
        "token_type":   "bearer",
        "doctor_name":  doctor.full_name,
        "doctor_id":    str(doctor.id),
        "role":         doctor.role,
        "hospital_id":  str(doctor.hospital_id)
    }


# ── GET MY PROFILE ────────────────────────────────────────
# GET /doctors/me
# Returns the logged-in doctor's profile
# Requires a valid token — no token, no access
@router.get("/me", response_model=DoctorResponse)
def get_my_profile(current_doctor: Doctor = Depends(get_current_doctor)):
    return current_doctor


# ── GET ANY DOCTOR (admin only) ───────────────────────────
# GET /doctors/{doctor_id}
# Only admins can look up other doctors
@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(
    doctor_id: str,
    db: Session = Depends(get_db),
    current_doctor: Doctor = Depends(require_role("admin"))
):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return doctor