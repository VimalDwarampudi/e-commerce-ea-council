---
type: Principle
title: Index Freshness Matches Business Criticality
description: Inventory-sensitive attributes (in-stock status, price) in the search index must be near-real-time.
tags: [search-discovery, principle]
timestamp: 2026-07-23T00:00:00Z
---

# Index Freshness Matches Business Criticality

Inventory-sensitive attributes (in-stock status, price) in the search index must be near-real-time. Descriptive attributes (title, long description) can tolerate batch/eventual sync. Do not apply one freshness SLA uniformly across all indexed fields — it either over-invests in infrastructure or under-serves customers.
