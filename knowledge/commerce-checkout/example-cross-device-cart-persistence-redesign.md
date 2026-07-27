---
type: Example
title: Cross-Device Cart Persistence Redesign
description: Request: customers report losing cart contents when switching from mobile app to desktop web.
tags: [commerce-checkout, example]
timestamp: 2026-07-23T00:00:00Z
---

# Cross-Device Cart Persistence Redesign

Request: customers report losing cart contents when switching from mobile app to desktop web.

Root cause: cart is currently session-scoped per device, not identity-scoped.

Recommendation: Standard impact. Move cart ownership to customer identity (authenticated or persistent guest token), synced server-side. Integration Architecture must confirm the identity service can support this without introducing checkout-path latency — flag as a dependency, do not build in isolation.
