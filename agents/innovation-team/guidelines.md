# Red Team Guidelines

## How to Conduct a Red Team Review

### Preparation

Before engaging, read the full council output (all domain + cross-cut assessments) in one pass. Do not start writing findings while reading — form an overall impression first. Then ask:

- What is this proposal trying to achieve, fundamentally?
- What must be true for it to succeed?
- What is the single most dangerous assumption in this proposal?

### Finding Classification

| Severity | Meaning | Chief Architect Response Required |
|---|---|---|
| **CRITICAL** | Invalidates the proposal or creates unacceptable risk that wasn't caught | Mandatory response; may trigger return to Phase 2 |
| **HIGH** | Significant weakness that should be addressed before approval | Required response with mitigation or explicit acceptance |
| **MEDIUM** | Real risk; manageable with targeted remediation | Recommended response; document in ADR |
| **LOW** | Marginal concern; worth noting but not blocking | Optional response; note in ADR |
| **FUNDAMENTAL FLAW** | Core premise of the proposal is wrong | Chief Architect must pause deliberation and re-scope |

### The Assumption Audit — Step by Step

1. Read the proposal and extract every assumption, stated or implied
2. For each assumption, ask: *how was this validated?*
3. Classify each assumption:
   - **VALIDATED** — there is explicit evidence (data, test, precedent)
   - **UNVALIDATED** — it's stated as true but without evidence
   - **QUESTIONABLE** — there's reason to believe it may be false
4. For UNVALIDATED and QUESTIONABLE assumptions, assess the consequence if they're wrong:
   - If the proposal still works → LOW risk
   - If the proposal needs modification → MEDIUM or HIGH risk
   - If the proposal collapses → CRITICAL / FUNDAMENTAL FLAW

### Historical Failure Pattern Library

Use these known failure patterns as lenses when reviewing proposals:

| Pattern | Description | Red Team Question |
|---|---|---|
| **Integration sprawl** | Too many point-to-point integrations create invisible dependencies | What breaks if System X is unavailable for 4 hours? |
| **The God Application** | One application accumulates too many responsibilities | What is the blast radius if this application fails? |
| **Security bolted on** | Security added after design, not designed in | Where was the security design? Or was it a checklist? |
| **Vendor lock-in creep** | Proprietary features adopted gradually until exit is impossible | What does it cost and how long does it take to exit this vendor in 3 years? |
| **The optimistic SLA** | RTO/RPO targets stated without a tested recovery design | Has the recovery procedure been tested? Who wrote the runbook? |
| **Undocumented data flows** | Real data flows differ from documented ones | What data flows exist that aren't in LeanIX? Who would know? |
| **Champion-driven adoption** | Technology chosen because one senior person likes it | What happens to this technology when that person leaves? |
| **Complexity debt** | Architecture adds layers to solve problems that shouldn't exist | What problem would disappear if we simplified instead? |
| **False consensus** | All agents agree because none challenged the framing | Is everyone agreeing with the proposal, or with the person who asked? |
| **Big Bang delivery** | Large-scope change with a single go-live | What is the rollback plan? What triggers rollback? |

### Operational Reality Test

For every proposal, mentally simulate this scenario:

> It is 2:15 AM on a Sunday. A critical incident is in progress. The on-call engineer has never worked with this system before. The senior architect is on vacation. The runbook is incomplete.

Ask:
- What breaks first and how obvious is it?
- What does the on-call engineer do that makes it worse?
- Where is the runbook, and does it cover this scenario?
- How long before customers or the business feels it?
- What would have prevented this at design time?

If the answer to any of these questions is "we don't know" — that is a finding.

## Confidence Rating Guidance

At the end of a Red Team review, assign a confidence rating to the overall proposal:

| Rating | Description |
|---|---|
| **HIGH** | The council has addressed the key risks; the proposal is robust; Red Team found only LOW/MEDIUM issues |
| **MEDIUM** | Meaningful risks remain; the proposal can proceed with conditions; HIGH findings require response |
| **LOW** | Fundamental weaknesses or CRITICAL findings; the proposal should not proceed without significant rework |

**Be honest.** A LOW confidence rating is not a failure of the council — it is the Red Team doing its job.
