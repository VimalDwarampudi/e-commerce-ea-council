---
type: API
title: pim-export-api
description: The PIM's published contract for downstream consumers (storefront, search index, marketplace feeds, store systems).
tags: [catalog-product, api, placeholder]
timestamp: 2026-07-24T00:00:00Z
status: PLACEHOLDER
---

# pim-export-api

**Contract:** REST, versioned (`/v2/products`)

`GET /v2/products/{sku}` — full product record
`GET /v2/products?category={id}&updated_since={ts}` — incremental sync
`POST /v2/products/{sku}/compliance-attributes` — used by the marketplace-onboarding flow

**Consumers:** Search & Discovery index pipeline, digital storefront, marketplace feed generator, store systems (via Omnichannel's inventory service). This is the only sanctioned path per the PIM-as-system-of-record policy — no consumer should read the PIM's underlying database directly.

> **PLACEHOLDER — sample only.** This concept illustrates the shape an asset concept should take once a live source system is connected (see `CLAUDE.md` "Data Sources"). Field names, endpoint paths, and metric values below are representative, not verified against a real system. Replace the body with the actual schema/contract/metric definition and remove `status: PLACEHOLDER` from the frontmatter when done.
