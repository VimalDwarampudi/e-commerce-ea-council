---
type: Example
title: Legacy Store Inventory System Rationalization
description: Request: assess whether to keep or replace the 12-year-old in-store inventory application.
tags: [application-architecture, example]
timestamp: 2026-07-23T00:00:00Z
---

# Legacy Store Inventory System Rationalization

Request: assess whether to keep or replace the 12-year-old in-store inventory application.

Scoring: Business Fit = H (still core to store operations), Technical Fit = L (no API, batch-only integration, blocking the Omnichannel real-time visibility requirement).

Recommendation: Major impact — re-platform, not decommission. This is the actual root cause of the BOPIS launch blocker identified by Omnichannel & Store Systems; sequence this work ahead of BOPIS, not in parallel.
