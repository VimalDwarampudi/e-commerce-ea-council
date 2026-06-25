# 01 — Platform Overview: Copilot Studio Concepts Mapped to EA Council

## What Copilot Studio Provides

Copilot Studio (as of 2025–2026) has two primary paradigms for building agents:

| Paradigm | Description | Used For |
|---|---|---|
| **Classic (Topics-based)** | Deterministic conversation flows driven by triggers and nodes | Structured workflows, form collection, fixed-path interactions |
| **Generative (Autonomous Agent)** | LLM-driven reasoning with tools, knowledge sources, and instructions | Open-ended reasoning, multi-step tasks — **this is what we use** |

The EA Council is built almost entirely in the **Generative Agent** paradigm. The Chief Architect uses autonomous reasoning to orchestrate, and each domain agent uses reasoning to produce its assessment.

---

## Core Copilot Studio Concepts

### Agent
A single deployable AI unit. Has:
- A **system prompt** (Instructions field) — its identity, behaviour rules, and constraints
- **Knowledge sources** — documents/SharePoint it can search
- **Actions** — tools it can call (APIs, connectors, other agents)
- **Topics** — optional deterministic triggers for specific phrases

In our design: each of the 9 council roles (1 orchestrator + 8 agents) is a **separate Copilot Studio agent**.

### Instructions (System Prompt)
The core behaviour definition for a generative agent. This is where `agent.md` content lands. Copilot Studio has a character limit (~8,000 characters for Instructions); longer content goes into Knowledge sources.

### Knowledge Sources
Documents the agent can search using semantic retrieval (RAG). Supports:
- SharePoint Online files and sites
- Uploaded documents (PDF, DOCX, TXT, MD)
- Public websites (via URL)
- Dataverse knowledge articles

In our design: `policies.md`, `principles.md`, `guidelines.md`, `shared/` files are loaded as knowledge sources.

### Actions
Capabilities the agent can invoke. Types:
- **Connector actions** — Power Platform connectors (HTTP, ServiceNow, SharePoint, etc.)
- **Flow actions** — Power Automate flows invoked as tools
- **Agent-to-agent** — calling another Copilot Studio agent as a tool
- **MCP (Model Context Protocol)** — external MCP servers exposed as tool collections

In our design: LeanIX MCP, ServiceNow REST, and sub-agent calls are all Actions.

### Topics
Deterministic conversation paths triggered by keywords or events. Used sparingly in our design — primarily for:
- Triage entry point (structured intake form)
- ADR output formatting
- Escalation notification triggers

### Generative Orchestration
When enabled, the agent uses its LLM to decide which actions and knowledge sources to invoke, in what order, based on the user's request. This is the core of the Chief Architect's behaviour.

---

## EA Council → Copilot Studio Mapping

| EA Council Concept | Copilot Studio Equivalent |
|---|---|
| Chief Architect (orchestrator) | Primary agent with generative orchestration; sub-agents as Actions |
| Domain agent (e.g., Application Architecture) | Separate agent; invoked by Chief Architect as an Action |
| Cross-cut agent (Security, Risk, Red Team) | Separate agent; invoked by Chief Architect as an Action |
| `agent.md` | Agent Instructions field (system prompt) |
| `policies.md` | Knowledge source (SharePoint document) |
| `principles.md` | Knowledge source (SharePoint document) |
| `guidelines.md` | Knowledge source (SharePoint document) |
| `shared/architecture-principles.md` | Knowledge source on ALL agents |
| `shared/tech-radar.md` | Knowledge source on Application + Tech & Infra agents |
| LeanIX MCP | MCP Action on relevant agents |
| ServiceNow REST API | HTTP connector Action (Power Automate flow) |
| Deliberation protocol | Encoded in Chief Architect Instructions + Topics |
| ADR output | Structured response using ADR template from Knowledge |
| Escalation | Adaptive Card or Teams message trigger via Power Automate |

---

## Architecture Decisions Made for Copilot Studio

### Decision: One Agent Per Role (Not One Agent With Routing)
**Why:** Copilot Studio's context window and Instructions field are limited. Packing all 8 domain roles into one agent produces worse results than dedicated agents with focused Instructions and Knowledge. Agent-to-agent calls are first-class in Copilot Studio.

### Decision: Generative Orchestration (Not Classic Topics) for Chief Architect
**Why:** The Chief Architect's routing logic is complex and context-dependent. Generative orchestration lets the LLM decide which agents to call based on the request — matching the `routing-rules.md` intent without building a brittle decision tree in Topics.

### Decision: SharePoint as Knowledge Store (Not Dataverse)
**Why:** SharePoint supports markdown/text files natively and integrates seamlessly with Copilot Studio knowledge sources. Files can be updated by the EA team without touching the agent configuration. Dataverse is more appropriate for structured records (ADR metadata, risk register sync).

### Decision: Power Automate for ServiceNow (Not Direct HTTP Action)
**Why:** ServiceNow OAuth flows, error handling, and response transformation are complex enough to warrant a dedicated Power Automate flow per operation. This also allows non-EA teams to trigger architecture workflows from ServiceNow directly.

### Decision: MCP for LeanIX (Not Custom Connector)
**Why:** LeanIX provides an MCP server. Copilot Studio supports MCP natively (preview/GA depending on your tenant's release ring). This gives richer, schema-aware tool calls with less connector development overhead.
