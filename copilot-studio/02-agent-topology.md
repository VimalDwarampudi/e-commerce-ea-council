# 02 — Agent Topology: Creating and Connecting Agents

## Full Agent Inventory

Create these 9 agents in Copilot Studio. All sit in the same Power Platform environment.

| Agent Name (display) | Internal ID (suggested) | Type | Invoked By |
|---|---|---|---|
| EA Council — Chief Architect | `ea-chief-architect` | Orchestrator | Human sponsors (direct) |
| EA Council — Business Strategy | `ea-business-strategy` | Domain Agent | Chief Architect |
| EA Council — Product Management | `ea-product-mgmt` | Domain Agent | Chief Architect |
| EA Council — Search & Discovery | `ea-search-discovery` | Domain Agent | Chief Architect |
| EA Council — Checkout & Payments | `ea-checkout-payments` | Domain Agent | Chief Architect |
| EA Council — Order Management | `ea-order-mgmt` | Domain Agent | Chief Architect |
| EA Council — Fulfillment & Logistics | `ea-fulfillment-logistics` | Domain Agent | Chief Architect |
| EA Council — Customer Experience | `ea-customer-exp` | Domain Agent | Chief Architect |
| EA Council — Data Platform | `ea-data-platform` | Domain Agent | Chief Architect |
| EA Council — Technology Infrastructure | `ea-tech-infra` | Domain Agent | Chief Architect |
| EA Council — Security Architecture | `ea-security` | Cross-Cut Agent | Chief Architect |
| EA Council — Risk & Compliance | `ea-risk-compliance` | Cross-Cut Agent | Chief Architect |
| EA Council — Innovation Team | `ea-innovation-team` | Cross-Cut Agent | Chief Architect |

---

## How Agent-to-Agent Calls Work in Copilot Studio

Copilot Studio supports **agent-to-agent invocation** as a first-class action type. The orchestrator (Chief Architect) calls a sub-agent by:

1. Adding the sub-agent as an **Action** of type "Agent"
2. Defining the **input** (what context is passed to the sub-agent)
3. Receiving the **output** (the sub-agent's response as a string)
4. The orchestrator then incorporates the response into its own reasoning

This is how the deliberation protocol's "parallel domain assessment" phase is implemented — the Chief Architect issues calls to each selected domain agent, collects their outputs, then synthesizes.

### Adding a Sub-Agent as an Action

In Copilot Studio (Chief Architect agent):
```
Actions → Add an action → Agent
→ Select: EA Council — Business Architecture
→ Name: ConsultBusinessArchitecture
→ Description: "Consult the Business Architecture agent for strategic alignment and capability assessment"
→ Input: requestContext (string) — the full request + domain-specific sub-question + relevant data
→ Output: domainAssessment (string) — the agent's structured assessment
```

Repeat for each of the 12 sub-agents.

---

## Agent Invocation Contract

Each sub-agent call uses this standard input structure (passed as a string):

```
REQUEST: {original_request}

YOUR SPECIFIC QUESTION: {domain_sub_question}

RELEVANT LEANIX DATA:
{leanix_data_for_this_domain}

RELEVANT SERVICENOW DATA:
{servicenow_data_if_applicable}

DELIBERATION PHASE: {Phase 2 / Phase 3 / Phase 4}

CONTEXT FROM PEER AGENTS (for cross-cut reviews):
{peer_outputs_if_phase_3_or_4}
```

The sub-agent always returns:
```
## {Domain Name} Assessment
{structured output per the agent's output format in agent.md}
```

---

## Sequencing: Parallel vs Sequential in Copilot Studio

Copilot Studio's generative orchestration currently invokes actions **sequentially** (one at a time), not truly in parallel. Design implications:

**For Phase 2 (Domain Assessment):**
- The Chief Architect calls each domain agent in sequence
- Each call is independent (no dependency on previous outputs)
- Effective latency = sum of individual agent response times
- Typical: 3–5 agents × 10–20s each = 30–100s total for Phase 2
- **Mitigation:** Only call agents that are relevant to the request (routing-rules.md logic)

**For Phase 3 (Cross-Cut Review):**
- Cross-cut agents receive the compiled Phase 2 outputs
- Sequential calls (Security → Risk & Compliance)
- Each cross-cut agent receives all domain outputs as context

**For Phase 4 (Red Team):**
- Red Team receives all Phase 2 + Phase 3 outputs combined
- Single call — no sequencing issue

**For Phase 5 (Synthesis):**
- Chief Architect's own reasoning — no sub-agent calls
- This is pure LLM generation by the orchestrator

---

## Publishing and Channels

The Chief Architect agent is the only agent published to end-user channels. Sub-agents are internal — they are not published directly to users.

### Recommended Channels for Chief Architect

| Channel | Use Case | Notes |
|---|---|---|
| **Microsoft Teams** | Primary channel for EA requests | Install as a Teams app; supports Adaptive Cards for ADR output |
| **SharePoint** | Embedded on EA intranet page | Embedded web chat widget |
| **Direct URL** | For EA team members | Copilot Studio web channel |
| **Power Apps** | Custom EA portal | Embed via PCF or iframe |

### Do NOT publish sub-agents to end-user channels
Sub-agents (domain and cross-cut) should be set to **Internal use only**. They have no user-facing conversation management — they are tools, not conversational agents.

---

## Environment Strategy

| Environment | Purpose |
|---|---|
| **Development** | Build, configure, and test agents; dummy LeanIX/ServiceNow connections |
| **Test / UAT** | Validation with real (read-only) LeanIX and ServiceNow data |
| **Production** | Live EA Council; write-back to LeanIX and ServiceNow enabled |

Use Power Platform solution exports to move agents between environments. Store solution files in your Git repository alongside the markdown knowledge files.

---

## Agent Settings Checklist (per agent)

Configure these settings for every agent:

- [ ] **Name:** follows naming convention above
- [ ] **Instructions:** system prompt from `agent.md` (core identity + scope + output format)
- [ ] **Language:** match your organization's primary language (English recommended for council)
- [ ] **Generative AI:** enabled (required for autonomous reasoning)
- [ ] **Knowledge sources:** policies, principles, guidelines, relevant shared files
- [ ] **Classic NLP:** disabled for domain/cross-cut agents (they don't need it — they're tools)
- [ ] **Fallback behaviour:** configured to return a structured "unable to assess" response rather than hallucinating
- [ ] **Content moderation:** set to organizational standard
- [ ] **Authentication:** configured to inherit calling user's identity or use service principal
