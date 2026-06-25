# Integration Architecture Principles

## IA-PRIN-001: Loose Coupling, High Cohesion

Systems must be integrated at the interface level, not the implementation level. Each system owns its data and exposes it through contracts. This enables independent evolution.

---

## IA-PRIN-002: Async by Default for Resilience

Asynchronous event-driven integration is preferred over synchronous request-reply for non-time-critical flows. Async integrations degrade gracefully under load; sync integrations cascade failures.

---

## IA-PRIN-003: Single Source of Truth per Data Domain

Data must have one authoritative source. Integrations move data from its source to consumers — they do not create competing sources of truth. Canonical data models define the contract.

---

## IA-PRIN-004: Integration Complexity Is a Cost

Every integration adds operational overhead: monitoring, versioning, error handling, documentation. This cost must be explicitly weighed. Prefer fewer, richer integrations over many thin ones.

---

## IA-PRIN-005: Observable Integrations

Every integration in production must be observable: metrics (volume, latency, error rate), tracing (request correlation IDs), and alerting (failure thresholds). Invisible integrations are unmanageable integrations.

---

## IA-PRIN-006: Design for Change

APIs and event contracts will change. Design for change from day one: versioning, deprecation lifecycle, and backward-compatibility commitments must be decided at design time, not retrofitted.

---

## IA-PRIN-007: Consumer-Driven Contracts

APIs and events are designed to serve their consumers, not the convenience of the producer. Consumer-driven contract testing ensures interfaces don't break consumers silently.
