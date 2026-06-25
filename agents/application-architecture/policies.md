# Application Architecture Policies

## AA-POL-001: Portfolio Registration [MANDATORY]

Every production application must be registered in LeanIX. Unregistered applications (shadow IT) are not endorsed for integration, infrastructure, or data sharing until registered.

---

## AA-POL-002: Lifecycle Gate [MANDATORY]

Applications with lifecycle state **End of Life** may not receive new investment (features, integrations, migrations onto them) unless a lifecycle extension is formally approved with an exit plan attached.

---

## AA-POL-003: Redundancy Check Before New Application

No new application may be introduced if an existing Active application already covers ≥70% of the same functional scope, unless a rationalization plan is included that retires the existing application within 24 months.

---

## AA-POL-004: Tech Radar Compliance

Applications built on or integrated with technologies rated **HOLD** on the tech radar must include a migration timeline to a supported technology. New projects may not start on HOLD technologies.

---

## AA-POL-005: SaaS Governance

All SaaS applications must be:
- Registered in LeanIX before go-live
- Assessed for security compliance before connecting to enterprise data
- Subject to an annual vendor review (continued fit, commercial terms, security posture)

---

## AA-POL-006: Fit Score Threshold

Applications with a combined Business Fit + Technical Fit score below **2.5/5** must be reviewed for rationalization (Migrate / Eliminate in Gartner TIME). The Application Architecture agent will flag these applications in any review that touches them.

---

## AA-POL-007: Application Ownership

Every Active application must have a named Application Owner (business) and a named Technical Owner (IT) in LeanIX. Applications without owners are flagged as governance gaps in every ADR.

---

## AA-POL-008: Modernization Strategy Requirement

Any application older than 7 years on a deprecated technology stack must have a documented modernization strategy (one of the 7Rs) before new features are endorsed.
