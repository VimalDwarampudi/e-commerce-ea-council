#!/usr/bin/env python3
"""Adds the OKF 'asset layer' (Table, API, Metric concepts describing actual system
assets, as sample placeholders) to domains that plausibly own them. Run from
/home/claude/retail-build, after generate.py.
"""
import os
import re

TS = "2026-07-24T00:00:00Z"


def fm(type_, title, description, tags, extra=None):
    lines = ["---", f"type: {type_}", f"title: {title}", f"description: {description}",
              f"tags: [{', '.join(tags)}]", f"timestamp: {TS}", "status: PLACEHOLDER"]
    if extra:
        for k, v in extra.items():
            lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines)


def slugify(title):
    return title.lower().replace(" ", "-").replace("/", "-").replace("&", "and").replace(",", "").replace("'", "").replace("(", "").replace(")", "")


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")


PLACEHOLDER_NOTE = (
    "\n\n> **PLACEHOLDER — sample only.** This concept illustrates the shape an asset "
    "concept should take once a live source system is connected (see `CLAUDE.md` \"Data "
    "Sources\"). Field names, endpoint paths, and metric values below are representative, "
    "not verified against a real system. Replace the body with the actual schema/contract/"
    "metric definition and remove `status: PLACEHOLDER` from the frontmatter when done."
)

