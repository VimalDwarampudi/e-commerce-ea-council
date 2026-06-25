# Integration Architecture Guidelines

## Integration Pattern Selection Guide

Use this guide to select the right integration pattern before designing any interface.

### Decision Tree

```
Does the consumer need a response immediately (< 2 sec)?
├── YES → Is it a simple query/command to one system?
│   ├── YES → REST API (synchronous request-reply)
│   └── NO → Is it a complex multi-step orchestration?
│       ├── YES → Orchestration pattern (workflow engine / Logic Apps)
│       └── NO → GraphQL (flexible query with multiple data sources)
└── NO → Can consumers react independently to what happened?
    ├── YES → Event-Driven / Publish-Subscribe (Event Bus / Service Bus / Kafka)
    └── NO → Is this large-volume, latency-tolerant bulk data?
        └── YES → Batch / ETL (scheduled file or DB transfer)
```

### Pattern Characteristics at a Glance

| Pattern | Coupling | Latency | Complexity | Resilience | Best For |
|---|---|---|---|---|---|
| REST (sync) | Medium | Low | Low | Medium | User-facing, real-time queries |
| GraphQL | Medium | Low | Medium | Medium | Flexible data fetching, BFF pattern |
| Async Messaging | Low | Medium | Medium | High | Decoupled domain events |
| Event Streaming | Very Low | Low | High | Very High | High-volume, real-time data flows |
| Batch/ETL | Low | High | Low | Medium | Bulk data, reporting, migrations |
| Orchestration | High | Medium | High | Low | Complex multi-step business processes |
| Choreography | Very Low | Medium | High | Very High | Autonomous domain reactions |

## API Design Standards

### REST API Checklist
- [ ] OpenAPI 3.x specification written before implementation
- [ ] Semantic versioning in URL path: `/api/v1/resource`
- [ ] HTTP verbs used correctly: GET (read), POST (create), PUT/PATCH (update), DELETE (remove)
- [ ] HTTP status codes used correctly: 200/201/204/400/401/403/404/409/422/500
- [ ] Pagination for collection endpoints: use cursor-based pagination for large datasets
- [ ] Error response body standardized: `{ "error": { "code": "", "message": "", "details": [] } }`
- [ ] Authentication: OAuth 2.0 / OIDC token or API key (internal)
- [ ] Rate limiting headers returned: `X-RateLimit-Limit`, `X-RateLimit-Remaining`
- [ ] Idempotency keys for POST/PUT mutations that could be retried
- [ ] CORS policy defined if browser-accessible

### AsyncAPI / Event Schema Checklist
- [ ] AsyncAPI 2.x specification written before publishing
- [ ] Event schema registered in the schema registry (Avro or JSON Schema)
- [ ] Event envelope includes: eventId, eventType, eventVersion, timestamp, source, correlationId
- [ ] Consumer group / subscription naming convention followed
- [ ] Dead-letter queue (DLQ) configured
- [ ] Retry policy defined: max attempts, backoff strategy
- [ ] Schema backward-compatibility rule: FULL_TRANSITIVE (prefer) or BACKWARD

## API Versioning Policy

| Change Type | Versioning Action | Consumer Impact |
|---|---|---|
| Add optional field to response | Patch — no version bump | None (consumers ignore unknown fields) |
| Add optional field to request | Minor — no version bump | None |
| Add required field to request | **Major version bump** | Consumers must update |
| Remove or rename a field | **Major version bump** | Consumers must update |
| Change field type or semantics | **Major version bump** | Consumers must update |
| New endpoint added | Minor — no version bump | None |
| Endpoint removed | **Major version bump** + deprecation period | Consumers must migrate |

**Deprecation lifecycle:**
1. Mark endpoint as deprecated in OpenAPI spec and documentation
2. Add `Deprecation` and `Sunset` response headers
3. Notify all registered consumers
4. Maintain deprecated version for minimum 6 months
5. Remove only after all consumers have migrated (verify via API gateway analytics)

## How to Document an Integration in LeanIX

Every interface must be documented with:
- **Source application** (LeanIX Application record)
- **Target application** (LeanIX Application record)
- **Data objects exchanged** (LeanIX Data Object records)
- **Protocol**: REST / SOAP / Event / File / DB / GraphQL
- **Direction**: Uni-directional or bi-directional
- **Frequency**: Real-time / Near-real-time / Scheduled (with interval)
- **Business criticality**: Mission Critical / Business Critical / Standard
- **Owner**: Integration owner (person or team)

## Integration Health Metrics to Define at Design Time

| Metric | Definition | Threshold Example |
|---|---|---|
| Availability | % uptime of the integration | ≥ 99.5% for business-critical |
| Latency (p99) | 99th percentile end-to-end latency | < 2s for sync user-facing |
| Error rate | % of calls/messages failing | < 0.1% for critical flows |
| Throughput | Messages or requests per second | Define based on peak load |
| DLQ depth | Messages stuck in dead-letter queue | Alert at > 0 for critical flows |
