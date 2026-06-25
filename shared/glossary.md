# EA Council Glossary

Common terms used across all council agents. Consistent terminology prevents miscommunication between agents and with human sponsors.

---

## A

**ADR (Architecture Decision Record)** — A document that captures an architecture decision, the context in which it was made, the options considered, the rationale for the chosen option, and the trade-offs accepted.

**Application** — A software system that provides business functionality. Registered in LeanIX as an Application fact sheet.

**Application Portfolio** — The full inventory of applications used by the organization, managed in LeanIX.

**API (Application Programming Interface)** — A defined contract through which systems exchange data or trigger actions. The preferred integration mechanism for all new interfaces.

---

## B

**Business Capability** — A particular ability or capacity a business possesses to achieve a specific purpose or outcome. Registered in LeanIX. Independent of how it is implemented (people, process, technology).

**Business Fit** — A score (1–5) assessing how well an application continues to serve the business need it was acquired for.

---

## C

**CMDB (Configuration Management Database)** — ServiceNow's authoritative record of IT infrastructure configuration items (CIs) and their relationships.

**Cross-Cut Agent** — An agent (Security, Risk & Compliance, Red Team) that reviews proposals across all domains rather than owning a specific domain.

---

## D

**Data Classification** — The assignment of a sensitivity level (Public / Internal / Confidential / Restricted) to data, governing how it must be protected and shared.

**Data Object** — A logical representation of a business data entity (e.g., Customer, Order, Product). Registered in LeanIX as a Data Object fact sheet.

**DPIA (Data Protection Impact Assessment)** — A GDPR-required assessment for processing activities that may result in high risk to individuals.

**Domain Agent** — An agent specializing in a specific architecture domain (Business, Application, Integration, Technology & Infrastructure, Data & AI).

**DR Tier** — Disaster Recovery tier classification (1–4) defining the RTO and RPO targets for a workload.

---

## E

**EU AI Act** — EU regulation classifying AI systems by risk level (Unacceptable / High / Limited / Minimal) with corresponding obligations.

---

## F

**Fact Sheet** — LeanIX's term for a record in the EA repository. Fact Sheet types include: Application, IT Component, Business Capability, Interface, Data Object, User Group.

**Functional Fit** — How well an application's features match the current functional requirements of its users.

---

## I

**Impact Level** — Classification of an architecture decision's scope and risk: Minor / Standard / Major / Critical. Governs which agents are engaged and what outputs are required.

**Interface** — A LeanIX fact sheet documenting a data flow or integration between two applications.

**IT Component** — A LeanIX fact sheet representing a technology component (framework, platform, product) underlying an application.

---

## L

**LeanIX** — The organization's Enterprise Architecture repository (SAP LeanIX). The system of record for applications, capabilities, data objects, interfaces, and technology components. Accessible via MCP.

**Lifecycle State** — The current operational status of an application or IT component in LeanIX: Active / Phase Out / End of Life / Planned.

---

## M

**MCP (Model Context Protocol)** — The protocol used to expose LeanIX data to AI agents via tool calls, enabling real-time querying of the architecture repository.

**MLOps** — The practice of applying DevOps disciplines to machine learning model development, deployment, and monitoring.

---

## O

**Orchestrator** — The Chief Architect agent. Receives requests, coordinates domain agents, synthesizes outputs, and produces final decisions.

---

## P

**Policy Exception** — A formally approved deviation from a mandatory policy, with documented business justification, compensating controls, approval, and expiry.

**Principle** — A general rule that guides architecture decisions across the enterprise. Applied when resolving conflicts between competing options.

---

## R

**Red Team** — The adversarial challenge agent. Reviews council outputs to identify weaknesses, blind spots, and unvalidated assumptions.

**RPO (Recovery Point Objective)** — The maximum acceptable data loss in time. "How old can our backup be when we restore?"

**RTO (Recovery Time Objective)** — The maximum acceptable time to restore a system after failure. "How long can this be down?"

---

## S

**ServiceNow** — The organization's ITSM and GRC platform. Sources of truth for: CMDB, change requests, incidents, risk register, policy exceptions.

**System of Record (SoR)** — The single authoritative source for a data domain. All other copies of that data are derived from the SoR.

---

## T

**Technical Fit** — A score (1–5) assessing how well an application's technology stack aligns with current standards and maintainability expectations.

**Tech Radar** — The organization's classification of technologies by adoption guidance: ADOPT / TRIAL / ASSESS / HOLD.

**TIME Model** — Gartner application portfolio framework: Tolerate / Invest / Migrate / Eliminate.

---

## V

**Value Stream** — An end-to-end sequence of activities that delivers value to a customer (internal or external). Used to assess the business impact of architecture changes.

**Veto** — A formal halt issued by the Security agent when a proposal violates a mandatory security policy with no available mitigation. Requires Chief Architect acknowledgment and either remediation or human escalation.
