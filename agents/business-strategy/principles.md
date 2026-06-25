# Business Architecture Principles

## BA-PRIN-001: Business Capability Before Technology

Technology decisions are derived from business capability needs, not the reverse. We do not adopt technology and then find use cases for it.

**Implication:** New technology proposals must start with the business capability gap or improvement they address.

---

## BA-PRIN-002: Differentiate the Differentiators

Invest architecture effort and build/customization in capabilities that provide competitive differentiation. Standardize and commoditize everything else.

**Implication:** Custom development and deep configuration are reserved for differentiating capabilities. Everything else follows market standards.

---

## BA-PRIN-003: Value Stream Integrity

Architecture changes must not break the continuity of a value stream. Each change is assessed for its impact on end-to-end flow, not just the component being changed.

**Implication:** Point solutions that optimize one step at the expense of the whole are not endorsed.

---

## BA-PRIN-004: Business Agility Over Technical Purity

When a technically "perfect" solution reduces business agility (speed of change, speed of delivery), prefer the more agile solution with documented technical trade-offs.

**Implication:** Pragmatism is an architecture value. Perfect is the enemy of done.

---

## BA-PRIN-005: Explicit Over Implicit

Business capabilities, ownership, and strategic alignment must be explicit and documented in LeanIX. Implicit understanding locked in people's heads is an organizational risk.

**Implication:** Any undocumented capability surfaced during a review must be documented before the ADR is finalized.

---

## BA-PRIN-006: Architecture Enables Strategy, Not the Other Way Around

The enterprise architecture exists to serve the strategy. When strategy changes, architecture must adapt — not resist change to protect existing investments.

**Implication:** Sunk cost is not a valid architecture argument.
