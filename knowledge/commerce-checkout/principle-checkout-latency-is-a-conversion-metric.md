---
type: Principle
title: Checkout Latency Is a Conversion Metric
description: Every added step or synchronous external call in the checkout flow (tax calculation, fraud check, promo validation) must be justified against its conversion impact.
tags: [commerce-checkout, principle]
timestamp: 2026-07-23T00:00:00Z
---

# Checkout Latency Is a Conversion Metric

Every added step or synchronous external call in the checkout flow (tax calculation, fraud check, promo validation) must be justified against its conversion impact. Default to asynchronous/optimistic patterns; synchronous blocking calls on the critical checkout path require explicit sign-off.
