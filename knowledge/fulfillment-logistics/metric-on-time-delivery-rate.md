---
type: Metric
title: on-time-delivery-rate
description: Share of shipments delivered by the promised date; primary carrier and fulfillment health metric.
tags: [fulfillment-logistics, metric, placeholder]
timestamp: 2026-07-24T00:00:00Z
status: PLACEHOLDER
---

# on-time-delivery-rate

**Definition:** `count(shipments delivered <= promised_date) / count(all shipments)`, segmented by carrier and fulfillment source (warehouse vs. ship-from-store).

**Target (placeholder):** track per-carrier to catch a single underperforming carrier before it drags the aggregate down — feeds carrier-abstraction-layer vendor reviews.

> **PLACEHOLDER — sample only.** This concept illustrates the shape an asset concept should take once a live source system is connected (see `CLAUDE.md` "Data Sources"). Field names, endpoint paths, and metric values below are representative, not verified against a real system. Replace the body with the actual schema/contract/metric definition and remove `status: PLACEHOLDER` from the frontmatter when done.
