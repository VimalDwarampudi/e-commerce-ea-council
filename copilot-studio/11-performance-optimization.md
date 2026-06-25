# 11 — Performance & Reliability Optimization

## Overview

This guide defines retrieval discipline, token budgets, and output constraints for all EA Council agents operating in Copilot Studio. Following these rules reduces token cost by 60–80%, improves reasoning quality (less noise in context), and prevents "runaway retrieval" loops.

---

## Core Principles

1. **Retrieve only what you need to make a decision** — not everything available
2. **Progressive disclosure** — list → summarize → shortlist → detail
3. **Field projection** — request specific fields, never raw record dumps
4. **Bounded results** — every query has a hard limit; default is 10 items
5. **Read-only by default** — writes require explicit user intent + ADR acceptance

---

## Retrieval Budget Defaults

These budgets apply to every agent, every turn.

| Budget | Default | Max (orchestrator override) | Notes |
|---|---|---|---|
| Items per query | **10** | 25 | Orchestrator can override with justification |
| Pages per list operation | **1** | 3 | Retrieve 1 page → summarize → decide if more needed |
| Total items per user question | **30** | 60 | Across all queries in a single deliberation |
| Fields per item | **6–8** | 12 | id, name, lifecycle, criticality, owner, key metric |
| Free-text per item | **1 short line** | 300 chars | Truncate long descriptions; note "full text available" |

### Stop Conditions (mandatory)
Stop fetching more data when ANY of these is true:
1. ✅ You can make a decision (evidence sufficiency)
2. ❌ The result set is clearly irrelevant (wrong domain/object type)
3. 🛑 You've hit the page or item budget

---

## Progressive Disclosure Protocol

Every data retrieval follows this sequence. Do not skip steps.

```
Step 1: LIST (page 1)
  → Query with limit: 10, minimal fields only
  → Purpose: get the landscape; see what exists

Step 2: SUMMARIZE
  → Count by category/status
  → Note top themes, notable outliers
  → Decide: do you need more data? If no → skip to Step 5

Step 3: SHORTLIST
  → Pick 3–7 items that are relevant to the decision
  → These are the items you'll investigate further

Step 4: DETAIL FETCH
  → Retrieve full details only for shortlisted items (by ID)
  → Still use field projection — don't pull everything

Step 5: DECIDE
  → Form your assessment based on retrieved evidence
  → Cite specific items: "Application X (LeanIX ID: abc-123) is Phase Out since 2024"
```

**Example — Application Architecture assessing an HR platform proposal:**
1. LIST: Query applications by HR Business Capability → 10 results, minimal fields
2. SUMMARIZE: "4 HR applications found: 2 Active, 1 Phase Out, 1 End of Life. 2 apps have no owner."
3. SHORTLIST: Pick the 3 that overlap with the proposed SuccessFactors scope
4. DETAIL: Fetch full records for those 3 (lifecycle phases, fit scores, IT components)
5. DECIDE: Form TIME model assessment

---

## LeanIX Query Optimization

### Default Field Sets (use these instead of full records)

**Application list (minimal — Step 1):**
```
fields: id, name, lifecycle.asString, businessCriticality, technicalFit, functionalFit
```
6 fields. No description, no owner, no relationships. Get those in Step 4 if needed.

**Application detail (shortlisted — Step 4):**
```
fields: id, name, lifecycle (full with phases), businessCriticality, technicalFit, 
        functionalFit, businessOwner, technicalOwner, 
        relApplicationToBusinessCapability.name,
        relApplicationToITComponent.name
```

**Interface list (minimal):**
```
fields: id, name, provider.name, consumer.name, description (first 100 chars)
```

**IT Component list (minimal):**
```
fields: id, name, category, lifecycle.asString, vendor
```

### LeanIX MCP Toolset Discipline

**MCP server URL pattern:**
```
https://{SUBDOMAIN}.leanix.net/services/mcp-server/v1/mcp?toolsets=inventory
```
Multiple toolsets (comma-separated):
```
https://{SUBDOMAIN}.leanix.net/services/mcp-server/v1/mcp?toolsets=inventory,roadmap_planning
```

> ⚠️ **Prerequisite:** Base AI Capabilities must be activated in your LeanIX workspace before connecting agents. Without this, MCP response precision is significantly reduced. Activate in LeanIX Admin → AI Settings → Base AI Capabilities.

> ⚠️ **Default behaviour:** When no `toolsets` parameter is provided, **all tools are returned** — including write-capable toolsets (`surveys`, `architecture_decisions`). Always pass an explicit `toolsets` parameter to limit the tool surface.

**Toolset reference (all 6 available):**

| Toolset | Read/Write | When to enable | Default |
|---|---|---|---|
| `inventory` | Read | Always — core fact sheet queries | ✅ Enabled |
| `roadmap_planning` | Read | Only for initiative, roadmap, or transformation questions | ❌ On demand |
| `report_diagrams` | Read | Only when user explicitly requests a diagram or visual | ❌ On demand |
| `self_built_software` | Read + Write | For shadow IT discovery and tech stack management; write only after write gate | ❌ On demand |
| `surveys` | Write | Only after ADR ACCEPTED + explicit user confirmation | ❌ Write-gated |
| `architecture_decisions` | Write | Only after ADR ACCEPTED + explicit user confirmation | ❌ Write-gated |

**Toolset limits (hard constraints from MCP server):**
- Maximum 10 toolsets per request (`TooManyToolsetsError` if exceeded)
- Each toolset name must not exceed 50 characters (`ToolsetTooLongError` if exceeded)
- Invalid/misspelled toolset name → server returns error (not empty result)

