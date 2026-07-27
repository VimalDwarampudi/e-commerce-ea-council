---
type: Table
title: store-inventory
description: Per-location inventory count, feeding the unified inventory availability service alongside WMS per the reference architecture.
tags: [omnichannel-store, table, placeholder]
timestamp: 2026-07-24T00:00:00Z
status: PLACEHOLDER
---

# store-inventory

**Owning system:** store inventory system

| Field | Type | Notes |
|---|---|---|
| store_id | string, FK | |
| sku | string, FK -> catalog-product.products | |
| on_hand_qty | int | |
| soft_hold_qty | int | BOPIS reservations per the soft-hold TTL pattern |
| last_synced_at | timestamp | Must be near-real-time per the inventory-visibility-is-real-time-or-its-wrong principle — flag if this drifts beyond a few minutes |

> **PLACEHOLDER — sample only.** This concept illustrates the shape an asset concept should take once a live source system is connected (see `CLAUDE.md` "Data Sources"). Field names, endpoint paths, and metric values below are representative, not verified against a real system. Replace the body with the actual schema/contract/metric definition and remove `status: PLACEHOLDER` from the frontmatter when done.
