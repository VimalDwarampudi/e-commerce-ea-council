---
type: Table
title: carts
description: Cart state, identity-scoped per the cross-device persistence principle.
tags: [commerce-checkout, table, placeholder]
timestamp: 2026-07-24T00:00:00Z
status: PLACEHOLDER
---

# carts

**Owning system:** cart service

| Field | Type | Notes |
|---|---|---|
| cart_id | string, PK | |
| customer_identity_id | string, FK -> data-ai customer identity graph | Not device- or session-scoped |
| line_items | jsonb | sku, qty, applied_promo_id per line |
| channel_origin | enum(web, app, store) | For channel-parity reporting, not for splitting cart ownership |
| updated_at | timestamp | |
| expires_at | timestamp | Soft expiry; see cross-device persistence principle for why this must be long enough to survive a channel switch |

> **PLACEHOLDER — sample only.** This concept illustrates the shape an asset concept should take once a live source system is connected (see `CLAUDE.md` "Data Sources"). Field names, endpoint paths, and metric values below are representative, not verified against a real system. Replace the body with the actual schema/contract/metric definition and remove `status: PLACEHOLDER` from the frontmatter when done.
