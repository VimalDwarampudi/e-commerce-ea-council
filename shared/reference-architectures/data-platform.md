# Reference Architecture: Enterprise Data Platform

## Purpose

This reference architecture defines the standard patterns for building and evolving the enterprise data platform on Azure. It covers the full spectrum from operational data to analytics, AI/ML, and data mesh adoption.

---

## Architecture Overview: Medallion Lakehouse on Microsoft Fabric

```
                         ┌─────────────────────────────────────────────────────┐
                         │              DATA SOURCES                            │
                         │                                                       │
                         │  SAP S/4HANA  │  Dynamics 365  │  Custom Apps        │
                         │  ServiceNow   │  External APIs  │  IoT / Streaming    │
                         └──────┬──────────────┬────────────────┬───────────────┘
                                │ CDC / ADF     │ Event Hubs     │ Batch / API
                                ▼              ▼                ▼
                    ┌────────────────────────────────────────────────┐
                    │         INGESTION LAYER                         │
                    │  Azure Data Factory  │  Azure Event Hubs        │
                    │  Logic Apps (SAP)    │  Azure Stream Analytics  │
                    └───────────────────────────┬────────────────────┘
                                                │
                                                ▼
                    ┌────────────────────────────────────────────────┐
                    │    BRONZE LAYER — Raw / Landing Zone            │
                    │         Azure Data Lake Storage Gen2            │
                    │   Exact copy of source data; immutable;         │
                    │   partitioned by source + date                  │
                    └───────────────────────────┬────────────────────┘
                                                │ Fabric Pipelines / Spark
                                                ▼
                    ┌────────────────────────────────────────────────┐
                    │    SILVER LAYER — Cleansed / Conformed          │
                    │         Microsoft Fabric Lakehouse              │
                    │   Validated, deduplicated, schema-enforced;     │
                    │   Delta Lake format; business keys standardized │
                    └───────────────────────────┬────────────────────┘
                                                │ Fabric Notebooks / dbt
                                                ▼
                    ┌────────────────────────────────────────────────┐
                    │    GOLD LAYER — Business / Serving              │
                    │     Microsoft Fabric Warehouse / Semantic Model │
                    │   Domain-oriented data products;                │
                    │   star schemas; aggregated; ML feature stores   │
                    └─────────┬──────────────────────────┬───────────┘
                              │                          │
                  ┌───────────▼────────┐    ┌────────────▼──────────┐
                  │   Power BI Reports  │    │   AI / ML Platform    │
                  │   (Fabric Direct   │    │   Azure ML Studio     │
                  │    Lake connection) │    │   OpenAI Fine-tuning  │
                  └────────────────────┘    └───────────────────────┘

     ────────────────────────── PLATFORM SERVICES ───────────────────────────
     │  Microsoft Purview (Governance)  │  Fabric Data Catalog               │
     │  Azure Key Vault (Encryption)    │  Entra ID (Access Control)          │
     │  Log Analytics (Audit Trail)     │  Microsoft Defender (Security)      │
     ─────────────────────────────────────────────────────────────────────────
```

---

## Layer Specifications

### Bronze Layer — Raw Landing Zone
**Technology:** Azure Data Lake Storage Gen2 (ADLS Gen2)  
**Format:** Source-native (JSON, Parquet, CSV, Avro — no transformation)  
**Retention:** Configurable per data domain (typically 2–7 years; longer for regulated data)  
**Access:** Restricted to platform engineers and automated pipelines. No direct BI access.  
**Partitioning:** `/bronze/{source_system}/{entity}/{year}/{month}/{day}/`

**What happens here:**
- Data lands exactly as received from source systems
- No transformation, no cleansing, no schema enforcement
- Immutable — existing files never modified (append-only pattern)
- Full audit trail of every ingest event

---

### Silver Layer — Cleansed & Conformed
**Technology:** Microsoft Fabric Lakehouse (Delta Lake tables)  
**Format:** Delta Lake (ACID transactions, time travel, schema enforcement)  
**Transformations applied:**
- Deduplication (using business keys)
- Data type standardization
- NULL handling and data quality checks
- Business key normalization (e.g., customer ID formats unified)
- PII tokenization / pseudonymization where required

**Quality gates (must pass before silver):**
- Completeness: critical fields non-null ≥ 95%
- Uniqueness: primary key uniqueness enforced
- Referential integrity: foreign key checks where applicable
- Range checks: numeric fields within valid business ranges
- Failed rows: quarantined to DLQ table with rejection reason

---

### Gold Layer — Business Serving
**Technology:** Microsoft Fabric Warehouse + Semantic Models (Power BI datasets)  
**Pattern:** Domain-oriented data products  
**Consumers:** Power BI, Azure ML, downstream applications via API

**Data product structure:**
```
/gold/
├── finance/
│   ├── dim_customer
│   ├── dim_product
│   ├── fact_revenue
│   └── agg_monthly_revenue_by_segment
├── hr/
│   ├── dim_employee
│   ├── dim_organisation
│   └── fact_headcount_snapshot
├── supply_chain/
│   ├── dim_supplier
│   ├── fact_purchase_order
│   └── fact_inventory_movement
└── _platform/
    ├── dim_date
    ├── dim_time
    └── meta_data_quality_scores
```

