#!/usr/bin/env python3
"""Generates the OKF knowledge bundle (knowledge/) and Claude Code subagents
(.claude/agents/) for the retail EA council. Run from /home/claude/retail-build.
"""
import os

TS = "2026-07-23T00:00:00Z"

def fm(type_, title, description, tags, mandatory=None, extra=None):
    lines = ["---", f"type: {type_}", f"title: {title}", f"description: {description}",
             f"tags: [{', '.join(tags)}]", f"timestamp: {TS}"]
    if mandatory is not None:
        lines.append(f"mandatory: {str(mandatory).lower()}")
    if extra:
        for k, v in extra.items():
            lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines)


DOMAINS = [
    dict(
        slug="business-strategy", display="Business Strategy & Capability Alignment",
        desc="Business capability mapping, market strategy alignment, value stream design.",
        authority="Advisory",
        principles=[
            ("Capability Before Technology", "Every architecture decision must trace to a named business capability. If a proposal cannot be mapped to a capability on the current capability map, the capability map is out of date or the proposal is solving the wrong problem — resolve that first, not the technology choice."),
            ("Omnichannel Is One Business, Not Two", "Store and digital are not separate business lines to be architected independently. Inventory, pricing, promotions, and customer identity must be modeled as single sources of truth consumed by both channels. Any proposal that creates a store-only or digital-only version of a shared capability requires explicit justification."),
        ],
        policies=[
            ("New Capability Requires Business Case", True, "No new business capability (e.g. a new fulfillment model, a new marketplace channel) may be architected without a documented business case including expected revenue/cost impact and the sponsoring business owner. Architecture work without a named business owner is not resourced correctly and will stall."),
            ("Store and Digital P&L Attribution", False, "Where a proposal affects revenue attribution between store and digital channels (e.g. BOPIS, ship-from-store), Finance must be consulted before the ADR is finalized. This is a policy, not mandatory-blocking, because Finance input can arrive after initial architecture work but must arrive before launch."),
        ],
        guidelines=[
            ("Capability Assessment Method", "Score each capability on Business Value (H/M/L) x Technical Maturity (H/M/L) x Differentiation (Core/Enabling/Commodity). Core capabilities with low technical maturity are the highest-priority investment targets. Commodity capabilities with high maturity are decommission/buy candidates, not build targets."),
        ],
        examples=[
            ("BOPIS Capability Assessment", "Request: assess readiness for buy-online-pickup-in-store as a new capability.\n\nCapability scoring: Business Value = H (competitive parity, reduces last-mile cost). Technical Maturity = L (no real-time cross-channel inventory visibility exists today). Differentiation = Enabling.\n\nRecommendation: BOPIS is a Major-impact capability investment. It is blocked on the Omnichannel & Store Systems domain's real-time inventory visibility work — sequence that first. Do not architect BOPIS as a store-side-only feature; it must consume the same inventory truth as digital checkout, per the Omnichannel principle above."),
        ],
    ),
    dict(
        slug="catalog-product", display="Catalog & Product Information Architecture",
        desc="Product information management (PIM), catalog data model, taxonomy, digital asset management.",
        authority="Advisory",
        principles=[
            ("Single Product Record, Many Views", "There is exactly one authoritative product record (owned by the PIM) per SKU. Store systems, the digital storefront, marketplace feeds, and search indexes are all downstream consumers/projections of that record, never independent sources of truth for product attributes."),
            ("Taxonomy Is a Contract", "Category taxonomy changes are breaking changes for search, navigation, and marketplace feed mappings. Taxonomy changes require the same change-control rigor as an API contract change, including a deprecation window for consumers."),
        ],
        policies=[
            ("PIM as System of Record", True, "No system other than the designated PIM may be treated as authoritative for product title, description, attributes, or category assignment. Point-to-point product data sync between two non-PIM systems is prohibited — all product data flows through the PIM and its published integration contract."),
            ("Marketplace Feed Attribute Mapping Review", False, "Any new marketplace channel (e.g. adding a new third-party marketplace) requires Integration Architecture review of the attribute mapping before go-live, since malformed feeds risk marketplace account suspension."),
        ],
        guidelines=[
            ("PIM vs. DAM Boundary", "Structured product attributes (price, size, material, compliance data) live in the PIM. Unstructured assets (images, video, 360-degree spins) live in a Digital Asset Management system and are referenced, not embedded, from PIM records. Do not let either system grow to duplicate the other's responsibility."),
        ],
        examples=[
            ("New Marketplace Channel Onboarding", "Request: onboard a new third-party marketplace channel.\n\nAssessment: existing PIM export supports 80% of the required attribute schema. Gap: marketplace-specific compliance attributes (country of origin, safety certifications) not currently modeled in PIM.\n\nRecommendation: extend the PIM schema rather than maintain a marketplace-specific side table — a side table would violate the single-source-of-record principle and create drift risk. Flag to Risk & Compliance since compliance attributes are involved."),
        ],
    ),
    dict(
        slug="search-discovery", display="Search & Discovery Architecture",
        desc="Search engines, indexing, relevance tuning, product discovery, on-site navigation.",
        authority="Advisory",
        principles=[
            ("Relevance Is Measured, Not Assumed", "Every material change to search ranking or relevance logic must be evaluated against a defined relevance metric (e.g. NDCG, click-through, zero-result rate) before and after rollout. Relevance changes are architecture decisions when they touch the underlying ranking model or index structure, not just merchandising configuration."),
            ("Index Freshness Matches Business Criticality", "Inventory-sensitive attributes (in-stock status, price) in the search index must be near-real-time. Descriptive attributes (title, long description) can tolerate batch/eventual sync. Do not apply one freshness SLA uniformly across all indexed fields — it either over-invests in infrastructure or under-serves customers."),
        ],
        policies=[
            ("Zero-Result Query Monitoring", False, "Any search platform must expose zero-result-rate as a monitored metric with alerting. A rising zero-result rate is a leading indicator of catalog or taxonomy problems and must be visible to Catalog & Product Information, not just Search & Discovery."),
            ("No PII in Search Query Logs Without Redaction", True, "Search query logs must not retain personally identifiable information (e.g. a customer typing their own email or address into search) beyond what is required for abuse detection, and must be redacted or purged per the retention policy in Risk & Compliance's data policies."),
        ],
        guidelines=[
            ("Search Platform Evaluation Criteria", "Evaluate candidate search platforms against: relevance tuning flexibility, faceted navigation performance at catalog scale, personalization hook availability (for Data & AI integration), peak-load query throughput (Black Friday scale), and total cost of ownership including relevance-tuning labor, not just licensing."),
        ],
        examples=[
            ("Search Platform Migration Assessment", "Request: evaluate migrating from a legacy on-prem search platform to a managed cloud search service.\n\nFindings: managed service meets relevance and throughput requirements; migration risk is primarily in re-tuning years of accumulated relevance boosting rules, which are undocumented.\n\nRecommendation: Standard impact. Require a relevance parity test suite be built from current production query logs before cutover, since the undocumented tuning rules are the real risk, not the platform capability."),
        ],
    ),
    dict(
        slug="commerce-checkout", display="Commerce & Checkout Architecture",
        desc="Shopping cart, checkout flow, session/state management, promotions and pricing at checkout.",
        authority="Advisory",
        principles=[
            ("Cart State Survives Everything", "A customer's cart must survive session expiry, device switch, and channel switch (start on mobile, finish on desktop or in-store) without data loss. Any checkout redesign that cannot preserve cart state across these transitions is a regression, not a simplification."),
            ("Checkout Latency Is a Conversion Metric", "Every added step or synchronous external call in the checkout flow (tax calculation, fraud check, promo validation) must be justified against its conversion impact. Default to asynchronous/optimistic patterns; synchronous blocking calls on the critical checkout path require explicit sign-off."),
        ],
        policies=[
            ("No Custom Cardholder Data Handling in Checkout UI", True, "The checkout flow's own application code must never receive, log, or store raw cardholder data. All payment collection must go through the PCI-scoped mechanism defined by Payments Architecture (iframe/tokenization). This eliminates checkout services from PCI-DSS scope — violating it brings the entire checkout platform into scope."),
            ("Promotion Stacking Rules Centrally Owned", False, "Discount/promotion stacking logic must live in one rules engine consulted by cart, checkout, and any channel (store POS included) — not reimplemented per channel. Divergent promo logic between channels is a top source of customer complaints and revenue leakage."),
        ],
        guidelines=[
            ("Guest vs. Account Checkout Design", "Guest checkout must be the default fast path; account creation should be offered post-purchase, not required pre-purchase, unless the business has an explicit strategic reason (e.g. subscription commerce) documented and approved by Business Strategy."),
        ],
        examples=[
            ("Cross-Device Cart Persistence Redesign", "Request: customers report losing cart contents when switching from mobile app to desktop web.\n\nRoot cause: cart is currently session-scoped per device, not identity-scoped.\n\nRecommendation: Standard impact. Move cart ownership to customer identity (authenticated or persistent guest token), synced server-side. Integration Architecture must confirm the identity service can support this without introducing checkout-path latency — flag as a dependency, do not build in isolation."),
        ],
    ),
    dict(
        slug="order-management", display="Order Management Architecture",
        desc="Order orchestration, order lifecycle state machine, order status tracking, order data model.",
        authority="Advisory",
        principles=[
            ("One Order, One Lifecycle, Many Fulfillments", "An order can split across multiple fulfillments (ship-from-store, warehouse, backorder) but must remain one logical order with one customer-facing status view. Do not let fulfillment splitting leak into the customer experience as multiple disconnected order records."),
            ("Order State Transitions Are Auditable", "Every order status transition must be logged with timestamp, actor (system or human), and reason. Order status is a common source of customer service escalations and regulatory inquiry (e.g. delivery guarantee disputes) — the audit trail is not optional instrumentation, it's a requirement."),
        ],
        policies=[
            ("OMS Is the System of Record for Order Status", True, "Store POS, the digital storefront, customer service tools, and shipping carriers all read order status from the OMS; none may maintain an independent order status of record. This directly parallels the Catalog domain's PIM policy and exists for the same reason — status divergence is a top driver of customer complaints."),
            ("Order Cancellation Window Enforcement", False, "Order cancellation/modification eligibility rules (e.g. cannot cancel after fulfillment picks the item) must be enforced server-side in the OMS, not merely hidden in the UI. UI-only enforcement is trivially bypassed and creates fulfillment exceptions."),
        ],
        guidelines=[
            ("Split-Fulfillment Orchestration Pattern", "When an order splits across fulfillment sources, orchestrate via a saga pattern with explicit compensation logic (e.g. partial refund if one leg fails) rather than a single distributed transaction — order fulfillment spans systems (OMS, WMS, store POS, carriers) that cannot participate in a shared transaction."),
        ],
        examples=[
            ("Split-Shipment Customer Communication Gap", "Request: customers confused when an order arrives in multiple packages with no warning.\n\nFinding: OMS correctly tracks the split internally but the notification system only fires on the original order, not per-shipment.\n\nRecommendation: Minor-to-Standard impact depending on volume. Extend notification triggers to per-shipment events sourced from the OMS lifecycle log (per the auditable-transitions principle) rather than building a parallel notification state machine."),
        ],
    ),
    dict(
        slug="payments", display="Payments Architecture",
        desc="Payment processing, PCI-DSS scope, tokenization, payment service providers, fraud detection, chargebacks.",
        authority="Advisory",
        principles=[
            ("Minimize PCI Scope Aggressively", "Every system touching cardholder data expands PCI-DSS audit scope and cost. Default to tokenization and PSP-hosted fields for any new payment surface (checkout, store POS, call-center order entry) so that raw cardholder data never enters retailer-owned infrastructure."),
            ("Fraud Rules Must Be Explainable and Reversible", "Automated fraud decisions (declines, holds) must be logged with the specific rule/model signal that triggered them and must support manual override by a human reviewer. An unexplainable fraud decline is both a customer-experience failure and a regulatory risk (see Risk & Compliance)."),
        ],
        policies=[
            ("No Raw Cardholder Data at Rest", True, "Raw PAN, CVV, or full track data must never be stored in retailer-owned databases, logs, or backups under any circumstance. CVV storage post-authorization is prohibited outright by card network rules, not just this policy — a violation here is an automatic Security veto with no negotiation path."),
            ("PSP Failover Required for Peak Events", True, "Payment processing must support automatic failover to a secondary PSP during peak load events (Black Friday, flash sales) or documented manual failover with a tested runbook. A single-PSP dependency with no failover path is a mandatory finding for any Major-impact peak-readiness review."),
        ],
        guidelines=[
            ("PSP Evaluation Criteria", "Evaluate payment service providers on: PCI-DSS Level 1 compliance status, tokenization/vault capability, supported payment methods per region, chargeback dispute tooling, and settlement reporting integration with Finance systems — not price alone."),
        ],
        examples=[
            ("Store POS Tokenization Gap", "Request: assess PCI exposure of the in-store POS payment flow.\n\nFinding: POS terminals are P2PE-certified (good), but the store network segment carrying terminal traffic is flat with the general store LAN, not segmented.\n\nSecurity Architecture involvement: mandatory — this is a network segmentation finding with veto-level severity if unmitigated, since it expands PCI scope to the entire store network. Recommendation: segment POS traffic on its own VLAN with strict firewall rules before this is considered resolved."),
        ],
    ),
    dict(
        slug="omnichannel-store", display="Omnichannel & Store Systems Architecture",
        desc="Point-of-sale (POS), BOPIS/ship-from-store, endless aisle, in-store inventory visibility, store network resilience.",
        authority="Advisory",
        principles=[
            ("Store Must Function Offline", "POS and core store operations must degrade gracefully during connectivity loss — a store losing internet must still be able to sell, using locally cached pricing/inventory with reconciliation on reconnect. A store-wide outage from a WAN blip is an unacceptable single point of failure for physical revenue."),
            ("Inventory Visibility Is Real-Time or It's Wrong", "BOPIS and endless-aisle features are only as trustworthy as inventory freshness. A promise of in-store availability based on stale (e.g. nightly-batch) inventory data will generate broken promises to customers at the point of pickup — this is treated as a functional defect, not a performance nice-to-have."),
        ],
        policies=[
            ("POS Network Segmentation", True, "POS terminal network traffic must be logically segmented from general store guest/corporate network traffic, per Security's zero-trust and PCI scope requirements. This is the store-side instantiation of the Payments domain's PSP/tokenization principle and cannot be waived at store level."),
            ("Store Associate Override Requires Audit Log", False, "Manual associate overrides (price override, inventory override for a sale despite system showing zero stock) must be logged with associate ID and reason code. Frequent override patterns are both a shrink-risk signal (Risk & Compliance) and an inventory-accuracy signal (Fulfillment & Logistics)."),
        ],
        guidelines=[
            ("BOPIS Reservation Pattern", "Reserve inventory at the moment of online order placement, not at pickup, using a short-TTL soft-hold that auto-releases if pickup doesn't occur within the promised window. This balances promise reliability against inventory lockup — a hard, indefinite hold starves in-store sale of the same unit."),
        ],
        examples=[
            ("BOPIS Launch Readiness Review", "Request: full-council review before BOPIS launch.\n\nDomains consulted: Omnichannel (lead), Order Management, Fulfillment & Logistics, Application, Integration, Security, Risk & Compliance.\n\nKey finding: current inventory sync between WMS and store systems is 15-minute batch, not real-time — violates the real-time-visibility principle above. Recommendation: BOPIS launch blocked pending a move to event-driven inventory updates (Integration Architecture to design). This is a Major-impact decision requiring human sponsor sign-off on the delay."),
        ],
    ),
    dict(
        slug="fulfillment-logistics", display="Fulfillment & Logistics Architecture",
        desc="Warehouse/inventory management (WMS), shipping and carrier integration, returns processing, third-party logistics (3PL).",
        authority="Advisory",
        principles=[
            ("Inventory Truth Has One Owner Per Location Type", "Warehouse inventory is owned by the WMS; store inventory is owned by the store inventory system; both publish to a unified inventory availability service consumed by Order Management, Omnichannel, and Search. No downstream system should query WMS and store systems separately and reconcile itself."),
            ("Returns Are a Fulfillment Flow, Not an Afterthought", "Returns processing (receiving, inspection, restock-or-dispose decisioning, refund trigger) must be architected as a first-class reverse-fulfillment flow with the same rigor as forward fulfillment, not bolted on as a manual/exception process."),
        ],
        policies=[
            ("Carrier Integration Abstraction Layer", False, "New carrier integrations must go through a shared carrier-abstraction service (rate shopping, label generation, tracking webhook normalization), not point-to-point integration per carrier per consuming system. This is an Integration Architecture-owned pattern that Fulfillment & Logistics must use, not bypass for speed."),
            ("Return Fraud Signal Sharing", True, "Return patterns indicating fraud (serial returners, wardrobing patterns) must be surfaced to Risk & Compliance and Payments' fraud detection systems, not siloed within the returns system. This is mandatory because return fraud is a material and growing loss category for retailers and cross-system signal sharing is the primary mitigation."),
        ],
        guidelines=[
            ("3PL Evaluation Criteria", "Evaluate third-party logistics providers on: system integration maturity (real-time API vs. batch/EDI), peak-capacity flexibility, geographic coverage matching customer base, and SLA/penalty structure for missed delivery promises."),
        ],
        examples=[
            ("Returns Fraud Pattern Detection Gap", "Request: reduce return-related shrink.\n\nFinding: the returns system currently has no visibility into a customer's return history across channels (store returns and online returns are tracked separately) — directly violates the return fraud signal-sharing policy above.\n\nRecommendation: Standard impact. Unify return history under customer identity (same identity model Commerce & Checkout uses for cart) and feed it to Payments' fraud engine. Flag to Risk & Compliance for fraud-threshold policy input."),
        ],
    ),
    dict(
        slug="application-architecture", display="Application Architecture",
        desc="Application portfolio, build/buy/SaaS decisions, application lifecycle, tech radar placement.",
        authority="Advisory",
        principles=[
            ("Buy Commodity, Build Differentiation", "Commodity capabilities (e.g. standard e-commerce platform functions) should default to SaaS/buy. Capabilities that are a genuine competitive differentiator for this retailer (e.g. a proprietary personalization approach) are build candidates. Do not build commodity capability out of habit or sunk cost."),
            ("Every Application Has a Named Owner", "No application in the portfolio may lack a named business and technical owner. Orphaned applications are the leading cause of unpatched vulnerabilities and undocumented integration dependencies discovered only during an incident."),
        ],
        policies=[
            ("New SaaS Vendor Security Review", True, "Any new SaaS application handling customer PII or payment-adjacent data must complete a Security Architecture review and a Risk & Compliance vendor risk assessment before contract signature, not after. Retrofitting security review after procurement commitment removes real leverage to require changes."),
            ("Application Retirement Requires Data Migration Plan", False, "Decommissioning an application requires a documented plan for what happens to its data (archived, migrated, or deleted per retention policy) before decommission, not as a follow-up task."),
        ],
        guidelines=[
            ("Portfolio Rationalization Method", "Score each application on Business Fit (H/M/L) x Technical Fit (H/M/L). Low/Low = decommission candidate. High business fit / low technical fit = re-platform candidate. Low business fit / high technical fit = candidate for repurposing or sunset regardless of technical quality."),
        ],
        examples=[
            ("Legacy Store Inventory System Rationalization", "Request: assess whether to keep or replace the 12-year-old in-store inventory application.\n\nScoring: Business Fit = H (still core to store operations), Technical Fit = L (no API, batch-only integration, blocking the Omnichannel real-time visibility requirement).\n\nRecommendation: Major impact — re-platform, not decommission. This is the actual root cause of the BOPIS launch blocker identified by Omnichannel & Store Systems; sequence this work ahead of BOPIS, not in parallel."),
        ],
    ),
    dict(
        slug="integration-architecture", display="Integration Architecture",
        desc="APIs, event streams, middleware, data flows between systems, carrier and marketplace integration patterns.",
        authority="Advisory",
        principles=[
            ("Event-Driven for Cross-Channel Consistency", "Anything requiring near-real-time consistency across channels (inventory, order status, pricing) should be event-driven (pub/sub) rather than batch or point-to-point polling. Batch sync is acceptable only for data that genuinely tolerates staleness."),
            ("No New Point-to-Point Integrations Without Justification", "Every new direct system-to-system integration must justify why it doesn't go through the existing API gateway/event bus. Point-to-point integration debt is the single largest driver of fragility in retail architectures with dozens of specialty systems (OMS, WMS, PIM, POS, PSP)."),
        ],
        policies=[
            ("API Gateway for All External-Facing Integrations", True, "All partner, marketplace, and third-party carrier integrations must route through the API gateway (rate limiting, auth, monitoring), never direct system access. This is mandatory because direct external access to internal systems is both a Security exposure and an operational blind spot."),
            ("Webhook Idempotency Required", False, "Any system consuming carrier or PSP webhooks (tracking updates, payment status) must implement idempotent processing, since webhook redelivery on transient failure is standard behavior for these providers and duplicate processing causes order/inventory corruption."),
        ],
        guidelines=[
            ("Event Schema Governance", "All events published to the shared event bus must be registered in a schema registry with versioning and backward-compatibility rules. Breaking schema changes require a deprecation window matching the Catalog domain's taxonomy-change policy."),
        ],
        examples=[
            ("Real-Time Inventory Event Bus Design", "Request: design the event-driven inventory sync needed to unblock BOPIS (see Omnichannel example).\n\nRecommendation: WMS and store inventory systems each publish inventory-changed events to the shared bus; a unified inventory availability service (per Fulfillment's ownership principle) consumes both streams and serves reads to Order Management, Search, and Omnichannel. This avoids point-to-point sync between WMS and every consumer, per the point-to-point policy above."),
        ],
    ),
    dict(
        slug="technology-infrastructure", display="Technology & Infrastructure",
        desc="Cloud hosting, runtime platforms, peak-load capacity planning, disaster recovery, store network infrastructure.",
        authority="Advisory",
        principles=[
            ("Design for Peak, Not Average", "Retail traffic is not evenly distributed — Black Friday/Cyber Monday and flash sales can be 10-50x normal load. Infrastructure capacity planning must be modeled against peak scenarios explicitly, with auto-scaling validated by load testing, not sized against average traffic with headroom guessed."),
            ("Store Connectivity Has No Single Point of Failure", "Every store location's network connectivity supporting POS and payment processing must have a failover path (secondary ISP, cellular backup). A single-ISP store is one outage away from being unable to transact — unacceptable for physical revenue."),
        ],
        policies=[
            ("Peak Load Testing Before Major Sales Events", True, "Full-scale load testing against a validated peak traffic model is mandatory before Black Friday/Cyber Monday and any planned flash sale expected to exceed 5x normal traffic. Skipping this for a major event is a mandatory finding that blocks sign-off."),
            ("DR Runbook Currency", False, "Disaster recovery runbooks for checkout, payments, and order management must be tested (not just documented) at least twice yearly, with results logged."),
        ],
        guidelines=[
            ("Cloud Region Strategy", "Primary customer-facing systems should run multi-AZ at minimum; multi-region is warranted for systems where an outage directly halts revenue (checkout, payments, POS backend) but may be excessive for internal/back-office systems — apply cost proportional to revenue impact, not uniformly."),
        ],
        examples=[
            ("Black Friday Capacity Review", "Request: annual pre-peak-season infrastructure review.\n\nFinding: checkout service auto-scales correctly under load test, but the tax-calculation third-party API (synchronous call in the checkout path, per Commerce & Checkout's latency principle) has no documented rate limit or fallback behavior under load.\n\nRecommendation: Major impact given the timing. Require a fallback (cached/estimated tax with async reconciliation) be built before peak season, since a synchronous external dependency with unknown limits is a checkout-wide single point of failure."),
        ],
    ),
    dict(
        slug="data-ai", display="Data & AI Architecture",
        desc="Data governance, customer data platform, personalization and recommendation systems, AI/ML strategy.",
        authority="Advisory",
        principles=[
            ("Personalization Requires Explicit Consent Tracking", "Any use of customer behavioral data for personalization or targeted marketing must be tied to a consent record that can be queried and honored (including opt-out) in real time across every channel it's used in — see Risk & Compliance for the regulatory basis."),
            ("One Customer Identity Graph", "Store purchase history, digital browsing behavior, loyalty program activity, and customer service interactions should resolve to a single customer identity graph, not siloed per-channel profiles. This is what makes cross-channel personalization and the unified return-history requirement (Fulfillment domain) possible."),
        ],
        policies=[
            ("PII Classification Required Before Model Training", True, "Any dataset used to train a personalization or recommendation model must have its fields classified for PII/sensitivity before training begins. Training on unclassified data is a mandatory-blocking finding — this is what prevents inadvertent use of, e.g., payment-adjacent data in a marketing model."),
            ("Recommendation Model Explainability Minimum", False, "Product recommendation and search-ranking models should support at least feature-level explainability (which signals drove a given recommendation), sufficient to answer customer or regulator questions about why something was shown, even if not full interpretability."),
        ],
        guidelines=[
            ("Build vs. Buy for Personalization", "Default to a commercial personalization/recommendation platform unless the retailer's differentiation strategy (per Business Strategy) specifically depends on proprietary ranking logic that off-the-shelf platforms cannot support — this follows Application Architecture's buy-commodity principle applied to the AI/ML case specifically."),
        ],
        examples=[
            ("Cross-Channel Personalization Consent Gap", "Request: extend personalization from digital-only to also personalize store associate recommendations via a clienteling app.\n\nFinding: current consent capture only covers digital cookie-based tracking; there is no consent record for using loyalty purchase history in a store-facing tool.\n\nRecommendation: Standard-to-Major impact depending on scale. Blocked pending Risk & Compliance review of whether existing consent language covers this use, or whether a new consent flow is required before launch."),
        ],
    ),
    dict(
        slug="security", display="Security Architecture",
        desc="Threat modeling, zero-trust, PCI-DSS technical controls, application/API/store-network security.",
        authority="Governance — veto power",
        principles=[
            ("Assume Breach, Design for Containment", "Every architecture must assume some component will eventually be compromised and be designed to limit blast radius — network segmentation, least-privilege access, and no single credential with access to both payment and customer PII systems."),
            ("Security Reviews Scale With Blast Radius, Not Team Preference", "The depth of security review required is a function of what could go wrong (customer PII exposure, payment data exposure, store network compromise), not the size or seniority of the requesting team. A small team's checkout change gets the same rigor as a large team's, if the blast radius is the same."),
        ],
        policies=[
            ("No Raw Cardholder Data at Rest", True, "Identical to and directly enforcing the Payments domain policy of the same name — Security has veto authority to enforce it independent of Payments' own review, as a second, independent check on the single highest-severity risk in a retail environment."),
            ("Store Network Segmentation Mandatory", True, "POS, corporate store network, and guest WiFi must be on segregated network segments with no default routing between them. This directly enforces the Omnichannel domain's store-network policy with veto authority."),
            ("External API Authentication Required", True, "No API exposed to partners, marketplaces, or third-party carriers may be unauthenticated or use a shared static API key with no rotation. This is mandatory because static, unrotated credentials are the most common root cause of retail supply-chain breaches."),
        ],
        guidelines=[
            ("Threat Modeling Trigger Criteria", "Run a full STRIDE threat model for any proposal introducing: a new external-facing endpoint, a new class of data exposure (e.g. first time exposing loyalty data externally), or a new trust boundary (e.g. new third-party integration with write access to an internal system)."),
        ],
        examples=[
            ("Marketplace Integration Threat Model", "Request: threat model for the new marketplace channel integration (see Catalog & Product example).\n\nFindings: marketplace webhook endpoint initially proposed with no signature verification — Spoofing/Tampering risk, HIGH severity.\n\nVeto Decision: VETO ISSUED pending signature verification implementation — this violates the external API authentication policy above. Path to lift veto: implement HMAC signature verification on all inbound marketplace webhooks before go-live."),
        ],
    ),
    dict(
        slug="risk-compliance", display="Risk Management & Compliance",
        desc="PCI-DSS program compliance, GDPR/CCPA/consumer privacy, consumer protection law, risk appetite, GRC obligations.",
        authority="Governance — escalation power",
        principles=[
            ("Regulatory Scope Follows Data, Not Geography Alone", "A retailer serving customers across jurisdictions must apply the most stringent applicable regulation to a given data flow by default (e.g. GDPR-equivalent handling for any EU customer data regardless of where systems are hosted), rather than trying to maintain separate compliance postures per region for shared systems."),
            ("Consent and Retention Are Linked, Not Independent", "Data retention schedules must be tied to the original purpose/consent basis for collecting the data. Data collected for order fulfillment cannot be silently repurposed for marketing retention without a fresh consent basis."),
        ],
        policies=[
            ("Annual PCI-DSS Attestation Required", True, "The organization must maintain current PCI-DSS attestation of compliance (SAQ or full assessment, depending on transaction volume) at all times; any architecture change expanding cardholder data scope resets the assessment clock and must be flagged before implementation, not discovered at annual audit."),
            ("Consumer Data Deletion Requests Honored Within Statutory Window", True, "Verified consumer data deletion/access requests (CCPA, GDPR, and equivalent) must be technically fulfillable within the statutory response window across all systems holding customer data, including backups and downstream analytics copies. Architecture that cannot support this (e.g. data replicated to a system with no deletion API) is a mandatory finding."),
        ],
        guidelines=[
            ("Risk Rating Method", "Rate identified risks as LOW/MEDIUM/HIGH/CRITICAL based on Likelihood x Impact, where Impact considers both direct financial exposure and regulatory/reputational exposure. CRITICAL ratings trigger mandatory escalation per the escalation matrix regardless of likelihood."),
        ],
        examples=[
            ("Cross-Border Customer Data Replication Review", "Request: assess a proposal to replicate customer order data to a new regional data center for latency reasons.\n\nFinding: proposed target region has no data processing agreement in place and the replication would include EU customer records.\n\nRisk Rating: HIGH — cross-border transfer without adequate safeguards.\n\nRecommendation: escalate per the Regulatory Uncertainty trigger in the escalation matrix; require Legal to confirm an adequate transfer mechanism (SCCs or equivalent) before this proceeds, or scope the replication to exclude EU customer records."),
        ],
    ),
    dict(
        slug="red-team", display="Red Team",
        desc="Adversarial challenge of council proposals — assumption testing, failure-mode analysis, groupthink detection. No veto.",
        authority="Challenge only — no veto",
        principles=[
            ("Your Job Is to Break It, Not Bless It", "Red Team output that reads like an endorsement has failed at its job. Every review must surface genuine weaknesses, even in strong proposals — if none are found, the review should say so explicitly and explain why, not default to silence."),
            ("Confidence Language Is a Trigger, Not a Conclusion", "Phrases like 'we're confident this is safe' or 'this is a well-understood pattern' anywhere in a council deliberation should be treated as a prompt to look harder, not as a signal to stand down — that language is exactly where groupthink hides."),
        ],
        policies=[],
        guidelines=[
            ("Retail-Specific Challenge Lenses", "Beyond the general challenge framework, apply retail-specific adversarial lenses: what happens at 50x normal traffic (peak event)? What happens if this fails during the two weeks around Black Friday, when change freezes are typically in effect? What does a fraud ring see in this flow that a legitimate customer doesn't? What breaks first if the store network goes down mid-transaction?"),
        ],
        examples=[
            ("BOPIS Proposal Challenge", "Reviewing the BOPIS launch proposal (see Omnichannel example).\n\nWeaknesses identified: (1) the soft-hold TTL design assumes customers pick up within the promised window — no analysis of what fraction historically don't, and whether repeated no-shows create a gaming vector for inventory manipulation. (2) No answer for what happens if a store's local system is offline (per Omnichannel's offline principle) at the exact moment of a BOPIS pickup attempt. (3) Confidence rated MEDIUM, not LOW — the core design is sound, but ship without answering (1) and (2) and the failure mode will surface in the first peak season, not before."),
        ],
    ),
]

