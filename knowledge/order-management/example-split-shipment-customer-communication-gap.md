---
type: Example
title: Split-Shipment Customer Communication Gap
description: Request: customers confused when an order arrives in multiple packages with no warning.
tags: [order-management, example]
timestamp: 2026-07-23T00:00:00Z
---

# Split-Shipment Customer Communication Gap

Request: customers confused when an order arrives in multiple packages with no warning.

Finding: OMS correctly tracks the split internally but the notification system only fires on the original order, not per-shipment.

Recommendation: Minor-to-Standard impact depending on volume. Extend notification triggers to per-shipment events sourced from the OMS lifecycle log (per the auditable-transitions principle) rather than building a parallel notification state machine.
