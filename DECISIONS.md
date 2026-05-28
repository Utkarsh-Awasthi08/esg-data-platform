# Engineering Decisions & Assumptions

## Overview

This document captures the major ambiguities, assumptions, architectural decisions, and trade-offs made during implementation of the ESG Analytics Platform.

The provided datasets and requirements intentionally left several areas open-ended. This document explains:

- What assumptions were made
- Why certain implementation choices were selected
- What was intentionally ignored
- What additional clarification would be requested from a Product Manager or ESG domain expert

---

# 1. Raw vs Normalized Data Separation

## Ambiguity

The requirements did not explicitly define whether source records should be modified directly or transformed into a separate ESG structure.

## Decision

A layered architecture was implemented:

- Raw source records stored unchanged
- Separate normalized ESG records created independently

Example:

- FuelRecord → FuelESGRecord
- ElectricityRecord → ElectricityESGRecord

## Why

This approach preserves:

- Source-of-truth integrity
- Auditability
- Reprocessing capability
- ESG transformation traceability

It also prevents accidental corruption of source system data.

## What I Would Ask the PM

- Should normalized ESG records be versioned?
- Should users be able to manually override normalized values?

---

# 2. Multi-Tenancy Design

## Ambiguity

The requirements mentioned multi-tenancy support but did not define tenant structure.

## Decision

The schema was designed to be tenant-ready using a future Tenant foreign key on major models.

Tenant isolation was planned but not fully implemented because authentication and organization management were outside the project scope.

## Why

This allows future SaaS scalability while keeping the current implementation simpler.

## What I Would Ask the PM

- Is the platform single-tenant or SaaS multi-tenant?
- Should tenants share emission factors?
- Are tenant-specific validation rules required?

---

# 3. ESG Scope Classification

## Ambiguity

The mapping of source datasets to Scope 1, 2, and 3 emissions was not explicitly defined.

## Decision

The following mapping was used:

| Data Type | Scope |
|---|---|
| Fuel | Scope 1 |
| Electricity | Scope 2 |
| Procurement | Scope 3 |
| Travel | Scope 3 |

## Why

This follows common GHG Protocol standards.

## What I Would Ask the PM

- Are there organization-specific scope mappings?
- Should purchased fuels ever be classified differently?
- Should hybrid emissions be supported?

---

# 4. Unit Normalization Strategy

## Ambiguity

The datasets contained inconsistent units and abbreviations.

Examples:

- L
- Liter
- litres
- GAL
- kWh

## Decision

A centralized normalization function was implemented:

python id="i0pbvd" normalize_unit_and_quantity() 

Normalized values are stored separately while preserving original source values.

## Why

This ensures:

- Consistent analytics
- Accurate emission calculations
- Cross-source comparability

## What I Would Ask the PM

- Which unit standards should be followed?
- Are imperial units expected globally?
- Should automatic currency conversion also be implemented?

---

# 5. Emission Factor Strategy

## Ambiguity

The requirements did not define official emission factor sources.

## Decision

A simplified internal EmissionFactor table was created.

Initial matching was keyword-based.

Examples:

- diesel
- gasoline
- jet fuel

## Why

This provided a working emissions engine while keeping implementation manageable.

## Trade-Off

Keyword matching is simpler but less accurate than taxonomy-based classification.

## What I Would Ask the PM

- Which regulatory standard should be followed?
  - EPA
  - DEFRA
  - GHG Protocol
  - IPCC
- Should emission factors be region-specific?
- Should historical factor versioning be supported?

---

# 6. Fuel Detection Logic

## Ambiguity

Product descriptions in procurement/fuel data were inconsistent and noisy.

Examples:

- Heavy Duty Engine Oil
- Aviation Turbine Fuel
- Hydraulic Fluid

## Decision

A whitelist and blacklist keyword approach was implemented.

### Valid Fuel Keywords

- diesel
- gasoline
- petrol
- jet fuel
- aviation turbine fuel
- lng
- cng

### Invalid Keywords

- filter
- lubricant
- hydraulic
- grease
- coolant

## Why

This reduced false positives while remaining easy to extend.

## Trade-Off

This approach may still misclassify edge cases.

## What I Would Ask the PM

- Is there an official product taxonomy available?
- Are ERP material codes standardized?
- Should ML/NLP classification be introduced later?

---

# 7. Validation Engine Design

## Ambiguity

Validation severity definitions were not specified.

## Decision

Three severity levels were introduced:

| Severity | Meaning |
|---|---|
| WARNING | Minor issue |
| SUSPICIOUS | Likely anomaly |
| FAILED | Invalid data |

Validation issues are stored independently using GenericForeignKey relationships.

## Why

This supports:

- Reusable validation architecture
- Centralized issue tracking
- Extensible rule management

## What I Would Ask the PM

- Which issues should block ingestion?
- Should validation rules be configurable by tenant?
- Should users be able to resolve validation issues manually?

---

# 8. Source-of-Truth Tracking

## Ambiguity

Requirements mentioned source tracking but not implementation details.

## Decision

An UploadedFile model was implemented to track:

- Filename
- Source system
- File type
- Upload timestamp

Each ESG record references its original raw record.

## Why

This enables full lineage tracking.

## What I Would Ask the PM

- Should ingestion batches be versioned?
- Should source systems have authentication metadata?
- Is rollback functionality required?

---

# 9. Audit Trail Strategy

## Ambiguity

The depth of auditability required was unspecified.

## Decision

The following audit fields were implemented:

- created_at
- normalized_payload
- source tracking
- validation history

## Why

This creates traceability without excessive complexity.

## Trade-Off

No historical row versioning was implemented.

## What I Would Ask the PM

- Are regulatory audit requirements expected?
- Is immutable event logging required?
- Should every edit be historically preserved?

---

# 10. Monthly Emissions Aggregation

## Ambiguity

The reporting granularity was not specified.

## Decision

Monthly aggregation was implemented using:

python id="p6ynw8" TruncMonth(activity_date) 

## Why

Monthly ESG reporting is standard for sustainability dashboards.

## What I Would Ask the PM

- Is quarterly reporting required?
- Should fiscal-year grouping be supported?
- Are custom reporting calendars needed?

---

# 11. Travel API Integration

## Ambiguity

The travel API provided limited booking information.

Missing:

- Distance
- Flight class
- Route
- Passenger count

## Decision

Travel emissions were estimated using spend-based calculations.

## Why

This allowed travel integration without requiring additional APIs.

## Trade-Off

Spend-based estimation is less accurate than distance-based emissions.

## What I Would Ask the PM

- Can route information be provided?
- Should cabin-class multipliers be supported?
- Should hotel and train travel also be included?

---

# 12. What Subsets Were Implemented

## Fuel Dataset

Handled:

- Fuel type
- Quantity
- Unit normalization
- Supplier
- Facility
- Activity date

Ignored:

- Storage location analytics
- Detailed SAP procurement hierarchy

---

## Procurement Dataset

Handled:

- Material description
- Supplier
- Spend amount
- Scope 3 categorization

Ignored:

- Asset accounting complexity
- Cost center hierarchy
- Depreciation logic

---

## Electricity Dataset

Handled:

- Meter usage
- Billing periods
- kWh normalization
- Scope 2 emissions

Ignored:

- Peak/off-peak tariff analysis
- Renewable energy certificates
- Grid-region emission differences

---

## Travel API

Handled:

- Booking amount
- Booking status
- Import timestamp

Ignored:

- Flight distance
- Cabin class
- Multi-leg travel
- Hotel emissions

---

# 13. Frontend Dashboard Decisions

## Ambiguity

Dashboard KPIs and visualizations were not specified.

## Decision

Implemented:

- Summary cards
- Monthly trend charts
- Scope distribution charts
- Validation insights table

Using:

- React
- Bootstrap
- Recharts

## Why

These visualizations demonstrate ESG analytics clearly while remaining lightweight.

## What I Would Ask the PM

- Which KPIs matter most?
- Should executive reporting exports exist?
- Is PDF report generation required?

---

# 14. Architecture Trade-Offs

## Chosen Priorities

The implementation prioritized:

- Clarity
- Extensibility
- Auditability
- Separation of concerns
- Demonstrable ESG workflows

Over:

- Microservice complexity
- Advanced optimization
- Enterprise-scale orchestration

---

# 15. Future Improvements

Potential next steps:

- Tenant authentication
- Async ingestion pipelines
- ML anomaly detection
- Real ESG factor registries
- Event sourcing
- Approval workflows
- ESG benchmarking
- GraphQL analytics APIs
- Data warehouse integration

---

# Conclusion

The implementation intentionally balanced:

- Practicality
- Simplicity
- Extensibility
- ESG domain alignment

The resulting architecture demonstrates:

- Enterprise-style ESG ingestion
- Data normalization
- Validation workflows
- Emission calculations
- Traceability
- Analytics reporting

while remaining maintainable and extensible for future development.
