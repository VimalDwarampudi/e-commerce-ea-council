# Example: Integration Architecture Assessment — Dynamics 365 ↔ SAP S/4HANA

## Input (Request Summary)

> "We need to integrate Dynamics 365 Sales with SAP S/4HANA to sync customer master data bidirectionally and enable quote-to-order from CRM."

## Output (Integration Architecture Assessment)

## Integration Architecture Assessment

### Current Integration Landscape
LeanIX Interfaces query returned 1 existing interface between CRM and SAP:

- **Siebel → SAP (file-based batch):** Daily flat-file export of closed opportunities to SAP order entry. Protocol: SFTP. Frequency: Nightly batch. Status: Active but rated HOLD technology (SFTP file integration). No error handling documented. **This interface will be replaced by the proposed integration.**

No existing REST or event-based integration between CRM and SAP found in LeanIX.

### Integration Pattern Recommendation

Two distinct integration flows are required. Different patterns apply to each:

**Flow 1: Customer Master Data Sync (bidirectional)**
- **Pattern:** Event-Driven / Publish-Subscribe
- **Rationale:** Customer data changes are domain events. Neither system is always the initiator — SAP creates customers from finance; Dynamics creates customers from sales. An event mesh decouples both systems from each other.
- **Platform:** Azure Service Bus (Topics with subscriptions for each consumer)
- **Direction:** SAP publishes `Finance.Customer.Created/Updated` → Service Bus → Dynamics 365 consumes; Dynamics 365 publishes `CRM.Account.Created/Updated` → Service Bus → SAP consumes
- **System of Record:** SAP S/4HANA for **master customer record** (BP/Customer entity). Dynamics 365 owns **CRM enrichment** (contacts, opportunities, activities). Conflict resolution: SAP master fields win on conflict.

**Flow 2: Quote-to-Order (Dynamics → SAP)**
- **Pattern:** Synchronous REST (orchestrated via Logic Apps)
- **Rationale:** Order creation requires immediate confirmation (order number, availability check). User is waiting for a response. Async would require a polling/notification pattern that adds UX complexity.
- **Platform:** Azure Logic Apps with SAP connector (OData to SAP S/4HANA Sales Order API)
- **Direction:** Dynamics 365 (on Quote Accepted) → Logic Apps → SAP S/4HANA Sales Order API → response returned to Dynamics with SAP order number

### Interface Design Guidance

**Customer Master Event Schema (register in schema registry):**
```json
{
  "eventId": "uuid",
  "eventType": "Finance.Customer.Updated",
  "eventVersion": "1.0",
  "timestamp": "ISO8601",
  "source": "SAP-S4HANA",
  "correlationId": "uuid",
  "data": {
    "customerId": "string (SAP BP number)",
    "crmAccountId": "string (Dynamics Account GUID — if known)",
    "name": "string",
    "addressLine1": "string",
    "city": "string",
    "country": "ISO3166-2",
    "vatNumber": "string",
    "lastModified": "ISO8601"
  }
}
```

**Quote-to-Order API contract (SAP OData):**
- Endpoint: `POST /sap/opu/odata/sap/API_SALES_ORDER_SRV/A_SalesOrder`
- Authentication: OAuth 2.0 via SAP BTP (not direct RFC)
- Idempotency: use Dynamics Quote ID as SAP external reference to prevent duplicate orders
- Timeout: 10 seconds (SAP availability check can be slow); implement async fallback if exceeded
- Error mapping: SAP BAPI errors mapped to standard error response body

### Dependency & Coupling Risk
- **Tight coupling risk — Flow 2:** Logic Apps orchestrates a synchronous call to SAP. If SAP is unavailable, quote submission fails. **Mitigation:** Circuit breaker pattern in Logic Apps; queue orders when SAP is down with retry and user notification.
- **Data model alignment:** SAP customer ID and Dynamics Account ID must be cross-referenced. Design a mapping table (Dataverse or dedicated Azure SQL) to maintain the bidirectional key mapping.
- **Existing SFTP interface:** Must be decommissioned once the new integration is live and stable. Do not run both in parallel indefinitely — dual-write creates data inconsistency risk.

### API Governance
- New interfaces must be registered in LeanIX before go-live: 2 new Interface records required.
- Event schemas registered in schema registry before first publish.
- Logic Apps workflow version-controlled in Git with IaC.
- SAP OData API version pinned — subscribe to SAP change notifications.

### Recommendation
1. Implement **Customer Master sync** as event-driven (Service Bus topics) with SAP as system of record.
2. Implement **Quote-to-Order** as synchronous Logic Apps orchestration with circuit breaker.
3. Retire the existing Siebel→SAP SFTP interface as part of this project (do not leave it running).
4. Register both new interfaces in LeanIX before go-live.
5. Implement cross-reference key mapping in Dataverse — owned by Integration Architecture.

### Dependencies on Peer Domains
- **Data & AI:** Customer data is personal data — confirm GDPR basis for cross-system sync; check data classification of fields in event payload.
- **Security Architecture:** OAuth 2.0 for SAP BTP authentication; review Service Bus access policies.
- **Technology & Infrastructure:** Logic Apps hosting and Service Bus namespace provisioning.

## Key Points Illustrated
- LeanIX Interfaces queried first — existing SFTP interface found and flagged
- Two different patterns chosen for two different flows — justified explicitly
- Pattern selection driven by decision tree (real-time need vs event-driven fit)
- Event schema provided in full (ready for schema registry)
- System of record declared explicitly for customer master
- Coupling risks identified with concrete mitigations
- Decommission of old interface included (not left as an assumption)
