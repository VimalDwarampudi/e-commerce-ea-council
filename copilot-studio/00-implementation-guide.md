# Copilot Studio Implementation Guide — EA Architecture Council

## Purpose

This guide covers everything needed to build the EA Architecture Council as a working multi-agent system in Microsoft Copilot Studio. It is structured as a sequence: read it top to bottom the first time, then use individual sections as reference.

## Guide Structure

| File | Contents |
|---|---|
| `00-implementation-guide.md` | This file — overview and reading order |
| `01-platform-overview.md` | Copilot Studio concepts mapped to EA Council design |
| `02-agent-topology.md` | How to create and configure each agent in Copilot Studio |
| `03-orchestrator-design.md` | Chief Architect orchestrator: topics, actions, prompt design |
| `04-sub-agent-design.md` | Domain and cross-cut agent configuration pattern |
| `05-leanix-mcp-integration.md` | Connecting LeanIX MCP to Copilot Studio |
| `06-servicenow-integration.md` | ServiceNow REST API connector configuration |
| `07-prompt-injection-patterns.md` | How markdown knowledge files feed agent behaviour |
| `08-knowledge-sources.md` | SharePoint / Dataverse knowledge store setup |
| `09-testing-and-validation.md` | How to test the council before going live |
| `10-governance-and-operations.md` | Ongoing management: updates, monitoring, versioning |

## Prerequisites

Before building, confirm you have:

- [ ] Microsoft Copilot Studio license (per-agent or per-message capacity)
- [ ] Microsoft 365 / Power Platform environment (Production recommended; Dev for build/test)
- [ ] Entra ID app registrations for: LeanIX MCP, ServiceNow OAuth client
- [ ] SAP LeanIX MCP server endpoint (provided by LeanIX or self-hosted)
- [ ] ServiceNow instance URL + OAuth 2.0 client credentials
- [ ] SharePoint Online site for knowledge base (markdown files)
- [ ] Power Automate Premium license (for custom connectors and HTTP actions)
- [ ] Azure subscription for: Key Vault (secrets), Log Analytics (logging)

## Recommended Build Order

1. Set up knowledge base (SharePoint + files) — `08-knowledge-sources.md`
2. Configure LeanIX MCP connector — `05-leanix-mcp-integration.md`
3. Configure ServiceNow connector — `06-servicenow-integration.md`
4. Build domain agents (start with Business Architecture) — `04-sub-agent-design.md`
5. Build cross-cut agents (Security, Risk & Compliance, Red Team) — `04-sub-agent-design.md`
6. Build Chief Architect orchestrator — `03-orchestrator-design.md`
7. Wire agents together — `02-agent-topology.md`
8. Test — `09-testing-and-validation.md`
9. Publish and operate — `10-governance-and-operations.md`