SHARED_PRINCIPLES = [
    ("Evidence Over Opinion", "Every architectural recommendation must be grounded in data (system telemetry, cost figures, customer impact metrics) or an explicitly flagged assumption. Opinion presented as fact is not acceptable council output."),
    ("Customer Trust Is Non-Negotiable", "Where a technical trade-off pits development speed or cost against customer data protection or payment security, the trust-preserving option wins by default. Exceptions require explicit Risk & Compliance and Security sign-off, not a unilateral engineering call."),
    ("One Truth Per Domain of Data", "Every category of business data (product, inventory, order, customer identity) has exactly one system of record. This principle recurs across nearly every domain's own principles because it is the single most common failure mode in retail architecture — silently drifting 'truths' between store and digital."),
    ("Design for Peak, Not Steady State", "Retail load is inherently seasonal and event-driven. Capacity, cost, and resilience planning must be validated against realistic peak scenarios, not steady-state averages."),
    ("Channel Parity by Default", "Store and digital customers should receive equivalent core experiences (pricing, promotions, order status visibility, return policy) unless a specific strategic reason justifies divergence — divergence should be the deliberate exception, not the accidental default."),
    ("Buy Commodity, Build Differentiation", "Applies portfolio-wide: build engineering effort where it creates genuine competitive differentiation; buy or adopt SaaS where the capability is table-stakes across the industry."),
    ("Security and Privacy by Design, Not Bolted On", "Security and privacy requirements are gathered at the start of architecture work, not retrofitted after a design is finalized. Retrofitting is both more expensive and more likely to leave gaps."),
    ("Reversibility Under Uncertainty", "When two options are otherwise comparable, prefer the one that is easier to reverse. This is the tie-breaker of last resort in the conflict-resolution hierarchy for a reason — retail architecture operates under real uncertainty about customer behavior and seasonal demand."),
    ("Proportional Governance", "The depth of council review scales with decision impact and blast radius, not with team size, seniority, or how urgently someone wants to ship. A Minor decision gets a quick pass; a Critical one gets the full council plus Red Team plus human sign-off."),
    ("Integration Through Contracts, Not Tribal Knowledge", "System integration points must be documented, versioned contracts (API specs, event schemas) — not undocumented behavior that happens to work because two engineers know how it works today."),
    ("Data Follows Consent", "Customer data use is scoped to what the customer consented to at collection time. Repurposing data for a new use requires a new consent basis, not a retroactive justification."),
    ("Every System Has a Named Owner", "No production system, integration, or data store may lack a named accountable owner. This applies enterprise-wide, beyond the Application Architecture domain where it's also stated, because orphaned ownership is a recurring root cause across incident postmortems in every domain."),
]