**Rule:** Default to `toolsets=inventory` for all read queries. Add additional toolsets only when the decision explicitly requires them. Never omit the `toolsets` parameter.

### `self_built_software` toolset — new capability

The `self_built_software` toolset exposes self-built software discovery APIs. Use cases for EA Council agents:
- **Application Architecture:** Discover undocumented custom-built applications (shadow IT) — feeds AA-POL-007 (Unowned Applications check)
- **Technology & Infrastructure:** Identify self-built components for lifecycle and tech radar assessment
- **R&D & EDA:** Discover internally-built research tools not registered in LeanIX

Enable only when explicitly investigating undocumented software. The write capability (creating self-built software records) is subject to the write gate protocol.

### Query Limit Enforcement

All LeanIX GraphQL queries must include:
```graphql
first: 10  # default — increase to 25 only with justification
```

Never use queries without `first:` — this risks pulling the entire landscape.

---

## ServiceNow Query Optimization

### Default Parameters (add to every query)

```
sysparm_limit=10                    # default 10, max 25
sysparm_fields=<projected_fields>   # always specify — never omit
sysparm_display_value=true          # human-readable labels
```

### Default Field Sets

**CMDB CI list (minimal):**
```
sysparm_fields=sys_id,name,short_description,install_status,operational_status,business_criticality,owned_by
```

**Change request list (minimal):**
```
sysparm_fields=number,short_description,state,priority,risk,start_date,end_date
```

**GRC risk list (minimal):**
```
sysparm_fields=number,short_description,risk_rating,state,assigned_to,review_date
```

### Excluding Large Fields

ServiceNow records often contain large text fields (description, work_notes, close_notes, comments). These burn tokens and add noise.

**Rule:** Never include these fields in list queries:
- `description` (use `short_description` instead)
- `work_notes`
- `comments`
- `close_notes`
- `resolution_notes`

Retrieve these only in Step 4 (detail fetch for shortlisted records) and truncate to 300 characters.

---

## Power Automate Flow Response Envelope

All Power Automate flows returning data to Copilot Studio agents should use this standard envelope:

```json
{
  "status": "success",
  "summary": "Found 4 HR applications, 2 Active, 1 Phase Out, 1 End of Life",
  "meta": {
    "source": "LeanIX",
    "query": "Applications by capability: Human Resources",
    "recordCount": 4,
    "pageSize": 10,
    "hasMore": false
  },
  "data": [
    {
      "id": "abc-123",
      "name": "HR-Legacy-PeopleOne",
      "lifecycle": "End of Life",
      "criticality": "LOW",
      "technicalFit": "1/5",
      "functionalFit": "1/5"
    }
  ]
}
```

**Why this matters:** The `summary` field gives the agent immediate context without parsing all records. The `meta.hasMore` flag tells the agent whether paging is needed. The `data` array is bounded and field-projected.

---

## Write Gate Protocol

No write operation (LeanIX update, ServiceNow change request creation) is executed without passing through this gate:

```
1. ADR status = ACCEPTED ✓
2. User has explicitly confirmed the write-back action ✓
   (via Adaptive Card button click or explicit text confirmation)
3. Write scope is specific and bounded ✓
   (update THIS application's lifecycle to Phase Out — not "update all HR apps")
4. Agent states what will be written before writing ✓
   ("I will update Application HR-Legacy-PeopleOne lifecycle to 'End of Life' in LeanIX. Confirm?")
```

Only when all four conditions are met does the orchestrator invoke the write action.

---

## Agent-Specific Optimization Rules

### Chief Architect (Orchestrator)
- Retrieve LeanIX/ServiceNow data BEFORE calling sub-agents — pass the data to them, don't have each agent query independently
- Budget: up to 60 total items across all Phase 1–6 queries (orchestrator max)
- When calling sub-agents: include the pre-fetched data in the prompt to avoid duplicate queries

### Domain Agents (all 7)
- Budget: 30 items max per assessment
- Use progressive disclosure: LIST → SUMMARIZE → SHORTLIST → DETAIL
- If the orchestrator already provided LeanIX/ServiceNow data: use it, don't re-query
- If data is stale or insufficient: one additional query allowed, with justification in output

### Cross-Cut Agents (Security, Risk & Compliance)
- These agents REVIEW data already retrieved by domain agents — they should rarely need their own queries
- Exception: Security may query ServiceNow GRC for existing risks; Risk & Compliance may query for policy exceptions
- Budget: 10 items max per additional query

### Red Team
- No external queries. Red Team works entirely on the agent outputs provided to it.
- Budget: 0 external queries (by design)

---

## Token Cost Estimation

With optimization applied:

| Scenario | Estimated tokens per deliberation |
|---|---|
| MINOR (2 agents, 1 query) | 8,000–15,000 |
| STANDARD (4 agents + Security, 3–5 queries) | 25,000–45,000 |
| MAJOR (7 agents + Security + Risk, 5–8 queries) | 50,000–80,000 |
| CRITICAL (all 10 agents + Red Team, 8–12 queries) | 80,000–120,000 |

Without optimization (no field projection, no limits): 3–5× higher.

---

## Monitoring Checklist

Track these metrics weekly:

- [ ] Average tokens per deliberation (by impact level)
- [ ] Number of LeanIX MCP calls per question
- [ ] Number of Power Automate flow runs per question
- [ ] Percentage of queries hitting the item budget (indicates budget may need adjustment)
- [ ] Percentage of queries returning 0 results (indicates query quality issue or data gap)
- [ ] Agent response time (end-to-end per sub-agent call)
