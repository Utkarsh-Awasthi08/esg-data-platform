# TRADEOFFS.md

## Overview

This document explains the major architectural and implementation tradeoffs made during development of the ESG Data Ingestion and Analytics Platform.

The goal of the project was to build a reliable, extensible, and auditable ESG ingestion system within limited development time while prioritizing correctness, normalization, validation, and analytics visibility.

---

# 1. Did Not Build Asynchronous Processing Pipeline

## What Was Not Built

The ingestion pipeline currently processes uploaded files synchronously inside the API request lifecycle.

This means:
- CSV parsing
- normalization
- emission calculation
- validation
- database persistence

all happen during the upload request itself.

I did not implement:
- Celery workers
- background jobs
- Kafka/RabbitMQ queues
- distributed processing
- retry orchestration

---

## Why

The current dataset sizes are relatively small and suitable for synchronous processing during evaluation.

Adding asynchronous infrastructure would significantly increase:
- operational complexity
- deployment requirements
- debugging overhead
- infrastructure dependencies

without materially improving the evaluation goals.

The priority was correctness, traceability, and domain modeling rather than high-scale distributed ingestion.

---

## Tradeoff

### Advantages
- Simpler architecture
- Easier debugging
- Faster development iteration
- Easier local setup
- Fewer infrastructure dependencies

### Limitations
- Large files may block requests
- Upload latency increases with dataset size
- No retry queue for failed processing
- Limited horizontal scalability

---

## Future Improvement

For production-scale ingestion, I would introduce:
- Celery workers
- Redis/RabbitMQ queues
- chunked batch processing
- async validation jobs
- retry/dead-letter handling

---

# 2. Did Not Implement Full Dynamic Emission Factor Engine

## What Was Not Built

Emission calculation currently uses:
- predefined emission factors
- keyword-based fuel matching
- category-based lookup logic

I did not implement:
- region-specific emission factors
- time-versioned factor libraries
- external emissions APIs
- AI/NLP-based material classification
- lifecycle analysis models
- factor hierarchy resolution

---

## Why

The primary evaluation goal appeared to focus on:
- ingestion architecture
- normalization
- validation
- auditability
- analytics capability

rather than scientific emissions modeling accuracy.

A simplified but extensible emission factor engine allowed:
- demonstrating Scope 1/2/3 calculations
- showing normalization workflows
- maintaining explainability
- keeping logic deterministic

without introducing excessive domain complexity.

---

## Tradeoff

### Advantages
- Transparent calculations
- Easy debugging
- Easy extensibility
- Deterministic outputs
- Minimal external dependencies

### Limitations
- Limited emissions accuracy
- Incomplete fuel categorization
- No geography-aware factors
- No temporal factor versioning
- Simplified Scope 3 procurement modeling

---

## Future Improvement

Future versions would include:
- factor version management
- EPA/IPCC factor datasets
- country/grid-specific electricity factors
- NLP-based procurement classification
- supplier-specific emissions profiles
- configurable factor hierarchies

---

# 3. Did Not Build Full Authentication & Tenant Isolation Layer

## What Was Not Built

The current system models multi-tenancy conceptually in the data architecture but does not yet implement:
- user authentication
- role-based access control
- tenant-aware query filtering
- organization-scoped dashboards
- API authorization policies

---

## Why

The focus of the assignment was primarily:
- ESG ingestion
- normalization
- validation
- analytics
- auditability

rather than security infrastructure or SaaS account management.

Implementing enterprise-grade multi-tenant authorization would require:
- JWT/OAuth flows
- RBAC systems
- tenant middleware
- scoped query managers
- permission matrices

which would significantly expand project scope.

Instead, the schema and architecture were designed so tenant isolation can be added later without major refactoring.

---

## Tradeoff

### Advantages
- Faster feature delivery
- Simpler testing
- Cleaner debugging
- More focus on ESG workflows

### Limitations
- No tenant-level security
- No user separation
- No permissions model
- No organization-scoped APIs

---

## Future Improvement

Production implementation would include:
- JWT authentication
- tenant-aware middleware
- RBAC permissions
- organization-level data isolation
- audit access logging
- API rate limiting

---

# Final Reflection

The project intentionally prioritizes:
1. Data correctness
2. Traceability
3. Validation visibility
4. ESG normalization workflows
5. Extensible architecture

over enterprise-scale infrastructure concerns.

The architecture was designed to remain extensible so that asynchronous processing, advanced emissions modeling, and enterprise multi-tenancy can be added incrementally without redesigning the core data model.
