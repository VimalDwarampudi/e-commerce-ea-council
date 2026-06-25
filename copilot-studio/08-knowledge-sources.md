# 08 — Knowledge Sources Setup

## Overview

The markdown files in this repository are the "brain" of each agent. They are loaded into Copilot Studio as Knowledge Sources via SharePoint Online. This setup enables:
- EA team updates knowledge files without touching agent configuration
- Version control of knowledge files in Git, synced to SharePoint
- Granular assignment of knowledge to specific agents

---

## SharePoint Site Structure

Create a dedicated SharePoint site: **EA Council Knowledge Base**

```
SharePoint Site: EA Council Knowledge Base
URL: https://{tenant}.sharepoint.com/sites/ea-council-kb

Document Libraries:
├── /shared/              ← All agents have access
│   ├── architecture-principles.md
│   ├── glossary.md
│   ├── tech-radar.md
│   └── standards/
│       ├── adr-template.md
│       ├── naming-conventions.md
│       └── documentation-standards.md
│   └── reference-architectures/
│       ├── cloud-native.md
│       ├── integration-patterns.md
│       └── data-platform.md
│
├── /agents/
│   ├── business-architecture/
│   │   ├── policies.md
│   │   ├── principles.md
│   │   ├── guidelines.md
│   │   └── examples/
│   ├── application-architecture/
│   │   ├── policies.md
│   │   ├── principles.md
│   │   ├── guidelines.md
│   │   └── examples/
│   ├── integration-architecture/
│   │   [same structure]
│   ├── technology-infrastructure/
│   │   [same structure]
│   ├── data-ai/
│   │   [same structure]
│   ├── security/
│   │   ├── policies.md
│   │   ├── principles.md
│   │   ├── guidelines.md
│   │   ├── veto-criteria.md
│   │   └── examples/
│   ├── risk-compliance/
│   │   ├── policies.md
│   │   ├── principles.md
│   │   ├── guidelines.md
│   │   ├── risk-appetite.md
│   │   └── examples/
│   └── red-team/
│       ├── policies.md
│       ├── guidelines.md
│       ├── challenge-framework.md
│       └── examples/
│
└── /outputs/             ← ADR store (written by Chief Architect)
    ├── adr-register.md
    └── adr/
        └── [ADR-YYYY-NNN-title.md files]
```

---

## Knowledge Source Assignment Per Agent

Configure knowledge sources in Copilot Studio for each agent:

### Chief Architect
```
/shared/ (entire library — full access)
/agents/ (all agents — for synthesis context)
/outputs/adr-register.md (to check existing decisions)
```

### Business Architecture Agent
```
/shared/architecture-principles.md
/shared/glossary.md
/shared/tech-radar.md (for strategic context)
/agents/business-architecture/policies.md
/agents/business-architecture/principles.md
/agents/business-architecture/guidelines.md
/agents/business-architecture/examples/
```

### Application Architecture Agent
```
/shared/architecture-principles.md
/shared/glossary.md
/shared/tech-radar.md          ← important: app agent uses this heavily
/agents/application-architecture/policies.md
/agents/application-architecture/principles.md
/agents/application-architecture/guidelines.md
/agents/application-architecture/examples/
```

### Integration Architecture Agent
```
/shared/architecture-principles.md
/shared/glossary.md
/shared/reference-architectures/integration-patterns.md
/agents/integration-architecture/policies.md
/agents/integration-architecture/principles.md
/agents/integration-architecture/guidelines.md
/agents/integration-architecture/examples/
```

### Technology & Infrastructure Agent
```
/shared/architecture-principles.md
/shared/glossary.md
/shared/tech-radar.md
/shared/reference-architectures/cloud-native.md
/agents/technology-infrastructure/policies.md
/agents/technology-infrastructure/principles.md
/agents/technology-infrastructure/guidelines.md
/agents/technology-infrastructure/examples/
```

### Data & AI Agent
```
/shared/architecture-principles.md
/shared/glossary.md
/shared/reference-architectures/data-platform.md
/agents/data-ai/policies.md
/agents/data-ai/principles.md
/agents/data-ai/guidelines.md
/agents/data-ai/examples/
```

### Security Architecture Agent
```
/shared/architecture-principles.md
/shared/glossary.md
/agents/security/policies.md
/agents/security/principles.md
/agents/security/guidelines.md
/agents/security/veto-criteria.md
/agents/security/examples/
```

### Risk & Compliance Agent
```
/shared/architecture-principles.md
/shared/glossary.md
/agents/risk-compliance/policies.md
/agents/risk-compliance/principles.md
/agents/risk-compliance/guidelines.md
/agents/risk-compliance/risk-appetite.md
/agents/risk-compliance/examples/
```

### Red Team Agent
```
/shared/architecture-principles.md
/shared/glossary.md
/agents/red-team/policies.md
/agents/red-team/guidelines.md
/agents/red-team/challenge-framework.md
/agents/red-team/examples/
```

---

## Syncing Git Repository to SharePoint

Maintain the markdown files in Git (your version-controlled source of truth), and sync to SharePoint:

### Option A: GitHub Actions → SharePoint (recommended)

```yaml
# .github/workflows/sync-to-sharepoint.yml
name: Sync EA Council Knowledge to SharePoint

on:
  push:
    branches: [main]
    paths:
      - 'ea-council/**'

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Upload to SharePoint
        uses: actions/office365-sharepoint-upload@v1
        with:
          site-url: ${{ secrets.SHAREPOINT_SITE_URL }}
          client-id: ${{ secrets.SP_CLIENT_ID }}
          client-secret: ${{ secrets.SP_CLIENT_SECRET }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          source-path: './ea-council/'
          destination-library: 'EA Council Knowledge Base'
```

### Option B: Power Automate scheduled sync
- Trigger: Recurrence (daily)
- Action: Get files from GitHub API → upsert to SharePoint document library
- Simpler to configure; slower to propagate changes

### Option C: OneDrive sync client (manual)
- Map SharePoint library to a local folder
- Commit to Git and save locally — SharePoint syncs automatically
- Fine for small teams; doesn't scale to CI/CD pipelines

---

## Knowledge Refresh and Agent Re-indexing

When knowledge files are updated in SharePoint:

1. Copilot Studio re-indexes knowledge sources **automatically** (typically within 1–4 hours)
2. For immediate effect after a critical update: go to Agent → Knowledge Sources → select file → "Re-index now"
3. After significant changes to `policies.md` or `principles.md`, run a validation test (see `09-testing-and-validation.md`)

---

## ADR Output Storage

When the Chief Architect produces an accepted ADR:

1. Power Automate flow creates a new markdown file in `/outputs/adr/`
2. File is named: `ADR-{YYYY}-{NNN}-{kebab-title}.md`
3. `adr-register.md` is updated with the new entry
4. The ADR becomes a knowledge source for the Chief Architect (future decisions can reference it)

This creates a growing institutional memory — each ADR informs future deliberations.
