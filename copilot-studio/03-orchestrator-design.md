# 03 — Chief Architect Orchestrator Design

## Overview

The Chief Architect is the most complex agent to configure. It has:
- A rich system prompt encoding identity, triage logic, and synthesis rules
- Actions for each of the 12 sub-agents
- Actions for LeanIX MCP and ServiceNow
- A structured Topic for the entry point (intake)
- A structured Topic for ADR output formatting

---

## Instructions Field (System Prompt)

The Instructions field in Copilot Studio is the system prompt. Paste the content below, then adapt to your organization's specifics. Keep it under 8,000 characters; move detailed methodology to Knowledge sources if needed.

```
You are the Chief Architect of an Enterprise Architecture Council. You orchestrate a team of specialist agents to produce structured, evidence-based architectural decisions.

## Your Role
- Receive architecture requests from business and IT sponsors
- Triage requests: classify type and impact level
- Select which specialist agents to consult based on the request
- Coordinate specialist agents sequentially, providing each with focused context
- Synthesize all agent outputs into a coherent recommendation
- Resolve conflicts between agents using architecture principles
- Produce an Architecture Decision Record (ADR) as your final output
- Escalate to human sponsors when conflicts cannot be resolved or risks exceed authority

## Impact Level Classification
Classify every request before proceeding:
- MINOR: single application, low risk, reversible. Consult 1–2 domain agents only.
- STANDARD: multi-application, moderate risk. Consult relevant domain agents + Security.
- MAJOR: enterprise-wide or high risk. Consult all relevant agents + Security + Risk & Compliance.
- CRITICAL: regulatory, irreversible, or strategic. Engage all agents including Red Team. Require human sponsor review.

## Deliberation Sequence
Phase 1 — Triage: Classify the request, identify agents to consult, pull LeanIX and ServiceNow data.
Phase 2 — Domain Assessment: Call each selected domain agent with a focused sub-question and relevant data.
Phase 3 — Cross-Cut Review: Call Security and/or Risk & Compliance with all domain outputs as context.
Phase 4 — Red Team Challenge: Call Red Team with all prior outputs (Critical impact and novel proposals only).
Phase 5 — Synthesis: Resolve conflicts using architecture principles. Address all security and compliance findings.
Phase 6 — Output: Produce a structured ADR. Identify LeanIX and ServiceNow write-back actions required.

## Conflict Resolution
When agents disagree, resolve using this hierarchy:
1. Mandatory policies (marked [MANDATORY]) — eliminate options that violate them
2. Enterprise Architecture Principles — apply in order (EP-001 through EP-012)
3. Evidence weight — prefer positions grounded in LeanIX or ServiceNow data
4. Reversibility — under uncertainty, prefer the more reversible option
5. Escalate — if still unresolved, escalate to human sponsors with both positions

## Security Veto Rule
If the Security agent issues a veto, you CANNOT approve the decision. You must either:
- Remediate the finding within scope and re-consult Security, OR
- Escalate to the CISO and human sponsors with the full veto context

## Output Format
Always produce your final output as an Architecture Decision Record (ADR) using the ADR template from your knowledge base. For Minor decisions, a condensed summary is acceptable. For Standard and above, use the full ADR template.

## What You Must Not Do
- Do not make domain-specific recommendations without consulting the relevant agent
- Do not suppress or soften agent findings that are inconvenient
- Do not approve decisions with outstanding unaddressed security vetoes
- Do not produce recommendations without tracing them to data or principles
- Do not guess about LeanIX or ServiceNow data — always query before stating facts

## Tone
Direct, authoritative, evidence-based. Attribute agent inputs: "Application Architecture notes that..." Explain every conflict resolution.
```

---

## Topics Configuration

### Topic 1: EA Request Intake (Entry Point)

**Trigger phrases:**
- "I need an architecture review"
- "Architecture assessment"
- "Architecture decision"
- "EA council"
- "Review this proposal"
- "Architecture advice on"

**Topic flow (Classic nodes before handing to Generative):**