# slug -> list of (asset_type, title, description_sentence, body_markdown)
ASSETS = {
    "catalog-product": [
        ("Table", "products", "Core product record owned by the PIM; every other system's product view is a projection of this table.",
         "**Owning system:** PIM (placeholder: e.g. Salsify, Akeneo, or in-house)\n\n"
         "| Field | Type | Notes |\n|---|---|---|\n"
         "| sku | string, PK | Stock keeping unit, immutable |\n"
         "| title | string | |\n"
         "| description | text | |\n"
         "| category_id | string, FK -> categories.id | Enforces the taxonomy contract (see `policy-taxonomy-is-a-contract` principle) |\n"
         "| price | decimal | Base price; channel/region overrides live in a separate pricing table, not here |\n"
         "| status | enum(active, discontinued, seasonal) | |\n"
         "| compliance_attributes | jsonb | Country of origin, safety certs — added per the marketplace-onboarding example |\n"
         "| updated_at | timestamp | |"),
        ("API", "pim-export-api", "The PIM's published contract for downstream consumers (storefront, search index, marketplace feeds, store systems).",
         "**Contract:** REST, versioned (`/v2/products`)\n\n"
         "`GET /v2/products/{sku}` — full product record\n"
         "`GET /v2/products?category={id}&updated_since={ts}` — incremental sync\n"
         "`POST /v2/products/{sku}/compliance-attributes` — used by the marketplace-onboarding flow\n\n"
         "**Consumers:** Search & Discovery index pipeline, digital storefront, marketplace feed generator, store systems (via Omnichannel's inventory service). This is the only sanctioned path per the PIM-as-system-of-record policy — no consumer should read the PIM's underlying database directly."),
    ],
    "search-discovery": [
        ("Metric", "zero-result-rate", "Share of search queries returning no results; a leading indicator of catalog or taxonomy gaps per this domain's monitoring policy.",
         "**Definition:** `count(queries WHERE result_count = 0) / count(all queries)`, rolled up daily.\n\n"
         "**Target (placeholder):** < 2% overall; < 5% for any single top-20 category.\n\n"
         "**Owning system:** search platform analytics (placeholder: e.g. Algolia Insights, Elastic dashboards).\n\n"
         "**Consumed by:** Catalog & Product Information (taxonomy gap signal), Data & AI (query understanding gaps)."),
    ],
    "commerce-checkout": [
        ("Table", "carts", "Cart state, identity-scoped per the cross-device persistence principle.",
         "**Owning system:** cart service\n\n"
         "| Field | Type | Notes |\n|---|---|---|\n"
         "| cart_id | string, PK | |\n"
         "| customer_identity_id | string, FK -> data-ai customer identity graph | Not device- or session-scoped |\n"
         "| line_items | jsonb | sku, qty, applied_promo_id per line |\n"
         "| channel_origin | enum(web, app, store) | For channel-parity reporting, not for splitting cart ownership |\n"
         "| updated_at | timestamp | |\n"
         "| expires_at | timestamp | Soft expiry; see cross-device persistence principle for why this must be long enough to survive a channel switch |"),
        ("Metric", "cart-abandonment-rate", "Share of created carts that don't convert to an order; a primary checkout health metric.",
         "**Definition:** `1 - (count(carts with order_id) / count(all carts created in period))`\n\n"
         "**Target (placeholder):** directional only — retail benchmarks vary widely by vertical; track trend, not an absolute target, and segment by channel to catch store/digital divergence early (see the channel-parity enterprise principle)."),
    ],
    "order-management": [
        ("Table", "orders", "System-of-record order header and lifecycle state; fulfillment splits reference this, never replace it.",
         "**Owning system:** OMS\n\n"
         "| Field | Type | Notes |\n|---|---|---|\n"
         "| order_id | string, PK | |\n"
         "| customer_identity_id | string, FK | |\n"
         "| status | enum(placed, allocated, picking, shipped, delivered, cancelled, returned) | Every transition logged — see order-state-transitions-are-auditable principle |\n"
         "| fulfillment_legs | jsonb array | One entry per split fulfillment source (warehouse, store) |\n"
         "| placed_at, updated_at | timestamp | |"),
        ("API", "oms-status-api", "The OMS's published contract for order status, consumed by every channel per the single-system-of-record policy.",
         "`GET /v1/orders/{order_id}` — current status + fulfillment legs\n"
         "`GET /v1/orders/{order_id}/history` — full auditable transition log\n"
         "`POST /v1/orders/{order_id}/cancel` — server-side enforcement of the cancellation-window policy\n\n"
         "**Consumers:** digital storefront, store POS, customer service tools, notification system. No consumer may cache order status as its own source of truth beyond a short TTL."),
    ],
    "payments": [
        ("Table", "transactions", "Payment transaction ledger. Contains no raw cardholder data — enforces the mandatory no-raw-cardholder-data-at-rest policy by design.",
         "**Owning system:** Payments service, backed by the PSP's tokenized vault\n\n"
         "| Field | Type | Notes |\n|---|---|---|\n"
         "| transaction_id | string, PK | |\n"
         "| order_id | string, FK -> order-management.orders | |\n"
         "| payment_token | string | PSP-issued token; never a PAN |\n"
         "| amount, currency | decimal, string | |\n"
         "| status | enum(authorized, captured, declined, refunded, chargeback) | |\n"
         "| fraud_signal_score | decimal | See risk-appetite in Risk & Compliance for threshold governance |\n"
         "| processed_at | timestamp | |"),
        ("API", "tokenization-endpoint", "PSP-hosted field/tokenization endpoint — the only path by which any checkout surface (digital, POS, call center) may collect payment detail, per the PCI-scope-minimization principle.",
         "`POST /v1/tokenize` (PSP-hosted, not retailer infrastructure) — returns a token, never touches retailer servers with raw PAN\n"
         "`POST /v1/charge` — retailer-initiated charge using a token, via the PSP orchestration layer (see the multi-PSP failover policy)\n\n"
         "**Note:** the actual endpoint is whichever PSP is integrated (placeholder — e.g. Stripe, Adyen, Braintree); this concept documents the retailer-side integration contract, not the PSP's own API docs."),
        ("Metric", "chargeback-rate", "Share of transactions disputed as chargebacks; a fraud and PSP-relationship health signal.",
         "**Definition:** `count(transactions with status=chargeback) / count(captured transactions)`, rolled up monthly.\n\n"
         "**Target (placeholder):** most card networks flag monitoring programs above ~0.9-1%; treat approaching that threshold as a Risk & Compliance escalation trigger, not just a Payments metric to watch quietly."),
    ],
    "omnichannel-store": [
        ("Table", "store-inventory", "Per-location inventory count, feeding the unified inventory availability service alongside WMS per the reference architecture.",
         "**Owning system:** store inventory system\n\n"
         "| Field | Type | Notes |\n|---|---|---|\n"
         "| store_id | string, FK | |\n"
         "| sku | string, FK -> catalog-product.products | |\n"
         "| on_hand_qty | int | |\n"
         "| soft_hold_qty | int | BOPIS reservations per the soft-hold TTL pattern |\n"
         "| last_synced_at | timestamp | Must be near-real-time per the inventory-visibility-is-real-time-or-its-wrong principle — flag if this drifts beyond a few minutes |"),
        ("Metric", "bopis-pickup-fulfillment-rate", "Share of BOPIS orders successfully picked up within the promised window vs. cancelled/no-show — the concrete measure of whether the soft-hold TTL design (see Omnichannel's worked example) is actually working.",
         "**Definition:** `count(BOPIS orders picked up within window) / count(BOPIS orders placed)`\n\n"
         "**Target (placeholder):** track alongside no-show rate; a rising no-show rate combined with inventory lockup complaints is the specific failure mode Red Team flagged in the BOPIS challenge example — this metric is what would surface it."),
    ],
    "fulfillment-logistics": [
        ("Table", "warehouse-inventory", "Warehouse-side inventory of record, feeding the unified inventory availability service alongside store-inventory.",
         "**Owning system:** WMS\n\n"
         "| Field | Type | Notes |\n|---|---|---|\n"
         "| warehouse_id | string, FK | |\n"
         "| sku | string, FK -> catalog-product.products | |\n"
         "| on_hand_qty, allocated_qty | int | |\n"
         "| last_synced_at | timestamp | Event-driven per the reference architecture, not batch |"),
        ("Metric", "on-time-delivery-rate", "Share of shipments delivered by the promised date; primary carrier and fulfillment health metric.",
         "**Definition:** `count(shipments delivered <= promised_date) / count(all shipments)`, segmented by carrier and fulfillment source (warehouse vs. ship-from-store).\n\n"
         "**Target (placeholder):** track per-carrier to catch a single underperforming carrier before it drags the aggregate down — feeds carrier-abstraction-layer vendor reviews."),
    ],
    "integration-architecture": [
        ("API", "api-gateway-contract", "The retailer's single external-facing API gateway; every partner, marketplace, and carrier integration must route through this per the mandatory gateway policy.",
         "**Capabilities:** auth (OAuth2/API key), rate limiting, request/response logging, webhook signature verification.\n\n"
         "**Registered integrations (placeholder — populate with actuals):** marketplace channel feeds, carrier tracking webhooks, PSP webhooks.\n\n"
         "No integration should exist that bypasses this gateway for direct system access — that's the specific failure mode caught in the Security domain's marketplace-webhook worked example."),
        ("Metric", "integration-error-rate", "Failed/retried message rate across the event bus and gateway; a fragility signal for the point-to-point-integration-debt principle.",
         "**Definition:** `count(failed or retried messages) / count(all messages)`, segmented by integration.\n\n"
         "**Target (placeholder):** a sustained rise for a single integration is a stronger signal than the aggregate — investigate per-integration, not just in the rolled-up number."),
    ],
    "technology-infrastructure": [
        ("Metric", "peak-load-capacity-headroom", "Validated headroom between current auto-scaled capacity and the peak traffic model, per the design-for-peak-not-average principle.",
         "**Definition:** `(load-tested max sustained throughput - modeled peak traffic) / modeled peak traffic`\n\n"
         "**Target (placeholder):** maintain positive headroom (e.g. >=20%) confirmed by an actual load test before each peak season — not inferred from auto-scaling configuration alone, per the mandatory peak-load-testing policy."),
    ],
    "data-ai": [
        ("Table", "customer_identity", "The unified identity graph resolving store, digital, and loyalty activity to one customer — referenced by carts, orders, and personalization.",
         "**Owning system:** Customer Data Platform (placeholder)\n\n"
         "| Field | Type | Notes |\n|---|---|---|\n"
         "| identity_id | string, PK | |\n"
         "| known_identifiers | jsonb | email, loyalty_id, device_ids — resolved, not raw PII duplicated across systems |\n"
         "| consent_record_id | string, FK -> consent table | Required before this identity's data is used for personalization, per the PII-classification and consent-tracking policies |\n"
         "| created_at | timestamp | |"),
        ("Metric", "personalization-consent-coverage", "Share of identities used in a personalization surface that have a valid, current consent record — the concrete check for the consent-tracking principle.",
         "**Definition:** `count(identities shown personalized content WITH valid consent_record) / count(all identities shown personalized content)`\n\n"
         "**Target (placeholder):** should be effectively 100% by design (personalization should be gated on consent, not audited after the fact) — a non-100% reading here is itself a policy violation worth escalating, not just a metric to trend."),
    ],
    "security": [
        ("Metric", "vulnerability-remediation-sla-compliance", "Share of identified vulnerabilities remediated within their severity-based SLA window.",
         "**Definition:** `count(vulnerabilities remediated within SLA) / count(all vulnerabilities found in period)`, segmented by severity (Critical/High/Medium/Low).\n\n"
         "**Target (placeholder):** Critical findings (e.g. the marketplace webhook signature gap in the worked example) should have a near-100% on-time SLA compliance target; lower severities can tolerate more slack."),
    ],
    "risk-compliance": [
        ("Metric", "deletion-request-response-time", "Time to fulfill a verified consumer data deletion/access request, measured against the statutory window per the mandatory policy of the same domain.",
         "**Definition:** `timestamp(request fulfilled across all systems, including backups/analytics copies) - timestamp(request verified)`\n\n"
         "**Target (placeholder):** must stay under the statutory window (varies by jurisdiction — GDPR and CCPA windows differ); track the actual measured time, not just a target, since the underlying architecture question (can every system holding customer data actually delete on demand?) is what this metric tests."),
    ],
}


