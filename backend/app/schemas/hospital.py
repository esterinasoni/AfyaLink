# schemas/hospital.py
# Hospital API schemas.

# Defines request and response models used to validate hospital data entering and leaving the API.

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class HospitalResponse(BaseModel):
    id:             uuid.UUID
    khis_code:      Optional[str] = None
    name:           str
    ownership:      str
    facility_level: str
    type:           str
    county:         str
    sub_county:     Optional[str] = None
    address:        Optional[str] = None
    phone:          Optional[str] = None
    email:          Optional[str] = None
    is_active:      bool

    class Config:
        from_attributes = True


# Lightweight hospital representation used for:
# - search results
# - dropdown selections
# - hospital listings
#
# Excludes less frequently needed fields to reduce payload size.
class HospitalSummary(BaseModel):
    id:             uuid.UUID
    name:           str
    ownership:      str
    facility_level: str
    type:           str
    county:         str
    sub_county:     Optional[str] = None
    phone:          Optional[str] = None

    class Config:
        from_attributes = True