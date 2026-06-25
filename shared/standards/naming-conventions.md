# Naming Conventions

Consistent naming across LeanIX, ServiceNow, Azure, and documentation ensures discoverability and reduces ambiguity.

---

## LeanIX Naming Conventions

### Applications
Format: `[BusinessUnit]-[Function]-[TechnologyHint]`  
All lowercase with hyphens. Business unit codes defined in the LeanIX Business Unit taxonomy.

Examples:
- `hr-recruitment-successfactors`
- `fin-reporting-sap-analytics`
- `ops-cmdb-servicenow`
- `crm-sales-dynamics365`

### IT Components
Format: `[Vendor]-[Product]-[Version or Edition]`

Examples:
- `microsoft-azure-sql`
- `sap-s4hana-cloud`
- `confluent-kafka`
- `hashicorp-terraform`

### Interfaces / Data Flows
Format: `[SourceApp]→[TargetApp]:[DataDomain]:[Protocol]`

Examples:
- `hr-recruitment-successfactors→fin-hrmaster-sap:employee:api-rest`
- `crm-sales-dynamics365→fin-reporting-sap-analytics:opportunity:event-async`

### Data Objects
Format: `[Domain].[Entity]` (PascalCase)

Examples:
- `Customer.Profile`
- `Employee.Contract`
- `Finance.Invoice`
- `Logistics.Shipment`

---

## ADR Naming

Format: `ADR-[YYYY]-[NNN]-[kebab-case-short-title].md`

Examples:
- `ADR-2026-001-migrate-hr-to-successfactors.md`
- `ADR-2026-002-event-driven-order-processing.md`

ADR numbers are sequential within a year. Maintained in a register in `outputs/adr-register.md`.

---

## Azure Resource Naming

Format: `[workload]-[env]-[resourcetype]-[instance]`  
Region and subscription are encoded in tags, not names, to avoid name length limits.

| Resource Type | Abbreviation | Example |
|---|---|---|
| Resource Group | `rg` | `hr-recruitment-prod-rg` |
| App Service | `app` | `hr-recruitment-prod-app-01` |
| Azure SQL | `sql` | `hr-recruitment-prod-sql-01` |
| Storage Account | `st` | `hrrecruitmentprodst01` (no hyphens; max 24 chars) |
| Key Vault | `kv` | `hr-recruitment-prod-kv` |
| Service Bus | `sb` | `hr-recruitment-prod-sb` |
| Container App | `ca` | `hr-recruitment-prod-ca-api` |
| AKS Cluster | `aks` | `hr-recruitment-prod-aks` |
| API Management | `apim` | `enterprise-prod-apim` (shared instance) |
| Log Analytics | `law` | `enterprise-prod-law` (shared) |

Environments: `dev` / `staging` / `prod`

---

## API and Event Naming

### REST API endpoints
Format: `/{resource-plural}/{id}/{sub-resource}`  
All lowercase, hyphens for multi-word resources.

Examples:
- `GET /customers/{id}`
- `POST /purchase-orders`
- `GET /customers/{id}/contracts`

### Event / Message types
Format: `[Domain].[Entity].[EventType]` (PascalCase)

Examples:
- `HR.Employee.Hired`
- `Finance.Invoice.Approved`
- `CRM.Opportunity.Closed`
- `Logistics.Shipment.Dispatched`

Event type naming rules:
- Use past tense for domain events (something happened)
- Use imperative for commands (do something): `HR.Employee.Onboard`
- Never use generic names like `Update`, `Change`, `Event`

---

## ServiceNow Naming

### Change Requests
Subject format: `[Action] [System/Component]: [Brief description]`

Examples:
- `Deploy HR Recruitment API v2.1: Add candidate scoring endpoint`
- `Migrate Finance Reporting DB: Upgrade Azure SQL to v12`
- `Decommission: CRM-Legacy-Siebel application`

### Configuration Items (CIs)
Follow the CMDB CI class naming standards defined in the ServiceNow CMDB baseline configuration. Application CIs must match the LeanIX application short name.

---

## Documentation Files

Markdown files: `kebab-case-descriptive-name.md`  
Never use spaces in filenames.  
Directories: `kebab-case` for multi-word names.