TECH_RADAR = [
    ("Composable Commerce (MACH) Architecture", "ADOPT", "Microservices, API-first, cloud-native, headless commerce architecture. Aligns with Application Architecture's build/buy principles and Integration's event-driven principle."),
    ("Real-Time Inventory Event Streaming", "ADOPT", "Event-driven inventory sync (Kafka/equivalent) replacing batch WMS-to-store sync. Prerequisite for BOPIS and endless-aisle capabilities per Omnichannel domain."),
    ("Headless / API-First Storefront", "TRIAL", "Decoupled frontend from commerce backend. Trial status pending a full performance and SEO impact assessment on the current storefront."),
    ("Vector Search for Product Discovery", "TRIAL", "Semantic/vector-based search to complement traditional keyword search, particularly for natural-language and visual search use cases."),
    ("Composable PSP Orchestration Layer", "TRIAL", "Multi-PSP orchestration/failover layer to satisfy the Payments domain's peak-event failover policy without hard-coding a single PSP integration."),
    ("Generative AI for Customer Service", "ASSESS", "Under assessment for customer service deflection use cases. Requires Data & AI explainability guideline compliance and Risk & Compliance review of any customer-facing automated decisioning."),
    ("Clienteling Mobile Apps for Store Associates", "ASSESS", "In-store associate tools surfacing customer history/recommendations. Blocked on the Data & AI cross-channel consent gap identified in that domain's worked example."),
    ("Point-to-Point Batch File Integration", "HOLD", "Legacy integration pattern. New integrations must use the API gateway/event bus per Integration Architecture policy; existing point-to-point batch integrations are migration candidates, not a pattern to extend."),
    ("Store-Local Product Databases (Unsynced)", "HOLD", "Any pattern where store systems maintain independent, unsynced local product/inventory copies is on hold — conflicts directly with the One Truth Per Domain of Data principle."),
    ("Single-PSP Hard Dependency", "HOLD", "New payment integrations designed against a single PSP with no abstraction/failover path are on hold per the Payments domain's peak-event failover policy."),
]

