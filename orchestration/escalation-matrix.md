# Escalation Matrix

## Purpose

Defines when and how the Chief Architect escalates beyond the AI council to human sponsors. Escalation is not failure — it is the correct response to decisions that exceed the council's authority or confidence.

## Escalation Triggers

| Trigger | Condition | Action |
|---|---|---|
| **Security veto — unresolvable** | Security agent issues a veto that cannot be remediated within the proposal scope | Pause decision. Escalate to CISO / Security Sponsor with full context |
| **Critical compliance risk** | Risk & Compliance rates a risk as CRITICAL | Pause decision. Escalate to Chief Risk Officer / Legal |
| **Agent deadlock** | Two or more agents in irreconcilable conflict after synthesis round | Present both positions to human sponsors with recommendation |
| **Outside principle coverage** | Request covers a scenario with no applicable architecture principle | Escalate to EA Board to establish a new principle |
| **Red Team: confidence LOW** | Red Team rates confidence in the proposal as LOW | Require additional analysis or escalate for human review |
| **Regulatory uncertainty** | Compliance situation is ambiguous (new regulation, unclear applicability) | Escalate to Legal/Compliance team |
| **Novel pattern** | Proposed architecture has no precedent in the organization | Escalate with a proof-of-concept proposal rather than a full decision |
| **Budget/resource impact** | Recommendation has material cost implications not pre-approved | Escalate to CTO / CFO |
| **Vendor lock-in > 3 years** | Proposal creates dependency on a single vendor for more than 3 years | Escalate to CTO for strategic approval |

## Escalation Format

When escalating, produce the following:

```
ESCALATION NOTICE

Date: [date]
Request: [original request summary]
Impact Level: [level]
Escalation Trigger: [trigger from matrix above]

Council Position:
[Summary of what the council has agreed on]

Point of Escalation:
[Specifically what the humans need to decide — one clear question]

Options Considered:
A. [Option A] — [pros/cons]
B. [Option B] — [pros/cons]

Recommendation (if council has a preference):
[Preferred option and why — or "no consensus" if genuine deadlock]

Agents with Dissenting Views:
[Agent name]: [their position]

Data Available:
[Key LeanIX / ServiceNow data relevant to the decision]

Requested Response:
[What the council needs back — a decision, more information, a new principle]
```

## Escalation Routing

| Escalation Type | Escalate To |
|---|---|
| Security veto | CISO + EA Lead |
| Compliance / regulatory | Chief Risk Officer + Legal |
| Strategic direction | CTO + EA Board |
| Budget / commercial | CTO + CFO |
| Novel principle needed | EA Board |
| Vendor strategy | CTO |

## Post-Escalation

Once humans provide a decision:
1. Chief Architect documents the human decision in the ADR
2. If a new principle was established, add it to `shared/architecture-principles.md`
3. If a policy exception was granted, document it in the relevant agent's `policies.md` with expiry date
4. Resume the deliberation process with the resolved constraint
