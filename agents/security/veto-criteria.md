# Security Veto Criteria

## When a Veto MAY Be Issued

A security veto is a serious action. It halts a proposal until the condition is remediated or escalated to human sponsors. Use it when the risk is real, not as a bureaucratic gate.

### Veto Condition 1: Mandatory Policy Violation

A proposal explicitly violates a policy marked `[MANDATORY]` in `policies.md` and no mitigation within the proposal's scope can address it.

**Example:** A proposal to expose an internal API to the internet without authentication.

---

### Veto Condition 2: Unacceptable Residual Risk

After applying all available mitigations, a threat scenario remains at HIGH probability AND HIGH impact. The residual risk exceeds the organization's stated risk appetite.

**Assessment:**

| Probability | Impact | Result |
|---|---|---|
| HIGH | HIGH | **VETO eligible** — escalate if no mitigation available |
| HIGH | MEDIUM | HIGH finding — require mitigation, no automatic veto |
| MEDIUM | HIGH | HIGH finding — require mitigation, no automatic veto |
| LOW | HIGH | MEDIUM finding — recommend mitigation |

---

### Veto Condition 3: Unauthorized Restricted Data Exposure

A proposal routes Restricted data (PII, health, financial, legal) to a destination that:
- Is not authenticated and authorized
- Is outside the approved data residency zone
- Is a third-party system that has not completed security assessment

---

### Veto Condition 4: AI System Without Human Oversight in High-Stakes Context

A High-risk AI system (under EU AI Act classification) is proposed for production without:
- A human review mechanism in the decision loop
- An audit trail of AI decisions
- A defined process for challenging AI outputs

---

## Veto Format

```
⛔ SECURITY VETO ISSUED

Condition: [Veto condition number and description]
Policy Reference: [Specific policy — e.g., SEC-POL-003]
Threat Scenario: [What the risk is]
Residual Risk: [Why mitigation is insufficient or unavailable]

To lift this veto:
1. [Specific action required]
2. [Specific action required]

Alternative path (if available):
[Description of a modified proposal that would not trigger the veto]
```

## What a Veto Is NOT

- A veto is not a "we need more information" request — that is a conditional approval with requirements
- A veto is not a preference for a different technology — that is a HIGH finding
- A veto is not a compliance objection without a security risk — defer to Risk & Compliance for pure regulatory issues
