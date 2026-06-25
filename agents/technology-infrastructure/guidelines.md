# Technology & Infrastructure Guidelines

## Cloud Platform Selection Guide

### Decision Framework

| Requirement | Azure | AWS | GCP | On-Prem |
|---|---|---|---|---|
| Deep Microsoft 365 / Entra ID integration | ✅ Preferred | — | — | — |
| SAP integration (BTP, Rise) | ✅ Strong | ✅ Strong | — | — |
| Multi-cloud or cloud-agnostic mandate | — | ✅ Broadest | ✅ Strong | — |
| Advanced ML/AI platform (Vertex, BigQuery) | — | — | ✅ Preferred | — |
| Data sovereignty (NL/EU) | ✅ EU regions | ✅ EU regions | ✅ EU regions | ✅ |
| Existing workloads already on platform | Favour that platform | | | |

> **Default: Azure** — given Microsoft Copilot Studio dependency and Entra ID usage. Deviations require explicit justification.

## Infrastructure Pattern Selection

### Compute Patterns

```
What is the workload?
├── Web API / Microservice → Container (AKS / ACA) or App Service
├── Event-driven function / Trigger → Azure Functions (serverless)
├── Batch processing → Azure Batch / Container Jobs
├── AI/ML training workload → Azure ML Compute
├── Legacy app (lift-and-shift) → Azure VM (with modernization roadmap)
└── SaaS product → No infrastructure owned (vendor managed)
```

### Storage Patterns

| Data Type | Recommended Service | Notes |
|---|---|---|
| Relational transactional | Azure SQL / PostgreSQL Flexible | Prefer managed over IaaS SQL |
| Document / JSON | Cosmos DB | Multi-region, multi-model |
| Large-scale analytics | Azure Synapse / Fabric | Lakehouse pattern |
| Object / blob | Azure Blob Storage | Tiered: hot/cool/archive |
| Messaging / events | Azure Service Bus / Event Hubs | Bus for queues; Event Hubs for streaming |
| Cache | Azure Cache for Redis | Session, computed data, API responses |
| Secrets | Azure Key Vault | Never store secrets in config/code |

## DR Tier Design Patterns

### Tier 1 — Mission Critical (RTO < 1h, RPO < 15min)
- Active-active deployment across two Azure regions
- Geo-redundant storage with automatic failover
- Traffic Manager or Front Door for automatic rerouting
- Automated failover tested quarterly
- Zero manual steps in the primary failover path

### Tier 2 — Business Critical (RTO < 4h, RPO < 1h)
- Active-passive with warm standby in secondary region
- Automated database replication (async)
- Manual failover procedure < 30 min
- Failover tested bi-annually

### Tier 3 — Important (RTO < 24h, RPO < 4h)
- Single region with cross-zone redundancy
- Automated backup to secondary region (scheduled)
- Failover via redeployment from IaC + data restore
- Tested annually

### Tier 4 — Standard (RTO < 72h, RPO < 24h)
- Single region, single zone
- Daily backup to geo-redundant storage
- Restore tested annually

## Infrastructure as Code Standards

All IaC must follow these conventions:

```
infrastructure/
├── modules/           # Reusable, parameterized modules
│   ├── networking/
│   ├── compute/
│   ├── storage/
│   └── security/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── prod/
├── pipelines/         # CI/CD pipeline definitions
└── README.md          # Architecture diagram + deployment instructions
```

**Tooling standard:** Bicep (Azure preferred) or Terraform (for multi-cloud)  
**State management:** Remote state in Azure Storage with state locking  
**Secrets in IaC:** References to Key Vault only — no inline secrets  
**Drift detection:** Scheduled plan/diff runs to detect manual changes  

## FinOps Tagging Standard

All Azure resources must carry these tags:

| Tag | Values | Required |
|---|---|---|
| `environment` | dev / staging / prod | ✅ |
| `application` | LeanIX application ID or short name | ✅ |
| `cost-centre` | Finance cost centre code | ✅ |
| `owner` | Email address of technical owner | ✅ |
| `project` | Project or initiative name | ✅ |
| `dr-tier` | 1 / 2 / 3 / 4 | ✅ |
| `data-classification` | public / internal / confidential / restricted | ✅ |

## Technology Lifecycle Review Process

Conduct this review quarterly as part of the tech radar update:

1. Pull all IT Components from LeanIX
2. Check vendor end-of-support dates
3. Flag components within 12 months of end-of-support → raise as HIGH finding
4. Flag components past end-of-support → raise as CRITICAL finding (policy violation)
5. For each flagged component: identify affected applications and assign migration timeline
6. Update LeanIX lifecycle state and create ServiceNow change request for remediation

## Observability Standards

Every production workload must implement the three pillars:

| Pillar | Tooling (Azure) | Minimum Requirements |
|---|---|---|
| **Metrics** | Azure Monitor / Application Insights | CPU, memory, request rate, error rate, latency (p50/p95/p99) |
| **Logs** | Log Analytics Workspace | Structured JSON logs; application + infrastructure logs in same workspace |
| **Traces** | Application Insights / OpenTelemetry | Distributed tracing with correlation IDs across all service boundaries |

**Alerting baseline:**
- Error rate > threshold → PagerDuty / ServiceNow incident
- Latency p99 > SLA → Warning alert
- Resource exhaustion (CPU > 80%, disk > 85%) → Warning + auto-scale trigger
- Security events → SIEM (separate pipeline)
