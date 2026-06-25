# Routing Rules — Which Agents to Engage

## Purpose

This file guides the Chief Architect in selecting which agents to consult for a given request. Engaging unnecessary agents wastes cycles; missing a relevant agent risks blind spots.

## Primary Routing Table

| Request Topic | Domain Agents | Cross-Cut Agents |
|---|---|---|
| New application adoption | Product Management, Technology Infrastructure | Security, Risk & Compliance |
| Application decommission | Product Management, Business Strategy | Risk & Compliance |
| Cloud migration | Technology Infrastructure, Product Management | Security, Risk & Compliance |
| New integration / API | Product Management, Technology Infrastructure | Security |
| Business capability mapping | Business Strategy | — |
| Strategy-to-technology alignment | Business Strategy, Product Management, Technology Infrastructure | — |
| Data platform or data governance | Data Platform, Product Management | Security, Risk & Compliance |
| AI/ML initiative | Data Platform, Product Management, Technology Infrastructure | Security, Risk & Compliance, Innovation Team |
| Security architecture review | (all relevant domain agents) | Security (lead), Risk & Compliance |
| Regulatory compliance assessment | Business Strategy, Product Management | Risk & Compliance (lead), Security |
| Technology radar update | Product Management, Technology Infrastructure, Data Platform | — |
| Reference architecture creation | All domain agents | Security, Risk & Compliance, Innovation Team |
| Major platform replacement | All domain agents | All cross-cut agents |
| Vendor / SaaS evaluation | Product Management, Technology Infrastructure | Security, Risk & Compliance |
| Incident-driven architecture review | Technology Infrastructure, Product Management | Security (lead), Risk & Compliance, Innovation Team |
| E-commerce search implementation | Search & Discovery, Data Platform, Customer Experience | Security |
| Product catalog management | Product Management, Data Platform | Security |
| Checkout process design | Checkout & Payments, Customer Experience | Security, Risk & Compliance |
| Order creation system | Order Management | Security |
| Order fulfillment integration | Fulfillment & Logistics, Order Management | Security |
| Payment gateway integration | Checkout & Payments | Security, Risk & Compliance |
| Receipt generation | Order Management, Risk & Compliance | Security |
| Returns processing | Fulfillment & Logistics, Customer Experience, Order Management | Security |

## Routing Logic

```
IF impact = Minor:
    → Consult 1–2 most relevant domain agents only
    → Skip cross-cut agents unless topic is security-sensitive

IF impact = Standard:
    → Consult all relevant domain agents
    → Always include Security
    → Include Risk & Compliance if regulatory/risk keywords present

IF impact = Major:
    → Consult all relevant domain agents
    → Always include Security + Risk & Compliance
    → Consider Red Team if proposal is novel or high-stakes

IF impact = Critical:
    → Engage full council (all domain + all cross-cut agents)
    → Red Team is mandatory
    → Human sponsor review is mandatory before finalizing
```

## Keyword Signals for Cross-Cut Agents

### Always include Security if request mentions:
- authentication, authorization, identity, IAM, SSO, OAuth
- data encryption, key management, TLS/HTTPS
- external-facing systems, public APIs, internet exposure
- cloud egress, network perimeter, firewall
- personal data, PII, sensitive data classification
- zero-trust, micro-segmentation
- SaaS onboarding, third-party access

### Always include Risk & Compliance if request mentions:
- GDPR, NIS2, SOX, ISO 27001, DORA, PCI-DSS
- data residency, data sovereignty, cross-border transfer
- audit trail, logging, regulatory reporting
- vendor risk, third-party dependency
- business continuity, disaster recovery
- risk appetite, tolerance, waiver, exception

### Always include Business Strategy if request mentions:
- business strategy, market analysis, competitive positioning
- capability mapping, value streams, business case
- strategic planning, roadmap alignment, KPI definition

### Always include Product Management if request mentions:
- product development, feature prioritization, roadmap
- catalog management, product lifecycle, A/B testing
- marketplace, vendor products, product analytics

### Always include Search & Discovery if request mentions:
- search engine, product search, query processing
- recommendations, discovery algorithms, relevance
- faceted search, filtering, personalization in search

### Always include Checkout & Payments if request mentions:
- checkout flow, payment processing, fraud detection
- PCI compliance, payment gateways, transaction security
- cart management, payment methods, BNPL

### Always include Order Management if request mentions:
- order creation, order status, order lifecycle
- order orchestration, inventory allocation, order tracking
- SLA management, order analytics

### Always include Fulfillment & Logistics if request mentions:
- order fulfillment, supply chain, delivery optimization
- warehouse management, logistics, last-mile delivery
- inventory management, shipping, returns processing

### Always include Customer Experience if request mentions:
- UX, UI, user experience, customer journey, wireframing
- personalization, recommendation engine, A/B testing
- accessibility, WCAG, inclusive design
- omnichannel, cross-device experience
- voice commerce, AR/VR shopping, PWA

### Always include Data Platform if request mentions:
- data architecture, data warehouse, data lake
- analytics, reporting, BI, data governance
- AI/ML, machine learning, data science
- ETL/ELT, data pipelines, data quality

### Always include Technology Infrastructure if request mentions:
- cloud infrastructure, DevOps, CI/CD
- scalability, performance, high availability
- hosting, containers, serverless, microservices

### Always include Security if request mentions:
- authentication, authorization, identity, IAM, SSO, OAuth
- data encryption, key management, TLS/HTTPS
- external-facing systems, public APIs, internet exposure
- cloud egress, network perimeter, firewall
- personal data, PII, sensitive data classification
- zero-trust, micro-segmentation
- SaaS onboarding, third-party access

### Always include Innovation Team if request mentions:
- new AI system or autonomous agent
- emerging technology, innovation, disruptive tech
- irreversible architectural change
- single point of failure in critical path
- "we're confident this is safe" (flag groupthink)
- novel architecture pattern not in reference architectures
- experimental features, beta testing, MVP

## Ambiguous Requests

If the request topic is unclear:
1. Ask the requester one clarifying question (topic + impact level)
2. Make a provisional routing decision and state it
3. Adjust routing if new information changes the scope