def regenerate_domain_index(slug, display, desc, authority):
    base = f"knowledge/{slug}"
    files = sorted(f for f in os.listdir(base) if f.endswith(".md") and f != "index.md")
    rows = []
    for fname in files:
        with open(f"{base}/{fname}") as f:
            head = f.read(600)
        m_type = re.search(r"^type:\s*(.+)$", head, re.M)
        m_title = re.search(r"^title:\s*(.+)$", head, re.M)
        m_mand = re.search(r"^mandatory:\s*true$", head, re.M)
        type_ = m_type.group(1).strip() if m_type else "?"
        if m_mand:
            type_ += " [MANDATORY]"
        title = m_title.group(1).strip() if m_title else fname
        rows.append((fname, type_, title))

    lines = [f"# {display} — Domain Index", "", desc, "", f"**Authority:** {authority}", "",
             "## Concepts in this domain", "", "| File | Type | Title |", "|---|---|---|"]
    for fname, type_, title in rows:
        lines.append(f"| [{fname}]({fname}) | {type_} | {title} |")
    lines += ["", "See also: `../shared/index.md` for enterprise-wide principles, tech radar, standards, and reference architectures that apply across all domains."]
    write(f"{base}/index.md", "\n".join(lines))


# minimal per-domain display/desc/authority needed just for re-writing index.md headers
DOMAIN_META = {
    "catalog-product": ("Catalog & Product Information Architecture", "Product information management (PIM), catalog data model, taxonomy, digital asset management.", "Advisory"),
    "search-discovery": ("Search & Discovery Architecture", "Search engines, indexing, relevance tuning, product discovery, on-site navigation.", "Advisory"),
    "commerce-checkout": ("Commerce & Checkout Architecture", "Shopping cart, checkout flow, session/state management, promotions and pricing at checkout.", "Advisory"),
    "order-management": ("Order Management Architecture", "Order orchestration, order lifecycle state machine, order status tracking, order data model.", "Advisory"),
    "payments": ("Payments Architecture", "Payment processing, PCI-DSS scope, tokenization, payment service providers, fraud detection, chargebacks.", "Advisory"),
    "omnichannel-store": ("Omnichannel & Store Systems Architecture", "Point-of-sale (POS), BOPIS/ship-from-store, endless aisle, in-store inventory visibility, store network resilience.", "Advisory"),
    "fulfillment-logistics": ("Fulfillment & Logistics Architecture", "Warehouse/inventory management (WMS), shipping and carrier integration, returns processing, third-party logistics (3PL).", "Advisory"),
    "integration-architecture": ("Integration Architecture", "APIs, event streams, middleware, data flows between systems, carrier and marketplace integration patterns.", "Advisory"),
    "technology-infrastructure": ("Technology & Infrastructure", "Cloud hosting, runtime platforms, peak-load capacity planning, disaster recovery, store network infrastructure.", "Advisory"),
    "data-ai": ("Data & AI Architecture", "Data governance, customer data platform, personalization and recommendation systems, AI/ML strategy.", "Advisory"),
    "security": ("Security Architecture", "Threat modeling, zero-trust, PCI-DSS technical controls, application/API/store-network security.", "Governance — veto power"),
    "risk-compliance": ("Risk Management & Compliance", "PCI-DSS program compliance, GDPR/CCPA/consumer privacy, consumer protection law, risk appetite, GRC obligations.", "Governance — escalation power"),
}


def main():
    touched = set()
    for slug, items in ASSETS.items():
        for type_, title, desc_sentence, body in items:
            fname = f"{type_.lower()}-{slugify(title)}.md"
            content = fm(type_, title, desc_sentence, [slug, type_.lower(), "placeholder"]) + \
                f"\n\n# {title}\n\n{body}{PLACEHOLDER_NOTE}\n"
            write(f"knowledge/{slug}/{fname}", content)
        touched.add(slug)

    for slug in touched:
        display, desc, authority = DOMAIN_META[slug]
        regenerate_domain_index(slug, display, desc, authority)

    # bundle-level index note
    print(f"Added asset-layer concepts to {len(touched)} domains: {sorted(touched)}")


if __name__ == "__main__":
    main()
