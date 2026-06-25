# Security Architecture Policies

## SEC-POL-001: Authentication Required for All APIs [MANDATORY]

All APIs — internal and external — must require authentication. Anonymous access is not permitted for any API that handles non-public data. Approved authentication mechanisms: OAuth 2.0 / OIDC, mTLS, API keys (internal only, with rotation policy).

---

## SEC-POL-002: Encryption in Transit [MANDATORY]

All data in transit must be encrypted using TLS 1.2 or higher. TLS 1.0 and 1.1 are prohibited. HTTP (unencrypted) is not permitted for any internal or external data exchange.

---

## SEC-POL-003: Encryption at Rest for Confidential and Restricted Data [MANDATORY]

Data classified as Confidential or Restricted must be encrypted at rest using AES-256 or equivalent. Key management must use a centralized key management service — application-managed keys are not approved.

---

## SEC-POL-004: Zero Trust Network Access

No system should trust another system by virtue of network location alone. All system-to-system communication must use identity-based authentication, even within the internal network.

---

## SEC-POL-005: Least Privilege [MANDATORY]

All access controls (user, service account, API) must follow the principle of least privilege. Overprivileged accounts (admin access for operational tasks, broad read access for single-purpose integrations) are a policy violation.

---

## SEC-POL-006: API Security Baseline [MANDATORY for all APIs]

All APIs must implement:
- Authentication (SEC-POL-001)
- Authorization (role/scope-based)
- Input validation (reject malformed input at the gateway)
- Rate limiting (prevent DoS and brute force)
- Audit logging (who accessed what, when)

---

## SEC-POL-007: Third-Party Security Assessment

All third-party SaaS applications and vendors that access Confidential or Restricted data must complete a security assessment before go-live. Assessment must cover: data handling, access controls, breach notification procedures, certifications (ISO 27001, SOC 2 Type II).

---

## SEC-POL-008: Secrets Management [MANDATORY]

No secrets (passwords, API keys, certificates, tokens) may be stored in source code, configuration files committed to version control, or environment variables without a secrets management system. Approved: Azure Key Vault, HashiCorp Vault, AWS Secrets Manager, or equivalent.

---

## SEC-POL-009: Security Logging and Monitoring

All systems handling Confidential or Restricted data must emit security-relevant events (authentication failures, privilege escalation, data access anomalies) to the central SIEM. Log retention minimum: 12 months.

---

## SEC-POL-010: Patch Management

All production systems must have a defined patch management process. Critical security patches must be applied within 72 hours of release. High patches within 14 days. This applies to both cloud-managed and self-managed components.