REFERENCE_ARCHITECTURES = {
    "cloud-native.md": ("ReferenceArchitecture", "Cloud-Native Retail Platform Baseline",
        "Baseline pattern: multi-AZ cloud deployment, containerized services, API gateway at the edge, event bus for cross-domain integration, autoscaling validated against peak-load models. Applies to all customer-facing domains (Commerce & Checkout, Order Management, Search & Discovery, Payments)."),
    "omnichannel-inventory.md": ("ReferenceArchitecture", "Unified Omnichannel Inventory Reference Architecture",
        "WMS and store inventory systems publish inventory-changed events to a shared event bus; a unified inventory availability service consumes both streams and serves reads to Order Management, Search & Discovery, and Omnichannel & Store Systems. Store-local systems maintain a short-TTL cache for offline resilience, reconciled on reconnect. This is the concrete implementation of the One Truth Per Domain of Data principle for inventory specifically, and directly unblocks the BOPIS capability referenced across the Business Strategy, Omnichannel, and Application Architecture worked examples."),
    "payment-processing.md": ("ReferenceArchitecture", "PCI-Minimized Payment Processing Reference Architecture",
        "All payment surfaces (digital checkout, store POS, call-center order entry) use PSP-hosted tokenization fields; no retailer-owned system receives raw cardholder data. Multi-PSP orchestration layer provides failover for peak events. Store POS traffic is network-segmented per Security's mandatory policy. This is the concrete implementation shared by the Payments, Security, and Omnichannel domains' cardholder-data and network-segmentation policies."),
}

