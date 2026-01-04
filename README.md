# Electoral Roll Integrity & Demographic Analysis (India)

## Overview

Electoral rolls are not merely databases; they are constitutional instruments that underpin democratic legitimacy.  
Errors, distortions, or stress—whether accidental or systemic—can affect public trust even when elections remain procedurally fair.

This repository contains a legally compliant, aggregate-level data analytics system designed to study:

- Structural health of electoral rolls  
- Demographic consistency  
- Migration-induced stress on constituencies  

No individual voter data is processed.  
No electoral roll modifications are performed.  
This project functions strictly as an administrative analytics layer, not an operational election system.

---

## Project Objectives

### Primary Goals

1. Assess statistical health of electoral rolls  
2. Study migration pressure and demographic stress  
3. Demonstrate legally safe, aggregate-only electoral analytics  

---

## Metrics Designed & Studied

### Statistical Health Index (SHI)

A diagnostic composite index, not an allegation mechanism.

**Elector Coverage Ratio (ECR)**  
ECR = Number of Electors / Total Population

**Gender Balance Ratio (GBR)**  
GBR = Female Population / Male Population

**Additional Signals**
- Population pyramid consistency  
- Age distribution sanity checks  
- Net roll additions vs deletions  

All metrics are ratio-based and scale-invariant.

---

### Migration Pressure Index (MPI)

MPI = Inward Migrant Electors / Total Electors

Used to identify constituencies under migration-induced administrative stress.

---

## Data Scope & Legal Constraints

### Included (Aggregate Only)

| Category | Granularity |
|--------|-------------|
| Population | District / State |
| Gender Ratio | District |
| Population Pyramid | District / State |
| Elector Counts | District |
| Per Capita Income | District |
| Migration Indicators | District / State |

### Explicitly Excluded

- Individual voter data  
- Booth-level data  
- Personally identifiable information  

---

## Data Acquisition Methodology

- No web scraping  
- Programmable Search Engine (Google CSE)  
- Domain allow-list enforced  
- Deterministic ranking + Gemini-based content ranking  
- Top PDFs selected based on relevance and granularity  

Storage structure:

data/raw/<task_name>/<pdf_hash>.pdf

---

## Knowledge Extraction Methodology

- Direct text extraction  
- OCR fallback for scanned PDFs  
- AI-assisted classification (no data invention)  
- Atomic fact extraction with confidence flags  

Garbage or partial values are retained but flagged.

---

## Maharashtra Case Study (2024–2025)

- Population (2026 est.): ~12.9 crore  
- Registered electors: ~9.7 crore  
- Elector coverage: ~75%  
- Balanced gender ratios with district-level variation  
- Urban districts show inward migration pressure  

---

## Ethical & Legal Safeguards

- No individual-level inference  
- No roll modification  
- No voting-day usage  
- Aggregate analytics only  

Aligned with ECI manuals, Representation of the People Act, and Supreme Court jurisprudence.

---

## Repository Purpose

This project demonstrates how electoral analytics can be conducted responsibly—  
combining statistical rigor, legal restraint, and explainable AI.

---

## Status

- Data ingestion: Complete  
- Metric formulation: Complete  
- Maharashtra pilot: Complete  
- Visualization: Pending  
- Simulation: Planned
