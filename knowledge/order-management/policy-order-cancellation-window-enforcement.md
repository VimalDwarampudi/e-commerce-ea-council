---
type: Policy
title: Order Cancellation Window Enforcement
description: Order cancellation/modification eligibility rules (e.
tags: [order-management, policy]
timestamp: 2026-07-23T00:00:00Z
mandatory: false
---

# Order Cancellation Window Enforcement

[RECOMMENDED]

Order cancellation/modification eligibility rules (e.g. cannot cancel after fulfillment picks the item) must be enforced server-side in the OMS, not merely hidden in the UI. UI-only enforcement is trivially bypassed and creates fulfillment exceptions.
