# Security Architecture Guidelines

## Threat Modeling — STRIDE Methodology

Run a STRIDE analysis on every new system, integration, or significant change. Structure it as follows:

### Step 1: Build a Data Flow Diagram (DFD)
Identify:
- **Processes** (circles) — code that transforms data
- **Data Stores** (parallel lines) — databases, files, caches
- **External Entities** (rectangles) — users, external systems
- **Data Flows** (arrows) — data moving between components
- **Trust Boundaries** (dashed lines) — where privilege or security context changes

### Step 2: Apply STRIDE per Element

| Element Type | Applicable STRIDE Threats |
|---|---|
| Process | S, T, R, I, D, E (all) |
| Data Store | T, R, I (Tampering, Repudiation, Info Disclosure) |
| Data Flow | T, I, D (Tampering, Info Disclosure, DoS) |
| External Entity | S, R (Spoofing, Repudiation) |

### STRIDE Quick Reference

| Letter | Threat | Violated Property | Example |
|---|---|---|---|
| **S** | Spoofing | Authentication | Attacker impersonates a user or service |
| **T** | Tampering | Integrity | Attacker modifies data in transit or at rest |
| **R** | Repudiation | Non-repudiation | User denies performing an action |
| **I** | Information Disclosure | Confidentiality | Data leaks to unauthorized party |
| **D** | Denial of Service | Availability | System made unavailable |
| **E** | Elevation of Privilege | Authorization | User gains permissions they shouldn't have |

### Step 3: Rate Each Threat (DREAD-lite)

| Rating | Probability | Impact | Severity |
|---|---|---|---|
| HIGH | Easily exploitable, known attack patterns | Business disruption, data breach, regulatory penalty | CRITICAL or HIGH |
| MEDIUM | Requires some skill or access | Partial exposure, degraded service | HIGH or MEDIUM |
| LOW | Requires significant effort or insider access | Limited scope | MEDIUM or LOW |

### Step 4: Define Mitigations

For every HIGH and CRITICAL finding, define a concrete mitigation:

```
Threat: [STRIDE category — description]
Severity: CRITICAL / HIGH / MEDIUM / LOW
Mitigation: [Specific control — e.g., "Implement OAuth 2.0 PKCE flow; validate tokens at API gateway"]
Control Type: Preventive / Detective / Corrective
Owner: [Team or role responsible]
Status: Proposed / Accepted / Implemented / Accepted Risk
```

## Zero Trust Architecture Guidelines

### Core Principles in Practice

1. **Identity is the perimeter** — Entra ID (Azure AD) is the authentication authority for all human and service identities
2. **Device posture** — Conditional Access policies; non-compliant devices denied access to sensitive resources
3. **Least privilege access** — PIM (Privileged Identity Management) for admin roles; just-in-time access
4. **Microsegmentation** — Network Security Groups at subnet level; no flat east-west traffic in production
5. **Session monitoring** — UEBA (User and Entity Behaviour Analytics); anomaly detection on privileged accounts

### Service-to-Service Authentication

| Scenario | Recommended Approach |
|---|---|
| Azure service to Azure service | Managed Identity (no credentials) |
| External API consumer | OAuth 2.0 Client Credentials flow |
| On-premises to Azure | Hybrid connection with mTLS + certificate |
| Third-party SaaS webhook inbound | HMAC signature validation on webhook payload |
| Legacy system with no OAuth support | API gateway with API key rotation (transitional only) |

## API Security Checklist

For every API entering production:

- [ ] **Authentication**: OAuth 2.0 / OIDC or API key (internal only) — no anonymous access for non-public data
- [ ] **Authorization**: Role/scope-based; principle of least privilege on API scopes
- [ ] **Input validation**: All inputs validated at gateway (schema, size, type, encoding)
- [ ] **Output encoding**: Responses sanitized — no internal stack traces, system paths, or secrets in error responses
- [ ] **Rate limiting**: Configured at API gateway level per consumer identity
- [ ] **TLS**: TLS 1.2+ enforced; HSTS header set
- [ ] **CORS**: Allowlist only; wildcard (`*`) not permitted for authenticated APIs
- [ ] **Audit logging**: Authentication events, authorization failures, and data access logged to SIEM
- [ ] **Secrets**: No secrets in URLs, query parameters, or response bodies
- [ ] **Dependency scan**: All API dependencies scanned for known CVEs before deployment

## Security Review Levels by Impact

| Impact Level | Security Review Required |
|---|---|
| **Minor** | Quick checklist review; document in ADR |
| **Standard** | Full STRIDE threat model; policy compliance check |
| **Major** | Full STRIDE + penetration test requirement before go-live |
| **Critical** | Full STRIDE + pen test + external security audit + sign-off from CISO |

## Cloud Security Posture Checklist (Azure)

- [ ] Azure Defender for Cloud enabled and baseline recommendations resolved
- [ ] All subscriptions enrolled in Microsoft Defender plans appropriate to workload
- [ ] Azure Policy applied: deny non-compliant resource configurations
- [ ] Network Security Groups: default-deny inbound; explicit allowlist only
- [ ] No storage accounts with public blob access (unless explicitly required)
- [ ] Key Vault: soft delete + purge protection enabled; access via RBAC not vault access policies
- [ ] Log Analytics: all resource diagnostic logs forwarded
- [ ] Privileged roles: no permanent assignments; PIM for all privileged roles
- [ ] External-facing resources: behind Azure Front Door / Application Gateway with WAF