STANDARDS = {
    "adr-template.md": ("Standard", "Architecture Decision Record Template",
        "Required ADR sections: Decision summary (one sentence). Context (problem and why now). Decision (what we're doing). Rationale (why this option over alternatives). Trade-offs (what we're accepting). Agents consulted and any dissenting positions. Risks and mitigations. Next steps and owners."),
    "naming-conventions.md": ("Standard", "Naming Conventions",
        "Services: lowercase-hyphenated, prefixed by owning domain where ambiguous (e.g. payments-tokenization-service). Events: PastTenseVerb.Domain.Entity (e.g. InventoryChanged.Fulfillment.SKU). ADRs: ADR-NNNN-short-title.md, numbered sequentially in outputs/adr-register.md."),
    "documentation-standards.md": ("Standard", "Documentation Standards",
        "Every system in the application portfolio must have: an owner (per the enterprise-wide ownership principle), an up-to-date integration diagram, and a data classification for any customer or payment data it touches. Documentation is reviewed at each major ADR affecting the system, not on a separate fixed schedule that tends to lapse."),
}

AGENT_TOOLS = "Read, Grep, Glob"
AGENT_MODEL = "sonnet"


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")


def slugify(title):
    return title.lower().replace(" ", "-").replace("/", "-").replace("&", "and").replace(",", "").replace("'", "").replace("(", "").replace(")", "")


