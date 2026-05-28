# patient table model
# Helps FastAPI communicate with the patients table

from sqlalchemy import Column, String, Date, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.database import Base


class Patient(Base):
    #connect this model to the patients table in PostgreSQL
    __tablename__ = "patients"

    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    national_id   = Column(String(10), unique=True, nullable=False)
    full_name     = Column(String(200), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender        = Column(String(20))
    phone         = Column(String(20), unique=True, nullable=False)
    email         = Column(String(200), unique=True)
    blood_type    = Column(String(5))
    allergies     = Column(Text)
    password_hash = Column(String(255), nullable=False)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())
    updated_at    = Column(DateTime(timezone=True), onupdate=func.now())