# AfyaLink
**Afya** (Swahili for *health*) + **Link** (connecting every part of the healthcare system).

AfyaLink is a digital health platform being built to improve continuity of care across healthcare facilities in Kenya.

### Vision

**One patient. One health record. Accessible whenever and wherever it is needed.**


## The problem

Healthcare records in Kenya are often fragmented across facilities.

A patient may receive treatment at one hospital, then visit another facility weeks later and be required to repeat their medical history, medication list, allergies, and previous diagnoses. In emergency situations, this lack of accessible information can delay critical care and increase the risk of medical errors.

AfyaLink aims to bridge this gap by enabling secure and controlled access to patient health information across participating healthcare providers.

## Current Features

### Authentication & Access Control
- Patient registration
- Patient login
- Doctor login
- JWT authentication
- Role based access control

### Hospital Management
- Hospital directory
- Hospital search and filtering
- County based hospital lookup
- Hospital profile retrieval

### Patient Management
- Patient registration
- Patient profile management
- Allergy information storage
- Chronic condition information storage

## Planned Features

- Online appointment booking
- Queue management
- Longitudinal patient health records
- Cross facility health record access
- Prescription management
- Drug interaction alerts
- Patient consent management
- Audit logging
- Doctor dashboard

## About the Developer

AfyaLink is being built by a licensed pharmacist with training in data science and a passion for strengthening healthcare systems through technology.

The project combines clinical expertise with modern software engineering to address real world challenges in healthcare continuity and patient safety.

## Architecture

```text
Patient
   ↓
React Frontend
   ↓
FastAPI Backend
   ↓
PostgreSQL Database
```

## Tech stack
| Layer | Technology |
|---|---|
| Backend API | Python · FastAPI |
| Database | PostgreSQL |
| Frontend | React · Tailwind CSS |
| Authentication | JWT · bcrypt |
| Data standard | FHIR-inspired schema |
| Synthetic data | Synthea |
| Deployment | Render (API) · Vercel (frontend) |

## Current API Modules

- Authentication
- Patient Management
- Doctor Management
- Hospital Management
- Role Based Access Control

## Security

### Implemented

- JWT authentication
- bcrypt password hashing
- Role-based access control
- Protected API endpoints
- Environment variable configuration for secrets

### Planned

- Audit logging
- Patient consent management
- AES-256 encryption at rest
- TLS 1.3 encryption in transit
- Security monitoring and alerting
- Compliance with the Kenya Data Protection Act (2019)

## Roadmap

- [x] Database schema design
- [x] Patient registration and login
- [x] Doctor authentication
- [x] Hospital endpoints
- [x] Role-based access control
- [ ] Appointment scheduling
- [ ] Queue management
- [ ] Medical records
- [ ] Prescription management
- [ ] Drug interaction engine
- [ ] Audit logging
- [ ] Deployment


## Project status
In active development - follow along commit by commit.

Current progress:

- ✅ Database schema
- ✅ Patient registration and login
- ✅ Doctor authentication
- ✅ Hospital management
- ⬜ Appointment scheduling
- ⬜ Medical records
- ⬜ Prescriptions
- ⬜ Drug interaction checker



## Running Locally

### Prerequisites
- Python 3.11+
- PostgreSQL
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/afyalink.git
cd afyalink

# Set up the database
createdb afyalink
psql afyalink < backend/database/schema.sql

# Set up the backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Add your environment variables
cp .env.example .env
# Edit .env with your database password and secret key

# Run the API
uvicorn app.main:app --reload
```

API will be running at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`


## Screenshots

Coming soon.

## License

MIT