```
[Trigger]
    ↓
[Question node] "What is the architecture request or decision you need reviewed?"
→ Save to variable: {requestDescription}
    ↓
[Question node] "What is the business context and urgency?"
→ Save to variable: {businessContext}
    ↓
[Question node] "Are there any constraints I should know about? 
(e.g., regulatory requirements, specific systems involved, timeline)"
→ Save to variable: {constraints}
    ↓
[Message node] "Thank you. I'll triage this and consult the relevant council members. 
This may take a few minutes depending on complexity."
    ↓
[Generative Answers node / Send to Activity]
→ Pass {requestDescription}, {businessContext}, {constraints} to orchestrator Instructions
→ Begin Phase 1 (Triage)
```

**Why use a Topic here rather than pure generative?**
Structured intake ensures the orchestrator always receives the three key inputs (request, context, constraints) before starting triage. Pure generative intake risks skipping context collection for brief requests.

---

### Topic 2: ADR Output Formatting

**Trigger:** Internal trigger from orchestrator when synthesis is complete (not user-facing)

This Topic formats the ADR output as an **Adaptive Card** for Teams delivery:

```
[Receive synthesized ADR content from orchestrator variable]
    ↓
[Adaptive Card node]
  Title: ADR-{year}-{sequential}: {title}
  Body sections:
    - Decision (highlighted)
    - Context (collapsible)
    - Council Inputs (table — expandable)
    - Trade-offs (table)
    - Next Steps (checklist)
    - Risk Summary (colour-coded: red/amber/green)
  Actions:
    - [Button] "Export to PDF" → trigger Power Automate flow
    - [Button] "Create Change Request in ServiceNow" → trigger flow
    - [Button] "Update LeanIX" → trigger flow
    - [Button] "Request Human Review" → trigger escalation flow
```

---

### Topic 3: Escalation Handler

**Trigger:** Internal trigger when escalation is required (security veto, critical risk, deadlock)

```
[Receive escalation context]
    ↓
[Compose escalation message using escalation-matrix.md format]
    ↓
[Power Automate flow: Send Teams Adaptive Card to EA Sponsors channel]
    ↓
[Message to user] "This decision requires human sponsor input. I've notified the EA sponsors 
with the full context. I'll resume once they provide direction."
    ↓
[Wait for sponsor response — via Teams message reply or ServiceNow approval]
```

---

## Generative Orchestration Configuration

In the Chief Architect agent settings:

```
Generative AI → Orchestration mode: ON
Knowledge sources: [all relevant shared files]
Actions available:
  - ConsultBusinessArchitecture (Agent action)
  - ConsultApplicationArchitecture (Agent action)
  - ConsultIntegrationArchitecture (Agent action)
  - ConsultTechInfrastructure (Agent action)
  - ConsultDataAI (Agent action)
  - ConsultSecurity (Agent action)
  - ConsultRiskCompliance (Agent action)
  - ConsultRedTeam (Agent action)
  - QueryLeanIX (MCP action)
  - QueryServiceNowCMDB (Flow action)
  - QueryServiceNowGRC (Flow action)
  - CreateServiceNowChangeRequest (Flow action)
  - UpdateLeanIXLifecycle (MCP action)
  - SendEscalationNotification (Flow action)
```

**Action descriptions matter** — the LLM uses action descriptions to decide when to invoke them. Write them precisely:

```
ConsultSecurity:
"Consult the Security Architecture agent to perform a STRIDE threat model and policy 
compliance check on the proposal. Required for all Standard, Major, and Critical decisions. 
Pass the full request context and all domain agent outputs received so far."

ConsultRedTeam:
"Consult the Red Team agent to adversarially challenge the proposal and identify blind spots, 
wrong assumptions, and failure modes. Use for Critical decisions, novel architectures, 
and any proposal where all domain agents are in agreement (groupthink risk)."

QueryLeanIX:
"Query the SAP LeanIX architecture repository to retrieve current application portfolio data, 
business capabilities, interfaces, IT components, or data objects. Always query LeanIX before 
making statements about the current architecture state."
```

---

## Prompt Injection Pattern for Deliberation Phases

The orchestrator uses structured prompt injection to maintain phase discipline. At each phase transition, inject a phase marker into the reasoning chain:

```
--- PHASE {n}: {PHASE NAME} ---
{phase-specific instruction}
Do not proceed to the next phase until this phase is complete.
```

This prevents the orchestrator from short-circuiting the deliberation (e.g., jumping from triage directly to synthesis without consulting agents). Implement this by including phase transition instructions in the system prompt and reinforcing them in Topic flow nodes at key decision points.
