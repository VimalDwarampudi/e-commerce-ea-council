---
type: Guideline
title: Split-Fulfillment Orchestration Pattern
description: When an order splits across fulfillment sources, orchestrate via a saga pattern with explicit compensation logic (e.
tags: [order-management, guideline]
timestamp: 2026-07-23T00:00:00Z
---

# Split-Fulfillment Orchestration Pattern

When an order splits across fulfillment sources, orchestrate via a saga pattern with explicit compensation logic (e.g. partial refund if one leg fails) rather than a single distributed transaction — order fulfillment spans systems (OMS, WMS, store POS, carriers) that cannot participate in a shared transaction.
