# Security Architecture Principles

## SEC-PRIN-001: Secure by Design

Security is a design requirement, not a feature added after development. Threat modeling happens at design time. Security controls are designed in — not bolted on.

---

## SEC-PRIN-002: Zero Trust

Never trust, always verify. Trust is not implied by network location, IP address, or previous authentication. Every request must authenticate and be authorized, every time.

---

## SEC-PRIN-003: Least Privilege

Every identity (human, service, machine) has only the access it needs to perform its function — no more. Privilege is granted explicitly and reviewed regularly.

---

## SEC-PRIN-004: Defense in Depth

No single security control is sufficient. Security is layered: network, platform, application, data, and identity controls each add a layer. An attacker who bypasses one layer must still overcome the others.

---

## SEC-PRIN-005: Assume Breach

Design systems assuming that a breach will occur. Minimize blast radius: segment networks, encrypt data at rest, limit access scope, maintain audit trails. Detect and respond, don't just prevent.

---

## SEC-PRIN-006: Shift Left on Security

Security review begins at architecture design, not after development. Finding a security flaw in design is 10x cheaper than finding it in production.

---

## SEC-PRIN-007: Transparency of Security Decisions

Security architecture decisions must be documented, communicated to stakeholders, and traceable. Security through obscurity is not a valid control.

---

## SEC-PRIN-008: Security Enables Business

Security exists to enable the business to operate safely — not to prevent change. Where security creates friction, it is our responsibility to find a secure path forward, not to say no without alternatives.
