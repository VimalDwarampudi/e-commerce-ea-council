# Deliberation Protocol — How the Retail Council Runs a Session

## Overview

Every council session follows a structured six-phase process. The Chief Architect drives each phase.
Agents do not freelance — they respond to structured prompts from the orchestrator, and ground every
response in the OKF knowledge bundle per `SKILL.md`.

---

## Phase 1: TRIAGE & DECOMPOSE

**Driver:** Chief Architect

**Steps:**
1. Read and interpret the incoming request.
2. Identify decision type: strategy / design / review / assessment / decision.
3. Assign an impact level (see `council-config.md`, including the retail-specific impact signals).
4. Decompose into domain-specific sub-questions.
5. Select agents to engage using `routing-rules.md`.
6. Read `knowledge/index.md` and `knowledge/shared/index.md` per `SKILL.md` to orient before dispatching.

**Output:**
```
TRIAGE RESULT
- Request summary: [one sentence]
- Decision type: [type]
- Impact level: [Minor / Standard / Major / Critical]
- Sub-questions per domain: [list]
- Agents engaged: [list]
- Rationale for scope: [why these agents, why not others]
```

---

## Phase 2: PARALLEL DOMAIN ASSESSMENT

**Driver:** Chief Architect (issues Task calls); Domain Agents (respond independently)

Prompt template per domain agent:
```
REQUEST: [full original request]
YOUR SPECIFIC QUESTION: [domain sub-question from triage]
RELEVANT OPERATIONAL DATA: [any live data supplied by the user, or "none — flag assumptions"]

Follow your Grounding Protocol and SKILL.md. Assess current state, give your domain recommendation,
identify domain-specific risks, flag dependencies on peer domains, and note anything Security or
Risk & Compliance should review. Cite the specific concept files backing each claim.
```

Never pre-answer before consulting agents. Do not let agents see each other's output at this stage.

---

## Phase 3: CROSS-CUT REVIEW

**Driver:** Chief Architect; Security + Risk & Compliance respond
**Condition:** Skip for Minor impact; mandatory for Standard and above; mandatory for anything touching
cardholder data or PCI scope regardless of stated impact level.

Cross-cut agents review the combined Phase 2 output (the proposal), not the raw original request.

---

## Phase 4: RED TEAM CHALLENGE

**Driver:** Chief Architect; Red Team responds
**Condition:** Mandatory for Critical impact; recommended for Major and for novel/first-of-its-kind
proposals (e.g. a capability with no existing reference architecture in `knowledge/shared/reference-architectures/`).

Red Team's job is explicitly to break the proposal, not endorse it — see
`knowledge/red-team/index.md` for its principles and retail-specific challenge lenses.

---

## Phase 5: SYNTHESIS & REFINEMENT

**Driver:** Chief Architect alone (no further Task calls, unless looping back)

1. List points of consensus across agents.
2. List conflicts and resolve each using the **Conflict Resolution Hierarchy** below.
3. Address Security/Risk findings: remediate where possible, escalate where not.
4. Address Red Team findings: accept, mitigate, or explicitly reject each, with rationale.
5. Formulate the synthesized recommendation.

**Conflict Resolution Hierarchy** (apply in order):
1. **Mandatory policies** — a policy with `mandatory: true` eliminates an option outright.
2. **Enterprise principles** — apply `knowledge/shared/index.md` principles in order.
3. **Evidence weight** — prefer the position with stronger data/telemetry support.
4. **Reversibility** — prefer the more reversible option under uncertainty.
5. **Escalate** — if still unresolved, escalate to human sponsors per `escalation-matrix.md`.

**Loop condition:** if Red Team or cross-cut review invalidates the core proposal, return to Phase 2 with a
revised decomposition.

---

## Phase 6: DECISION & OUTPUT

**Driver:** Chief Architect
**Output:** ADR using `knowledge/shared/standards/adr-template.md`, appended to `outputs/adr-register.md`.

**ADR must include:** decision summary, context, decision, rationale, trade-offs, agents consulted + any
dissent, risks and mitigations, next steps and owners, and the specific concept files (policies,
principles, reference architectures) the decision traces to.

If the decision would normally write back to an operational system (OMS, PIM, inventory), state that this
is a manual follow-up step — see `CLAUDE.md` "Data Sources."

---

## Session Types

| Type | Phases Used | Typical Use |
|---|---|---|
| Quick Query | 1, 2 (1 agent), 6 (summary only) | Minor impact |
| Standard Review | 1–3, 5–6 | Standard impact |
| Full Council | 1–6 | Major impact |
| Critical Decision | 1–6 + human review loop | Critical impact |
