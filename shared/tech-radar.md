# Enterprise Technology Radar

## How to Read This Radar

| Ring | Meaning | Action |
|---|---|---|
| **ADOPT** | Proven; recommended for new and existing projects | Use confidently; no special approval needed |
| **TRIAL** | Promising; use in non-critical projects to build experience | Allowed with EA awareness; share learnings |
| **ASSESS** | Worth watching; not yet ready for production | Only in sandboxes/PoCs; brief EA before starting |
| **HOLD** | Avoid for new use; plan migration for existing | No new projects; existing use requires migration roadmap |

**Last updated:** 2026-Q1  
**Next review:** 2026-Q3  
> Update this file quarterly via the Technology Radar update process (see `guidelines.md` in Technology & Infrastructure)

---

## Cloud Platforms

| Technology | Ring | Notes |
|---|---|---|
| Microsoft Azure | **ADOPT** | Primary cloud platform |
| Azure Government / Sovereign | **ADOPT** | For regulated/public sector workloads |
| AWS | **TRIAL** | Allowed where Azure lacks capability or for multi-cloud resilience |
| Google Cloud Platform | **ASSESS** | Evaluate for specific ML/data workloads |
| On-premises self-managed | **HOLD** | No new workloads; migration required for existing |

## Compute & Containers

| Technology | Ring | Notes |
|---|---|---|
| Azure Kubernetes Service (AKS) | **ADOPT** | Default for containerized workloads |
| Azure Container Apps (ACA) | **ADOPT** | Preferred for new microservices (managed Kubernetes) |
| Azure Functions | **ADOPT** | Event-driven, stateless workloads |
| Azure App Service | **ADOPT** | Traditional web apps and APIs |
| Azure Virtual Machines | **HOLD** | Only for lift-and-shift legacy; migrate to containers |
| Docker | **ADOPT** | Standard container runtime |

## Integration & Messaging

| Technology | Ring | Notes |
|---|---|---|
| Azure Service Bus | **ADOPT** | Enterprise messaging; queues and topics |
| Azure Event Hubs | **ADOPT** | High-throughput event streaming |
| Azure API Management (APIM) | **ADOPT** | API gateway and developer portal |
| Azure Logic Apps | **ADOPT** | Low-code orchestration; SAP/ServiceNow connectors |
| Azure Event Grid | **ADOPT** | Event routing; serverless triggers |
| MuleSoft Anypoint | **TRIAL** | For complex enterprise integration patterns |
| Apache Kafka | **TRIAL** | For streaming at very high scale; evaluate vs Event Hubs |
| SOAP/WS-* web services | **HOLD** | No new interfaces; REST/AsyncAPI for new |
| FTP/SFTP file-based integration | **HOLD** | Legacy only; migrate to API or event patterns |

## Data & Analytics

| Technology | Ring | Notes |
|---|---|---|
| Microsoft Fabric | **ADOPT** | Unified analytics platform; replaces Synapse for new |
| Azure Data Lake Storage Gen2 | **ADOPT** | Standard for raw data storage |
| Azure SQL Database | **ADOPT** | Relational transactional data |
| Azure PostgreSQL Flexible Server | **ADOPT** | Open-source relational; preferred for new open-source workloads |
| Azure Cosmos DB | **ADOPT** | Multi-model NoSQL; global distribution |
| Azure Cache for Redis | **ADOPT** | Caching and session |
| Azure Synapse Analytics | **TRIAL** | Legacy path; new projects prefer Fabric |
| Power BI | **ADOPT** | Standard BI and reporting |
| Databricks | **TRIAL** | For advanced ML/data engineering workloads |
| On-premises SQL Server | **HOLD** | Migrate to Azure SQL or PostgreSQL |

## AI & Machine Learning

| Technology | Ring | Notes |
|---|---|---|
| Azure OpenAI Service | **ADOPT** | LLM platform; enterprise-grade, data residency |
| Azure Machine Learning | **ADOPT** | ML platform for training, registry, deployment |
| Microsoft Copilot Studio | **ADOPT** | Agentic AI and conversational UI |
| Azure AI Search | **ADOPT** | Vector search and RAG patterns |
| GitHub Copilot | **ADOPT** | Developer productivity; approved for code assist |
| Azure AI Foundry | **TRIAL** | Next-gen AI development hub; evaluate for agent orchestration |
| Hugging Face (self-hosted) | **TRIAL** | Open-source models; evaluate on Azure ML |
| OpenAI API (direct) | **HOLD** | Use Azure OpenAI instead for data residency compliance |

## Security

| Technology | Ring | Notes |
|---|---|---|
| Microsoft Entra ID (Azure AD) | **ADOPT** | Identity platform; SSO, MFA, PIM |
| Azure Key Vault | **ADOPT** | Secrets, keys, certificates |
| Microsoft Defender for Cloud | **ADOPT** | Cloud security posture management |
| Microsoft Sentinel | **ADOPT** | SIEM and SOAR |
| Azure Front Door + WAF | **ADOPT** | External-facing application protection |
| Conditional Access | **ADOPT** | Zero trust access control |
| Legacy username/password auth (no MFA) | **HOLD** | Migrate to Entra ID with MFA |

## DevOps & CI/CD

| Technology | Ring | Notes |
|---|---|---|
| GitHub Actions | **ADOPT** | CI/CD pipeline standard |
| Azure DevOps Pipelines | **ADOPT** | Legacy CI/CD; new projects prefer GitHub Actions |
| Terraform | **ADOPT** | IaC for multi-cloud |
| Azure Bicep | **ADOPT** | IaC for Azure-native workloads |
| ArgoCD | **TRIAL** | GitOps for Kubernetes deployments |
| Jenkins | **HOLD** | Migrate to GitHub Actions or Azure DevOps |

## Enterprise Applications

| Technology | Ring | Notes |
|---|---|---|
| SAP (S/4HANA Cloud) | **ADOPT** | ERP platform |
| SAP LeanIX | **ADOPT** | Enterprise Architecture repository (MCP available) |
| ServiceNow | **ADOPT** | ITSM, CMDB, GRC platform |
| Microsoft 365 | **ADOPT** | Productivity and collaboration platform |
| Microsoft Teams | **ADOPT** | Collaboration and communication |
| SharePoint Online | **ADOPT** | Document management and intranet |
