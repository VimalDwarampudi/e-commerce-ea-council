# Application Architecture Principles

## AA-PRIN-001: Fewer, Better Applications

A smaller, well-maintained portfolio is preferred over a large, fragmented one. Every addition to the portfolio must reduce complexity, not add to it, on a net basis.

---

## AA-PRIN-002: Lifecycle Discipline

Every application has a lifecycle. Ignoring end-of-life creates technical debt, security risk, and vendor dependency. Lifecycle management is not optional maintenance — it is risk management.

---

## AA-PRIN-003: Configurability Over Customization

Prefer configuring standard software to meet business needs over custom code. Custom code is a liability: it must be maintained, migrated, and documented. Customization is only justified for differentiating capabilities (see Business Architecture principles).

---

## AA-PRIN-004: Loose Coupling

Applications must not have hard dependencies on the internals of other applications. All cross-application interactions go through defined interfaces (APIs, events). This enables independent lifecycle management.

---

## AA-PRIN-005: Cloud-First for New Applications

New applications default to cloud-hosted (SaaS or PaaS). On-premises hosting requires explicit justification (data sovereignty, regulatory, latency, or exceptional cost argument).

---

## AA-PRIN-006: Rationalization Is Ongoing

Portfolio rationalization is not a one-time project. It is a continuous responsibility. Every ADR is an opportunity to reduce portfolio complexity.

---

## AA-PRIN-007: Transparency of Total Cost

Application decisions must be transparent about total cost of ownership. License cost alone is not the cost of an application — consider integration, support, training, migration, and exit costs.
