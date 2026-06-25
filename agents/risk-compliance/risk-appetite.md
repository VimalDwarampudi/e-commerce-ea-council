# Organization Risk Appetite

## Purpose

This file defines the organization's risk appetite as it applies to architecture decisions. The Risk & Compliance agent uses this to calibrate risk ratings and escalation decisions.

> **Note:** This is a template. Update this file with the actual risk appetite statements from your organization's risk management framework.

---

## Overall Risk Stance

**Moderate risk tolerance** — the organization is willing to accept measured risks in pursuit of strategic objectives, but maintains a low tolerance for regulatory, reputational, and safety risks.

---

## Risk Appetite by Category

| Risk Category | Appetite | Rationale |
|---|---|---|
| **Regulatory & Compliance** | Very Low | Regulatory penalties and enforcement carry unacceptable business and reputational impact |
| **Data Privacy (GDPR)** | Very Low | Personal data breaches carry regulatory, legal, and reputational risk |
| **Information Security** | Low | Breaches damage customer trust and business continuity |
| **Operational Resilience** | Low | System outages in core processes are unacceptable beyond defined RTO/RPO |
| **Strategic / Business** | Moderate | Innovation and transformation require accepting some failure |
| **Technology Modernization** | Moderate-High | Accepting temporary operational risk to reduce long-term technical debt |
| **Vendor Dependency** | Moderate | Some strategic vendor relationships are accepted; concentration risk is monitored |
| **AI & Emerging Technology** | Moderate | Willing to explore but requires governance guardrails |

---

## Risk Rating Scale

| Rating | Description | Response |
|---|---|---|
| **CRITICAL** | Immediate threat to operations, regulatory standing, or safety | Stop. Escalate immediately. Do not proceed. |
| **HIGH** | Significant risk requiring active management | Require mitigations before approval; escalate if unmitigable |
| **MEDIUM** | Manageable risk with controls | Document, assign owner, review at ADR follow-up |
| **LOW** | Minimal risk, acceptable with normal controls | Note and monitor |

---

## Risk Calculation Matrix

```
           │  LOW Impact  │ MEDIUM Impact │ HIGH Impact
───────────┼──────────────┼───────────────┼─────────────
LOW Prob   │     LOW      │    MEDIUM     │    HIGH
MEDIUM Prob│    MEDIUM    │     HIGH      │    HIGH
HIGH Prob  │     HIGH     │     HIGH      │  CRITICAL
```

---

## Escalation Thresholds

- **CRITICAL** → Immediate escalation to CRO + Legal; Chief Architect pauses the ADR
- **HIGH** (regulatory) → Escalate to CRO
- **HIGH** (security) → Security agent to veto or require mitigation; escalate to CISO
- **MEDIUM** → Document and mitigate; no escalation required but Chief Architect must acknowledge
