---
type: Metric
title: bopis-pickup-fulfillment-rate
description: Share of BOPIS orders successfully picked up within the promised window vs. cancelled/no-show — the concrete measure of whether the soft-hold TTL design (see Omnichannel's worked example) is actually working.
tags: [omnichannel-store, metric, placeholder]
timestamp: 2026-07-24T00:00:00Z
status: PLACEHOLDER
---

# bopis-pickup-fulfillment-rate

**Definition:** `count(BOPIS orders picked up within window) / count(BOPIS orders placed)`

**Target (placeholder):** track alongside no-show rate; a rising no-show rate combined with inventory lockup complaints is the specific failure mode Red Team flagged in the BOPIS challenge example — this metric is what would surface it.

> **PLACEHOLDER — sample only.** This concept illustrates the shape an asset concept should take once a live source system is connected (see `CLAUDE.md` "Data Sources"). Field names, endpoint paths, and metric values below are representative, not verified against a real system. Replace the body with the actual schema/contract/metric definition and remove `status: PLACEHOLDER` from the frontmatter when done.
