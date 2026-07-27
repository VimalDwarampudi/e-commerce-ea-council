---
type: Metric
title: integration-error-rate
description: Failed/retried message rate across the event bus and gateway; a fragility signal for the point-to-point-integration-debt principle.
tags: [integration-architecture, metric, placeholder]
timestamp: 2026-07-24T00:00:00Z
status: PLACEHOLDER
---

# integration-error-rate

**Definition:** `count(failed or retried messages) / count(all messages)`, segmented by integration.

**Target (placeholder):** a sustained rise for a single integration is a stronger signal than the aggregate — investigate per-integration, not just in the rolled-up number.

> **PLACEHOLDER — sample only.** This concept illustrates the shape an asset concept should take once a live source system is connected (see `CLAUDE.md` "Data Sources"). Field names, endpoint paths, and metric values below are representative, not verified against a real system. Replace the body with the actual schema/contract/metric definition and remove `status: PLACEHOLDER` from the frontmatter when done.
