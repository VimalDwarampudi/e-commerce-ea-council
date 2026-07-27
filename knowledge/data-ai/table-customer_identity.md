---
type: Table
title: customer_identity
description: The unified identity graph resolving store, digital, and loyalty activity to one customer — referenced by carts, orders, and personalization.
tags: [data-ai, table, placeholder]
timestamp: 2026-07-24T00:00:00Z
status: PLACEHOLDER
---

# customer_identity

**Owning system:** Customer Data Platform (placeholder)

| Field | Type | Notes |
|---|---|---|
| identity_id | string, PK | |
| known_identifiers | jsonb | email, loyalty_id, device_ids — resolved, not raw PII duplicated across systems |
| consent_record_id | string, FK -> consent table | Required before this identity's data is used for personalization, per the PII-classification and consent-tracking policies |
| created_at | timestamp | |

> **PLACEHOLDER — sample only.** This concept illustrates the shape an asset concept should take once a live source system is connected (see `CLAUDE.md` "Data Sources"). Field names, endpoint paths, and metric values below are representative, not verified against a real system. Replace the body with the actual schema/contract/metric definition and remove `status: PLACEHOLDER` from the frontmatter when done.
