# Data & AI Architecture Guidelines

## Data Platform Pattern Selection

### When to Use Which Pattern

| Pattern | Use When | Avoid When |
|---|---|---|
| **Data Warehouse** (Synapse, Fabric) | Structured, historical, analytical queries; known schema; business reporting | Real-time streaming; highly variable schema |
| **Data Lake** (ADLS Gen2) | Raw data storage; diverse formats; exploration; ML training data | Single source of truth for operational data |
| **Data Lakehouse** (Fabric / Delta Lake) | Combine warehouse structure with lake flexibility; ACID on large data | Simple reporting-only scenarios (overkill) |
| **Data Mesh** | Multiple autonomous domain teams; data-as-product ownership model; scale beyond central platform team | Small org; single domain; limited data engineering capacity |
| **Operational data store** (Cosmos DB) | Real-time, transactional read/write; global distribution | Large-scale batch analytics |

### Data Mesh Domain Data Product Checklist

A domain data product is production-ready when it has:
- [ ] A named Data Product Owner (business role)
- [ ] Documented schema with field-level definitions and data types
- [ ] Data classification applied to every field
- [ ] SLA defined: freshness, availability, quality threshold
- [ ] Registered in the data catalog (LeanIX Data Objects or external catalog)
- [ ] Lineage documented: source systems → transformations → output
- [ ] Access control defined: who can read, who can write, approval process
- [ ] Retention policy defined and enforced
- [ ] Quality checks automated (null rates, referential integrity, range checks)

## Data Classification Process

1. Identify all data fields/entities in the scope of the proposal
2. Apply classification (Public / Internal / Confidential / Restricted) per field using these triggers:

| Classification | Apply when field contains |
|---|---|
| **Public** | Information already public; non-sensitive metadata |
| **Internal** | Business operations data, non-personal; internal reports |
| **Confidential** | Commercial sensitive; personal data (name, email, employee records) |
| **Restricted** | Special category personal data (health, biometric, race); financial account data; legal privilege; regulated data under GDPR Art. 9 |

3. Apply controls based on classification — see `agents/security/policies.md`
4. Register classifications in LeanIX Data Objects

## AI/ML System Design Guidelines

### Before Building Any AI System

Answer these questions before beginning design:

| Question | Required For |
|---|---|
| What is the EU AI Act risk classification? | All AI systems |
| What is the system's decision scope? (advisory vs. automated) | All AI systems |
| What training data is being used and what is its provenance? | All ML models |
| How will the model's decisions be explained to users? | High-risk systems |
| What is the human override / review mechanism? | High-risk systems |
| How will model drift be detected and addressed? | Production ML systems |
| What happens if the model is wrong? (failure mode) | All AI systems |
| What biases could the training data introduce? | All ML models |

### EU AI Act Risk Classification Quick Reference

| Risk Level | Examples | Architecture Requirements |
|---|---|---|
| **Unacceptable** | Social scoring, real-time biometric surveillance in public | **Prohibited — do not build** |
| **High Risk** | CV screening, credit scoring, employee monitoring, safety-critical systems | Conformity assessment, human oversight, explainability, bias testing, audit trail, registration in EU database |
| **Limited Risk** | Chatbots, deepfakes | Transparency obligation: users must know they interact with AI |
| **Minimal Risk** | Spam filters, recommendation engines, AI in games | Standard development and monitoring |

### MLOps Maturity Model (target state: Level 3)

| Level | Description | Key Capabilities |
|---|---|---|
| **0 — Manual** | Ad hoc scripts, no pipeline, manual deployment | — |
| **1 — ML Pipeline** | Automated training pipeline; manual deployment | Reproducible training, experiment tracking |
| **2 — CI/CD** | Automated testing and deployment of models | Model registry, automated evaluation gate |
| **3 — Automated Retraining** | Models retrain on trigger (drift or schedule) | Full automation, monitoring, rollback |

> **Requirement:** Production AI systems must achieve MLOps Level 2 minimum before go-live. Level 3 required for High-Risk AI systems.

## How to Write a Data Architecture Decision

```
## Data Architecture Decision

Data Domain: [e.g., Customer, Product, Order]
System of Record: [Application name + LeanIX ID]
Data Objects Affected: [LeanIX Data Object IDs]
Classification: [Public / Internal / Confidential / Restricted]

Storage Pattern: [Data warehouse / Lake / Lakehouse / Operational DB / etc.]
Rationale: [Why this pattern for this data]

Lineage:
  Source: [System A] → Transform: [Pipeline/Process] → Consumer: [System B, System C]

Governance:
  Owner: [Business role — not a team name]
  Steward: [Data steward name/role]
  Quality SLA: [Completeness ≥ X%, Freshness within Y hours]
  Retention: [Period] — Deletion method: [how]

Privacy:
  Personal data present: YES / NO
  DPIA required: YES / NO / COMPLETED [link]
  Data minimization applied: [description]
```
