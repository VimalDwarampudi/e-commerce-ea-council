# Documentation Standards

## Principle: Documentation Is Architecture

Architecture that is not documented does not exist in an institutional sense. When a key person leaves, undocumented decisions leave with them.

---

## What Must Be Documented

| Artefact | Where | When | Owner |
|---|---|---|---|
| Architecture Decision (Standard+) | ADR in `outputs/` | Before implementation starts | Chief Architect |
| Application portfolio record | LeanIX Application fact sheet | Before go-live | Application Owner |
| Integration / data flow | LeanIX Interface fact sheet | Before go-live | Integration Owner |
| Technology component | LeanIX IT Component fact sheet | When introduced or changed | Technical Owner |
| Data object | LeanIX Data Object fact sheet | When data domain is formalized | Data Owner |
| Infrastructure CI | ServiceNow CMDB | Within 5 business days of provisioning | Technical Owner |
| Risk | ServiceNow GRC risk register | Within 5 business days of identification | Risk Owner |
| Policy exception | ServiceNow GRC policy exception log | Before exception is exercised | Risk & Compliance |

---

## Markdown File Standards

All markdown files in the EA Council knowledge base must follow this structure:

```markdown
# [Title — Noun phrase, not a sentence]

## Purpose (optional for short files)
[One paragraph explaining what this file is for and who uses it]

## [Content sections]
...

## Last Updated
[Date] — [What changed]
```

**Formatting rules:**
- Use `##` for top-level sections, `###` for sub-sections
- Use tables for comparisons (3+ options) — not bullet lists
- Use bullet lists for enumerations (order doesn't matter)
- Use numbered lists for sequences (order matters)
- Use `>` blockquotes for definitions, rules, and important callouts
- Use `[MANDATORY]` tag for non-negotiable policies
- Use code blocks for templates, examples, CLI, and structured formats
- Keep files to a single topic — don't let them grow into wikis

---

## Agent Knowledge File Types

| File | Purpose | Updated When |
|---|---|---|
| `agent.md` | System prompt, identity, scope, output format | Agent behaviour changes |
| `policies.md` | Mandatory and standard policies the agent enforces | Policy changes |
| `principles.md` | Architectural principles for the domain | Principles added/revised |
| `guidelines.md` | How-to guidance, methodologies, frameworks | Better practices discovered |
| `examples/` | Sample inputs and outputs for few-shot learning | Good real examples emerge |

---

## ADR Quality Standards

An ADR is complete when it has:

- [ ] Clear one-sentence decision statement
- [ ] Context section that explains *why* the decision was needed now
- [ ] At least two options considered (not just the chosen one)
- [ ] Rationale tracing to at least one architecture principle
- [ ] Council input section with all engaged agents documented
- [ ] Trade-offs table with explicit acceptance
- [ ] Risk table with ratings, owners, and ServiceNow Risk IDs
- [ ] LeanIX and ServiceNow update checklist completed
- [ ] Next steps with owners and dates

An ADR with missing sections is `DRAFT`, not `ACCEPTED`.

---

## LeanIX Documentation Standards

### Minimum required fields per fact sheet type

**Application:**
- Name (per naming convention)
- Lifecycle state
- Business criticality (LOW / MEDIUM / HIGH / MISSION CRITICAL)
- Technical Fit score (1–5)
- Business Fit score (1–5)
- Business Owner (person)
- Technical Owner (person)
- Linked Business Capabilities (≥ 1)
- Linked IT Components (≥ 1)
- Description (one paragraph)

**Interface:**
- Source application
- Target application
- Data objects exchanged
- Protocol
- Direction
- Business criticality
- Owner

**Data Object:**
- Name (per naming convention)
- Data classification
- Owner (business role)
- Linked applications (producing and consuming)
- Description

**IT Component:**
- Name (per naming convention)
- Lifecycle state
- End-of-support date (if known)
- Linked applications

---

## Review and Maintenance Cadence

| Document Type | Review Frequency | Owner |
|---|---|---|
| Architecture principles | Annual (or when a gap is identified) | Chief Architect |
| Tech radar | Quarterly | Technology & Infrastructure + Application |
| Agent policies | Semi-annual (or when regulation changes) | Relevant domain agent owner |
| Agent guidelines | As needed when better practices emerge | Relevant domain agent owner |
| ADRs | Review trigger-based (see each ADR's review date) | Chief Architect |
| LeanIX records | Continuous — updated with every ADR | Application/Integration owners |
