# SOURCES.md

# Overview

This document explains the external source formats researched for the ESG ingestion platform, what assumptions were made while modeling them, how the sample datasets were designed, and what limitations or operational risks would exist in a real-world deployment.

The system currently supports three ESG data sources:

1. Fuel Procurement Data
2. Procurement / Purchased Goods Data
3. Electricity Utility Data

Additionally, a travel booking API integration was partially modeled for future Scope 3 travel emissions.

---

# 1. Fuel Procurement Source

## Real-World Format Researched

The fuel procurement source was modeled after SAP ERP procurement exports, especially:
- SAP MM (Materials Management)
- Purchase Order extracts
- Vendor procurement datasets

Typical enterprise exports from SAP are delivered as:
- CSV exports
- Excel reports
- scheduled flat-file dumps
- IDoc/API integrations

Common SAP fields researched included:
- EBELN (Purchase Order)
- MATNR (Material Number)
- TXZ01 (Material Description)
- MENGE (Quantity)
- MEINS (Unit)
- WERKS (Plant/Facility)
- LIFNR (Vendor ID)

---

## What I Learned

Real-world fuel procurement datasets are highly inconsistent because:
- fuel names are not standardized
- units vary across suppliers
- procurement descriptions often contain unrelated maintenance products
- organizations mix fuel and non-fuel items in the same extracts

For example:
- "Diesel Fuel"
- "Diesel ULSD"
- "Automotive Gas Oil"
- "Jet A-1"
- "Hydraulic Oil"
- "Heavy Duty Lubricant"

all appear in similar procurement feeds.

This required:
- keyword-based classification
- invalid keyword filtering
- unit normalization
- validation rules for suspicious records

---

## What My Sample Data Looks Like

The sample dataset includes:
- diesel fuel purchases
- gasoline/petrol purchases
- aviation fuel
- LNG/CNG examples
- supplier metadata
- facility metadata
- inconsistent units

Example fields:
- fuel description
- quantity
- unit
- supplier
- plant/facility
- procurement date

I intentionally included:
- invalid fuel-like products
- missing units
- suspicious quantities
- inconsistent naming

to test validation and normalization logic.

---

## Why I Chose This Structure

The structure demonstrates:
- Scope 1 fuel activity ingestion
- normalization workflows
- emission calculation
- validation visibility
- source-of-truth traceability

while remaining realistic enough for enterprise procurement data.

---

## What Would Break in Real Deployment

Several issues would arise in production:

### 1. Material Classification Complexity
Keyword matching would fail for:
- multilingual descriptions
- internal ERP naming conventions
- vendor-specific abbreviations

A production system would require:
- master data mapping
- ML/NLP classification
- supplier catalogs

---

### 2. Unit Inconsistency
Real deployments encounter:
- liters
- gallons
- kilograms
- barrels
- metric tons

often within the same source.

Current normalization handles only a subset.

---

### 3. Duplicate Procurement Records
SAP exports frequently contain:
- reposted entries
- reversed invoices
- adjustment records
- duplicate extracts

Current implementation does not yet support deduplication strategies.

---

### 4. Missing Activity Dates
Enterprise procurement systems often:
- omit dates
- use multiple date columns
- use fiscal periods instead of transaction dates

The current implementation assumes a single activity date field.

---

# 2. Procurement / Purchased Goods Source

## Real-World Format Researched

This source was modeled after:
- SAP procurement extracts
- supplier spend reports
- ERP purchasing exports

with a focus on Scope 3 purchased goods and services emissions.

Typical enterprise procurement feeds contain:
- material descriptions
- categories
- spend amounts
- suppliers
- currencies
- facilities/business units

---

## What I Learned

Procurement emissions are significantly more ambiguous than fuel or electricity data because:
- spend-based accounting is common
- material descriptions are inconsistent
- suppliers rarely provide embedded carbon data
- categories are difficult to classify automatically

Most organizations estimate Scope 3 procurement emissions using:
- spend-based emission factors
- category mappings
- supplier averages

rather than direct activity measurements.

---

## What My Sample Data Looks Like

The sample procurement dataset includes:
- machinery procurement
- industrial materials
- maintenance items
- supplier information
- spend amounts
- currencies
- quantity/unit combinations

