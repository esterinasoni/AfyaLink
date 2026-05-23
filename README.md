# AfyaLink

> *Afya* - (Swahili for health) *Link* - (connecting every part of the system).

A universal digital health platform built for Kenya, designed to:
- Eliminate long hospital queues through online appointment booking
- Give authorised doctors a complete patient history across all facilities
- Prevent dangerous drug interactions at the point of prescribing
- Work across both public and private hospitals

## The problem
A patient visits Kenyatta National Hospital. Their records are there.
They later visit a private clinic in Westlands. The doctor starts fresh -
no history, no medication list, no allergy flags. This is the norm across Kenya.
AfyaLink fixes this.

## Built by
A pharmacist turned digital health specialist. Clinical knowledge + data science
= a system designed by someone who understands what happens when records are missing.

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

## Security
- AES-256 encryption at rest
- TLS 1.3 in transit
- Role based access control (patient / doctor / admin)
- Full audit logging on every record access
- Kenya Data Protection Act 2019 compliant design
- Patient consent management

## Project status
In active development - follow along commit by commit.

## Phases
- [ ] Phase 1 - Database schema and FastAPI backend
- [ ] Phase 2 - Patient portal (appointment booking)
- [ ] Phase 3 - Doctor dashboard (patient history + drug interaction checker)
- [ ] Phase 4 - Security layer
- [ ] Phase 5 - Deployment and demo

## Running locally
_Setup instructions coming as each phase completes._

## License
MIT