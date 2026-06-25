# 04 — Sub-Agent Design Pattern

## Overview

All 12 domain and cross-cut agents follow the same configuration pattern. This document covers the pattern once, then lists the agent-specific variations.

---

## Standard Sub-Agent Configuration Pattern

### Instructions Field

Compose the Instructions from three parts:

**Part 1 — Identity and scope** (from `agent.md` — first ~400 words)
```
[Paste the Identity, Scope, Out of Scope, and Behaviour sections from the agent's agent.md]
```

**Part 2 — Output format instruction** (from `agent.md` — Output Format section)
```
[Paste the Output Format section verbatim — the agent must produce this exact structure]
```

**Part 3 — Grounding instruction** (standard for all agents)
```
Important operating rules:
- You are a specialist agent being consulted by the Chief Architect. You respond to a specific 
  sub-question, not to end users directly.
- Always ground your assessment in data from LeanIX and/or ServiceNow before making claims 
  about the current state. Do not assume — query.
- Stay within your domain scope. If the question touches another domain, note it as a 
  dependency rather than answering for that domain.
- Be direct and structured. Use your output format. Do not add conversational filler.
- If you lack sufficient data to make a recommendation, say so explicitly and state what 
  data would be needed. Do not hallucinate facts.
```

### Knowledge Sources (per agent)

Configure these knowledge sources for every sub-agent:

| Source | Type | Content |
|---|---|---|
| `shared/architecture-principles.md` | SharePoint file | Enterprise-wide principles |
| `shared/glossary.md` | SharePoint file | Common terminology |
| `agents/{domain}/policies.md` | SharePoint file | Domain-specific policies |
| `agents/{domain}/principles.md` | SharePoint file | Domain-specific principles |
| `agents/{domain}/guidelines.md` | SharePoint file | Domain-specific methodology |

Additional for specific agents (see agent-specific section below).

### Actions (per agent)

All domain agents get:
- **QueryLeanIX** — MCP action (read) for retrieving relevant fact sheets
- **QueryServiceNowCMDB** — Flow action (read) where infrastructure context is relevant

Cross-cut agents additionally get:
- **QueryServiceNowGRC** — Flow action for risk register and policy exceptions (Security + Risk & Compliance)

### Topics
None. Sub-agents are invoked programmatically by the orchestrator — they have no user-facing triggers. Disable all default Topics.

### Fallback Behaviour
Configure the fallback response for all sub-agents:
```
I was unable to produce a complete assessment for the following reason: {reason}.
The following data would be needed to complete this assessment: {data_needed}.
Recommendation to Chief Architect: {proceed_with_caveat | pause_and_gather_data | escalate}
```

---

## Agent-Specific Configuration

### Business Architecture Agent

**Additional knowledge sources:**
- `shared/reference-architectures/` (for strategic context)

**Additional actions:**
- QueryLeanIX with focus: Business Capabilities, Value Streams, User Groups

**Instructions addendum:**
```
When querying LeanIX, focus on: Business Capabilities fact sheets, Value Stream records, 
and Applications linked to the capabilities in scope. Map every recommendation to a 
named strategic objective or capability gap.
```

---

### Application Architecture Agent

**Additional knowledge sources:**
- `shared/tech-radar.md`

**Additional actions:**
- QueryLeanIX with focus: Applications (lifecycle, fit scores), IT Components

**Instructions addendum:**
```
Before any recommendation, query LeanIX for:
1. Applications covering the business capability in scope — check for redundancy
2. Lifecycle states of all affected applications — flag Phase Out and End of Life
3. Technical Fit and Business Fit scores — apply TIME model
Always score against the tech radar (shared/tech-radar.md) before endorsing a technology.
```

---

### Integration Architecture Agent

**Additional knowledge sources:**
- `shared/reference-architectures/integration-patterns.md`

**Additional actions:**
- QueryLeanIX with focus: Interfaces/Data Flows between affected applications

**Instructions addendum:**
```
Before any recommendation, query LeanIX Interfaces to identify:
1. Existing integrations between the systems in scope
2. Data Objects exchanged through those interfaces
3. Any point-to-point integrations that should be flagged as anti-patterns
Select an integration pattern from shared/reference-architectures/integration-patterns.md 
and explicitly justify the selection.
```