I intentionally included:
- incomplete procurement categories
- inconsistent units
- missing supplier metadata
- suspiciously large quantities

to exercise the validation engine.

---

## Why I Chose This Structure

The dataset demonstrates:
- Scope 3 ingestion
- procurement normalization
- supplier traceability
- spend tracking
- auditability

without requiring highly specialized lifecycle-analysis datasets.

---

## What Would Break in Real Deployment

### 1. Supplier Emissions Are Missing
Real ESG systems often require:
- supplier-specific carbon disclosures
- EPDs (Environmental Product Declarations)
- lifecycle emissions data

The current implementation uses simplified estimation logic.

---

### 2. Procurement Categories Are Inconsistent
Organizations use:
- custom material groups
- internal ERP taxonomies
- inconsistent category naming

which makes automatic categorization difficult.

---

### 3. Currency Conversion
Real deployments require:
- FX conversion
- historical exchange rates
- multi-region accounting

The current system stores currency but does not normalize FX values.

---

### 4. Spend-Based Calculations
Production Scope 3 systems often calculate emissions using:
- spend × category factor

The current implementation only partially models this.

---

# 3. Electricity Utility Source

## Real-World Format Researched

The electricity source was modeled after:
- utility billing exports
- smart meter reports
- energy management system CSV exports

Common fields researched:
- meter ID
- facility ID
- billing period
- kWh usage
- tariff code
- readings
- charges
- currency

---

## What I Learned

Electricity data is operationally cleaner than procurement data but still contains:
- inconsistent billing periods
- estimated readings
- duplicated invoices
- multiple meter types
- missing usage values

I also learned that electricity datasets frequently contain:
- financial billing information
- tax lines
- tariff structures

mixed together with consumption data.

---

## What My Sample Data Looks Like

The sample utility dataset includes:
- facility identifiers
- billing periods
- electricity consumption
- meter readings
- tariff metadata
- charges and currency

I intentionally included:
- missing readings
- abnormal usage values
- incomplete billing periods
- suspicious consumption spikes

to support validation testing.

---

## Why I Chose This Structure

This structure demonstrates:
- Scope 2 emissions ingestion
- utility normalization
- monthly emissions analytics
- meter-level tracking
- facility-level reporting

while remaining realistic for utility invoice exports.

---

## What Would Break in Real Deployment

### 1. Regional Grid Factors
Electricity emissions depend heavily on:
- geography
- utility provider
- grid mix
- renewable sourcing

The current implementation uses simplified factors.

---

### 2. Billing Period Complexity
Real invoices often:
- overlap months
- contain corrections
- use estimated readings
- include multiple meters

The current implementation treats each row independently.

---

### 3. Time-Series Aggregation
Production systems require:
- hourly granularity
- interval meter data
- peak/off-peak calculations

The current system only supports simplified monthly aggregation.

---

### 4. Renewable Energy Accounting
Real ESG systems may require:
- RECs
- PPAs
- market-based accounting
- location-based accounting

which are not yet implemented.

---

# 4. Travel Booking API (Future Scope 3 Integration)

## Real-World Format Researched

The travel integration was modeled after corporate travel booking APIs containing:
- booking IDs
- trip IDs
- booking status
- fare amounts
- currencies
- timestamps

---

## What I Learned

Travel data is highly fragmented across:
- airlines
- hotels
- rail providers
- expense systems

Most APIs expose:
- financial data
- itinerary metadata
- booking status

but not direct emissions.

Emissions must usually be derived from:
- route distance
- cabin class
- travel type
- transport mode

---

## Why It Was Only Partially Implemented

The assignment focus appeared centered on:
- ingestion architecture
- ESG normalization
- validation
- analytics

rather than full travel lifecycle modeling.

I modeled the ingestion structure and API handling approach but did not fully implement:
- flight distance calculations
- travel emissions factors
- itinerary parsing

---

# Final Reflection

The datasets were intentionally designed to balance:
- realism
- implementation feasibility
- ESG domain coverage
- validation complexity

The system prioritizes:
- auditability
- extensibility
- normalization
- traceability

over exhaustive production-grade ESG accounting complexity.

The architecture is intentionally extensible so more sophisticated:
- emissions methodologies
- supplier integrations
- regional factors
- asynchronous ingestion pipelines

can be added incrementally.
