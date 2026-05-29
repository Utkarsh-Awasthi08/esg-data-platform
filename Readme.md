# ESG Data Platform

A full-stack ESG (Environmental, Social, and Governance) analytics platform that ingests raw enterprise operational data, normalizes it into ESG-compliant structures, validates suspicious records, calculates emissions, and visualizes insights through an interactive analytics dashboard.

---

# Live Demo

## Frontend
https://esg-data-platform-frontend.vercel.app

## Backend API
https://esg-data-platform-km4q.onrender.com

---

# Project Overview

This project simulates a real-world ESG data ingestion and analytics pipeline used by enterprises to monitor sustainability metrics across multiple operational domains.

The platform supports ingestion and normalization of:

- Fuel procurement data
- Electricity utility data
- Procurement / supply chain data
- Travel booking data via external API

The system transforms raw operational records into ESG-ready normalized entities while maintaining:

- Source-of-truth traceability
- Auditability
- Validation issue tracking
- Unit normalization
- Scope 1 / Scope 2 / Scope 3 categorization
- Emission calculations

---

# Features

## Data Ingestion

Supports ingestion from:

- CSV uploads
- External REST APIs

### Supported Sources

| Source | Type |
|---|---|
| Fuel Procurement | CSV |
| Electricity Utility | CSV |
| Procurement Data | CSV |
| Travel Bookings | External API |

---

# ESG Normalization

Raw operational data is converted into ESG-normalized records.

Examples:

- Fuel quantities normalized into standard units
- Electricity usage standardized to kWh
- Procurement spend categorized into Scope 3
- Travel emissions classified under Scope 3

---

# Validation Engine

The platform automatically validates incoming records and detects:

- Missing values
- Suspicious quantities
- Abnormal consumption patterns
- Invalid units
- Data inconsistencies

Validation issues are categorized into:

- WARNING
- SUSPICIOUS
- FAILED

---

# Emission Calculations

The platform calculates emissions using simplified emission factors.

Examples:

- Diesel fuel emissions
- Electricity emissions
- Procurement-related emissions
- Travel emissions

---

# ESG Analytics Dashboard

Interactive frontend dashboard built using React and Recharts.

Features include:

- Emission summary cards
- Scope-wise emissions chart
- Monthly emissions trend analysis
- Validation issue visualization
- Validation insights table

---

# Tech Stack

## Frontend

- React.js
- Bootstrap 5
- Axios
- Recharts
- Vite

## Backend

- Django
- Django REST Framework
- PostgreSQL
- Pandas

## Deployment

| Service | Platform |
|---|---|
| Frontend | Vercel |
| Backend | Render |
| Database | Neon PostgreSQL |

---

# Project Structure

bash Intern_Assignment/ │ ├── esg_backend/ │   ├── backend/ │   ├── ingestion/ │   ├── manage.py │   └── requirements.txt │ ├── esg-frontend/ │   ├── src/ │   ├── public/ │   └── package.json │ ├── MODEL.md ├── DECISIONS.md ├── TRADEOFFS.md ├── SOURCES.md └── README.md 

---

# API Endpoints

## Upload APIs

| Endpoint | Description |
|---|---|
| /api/upload/fuel/ | Upload fuel procurement CSV |
| /api/upload/electricity/ | Upload electricity CSV |
| /api/upload/procurement/ | Upload procurement CSV |

---

## Analytics APIs

| Endpoint | Description |
|---|---|
| /api/dashboard/ | ESG dashboard summary |
| /api/analytics/monthly-emissions/ | Monthly emissions trend |
| /api/analytics/validation-insights/ | Validation issue insights |

---

## Travel API Integration

| Endpoint | Description |
|---|---|
| /api/import/travel/ | Import travel booking data |

---

# Database Design Highlights

The data model was designed to support:

- Multi-tenancy
- Audit trails
- ESG normalization
- Generic validation engine
- Source-of-truth tracking
- Scope categorization
- Extensible ingestion pipelines

Separate models exist for:

- Raw source records
- ESG normalized records
- Validation issues
- Uploaded files

This architecture preserves raw source integrity while enabling ESG analytics independently.

---

# Deployment Architecture

text Frontend (Vercel)         |         v Backend API (Render)         |         v Neon PostgreSQL Database 

---

# Environment Variables

## Backend

Create .env inside esg_backend/

env SECRET_KEY=your_secret_key DEBUG=False  DATABASE_URL=your_neon_database_url ALLOWED_HOSTS=your-render-domain.onrender.com 

---

## Frontend

Create .env inside esg-frontend/

env VITE_API_BASE_URL=https://your-backend-url.onrender.com/api 

---

# Running Locally

## Backend

bash cd esg_backend  python -m venv venv  source venv/bin/activate  pip install -r requirements.txt  python manage.py migrate  python manage.py runserver 

---

## Frontend

bash cd esg-frontend  npm install  npm run dev 

---

# Key Engineering Decisions

- Raw source records stored separately from ESG normalized records
- Validation implemented as a reusable generic system
- Scope categorization embedded into normalized ESG models
- CSV ingestion pipelines designed independently per source
- Dashboard APIs separated from ingestion APIs for scalability

---

# Future Improvements

Potential future enhancements:

- Authentication & RBAC
- Multi-tenant isolation
- Real emission factor databases
- AI-powered anomaly detection
- Scheduled ingestion jobs
- File versioning
- Advanced ESG reporting exports
- Kafka/event-driven ingestion pipeline

---

# Author

Utkarsh Awasthi

- Full Stack Developer
- Java & Spring Backend Developer
- React Frontend Developer
- ESG Data Platform Project
