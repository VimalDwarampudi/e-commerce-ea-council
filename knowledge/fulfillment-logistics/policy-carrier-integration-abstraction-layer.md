---
type: Policy
title: Carrier Integration Abstraction Layer
description: New carrier integrations must go through a shared carrier-abstraction service (rate shopping, label generation, tracking webhook normalization), not point-to-point integration per carrier per consuming system.
tags: [fulfillment-logistics, policy]
timestamp: 2026-07-23T00:00:00Z
mandatory: false
---

# Carrier Integration Abstraction Layer

[RECOMMENDED]

New carrier integrations must go through a shared carrier-abstraction service (rate shopping, label generation, tracking webhook normalization), not point-to-point integration per carrier per consuming system. This is an Integration Architecture-owned pattern that Fulfillment & Logistics must use, not bypass for speed.
