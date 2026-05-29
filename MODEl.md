# ESG Data Model Design

## Overview

The ESG Analytics Platform is designed to ingest, normalize, validate, and analyze sustainability data coming from multiple enterprise systems such as SAP, Oracle, utility providers, and external APIs.

The data model was designed with the following goals:

- Multi-tenancy support
- Scope 1 / 2 / 3 categorization
- Source-of-truth tracking
- Unit normalization
- Auditability and traceability
- Extensibility for future ESG domains
- Separation between raw ingestion data and normalized ESG records

The architecture follows a layered ingestion approach:

1. Raw Source Data
2. Normalized ESG Records
3. Validation Layer
4. Emission Calculation Layer
5. Analytics Layer

Currently the model includes emissions from Fuel only. However the records for other procurements and electricty can be uploaded and saved in db but emission calculation logic is only remaining. Thoroughly researched NAVAN API response for bookings. The inclusion of its API is left as I require credentials of a company for that.
---

# Core Design Philosophy

Instead of directly modifying uploaded source data, the platform stores:

- Raw immutable records
- Separate normalized ESG records
- Validation issues independently
- Calculated emissions separately

This preserves the original source-of-truth while enabling ESG standardization and analytics.

---

# Multi-Tenancy Design

The system is designed to support multiple organizations (tenants).

A future Tenant model can be added:

python class Tenant(models.Model):     id = models.UUIDField(primary_key=True)     name = models.CharField(max_length=255) 

Every major entity can then reference the tenant:

python tenant = models.ForeignKey(     Tenant,     on_delete=models.CASCADE ) 

This ensures:

- Data isolation between organizations
- Tenant-level analytics
- Secure segregation of ESG data
- Scalability for SaaS deployment

---

# Source-of-Truth Tracking

The platform preserves complete traceability of incoming data.

## UploadedFile Model

The UploadedFile model tracks:

- Original filename
- Source system
- File type
- Upload timestamp

Example sources:

- SAP
- Oracle
- Utility Provider
- Travel API
- Manual Upload

This allows every ESG record to be traced back to its original source.

---

# Raw Record Layer

Separate raw models were created for each ingestion domain:

- FuelRecord
- ProcurementRecord
- ElectricityRecord
- TravelBooking

These models preserve the exact source schema from upstream systems.

Example:

python class FuelRecord(models.Model):     EBELN = models.CharField(...)     TXZ01 = models.TextField(...)     MENGE = models.FloatField(...) 

Why this design was chosen:

- Prevents loss of source information
- Enables reprocessing later
- Allows audit and debugging
- Keeps ingestion independent from ESG normalization logic

Raw records are never modified after ingestion.

---

# ESG Normalized Layer

Normalized ESG models were created separately:

- FuelESGRecord
- ProcurementESGRecord
- ElectricityESGRecord
- TravelESGRecord

These contain standardized fields used for ESG analytics.

Example normalized fields:

- activity_date
- facility
- supplier
- scope
- normalized_quantity
- normalized_unit
- calculated_emission

This separation enables:

- Consistent analytics
- Easier reporting
- Cross-source aggregation
- Standardized emissions calculation

---

# Scope 1 / 2 / 3 Categorization

The system explicitly stores ESG scope classification.

## Scope Mapping

### Scope 1
Direct emissions from owned operations.

Example:
- Diesel fuel
- Gasoline
- Natural gas

Stored in:
- FuelESGRecord

---

### Scope 2
Indirect emissions from purchased electricity.

Stored in:
- ElectricityESGRecord

---

### Scope 3
Indirect supply chain and travel emissions.

Examples:
- Procurement
- Business travel

Stored in:
- ProcurementESGRecord
- TravelESGRecord

---

# Unit Normalization

Enterprise systems often provide inconsistent units:

Examples:

- L
- Liter
- litres
- GAL
- kg
- tons

A normalization layer converts them into standardized units.

Example:

python normalize_unit_and_quantity() 

This ensures:

- Consistent emission calculations
- Accurate aggregation
- Cross-system comparability

Normalized fields stored:

python normalized_quantity normalized_unit 

The original source values are still preserved in raw records.

---

# Emission Calculation Engine

Emission calculations are separated into reusable functions:

Examples:

python calculate_fuel_emission() calculate_electricity_emission() calculate_travel_emission() 

Emission factors are stored separately in the EmissionFactor table.

Benefits:

- Easy factor updates
- Regulatory adaptability
- Reusable calculation logic
- Cleaner architecture

---

# Validation Engine

Validation logic is decoupled from ingestion.

Validation issues are stored independently using:

python ValidationIssue 

Supported severities:

- WARNING
- SUSPICIOUS
- FAILED

Examples:

- Missing activity date
- Extremely high fuel quantity
- Invalid unit
- Missing supplier
- Suspicious travel expense

This enables:

- Data quality dashboards
- Governance workflows
- ESG audit readiness

---

# Audit Trail

Auditability is a major requirement in ESG systems.

The platform can support audit trails by including its logic in backend using timestamps and other fields.

---

# Normalized Payload Storage

Each ESG model stores:

python normalized_payload = models.JSONField(default=dict) 

This allows:

- Flexible metadata storage
- Schema evolution
- Preservation of transformation details
- Easier debugging

Without requiring schema migrations for every new field.

---

# Generic Validation Architecture

The validation engine uses Django GenericForeignKey:

python content_type object_id content_object 

This allows a single ValidationIssue table to work across:

- Fuel records
- Procurement records
- Electricity records
- Travel records

Benefits:

- Centralized validation system
- Extensible architecture
- Reduced duplication

---

# Monthly Analytics Design

The analytics layer aggregates emissions using:

python TruncMonth(activity_date) 

This enables:

- Monthly ESG reporting
- Trend analysis
- Dashboard visualizations
- Scope-wise analytics

---

# Frontend Integration

The React frontend consumes APIs for:

- Dashboard summaries
- Monthly emissions
- Validation insights
- ESG record listings
- File uploads

Bootstrap and Recharts are used for:

- Responsive dashboards
- Interactive charts
- Validation tables
- ESG analytics visualization

---

# Scalability Considerations

The platform was designed to scale with additional ESG domains.

Future extensibility includes:

- Water consumption
- Waste management
- Renewable energy
- Supplier sustainability scoring
- Carbon offsets
- ESG benchmarking
- AI-powered anomaly detection

New ESG domains can be added without changing the existing architecture.

---

# Why This Data Model Was Chosen

This architecture was chosen because enterprise ESG systems require:

- Strong traceability
- Immutable source preservation
- Standardized analytics
- Audit readiness
- Flexible ingestion
- Extensibility

The layered model separates concerns cleanly:

| Layer | Responsibility |
|---|---|
| Raw Records | Preserve source data |
| ESG Records | Standardize ESG structure |
| Validation Engine | Ensure data quality |
| Calculation Engine | Compute emissions |
| Analytics Layer | Reporting and dashboards |

This design improves maintainability, scalability, and regulatory compliance.
