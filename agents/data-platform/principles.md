# Data & AI Architecture Principles

## DA-PRIN-001: Data Is a Strategic Asset

Data has value beyond its immediate use. It must be managed, curated, and governed accordingly. Treating data as an afterthought creates technical and regulatory debt.

---

## DA-PRIN-002: Single Source of Truth

Every data domain has one authoritative source. Duplication is permitted only in read-optimized copies with a clear synchronization strategy and a defined SoR.

---

## DA-PRIN-003: Data Ownership Is Business Ownership

Data is owned by the business domain that generates it, not by IT. IT provides the platforms; the business provides the ownership, definitions, and quality standards.

---

## DA-PRIN-004: Privacy by Design

Privacy is built into data architectures, not added later. Data minimization, purpose limitation, and access control are design requirements, not compliance add-ons.

---

## DA-PRIN-005: Trustworthy AI

AI systems must be explainable to their operators, fair in their outcomes, robust against adversarial inputs, and subject to human oversight. Opacity is not acceptable in high-stakes decisions.

---

## DA-PRIN-006: Data Quality Is Shared Responsibility

Data quality is not the responsibility of the data platform team alone. It is a shared responsibility between data owners (accuracy, completeness) and platform (reliability, availability).

---

## DA-PRIN-007: Interoperability Over Lock-In

Data platforms and AI/ML tooling must use open formats and standards where possible. Vendor-proprietary data formats that prevent portability are an architectural risk.

---

## DA-PRIN-008: Fail Safely in AI

AI systems that fail must fail safely. In high-stakes contexts, failure should defer to human judgment — not to a default model output. Design the failure mode before you design the happy path.
