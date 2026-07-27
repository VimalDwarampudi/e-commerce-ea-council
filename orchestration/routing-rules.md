# Routing Rules — Which Agents to Engage

## Purpose

Guides the Chief Architect in selecting which of the 15 agents to consult for a given request. Engaging
unnecessary agents wastes cycles; missing a relevant agent risks blind spots.

## Primary Routing Table

| Request Topic | Domain Agents | Cross-Cut Agents |
|---|---|---|
| New capability / business line (e.g. BOPIS, subscription commerce) | Business Strategy, + all directly implicated domains | Security, Risk & Compliance, Red Team |
| Product catalog / taxonomy change | Catalog & Product Information, Search & Discovery | — |
| New marketplace channel | Catalog & Product Information, Integration | Security, Risk & Compliance |
| Search platform change / relevance tuning | Search & Discovery, Data & AI | — |
| Checkout flow / cart redesign | Commerce & Checkout | Security (if payment-adjacent) |
| Promotion / pricing logic | Commerce & Checkout, Application | — |
| Order lifecycle / OMS design | Order Management, Integration | — |
| Split-fulfillment / order orchestration | Order Management, Fulfillment & Logistics | — |
| Payment processing / PSP integration | Payments | Security (always), Risk & Compliance |
| Fraud / chargeback handling | Payments, Data & AI | Risk & Compliance |
| POS / in-store systems | Omnichannel & Store Systems | Security |
| BOPIS / ship-from-store / endless aisle | Omnichannel & Store Systems, Order Management, Fulfillment & Logistics | Security, Risk & Compliance |
| Store network design | Omnichannel & Store Systems, Technology & Infrastructure | Security (always) |
| Inventory / WMS design | Fulfillment & Logistics, Integration | — |
| Shipping / carrier integration | Fulfillment & Logistics, Integration | — |
| Returns processing | Fulfillment & Logistics | Risk & Compliance (if fraud pattern) |
| New application / vendor / SaaS adoption | Application | Security (always), Risk & Compliance |
| Application decommission | Application | Risk & Compliance |
| New integration / API / event schema | Integration | Security |
| Cloud migration / hosting change | Technology & Infrastructure, Application | Security, Risk & Compliance |
| Peak-event (Black Friday) capacity review | Technology & Infrastructure, + all customer-facing domains touched | Security |
| Personalization / recommendation initiative | Data & AI, Application | Security, Risk & Compliance, Red Team |
| Customer identity / consent | Data & AI | Risk & Compliance (always) |
| AI/ML model (any) | Data & AI | Security, Risk & Compliance, Red Team |
| Security architecture review | (all directly implicated domains) | Security (lead), Risk & Compliance |
| Regulatory / compliance assessment (PCI, GDPR, CCPA) | (all directly implicated domains) | Risk & Compliance (lead), Security |
| Cross-border data flow | Data & AI | Risk & Compliance (always) |
| Incident-driven review | (implicated domains) | Security (lead), Risk & Compliance, Red Team |

## Routing Logic

```
IF impact = Minor:
    → Consult 1–2 most relevant domain agents only
    → Skip cross-cut agents unless topic is security- or payment-sensitive

IF impact = Standard:
    → Consult all relevant domain agents
    → Always include Security
    → Include Risk & Compliance if regulatory/data/fraud keywords present

IF impact = Major:
    → Consult all relevant domain agents
    → Always include Security + Risk & Compliance
    → Consider Red Team if proposal is novel or high-stakes

IF impact = Critical:
    → Engage full council (all 12 domain + all 3 cross-cut agents)
    → Red Team is mandatory
    → Human sponsor review is mandatory before finalizing
```

## Keyword Signals for Cross-Cut Agents

### Always include Security if request mentions:
- cardholder data, PAN, CVV, tokenization, PCI-DSS, PSP
- authentication, authorization, IAM, SSO, API keys
- external-facing systems, public APIs, marketplace/partner integration
- store network, POS, guest WiFi, network segmentation
- PII, customer data exposure

### Always include Risk & Compliance if request mentions:
- GDPR, CCPA, consumer protection, data residency, cross-border transfer
- consent, data deletion request, retention
- fraud (return fraud, payment fraud, chargeback thresholds)
- vendor risk, third-party dependency
- risk appetite, waiver, exception

### Always include Red Team if request mentions:
- new capability with no existing reference architecture in `knowledge/shared/reference-architectures/`
- peak-event (Black Friday/Cyber Monday) readiness for a new or changed system
- irreversible architectural change
- single point of failure in checkout, payments, or store network
- "we're confident this is safe" or similar (flag groupthink)

## Ambiguous Requests

If the request topic is unclear:
1. Ask the requester one clarifying question (topic + impact level).
2. Make a provisional routing decision and state it.
3. Adjust routing if new information changes the scope.
