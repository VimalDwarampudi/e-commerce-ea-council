# Technology & Infrastructure Policies

## TI-POL-001: Cloud-First [MANDATORY for new workloads]

All new workloads default to cloud-hosted deployment. On-premises hosting is only approved when:
- Data sovereignty or regulatory requirements explicitly prohibit cloud hosting, OR
- Latency requirements cannot be met by cloud, OR
- Exceptional cost analysis demonstrates on-premises TCO is lower over 5 years

All exceptions require documented approval from the Chief Architect.

---

## TI-POL-002: Approved Cloud Providers

New workloads must use approved cloud platforms listed in `shared/tech-radar.md`. Use of non-approved cloud providers requires Architecture approval and a migration plan.

---

## TI-POL-003: No Unmanaged Infrastructure [MANDATORY]

All production infrastructure must be registered in the ServiceNow CMDB within 5 business days of provisioning. Shadow infrastructure discovered in reviews must be registered as a prerequisite for endorsement.

---

## TI-POL-004: Infrastructure as Code

All cloud infrastructure for production workloads must be provisioned and managed as code (IaC). Manual console-provisioned infrastructure is not approved for production (exceptions: emergency break-glass, with post-incident remediation required).

---

## TI-POL-005: Technology End-of-Support

Production workloads must not run on technology components that have passed their vendor end-of-support date. Components within 12 months of end-of-support must have a documented remediation plan.

---

## TI-POL-006: DR Tier Assignment [MANDATORY]

Every workload must have an assigned DR tier with defined RTO and RPO targets. Workloads without DR tier assignment are not approved for production.

| DR Tier | RTO | RPO | Typical Use |
|---|---|---|---|
| Tier 1 — Mission Critical | < 1 hour | < 15 min | Customer-facing, revenue-generating, regulatory |
| Tier 2 — Business Critical | < 4 hours | < 1 hour | Key internal operations |
| Tier 3 — Important | < 24 hours | < 4 hours | Supporting business functions |
| Tier 4 — Standard | < 72 hours | < 24 hours | Non-critical internal tools |

---

## TI-POL-007: FinOps Tagging

All cloud resources must be tagged with: environment, application, cost centre, owner, and project. Untagged resources will be flagged in cost reviews and may be terminated after a warning period.

---

## TI-POL-008: Containerization Standard

New application workloads should be containerized (Docker) and orchestrated (Kubernetes or managed equivalent) unless the workload is a SaaS product. Legacy VM-based deployments must have a containerization roadmap for Tier 1 and Tier 2 workloads.
