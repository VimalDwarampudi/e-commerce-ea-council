# 10 — Governance and Operations

## Overview

Building the EA Council is phase one. Operating it sustainably is phase two. This document covers the ongoing management model: who owns what, how to monitor the system, how to update it, and how to evolve it over time.

---

## Ownership Model

| Component | Owner | Backup Owner |
|---|---|---|
| Chief Architect agent configuration | EA Lead / Enterprise Architect | Senior EA team member |
| Domain agent configurations | Relevant domain architect | EA Lead |
| Knowledge files (markdown) | EA team (collective ownership) | EA Lead |
| LeanIX MCP connector | Integration Architect / IT team | EA Lead |
| ServiceNow connector & flows | ServiceNow admin + EA team | IT Operations |
| SharePoint knowledge base | EA team + SharePoint admin | IT Operations |
| Azure Key Vault (secrets) | IT Security + EA Lead | IT Operations |
| ADR register and archive | EA team | EA Lead |

---

## Change Management for the System

The EA Council is itself subject to architecture governance. Changes to agent configurations, knowledge files, and connectors follow this process:

### Minor changes (wording, formatting, adding examples)
- Update in Git → merge to main → auto-sync to SharePoint → Copilot Studio re-indexes
- No approval required; document in Git commit message

### Standard changes (policy updates, new guidelines, action changes)
- Raise as a change proposal in the EA team
- Review by EA Lead
- Test in Development environment before merging
- Document change in the relevant file's "Last Updated" section
- Notify council users of significant behaviour changes

### Major changes (new agents, structural redesign, new integrations)
- Full ADR through the EA Council itself (meta: the council reviews its own architecture)
- Test in full UAT cycle (`09-testing-and-validation.md`)
- Staged rollout: Development → Test → Production

---

## Monitoring

### What to Monitor

| Metric | Where | Alert Threshold |
|---|---|---|
| **Agent usage** — requests per day/week | Copilot Studio Analytics | Baseline ± 50% (spike or sudden drop) |
| **Response quality score** | Copilot Studio feedback (thumbs up/down) | < 70% positive in rolling 7 days |
| **Action error rate** — LeanIX / ServiceNow failures | Power Automate run history | > 5% failure rate in 24h |
| **Avg deliberation time** — end to end | Custom logging (see below) | > 3 minutes for Standard decisions |
| **Escalation rate** | ADR register | > 20% of decisions escalated (sign of miscalibration) |
| **Veto rate** | ADR register | Track trend; sudden spike = policy change or agent drift |
| **ADRs produced** | ADR register | Track velocity; sudden drop = adoption issue |

### Custom Logging via Power Automate

Instrument the Chief Architect Topic to log each deliberation to a SharePoint list or Dataverse table:

```
EA Council Deliberation Log (SharePoint List columns):
- Session ID
- Timestamp
- Request summary (first 200 chars)
- Impact level
- Agents consulted (comma-separated)
- Veto issued (Y/N)
- Escalation triggered (Y/N)
- ADR produced (Y/N)
- ADR ID (if produced)
- Duration (seconds)
- User (if not anonymous)
- Feedback score (from Teams Adaptive Card thumbs up/down)
```

---

## Periodic Maintenance Tasks

### Weekly
- [ ] Review Power Automate flow run history — check for ServiceNow/LeanIX connector failures
- [ ] Review Copilot Studio conversation logs — spot-check 3–5 recent ADRs for quality
- [ ] Check ADR register — are ADRs being produced and stored correctly?

### Monthly
- [ ] Review agent feedback scores — identify any agent with declining quality
- [ ] Review escalation log — patterns in what's being escalated (policy gaps? scope issues?)
- [ ] Check Azure Key Vault secret expiry dates — rotate before expiry
- [ ] Review LeanIX API token expiry (if using token auth)

### Quarterly
- [ ] **Tech radar update** — EA team reviews and updates `shared/tech-radar.md`; re-sync to SharePoint
- [ ] **Policy review** — scan all `policies.md` files for outdated content; update and version
- [ ] **Regulatory radar** — Risk & Compliance agent knowledge reviewed against new/amended regulations
- [ ] **Agent quality audit** — run full test suite from `09-testing-and-validation.md`
- [ ] **LeanIX data quality check** — ensure LeanIX portfolio is current; flag stale records

