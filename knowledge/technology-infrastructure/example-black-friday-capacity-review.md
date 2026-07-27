---
type: Example
title: Black Friday Capacity Review
description: Request: annual pre-peak-season infrastructure review.
tags: [technology-infrastructure, example]
timestamp: 2026-07-23T00:00:00Z
---

# Black Friday Capacity Review

Request: annual pre-peak-season infrastructure review.

Finding: checkout service auto-scales correctly under load test, but the tax-calculation third-party API (synchronous call in the checkout path, per Commerce & Checkout's latency principle) has no documented rate limit or fallback behavior under load.

Recommendation: Major impact given the timing. Require a fallback (cached/estimated tax with async reconciliation) be built before peak season, since a synchronous external dependency with unknown limits is a checkout-wide single point of failure.
