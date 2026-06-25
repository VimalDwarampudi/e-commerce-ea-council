# 07 — Prompt Injection Patterns

## The Problem This Solves

Copilot Studio's Instructions field has a ~8,000 character limit. The full content of `agent.md` + `policies.md` + `principles.md` + `guidelines.md` for each agent far exceeds this. The solution is a layered approach:

| Layer | Where It Lives | How the Agent Accesses It |
|---|---|---|
| **Core identity + output format** | Instructions field | Always in context (system prompt) |
| **Policies + principles** | Knowledge sources (SharePoint) | Retrieved via semantic search when relevant |
| **Guidelines + examples** | Knowledge sources (SharePoint) | Retrieved via semantic search when relevant |
| **Shared principles + tech radar** | Knowledge sources (SharePoint) | Retrieved via semantic search when relevant |
| **LeanIX / ServiceNow data** | Real-time via Actions | Retrieved on-demand during deliberation |

---

## What Goes in the Instructions Field

Keep the Instructions field focused on **always-needed, core behaviour**. Use this template as the skeleton:

```
## Identity
[2–3 sentences from agent.md Identity section]

## Scope
[Scope bullet list from agent.md — abbreviated to ~200 words]

## Core Behaviour Rules
[Behaviour section from agent.md — keep to 5–8 critical rules]

## Output Format
[Full output format template from agent.md — this must always be in context]

## Grounding Rules
[Standard grounding instruction from 04-sub-agent-design.md Part 3]
```

**Character budget guideline:**
- Identity: ~200 chars
- Scope (abbreviated): ~400 chars
- Behaviour rules: ~600 chars
- Output format template: ~800 chars
- Grounding rules: ~400 chars
- **Total: ~2,400 chars** — leaves headroom for Copilot Studio's own system additions

---

## Knowledge Source Retrieval Patterns

Copilot Studio uses **semantic search (RAG)** to retrieve relevant knowledge source content. The agent's query to the knowledge source is derived from the conversation context — you don't control it directly. However, you can influence retrieval quality:

### Pattern 1: Explicit Knowledge Pull via Instructions

Add this to the Instructions field for policies and principles:

```
Before producing your assessment, retrieve and apply:
1. Your domain policies (policies.md) — check every recommendation against mandatory policies
2. Your domain principles (principles.md) — ground every recommendation in a named principle
3. Enterprise architecture principles (architecture-principles.md) — apply EP-003 and EP-010 first
If a policy or principle is directly relevant to the request, cite it by ID in your output.
```

This instruction causes the agent to actively search its knowledge sources, rather than waiting for Copilot Studio to retrieve passively.

### Pattern 2: Structured Retrieval Anchors in Files

Format policy and principle files with consistent, searchable headings so RAG retrieval is accurate:

```markdown
## SEC-POL-001: Authentication Required for All APIs [MANDATORY]
[content]

## SEC-POL-002: Encryption in Transit [MANDATORY]
[content]
```

The `[MANDATORY]` tag is a retrieval anchor — when the agent searches for "mandatory security policies", these headings surface reliably.

### Pattern 3: Examples as Few-Shot Retrievable Content

Place worked examples in `examples/` folders. When the agent needs to produce an output, it can retrieve a relevant example to calibrate format and depth.

Structure each example file as:
```markdown
# Example: [Scenario Title]

## Input (Request Summary)
[Brief description of the request that triggered this assessment]

## Output (Agent Assessment)
[Full example output in the agent's output format]

## Key Points Illustrated
- [What makes this a good example of the format]
- [Which principle or policy was applied]
```

---

## Dynamic Context Injection

For the Chief Architect orchestrator, context grows during deliberation (each agent adds ~500–2,000 tokens). Manage this with structured accumulation:

### Deliberation Context Object

The Chief Architect maintains a running context object across phases:

```
DELIBERATION CONTEXT
====================
Request: {original request}
Impact Level: {Minor/Standard/Major/Critical}
Triage Date: {timestamp}

LeanIX Data Retrieved:
{summary of what was queried and key findings}

ServiceNow Data Retrieved:
{summary}

Phase 2 — Domain Assessments:
[Business Architecture]: {assessment summary — 200 words max}
[Application Architecture]: {assessment summary}
[Integration Architecture]: {assessment summary}
[Technology & Infrastructure]: {assessment summary}
[Data & AI]: {assessment summary}

Phase 3 — Cross-Cut Reviews:
[Security Architecture]: {assessment summary + veto status}
[Risk & Compliance]: {assessment summary + escalation status}

Phase 4 — Red Team:
[Red Team]: {top findings + confidence rating}

Phase 5 — Synthesis:
[Status: IN PROGRESS / COMPLETE]
[Conflicts identified: {list}]
[Conflicts resolved: {how}]
[Outstanding: {what needs escalation}]
```

Pass this context object to each subsequent agent call. This prevents agents from receiving stale or partial context.

### Token Management

Full agent outputs can be verbose. The Chief Architect should:
1. Request **summary** outputs from domain agents (200–400 words each)
2. Request **full** outputs only when synthesis reveals a conflict that requires deeper review
3. Truncate LeanIX/ServiceNow raw data to key findings before injecting into agent prompts

Add to Chief Architect Instructions:
```
When calling sub-agents, request summary outputs (200–400 words). 
If a conflict emerges during synthesis that requires deeper analysis from a specific agent, 
call that agent again with the instruction: "Provide a detailed analysis of [specific point]. 
Context: [conflicting positions]."
```

---

## Handling the Instructions Character Limit

If your Instructions field approaches the limit, use this prioritization:

**Must be in Instructions (never move to Knowledge):**
- Agent identity and persona
- Scope and out-of-scope boundaries
- Output format template (exact structure)
- Grounding rules (query before stating facts)
- Veto/escalation rules (for Security and Risk agents)

**Can be in Knowledge (retrieved when relevant):**
- Full policy text (just reference in Instructions: "Apply policies from policies.md")
- Full principle text (just reference: "Apply principles from principles.md")
- Detailed guidelines and methodology
- Framework references (TOGAF, GDPR, EU AI Act details)
- Examples

**Instruction shorthand for knowledge retrieval:**
```
Apply your policies (policies.md) and principles (principles.md) from your knowledge base.
For MANDATORY policies: check compliance and flag violations in your assessment.
For principles: cite the relevant principle ID when making each recommendation.
```
