# schemas/patient.py
# Checks patient data before saving to database

from pydantic import BaseModel, EmailStr, field_validator
from datetime import date, datetime
from uuid import UUID
from typing import Optional
import re


# Data required to register a new patient
class PatientCreate(BaseModel):
    national_id:   str
    full_name:     str
    date_of_birth: date
    gender:        Optional[str] = None
    phone:         str
    email:         Optional[EmailStr] = None
    blood_type:    Optional[str] = None
    allergies:     Optional[str] = None
    password:      str

    # Validate national_id, should be 7-10 digits
    @field_validator('national_id')
    def validate_national_id(cls, v):
        if not re.match(r'^\d{7,10}$', v):
            raise ValueError('National ID must be 7 to 10 digits')
        return v
    
    # Gender backend normalization
    @field_validator('gender')
    def validate_gender(cls, v):
        if v is None:
            return v
        v = v.lower()
        if v not in {"male", "female", "other"}:
            raise ValueError("Gender must be male, female, or other")
        return v

    # Validate password strength
    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


# Data returned after patient registration — never send password back
class PatientResponse(BaseModel):
    id:            UUID
    national_id:   str
    full_name:     str
    date_of_birth: date
    gender:        Optional[str]
    phone:         str
    email:         Optional[str]
    blood_type:    Optional[str]
    allergies:     Optional[str]
    created_at:    datetime

    class Config:
        from_attributes = True


# Data required to LOGIN
class PatientLogin(BaseModel):
    phone:    str
    password: str