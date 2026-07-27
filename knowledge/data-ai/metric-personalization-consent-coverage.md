---
type: Metric
title: personalization-consent-coverage
description: Share of identities used in a personalization surface that have a valid, current consent record — the concrete check for the consent-tracking principle.
tags: [data-ai, metric, placeholder]
timestamp: 2026-07-24T00:00:00Z
status: PLACEHOLDER
---

# personalization-consent-coverage

**Definition:** `count(identities shown personalized content WITH valid consent_record) / count(all identities shown personalized content)`

**Target (placeholder):** should be effectively 100% by design (personalization should be gated on consent, not audited after the fact) — a non-100% reading here is itself a policy violation worth escalating, not just a metric to trend.

> **PLACEHOLDER — sample only.** This concept illustrates the shape an asset concept should take once a live source system is connected (see `CLAUDE.md` "Data Sources"). Field names, endpoint paths, and metric values below are representative, not verified against a real system. Replace the body with the actual schema/contract/metric definition and remove `status: PLACEHOLDER` from the frontmatter when done.
