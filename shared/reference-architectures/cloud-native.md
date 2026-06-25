# Reference Architecture: Cloud-Native Application on Azure

## Purpose

This reference architecture defines the standard pattern for deploying a new cloud-native application on Azure. Use as the baseline — adapt for workload-specific needs, but document deviations.

---

## Architecture Overview

```
                     ┌─────────────────────────────────────────┐
                     │           Azure Front Door + WAF         │
                     │    (Global load balancing + DDoS + WAF)  │
                     └──────────────────┬──────────────────────┘
                                        │ HTTPS
                                        ▼
                     ┌─────────────────────────────────────────┐
                     │         Azure API Management (APIM)      │
                     │   Auth | Rate limit | Routing | Logging  │
                     └────────┬──────────────────┬─────────────┘
                              │                  │
               ┌──────────────▼──┐     ┌─────────▼──────────────┐
               │  Frontend App   │     │   Backend API Layer     │
               │  (Static Web /  │     │  (Azure Container Apps  │
               │   React SPA)    │     │   or App Service)       │
               └─────────────────┘     └──────┬──────────┬───────┘
                                              │          │
                              ┌───────────────▼──┐   ┌───▼────────────────┐
                              │   Azure SQL /     │   │  Azure Service Bus  │
                              │   Cosmos DB       │   │  (async messaging)  │
                              └───────────────────┘   └────────────────────┘
                                                              │
                                              ┌───────────────▼────────┐
                                              │   Background Workers   │
                                              │  (Azure Functions /    │
                                              │   Container Jobs)      │
                                              └────────────────────────┘

     ──────────────────────── Shared Platform Services ────────────────────────
     │  Entra ID (Identity)  │  Key Vault (Secrets)  │  Log Analytics (Logs)  │
     │  Defender for Cloud   │  Azure Monitor         │  Application Insights  │
     ─────────────────────────────────────────────────────────────────────────
```

---

## Layer Specifications

### Layer 1: Edge (Azure Front Door + WAF)
- Global anycast routing for low-latency entry
- DDoS Protection Standard
- Web Application Firewall (WAF) with OWASP ruleset
- SSL/TLS termination; minimum TLS 1.2
- Origin health probes; automatic failover to secondary region

### Layer 2: API Gateway (APIM)
- OAuth 2.0 / OIDC token validation (Entra ID)
- Rate limiting per consumer identity
- Request/response transformation where needed
- API versioning enforcement
- Centralized API logging → Log Analytics
- Developer portal for internal consumers

### Layer 3: Application Layer
**Preferred compute:** Azure Container Apps (ACA)
- Managed Kubernetes; KEDA-based autoscaling
- Dapr sidecar for service-to-service and pub/sub (optional, evaluate per workload)
- Managed identity for downstream service authentication (no credentials in code)

**Alternative:** Azure App Service (for simpler web/API workloads without container requirements)

### Layer 4: Data Layer
- **Transactional data:** Azure SQL (serverless tier for variable loads) or PostgreSQL Flexible
- **Document/NoSQL:** Cosmos DB with appropriate consistency level
- **Cache:** Azure Cache for Redis (session, computed results, token caching)
- All databases: private endpoint only (no public internet access)
- All databases: managed identity authentication (no SQL passwords)

### Layer 5: Async Messaging
- **Azure Service Bus:** queues and topics for reliable messaging; dead-letter queue enabled
- **Azure Event Hubs:** high-volume event streaming (telemetry, audit streams)
- **Azure Event Grid:** lightweight event routing to Azure Functions or Logic Apps

### Layer 6: Shared Platform Services
These are enterprise shared services — not provisioned per application:
- **Entra ID:** SSO, MFA, PIM, Conditional Access, Managed Identities
- **Key Vault:** all secrets, certificates, keys (never in config or code)
- **Log Analytics Workspace:** centralized logs (all application + infrastructure logs)
- **Application Insights:** distributed tracing, performance monitoring, availability tests
- **Microsoft Defender for Cloud:** security posture, threat detection

---

## Security Baseline for This Pattern

- [ ] All traffic encrypted: TLS 1.2+ at every hop
- [ ] No public endpoints on databases or service bus (private endpoints)
- [ ] All application identities: Managed Identity (no service account passwords)
- [ ] Secrets: Key Vault references only
- [ ] APIM: OAuth 2.0 validation on all non-public APIs
- [ ] WAF: enabled with OWASP Core Rule Set
- [ ] NSGs: default deny inbound; explicit allow for required flows only
- [ ] Defender for Cloud: all relevant plans enabled
- [ ] PIM: all privileged roles on JIT access

---

## DR Configuration (Tier 2 default; adjust per workload)

| Component | DR Approach |
|---|---|
| Azure Front Door | Global by default — multi-region failover built in |
| APIM | Zone-redundant deployment |
| Container Apps | Zone-redundant within primary region; manual failover to secondary |
| Azure SQL | Active geo-replication to secondary region; auto-failover group |
| Service Bus | Premium tier with geo-disaster recovery |
| Key Vault | Soft delete + purge protection; geo-redundant by default |

---

## Deviation from This Pattern

Deviations must be documented in the ADR. Common justified deviations:

| Deviation | When Acceptable |
|---|---|
| Skip Front Door | Internal-only applications with no external consumers |
| Use Azure Functions instead of ACA | Event-driven, short-lived, stateless workloads |
| Use Cosmos DB instead of SQL | Truly unstructured or globally distributed data requirements |
| Add a second region (active-active) | Tier 1 mission-critical workloads |
