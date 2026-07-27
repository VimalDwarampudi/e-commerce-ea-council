---
type: Table
title: orders
description: System-of-record order header and lifecycle state; fulfillment splits reference this, never replace it.
tags: [order-management, table, placeholder]
timestamp: 2026-07-24T00:00:00Z
status: PLACEHOLDER
---

# orders

**Owning system:** OMS

| Field | Type | Notes |
|---|---|---|
| order_id | string, PK | |
| customer_identity_id | string, FK | |
| status | enum(placed, allocated, picking, shipped, delivered, cancelled, returned) | Every transition logged — see order-state-transitions-are-auditable principle |
| fulfillment_legs | jsonb array | One entry per split fulfillment source (warehouse, store) |
| placed_at, updated_at | timestamp | |

> **PLACEHOLDER — sample only.** This concept illustrates the shape an asset concept should take once a live source system is connected (see `CLAUDE.md` "Data Sources"). Field names, endpoint paths, and metric values below are representative, not verified against a real system. Replace the body with the actual schema/contract/metric definition and remove `status: PLACEHOLDER` from the frontmatter when done.