def gen_domain(d):
    base = f"knowledge/{d['slug']}"
    entries = []  # (filename, type, title)

    for title, body in d["principles"]:
        fname = f"principle-{slugify(title)}.md"
        content = fm("Principle", title, body.split(".")[0] + ".", [d["slug"], "principle"]) + f"\n\n# {title}\n\n{body}\n"
        write(f"{base}/{fname}", content)
        entries.append((fname, "Principle", title))

    for title, mandatory, body in d["policies"]:
        fname = f"policy-{slugify(title)}.md"
        content = fm("Policy", title, body.split(".")[0] + ".", [d["slug"], "policy"], mandatory=mandatory) + f"\n\n# {title}\n\n{'**[MANDATORY]**' if mandatory else '[RECOMMENDED]'}\n\n{body}\n"
        write(f"{base}/{fname}", content)
        entries.append((fname, "Policy" + (" [MANDATORY]" if mandatory else ""), title))

    for title, body in d["guidelines"]:
        fname = f"guideline-{slugify(title)}.md"
        content = fm("Guideline", title, body.split(".")[0] + ".", [d["slug"], "guideline"]) + f"\n\n# {title}\n\n{body}\n"
        write(f"{base}/{fname}", content)
        entries.append((fname, "Guideline", title))

    for title, body in d["examples"]:
        fname = f"example-{slugify(title)}.md"
        content = fm("Example", title, body.split(".")[0] + ".", [d["slug"], "example"]) + f"\n\n# {title}\n\n{body}\n"
        write(f"{base}/{fname}", content)
        entries.append((fname, "Example", title))

    # domain index.md
    lines = [f"# {d['display']} — Domain Index", "", d["desc"], "", f"**Authority:** {d['authority']}", "", "## Concepts in this domain", ""]
    lines.append("| File | Type | Title |")
    lines.append("|---|---|---|")
    for fname, type_, title in entries:
        lines.append(f"| [{fname}]({fname}) | {type_} | {title} |")
    lines.append("")
    lines.append("See also: `../shared/index.md` for enterprise-wide principles, tech radar, standards, and reference architectures that apply across all domains.")
    write(f"{base}/index.md", "\n".join(lines))
    return entries