### Annually
- [ ] Full architecture review of the EA Council itself (use the council to review its own architecture)
- [ ] Review all agent Instructions fields — do they reflect current best practice?
- [ ] Review all reference architectures — update for platform changes (Azure services, SAP updates)
- [ ] Revalidate all integration test scenarios against current LeanIX and ServiceNow data

---

## Version Control Strategy

```
Git repository: ea-council-knowledge
Branch strategy:
  main        → Production (auto-syncs to SharePoint production site)
  develop     → Development environment
  feature/*   → Individual changes (PR to develop, then develop to main)

Tagging:
  v{YYYY}.{Q}{N} — quarterly baseline tags
  e.g., v2026.Q2.1 — first release of Q2 2026
```

**Commit message convention:**
```
[agent/shared/copilot] [change type]: brief description

Examples:
[security] policy: add SEC-POL-011 for container image scanning
[shared] tech-radar: move ArgoCD from TRIAL to ADOPT
[copilot] orchestrator: improve veto acknowledgment instructions
[data-ai] guidelines: add EU AI Act 2026 amendment guidance
```

---

## Evolving the Council

### Adding a New Domain Agent

When a new domain is needed (e.g., Sustainability Architecture, IoT Architecture):

1. Create agent folder: `agents/{new-domain}/`
2. Write `agent.md`, `policies.md`, `principles.md`, `guidelines.md`
3. Upload to SharePoint knowledge base
4. Create new Copilot Studio agent following `04-sub-agent-design.md` pattern
5. Add as Action to Chief Architect: `Consult{NewDomain}`
6. Update `orchestration/routing-rules.md` with new routing triggers
7. Update `council-config.md` council composition table
8. Test per `09-testing-and-validation.md` Level 1 + Level 3

### Updating Policies After a Regulatory Change

1. EA team and Legal review the regulatory change
2. Update affected `policies.md` files — new or amended policies tagged `[MANDATORY]` or not
3. Add a note to `agents/risk-compliance/guidelines.md` if it changes the compliance assessment process
4. Sync to SharePoint; trigger knowledge re-index
5. Run relevant test cases from Level 2 (cross-cut agent tests) to verify policy enforcement
6. Notify council users via Teams channel post

### Handling Agent Drift

LLM behaviour can drift with model updates or context changes. Signs of drift:
- Agent outputs no longer follow the output format
- Agents answer outside their domain scope
- Veto fires too frequently or not enough
- Synthesis quality degrades

**Response:**
1. Run the full test suite to quantify the drift
2. Review Instructions field — add more explicit constraints where drift is occurring
3. Add concrete examples to the `examples/` folder for the affected agent
4. If model was updated by Microsoft: test against the new model version in Development first
5. Consider adding negative examples: "Do NOT produce outputs like this: [bad example]"

---

## Capacity Planning

Copilot Studio licensing for this system:

| Component | Licensing Model |
|---|---|
| Chief Architect (user-facing) | Per-message capacity (Messages capacity pool) |
| 8 Sub-agents (internal, called by orchestrator) | Counted as orchestrator messages — each sub-agent call consumes messages |
| Power Automate flows | Power Automate Premium per flow |
| SharePoint knowledge sources | Included in Microsoft 365 |
| LeanIX MCP calls | Subject to LeanIX API rate limits |
| ServiceNow API calls | Subject to ServiceNow API rate limits |

**Rough message consumption per request:**
- Minor decision: ~5–10 messages (triage + 1–2 agent calls + synthesis)
- Standard decision: ~15–25 messages (triage + 4–5 agent calls + 2 cross-cut + synthesis)
- Major decision: ~25–40 messages (triage + 6 agent calls + 3 cross-cut + synthesis)
- Critical decision: ~40–60 messages (full council + multiple synthesis rounds)

Plan capacity based on expected request volume. Monitor via Copilot Studio Analytics.
