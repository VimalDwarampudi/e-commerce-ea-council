# Risk Management & Compliance Guidelines

## Risk Assessment Methodology

### Step 1: Identify Risks

For every proposal, brainstorm risks across these categories:
- **Regulatory** — does it create exposure under GDPR, NIS2, DORA, SOX, etc.?
- **Operational** — could it disrupt business processes if it fails?
- **Vendor** — does it create a critical dependency on a third party?
- **Data** — does it create new personal data flows, storage, or processing?
- **Reputational** — if this goes wrong, would it be news?
- **Strategic** — does it lock us into something that conflicts with future strategy?
- **Financial** — does it create unbudgeted cost exposure?

### Step 2: Rate Each Risk

Use the Risk Matrix from `risk-appetite.md`:

```
Rating = f(Probability, Impact)
CRITICAL = HIGH × HIGH
HIGH     = HIGH × MEDIUM or MEDIUM × HIGH
MEDIUM   = MEDIUM × MEDIUM or HIGH × LOW or LOW × HIGH
LOW      = LOW × MEDIUM or MEDIUM × LOW or LOW × LOW
```

### Step 3: Define Controls and Residual Risk

For each risk, identify:
- **Preventive controls** — stop the risk from occurring
- **Detective controls** — detect it quickly when it does
- **Corrective controls** — recover from it when detected
- **Residual risk** — rating after controls are applied

### Step 4: Determine Action

| Residual Risk | Action |
|---|---|
| CRITICAL | Halt. Escalate to CRO/Legal. Do not proceed. |
| HIGH | Require mitigations in the ADR. Risk owner must accept explicitly. |
| MEDIUM | Document in risk register. Assign owner and review date. |
| LOW | Note in ADR. No escalation. |

## Regulatory Compliance Assessment Process

### GDPR Quick Assessment

Ask these questions for any proposal involving personal data:

1. **What personal data is processed?** (name, email, IP, location, health, biometric...)
2. **What is the legal basis for processing?** (consent, contract, legal obligation, legitimate interest, vital interest, public task)
3. **Where is data stored?** (EU/EEA region? Is a transfer mechanism needed for non-EEA?)
4. **Who has access?** (internal roles, third-party processors — is a DPA in place?)
5. **How long is data retained?** (retention schedule defined and enforced?)
6. **Can data subjects exercise rights?** (access, rectification, erasure, portability — are these technically possible?)
7. **Is a DPIA required?** (triggers: new technology, systematic processing, large scale, special categories)

### NIS2 Applicability Check

NIS2 applies if the organization is classified as an Essential or Important Entity. If NIS2 applies, check:
- [ ] Risk management measures documented and applied
- [ ] Incident reporting process: significant incidents to national authority within 24h (initial) / 72h (detailed)
- [ ] Supply chain security requirements applied to critical suppliers
- [ ] Business continuity measures in place and tested
- [ ] Encryption and access controls meeting NIS2 technical measures
- [ ] Senior management accountability documented

### DORA Applicability Check (Financial Sector)

If DORA applies:
- [ ] ICT risk management framework in place
- [ ] Incident classification and reporting process defined
- [ ] Digital operational resilience testing program (TLPT for significant firms)
- [ ] Third-party ICT provider risk management: contractual requirements, concentration risk assessment
- [ ] DORA-compliant contractual clauses in all critical ICT vendor contracts

## Vendor Risk Assessment Template

```
Vendor Risk Assessment: [Vendor Name]
Date: [Date]
Assessed by: [Risk & Compliance Agent / Human reviewer]

Data Classification handled: [Public / Internal / Confidential / Restricted]
Data types: [Personal data? Special categories? Financial?]
Data residency: [Country/region where data is stored and processed]

Certifications held:
- ISO 27001: YES / NO / In progress (expiry: )
- SOC 2 Type II: YES / NO (period: )
- Other: 

Contractual:
- Data Processing Agreement in place: YES / NO
- Sub-processor disclosure available: YES / NO
- Breach notification SLA: [hours] hours
- Audit rights clause: YES / NO
- Data deletion on termination: YES / NO

Security posture:
- Penetration test (last 12 months): YES / NO
- Bug bounty / responsible disclosure: YES / NO
- Encryption in transit: YES / NO
- Encryption at rest: YES / NO

Risk Rating: LOW / MEDIUM / HIGH / CRITICAL
Recommendation: APPROVE / APPROVE WITH CONDITIONS / REJECT

Conditions (if applicable):
[List required conditions before approval]
```

## Policy Exception Request Template

```
Policy Exception Request

Policy: [Policy ID and name — e.g., SEC-POL-001: Authentication Required for All APIs]
Exception Requested By: [Team/project]
Date: [Date]
Expiry: [Date — maximum 12 months; shorter if possible]

Business Justification:
[Why the exception is needed — specific, not generic]

Risk Assessment:
[What risk is created by this exception?]
[Risk rating without compensating controls: ]
[Risk rating with compensating controls: ]

Compensating Controls:
[What alternative controls are in place to mitigate the risk created by the exception]

Approval Required From: [CISO / CRO / EA Lead — per escalation matrix]
Approved By: [Name, role, date]

Exception ID: [Assigned by Risk & Compliance on approval]
Review Date: [Must be reviewed before expiry]
```