def gen_shared():
    entries = []
    for title, body in SHARED_PRINCIPLES:
        fname = f"principle-{slugify(title)}.md"
        content = fm("Principle", title, body.split(".")[0] + ".", ["shared", "enterprise-principle"]) + f"\n\n# {title}\n\n{body}\n"
        write(f"knowledge/shared/{fname}", content)
        entries.append((fname, "Principle", title))

    glossary_body = """# Retail EA Council Glossary

- **BOPIS** — Buy Online, Pickup In Store
- **PIM** — Product Information Management (system of record for product data)
- **OMS** — Order Management System (orchestrates order lifecycle across fulfillment sources)
- **WMS** — Warehouse Management System
- **PSP** — Payment Service Provider
- **PCI-DSS** — Payment Card Industry Data Security Standard
- **3PL** — Third-Party Logistics provider
- **DAM** — Digital Asset Management
- **P2PE** — Point-to-Point Encryption (payment terminal security standard)
- **SKU** — Stock Keeping Unit
- **NDCG** — Normalized Discounted Cumulative Gain (a search relevance metric)
- **Endless Aisle** — In-store kiosk/tablet experience letting customers order out-of-stock items for delivery/pickup
- **Wardrobing** — Return fraud pattern where an item is purchased, used, then returned as unused
"""
    write("knowledge/shared/glossary.md", fm("Glossary", "Retail EA Council Glossary", "Common terminology used across all council domains.", ["shared", "glossary"]) + "\n\n" + glossary_body)
    entries.append(("glossary.md", "Glossary", "Retail EA Council Glossary"))

    # tech radar
    radar_lines = ["# Technology Radar — Domain Index", "", "| Technology | Status | File |", "|---|---|---|"]
    for title, status, body in TECH_RADAR:
        fname = f"{slugify(title)}.md"
        content = fm("TechRadarEntry", title, body.split(".")[0] + ".", ["shared", "tech-radar", status.lower()], extra={"status": status}) + f"\n\n# {title}\n\n**Status:** {status}\n\n{body}\n"
        write(f"knowledge/shared/tech-radar/{fname}", content)
        radar_lines.append(f"| {title} | {status} | [{fname}]({fname}) |")
    write("knowledge/shared/tech-radar/index.md", "\n".join(radar_lines))

    # standards
    for fname, (type_, title, body) in STANDARDS.items():
        content = fm(type_, title, body.split(".")[0] + ".", ["shared", "standard"]) + f"\n\n# {title}\n\n{body}\n"
        write(f"knowledge/shared/standards/{fname}", content)

    # reference architectures
    for fname, (type_, title, body) in REFERENCE_ARCHITECTURES.items():
        content = fm(type_, title, body.split(".")[0] + ".", ["shared", "reference-architecture"]) + f"\n\n# {title}\n\n{body}\n"
        write(f"knowledge/shared/reference-architectures/{fname}", content)

    return entries


def gen_bundle_index(domain_entry_counts):
    lines = ["# Retail EA Council — Knowledge Bundle Index (OKF)", "",
             "This is the OKF bundle root. Read this file first (per `SKILL.md`), then drill into the domain",
             "sub-bundle relevant to the question at hand.", "",
             "## Domain sub-bundles", "",
             "| Domain | Path | Concepts |", "|---|---|---|"]
    for d in DOMAINS:
        lines.append(f"| {d['display']} | `{d['slug']}/index.md` | {domain_entry_counts[d['slug']]} |")
    lines += ["", "## Enterprise-wide (shared)", "",
              "| Content | Path |", "|---|---|",
              "| 12 enterprise architecture principles | `shared/index.md` |",
              "| Technology radar (ADOPT/TRIAL/ASSESS/HOLD) | `shared/tech-radar/index.md` |",
              "| Glossary | `shared/glossary.md` |",
              "| Standards (ADR template, naming, documentation) | `shared/standards/` |",
              "| Reference architectures | `shared/reference-architectures/` |",
              "", "See `log.md` for the chronological change history of this bundle."]
    write("knowledge/index.md", "\n".join(lines))


def gen_shared_index(entries):
    lines = ["# Shared / Enterprise-Wide — Domain Index", "",
             "Enterprise-wide principles, glossary, tech radar, standards, and reference architectures that apply",
             "across all 15 council domains.", "",
             "## Concepts", "", "| File | Type | Title |", "|---|---|---|"]
    for fname, type_, title in entries:
        lines.append(f"| [{fname}]({fname}) | {type_} | {title} |")
    lines += ["", "| tech-radar/index.md | Index | Technology Radar |",
              "| standards/ | Standards | ADR template, naming, documentation |",
              "| reference-architectures/ | ReferenceArchitecture | Cloud-native, omnichannel inventory, payment processing |"]
    write("knowledge/shared/index.md", "\n".join(lines))


def gen_log():
    write("knowledge/log.md", f"""# Bundle Change Log

## [{TS[:10]}] initial | Retail EA Council knowledge bundle created
Initial OKF bundle: 15 domain sub-bundles + shared enterprise-wide content, generated for the
retail EA architecture council. See `council-config.md` at the repo root for the full roster.
""")


