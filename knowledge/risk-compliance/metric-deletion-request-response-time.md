---
type: Metric
title: deletion-request-response-time
description: Time to fulfill a verified consumer data deletion/access request, measured against the statutory window per the mandatory policy of the same domain.
tags: [risk-compliance, metric, placeholder]
timestamp: 2026-07-24T00:00:00Z
status: PLACEHOLDER
---

# deletion-request-response-time

**Definition:** `timestamp(request fulfilled across all systems, including backups/analytics copies) - timestamp(request verified)`

**Target (placeholder):** must stay under the statutory window (varies by jurisdiction — GDPR and CCPA windows differ); track the actual measured time, not just a target, since the underlying architecture question (can every system holding customer data actually delete on demand?) is what this metric tests.

> **PLACEHOLDER — sample only.** This concept illustrates the shape an asset concept should take once a live source system is connected (see `CLAUDE.md` "Data Sources"). Field names, endpoint paths, and metric values below are representative, not verified against a real system. Replace the body with the actual schema/contract/metric definition and remove `status: PLACEHOLDER` from the frontmatter when done.
