# auth.py
# AfyaLink Authentication Utilities
# -------------------------------------------------------------
# Central authentication and authorization module
# All protected endpoints import functions from this file

# Responsibilities
# - Validates JWT access tokens
# - Identify the currently logged in user
# - Enforce role based access control
# - Protect sensitive healthcare data

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.database import get_db
from app.models.doctor import Doctor
from dotenv import load_dotenv
import os


# Load security settings fron environment variables.
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY") # used to sign and verify JWT tokens.
ALGORITHM  = os.getenv("ALGORITHM")  # defines the encryption algorithm used.

# Configure OAuth2 authentication.
# FastAPI will automatically look for a JWT token in the Authorization header:
# -----------------------------------------------------------------------------
# Authorization: Bearer <access_token>
#
#Token is issued after a successful login.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/doctors/login")


# ------------------------------------------------------------
# Retrieve the currently authenticated doctor.
#
# Process:
# 1. Extract JWT token from request header
# 2. Verify token signature and validity
# 3. Extract doctor information from token payload
# 4. Retrieve doctor record from database
# 5. Return authenticated doctor object
#
# Raises:
# - 401 Unauthorized if token is missing, invalid,
#   expired, or belongs to a non existent user.
# ------------------------------------------------------------
def get_current_doctor(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Doctor:
    """
    Decode the JWT token and return the logged in doctor.
    Called automatically on any protected endpoint.
    If token is missing or invalid, returns 401.
    """
    credentials_error = HTTPException(           # Standard authentication failure response. Returned whenever a token cannot be trusted.
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token. Please log in again.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the token
        # --------------------------------------------------------------
        # Verify JWT signature and extract user identity
        # information stored within the token payload.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        doctor_id: str = payload.get("sub")
        role: str = payload.get("role")

        if doctor_id is None:
            raise credentials_error

    except JWTError:
        raise credentials_error

    # Fetch the doctor from database
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if doctor is None or not doctor.is_active:
        raise credentials_error

    return doctor


def require_role(*allowed_roles: str):
    """
    Role guard — use this to restrict endpoints to specific roles.

    Example usage:
        @router.get("/records")
        def get_records(doctor = Depends(require_role("doctor", "admin"))):

    A pharmacist trying to access a doctor-only endpoint gets 403.
    """
    def role_checker(current_doctor: Doctor = Depends(get_current_doctor)):
        if current_doctor.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {', '.join(allowed_roles)}"
            )
        return current_doctor
    return role_checker