# models/doctor.py
# Python representation of the doctors table

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id             = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hospital_id    = Column(UUID(as_uuid=True), ForeignKey("hospitals.id"), nullable=False)
    full_name      = Column(String(200), nullable=False)
    specialisation = Column(String(200))
    licence_number = Column(String(100), unique=True)
    phone          = Column(String(20))
    email          = Column(String(200), unique=True, nullable=False)
    password_hash  = Column(String(255), nullable=False)
    role           = Column(String(50), nullable=False)
    is_active      = Column(Boolean, default=True)
    created_at     = Column(DateTime(timezone=True), server_default=func.now())