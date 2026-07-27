---
type: Metric
title: chargeback-rate
description: Share of transactions disputed as chargebacks; a fraud and PSP-relationship health signal.
tags: [payments, metric, placeholder]
timestamp: 2026-07-24T00:00:00Z
status: PLACEHOLDER
---

# chargeback-rate

**Definition:** `count(transactions with status=chargeback) / count(captured transactions)`, rolled up monthly.

**Target (placeholder):** most card networks flag monitoring programs above ~0.9-1%; treat approaching that threshold as a Risk & Compliance escalation trigger, not just a Payments metric to watch quietly.

> **PLACEHOLDER — sample only.** This concept illustrates the shape an asset concept should take once a live source system is connected (see `CLAUDE.md` "Data Sources"). Field names, endpoint paths, and metric values below are representative, not verified against a real system. Replace the body with the actual schema/contract/metric definition and remove `status: PLACEHOLDER` from the frontmatter when done.
