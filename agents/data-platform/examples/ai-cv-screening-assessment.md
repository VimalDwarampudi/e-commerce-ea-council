# Example: Data & AI Assessment — AI-Powered CV Screening System

## Input (Request Summary)

> "We want to implement an AI system that automatically shortlists candidates from CV uploads before any human recruiter reviews them. The model would be trained on our historical hiring data."

## Output (Data & AI Assessment)

## Data & AI Architecture Assessment

### Data Landscape Context
**LeanIX Data Objects query:**
- `HR.Candidate.Profile` — Data classification: **Restricted** (personal data including name, address, employment history, education). Owner: HR Director. System of record: HR-Recruitment-Greenhouse.
- `HR.Employee.HiringDecision` — Data classification: **Restricted** (hiring decisions linked to individuals). Owner: HR Director. Currently not formally modelled as a Data Object in LeanIX — flagged as documentation gap.

**Known data quality issues:** Historical hiring data in Greenhouse spans 8 years and 3 prior ATS systems. Data consistency across periods is unknown. A data quality assessment must be completed before this data is used as training data.

### Data Architecture Recommendation
**Training data pipeline:**
- Source: HR-Recruitment-Greenhouse + historical ATS exports (Bronze layer in ADLS Gen2)
- Processing: Azure ML data pipeline — feature engineering from CV text + structured fields
- Feature store: Fabric Gold layer, `HR.Candidate.Features` data product
- Model registry: Azure ML Model Registry (versioned, with lineage to training dataset)

**Inference pipeline:**
- Trigger: New CV upload to Greenhouse (webhook → Azure Function)
- Processing: Azure ML Managed Endpoint (real-time inference)
- Output: Shortlist score + explanation written back to Greenhouse as a custom field
- **Human review gate: MANDATORY** (see EU AI Act classification below)

### ⚠️ EU AI Act Classification: HIGH RISK

This system falls under **EU AI Act Annex III — HIGH RISK AI system.**

**Applicable category:** Annex III, Point 4 — "AI systems used for recruitment or selection of natural persons, notably for advertising vacancies, screening or filtering applications, evaluating candidates in the course of interviews or tests."

**Mandatory requirements before deployment:**
| Requirement | Status | Action Required |
|---|---|---|
| Conformity assessment | ❌ Not done | Internal conformity assessment required |
| Human oversight mechanism | ❌ Not in proposal | **MUST be designed in — see below** |
| Explainability of decisions | ❌ Not in proposal | Responsible AI Dashboard required |
| Bias / fairness testing | ❌ Not in proposal | Fairness testing on protected characteristics required |
| Audit trail of AI decisions | ❌ Not in proposal | Immutable log of every shortlist decision required |
| Registration in EU AI database | ❌ Not done | Required before deployment |
| Technical documentation | ❌ Not done | Model card + system documentation required |

**Current proposal as stated CANNOT be approved.** It describes a fully automated shortlisting system with no human review before candidates are rejected. This is non-compliant under EU AI Act for a High-Risk system.

### Recommended Redesign for Compliance

The system can be built — but the workflow must change:

```
CURRENT (proposed — non-compliant):
CV Upload → AI Model → Shortlist/Reject → Recruiter sees only shortlisted candidates

REQUIRED (compliant):
CV Upload → AI Model → Ranked candidates + explanation scores → Recruiter reviews ALL 
           candidates with AI scores as a decision-support tool → Recruiter makes final 
           shortlisting decision → AI recommendation vs final decision logged for audit
```

**Key difference:** The AI is a **decision-support tool**, not a decision-making system. Recruiters see all candidates; the AI provides ranked scores and explanations to help prioritise review. Rejection requires human action.

### Privacy & Data Minimization
**DPIA is mandatory** — this system processes special category data (employment-related personal data at scale, using new AI technology, with potential for systematic impact on individuals).

**GDPR Article 22 risk:** Automated individual decision-making. The compliant redesign above (human in the loop) mitigates this, but the DPIA must confirm that no candidates are rejected solely by automated means.

**Data minimization:** Training data must be limited to fields relevant to job performance prediction. Fields like name, address, photo, date of birth, and nationality must be **excluded from training features** to reduce bias risk and comply with data minimization (GDPR Art. 5).

**Retention of AI decision data:** AI scores and explanations are personal data and must be retained for the duration of the recruitment process + any applicable appeal period. After that, they are subject to the same deletion rights as other recruitment data.

### Recommendation
**Do not approve this proposal as currently described.** Approve it only after:

1. Redesigning the workflow: AI as decision-support, not decision-maker (human in the loop)
2. Completing a DPIA (mandatory — RC-POL-002)
3. Excluding protected characteristic proxies from training features
4. Implementing the Responsible AI Dashboard (explainability + fairness monitoring)
5. Designing and implementing an immutable audit trail
6. Completing a conformity assessment for EU AI Act High-Risk classification
7. Registering the system in the EU AI database before deployment

### Dependencies on Peer Domains
- **Risk & Compliance:** DPIA required before architecture endorsement; EU AI Act conformity assessment process.
- **Security Architecture:** Threat model on training data pipeline; model poisoning risk; data access to Restricted HR data.
- **Application Architecture:** Greenhouse integration design for AI score write-back.

## Key Points Illustrated
- LeanIX Data Objects queried first; documentation gap found
- EU AI Act classification performed immediately — governs everything else
- Proposal is not rejected outright; a compliant path forward is provided
- GDPR Art. 22 risk identified and mitigated in the redesign
- Data minimization applied to training features
- All mandatory EU AI Act requirements listed with current status
- DPIA trigger correctly identified