---

## Data Mesh Overlay (for large, multi-domain organisations)

When the central platform team cannot scale to serve all domains, overlay a data mesh operating model:

```
┌─────────────────────────────────────────────────────────┐
│                  DATA MESH OPERATING MODEL               │
│                                                          │
│  Domain: Finance        Domain: HR         Domain: SCM  │
│  ┌────────────┐        ┌────────────┐     ┌──────────┐  │
│  │ Finance    │        │ HR Data    │     │ SCM Data │  │
│  │ Data       │        │ Product    │     │ Product  │  │
│  │ Product    │        │ Team       │     │ Team     │  │
│  │ Team       │        └─────┬──────┘     └────┬─────┘  │
│  └─────┬──────┘              │                 │        │
│        └────────────┬────────┘                 │        │
│                     ▼                           │        │
│          ┌──────────────────────────────────────┘        │
│          │       Fabric Self-Serve Data Platform         │
│          │  (Shared infra, governance, standards)         │
│          └──────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────┘
```

**Data Mesh adoption checklist (per domain):**
- [ ] Domain data product owner identified (business role)
- [ ] Data products catalogued with SLA (freshness, availability, quality)
- [ ] Schema published to Fabric catalog
- [ ] Access request workflow in place
- [ ] Quality scores published and monitored
- [ ] Lineage documented (source → gold)

---

## Governance Layer — Microsoft Purview

| Capability | Configuration |
|---|---|
| **Data Catalog** | Auto-scan Fabric, ADLS, Azure SQL; classify automatically |
| **Data Classification** | Built-in + custom classifiers for PII, financial, health data |
| **Data Lineage** | Auto-captured from ADF, Fabric pipelines, dbt |
| **Access Policies** | Purview access policies for ADLS Gen2 (attribute-based) |
| **Sensitivity Labels** | Microsoft 365 labels applied to data assets (M365 E5) |
| **Data Map** | Visualise data estate; link to LeanIX Data Objects |

**Purview ↔ LeanIX sync:** Map Purview data assets to LeanIX Data Object fact sheets using the `u_purview_asset_id` custom field. This connects the technical data catalog (Purview) to the business data landscape (LeanIX).

---

## AI/ML Platform — Azure Machine Learning

```
┌────────────────────────────────────────────────────────┐
│                  Azure ML Platform                      │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Experiment  │  │   Model      │  │  Endpoint    │  │
│  │  Tracking   │  │   Registry   │  │  (Managed /  │  │
│  │  (MLflow)   │  │              │  │  Batch /     │  │
│  └──────┬───────┘  └──────┬───────┘  │  Serverless) │  │
│         │                 │          └──────┬───────┘  │
│         └─────────────────┘                 │          │
│                                             │          │
│  ┌──────────────────────────────────────────┘          │
│  │  Responsible AI Dashboard                           │
│  │  (Fairness, Explainability, Error Analysis)         │
│  └──────────────────────────────────────────────────── │
└────────────────────────────────────────────────────────┘
         │ Training data                    │ Predictions
         ▼                                  ▼
   Fabric Gold Layer                 Consumer Applications
   (Feature Store)
```

**Model governance requirements per EU AI Act risk level:**

| Requirement | Minimal Risk | Limited Risk | High Risk |
|---|---|---|---|
| Model card / documentation | Recommended | Required | Required |
| Training data provenance | Recommended | Required | Required + auditable |
| Bias / fairness testing | Recommended | Required | Required + continuous |
| Human oversight mechanism | Optional | Optional | **Mandatory** |
| Conformity assessment | No | No | Yes (internal or third-party) |
| EU database registration | No | No | Yes |
| Audit trail of decisions | Recommended | Required | Required + immutable |
| Model monitoring (drift) | Recommended | Required | Required + automated alerts |

---

## Security Baseline for Data Platform

- [ ] All ADLS Gen2 containers: no public access; private endpoint only
- [ ] All containers: hierarchical namespace enabled (POSIX ACLs)
- [ ] Encryption: customer-managed keys (CMK) in Key Vault for Restricted data
- [ ] Fabric workspace: tenant-level isolation; no cross-tenant access
- [ ] Service principals for pipelines: Managed Identity (no client secrets)
- [ ] Purview data classifications: auto-applied; Restricted data triggers alerts
- [ ] Row-level security (RLS) on Power BI semantic models for Confidential data
- [ ] Azure Monitor + Purview audit logs: all data access logged
- [ ] Data exfiltration prevention: Fabric managed VNet; no internet egress from pipelines

---

## DR Configuration

| Component | DR Approach | RTO | RPO |
|---|---|---|---|
| ADLS Gen2 (Bronze) | Geo-redundant storage (GRS) | N/A (data not lost) | 0 (geo-replication) |
| Fabric Lakehouse (Silver/Gold) | Fabric built-in redundancy + daily OneLake backup | 4h | 24h |
| Azure ML Model Registry | Geo-redundant; models pinned by version | 4h | 0 (immutable) |
| Power BI Semantic Models | Rebuild from Gold layer; datasets backed up via XMLA | 4h | 24h |

> Classify the data platform as **DR Tier 2** by default. Elevate specific Gold layer data products to Tier 1 if they feed mission-critical operational processes.
