---
type: API
title: oms-status-api
description: The OMS's published contract for order status, consumed by every channel per the single-system-of-record policy.
tags: [order-management, api, placeholder]
timestamp: 2026-07-24T00:00:00Z
status: PLACEHOLDER
---

# oms-status-api

`GET /v1/orders/{order_id}` — current status + fulfillment legs
`GET /v1/orders/{order_id}/history` — full auditable transition log
`POST /v1/orders/{order_id}/cancel` — server-side enforcement of the cancellation-window policy

**Consumers:** digital storefront, store POS, customer service tools, notification system. No consumer may cache order status as its own source of truth beyond a short TTL.

> **PLACEHOLDER — sample only.** This concept illustrates the shape an asset concept should take once a live source system is connected (see `CLAUDE.md` "Data Sources"). Field names, endpoint paths, and metric values below are representative, not verified against a real system. Replace the body with the actual schema/contract/metric definition and remove `status: PLACEHOLDER` from the frontmatter when done.
