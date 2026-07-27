---
type: Policy
title: Webhook Idempotency Required
description: Any system consuming carrier or PSP webhooks (tracking updates, payment status) must implement idempotent processing, since webhook redelivery on transient failure is standard behavior for these providers and duplicate processing causes order/inventory corruption.
tags: [integration-architecture, policy]
timestamp: 2026-07-23T00:00:00Z
mandatory: false
---

# Webhook Idempotency Required

[RECOMMENDED]

Any system consuming carrier or PSP webhooks (tracking updates, payment status) must implement idempotent processing, since webhook redelivery on transient failure is standard behavior for these providers and duplicate processing causes order/inventory corruption.
