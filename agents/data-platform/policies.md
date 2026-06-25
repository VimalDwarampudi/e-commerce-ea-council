# Data & AI Architecture Policies

## DA-POL-001: Data Classification is Mandatory [MANDATORY]

All data objects must be classified before they are used in any architecture proposal. Classification levels:

| Level | Description | Handling |
|---|---|---|
| **Public** | Intentionally public information | No restrictions |
| **Internal** | Business operational data, not sensitive | Access controls, no external sharing without approval |
| **Confidential** | Commercially sensitive, personal data | Encryption at rest and in transit, access audit trail |
| **Restricted** | Regulated data (PII, health, financial, legal) | Strictest controls, GDPR/regulatory compliance required |

Unclassified data is treated as **Confidential** by default.

---

## DA-POL-002: System of Record Designation [MANDATORY]

Every data domain must have a single designated System of Record (SoR). Architecture proposals that create a second authoritative source for an existing data domain must include a consolidation plan.

---

## DA-POL-003: Data Lineage Documentation

All Confidential and Restricted data flows must have documented lineage (source → transformations → consumers). Lineage must be maintained in LeanIX Data Objects and/or the data catalog.

---

## DA-POL-004: AI/ML Risk Assessment [MANDATORY for AI proposals]

All AI/ML systems must be classified under the EU AI Act risk framework before deployment:
- **Unacceptable risk** — Prohibited. No deployment.
- **High risk** — Mandatory human oversight, explainability, bias testing, audit trail, registration.
- **Limited risk** — Transparency obligations (users must know they interact with AI).
- **Minimal risk** — Standard development and monitoring.

High-risk AI systems require an AI Impact Assessment before Architecture endorsement.

---

## DA-POL-005: Training Data Provenance

AI/ML models must document the provenance of their training data: source, collection date, licensing, known biases, and consent status where personal data is involved. Models trained on undocumented or unlicensed data are not approved for production.

---

## DA-POL-006: Data Minimization

Systems must only collect and process personal data that is necessary for the stated purpose (GDPR Article 5). Architecture proposals that expand personal data collection require a Data Protection Impact Assessment (DPIA).

---

## DA-POL-007: Model Monitoring [MANDATORY for AI in production]

AI/ML models in production must have:
- Performance monitoring (accuracy/drift detection)
- Fairness monitoring (bias drift detection for high-risk systems)
- An automated or scheduled model review cycle
- A documented process for model retirement or replacement

---

## DA-POL-008: Data Retention and Deletion

All data stores must have documented retention policies. Personal data must be deletable in response to a data subject request (GDPR Article 17). Systems that cannot support deletion of personal data are not approved.
