# routers/patients.py
# actual API endpoints for patient operations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientResponse, PatientLogin
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()

# password hashing and checking
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# router creation 
# for patient related endpoints
router = APIRouter(
    prefix="/patients",   # all endpoints start with /patients
    tags=["Patients"]     # groups them in the docs page
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM  = os.getenv("ALGORITHM")
EXPIRE_MIN = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


def create_token(data: dict):
    """Create a JWT token for a logged-in patient"""
    payload = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=EXPIRE_MIN)
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# ── REGISTER ──
# POST /patients/register
@router.post("/register", response_model=PatientResponse, status_code=201)
def register_patient(patient: PatientCreate, db: Session = Depends(get_db)):

    # Check if national_id already exists
    existing = db.query(Patient).filter(
        Patient.national_id == patient.national_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="A patient with this National ID already exists"
        )

    # Check if phone already exists
    existing_phone = db.query(Patient).filter(
        Patient.phone == patient.phone
    ).first()
    if existing_phone:
        raise HTTPException(
            status_code=400,
            detail="A patient with this phone number already exists"
        )

    # Hash the password
    hashed_password = pwd_context.hash(patient.password)

    # Create the new patient object
    new_patient = Patient(
        national_id   = patient.national_id,
        full_name     = patient.full_name,
        date_of_birth = patient.date_of_birth,
        gender        = patient.gender,
        phone         = patient.phone,
        email         = patient.email,
        blood_type    = patient.blood_type,
        allergies     = patient.allergies,
        password_hash = hashed_password
    )

    # Save to database
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


# ── LOGIN ──
# POST /patients/login
# Patient sends phone + password, gets back a token
@router.post("/login")
def login_patient(credentials: PatientLogin, db: Session = Depends(get_db)):

    # Find patient by phone
    patient = db.query(Patient).filter(
        Patient.phone == credentials.phone
    ).first()

    # Check patient exists and password is correct
    if not patient or not pwd_context.verify(credentials.password, patient.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Incorrect phone number or password"
        )

    # Create a JWT - Jason Web Token
    token = create_token({
        "sub":  str(patient.id),
        "role": "patient",
        "name": patient.full_name
    })

    return {
        "access_token": token,
        "token_type":   "bearer",
        "patient_name": patient.full_name,
        "patient_id":   str(patient.id)
    }


# ── GET PROFILE ──
# GET /patients/{patient_id}
# Fetch a patient's basic profile
@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: str, db: Session = Depends(get_db)):

    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return patient