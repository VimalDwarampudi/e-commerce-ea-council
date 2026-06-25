# Output Formats — EA Council Deliverables

## Purpose

Defines how the Chief Architect and domain agents format their outputs for different audiences and surfaces. Consistent formatting makes outputs actionable, comparable, and archivable.

---

## Format 1: Quick Recommendation (Minor impact)

**When:** Minor decisions; single-agent consultations; quick advisory.  
**Length:** 200–400 words.  
**Audience:** Requestor (architect, developer, team lead).

```markdown
## Quick Architecture Recommendation

**Request:** {one-sentence summary}
**Impact Level:** Minor
**Date:** {date}

### Recommendation
{Clear action in one or two sentences}

### Rationale
{2–3 bullet points grounding the recommendation in principles or data}
- [Principle/policy reference if applicable]
- [LeanIX/ServiceNow data point if applicable]

### Conditions / Watch-outs
{Any conditions or risks the requestor should be aware of — optional if none}

### Next Steps
- {Action 1} — Owner: {role}
- {Action 2} — Owner: {role}

*Agents consulted: {list}*
```

---

## Format 2: Architecture Decision Record (Standard / Major / Critical)

**When:** All Standard, Major, and Critical decisions.  
**Template:** See `shared/standards/adr-template.md` — use it verbatim.  
**Length:** Full ADR — typically 500–1,500 words depending on complexity.  
**Audience:** EA team, business sponsors, technical teams, future architects (archival).  
**Storage:** `/outputs/adr/ADR-{YYYY}-{NNN}-{title}.md` + entry in `outputs/adr-register.md`.

---

## Format 3: Domain Assessment (Sub-agent output to Chief Architect)

**When:** Each domain agent's output during deliberation phases 2–4.  
**Length:** 200–500 words (summary mode) or 500–1,000 words (detailed mode).  
**Audience:** Chief Architect (internal; not shown to end users directly).

Each domain agent uses the output format defined in their own `agent.md`. This is the canonical format and must be followed exactly for synthesis to work reliably.

---

## Format 4: Escalation Notice

**When:** Triggered by security veto, critical compliance risk, or agent deadlock.  
**Audience:** Human sponsors (CISO, CRO, CTO, EA Board).  
**Delivery:** Teams Adaptive Card + email via Power Automate.

```markdown
## ⚠️ EA Council Escalation Notice

**Date:** {date}
**Request:** {original request summary}
**Escalation Trigger:** {trigger — e.g., "Security veto: SEC-POL-001 violation"}
**Urgency:** {CRITICAL / HIGH}

---

### What the Council Has Agreed
{Summary of council consensus — what's not in dispute}

### The Decision Required from You
> {Single clear question the human sponsor must answer}

### Options
**Option A:** {description}
- Pros: {list}
- Cons: {list}

**Option B:** {description}
- Pros: {list}
- Cons: {list}

### Council Recommendation (if consensus exists)
{Preferred option and why — or "No consensus" if genuine deadlock}

### Supporting Data
- LeanIX: {key data points}
- ServiceNow: {relevant records}
- Agent raising escalation: {agent name + summary of concern}

### What We Need Back
{Specific response required — decision, more information, or new principle}

*EA Council | {date} | ADR Reference: {ADR-in-progress ID}*
```

---

## Format 5: Technology Radar Update Summary

**When:** Quarterly tech radar review produces changes.  
**Audience:** All architects, developers, IT leadership.

```markdown
## Technology Radar Update — {Quarter} {Year}

### Changes This Quarter

**Moved to ADOPT:**
| Technology | Previous Ring | Rationale |
|---|---|---|
| {tech} | TRIAL | {brief reason} |

**Moved to TRIAL:**
| Technology | Previous Ring | Rationale |
|---|---|---|

**Moved to HOLD:**
| Technology | Previous Ring | Rationale |
|---|---|---|

**Retired from Radar:**
| Technology | Last Ring | Note |
|---|---|---|

### Key Messages for Teams
- {Message 1 — what teams need to act on}
- {Message 2}

### Impact on Existing Systems
{Any existing systems affected by HOLD decisions — migration timelines}

*Approved by: Chief Architect | Next review: {quarter}*
```

---

## Format 6: Red Team Summary (standalone)

**When:** Red Team findings are surfaced to sponsors for a Critical decision.  
**Audience:** Human sponsors who need to understand adversarial findings.

```markdown
## Red Team Review Summary

**Decision Under Review:** {ADR title}
**Date:** {date}
**Confidence Rating:** {LOW / MEDIUM / HIGH}

---

### Why This Rating
{1–2 sentences explaining the confidence rating}

### Top Findings

| # | Finding | Severity | Type | Status |
|---|---|---|---|---|
| 1 | {title} | CRITICAL/HIGH/MEDIUM | {type} | ADDRESSED / OPEN |
| 2 | {title} | | | |

### Pre-Mortem
*If this decision fails in 18 months, here's what happened:*
{3–5 sentence narrative}

### What Was Addressed
{How the Chief Architect responded to key findings}

### What Remains Open
{Any findings not addressed and why — or "All findings addressed"}
```

---

## Teams Adaptive Card Structure (ADR output)

The Chief Architect delivers ADRs to Microsoft Teams as Adaptive Cards. Structure:

```json
{
  "type": "AdaptiveCard",
  "version": "1.5",
  "body": [
    {
      "type": "TextBlock",
      "text": "ADR-{YYYY}-{NNN}: {Title}",
      "size": "Large",
      "weight": "Bolder"
    },
    {
      "type": "FactSet",
      "facts": [
        { "title": "Status", "value": "PROPOSED" },
        { "title": "Impact", "value": "{level}" },
        { "title": "Date", "value": "{date}" },
        { "title": "Agents Consulted", "value": "{list}" }
      ]
    },
    {
      "type": "TextBlock",
      "text": "**Decision**",
      "weight": "Bolder"
    },
    {
      "type": "TextBlock",
      "text": "{decision statement}",
      "wrap": true
    },
    {
      "type": "TextBlock",
      "text": "**Risk Summary**",
      "weight": "Bolder"
    },
    {
      "type": "ColumnSet",
      "columns": [
        { "type": "Column", "width": "stretch",
          "items": [{ "type": "TextBlock", "text": "🔴 Critical: {n}", "wrap": true }] },
        { "type": "Column", "width": "stretch",
          "items": [{ "type": "TextBlock", "text": "🟠 High: {n}", "wrap": true }] },
        { "type": "Column", "width": "stretch",
          "items": [{ "type": "TextBlock", "text": "🟡 Medium: {n}", "wrap": true }] }
      ]
    }
  ],
  "actions": [
    { "type": "Action.Submit", "title": "✅ Accept ADR",
      "data": { "action": "accept_adr", "adrId": "{id}" } },
    { "type": "Action.Submit", "title": "📋 View Full ADR",
      "data": { "action": "view_adr", "adrId": "{id}" } },
    { "type": "Action.Submit", "title": "🔄 Update LeanIX",
      "data": { "action": "writeback_leanix", "adrId": "{id}" } },
    { "type": "Action.Submit", "title": "🎫 Create ServiceNow CHG",
      "data": { "action": "create_change", "adrId": "{id}" } },
    { "type": "Action.Submit", "title": "⚠️ Escalate to Sponsors",
      "data": { "action": "escalate", "adrId": "{id}" } }
  ]
}
```
