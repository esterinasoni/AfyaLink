# database.py
# connect FastAPI to PostgreSQL

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Get the database connection URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Create PostgreSQL connection
engine = create_engine(DATABASE_URL)

# create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all database models
Base = declarative_base()


# open database session for API requests
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()