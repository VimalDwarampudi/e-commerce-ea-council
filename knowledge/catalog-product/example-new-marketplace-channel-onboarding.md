---
type: Example
title: New Marketplace Channel Onboarding
description: Request: onboard a new third-party marketplace channel.
tags: [catalog-product, example]
timestamp: 2026-07-23T00:00:00Z
---

# New Marketplace Channel Onboarding

Request: onboard a new third-party marketplace channel.

Assessment: existing PIM export supports 80% of the required attribute schema. Gap: marketplace-specific compliance attributes (country of origin, safety certifications) not currently modeled in PIM.

Recommendation: extend the PIM schema rather than maintain a marketplace-specific side table — a side table would violate the single-source-of-record principle and create drift risk. Flag to Risk & Compliance since compliance attributes are involved.
