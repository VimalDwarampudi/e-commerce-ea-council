# Escalation Matrix

## Purpose

Defines when and how the Chief Architect escalates beyond the AI council to human sponsors. Escalation is
not failure — it is the correct response to decisions that exceed the council's authority or confidence.

## Escalation Triggers

| Trigger | Condition | Action |
|---|---|---|
| **Security veto — unresolvable** | Security issues a veto that cannot be remediated within the proposal scope | Pause decision. Escalate to CISO / Security Sponsor |
| **Critical compliance risk** | Risk & Compliance rates a risk CRITICAL (e.g. cross-border transfer with no adequate safeguard) | Pause decision. Escalate to Chief Risk Officer / Legal |
| **PCI scope expansion undecided** | A proposal would expand PCI-DSS audit scope and no budget/timeline has been pre-approved for the resulting assessment | Escalate to CISO + CFO before proceeding |
| **Peak-season timeline conflict** | A Major/Critical decision's remediation work cannot realistically complete before the next peak season (Black Friday/Cyber Monday) | Escalate to CTO + Business Strategy sponsor — the choice is delay launch vs. accept risk, and that's a business call |
| **Agent deadlock** | Two or more agents in irreconcilable conflict after synthesis | Present both positions to human sponsors with recommendation |
| **Outside principle coverage** | Request covers a scenario with no applicable principle in `knowledge/shared/` or the relevant domain | Escalate to EA Board to establish a new principle, add it to the bundle afterward |
| **Red Team: confidence LOW** | Red Team rates confidence in the proposal LOW | Require additional analysis or escalate for human review |
| **Regulatory uncertainty** | Compliance situation is ambiguous (new regulation, unclear applicability across jurisdictions) | Escalate to Legal/Compliance |
| **Novel pattern** | Proposed architecture has no precedent and no matching `ReferenceArchitecture` concept in the bundle | Escalate with a proof-of-concept proposal rather than a full decision |
| **Budget/resource impact** | Recommendation has material cost implications not pre-approved | Escalate to CTO / CFO |
| **Vendor lock-in > 3 years** | Proposal creates dependency on a single vendor (e.g. single PSP with no failover) for more than 3 years | Escalate to CTO |

## Escalation Format

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

Relevant Bundle Content:
[Specific concept files — policies, principles, reference architectures — relevant to the decision]

Requested Response:
[What the council needs back — a decision, more information, a new principle to add to the bundle]
```

## Escalation Routing

| Escalation Type | Escalate To |
|---|---|
| Security veto | CISO + EA Lead |
| Compliance / regulatory | Chief Risk Officer + Legal |
| PCI scope expansion | CISO + CFO |
| Peak-season timeline | CTO + Business Strategy sponsor |
| Strategic direction | CTO + EA Board |
| Budget / commercial | CTO + CFO |
| Novel principle needed | EA Board |
| Vendor strategy | CTO |

## Post-Escalation

Once humans provide a decision:
1. Chief Architect documents the human decision in the ADR.
2. If a new principle was established, add it as a new `Principle` concept file in the appropriate
   `knowledge/<domain>/` folder (or `knowledge/shared/` if enterprise-wide), and update that folder's
   `index.md`.
3. If a policy exception was granted, document it in the relevant domain's policy concept file with an
   expiry date in its frontmatter.
4. Append an entry to `knowledge/log.md` recording the bundle change.
5. Resume the deliberation process with the resolved constraint.
