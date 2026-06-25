# Integration Architecture Policies

## IA-POL-001: No Undocumented Integrations [MANDATORY]

All production integrations must be documented in LeanIX as Interface / Data Flow records before go-live. Undocumented integrations discovered during a review must be documented as a prerequisite for endorsement of further changes.

---

## IA-POL-002: No Direct Database Integration [MANDATORY]

Applications must not integrate by reading or writing directly to another application's database. All cross-system data exchange must occur through defined APIs or event streams. Direct DB coupling is a hard veto.

---

## IA-POL-003: API-First for New Integrations

All new integrations must be designed API-first (REST or AsyncAPI specification written before implementation). File-based or database-level integrations are only permitted for legacy systems with no API capability and must include a migration plan.

---

## IA-POL-004: API Versioning [MANDATORY]

All APIs must implement semantic versioning. Breaking changes must be introduced as a new major version. The previous version must remain available for a minimum transition period of 6 months (or as contractually required).

---

## IA-POL-005: Integration Platform Standardization

New integrations must use the approved integration platform(s) listed in `shared/tech-radar.md`. Bespoke point-to-point integrations bypassing the integration platform require explicit Architecture approval and a migration plan.

---

## IA-POL-006: Event Schema Registry

All events published to the event bus must be registered in the schema registry with an owner and a version. Unregistered events are not approved for production use.

---

## IA-POL-007: API Security Baseline

All APIs must comply with the API security baseline defined in `agents/security/policies.md`. This includes authentication, rate limiting, and input validation as a minimum.

---

## IA-POL-008: Retry and Error Handling

All integrations must define and implement retry logic, dead-letter queue behaviour, and alerting for integration failures. "Best effort" with no error handling is not approved for business-critical flows.
