# Deliberation Protocol — How the Council Runs a Session

## Overview

Every council session follows a structured six-phase process. The Chief Architect drives each phase. Agents do not freelance — they respond to structured prompts from the orchestrator.

---

## Phase 1: TRIAGE & DECOMPOSE

**Driver:** Chief Architect  
**Duration:** Single pass

**Steps:**
1. Read and interpret the incoming request
2. Identify the decision type: strategy / design / review / assessment / decision
3. Assign an impact level: Minor / Standard / Major / Critical (see `council-config.md`)
4. Decompose the request into domain-specific sub-questions
5. Select agents to engage using `routing-rules.md`
6. Pull relevant context from LeanIX and ServiceNow

**Output:**
```
TRIAGE RESULT
- Request summary: [one sentence]
- Decision type: [type]
- Impact level: [level]
- Sub-questions per domain:
  - Business Architecture: [question]
  - Application Architecture: [question]
  - [etc.]
- Agents engaged: [list]
- LeanIX data loaded: [list of relevant fact sheets / queries run]
- ServiceNow data loaded: [list of relevant records / queries run]
```

---

## Phase 2: PARALLEL DOMAIN ASSESSMENT

**Driver:** Chief Architect (issues prompts); Domain Agents (respond)  
**Pattern:** Parallel (all selected domain agents run simultaneously if the platform supports it, or sequentially)

**Prompt template for each domain agent:**
```
You are [Agent Name].

REQUEST: [full original request]

YOUR SPECIFIC QUESTION: [domain sub-question from triage]

RELEVANT DATA:
[LeanIX data relevant to this domain]
[ServiceNow data relevant to this domain]

Instructions:
1. Assess the current state relevant to your domain
2. Provide your domain recommendation
3. Identify risks from your domain perspective
4. Flag any dependencies on peer domains
5. Note anything that should be reviewed by Security or Risk & Compliance
6. Use the output format in your agent.md

Stay within your domain scope. Do not answer for other agents.
```

**Output per agent:** Domain Assessment following the format in each agent's `agent.md`

---

## Phase 3: CROSS-CUT REVIEW

**Driver:** Chief Architect; Security Agent + Risk & Compliance Agent respond  
**Condition:** Skip for Minor impact; mandatory for Standard and above

**Prompt template:**
```
You are [Security / Risk & Compliance Agent].

The following domain assessments have been produced for this request:
[Full outputs from Phase 2]

ORIGINAL REQUEST: [request]

Instructions:
1. Review all domain outputs through your governance lens
2. Identify any security / compliance / risk concerns they may have missed
3. Flag specific items that require remediation before approval
4. If any item meets veto criteria (Security) or escalation criteria (Risk), state it explicitly
5. Rate overall risk level: LOW / MEDIUM / HIGH / CRITICAL
```

---

## Phase 4: RED TEAM CHALLENGE

**Driver:** Chief Architect; Red Team Agent responds  
**Condition:** Mandatory for Critical impact; recommended for Major and novel proposals

**Prompt template:**
```
You are the Red Team Agent.

The following proposal has been developed by the EA Council:
[Combined domain assessments + cross-cut review]

Your job is NOT to endorse this proposal. Your job is to break it.

Instructions:
1. Identify the top 3–5 weaknesses or blind spots in this proposal
2. What assumptions is the council making that could be wrong?
3. What failure modes are not accounted for?
4. What does the adversary / regulator / auditor see that we don't?
5. Is there a simpler approach the council has overlooked?
6. Rate confidence in the proposal: LOW / MEDIUM / HIGH with rationale
```

---

## Phase 5: SYNTHESIS & REFINEMENT

**Driver:** Chief Architect  
**Duration:** Single pass (or two if Red Team surfaces major issues)

**Steps:**
1. List all points of consensus between domain agents
2. List all conflicts — resolve each using `shared/architecture-principles.md`
3. Address Security and Risk & Compliance findings:
   - Remediate where possible
   - Escalate to humans where not resolvable within scope
4. Address Red Team findings:
   - Accept, mitigate, or explicitly reject each — with rationale
5. Formulate the synthesized recommendation

**If a conflict cannot be resolved:**
- Document both positions, the principle that should govern it, and why it doesn't resolve cleanly
- Flag for human escalation per `escalation-matrix.md`

**Loop condition:** If Red Team or cross-cut agents surface findings that invalidate the core proposal, return to Phase 2 with a revised decomposition.

---

## Phase 6: DECISION & OUTPUT

**Driver:** Chief Architect  
**Output:** Architecture Decision Record (ADR) using `shared/standards/adr-template.md`

**Steps:**
1. Produce the ADR
2. List next actions with owners
3. Write back to LeanIX if the decision changes application lifecycle, tech radar position, or interface data
4. Write back to ServiceNow if the decision generates a change request or GRC record
5. Notify human sponsors if escalation is needed

**ADR must include:**
- Decision summary (one sentence)
- Context (what problem we're solving and why now)
- Decision (what we're doing)
- Rationale (why this option over alternatives)
- Trade-offs (what we're accepting)
- Agents consulted + any dissenting positions
- Risks and mitigations
- Next steps and owners

---

## Conflict Resolution Hierarchy

When two agents disagree, resolve in this order:

1. **Mandatory policies** — if one option violates a `[MANDATORY]` policy, it is eliminated
2. **Architecture principles** — apply `shared/architecture-principles.md` in order
3. **Evidence weight** — prefer the position with stronger LeanIX/ServiceNow data support
4. **Impact and reversibility** — prefer the more reversible option under uncertainty
5. **Escalate** — if still unresolved, escalate to human sponsors

---

## Session Types

| Type | Phases Used | Typical Duration |
|---|---|---|
| Quick Query | 1, 2 (1 agent), 6 (summary only) | Minutes |
| Standard Review | 1–3, 5–6 | 1 deliberation cycle |
| Full Council | 1–6 | Full deliberation cycle |
| Critical Decision | 1–6 + human review loop | Multiple cycles |
