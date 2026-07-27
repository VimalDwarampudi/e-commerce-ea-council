---
type: Example
title: Real-Time Inventory Event Bus Design
description: Request: design the event-driven inventory sync needed to unblock BOPIS (see Omnichannel example).
tags: [integration-architecture, example]
timestamp: 2026-07-23T00:00:00Z
---

# Real-Time Inventory Event Bus Design

Request: design the event-driven inventory sync needed to unblock BOPIS (see Omnichannel example).

Recommendation: WMS and store inventory systems each publish inventory-changed events to the shared bus; a unified inventory availability service (per Fulfillment's ownership principle) consumes both streams and serves reads to Order Management, Search, and Omnichannel. This avoids point-to-point sync between WMS and every consumer, per the point-to-point policy above.
