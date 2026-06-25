# Reference Architecture: Integration Patterns

## Purpose

This document defines the approved integration patterns for the enterprise. Every new integration should start here, select the appropriate pattern, and then design within it.

---

## Pattern 1: Synchronous REST API

**Use when:** Consumer needs an immediate response; real-time user interactions; query/command to a single system.

```
Consumer ──── HTTPS/REST ────► API Gateway (APIM) ──── OAuth2 ────► Provider API
                                    │
                                    ├─ Rate limiting
                                    ├─ Authentication
                                    └─ Logging
```

**Design requirements:**
- OpenAPI 3.x spec published in APIM developer portal
- OAuth 2.0 authentication (Entra ID)
- Idempotency keys for POST/PUT operations
- Timeout defined: recommend 5s default, 30s max
- Retry: max 3 attempts with exponential backoff (consumer responsibility)
- Error handling: standardized error response body

**When NOT to use:**
- Long-running operations (> 30s) → use async pattern
- High-volume data transfer → use batch or streaming
- Loose coupling more important than immediacy → use events

---

## Pattern 2: Asynchronous Messaging (Command/Request)

**Use when:** Processing that does not need to complete synchronously; workload levelling; decoupling producer from consumer availability.

```
Producer ──► Service Bus Queue ──► Consumer
                    │
                    ├─ Dead Letter Queue (DLQ)
                    ├─ Retry policy
                    └─ Message lock / at-least-once delivery
```

**Design requirements:**
- Message schema: standardized envelope (messageId, timestamp, source, correlationId, payload)
- Dead-letter queue: configured and monitored
- Idempotent consumer: consumer must handle duplicate delivery gracefully
- Poison message handling: DLQ review process defined
- Visibility timeout: set appropriately for expected processing time

---

## Pattern 3: Event-Driven (Publish-Subscribe)

**Use when:** Multiple consumers react to the same event; domain events that other domains should know about; choreography over orchestration.

```
Domain A ──► Event Bus (Service Bus Topics / Event Hubs)
                    │
                    ├─────────► Domain B (Subscription)
                    ├─────────► Domain C (Subscription)
                    └─────────► Audit / Archival (Subscription)
```

**Design requirements:**
- Event schema registered in schema registry (Avro or JSON Schema)
- Event envelope: `{ eventId, eventType, eventVersion, timestamp, source, correlationId, data }`
- Topic-per-domain (not per-event-type) to avoid topic proliferation
- Consumer groups / subscriptions named per consuming application
- Schema evolution: backward-compatible changes only without version bump

**Event naming:** `[Domain].[Entity].[PastTenseVerb]` — e.g., `Finance.Invoice.Approved`

---

## Pattern 4: SAP Integration via BTP / Event Mesh

**Use when:** Integrating with SAP S/4HANA for business process events or data extraction.

```
SAP S/4HANA ──► SAP BTP Event Mesh ──► Azure Event Hubs ──► Consumers
                        OR
SAP S/4HANA ──► SAP Integration Suite (iFlow) ──► Azure Service Bus ──► Consumers
                        OR
Azure Logic Apps ──► SAP Connector ──► SAP S/4HANA (OData/BAPI/RFC)
```

**Approved connectors:**
- **Azure Logic Apps SAP connector** — for pull-based or orchestrated SAP interactions
- **SAP BTP Integration Suite** — for complex SAP-to-SAP or SAP-to-cloud iFlows
- **LeanIX MCP** — read-only access to SAP LeanIX EA repository

**Avoid:**
- Direct RFC/BAPI calls from non-SAP systems without an abstraction layer
- Bypassing SAP BTP and connecting directly to SAP database tables

---

## Pattern 5: ServiceNow Integration

**Use when:** Triggering ITSM workflows, reading CMDB, writing risk records, or creating change requests from architecture processes.

```
EA Council Agent ──► ServiceNow REST API ──► ServiceNow Platform
                            │
                            ├─ Table API (CRUD on any table)
                            ├─ Import Sets API (bulk data)
                            ├─ Scripted REST API (custom endpoints)
                            └─ Flow Designer / IntegrationHub (outbound webhooks)
```

**Key endpoints used by EA Council:**
- `GET /api/now/table/cmdb_ci_appl` — Application CIs
- `GET /api/now/table/cmdb_rel_ci` — CI relationships
- `POST /api/now/table/change_request` — Create change request
- `GET/POST /api/now/table/sn_risk_risk` — Risk register
- `GET /api/now/table/sn_compliance_policy_exception` — Policy exceptions

**Authentication:** OAuth 2.0 with ServiceNow as the OAuth provider (Client Credentials flow for system-to-system)

---

## Pattern 6: Batch / ETL

**Use when:** Large-volume data movement; latency-tolerant (hours acceptable); bulk reporting extraction; data migration.

```
Source System ──► Azure Data Factory ──► Azure Data Lake (raw) ──► Transformation ──► Target
                   or Logic Apps             (ADLS Gen2)             (ADF / Fabric)
```

**Design requirements:**
- Schedule defined and documented (cron expression)
- Incremental load preferred over full extract (delta/CDC where available)
- Failed run alerting: notify owner within 30 minutes of failure
- Idempotent transforms: re-running the job produces the same result
- Data lineage documented in LeanIX or Fabric data catalog

---

## Pattern 7: LeanIX MCP Integration

**Use when:** An EA Council agent needs to query the architecture repository in real time.

```
EA Council Agent ──► MCP Client ──► LeanIX MCP Server ──► LeanIX GraphQL API
```

**Standard queries** (see `connectors/leanix-queries.md`):
- Application portfolio with lifecycle and fit scores
- Applications by business capability
- Interfaces between two applications
- IT Components and tech stack for an application
- Data Objects and their owners
- Tech radar positions

**Write-back** (post-decision):
- Lifecycle state changes
- New Interface records
- Technology radar position updates
- New Data Object records

**Rate limiting:** LeanIX API has rate limits. Batch queries where possible; avoid per-item loops.