AGENT_DESCRIPTIONS = {
    "business-strategy": "Advisory domain agent for business capability mapping and strategy alignment. Use PROACTIVELY for capability assessments, new business-line/channel decisions, or strategy-to-technology alignment. No special authority.",
    "catalog-product": "Advisory domain agent for PIM, catalog data model, and taxonomy. Use PROACTIVELY for product data model changes, taxonomy changes, marketplace feed mapping, or DAM/PIM boundary questions. No special authority.",
    "search-discovery": "Advisory domain agent for search engines, indexing, relevance, and product discovery. Use PROACTIVELY for search platform evaluation, relevance/ranking changes, or discovery UX architecture. No special authority.",
    "commerce-checkout": "Advisory domain agent for cart, checkout flow, session/state, and checkout-time pricing/promotions. Use PROACTIVELY for checkout redesigns, cart persistence issues, or promotion-stacking logic. No special authority.",
    "order-management": "Advisory domain agent for order lifecycle, order orchestration, and order status tracking. Use PROACTIVELY for OMS design, split-fulfillment orchestration, or order status/notification questions. No special authority.",
    "payments": "Advisory domain agent for payment processing, PCI-DSS scope, tokenization, PSPs, and fraud/chargebacks. Use PROACTIVELY \u2014 and always alongside Security \u2014 for any request touching cardholder data, PSP integration, or fraud rules. No special authority (Security holds the veto for cardholder-data violations).",
    "omnichannel-store": "Advisory domain agent for POS, BOPIS/ship-from-store, endless aisle, in-store inventory visibility, and store network resilience. Use PROACTIVELY for any request mentioning stores, POS, BOPIS, curbside, or in-store systems. No special authority.",
    "fulfillment-logistics": "Advisory domain agent for warehouse/inventory management, shipping/carrier integration, returns, and 3PL. Use PROACTIVELY for WMS design, carrier integration, returns processing, or inventory-accuracy questions. No special authority.",
    "application-architecture": "Advisory domain agent for application portfolio, build/buy/SaaS decisions, and tech radar placement. Use PROACTIVELY for new application adoption, decommission, vendor/SaaS evaluation, or portfolio rationalization. No special authority.",
    "integration-architecture": "Advisory domain agent for APIs, events, middleware, and cross-system data flows. Use PROACTIVELY for new integration/API design, event schema questions, or point-to-point integration risk. No special authority.",
    "technology-infrastructure": "Advisory domain agent for cloud hosting, peak-load capacity planning, DR, and store network infrastructure. Use PROACTIVELY for capacity planning, peak-event (Black Friday) readiness, or DR/HA requests. No special authority.",
    "data-ai": "Advisory domain agent for data governance, customer identity graph, personalization/recommendation systems, and AI/ML strategy. Use PROACTIVELY for personalization initiatives, consent/PII classification, or any AI/ML model proposal. No special authority.",
    "security": "Governance cross-cut agent with VETO POWER over proposals violating a [MANDATORY] security policy. Use PROACTIVELY \u2014 and always for Standard impact and above \u2014 for requests involving cardholder data, external-facing APIs, store network design, or PII exposure. Runs STRIDE threat modeling and can block a decision outright.",
    "risk-compliance": "Governance cross-cut agent with ESCALATION POWER for regulatory/privacy/risk-appetite concerns (PCI-DSS program compliance, GDPR/CCPA, consumer protection). Use PROACTIVELY \u2014 and always for Major impact and above \u2014 for requests mentioning cross-border data, consent, deletion requests, or return/payment fraud thresholds. Cannot veto but can force human escalation on CRITICAL risk ratings.",
    "red-team": "Adversarial challenge agent. Its job is to break the proposal, not endorse it. Use PROACTIVELY for Critical impact decisions, novel patterns (e.g. first-of-its-kind omnichannel feature), irreversible changes, or whenever the council sounds overconfident. Cannot veto \u2014 challenge only.",
}


def gen_subagent(d):
    slug = d["slug"]
    content = f"""---
name: {slug}
description: {AGENT_DESCRIPTIONS[slug]}
tools: {AGENT_TOOLS}
model: {AGENT_MODEL}
---

# {d['display']}

## Identity

You are the **{d['display']}** specialist on the Retail Enterprise Architecture Council. Scope: {d['desc']}

**Authority:** {d['authority']}

## Grounding Protocol (read before responding, in this order)

This council's knowledge base is an **OKF bundle** at `knowledge/`, not a single file to read top to bottom.
Follow `SKILL.md` at the repo root for the general navigation procedure. Specifically for your domain:

1. **Read `knowledge/{slug}/index.md`** \u2014 the catalog of every concept file in your domain, with its `type`.
2. **Read every `policy-*.md` file in `knowledge/{slug}/`** \u2014 check every recommendation against policies
   with `mandatory: true` in their frontmatter. A mandatory policy violation eliminates an option outright.
3. **Read every `principle-*.md` file in `knowledge/{slug}/`** \u2014 ground every recommendation in a named
   principle.
4. **Read `guideline-*.md` files** relevant to the specific question \u2014 apply the methodology described.
5. **Skim `example-*.md` files** if a similar worked example exists \u2014 match its structure and rigor, and
   note that several examples cross-reference other domains' worked examples (the bundle is a linked graph,
   not isolated silos \u2014 follow those links when they're relevant to your assessment).
6. **Read `knowledge/shared/index.md`** \u2014 the 12 enterprise-wide principles take precedence over
   domain-specific preferences when they conflict. Check `knowledge/shared/tech-radar/index.md` if your
   assessment involves a specific technology choice, and `knowledge/shared/reference-architectures/` if a
   reference pattern already exists for the scenario.

**Stay within your domain scope.** Do not answer for other agents \u2014 if a question is out of scope, say so
and name which agent should own it.

**Output format:** structure your response as: current-state assessment, recommendation, domain-specific
risks, dependencies on peer domains, and anything Security or Risk & Compliance should review. Cite the
specific concept file (principle/policy) backing each claim.

**Data note:** this deployment does not have live system connectors (OMS, PIM, WMS, POS) wired in yet.
When your assessment would normally cite live operational data, state the assumption explicitly rather
than inventing figures.
"""
    write(f".claude/agents/{slug}.md", content)


def main():
    domain_entry_counts = {}
    for d in DOMAINS:
        entries = gen_domain(d)
        domain_entry_counts[d["slug"]] = len(entries)
        gen_subagent(d)
    shared_entries = gen_shared()
    gen_shared_index(shared_entries)
    gen_bundle_index(domain_entry_counts)
    gen_log()
    print("Done.")
    print("Domains:", len(DOMAINS))
    print("Total domain concept files:", sum(domain_entry_counts.values()))


if __name__ == "__main__":
    main()
