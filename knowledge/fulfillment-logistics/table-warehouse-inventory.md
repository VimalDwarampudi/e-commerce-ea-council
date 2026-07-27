---
type: Table
title: warehouse-inventory
description: Warehouse-side inventory of record, feeding the unified inventory availability service alongside store-inventory.
tags: [fulfillment-logistics, table, placeholder]
timestamp: 2026-07-24T00:00:00Z
status: PLACEHOLDER
---

# warehouse-inventory

**Owning system:** WMS

| Field | Type | Notes |
|---|---|---|
| warehouse_id | string, FK | |
| sku | string, FK -> catalog-product.products | |
| on_hand_qty, allocated_qty | int | |
| last_synced_at | timestamp | Event-driven per the reference architecture, not batch |

> **PLACEHOLDER — sample only.** This concept illustrates the shape an asset concept should take once a live source system is connected (see `CLAUDE.md` "Data Sources"). Field names, endpoint paths, and metric values below are representative, not verified against a real system. Replace the body with the actual schema/contract/metric definition and remove `status: PLACEHOLDER` from the frontmatter when done.
