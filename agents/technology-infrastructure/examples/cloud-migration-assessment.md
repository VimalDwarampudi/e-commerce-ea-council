# Example: Technology & Infrastructure Assessment — Legacy App Cloud Migration

## Input (Request Summary)

> "We want to migrate our on-premises Order Management System (OMS) from a Windows Server 2016 VM to Azure. It runs on .NET Framework 4.7 and SQL Server 2017."

## Output (Technology & Infrastructure Assessment)

## Technology & Infrastructure Assessment

### Current Landscape
**ServiceNow CMDB query results:**
- CI: `oms-prod-vm-01` — Windows Server 2016, 16 vCPU, 64GB RAM, 2TB disk
- CI: `oms-db-01` — SQL Server 2017 Standard, 500GB data, 8 vCPU, 32GB RAM
- DR Tier: **Currently unassigned** — flagged as policy violation (TI-POL-006)
- Last incident (P2): 3 incidents in last 6 months — all disk-related on `oms-prod-vm-01`
- Relationships: Connected to SAP (order feed), Dynamics 365 (quote input), Reporting DB (read replica)

**LeanIX IT Components:**
- Microsoft Windows Server 2016: Lifecycle = **Phase Out** (Microsoft EOS: Oct 2027)
- .NET Framework 4.7: Lifecycle = Active (supported via Windows lifecycle)
- SQL Server 2017 Standard: Lifecycle = **Phase Out** (Microsoft EOS: Oct 2027)

**⚠️ Critical finding:** Both OS and DB are approaching end of support in October 2027 — 19 months from now. Migration must land before this date. TI-POL-005 violation risk.

### Platform Recommendation
**Recommended target: Azure — Replatform (Tier 2)**

Given the .NET Framework 4.7 dependency, a full containerization to AKS is not viable without refactoring. Recommend **Azure App Service (Windows)** for the application tier and **Azure SQL Managed Instance** for the database — this is the minimum-friction cloud path:

| Component | Current | Target | Migration Approach |
|---|---|---|---|
| Application | .NET 4.7 on Windows Server 2016 VM | Azure App Service (Windows P2v3) | Replatform — minimal code change |
| Database | SQL Server 2017 on VM | Azure SQL Managed Instance (Business Critical) | Lift database; use SSMA or backup/restore |
| Storage | Local disk (2TB) | Azure Files (Premium) + Azure Blob (archive) | Migrate with AzCopy |

**Why not AKS?** Containerizing a .NET Framework 4.7 application requires Windows containers on AKS — increased complexity, higher cost, and limited benefit over App Service for this workload. Revisit when/if the application is re-platformed to .NET 8 (see modernization roadmap below).

**Why SQL Managed Instance vs Azure SQL Database?** OMS uses SQL Server Agent jobs and linked server features — both require Managed Instance. Azure SQL Database (PaaS) would require application changes to remove these dependencies.

### Infrastructure Pattern
Follows the cloud-native reference architecture (`shared/reference-architectures/cloud-native.md`) with deviations noted:

- **Compute:** Azure App Service (Windows) — deviation from ACA standard (justified above)
- **Database:** Azure SQL Managed Instance — deviation from Azure SQL Database (justified above)
- **Networking:** Private endpoints for SQL MI; App Service VNet integration
- **Ingress:** Azure Application Gateway with WAF (OMS is internal-facing; Front Door not required)
- **Secrets:** Azure Key Vault for SQL connection strings and API keys
- **Monitoring:** Application Insights + Log Analytics (standard pattern — no deviation)

### Operational Considerations
**Availability:** App Service P2v3 with zone-redundancy = 99.95% SLA. SQL MI Business Critical = 99.99% SLA. Together: sufficient for a Tier 2 workload.

**DR Tier assignment:** Based on business criticality (order management is business-critical):
**DR Tier 2 — Business Critical (RTO < 4h, RPO < 1h)**
- App Service: zone-redundant in primary region; geo-restore from backup in secondary
- SQL MI: auto-failover group with secondary MI in paired region
- Target: Amsterdam (primary) → West Europe or UK South (secondary)

**Runbook requirements:** Failover procedure must be documented before go-live. Current OMS has no DR runbook — this is a pre-migration requirement.

**Team capability:** App Service and SQL MI are managed services. On-call team does not need Kubernetes or SQL DBA skills. Operational complexity is lower than current VM-based management.

### Technology Lifecycle
| Component | EOS Date | Status | Action |
|---|---|---|---|
| Windows Server 2016 | Oct 2027 | Phase Out | **Retired by migration** ✅ |
| SQL Server 2017 | Oct 2027 | Phase Out | **Retired by migration** ✅ |
| Azure App Service (Windows) | N/A (managed) | Active | Standard — no action |
| Azure SQL Managed Instance | N/A (managed) | Active | Standard — no action |
| .NET Framework 4.7 | Supported via App Service | Active | Flag for future modernization |

**Modernization roadmap note:** .NET Framework 4.7 is supported but not modern. Recommend a follow-up ADR to assess migration to .NET 8 within 24 months — this would enable Linux containers and reduce App Service cost by ~30%.

### Cost Estimate (indicative)
| Component | Current (estimated) | Azure Target | Delta |
|---|---|---|---|
| Compute | £1,200/mo (VM licensing + hardware) | £620/mo (App Service P2v3 × 2 zones) | −48% |
| Database | £800/mo (SQL Server Standard + HW) | £1,100/mo (SQL MI Business Critical — zone redundant) | +38% |
| Storage/network | £200/mo | £150/mo | −25% |
| **Total** | **~£2,200/mo** | **~£1,870/mo** | **−15%** |

Note: SQL MI Business Critical is more expensive than SQL Server Standard — but provides HA, auto-patching, and geo-replication that currently don't exist. TCO justification is resilience and lifecycle risk reduction, not raw cost.

### Recommendation
1. **Replatform** OMS to Azure App Service (Windows) + SQL Managed Instance.
2. Assign **DR Tier 2** and complete DR runbook before go-live.
3. Use this migration to resolve the End-of-Support risk for Windows Server 2016 and SQL Server 2017 (both October 2027 deadline).
4. Initiate a follow-up ADR for .NET 8 modernization within 6 months of successful migration.
5. Update ServiceNow CMDB and LeanIX IT Components after migration.

### Dependencies on Peer Domains
- **Integration Architecture:** Verify SAP order feed and Dynamics 365 connectivity to new Azure endpoints; update interface records.
- **Security Architecture:** Review NSG rules, App Service access restrictions, SQL MI firewall; ensure private endpoint configuration.
- **Application Architecture:** Confirm 7R decision (Replatform vs Refactor vs Re-architect) is aligned with the application roadmap.
