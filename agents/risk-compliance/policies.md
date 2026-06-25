# Risk Management & Compliance Policies

## RC-POL-001: Risk Register Update [MANDATORY]

Any architecture decision that introduces a new risk rated MEDIUM or above must result in a risk record being created or updated in the ServiceNow GRC risk register within 5 business days of the ADR being approved.

---

## RC-POL-002: DPIA Requirement [MANDATORY]

A Data Protection Impact Assessment (DPIA) is required before any of the following:
- Systematic processing of special categories of personal data (health, biometric, etc.)
- Large-scale processing of personal data
- Systematic monitoring of individuals (including employees)
- Processing using new technologies with high privacy risks
- AI systems that make decisions about individuals

DPIAs must be reviewed by the Data Protection Officer (DPO) before the architecture receives endorsement.

---

## RC-POL-003: Vendor Risk Assessment [MANDATORY for Confidential/Restricted data]

Any vendor or SaaS provider that processes Confidential or Restricted data must complete a vendor risk assessment before data is shared. Assessment criteria:
- Data processing agreement (DPA) in place
- Sub-processor disclosure
- Data residency location
- Breach notification process
- Security certifications (ISO 27001 or SOC 2 Type II preferred)

---

## RC-POL-004: Policy Exception Process

When a proposal requires an exception to a mandatory policy:
1. Document the exception request: policy being excepted, business justification, compensating controls, expiry date
2. Obtain approval from: Chief Risk Officer (for regulatory) or CISO (for security)
3. Record the approved exception in the ServiceNow GRC policy exception log
4. Review exceptions at expiry — they do not auto-renew

---

## RC-POL-005: Audit Trail for Regulated Processes

Any system that participates in a regulated process (financial reporting, payment processing, personal data processing, etc.) must maintain an immutable audit trail covering:
- Who performed an action
- What action was performed
- On what data/record
- When (timestamp, timezone-aware)
- From where (system, IP)

---

## RC-POL-006: Business Continuity Requirements

For Tier 1 and Tier 2 business processes (per DR tier classification), architecture proposals must demonstrate:
- Defined RTO and RPO targets met by the design
- Tested recovery procedures (at least annually)
- Documented fallback to manual process if applicable

---

## RC-POL-007: Retention and Deletion Alignment

Architecture must align with the organization's data retention schedule. Systems that cannot enforce automatic retention and deletion policies are not approved for Restricted data.

---

## RC-POL-008: Regulatory Change Monitoring

The Risk & Compliance agent maintains a regulatory radar. When new or amended regulations affect existing architecture, affected ADRs are flagged for review. Mandatory regulatory updates are treated as Critical impact decisions.