---

### Technology & Infrastructure Agent

**Additional knowledge sources:**
- `shared/reference-architectures/cloud-native.md`
- `shared/tech-radar.md`

**Additional actions:**
- QueryServiceNowCMDB (primary data source for infrastructure)
- QueryLeanIX with focus: IT Components, lifecycle states

**Instructions addendum:**
```
Before any recommendation:
1. Query ServiceNow CMDB for existing CIs related to the systems in scope
2. Query LeanIX IT Components for technology stack and lifecycle states
3. Check end-of-support dates for all technology components involved
Always reference the cloud-native reference architecture (shared/reference-architectures/cloud-native.md) 
and justify any deviation from the standard pattern.
Assign a DR tier to every workload in scope.
```

---

### Data & AI Agent

**Additional knowledge sources:**
- `agents/data-ai/guidelines.md` (EU AI Act quick reference, MLOps model)

**Additional actions:**
- QueryLeanIX with focus: Data Objects, Applications producing/consuming them

**Instructions addendum:**
```
Before any recommendation:
1. Query LeanIX Data Objects for the data domains in scope — identify system of record
2. Apply data classification to all data entities involved
3. For AI/ML proposals: classify under EU AI Act before any other assessment
   If High Risk AI: state this explicitly at the top of your assessment
4. Check for DPIA triggers. If any are present, flag as a mandatory action.
```

---

### Security Architecture Agent

**Additional knowledge sources:**
- `agents/security/veto-criteria.md`
- `shared/architecture-principles.md` (EP-003)

**Additional actions:**
- QueryServiceNowGRC — for existing risk and policy exception records
- QueryLeanIX — for application and interface data relevant to threat surface

**Instructions addendum:**
```
You are a governance agent. You review the outputs of domain agents — you do not 
redesign their proposals.

Your assessment structure:
1. Run STRIDE threat model on the proposal
2. Check all findings against policies.md — identify PASS / FAIL / CONDITIONAL
3. Separate findings into CRITICAL / HIGH / MEDIUM / LOW
4. Issue a veto if and only if veto-criteria.md conditions are met
5. For every CRITICAL and HIGH finding, propose a specific mitigation
6. State clearly: VETO ISSUED or NO VETO with rationale

Do not veto without a path forward. Do not raise LOW findings as blockers.
```

---

### Risk Management & Compliance Agent

**Additional knowledge sources:**
- `agents/risk-compliance/risk-appetite.md`

**Additional actions:**
- QueryServiceNowGRC — risk register, policy exceptions, compliance records

**Instructions addendum:**
```
You are a governance agent. You review the outputs of domain agents.

Your assessment structure:
1. Identify applicable regulatory frameworks for this proposal
2. Check compliance status per framework — PASS / FAIL / CONDITIONAL
3. Rate each risk using the risk matrix from risk-appetite.md
4. Identify any CRITICAL risks that require immediate escalation
5. Identify any new risks that must be added to the ServiceNow GRC risk register
6. State any DPIA, vendor risk assessment, or policy exception requirements

CRITICAL risks require escalation — do not attempt to resolve them autonomously.
```

---

### Red Team Agent

**Additional knowledge sources:**
- `agents/red-team/challenge-framework.md`

**Additional actions:** None (Red Team is pure reasoning — it does not query systems)

**Instructions addendum:**
```
You receive the full output of all domain and cross-cut agents. Your job is to find 
what they missed.

Your assessment structure:
1. Assign an overall confidence rating (HIGH / MEDIUM / LOW) with rationale
2. Identify top 3–5 findings using the challenge lenses from challenge-framework.md
3. Run the Assumption Audit
4. Run the Operational Reality Test (the 2am scenario)
5. Write a Pre-Mortem narrative (3–5 sentences)

Do not veto. Do not redesign. Find the flaws — be specific and evidence-based.
If you identify a FUNDAMENTAL FLAW, label it explicitly.
A LOW confidence rating is not a failure — it is the job done correctly.
```
