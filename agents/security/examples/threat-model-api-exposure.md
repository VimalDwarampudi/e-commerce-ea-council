# Example: Security Architecture Assessment — External Partner API Exposure

## Input (Request Summary)

> "We want to expose our Order Management API to external logistics partners so they can query order status and submit delivery confirmations. Authentication will use a shared API key distributed to all partners."

## Output (Security Architecture Assessment)

## Security Architecture Assessment

### Threat Model Summary
Data Flow Diagram elements identified:
- **External Entity:** 3 logistics partners (external — untrusted)
- **Process:** Order Management API (Azure App Service)
- **Data Store:** OMS Database (Azure SQL MI — Restricted: order data linked to customers)
- **Trust Boundary:** Internet → Azure API Management → OMS App Service

STRIDE analysis:

| Threat | Category | Probability | Impact | Severity | Mitigation |
|---|---|---|---|---|---|
| Partner A uses stolen API key to impersonate Partner B | Spoofing | HIGH | HIGH | **CRITICAL** | Per-partner OAuth 2.0 client credentials — no shared keys |
| Attacker intercepts shared API key from one partner's environment | Information Disclosure | HIGH | HIGH | **CRITICAL** | Per-partner OAuth 2.0; key rotation; TLS 1.2+ enforcement |
| Partner queries order data belonging to other partners | Information Disclosure | HIGH | HIGH | **CRITICAL** | Per-partner data scope in OAuth claims; API authorization checks |
| Malicious partner submits fraudulent delivery confirmations at scale | Tampering | MEDIUM | HIGH | HIGH | Per-partner rate limiting; delivery confirmation validation; audit log |
| Partner system sends malformed payloads to exploit parser | Tampering | MEDIUM | MEDIUM | HIGH | Input validation at API gateway; JSON schema enforcement |
| Overwhelming API with requests — denial of service | Denial of Service | MEDIUM | MEDIUM | HIGH | Rate limiting per partner identity at APIM; DDoS protection |
| Partner repudiates a delivery confirmation they submitted | Repudiation | LOW | HIGH | HIGH | Immutable audit log with partner identity + timestamp + payload hash |

### Policy Compliance Check

| Policy | Requirement | Status |
|---|---|---|
| SEC-POL-001 | Authentication required for all APIs | **FAIL** — shared API key is not per-consumer authentication |
| SEC-POL-002 | Encryption in transit (TLS 1.2+) | PASS — assuming APIM enforces TLS (confirm) |
| SEC-POL-003 | Encryption at rest (Restricted data) | PASS — Azure SQL MI encrypted at rest by default |
| SEC-POL-004 | Zero trust — no implicit trust by network | **FAIL** — shared key means all partners are implicitly trusted equally |
| SEC-POL-006 | API security baseline | **FAIL** — rate limiting not per-partner; no authorization scope |
| SEC-POL-007 | Third-party security assessment | CONDITIONAL — partners must complete security assessment before key issuance |

### Security Findings

**CRITICAL (must resolve before approval):**
- **C1: Shared API key is not acceptable.** A single shared key distributed to 3 external partners means: (1) any partner can impersonate any other partner; (2) rotating the key requires all partners to update simultaneously; (3) key leakage at one partner compromises all. This violates SEC-POL-001 and SEC-POL-004.
- **C2: No per-partner data scope.** Without per-partner authorization, Partner A could query Partner B's orders. Customer order data is Restricted — unauthorized exposure violates SEC-POL-003 principles and GDPR.

**HIGH (must resolve or accept with risk documentation):**
- **H1: Rate limiting not per partner.** Shared rate limits allow one misbehaving partner to exhaust capacity for others, and make abuse detection impossible.
- **H2: No audit trail of partner actions.** Delivery confirmation fraud cannot be investigated without an immutable log of who submitted what.
- **H3: No partner security baseline.** Partners will have access to Restricted order data. Their security posture is unknown.

**MEDIUM:**
- **M1: Input validation scope undefined.** Confirm JSON schema enforcement and payload size limits at APIM.
- **M2: TLS version enforcement.** Confirm APIM policy blocks TLS < 1.2. Default APIM allows older versions if not explicitly disabled.

### ⛔ SECURITY VETO ISSUED

**Condition:** Veto Condition 1 — mandatory policy violation (SEC-POL-001) with no in-scope mitigation in the current proposal. Veto Condition 3 — Restricted data (customer order records) exposed to unauthenticated parties (shared key = effectively unauthenticated for per-partner purposes).

**To lift this veto:**
1. Replace shared API key with **OAuth 2.0 Client Credentials flow** — one client ID and secret per partner, managed in Entra ID (External Identities or app registrations per partner)
2. Implement **per-partner OAuth scopes** in APIM policy: `orders:read:{partner-id}` and `deliveries:write:{partner-id}` — enforced at the API authorization layer
3. Implement **per-partner rate limiting** in APIM using subscription keys tied to partner identity
4. Implement **immutable audit log** of all API calls including partner identity, timestamp, operation, and payload hash — stored in Log Analytics (minimum 12 months)
5. Complete **security assessment** for each partner before credential issuance (SEC-POL-007)

**Alternative path (simpler for a small number of partners):** Azure API Management with per-partner subscriptions and APIM-managed OAuth. This is lower implementation complexity than a full Entra B2B setup and achieves the same security outcome for this use case.

### Recommended Mitigations
Full mitigation set addressing all CRITICAL and HIGH findings:

| Finding | Mitigation | Owner | Effort |
|---|---|---|---|
| C1, C2 | OAuth 2.0 per-partner client credentials in APIM | Integration Arch + IT Security | Medium |
| C2 | JWT claim-based authorization policy in APIM | Integration Arch | Low |
| H1 | Per-subscription rate limiting in APIM | Integration Arch | Low |
| H2 | APIM diagnostic logging → Log Analytics; immutable retention | Tech & Infra | Low |
| H3 | Partner security questionnaire; review before credential issuance | IT Security | Medium |
| M1 | APIM validate-content policy with JSON schema | Integration Arch | Low |
| M2 | APIM TLS policy: minimum TLS 1.2 | Tech & Infra | Low |

### Conditions for Approval
1. OAuth 2.0 per-partner authentication implemented and tested ✓ (lifts veto)
2. Per-partner authorization scopes enforced ✓ (lifts veto)
3. Security assessment completed for all 3 partners before go-live
4. Audit log implemented and confirmed flowing to Log Analytics
5. Partner security requirements documented in the partner onboarding process

## Key Points Illustrated
- STRIDE applied to every element in the data flow
- Every threat rated with probability + impact + severity
- Policy compliance check explicit (PASS/FAIL/CONDITIONAL per policy)
- Veto issued with precise condition and policy references
- Path forward provided — veto is not a dead end
- Mitigations are concrete and assigned
- Alternative (simpler) path offered to reduce implementation friction
