# main.py
# Starting point of the AfyaLink backend

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import patient, doctor

# Create the FastAPI application
app = FastAPI(
    title="AfyaLink API",
    description="Universal digital health platform for Kenya — connecting patients, doctors, and hospitals.",
    version="1.0.0"  
)
# CORS middleware — allows the frontend to communicate with backend
# Useful later when React frontend starts making API requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers — connect patient routers/endpoints to the main app
app.include_router(patient.router)
app.include_router(doctor.router)
# Root endpoint — simple test route to confirm API is working
@app.get("/")
def root():
    return {
        "message": "AfyaLink API is running",
        "version": "1.0.0",
        "docs":    "Visit /docs for interactive API documentation"
    }