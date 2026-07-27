---
type: Principle
title: Event-Driven for Cross-Channel Consistency
description: Anything requiring near-real-time consistency across channels (inventory, order status, pricing) should be event-driven (pub/sub) rather than batch or point-to-point polling.
tags: [integration-architecture, principle]
timestamp: 2026-07-23T00:00:00Z
---

# Event-Driven for Cross-Channel Consistency

Anything requiring near-real-time consistency across channels (inventory, order status, pricing) should be event-driven (pub/sub) rather than batch or point-to-point polling. Batch sync is acceptable only for data that genuinely tolerates staleness.
