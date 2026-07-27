---
type: Metric
title: zero-result-rate
description: Share of search queries returning no results; a leading indicator of catalog or taxonomy gaps per this domain's monitoring policy.
tags: [search-discovery, metric, placeholder]
timestamp: 2026-07-24T00:00:00Z
status: PLACEHOLDER
---

# zero-result-rate

**Definition:** `count(queries WHERE result_count = 0) / count(all queries)`, rolled up daily.

**Target (placeholder):** < 2% overall; < 5% for any single top-20 category.

**Owning system:** search platform analytics (placeholder: e.g. Algolia Insights, Elastic dashboards).

**Consumed by:** Catalog & Product Information (taxonomy gap signal), Data & AI (query understanding gaps).

> **PLACEHOLDER — sample only.** This concept illustrates the shape an asset concept should take once a live source system is connected (see `CLAUDE.md` "Data Sources"). Field names, endpoint paths, and metric values below are representative, not verified against a real system. Replace the body with the actual schema/contract/metric definition and remove `status: PLACEHOLDER` from the frontmatter when done.
