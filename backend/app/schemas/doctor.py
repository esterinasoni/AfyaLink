# schemas/doctor.py
# Validates data coming in and going out of doctor endpoints

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid


# doctor'log in
class DoctorLogin(BaseModel):
    email:    str
    password: str


# successful login details sent
class DoctorLoginResponse(BaseModel):
    access_token:  str
    token_type:    str
    doctor_name:   str
    doctor_id:     str
    role:          str
    hospital_id:   str


# Doctor profile returned from API - password not included
class DoctorResponse(BaseModel):
    id:            uuid.UUID
    hospital_id:   uuid.UUID
    full_name:     str
    specialisation: Optional[str] = None
    licence_number: Optional[str] = None
    phone:         Optional[str] = None
    email:         str
    role:          str
    is_active:     bool
    created_at:    datetime

    class Config:
        from_attributes = True