---
type: Metric
title: peak-load-capacity-headroom
description: Validated headroom between current auto-scaled capacity and the peak traffic model, per the design-for-peak-not-average principle.
tags: [technology-infrastructure, metric, placeholder]
timestamp: 2026-07-24T00:00:00Z
status: PLACEHOLDER
---

# peak-load-capacity-headroom

**Definition:** `(load-tested max sustained throughput - modeled peak traffic) / modeled peak traffic`

**Target (placeholder):** maintain positive headroom (e.g. >=20%) confirmed by an actual load test before each peak season — not inferred from auto-scaling configuration alone, per the mandatory peak-load-testing policy.

> **PLACEHOLDER — sample only.** This concept illustrates the shape an asset concept should take once a live source system is connected (see `CLAUDE.md` "Data Sources"). Field names, endpoint paths, and metric values below are representative, not verified against a real system. Replace the body with the actual schema/contract/metric definition and remove `status: PLACEHOLDER` from the frontmatter when done.
