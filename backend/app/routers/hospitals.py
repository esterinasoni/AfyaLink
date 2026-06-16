# routers/hospitals.py

# Hospital endpoints.

# Provides public hospital discovery functionality, including hospital search, filtering, listings, and hospital profile retrieval.

# Authentication is not required because patients must be able to browse facilities before booking appointments.

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.database import get_db
from app.models.hospital import Hospital
from app.schemas.hospital import HospitalResponse, HospitalSummary

#All hospital related endpoints 
router = APIRouter(
    prefix="/hospitals",
    tags=["Hospitals"]
)


# Hospital search endpoint.

# Supports filtering by:
# - county
# - ownership
# - facility level
# - facility type

# Only active facilities are returned.

# Example:
# GET /hospitals?county=Nairobi&ownership=public

@router.get("/", response_model=List[HospitalSummary])
def list_hospitals(
    county:         Optional[str] = Query(None, description="Filter by county e.g. Nairobi"),
    ownership:      Optional[str] = Query(None, description="public, private, faith_based, ngo"),
    facility_level: Optional[str] = Query(None, description="level_2 through level_6"),
    type:           Optional[str] = Query(None, description="clinic, county_hospital etc"),
    db:             Session = Depends(get_db)
):
    # Patients should only see facilities that are active
    query = db.query(Hospital).filter(Hospital.is_active == True)

    # Apply filters only if provided
    # This way the same endpoint handles both
    # If no filters are supplied, all active hospitals are returned.
    if county:
        query = query.filter(
            func.lower(Hospital.county) == func.lower(county)
        )
    if ownership:
        query = query.filter(Hospital.ownership == ownership)
    if facility_level:
        query = query.filter(Hospital.facility_level == facility_level)
    if type:
        query = query.filter(Hospital.type == type)

    hospitals = query.order_by(Hospital.name).all()

    if not hospitals:
        raise HTTPException(
            status_code=404,
            detail="No hospitals found matching your search"
        )

    return hospitals


# ── GET SINGLE HOSPITAL ───────────────────────────────────
# Retrieve the complete profile of a single hospital.
# Typically called after a user selects a facility from search results.
@router.get("/{hospital_id}", response_model=HospitalResponse)
def get_hospital(hospital_id: str, db: Session = Depends(get_db)):

    hospital = db.query(Hospital).filter(
        Hospital.id == hospital_id,
        Hospital.is_active == True
    ).first()

    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")

    return hospital


# ── LIST COUNTIES ─────────────────────────────────────────
# GET /hospitals/counties/list
# Returns a unique list of counties containing active facilities.
# Used to populate county filter dropdowns in the frontend.
@router.get("/counties/list", response_model=List[str])
def list_counties(db: Session = Depends(get_db)):
    counties = db.query(Hospital.county)\
        .filter(Hospital.is_active == True)\
        .distinct()\
        .order_by(Hospital.county)\
        .all()

    # SQLAlchemy returns list of tuples - extract just the string
    return [c[0] for c in counties]