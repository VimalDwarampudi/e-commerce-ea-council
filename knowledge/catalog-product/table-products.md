---
type: Table
title: products
description: Core product record owned by the PIM; every other system's product view is a projection of this table.
tags: [catalog-product, table, placeholder]
timestamp: 2026-07-24T00:00:00Z
status: PLACEHOLDER
---

# products

**Owning system:** PIM (placeholder: e.g. Salsify, Akeneo, or in-house)

| Field | Type | Notes |
|---|---|---|
| sku | string, PK | Stock keeping unit, immutable |
| title | string | |
| description | text | |
| category_id | string, FK -> categories.id | Enforces the taxonomy contract (see `policy-taxonomy-is-a-contract` principle) |
| price | decimal | Base price; channel/region overrides live in a separate pricing table, not here |
| status | enum(active, discontinued, seasonal) | |
| compliance_attributes | jsonb | Country of origin, safety certs — added per the marketplace-onboarding example |
| updated_at | timestamp | |

> **PLACEHOLDER — sample only.** This concept illustrates the shape an asset concept should take once a live source system is connected (see `CLAUDE.md` "Data Sources"). Field names, endpoint paths, and metric values below are representative, not verified against a real system. Replace the body with the actual schema/contract/metric definition and remove `status: PLACEHOLDER` from the frontmatter when done.
