# models/hospital.py
# Hospital database model

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.database import Base


class Hospital(Base):
    __tablename__ = "hospitals"

    id             = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    khis_code      = Column(String(20), unique=True)
    name           = Column(String(200), nullable=False)
    ownership      = Column(String(50), nullable=False)
    facility_level = Column(String(50), nullable=False)
    type           = Column(String(50), nullable=False)
    county         = Column(String(100), nullable=False)
    sub_county     = Column(String(100))
    address        = Column(String(255))
    phone          = Column(String(20))
    email          = Column(String(200))
    is_active      = Column(Boolean, default=True)
    created_at     = Column(DateTime(timezone=True), server_default=func.now())